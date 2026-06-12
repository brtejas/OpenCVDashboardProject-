import cv2
import numpy as np

# Converting every project into function
def process_frame(frame):
 
# Start webcam
 #cap = cv2.VideoCapture(0)

# Check webcam
 #if not cap.isOpened():
    #print("Cannot Access WebCam")
    #exit()

 #while True:
    # Read frame from the webcam
     #ret, frame = cap.read()
     #if not ret :
        #print("Unable to read frame")
       # break
     
    # Copy original frame
     img = frame.copy()
     

    # ---- STEP 1: Convert to HSV ---- 
     img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # ---- STEP 2: Detect teal label color ----
     lower_teal = np.array([80,50,50])
     upper_teal = np.array([140,255,255])
    
     img_mask = cv2.inRange(img_hsv, lower_teal, upper_teal)

    # ---- STEP 3: Clean mask ----
     kernel = np.ones((5,5), np.uint8)

     img_mask = cv2.morphologyEx(img_mask, cv2.MORPH_CLOSE, kernel)

    # ---- STEP 4: Find contours ----
     contours, _ = cv2.findContours(img_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

     label_detected = False
     label_Type = 'No Label'

     if contours:
        # Biggest contour
         largest_contour = max(contours, key = cv2.contourArea)

         area = cv2.contourArea(largest_contour)

        # Ignore small regions
         if area > 4000:
             label_detected = True

            # Rotated rectangle
             rect = cv2.minAreaRect(largest_contour)
             (x,y), (w,h), angle = rect

            # Normalize angle
             if w < h:
                 angle = angle + 90 

                 angle = abs(angle)
            
            # Classification
             if angle < 10:
                 label_Type = 'Straight Label'
             else:
                 label_Type = 'Tilted Label'
            
            # Bounding box
             bbox = cv2.boxPoints(rect)
             bbox = np.int32(bbox)

            # Draw Contours
             cv2.drawContours(img,[bbox],0, (0,255,0), 2)

            # Put text
             cv2.putText(img, f"{label_Type} {int(angle)} deg", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
        
    # No label detected

     if not label_detected:
        cv2.putText(img,"No Label", (50,50),cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)
        return img,"No Label"

    # Show windows
     #cv2.imshow("Bottle Label Detection",img)
     #cv2.imshow("Mask", img_mask)

    # Press Q to quit
     #key = cv2.waitKey(1) & 0xFF

    # if key == ord('q'):
        # break

# Cleanup
 #cap.release()
 #cv2.destroyAllWindows()
     return img, label_Type



           
