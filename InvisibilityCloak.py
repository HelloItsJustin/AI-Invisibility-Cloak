import cv2
import numpy as np
import time
from collections import deque
from pyzbar import pyzbar

cloak_active = False
background_mode = "static"

# Background options
custom_backgrounds = {
    "video": None,
    "image": None,
}

# FPS calculation variables
fps_deque = deque(maxlen=30)
prev_frame_time = 0

# QR code control
last_qr_data = None
qr_cooldown = 0
QR_COOLDOWN_FRAMES = 30  # To Prevent multiple triggers

print(cv2.__version__)

def detect_qr_codes(frame):
    # Decode QR codes
    decoded_objects = pyzbar.decode(frame)
    
    for obj in decoded_objects:
        # Draw rectangle around QR code
        points = obj.polygon
        if len(points) > 4:
            hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
            points = hull
        
        n = len(points)
        for j in range(n):
            cv2.line(frame, tuple(points[j]), tuple(points[(j+1) % n]), (0, 255, 0), 3)
        
        # Get decoded data
        qr_data = obj.data.decode('utf-8')
        
        # Display QR data on frame
        x = obj.rect.left
        y = obj.rect.top
        cv2.putText(frame, qr_data, (x, y - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        return qr_data, frame
    
    return None, frame

def get_dynamic_background(static_bg, frame_shape):
    global background_mode, custom_backgrounds
    
    if background_mode == "static":
        return static_bg
    
    elif background_mode == "video" and custom_backgrounds["video"] is not None:
        ret, bg_frame = custom_backgrounds["video"].read()
        if not ret:
            custom_backgrounds["video"].set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, bg_frame = custom_backgrounds["video"].read()
        
        if ret:
            bg_frame = cv2.resize(bg_frame, (frame_shape[1], frame_shape[0]), 
                                 interpolation=cv2.INTER_LINEAR)
            bg_frame = np.flip(bg_frame, axis=1)
            return bg_frame
        return static_bg
    
    elif background_mode == "image" and custom_backgrounds["image"] is not None:
        bg_image = cv2.resize(custom_backgrounds["image"], (frame_shape[1], frame_shape[0]),
                             interpolation=cv2.INTER_LINEAR)
        bg_image = np.flip(bg_image, axis=1)
        return bg_image
    
    return static_bg

def calculate_fps():
    global prev_frame_time, fps_deque
    
    current_time = time.time()
    frame_time = current_time - prev_frame_time
    prev_frame_time = current_time
    
    if frame_time > 0:
        fps_deque.append(1 / frame_time)
    
    return int(np.mean(fps_deque)) if len(fps_deque) > 0 else 0

def main():
    global cloak_active, prev_frame_time, background_mode, custom_backgrounds
    global last_qr_data, qr_cooldown
    
    # Video capture
    capture_video = cv2.VideoCapture(0)
    
    # Optimize camera settings
    capture_video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    capture_video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    capture_video.set(cv2.CAP_PROP_FPS, 60)
    capture_video.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    capture_video.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
    
    time.sleep(2)
    
    # Capture initial background
    print("Capturing background in 3 seconds...")
    print("Make sure the red/pink cloth is NOT in frame!")
    time.sleep(3)
    
    background_frames = []
    for i in range(30):
        ret, bg = capture_video.read()
        if ret:
            background_frames.append(bg)
    
    background = np.median(background_frames, axis=0).astype(np.uint8)
    background = np.flip(background, axis=1)
    
    print("\n" + "="*60)
    print("Background captured!")
    print("="*60)
    print("\n QR CODE CONTROL:")
    print("─" * 60)
    print("Generate QR codes with these texts:")
    print("  • 'CLOAK_ON' or 'INVISIBLE' → Activate cloak")
    print("  • 'CLOAK_OFF' or 'VISIBLE' → Deactivate cloak")
    print("  • 'TOGGLE' → Switch cloak state")
    print("─" * 60)
    print("\n Keyboard Shortcuts:")
    print("  • 'C' - Manual toggle")
    print("  • 'ESC' - Exit")
    print("="*60 + "\n")
    
    # Pre-create kernels
    kernel_open = np.ones((7, 7), np.uint8)
    kernel_close = np.ones((7, 7), np.uint8)
    kernel_dilate = np.ones((5, 5), np.uint8)
    
    prev_frame_time = time.time()
    
    while capture_video.isOpened():
        ret, img = capture_video.read()
        if not ret:
            break
        
        img = np.flip(img, axis=1)
        
        # Create copy for QR detection
        display_img = img.copy()
        
        # Detect QR codes
        qr_data, display_img = detect_qr_codes(display_img)
        
        # Process QR code with cooldown
        if qr_cooldown > 0:
            qr_cooldown -= 1
        else:
            if qr_data is not None and qr_data != last_qr_data:
                qr_data_upper = qr_data.upper()
                
                if qr_data_upper in ['CLOAK_ON', 'INVISIBLE', 'ON', 'ACTIVATE']:
                    cloak_active = True
                    print("QR Code Scanned: Cloak ACTIVATED")
                    qr_cooldown = QR_COOLDOWN_FRAMES
                    last_qr_data = qr_data
                
                elif qr_data_upper in ['CLOAK_OFF', 'VISIBLE', 'OFF', 'DEACTIVATE']:
                    cloak_active = False
                    print("QR Code Scanned: Cloak DEACTIVATED")
                    qr_cooldown = QR_COOLDOWN_FRAMES
                    last_qr_data = qr_data
                
                elif qr_data_upper in ['TOGGLE', 'SWITCH']:
                    cloak_active = not cloak_active
                    print(f"QR Code Scanned: Cloak {'ON' if cloak_active else 'OFF'}")
                    qr_cooldown = QR_COOLDOWN_FRAMES
                    last_qr_data = qr_data
            
            elif qr_data is None:
                last_qr_data = None
        
        if cloak_active:
            # Apply Gaussian blur
            blurred = cv2.GaussianBlur(img, (7, 7), 0)
            hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
            
            # Better HSV ranges for red/pink
            lower_red1 = np.array([0, 100, 50])
            upper_red1 = np.array([10, 255, 255])
            mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
            
            lower_red2 = np.array([160, 100, 50])
            upper_red2 = np.array([180, 255, 255])
            mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
            
            mask = cv2.bitwise_or(mask1, mask2)
            
            # Morphological operations
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel_open, iterations=2)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel_close, iterations=2)
            mask = cv2.dilate(mask, kernel_dilate, iterations=2)
            mask = cv2.GaussianBlur(mask, (5, 5), 0)
            
            mask_inv = cv2.bitwise_not(mask)
            
            current_bg = get_dynamic_background(background, img.shape)
            
            res_bg = cv2.bitwise_and(current_bg, current_bg, mask=mask)
            res_fg = cv2.bitwise_and(img, img, mask=mask_inv)
            
            final_output = cv2.addWeighted(res_bg, 1, res_fg, 1, 0)
        else:
            final_output = display_img
        
        # Calculate FPS
        fps = calculate_fps()
        
        # Display info
        cv2.putText(final_output, f"FPS: {fps}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        
        status_color = (0, 255, 0) if cloak_active else (0, 0, 255)
        status_text = "CLOAK: ON" if cloak_active else "CLOAK: OFF"
        cv2.putText(final_output, status_text, (10, 420), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 2)
        
        cv2.putText(final_output, "Show QR Code to control", (10, 450), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 200, 100), 1)
        
        # Show cooldown
        if qr_cooldown > 0:
            cv2.putText(final_output, f"Cooldown: {qr_cooldown}", (10, 470), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 165, 0), 1)
        
        cv2.imshow("AI Invisibility Cloak", final_output)
        
        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            break
        elif key == ord('c'):
            cloak_active = not cloak_active
            print(f"Manual toggle: Cloak {'ON' if cloak_active else 'OFF'}")
    
    capture_video.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()