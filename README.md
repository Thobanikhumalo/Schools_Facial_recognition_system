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

4. **Register New User Function:**
   - When the user clicks the "Register New User" button, they are prompted to input a username and parent's email.
   - The code captures the user's face and saves it as an image in the database folder.
   - It also saves the username and email in a log file for future reference.

5. **Login Function:**
   - When the user clicks the "Login" button, the code captures the current frame, saves it as an image, and compares it to 
     known face encodings in the database.
   - If a match is found, it sends an email to the student's parents with the current time and a message confirming their 
     child's arrival.

6. **Sending Email Notifications:**
   - The code uses the smtplib library to send email notifications.
   - It configures the SMTP server, sender's email, and sender's password.
   - It retrieves the parent's email based on the recognized username.
  
7. **Other Utility Functions:**
   - The code includes several utility functions for creating buttons, labels, and text entry fields, as well as functions 
     to display message boxes and recognize faces based on the saved database.

## How to Use the System

1. Run the application.
2. Click the "Register New User" button to add a new student to the system.
3.Click the "Login" button to recognize a student's face and send an email to their parents.

## Dependencies

The system relies on the following Python libraries and modules:
- OpenCV (cv2)
- tkinter
- Pillow (PIL)
- smtplib
- face_recognition

# Enjoy using the School Facial Recognition System!
