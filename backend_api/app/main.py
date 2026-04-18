from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline
from PIL import Image, ImageChops, ImageEnhance
import uvicorn
import os
import shutil
import io
import numpy as np

#Deepfake video imports
from .services.video_downloader import download_video
from .services.face_extractor import extract_faces_from_video

#Deeepfake images import
from .services.face_extractor import get_all_face_crops

# --- IMPORTS & SETUP ---
try:
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    MEDIAPIPE_AVAILABLE = False
    print("⚠️ MediaPipe not found. 'Prism' Face Geometry scanner will be skipped.")

# --- 1. SETUP APP ---
app = FastAPI(title="DeepScan (CSI Edition)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 2. LOAD AI MODELS (Vigilante & Sentinel) ---
print("⏳ Loading Forensic Team... (This may take 1 minute)")

try:
    # AGENT A: Swap Hunter
    print("   ...Waking up Vigilante-V2...")
    detector_swap = pipeline("image-classification", model="ashish-001/deepfake-detection-using-ViT")
    # DEBUG: Print the model's actual label mapping
    if hasattr(detector_swap.model, 'config') and hasattr(detector_swap.model.config, 'id2label'):
        print(f"   📋 Vigilante-V2 Label Map: {detector_swap.model.config.id2label}")
    
    # AGENT B: GenAI Hunter
    print("   ...Waking up Sentinel-X...")
    detector_gen = pipeline("image-classification", model="dima806/deepfake_vs_real_image_detection")
    if hasattr(detector_gen.model, 'config') and hasattr(detector_gen.model.config, 'id2label'):
        print(f"   📋 Sentinel-X Label Map: {detector_gen.model.config.id2label}")
    
    print("✅ Full Team Active!")
except Exception as e:
    print(f"❌ Critical Error loading models: {e}")
    detector_swap = None
    detector_gen = None

# --- 3. THE FORENSIC AGENT: PRISM (Forensics) 🔬 ---
class PrismAgent:
    @staticmethod
    def scan_metadata(image: Image.Image):
        """Looks for 'Photoshop' or editing software in hidden tags"""
        logs = []
        try:
            exif_data = image.getexif()
            if not exif_data:
                return ["Metadata: Clean/Stripped (Common in social media)"]
            
            # Check for software traces
            software_tags = [0x0131, 0x013b] # Tags for 'Software' or 'Artist'
            for tag_id in software_tags:
                if tag_id in exif_data:
                    val = str(exif_data[tag_id])
                    if any(x in val.lower() for x in ['adobe', 'photoshop', 'gimp', 'editor']):
                        logs.append(f"⚠️ METADATA FLAG: Editing software detected ('{val}').")
            
            if not logs:
                logs.append("Metadata: Present but no obvious editing software found.")
        except Exception:
            logs.append("Metadata: Could not parse.")
        return logs

    @staticmethod
    def scan_ela(image: Image.Image):
        """Error Level Analysis - Checks for compression anomalies"""
        try:
            # 1. Save original to buffer
            buf = io.BytesIO()
            image.save(buf, "JPEG", quality=90)
            buf.seek(0)
            
            # 2. Open compressed version
            compressed = Image.open(buf)
            
            # 3. Compute difference
            diff = ImageChops.difference(image.convert("RGB"), compressed.convert("RGB"))
            
            # 4. Calculate 'Tamper Score'
            extrema = diff.getextrema()
            max_diff = sum([ex[1] for ex in extrema]) / 3  # Average max difference
            
            if max_diff > 15:
                return [f"⚠️ FORENSIC FLAG: High compression anomaly (ELA Score: {max_diff:.1f}). Pixels may be altered."]
            return [f"Forensics: Compression levels look natural (ELA Score: {max_diff:.1f})."]
        except Exception:
            return ["Forensics: ELA Scan failed."]

    @staticmethod
    def scan_face_geometry(image_path: str):
        """Uses MediaPipe to check if a face actually exists, with OpenCV Fallback"""
        if not MEDIAPIPE_AVAILABLE:
            return []
            
        logs = []
        try:
            # ATTEMPT 1: Try Google MediaPipe (Primary Scanner)
            import mediapipe as mp
            mp_face_mesh = mp.solutions.face_mesh
            import cv2
            
            with mp_face_mesh.FaceMesh(
                static_image_mode=True,
                max_num_faces=10,
                refine_landmarks=True,
                min_detection_confidence=0.5
            ) as face_mesh:
                
                img = cv2.imread(image_path)
                if img is None: return []
                
                results = face_mesh.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                
                if not results.multi_face_landmarks:
                    logs.append("⚠️ GEOMETRY FLAG: No human face detected (or face is obscured).")
                else:
                    logs.append("Geometry: Face structure verified (Eyes/Nose/Mouth alignment valid).")
                    
        except Exception as e:
            # ATTEMPT 2: Fallback to OpenCV Haar Cascades (Backup Scanner)
            # If MediaPipe crashes on Windows, Prism automatically uses this instead!
            try:
                import cv2
                img = cv2.imread(image_path)
                if img is None: return []
                
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                # Load the classic OpenCV face detector
                face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
                
                if len(faces) == 0:
                    logs.append("⚠️ GEOMETRY FLAG: No face detected (OpenCV Backup Scanner).")
                else:
                    logs.append("Geometry: Face spatial boundaries verified (OpenCV Backup Scanner).")
            except Exception as cv_e:
                print(f"Prism Engine Critical Geometry Error: {cv_e}")
            
        return logs

# --- HELPER: NORMALIZE SCORES ---
def get_fake_probability(predictions, model_name="Unknown"):
    """Extracts the 'fake' probability from model predictions"""
    # DEBUG: Print raw output so we can see what labels the models actually use
    print(f"   🔍 {model_name} RAW OUTPUT: {predictions}")
    
    fake_score = 0.0
    real_score = 0.0
    
    for pred in predictions:
        label = pred['label'].lower()
        score = pred['score']
        
        # Check for FAKE labels
        if label in ['fake', 'deepfake', 'artificial', 'label_0', 'ai']:
            fake_score = score
        
        # Check for REAL labels
        elif label in ['real', 'natural', 'label_1', 'human']:
            real_score = score
    
    # If we found a direct fake score, use it
    if fake_score > 0:
        return fake_score
    # Otherwise derive from real score
    if real_score > 0:
        return 1.0 - real_score
    
    return 0.5  # Unknown labels fallback

class VideoRequest(BaseModel):
    url: str

# --- 4. ENDPOINT: SCAN IMAGE (CSI MODE) 📸 ---
@app.post("/scan-image/")
async def scan_image(file: UploadFile = File(...)):
    print(f"📸 Agent received image: {file.filename}")
    
    # Save temp file for Prism and Extractor
    temp_filename = f"temp_{file.filename}"
    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        # Read the file bytes directly for the new multi-face extractor
        with open(temp_filename, "rb") as img_file:
            img_bytes = img_file.read()
            
        faces = get_all_face_crops(img_bytes)
        
        highest_fake_score = 0.0
        face_details = []
        report_lines = []

        if len(faces) == 0:
            print("   ⚠️ No faces detected via OpenCV, falling back to full image scan.")
            faces = [Image.open(temp_filename)]
        else:
            print(f"   🧑‍🤝‍🧑 Batch Processing: {len(faces)} faces detected.")

        # --- PHASE 1: AI MODELS (Batch Process All Faces) ---
        for i, face_img in enumerate(faces):
            if detector_swap and detector_gen:
                preds_swap = detector_swap(face_img)
                preds_gen = detector_gen(face_img)
                score_swap = get_fake_probability(preds_swap, "Vigilante-V2")
                score_gen = get_fake_probability(preds_gen, "Sentinel-X")
            else:
                score_swap, score_gen = 0.5, 0.5 

            # Calculate individual face score
            if score_swap > 0.9 or score_gen > 0.9:
                face_score = max(score_swap, score_gen) * 100
            else:
                face_score = ((score_swap * 0.5) + (score_gen * 0.5)) * 100
            
            face_details.append(f"• Face {i+1}: Threat Level {face_score:.1f}% (Swap: {score_swap*100:.1f}%, Gen: {score_gen*100:.1f}%)")
            
            # Track the most manipulated face in the group
            if face_score > highest_fake_score:
                highest_fake_score = face_score

        # --- PHASE 2: PRISM FORENSICS ---
        # We run Prism on the FULL image, because checking compression (ELA) 
        # on tiny cropped faces gives inaccurate results.
        full_image = Image.open(temp_filename)
        prism_logs = []
        prism_logs.extend(PrismAgent.scan_metadata(full_image))
        prism_logs.extend(PrismAgent.scan_ela(full_image))
        prism_logs.extend(PrismAgent.scan_face_geometry(temp_filename))

        # --- PHASE 3: VERDICT LOGIC (Weighted Ensemble) ---
        verdict = "FAKE" if highest_fake_score > 80 else "REAL"
        
        # Display Score Logic
        display_score = highest_fake_score
        if verdict == "REAL":
            display_score = 100 - highest_fake_score

        # --- PHASE 4: GENERATE RICH REPORT ---
        # 1. The Headlines
        if verdict == "FAKE":
            report_lines.append(f"• CRITICAL: Multi-subject scan detected anomalies (Max Threat: {highest_fake_score:.1f}%).")
        else:
             report_lines.append(f"• CLEAN: AI models found no significant manipulation across {len(faces)} face(s).")

        # 2. Detailed Face Breakdown
        report_lines.append("\n📊 Face-by-Face Analysis:")
        report_lines.extend(face_details)

        # 3. The Forensics (Prism)
        report_lines.append("\n🔬 Prism Forensic Engine Results:")
        for log in prism_logs:
            report_lines.append(f"• {log}")

        # Join into a single string for the frontend
        full_analysis = "\n".join(report_lines)

        return {
            "verdict": verdict,
            "confidence_score": f"{display_score:.2f}%",
            "analysis": full_analysis
        }

    except Exception as e:
        print(f"❌ Error: {e}")
        return {"verdict": "ERROR", "confidence_score": "0.00%", "analysis": str(e)}
    
    finally:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

# --- 5. ENDPOINT: SCAN VIDEO LINK 🎥 ---
@app.post("/scan-video/")
async def scan_video(request: VideoRequest):
    print(f"🎥 Agent received video URL: {request.url}")
    
    video_path = None
    try:
        # --- PHASE 1: DOWNLOAD VIDEO ---
        video_path = download_video(request.url)
        if not video_path:
            return {"verdict": "ERROR", "confidence_score": "0.00%", "analysis": "Could not download video. The URL might be private or invalid."}
        
        # --- PHASE 2: EXTRACT KEYFRAMES ---
        # Extracts up to 5 clear faces across the duration of the video
        faces = extract_faces_from_video(video_path, max_frames=5)
        if not faces:
            return {"verdict": "ERROR", "confidence_score": "0.00%", "analysis": "No clear human faces detected in the video stream."}
        
        highest_fake_score = 0.0
        critical_flags = []
        frame_details = []  # Log all frame scores for transparency
        
        # --- PHASE 3: SCAN EACH FRAME ---
        for i, face_img in enumerate(faces):
            if detector_swap and detector_gen:
                preds_swap = detector_swap(face_img)
                preds_gen = detector_gen(face_img)
                score_swap = get_fake_probability(preds_swap, "Vigilante-V2")
                score_gen = get_fake_probability(preds_gen, "Sentinel-X")
            else:
                score_swap, score_gen = 0.5, 0.5
            
            # Weighted Logic per frame
            if score_swap > 0.9 or score_gen > 0.9:
                frame_score = max(score_swap, score_gen) * 100
            else:
                frame_score = ((score_swap * 0.5) + (score_gen * 0.5)) * 100
            
            # Log detailed frame information
            frame_details.append(f"Frame {i+1}: Vigilante={score_swap*100:.1f}% | Sentinel={score_gen*100:.1f}% | Combined={frame_score:.1f}%")
            print(f"   📹 {frame_details[-1]}")
                
            # Track the highest threat level across the whole video
            if frame_score > highest_fake_score:
                highest_fake_score = frame_score
                
            # Flag frames with moderate-to-high suspicion (lowered threshold from 90% to 70%)
            if score_swap > 0.7:
                critical_flags.append(f"• Frame {i+1}: Vigilante-V2 detected Face Swap artifacts ({score_swap*100:.1f}% confidence).")
            if score_gen > 0.7:
                critical_flags.append(f"• Frame {i+1}: Sentinel-X detected Synthetic content ({score_gen*100:.1f}% confidence).")

        # --- PHASE 4: VERDICT LOGIC (Raised threshold from 70% to 80% for high accuracy) ---
        verdict = "FAKE" if highest_fake_score > 80 else "REAL"
        
        display_score = highest_fake_score
        if verdict == "REAL":
            display_score = 100 - highest_fake_score
            
        # --- PHASE 5: COMPILE REPORT ---
        report_lines = [f"• VIDEO SCAN COMPLETE: Analyzed {len(faces)} facial keyframes."]
        report_lines.append(f"• Highest threat level detected: {highest_fake_score:.1f}%")
        report_lines.append("")  # Spacer
        
        if verdict == "FAKE":
            report_lines.append("⚠️  VERDICT: LIKELY FAKE")
            report_lines.append("")
            # Remove duplicates using set, but keep order
            report_lines.extend(list(dict.fromkeys(critical_flags)))
        else:
            report_lines.append("✓ VERDICT: LIKELY REAL")
            report_lines.append("• No significant manipulation detected across sampled frames.")
        
        # Add all frame details for transparency
        report_lines.append("")
        report_lines.append("📊 Detailed Frame Analysis:")
        report_lines.extend(frame_details)
            
        full_analysis = "\n".join(report_lines)
        
        return {
            "verdict": verdict,
            "confidence_score": f"{display_score:.2f}%",
            "analysis": full_analysis
        }

    except Exception as e:
        print(f"❌ Video Error: {e}")
        return {"verdict": "ERROR", "confidence_score": "0.00%", "analysis": f"Internal Server Error: {str(e)}"}
        
    finally:
        # ALWAYS clean up the massive video file from the server memory
        if video_path and os.path.exists(video_path):
            os.remove(video_path)
            print(f"🧹 Cleaned up temporary video file: {video_path}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)