# Importing libraries
import cv2
import numpy as np
import os

# -----------------------------------------
# CREATE FOLDERS
# -----------------------------------------
template_folder = r"C:\Users\User\Downloads\OPEN_CV\QRCodeDetection\saved_templates"

captured_folder = r"C:\Users\User\Downloads\OPEN_CV\QRCodeDetection\captured_objects"

os.makedirs(template_folder, exist_ok=True)

os.makedirs(captured_folder, exist_ok=True)

# -----------------------------------------
# GLOBAL TEMPLATE
# -----------------------------------------
template_image = None 
# -----------------------------------------
# SELECT TEMPLATE IMAGE
# -----------------------------------------
#template_path = input("Enter the template image: ")
# -----------------------------------------
# TEACH TEMPLATE
# -----------------------------------------
def teach_template(frame):
    global template_image
    h, w, _ = frame.shape
    template_image = frame[h//4:3*h//4, w//4:3*w//4].copy()
    print("Template Learned")


# -----------------------------------------
# SAVE TEMPLATE COPY
# -----------------------------------------
    template_save_path = os.path.join(template_folder, "template_image.png")

    cv2.imwrite(template_save_path, template_image)
    print("Template saved Successfully")

# -----------------------------------------
# PROCESS FRAME
# -----------------------------------------
def process_frame(frame):
    global template_image 
    # -----------------------------------------
    # NO TEMPLATE
    # -----------------------------------------
    if template_image is None:
        cv2.putText(frame, "No Template Loaded", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        # -----------------------------------------
        # RETURN FRAME
        # -----------------------------------------
        return frame

    # -----------------------------------------
    # CONVERT TEMPLATE TO GRAYSCALE
    # -----------------------------------------

    template_gray = cv2.cvtColor(template_image, cv2.COLOR_BGR2GRAY)

    # Get template width and height
    template_height, template_width = template_gray.shape

# -----------------------------------------
# START WEBCAM
# -----------------------------------------
#cap = cv2.VideoCapture(0)


# -----------------------------------------
# WEBCAM LOOP
# -----------------------------------------
#while True:
     # Read webcam frame
    #ret, frame = cap.read()
    # Safety check
    #if not ret:
       # print("Unable to read frame")
        #break

    # -----------------------------------------
    # CONVERT FRAME TO GRAYSCALE
    # -----------------------------------------
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # -----------------------------------------
    # TEMPLATE MATCHING
    # -----------------------------------------
    result = cv2.matchTemplate(gray, template_gray, cv2.TM_CCOEFF_NORMED)

    # -----------------------------------------
    # FIND BEST MATCH
    # -----------------------------------------
    min_val,max_val,min_loc,max_loc = cv2.minMaxLoc(result)
    # -----------------------------------------
    # THRESHOLD
    # -----------------------------------------
    threshold = 0.6
    # -----------------------------------------
    # MATCH FOUND
    # -----------------------------------------
    if max_val >= threshold:
        # Top-left point
        top_left = max_loc
        # Bottom-right point
        bottom_right = (top_left[0] + template_width, top_left[1] + template_height)
        # Draw rectangle
        cv2.rectangle(frame, top_left,bottom_right, (0,255,0), 2)
        # Display text
        cv2.putText(frame, f"MATCH FOUND: {max_val:.2f}", (20,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2, lineType = cv2.LINE_AA)
        # -----------------------------------------
        # CROP DETECTED OBJECT
        # -----------------------------------------
        cropped_object = frame[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
        # -----------------------------------------
        # SAVE DETECTED OBJECT
        # -----------------------------------------
        object_save_path = os.path.join(captured_folder, "detected_object.png")
        cv2.imwrite(object_save_path, cropped_object)
        print("Image saved")
    # -----------------------------------------
    # NO MATCH FOUND
    # -----------------------------------------
    else:
        cv2.putText(frame, f"DEFECT DETECTED : {max_val:.2f}", (20,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2, lineType = cv2.LINE_AA)
        return frame, f"DEFECT DETECTED : {max_val:.2f}"
    return frame, f"MATCH FOUND : {max_val:.2f}"


    # -----------------------------------------
    # SHOW WINDOWS
    # -----------------------------------------
    #cv2.imshow("Live Detection", frame)
    #cv2.imshow("Template Image", template)
    # -----------------------------------------
    # EXIT KEY
    # -----------------------------------------
    #key = cv2.waitKey(1)
    #if key == ord('q'):
       # break

# -----------------------------------------
# RELEASE CAMERA
# -----------------------------------------
#cap.release()
#cv2.destroyAllWindows()

# Other modules are: stateless, Template matcher is: stateful
# WHAT IS STATE? State means: remembering something from the past 
# Example: user taught template 10 seconds ago System must REMEMBER it. That remembered data is: STATE
# OTHER MODULES DON'T REMEMBER ANYTHING Example: Bottle detector: 
# Frame comes ↓ detect teal ↓ done ↓ forget everything Next frame: starts fresh, No memory. No state.




