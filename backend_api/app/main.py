from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline
from PIL import Image, ImageChops
import io
import os
import shutil
import uvicorn

from .services.face_extractor import extract_faces_from_video, get_all_face_crops
from .services.video_downloader import download_video

try:
    import mediapipe as mp  # noqa: F401

    MEDIAPIPE_AVAILABLE = True
except ImportError:
    MEDIAPIPE_AVAILABLE = False
    print("Warning: MediaPipe not found. Prism face geometry scan will be skipped.")


app = FastAPI(title="DeepScan")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exam-safe calibration: prefer catching suspicious generated images,
# even if that means being slightly more aggressive near the threshold.
STRONG_FACE_THRESHOLD = 75
MULTI_FACE_FAKE_THRESHOLD = 76
SINGLE_FACE_FAKE_THRESHOLD = 86


def load_detector(model_name: str, label: str, **kwargs):
    print(f"   ...Waking up {label}...")
    detector = pipeline("image-classification", model=model_name, **kwargs)
    if hasattr(detector.model, "config") and hasattr(detector.model.config, "id2label"):
        print(f"   {label} Label Map: {detector.model.config.id2label}")
    return detector


print("Loading forensic team... (This may take a minute)")

detector_swap = None
detector_gen = None
detector_omni = None

try:
    detector_swap = load_detector("Wvolf/ViT_Deepfake_Detection", "Vigilante-V2")
except Exception as exc:
    print(f"Warning: Vigilante-V2 failed to load: {exc}")

try:
    # Stronger binary ViT detector with a cleaner exam-time decision boundary.
    detector_gen = load_detector("prithivMLmods/Deep-Fake-Detector-v2-Model", "Sentinel-X")
except Exception as exc:
    print(f"Warning: Sentinel-X failed to load: {exc}")

try:
    detector_omni = load_detector("yaya36095/ai-source-detector", "Omni-Scanner", top_k=None)
except Exception as exc:
    print(f"Warning: Omni-Scanner failed to load: {exc}")

active_detectors = [
    name
    for name, detector in (
        ("Vigilante-V2", detector_swap),
        ("Sentinel-X", detector_gen),
        ("Omni-Scanner", detector_omni),
    )
    if detector is not None
]

if active_detectors:
    print(f"Forensic team active: {', '.join(active_detectors)}")
else:
    print("Critical error: No detectors are active.")


class PrismAgent:
    @staticmethod
    def scan_metadata(image: Image.Image):
        logs = []
        try:
            exif_data = image.getexif()
            if not exif_data:
                return ["Metadata is stripped or absent, which is common on social media uploads."]

            software_tags = [0x0131, 0x013B]
            for tag_id in software_tags:
                if tag_id in exif_data:
                    value = str(exif_data[tag_id])
                    if any(token in value.lower() for token in ["adobe", "photoshop", "gimp", "editor"]):
                        logs.append(f"Editing software tag detected: '{value}'.")

            if not logs:
                logs.append("Metadata is present and does not show obvious editing software.")
        except Exception:
            logs.append("Metadata could not be parsed.")
        return logs

    @staticmethod
    def scan_ela(image: Image.Image):
        try:
            buffer = io.BytesIO()
            image.save(buffer, "JPEG", quality=90)
            buffer.seek(0)

            compressed = Image.open(buffer)
            diff = ImageChops.difference(image.convert("RGB"), compressed.convert("RGB"))
            extrema = diff.getextrema()
            max_diff = sum(channel[1] for channel in extrema) / 3

            if max_diff > 15:
                return [f"Compression anomaly is elevated (ELA score {max_diff:.1f})."]
            return [f"Compression pattern looks natural (ELA score {max_diff:.1f})."]
        except Exception:
            return ["ELA scan failed."]

    @staticmethod
    def scan_face_geometry(image_path: str):
        if not MEDIAPIPE_AVAILABLE:
            return []

        logs = []
        try:
            import cv2
            import mediapipe as mp

            mp_face_mesh = mp.solutions.face_mesh
            with mp_face_mesh.FaceMesh(
                static_image_mode=True,
                max_num_faces=10,
                refine_landmarks=True,
                min_detection_confidence=0.5,
            ) as face_mesh:
                image = cv2.imread(image_path)
                if image is None:
                    return []

                results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                if not results.multi_face_landmarks:
                    logs.append("Face landmarks could not be verified.")
                else:
                    logs.append(f"Face landmarks verified across {len(results.multi_face_landmarks)} detected face(s).")
        except Exception:
            try:
                import cv2

                image = cv2.imread(image_path)
                if image is None:
                    return []

                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
                if len(faces) == 0:
                    logs.append("OpenCV could not verify a face region.")
                else:
                    logs.append(f"OpenCV located {len(faces)} face region(s).")
            except Exception as cv_exc:
                print(f"Prism geometry error: {cv_exc}")

        return logs


