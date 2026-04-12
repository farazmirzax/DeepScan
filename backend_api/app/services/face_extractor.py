import cv2
import numpy as np
from PIL import Image
import io
import os

# --- INITIALIZE DETECTOR ---
# We use the standard "Haar Cascade" detector built into OpenCV
# It's fast, lightweight, and works on EVERY Python version.
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def calculate_image_sharpness(image_array):
    """
    Calculate image sharpness using Laplacian variance.
    Higher value = sharper/clearer image
    Lower value = blurry image
    """
    if image_array is None or image_array.size == 0:
        return 0
    
    gray = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    variance = laplacian.var()
    return variance

def get_face_crop(image_bytes):
    """
    Takes raw image bytes (from a file upload), finds the face using OpenCV, 
    and returns the cropped PIL Image.
    """
    # 1. Convert bytes to OpenCV format
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if image is None:
        return None

    # 2. Convert to Grayscale (Face detectors need black & white)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 3. Detect Faces
    # scaleFactor=1.1, minNeighbors=5 are standard settings
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    if len(faces) == 0:
        # print("❌ No face detected by OpenCV.") 
        # (Commented out print to keep logs clean during video scanning)
        return None

    # 4. Get the biggest face (if multiple, pick the main one)
    # (x, y, w, h) are the coordinates
    x, y, w, h = faces[0] 
    
    # 5. Add Padding (Don't crop too tight!)
    padding = 40
    height, width, _ = image.shape
    
    x = max(0, x - padding)
    y = max(0, y - padding)
    w = min(width - x, w + (padding * 2))
    h = min(height - y, h + (padding * 2))

    # 6. Crop and Convert back to RGB
    face_crop = image[y:y+h, x:x+w]
    face_rgb = cv2.cvtColor(face_crop, cv2.COLOR_BGR2RGB)
    
    return Image.fromarray(face_rgb)

def extract_faces_from_video(video_path, max_frames=5):
    """
    Takes a video file path (mp4).
    Scans through the video and returns a LIST of cropped face images (PIL Images).
    Filters out blurry/poor quality frames for better detection accuracy.
    """
    cap = cv2.VideoCapture(video_path)
    faces_found = []
    
    if not cap.isOpened():
        print(f"❌ Error: Could not open video at {video_path}")
        return []

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Safety: If video is short or empty
    if total_frames <= 0:
        return []

    # We don't want to check every single frame (too slow).
    # Let's check 'max_frames' spread out evenly across the video.
    skip_step = max(1, total_frames // max_frames)
    
    print(f"🎞️ Scanning video: {total_frames} frames. Checking every {skip_step}th frame...")

    SHARPNESS_THRESHOLD = 100  # Minimum sharpness score (filters blurry frames)

    for i in range(0, total_frames, skip_step):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = cap.read()
        
        if not ret:
            break
        
        # --- QUALITY CHECK: Calculate frame sharpness ---
        sharpness = calculate_image_sharpness(frame)
        
        if sharpness < SHARPNESS_THRESHOLD:
            print(f"   ⚠️  Frame {i}: Skipped (too blurry, sharpness={sharpness:.1f})")
            continue
            
        # Convert frame to bytes so we can reuse our existing get_face_crop logic!
        # This keeps our code clean and consistent.
        is_success, buffer = cv2.imencode(".jpg", frame)
        if is_success:
            byte_data = buffer.tobytes()
            face = get_face_crop(byte_data) # Reuse the function above ⬆️
            
            if face:
                faces_found.append(face)
                print(f"   ✓ Frame {i}: Valid face extracted (sharpness={sharpness:.1f})")
    
    cap.release()
    print(f"✅ Extracted {len(faces_found)} valid high-quality faces from video.")
    return faces_found