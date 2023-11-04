# Face-attendance-system_for_schools
The School Facial Recognition System is an application that allows schools to keep track of student attendance using facial recognition technology. This system can recognize and record the time when a student arrives at school and send an email notification to the parents.
## How the Code Works
The code is written in Python and uses various libraries and modules to achieve its functionality. Here's an overview of how the code works:

1. **Importing Necessary Libraries and Modules:**
   - The code imports libraries such as OpenCV (cv2), tkinter, os, util, and face_recognition. It also uses the Pillow library (PIL) for image manipulation and smtplib for sending email notifications.

2. **Initializing the Main Application:**
   - The `App` class is the main application window for the system. It includes the login and registration features.

3. **Processing the Webcam Feed:**
   - The code captures the webcam feed using OpenCV and displays it in a tkinter window.
   - It continuously captures frames from the webcam and displays the most recent frame.