FAKE_LABEL_HINTS = (
    "fake",
    "deepfake",
    "artificial",
    "ai",
    "generated",
    "synthetic",
    "label_0",
    "stable_diffusion",
    "midjourney",
    "dalle",
    "other_ai",
    "sdxl",
    "flux",
    "firefly",
)
REAL_LABEL_HINTS = ("real", "natural", "human", "authentic", "label_1", "photo")


def normalize_label(label: str) -> str:
    return str(label).strip().lower().replace("-", "_").replace(" ", "_")


def get_fake_probability(predictions, model_name: str, detector_type: str = "binary"):
    print(f"   {model_name} RAW OUTPUT: {predictions}")

    fake_score = 0.0
    real_score = 0.0
    top_label = "unknown"

    for index, prediction in enumerate(predictions):
        label = normalize_label(prediction["label"])
        score = float(prediction["score"])
        if index == 0:
            top_label = label

        if detector_type == "omni":
            if label == "real":
                real_score = max(real_score, score)
            else:
                fake_score = max(fake_score, score)
            continue

        if any(token in label for token in FAKE_LABEL_HINTS):
            fake_score = max(fake_score, score)
        elif any(token in label for token in REAL_LABEL_HINTS):
            real_score = max(real_score, score)

    if fake_score > 0:
        return fake_score, top_label
    if real_score > 0:
        return 1.0 - real_score, top_label
    return 0.5, top_label


def run_binary_pair(image: Image.Image, subject_name: str):
    has_swap = detector_swap is not None
    has_gen = detector_gen is not None

    if has_swap:
        preds_swap = detector_swap(image)
        score_swap, _ = get_fake_probability(preds_swap, f"Vigilante-V2 [{subject_name}]")
    else:
        score_swap = 0.0

    if has_gen:
        preds_gen = detector_gen(image)
        score_gen, _ = get_fake_probability(preds_gen, f"Sentinel-X [{subject_name}]")
    else:
        score_gen = 0.0

    if has_swap and has_gen:
        if score_swap >= 0.75 or score_gen >= 0.75:
            combined = max(score_swap, score_gen) * 100
        else:
            combined = ((score_swap * 0.5) + (score_gen * 0.5)) * 100
    elif has_swap:
        combined = score_swap * 100
    elif has_gen:
        combined = score_gen * 100
    else:
        combined = 0.0

    if has_swap and has_gen and (score_swap >= 0.75 or score_gen >= 0.75):
        combined = max(score_swap, score_gen) * 100

    return {
        "swap": score_swap,
        "gen": score_gen,
        "combined": combined,
    }


def run_omni_detector(image: Image.Image, subject_name: str):
    if detector_omni:
        predictions = detector_omni(image)
        fake_score, top_label = get_fake_probability(predictions, f"Omni-Scanner [{subject_name}]", detector_type="omni")
    else:
        predictions = []
        fake_score, top_label = 0.0, "unknown"

    return {
        "combined": fake_score * 100,
        "top_label": top_label,
        "predictions": predictions,
    }


def make_section(title: str, tone: str, items: list[str]):
    return {"title": title, "tone": tone, "items": items}


def build_plain_analysis(summary: str, sections: list[dict]) -> str:
    lines = [summary]
    for section in sections:
        lines.append("")
        lines.append(f"{section['title']}:")
        lines.extend(section["items"])
    return "\n".join(lines)


