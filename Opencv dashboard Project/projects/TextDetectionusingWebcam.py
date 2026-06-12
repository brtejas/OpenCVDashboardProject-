import cv2
import pytesseract
from PIL import Image

# Converting each project into function
def process_frame(frame):
    return frame

 #camera = cv2.VideoCapture(0)

 #while True:
    # _,image = camera.read()
def extract_text(frame):
    image = frame
    # cv2.imshow("Text Detected: ", image)
     #if cv2.waitKey(1) & 0xFF == ord('s'):
    #cv2.imwrite("test1.jpg",image)
       # break
 #camera.release()
 #cv2.destroyAllWindows()

    def tesseract():
     pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
     #image_path = "test1.jpg"
     #text = pytesseract.image_to_string(Image.open(image_path))
     text = pytesseract.image_to_string(image)
     return text.strip()
    # print(text[:-1])
    return tesseract()
    