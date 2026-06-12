# importing libraries - 1. cv2 - used for image processing, 2. sys - used for starting and stopping the application
import cv2
import sys

# importing all the projects and its functionalities
from projects.BottleLabelDetectionusingWebcam import process_frame as bottle_process
from projects.ObjectCountingwithMorphopsusingwebcam import process_frame as object_process
from projects.QRCodePatternMatchingusingWebcam import process_frame as qr_process
from projects.GlobalTemplateMatcherusingWebcam import process_frame as global_process, teach_template
from projects.TextDetectionusingWebcam import process_frame as text_process, extract_text

# importing the pyqt5 functionalities
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap

# importing the ui file of project
from pyqt_ui.ui_dashboard import Ui_MainWindow

# creating a dashboard class with inherting QMainWindow as parent class def __init__() as constructor
class Dashboard(QMainWindow):
    def __init__(self):
        # Runs QMainWindow's constructor : without it, Window may not initialize properly.
        super().__init__()
        # UI object is created : Creates UI object.
        self.ui = Ui_MainWindow()
        # Build UI : Creates every button, Creates labels, Creates dropdown, Creates layouts inside Dashboard.
        self.ui.setupUi(self)
        # Webcam object initialization no opening at first so None.
        self.cap = None
        # Creates timer object - in open cv we have while True: loop instead of QTimer in pyqt the while true: freezes everything in ui so we use QTimer in pyqt5
        self.timer = QTimer()
        # Signal and slot connection - if the timer ends (event - signal) we need to start the update_frame() function (reaction to event - slot) to maintain the looping. 
        # real world analogy - signal: door bell ringing (event) slot: deciding to open the door (reaction to that event)
        self.timer.timeout.connect(self.update_frame)
        # Button Clicked (event signal) -> start_camera() (event reaction slot) : Signal and slot mechanism
        self.ui.startCameraButton.clicked.connect(self.start_camera)
        # Button Clicked (event signal) -> stop_camera() (event reaction slot) : Signal and slot mechanism
        self.ui.stopCameraButton.clicked.connect(self.stop_camera)
        # Log : Displays: System Ready in Output Window.
        self.log("System Ready")
        # Current Project - Initially: No project selected so None.
        self.selected_project = None
        # Hide Buttons - at the start of the module we do not require these buttons these are program specific so making these button invisible at first.
        self.ui.captureButton.hide()
        self.ui.teachButton.hide()
        #  Dropdown Event - User selects project -> project_changed()
        self.ui.projectDropdown.currentTextChanged.connect(self.project_changed)
        # Run button Event - User selects runButton -> run_project() gets activated
        self.ui.runButton.clicked.connect(self.run_project)
        # stop button Event - User selects stopButton -> stop_project() gets activated
        self.ui.stopButton.clicked.connect(self.stop_project)
        # capture button Event - User selects captureButton -> capture_text() gets activated
        self.ui.captureButton.clicked.connect(self.capture_text)
        # Teach pattern button Event - User selects runButton -> teach_pattern() gets activated
        self.ui.teachButton.clicked.connect(self.teach_pattern)
        self.project_changed()
        # to execute the teachpattern and capturetext we need last frame to be captured and executed and last message to be printed, so we use these declarations. 
        # current_frame  = Latest camera screenshot
        self.current_frame = None
        # last_message = Remember the previous result, to avoid duplicate logs
        self.last_message = ""
        
    
    # Without it, every place in the code would need: self.ui.outputWindow.append("Camera Started") - to reuse it again we use this function and declare everywhere using self.log() - Repeated everywhere.
    def log(self, message):
        self.ui.outputWindow.append(message)
    # starting camera function
    def start_camera(self):
        # Opens webcam.
        self.cap = cv2.VideoCapture(0)
        # Starts frame updates.
        self.timer.start(30)
        # Changes status label.
        self.ui.statusLabel.setText("Status : Camera Running")
        self.log("Start Camera")
    # stops the camera function
    def stop_camera(self):
        # Stops frame updates.
        self.timer.stop()
        if self.cap is not None:
            # Releases webcam.
            self.cap.release()
        self.ui.cameraDisplayLabel.setText("Camera not Started")
        self.ui.statusLabel.setText("Status : Camera Stopped")
        self.log("Camera Stopped")
    # This is the heart of your application.
    def update_frame(self):
        if self.cap is None:
            return
        # Gets webcam frame.
        ret, frame = self.cap.read()
        if not ret:
            return
        # Stores frame. used by teach pattern and capture text
        self.current_frame = frame.copy()
        # Project routing
        if self.selected_project == "Bottle Label Detector":
            frame, msg = bottle_process(frame)
            self.updated_result(msg)
        elif self.selected_project == "QR Template Matcher":
            frame,msg = qr_process(frame)
            self.updated_result(msg)
        elif self.selected_project == "Object Counter":
            frame,msg = object_process(frame)
            self.updated_result(msg)
        elif self.selected_project == "Global Template Matcher":
            frame,msg = global_process(frame)
            self.updated_result(msg)
        elif self.selected_project == "Text Detector":
            frame = text_process(frame)
        # converting BGR(opencv) to RGB(pyqt5)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h,w,ch = frame.shape
        bytes_per_line = ch * w
        # Convert: QImage: Creates Qt image.
        qt_image = QImage(frame.data, w, h , bytes_per_line, QImage.Format_RGB888)
        # Convert: QPixmap: Converts to displayable image.
        pixmap = QPixmap.fromImage(qt_image)
        # Display: Displays frame.
        self.ui.cameraDisplayLabel.setPixmap(pixmap)
    # project_changed() -> Controls button visibility.
    def project_changed(self):
        project = self.ui.projectDropdown.currentText()
        self.ui.captureButton.hide()
        self.ui.teachButton.hide()
        self.ui.runButton.show()
        self.ui.stopButton.show()
        if project == "Text Detector":
            self.ui.captureButton.show()
            self.ui.runButton.hide()
            self.ui.stopButton.hide()
        if project == "Global Template Matcher":
            self.ui.teachButton.show()
        self.log(f"Selected Project : {project}")
    # Stores: self.selected_project : which tells: update_frame() -> which algorithm to execute.
    def run_project(self):
        self.selected_project = (self.ui.projectDropdown.currentText())
        self.log(f"Running : {self.selected_project}")
        self.ui.statusLabel.setText(f"Status : Running")
    # stops any running project
    def stop_project(self):
        self.selected_project = None
        self.log(f"Stopping : {self.selected_project}")
        self.ui.statusLabel.setText(f"Status : Stopping")
    # Runs OCR.
    def capture_text(self):
        if self.current_frame is None:
            self.log("No Camera Frame Available")
            return
        text = extract_text(self.current_frame)
        if text:
            self.log(f"OCR Result: {text}")
        else:
            self.log("No Text Detected")
    # Stores template image.
    def teach_pattern(self):
        if self.current_frame is None:
            self.log("No Camera Frame available")
            return
        teach_template(self.current_frame)
        self.log("Template Learned Sucessfully")
    # Prevents duplicate logs. This is actually one of the best additions in your current architecture.
    def updated_result(self, message):
        if message != self.last_message:
            self.log(message)
            self.last_message = message

    

# Means: Run only when file executed directly.
if __name__ == "__main__":
    # Create application.
    app = QApplication(sys.argv)
    # Create Window.
    window = Dashboard()
    # Display window.
    window.show()
    # Start Qt Event Loop. This line keeps the GUI alive waiting for: Button Clicks, Timer Events, Dropdown Changes, until user closes the application.
    sys.exit(app.exec_())



     