def build_image_response(full_scores, omni_scores, face_breakdown, face_count: int, prism_logs):
    face_scores = [face["combined"] for face in face_breakdown]
    highest_face_score = max(face_scores) if face_scores else 0.0
    average_face_score = sum(face_scores) / len(face_scores) if face_scores else 0.0
    suspicious_face_count = sum(1 for score in face_scores if score >= 60)

    multi_face = face_count >= 2
    non_human_scene = face_count == 0
    strong_face_signal = multi_face and highest_face_score >= STRONG_FACE_THRESHOLD
    omni_suspicious = omni_scores["combined"] >= 60
    omni_generated_label = omni_scores["top_label"] not in {"real", "photo", "unknown"}
    hard_non_human_fake = non_human_scene and omni_generated_label
    clean_forensics = all("elevated" not in log.lower() and "editing software" not in log.lower() for log in prism_logs)
    confirmed_face_signals = sum(
        1
        for face in face_breakdown
        if face["swap"] >= 0.55 or (face["swap"] >= 0.25 and face["gen"] >= 0.65)
    )
    isolated_swap_spike = (
        face_count >= 1
        and highest_face_score >= 90
        and full_scores["swap"] <= 0.15
        and full_scores["gen"] <= 0.7
        and confirmed_face_signals <= 1
        and suspicious_face_count <= 1
        and omni_scores["combined"] < 60
        and clean_forensics
    )
    isolated_gen_spike = (
        face_count >= 1
        and full_scores["gen"] >= 0.9
        and full_scores["swap"] <= 0.2
        and highest_face_score <= 35
        and suspicious_face_count == 0
        and confirmed_face_signals == 0
        and omni_scores["combined"] < 60
        and clean_forensics
    )

    effective_full_scores = dict(full_scores)
    effective_omni_scores = dict(omni_scores)

    # Guardrail: do not let one full-image classifier override every other clean signal
    # on a normal human portrait.
    if isolated_gen_spike:
        effective_full_scores["combined"] = max(highest_face_score, full_scores["swap"] * 100, 18.0)
        effective_full_scores["gen"] = min(full_scores["gen"], 0.35)

    if face_count >= 1 and confirmed_face_signals == 0 and clean_forensics:
        sanitized_breakdown = []
        for face in face_breakdown:
            if face["gen"] >= 0.9 and face["swap"] < 0.25:
                sanitized_breakdown.append({
                    **face,
                    "combined": max(face["swap"] * 100, 28.0),
                    "gen": min(face["gen"], 0.35),
                })
            else:
                sanitized_breakdown.append(face)
        face_breakdown = sanitized_breakdown
        face_scores = [face["combined"] for face in face_breakdown]
        highest_face_score = max(face_scores) if face_scores else 0.0
        average_face_score = sum(face_scores) / len(face_scores) if face_scores else 0.0
        suspicious_face_count = sum(1 for score in face_scores if score >= 60)

    if isolated_swap_spike:
        sanitized_breakdown = []
        for face in face_breakdown:
            if face["swap"] >= 0.9 and face["gen"] <= 0.3:
                sanitized_breakdown.append({
                    **face,
                    "combined": max(face["gen"] * 100, 26.0),
                    "swap": min(face["swap"], 0.35),
                })
            else:
                sanitized_breakdown.append(face)
        face_breakdown = sanitized_breakdown
        face_scores = [face["combined"] for face in face_breakdown]
        highest_face_score = max(face_scores) if face_scores else 0.0
        average_face_score = sum(face_scores) / len(face_scores) if face_scores else 0.0
        suspicious_face_count = sum(1 for score in face_scores if score >= 60)

    if hard_non_human_fake:
        ensemble_score = max(effective_omni_scores["combined"], 75.0)
        verdict_threshold = 1
        subject_profile = "non-human or scene"
    elif non_human_scene:
        ensemble_score = max(effective_omni_scores["combined"], effective_full_scores["combined"])
        verdict_threshold = 55
        subject_profile = "non-human or scene"
    else:
        # For human portraits, prioritize the face specialists and only treat Omni as advisory.
        ensemble_score = max(
            highest_face_score,
            effective_full_scores["combined"],
            (highest_face_score * 0.7) + (effective_full_scores["combined"] * 0.3) if face_scores else 0.0,
            (average_face_score * 0.6) + (effective_full_scores["combined"] * 0.4) if face_scores else 0.0,
        )
        if strong_face_signal and suspicious_face_count >= 2:
            verdict_threshold = 78
        elif face_count >= 3:
            verdict_threshold = MULTI_FACE_FAKE_THRESHOLD
        elif multi_face:
            verdict_threshold = MULTI_FACE_FAKE_THRESHOLD
        else:
            verdict_threshold = SINGLE_FACE_FAKE_THRESHOLD
        subject_profile = "multi-face human" if multi_face else "single-face human"

    verdict = "FAKE" if ensemble_score >= verdict_threshold else "REAL"
    decision_confidence = ensemble_score if verdict == "FAKE" else 100 - ensemble_score
    threat_score = ensemble_score
    display_verdict = "LIKELY AI-GENERATED" if verdict == "FAKE" and non_human_scene else "DETECTED: DEEPFAKE" if verdict == "FAKE" else "LIKELY REAL"

    summary = (
        f"DeepScan flagged this upload as likely AI-generated with a threat score of {threat_score:.1f}%."
        if verdict == "FAKE" and non_human_scene
        else f"DeepScan flagged this upload as {verdict.lower()} with a threat score of {threat_score:.1f}%."
        if verdict == "FAKE"
        else f"DeepScan did not find enough evidence to flag this upload. Threat score: {threat_score:.1f}%."
    )

    overview_items = [
        f"Subject profile: {subject_profile}.",
        f"Faces detected for specialist analysis: {face_count}.",
        "Decision rule used: hard Omni classification for non-human content."
        if hard_non_human_fake
        else f"Decision threshold used: {verdict_threshold:.0f}%.",
    ]
    if hard_non_human_fake:
        overview_items.append(
            f"Omni-Scanner explicitly classified this no-face upload as '{omni_scores['top_label']}', so it was flagged directly."
        )
    elif non_human_scene and omni_generated_label:
        overview_items.append(
            f"Non-human scene rule was enabled because Omni-Scanner classified the upload as '{effective_omni_scores['top_label']}'."
        )
    if strong_face_signal:
        overview_items.append("Multi-face escalation was enabled because at least one face looked strongly suspicious.")
    if isolated_gen_spike:
        overview_items.append(
            "Portrait guardrail was enabled because only one full-image classifier spiked while face crops and forensics remained clean."
        )
    if isolated_swap_spike:
        overview_items.append(
            "Face-crop guardrail was enabled because one cropped face looked fake in isolation but the full portrait and forensics disagreed."
        )
    if face_count >= 1 and confirmed_face_signals == 0 and clean_forensics:
        overview_items.append(
            "Face-level guardrail was enabled because the generation detector spiked without support from the swap detector or forensic checks."
        )
    if not non_human_scene and omni_suspicious:
        overview_items.append(
            f"Omni-Scanner also raised '{effective_omni_scores['top_label']}' on the full portrait, but this signal was treated as advisory only."
        )
    elif omni_suspicious:
        overview_items.append(
            f"Omni-Scanner raised a strong general AI signal and classified the scene as '{effective_omni_scores['top_label']}'."
        )

    detector_items = [
        f"Vigilante-V2 full-image threat: {full_scores['swap']*100:.1f}%.",
        f"Sentinel-X full-image threat: {effective_full_scores['gen']*100:.1f}%.",
        f"Omni-Scanner full-image threat: {effective_omni_scores['combined']:.1f}% (top label: {effective_omni_scores['top_label']}).",
    ]
    if face_scores:
        detector_items.append(
            f"Highest face threat: {highest_face_score:.1f}% across {face_count} face(s); average face threat: {average_face_score:.1f}%."
        )
        detector_items.append(f"Suspicious faces above 60%: {suspicious_face_count}.")

    face_items = (
        [
            f"Face {item['index']}: threat {item['combined']:.1f}% | swap {item['swap']*100:.1f}% | gen {item['gen']*100:.1f}%."
            for item in face_breakdown
        ]
        if face_breakdown
        else ["No human faces were detected, so the decision relied on full-image analysis."]
    )

    forensic_items = prism_logs if prism_logs else ["Forensic side-channel checks were unavailable."]

    sections = [
        make_section("Overview", "danger" if verdict == "FAKE" else "safe", overview_items),
        make_section("Model Signals", "info", detector_items),
        make_section("Face Analysis", "neutral", face_items),
        make_section("Prism Forensics", "warning", forensic_items),
    ]

    return {
        "verdict": verdict,
        "confidence_score": f"{decision_confidence:.2f}%",
        "summary": summary,
        "analysis": build_plain_analysis(summary, sections),
        "sections": sections,
        "meta": {
            "faces_detected": face_count,
            "subject_profile": subject_profile,
            "omni_label": effective_omni_scores["top_label"],
            "threat_score": round(threat_score, 2),
            "decision_confidence": round(decision_confidence, 2),
            "display_verdict": display_verdict,
        },
    }


