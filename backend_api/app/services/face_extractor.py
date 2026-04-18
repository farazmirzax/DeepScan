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

def get_all_face_crops(image_bytes):
    """
    Takes raw image bytes, finds ALL faces using OpenCV, 
    and returns a list of cropped PIL Images.
    """
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if image is None:
        return []

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    if len(faces) == 0:
        return []

    extracted_faces = []
    padding = 40
    height, width, _ = image.shape

    # LOOP through ALL faces instead of just picking faces[0]
    for (x, y, w, h) in faces:
        px = max(0, x - padding)
        py = max(0, y - padding)
        pw = min(width - px, w + (padding * 2))
        ph = min(height - py, h + (padding * 2))

        face_crop = image[py:py+ph, px:px+pw]
        face_rgb = cv2.cvtColor(face_crop, cv2.COLOR_BGR2RGB)
        extracted_faces.append(Image.fromarray(face_rgb))
        
    return extracted_faces

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
       # Change this section inside extract_faces_from_video:
        is_success, buffer = cv2.imencode(".jpg", frame)
        if is_success:
            byte_data = buffer.tobytes()
            # Use the new multi-face function
            faces_in_frame = get_all_face_crops(byte_data) 
            
            if faces_in_frame:
                faces_found.extend(faces_in_frame) # Use .extend() to add the whole list
                print(f"   ✓ Frame {i}: {len(faces_in_frame)} valid faces extracted.")
    
    cap.release()
    print(f"✅ Extracted {len(faces_found)} valid high-quality faces from video.")
    return faces_found