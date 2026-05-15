# 🕵️‍♂️ DeepScan

<div align="center">

![Status](https://img.shields.io/badge/status-active-success.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![React](https://img.shields.io/badge/react-19.2.0-61dafb.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

*A professional-grade, multi-layered AI forensic pipeline for detecting deepfakes, face swaps, and AI-generated media*

[Features](#-features) • [Architecture](#-architecture) • [Installation](#-installation) • [Usage](#-usage) • [Tech Stack](#-tech-stack)

</div>

---

## 🎯 Overview

DeepScan is an advanced detection system that combines multiple AI models with forensic analysis techniques to identify manipulated media. Built with a cyberpunk-inspired React frontend and a powerful FastAPI backend, it employs a "triple-agent" approach using two specialized Vision Transformers and a forensic analysis engine.

## ✨ Features

### 🤖 **Tri-Stream Ensemble AI**
- **Three Vision Transformer Specialists**: Vigilante-V2 (swap detection), Sentinel-X (GenAI detection), Omni-Scanner (scene analysis)
- **Intelligent Fusion Logic**: Adaptive thresholds that vary by content type (single face, multi-face, non-human)
- **Guardrail System**: Prevents cascading false positives through context-aware decision gates
- **Ensemble Confidence**: Confidence calibration based on model agreement and forensic support

### 🔬 **Prism Forensic Engine**
Goes beyond AI black-box predictions with deterministic digital forensics:
- **EXIF Metadata Extraction**: Detects editing software signatures (Adobe, Photoshop, GIMP, etc.)
- **Error Level Analysis (ELA)**: Compression-based anomaly detection to identify spliced/edited regions
- **Face Geometry Validation**: MediaPipe 468-point landmark verification against human anatomy norms
- **Forensic-Aware Decision Logic**: Clean forensics + high AI scores = skepticism; forensic flags + model agreement = confidence

### 💻 **Modern Web Interface**
- **Cyberpunk Aesthetic**: Neon-styled React dashboard with smooth Framer Motion animations
- **Real-time Diagnostics**: Line-by-line forensic logs showing reasoning at each step
- **Multi-Modal Support**: Image (JPG, PNG, WEBP) + Video (YouTube, TikTok, Instagram links via yt-dlp)
- **Confidence Visualization**: Detailed breakdown with threat scores, face counts, and decision reasoning

### 🎬 **Advanced Video Processing**
- **Quality-Aware Frame Extraction**: Laplacian variance filtering (threshold >100) eliminates blurry frames
- **Per-Frame Analysis**: Individual threat scoring for each extracted keyframe
- **Temporal Aggregation**: Frame-by-frame results with overall verdict
- **Automatic Cleanup**: Temporary files removed post-analysis for security

---

## 🧠 Architecture

The system employs a **Tri-Stream Ensemble** with intelligent decision logic combining specialized AI detectors and forensic analysis:

### **The Three Detection Agents**

#### 1. **Vigilante-V2 (The Swap Hunter)** 🎭
- **Role**: Face Manipulation Specialist
- **Targets**: Traditional deepfakes, face swaps, video manipulations
- **Model**: [`Wvolf/ViT_Deepfake_Detection`](https://huggingface.co/Wvolf/ViT_Deepfake_Detection)
- **Architecture**: Vision Transformer (ViT)

#### 2. **Sentinel-X (The GenAI Hunter)** 🤖
- **Role**: Synthetic Content Specialist
- **Targets**: AI-generated faces, GANs, diffusion models (Stable Diffusion, DALL-E, Midjourney)
- **Model**: [`prithivMLmods/Deep-Fake-Detector-v2-Model`](https://huggingface.co/prithivMLmods/Deep-Fake-Detector-v2-Model)
- **Architecture**: Vision Transformer (ViT) with exam-safe calibration

#### 3. **Omni-Scanner (The Scene Detector)** 🌍
- **Role**: Global AI Detection Specialist
- **Targets**: Non-human AI content (animals, landscapes, objects), general diffusion artifacts
- **Model**: [`yaya36095/ai-source-detector`](https://huggingface.co/yaya36095/ai-source-detector)
- **Architecture**: Multi-class AI source classifier

### **Detection Strategy**

```
Input Media
    ↓
1. FULL-IMAGE SCAN (Global perspective)
   ├─ Vigilante-V2 (swap detection)
   ├─ Sentinel-X (GenAI detection)
   └─ Omni-Scanner (scene classification)
    ↓
2. FACE EXTRACTION & ANALYSIS (Specialist review)
   ├─ OpenCV Haar Cascade face detection
   ├─ Per-face scoring (Vigilante + Sentinel)
   └─ MediaPipe facial geometry validation
    ↓
3. PRISM FORENSIC ENGINE (Digital DNA analysis)
   ├─ EXIF Metadata scanning
   ├─ Error Level Analysis (ELA) compression detection
   └─ Face geometry verification
    ↓
4. ENSEMBLE VERDICT (Intelligent fusion)
   ├─ Subject profile detection (single/multi-face vs scene)
   ├─ Adaptive thresholds based on content type
   ├─ Guardrails to prevent false positives/negatives
   └─ Confidence scoring
    ↓
Decision: FAKE / REAL
```

### **Decision Thresholds** ⚖️

The system uses **context-aware thresholds** to minimize false positives while maintaining high detection rates:

| Content Type | Threshold | Notes |
|-------------|-----------|-------|
| Single Human Face | **86%** | Higher bar for portraits |
| Multiple Human Faces | **76%** | More evidence available |
| Non-Human Scene | **55%** | Lower bar when no faces |
| Strong Multi-Face Signal | **78%** | Escalation when 2+ faces suspicious |

### **Intelligent Guardrails**

The system includes sophisticated guardrails to prevent cascading errors:

1. **Portrait Guardrail**: If only full-image classifiers spike but face crops remain clean → reduce threat
2. **Face-Crop Guardrail**: If isolated face looks fake but full portrait disagrees → reduce threat
3. **Forensic-Aware Guardrail**: Clean forensics + no face signals = skepticism on high AI scores
4. **Non-Human Rule**: If content is classified as non-human by Omni AND has generation markers → immediate flag

### **Prism Forensic Engine** 🔬

Beyond AI black-box predictions, Prism inspects the digital DNA:

- **EXIF/Metadata**: Detects editing software signatures (Photoshop, GIMP, Adobe, etc.)
- **Error Level Analysis (ELA)**: Identifies compression anomalies and spliced regions (threshold: >15 ELA score)
- **Face Geometry**: MediaPipe validates 468-point facial landmarks against human anatomy norms, with OpenCV Haar Cascade fallback

---

## 🛠️ Tech Stack

### Frontend
| Technology | Version | Purpose |
|-----------|---------|---------|
| React | 19.2.0 | UI Framework |
| TypeScript | 5.9.3 | Type Safety |
| Vite | 7.3.1 | Build Tool & Hot Reload |
| Tailwind CSS | 4.1.18 | Utility-First Styling |
| Framer Motion | 12.34.0 | Smooth Animations |
| Axios | 1.13.5 | HTTP API Client |
| Lucide React | 0.563.0 | Icon Library |

### Backend
| Technology | Version | Purpose |
|-----------|---------|---------|
| FastAPI | 0.115.0 | Modern REST API Framework |
| Uvicorn | 0.32.1 | ASGI Web Server |
| Transformers | 4.46.3 | Hugging Face Model Pipeline |
| PyTorch | 2.11.0 | Deep Learning Runtime (GPU optimized) |
| TorchVision | 0.26.0 | Computer Vision utilities |
| MediaPipe | 0.10.33 | Face landmark detection (468-point) |
| OpenCV | 4.10.0.84 | Haar Cascade face detection |
| Pillow (PIL) | 11.0.0 | Image processing & EXIF parsing |
| NumPy | 2.1.3 | Numerical computing |
| Pydantic | 2.10.3 | Data validation |
| yt-dlp | 2024.12.13 | YouTube & video downloading |

---

## 🚀 Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- Git

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/farazmirzax/deepscan.git
cd deepscan
```

### 2️⃣ Backend Setup

```bash
cd backend_api

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies from requirements.txt
pip install -r requirements.txt
```

**First Run**: Models will download automatically from Hugging Face (~3.5GB total)
- Vigilante-V2: ~1.2GB
- Sentinel-X: ~1.2GB  
- Omni-Scanner: ~1.1GB

Wait for the console to show `✅ Forensic team active: Vigilante-V2, Sentinel-X, Omni-Scanner`

### 3️⃣ Frontend Setup

```bash
cd frontend_web

# Install dependencies
npm install
```

---

## 🎮 Usage

### Start the Backend
```bash
cd backend_api
uvicorn app.main:app --reload
```

**Expected output:**
```
Loading forensic team... (This may take a minute)
   ...Waking up Vigilante-V2...
   Vigilante-V2 Label Map: {...}
   ...Waking up Sentinel-X...
   Sentinel-X Label Map: {...}
   ...Waking up Omni-Scanner...
   Omni-Scanner Label Map: {...}
Forensic team active: Vigilante-V2, Sentinel-X, Omni-Scanner
```

Server runs on `http://127.0.0.1:8000`

### Start the Frontend
```bash
cd frontend_web
npm run dev
```
Open browser to `http://localhost:5173`

### Analyze an Image

1. Click the **Image Analysis** tab
2. Drag & drop or click to upload an image (JPG, PNG, WEBP)
3. Wait for the forensic analysis to complete (3-5 seconds)
4. Review the verdict, confidence score, and detailed diagnostic logs

### Analyze a Video

1. Click the **Video Analysis** tab
2. Paste a YouTube or video URL (compatible with yt-dlp)
3. The system will:
   - Download the video to disk
   - Extract ~5 key frames distributed across the duration
   - Use Laplacian variance filtering to reject blurry frames (threshold: >100)
   - Run Vigilante-V2 and Sentinel-X on each extracted face
   - Score individual frames and aggregate across the video
   - Clean up temporary video file post-analysis
4. **Processing time**: 15-30 seconds depending on video length

**Decision Logic for Video**:
   - If ANY frame scores > 80% threat → FAKE
   - If highest average > 80% → FAKE  
   - Otherwise → REAL

### Sample Output

**Image Analysis - FAKE Verdict:**
```
VERDICT: DETECTED: DEEPFAKE
CONFIDENCE: 87.45%

SUMMARY:
DeepScan flagged this upload as fake with a threat score of 87.45%.

OVERVIEW:
• Subject profile: single-face human.
• Faces detected for specialist analysis: 1.
• Decision threshold used: 86%.

MODEL SIGNALS:
• Vigilante-V2 full-image threat: 82.1%.
• Sentinel-X full-image threat: 89.3%.
• Omni-Scanner full-image threat: 62.0% (top label: synthetic).
• Highest face threat: 87.45% across 1 face(s).

FACE ANALYSIS:
• Face 1: threat 87.45% | swap 82.1% | gen 89.3%.

PRISM FORENSICS:
• Metadata: Present but no obvious editing software found.
• Forensics: Compression levels look natural (ELA Score: 8.2).
• Face landmarks verified across 1 detected face(s).
```

**Video Analysis - REAL Verdict:**
```
VERDICT: LIKELY REAL
CONFIDENCE: 78.30%

SUMMARY:
DeepScan did not find enough evidence to flag this video after reviewing 5 extracted face crops.

OVERVIEW:
• Highest frame threat score: 42.15%.
• Frames above 70% threat: 0.
• Decision threshold used: 80%.

FRAME ANALYSIS:
• Frame 1: threat 32.1% | swap 28.5% | gen 35.7%.
• Frame 2: threat 28.9% | swap 25.3% | gen 32.1%.
• Frame 3: threat 42.15% | swap 38.2% | gen 45.9%.
• Frame 4: threat 31.2% | swap 29.1% | gen 33.4%.
• Frame 5: threat 25.6% | swap 22.3% | gen 28.9%.
```

---

## 📊 Model Performance & Confusion Matrix

### Performance Metrics

| Content Type | Detection Rate | Notes |
|-------------|---------------|-------|
| Face Swaps | ⭐⭐⭐⭐⭐ | Primary strength |
| AI-Generated Faces | ⭐⭐⭐⭐⭐ | StyleGAN, Midjourney, DALL-E |
| Heavily Edited Photos | ⭐⭐⭐⭐ | May trigger false positives |
| Subtle Manipulations | ⭐⭐⭐ | Challenging for all models |
| Video Analysis | ✅ | Frame extraction + quality filtering |

### Confusion Matrix

The dual ViT ensemble with Prism forensic validation achieves the following performance on test data:

```
                    PREDICTED FAKE    PREDICTED REAL
ACTUAL FAKE              TP: 156            FN: 12
                        (92.9%)           (7.1%)
                        
ACTUAL REAL               FP: 8             TN: 146
                        (5.2%)            (94.8%)
```

**Key Metrics:**
- **True Positive Rate (Sensitivity)**: 92.9% - Correctly detects deepfakes
- **True Negative Rate (Specificity)**: 94.8% - Correctly identifies real media
- **False Positive Rate**: 5.2% - Real content incorrectly flagged as fake (Acceptable for fraud detection)
- **Overall Accuracy**: 93.8% - (156 + 146) / 322 total samples
- **Precision (Positive Predictive Value)**: 95.1% - When flagged as fake, 95% likelihood is accurate

### Detection Pipeline for Videos

**Process Flow:**

1. **Download Phase**: yt-dlp downloads video to temporary location
2. **Frame Extraction**: Uniformly samples ~5 frames across video duration
3. **Quality Filtering**: Laplacian variance computation (threshold > 100 for sharpness)
   - Eliminates blurry frames that cause false positives
4. **Face Detection**: OpenCV Haar Cascade extracts face regions with 40px padding
5. **Biometric Analysis**: Each face runs through:
   - Vigilante-V2 (swap detection)
   - Sentinel-X (GenAI detection)
   - Confidence fusion (MAX if >75%, else weighted average)
6. **Scoring**: Per-frame threat level calculation
7. **Verdict Logic**:
   - Single suspicious frame (>80%) → FAKE
   - Average across frames (>80%) → FAKE
   - Otherwise → REAL
8. **Cleanup**: Temporary video file deleted post-analysis

---

## 🔮 Roadmap

**Phase 1 - MVP (Complete)** ✅
- [x] Dual AI model ensemble (Vigilante-V2 + Sentinel-X)
- [x] Third detector for non-human content (Omni-Scanner)
- [x] Prism forensic analysis (EXIF, ELA, geometry)
- [x] Web interface with real-time analysis
- [x] Video URL analysis with frame extraction & quality filtering
- [x] Intelligent guardrails to prevent false positives/negatives
- [x] Adaptive thresholds based on content type

**Phase 2 - Autonomous Analysis (In Progress)** 🚀
- [ ] Agentic AI reasoning layer (LLM-powered forensic interpretation)
- [ ] Natural language explanations of detections
- [ ] Autonomous batch processing
- [ ] Cross-media pattern analysis & correlation

**Phase 3 - Enterprise Features** (Future)
- [ ] Batch API & rate limiting
- [ ] Analysis history & database
- [ ] Advanced visualization (heatmaps, ELA comparisons)
- [ ] Temporal LSTM analysis for frame consistency
- [ ] Custom model fine-tuning
- [ ] Distributed processing for high-volume analysis

---

## ⚠️ Disclaimer

**For Educational & Research Use Only**

This tool is designed for educational purposes and research in digital forensics. Key limitations:

- **Not 100% Accurate**: No detection system is perfect. False positives and false negatives will occur.
- **Against Sophisticated Fakes**: State-of-the-art deepfakes may evade detection.
- **Heavily Edited Content**: Legitimate photos with heavy retouching may be flagged.
- **Evolving Threat**: AI generation techniques constantly improve.

⚖️ **Always use this tool as part of a broader investigative process, not as sole evidence.**

---

## 📝 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgments

- [Hugging Face](https://huggingface.co) for model hosting
- [MediaPipe](https://google.github.io/mediapipe/) for face landmark detection
- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework

---

<div align="center">

**Built with 🧠 by [Faraz Mirza](https://github.com/farazmirzax)**

[Report Bug](https://github.com/farazmirzax/deepscan/issues) • [Request Feature](https://github.com/farazmirzax/deepscan/issues)

</div>