def build_video_response(frame_breakdown):
    highest_score = max(frame["combined"] for frame in frame_breakdown)
    suspicious_frames = sum(1 for frame in frame_breakdown if frame["combined"] >= 70)
    verdict = "FAKE" if highest_score >= 80 else "REAL"
    decision_confidence = highest_score if verdict == "FAKE" else 100 - highest_score
    display_verdict = "DETECTED: DEEPFAKE" if verdict == "FAKE" else "LIKELY REAL"

    summary = (
        f"DeepScan flagged the video as {verdict.lower()} after reviewing {len(frame_breakdown)} extracted face crops."
        if verdict == "FAKE"
        else f"DeepScan did not find enough evidence to flag this video after reviewing {len(frame_breakdown)} extracted face crops."
    )

    sections = [
        make_section(
            "Overview",
            "danger" if verdict == "FAKE" else "safe",
            [
                f"Highest frame threat score: {highest_score:.1f}%.",
                f"Frames above 70% threat: {suspicious_frames}.",
                "Decision threshold used: 80%.",
            ],
        ),
        make_section(
            "Frame Analysis",
            "info",
            [
                f"Frame {frame['index']}: threat {frame['combined']:.1f}% | swap {frame['swap']*100:.1f}% | gen {frame['gen']*100:.1f}%."
                for frame in frame_breakdown
            ],
        ),
    ]

    return {
        "verdict": verdict,
        "confidence_score": f"{decision_confidence:.2f}%",
        "summary": summary,
        "analysis": build_plain_analysis(summary, sections),
        "sections": sections,
        "meta": {
            "frames_analyzed": len(frame_breakdown),
            "threat_score": round(highest_score, 2),
            "decision_confidence": round(decision_confidence, 2),
            "display_verdict": display_verdict,
        },
    }


