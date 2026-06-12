import cv2
import numpy as np 

#Converting each project into function
def process_frame(frame):
     
# Start webcam
 #cap = cv2.VideoCapture(0)

# check webcam
 #if not cap.isOpened():
     #print("Cannot access webcam")
     #exit()

 #while True:
     # Read frame
     #ret, frame = cap.read()

     #if not ret:
         #print("Failed to grab image")
         #break
    
     # Resize frame
     img = cv2.resize(frame, (600,400) )

    # Convert to grayscale
     img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Blur to reduce noise
     img_blur = cv2.GaussianBlur(img_gray, (5,5),0)

    # Threshold
     _, thresh = cv2.threshold(img_blur, 105, 255, cv2.THRESH_BINARY)

       # -------------------------------
    # Morphological Operations
    # -------------------------------

    # Elliptical kernel
     kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))

    # Closing operation
     closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations = 2)

     processed = closing

    # Find contours
     contours, _ = cv2.findContours(processed, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

     count = 0

     for contour in contours:
         area = cv2.contourArea(contour)
        
        # Ignore small noise
         if area > 500:
             count =+ 1
        
        # Draw contour
         cv2.drawContours(img, [contour], -1, (0,255,0), 2)

        # Display count
     cv2.putText(img, f"Count: {count}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, lineType = cv2.LINE_AA)
     return img, f"Count: {count}"

        # Show windows
     #cv2.imshow("Threshold", thresh)
     #cv2.imshow("After Morphology", processed)
     #cv2.imshow("Objects Counted",img)

        # Press Q to quit
     #key = cv2.waitKey(1) & 0xFF

    # if key == ord('q'):
             #break

# Cleanup
 #cap.release()
 #cv2.destroyAllWindows()




       