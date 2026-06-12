import cv2
import numpy as np
import os 

# Converting each project into function
def process_frame(frame):
 message = "No QR Match"
# Load template
 template = cv2.imread(r"C:\Users\User\Downloads\OPEN_CV\QRCodeDetection\template_2.png")
 template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

 detector = cv2.QRCodeDetector()

# Folder to save images
 saved_path = r"C:\Users\User\Downloads\OPEN_CV\QRCodeDetection\saved_qr_images"

# This does two things:
# Creates the folder if it doesn’t exist
# If it already exists → no error (because of exist_ok=True)
 os.makedirs(saved_path, exist_ok=True)

# To Avoid saving duplicates -> A set is used to store unique values -> Fast lookup, No duplicates allowed
 saved_data = set()


# Webcam 
 #cap = cv2.VideoCapture(0)

# while True:
    # ret, frame = cap.read()
    # if not ret:
       #  break

 gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

 best_val = -1
 best_loc = None
 best_size = None

    # Multi-scale matching
 for scale in np.linspace(0.5, 1.5, 15):
  resized = cv2.resize(template_gray, None, fx=scale, fy=scale)

  if resized.shape[0] > gray.shape[0] or resized.shape[1] > gray.shape[1]:
         continue

  result = cv2.matchTemplate(gray, resized, cv2.TM_CCOEFF_NORMED)
  _, max_val, _, max_loc = cv2.minMaxLoc(result)

  if max_val > best_val:
    best_val = max_val
    best_loc = max_loc
    best_size = resized.shape[::-1]

    # Detection
    #Why 0.4 specifically? It’s just a threshold—a cutoff you choose. > 0.7 → very strict (few but accurate matches)
    # > 0.5 → moderate
    # > 0.3–0.4 → more lenient (detects more, but may include false matches)
 if best_loc is not None and best_val > 0.4:
        top_left = best_loc
        w, h = best_size
        bottom_right = (top_left[0] + w, top_left[1] + h)

        cv2.rectangle(frame, top_left, bottom_right, (0,255,0), 2)

        # Correct cropping
        cropped = frame[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

        data, bbox, _ = detector.detectAndDecode(cropped)

        if bbox is not None:
             message = f"QR Detected: {data}"
             #print("QR Detected:", data)
             #print(data)

            # Make filename safe (remove invalid characters) data = "Hello@123" -> data = "Hello_123" removes all these (spaces, @, #, %, -, _, etc.) characters and converts those into "_"
            #string.isalnum() Returns:
            # True → if all characters are letters (A–Z, a–z) or numbers (0–9)
            # False → if anything else is present
             safe_name = "".join(c if c.isalnum() else "_" for c in data)
            # Avoid duplicate saving : Check: “Have I already saved this QR before?” If NOT saved before: Builds full path
             if safe_name not in saved_data:
                 filename = os.path.join(saved_path, f"{safe_name}.png")
                # Saves the cropped QR image to disk
                 cv2.imwrite(filename, cropped)
                 #print("Saved: " ,filename)
                # Add this QR to the set -> same QR → ignored
                 saved_data.add(safe_name)

                 cv2.putText(frame, data, (top_left[0], top_left[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
        else:
             message = "QR not Detected"
 return frame, message

            

         #cv2.imshow("Cropped", cropped)

     #cv2.imshow("Webcam Detection", frame)
   

     #if cv2.waitKey(1) == ord('q'):
         #break

 #cap.release()
# cv2.destroyAllWindows()
        