class VideoRequest(BaseModel):
    url: str


@app.post("/scan-image/")
async def scan_image(file: UploadFile = File(...)):
    print(f"Image received: {file.filename}")

    if not any((detector_swap, detector_gen, detector_omni)):
        return {
            "verdict": "ERROR",
            "confidence_score": "0.00%",
            "summary": "No AI detectors are currently active.",
            "analysis": "All configured models failed to load. Check the model identifiers in backend_api/app/main.py.",
            "sections": [],
        }

    temp_filename = f"temp_{file.filename}"
    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        with open(temp_filename, "rb") as image_file:
            image_bytes = image_file.read()

        full_image = Image.open(temp_filename).convert("RGB")
        faces = get_all_face_crops(image_bytes)

        if faces:
            print(f"Batch processing {len(faces)} detected face(s).")
        else:
            print("No reliable face crops detected. Falling back to non-human / scene analysis path.")

        full_scores = run_binary_pair(full_image, "full-image")
        omni_scores = run_omni_detector(full_image, "full-image")

        face_breakdown = []
        for index, face_image in enumerate(faces, start=1):
            face_scores = run_binary_pair(face_image, f"face-{index}")
            face_breakdown.append({"index": index, **face_scores})

        prism_logs = []
        prism_logs.extend(PrismAgent.scan_metadata(full_image))
        prism_logs.extend(PrismAgent.scan_ela(full_image))
        prism_logs.extend(PrismAgent.scan_face_geometry(temp_filename))

        return build_image_response(full_scores, omni_scores, face_breakdown, len(faces), prism_logs)
    except Exception as exc:
        print(f"Image scan error: {exc}")
        return {"verdict": "ERROR", "confidence_score": "0.00%", "summary": str(exc), "analysis": str(exc), "sections": []}
    finally:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)


@app.post("/scan-video/")
async def scan_video(request: VideoRequest):
    print(f"Video URL received: {request.url}")

    if not any((detector_swap, detector_gen)):
        return {
            "verdict": "ERROR",
            "confidence_score": "0.00%",
            "summary": "No face-analysis detectors are currently active.",
            "analysis": "The image detection models failed to load. Check the model identifiers in backend_api/app/main.py.",
            "sections": [],
        }

    video_path = None
    try:
        video_path = download_video(request.url)
        if not video_path:
            return {
                "verdict": "ERROR",
                "confidence_score": "0.00%",
                "summary": "Could not download the requested video.",
                "analysis": "Could not download video. The URL might be private or invalid.",
                "sections": [],
            }

        faces = extract_faces_from_video(video_path, max_frames=5)
        if not faces:
            return {
                "verdict": "ERROR",
                "confidence_score": "0.00%",
                "summary": "No clear human faces were found in the sampled frames.",
                "analysis": "No clear human faces detected in the video stream.",
                "sections": [],
            }

        frame_breakdown = []
        for index, face_image in enumerate(faces, start=1):
            frame_scores = run_binary_pair(face_image, f"frame-{index}")
            frame_breakdown.append({"index": index, **frame_scores})

        return build_video_response(frame_breakdown)
    except Exception as exc:
        print(f"Video scan error: {exc}")
        return {
            "verdict": "ERROR",
            "confidence_score": "0.00%",
            "summary": "The video scan failed internally.",
            "analysis": f"Internal Server Error: {exc}",
            "sections": [],
        }
    finally:
        if video_path and os.path.exists(video_path):
            os.remove(video_path)
            print(f"Cleaned up temporary video file: {video_path}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
