import subprocess
import tkinter as tk
import cv2
import os
import util
from PIL import Image, ImageTk
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from datetime import datetime
import face_recognition


class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1200x520+350+100")

        # Adding background
        background_image = Image.open("background.jpg")
        background_photo = ImageTk.PhotoImage(background_image)

        background_label = tk.Label(self.main_window, image=background_photo)
        background_label.place(width=1500,height=700,y=-50,x=-50)
        background_label.photo = background_photo

        self.login_button_main_window = util.get_button(self.main_window, 'login', 'green', self.login)
        self.login_button_main_window.place(x=750, y=300)

        self.register_new_user_button_main_window = util.get_button(self.main_window, 'register new user', 'gray',
                                                                self.register_new_user, fg='black')
        self.register_new_user_button_main_window.place(x=750, y=400)        

        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500)

        self.add_webcam(self.webcam_label)

        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        self.log_path = './log.txt'

    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)

        self.label = label
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()
        self.most_recent_capture_arr = frame

        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)

        self.most_recent_capture_pil = Image.fromarray(img_)

        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        self.label.imgtk = imgtk
        self.label.configure(image=imgtk)

        self.label.after(20, self.process_webcam)

    def login(self):
        unknown_img_path = './.tmp.jpg'
        cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)

        # Load known face encodings from the database
        known_face_encodings = []
        known_face_names = []

        for filename in os.listdir(self.db_dir):
            if filename.endswith('.jpg'):
                username = os.path.splitext(filename)[0]
                image_path = os.path.join(self.db_dir, filename)
                image = face_recognition.load_image_file(image_path)
                encoding = face_recognition.face_encodings(image)[0]
                known_face_encodings.append(encoding)
                known_face_names.append(username)

        # Load the unknown image
        unknown_image = face_recognition.load_image_file(unknown_img_path)
        unknown_face_encodings = face_recognition.face_encodings(unknown_image)

        if not unknown_face_encodings:
            util.msg_box('No Face Found', 'No face detected. Email not sent.')
            os.remove(unknown_img_path)
            return

        # Compare the unknown face with known faces
        matches = face_recognition.compare_faces(known_face_encodings, unknown_face_encodings[0])

        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
            util.msg_box('Success', f'Welcome, {name}!')
            self.send_login_email(name)  # Send login email
        else:
            util.msg_box('Authentication Failed', 'Unknown person detected. Access denied.')

        os.remove(unknown_img_path)

    def send_login_email(self, username):
        # Configure your email settings
        smtp_server = 'smtp.gmail.com'  # SMTP server address
        smtp_port = 587  # SMTP server port
        sender_email = 'your email'
        sender_password = 'your password'

        # Get the recipient email (parent's email) based on the provided username
        recipient_email = self.get_parent_email(username)

        if not recipient_email:
            util.msg_box('Error', 'Recipient email not found for the provided username.')
            return

        subject = 'Arrival Time'
        current_time = datetime.now().strftime('%H:%M')  # Get the current time in HH:MM format
        message = f'Dear {username}\'s parents,\n\n{username} arrived at {current_time}.\n\nBest regards,\nYour Attendance System'

        # Create a MIMEText message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        # Attach the user's picture
        with open('./.tmp.jpg', 'rb') as image_file:
            image = MIMEImage(image_file.read(), name='user_picture.jpg')
            msg.attach(image)

        # Send the email
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
            server.quit()
        except Exception as e:
            print(f"Failed to send email: {e}")

    def get_parent_email(self, username):
        try:
            with open(self.log_path, 'r') as log_file:
                for line in log_file:
                    parts = line.strip().split(', ')
                    if len(parts) == 2:
                        username_parts = parts[0].split(': ')
                        email_parts = parts[1].split(': ')
                        if len(username_parts) == 2 and username_parts[0] == 'Username' and username_parts[
                            1] == username:
                            print(f"Found matching username: {username}")
                            if len(email_parts) == 2 and email_parts[0] == 'Email':
                                return email_parts[1].strip()
        except Exception as e:
            print(f"Error while retrieving parent email: {e}")

        print(f"Recipient email not found for username: {username}")
        return None

    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1200x520+370+120")

        self.accept_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Accept', 'green',
                                                                      self.accept_register_new_user)
        self.accept_button_register_new_user_window.place(x=750, y=300)

        self.try_again_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Try again',
                                                                         'red', self.try_again_register_new_user)
        self.try_again_button_register_new_user_window.place(x=750, y=400)

        self.capture_label = util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)

        self.add_img_to_label(self.capture_label)

        self.entry_text_username = util.get_entry_text(self.register_new_user_window)
        self.entry_text_username.place(x=750, y=100)

        self.entry_text_email = util.get_entry_text(self.register_new_user_window)
        self.entry_text_email.place(x=750, y=200)

        self.text_label_username = util.get_text_label(self.register_new_user_window, 'Please, input username:')
        self.text_label_username.place(x=750, y=70)

        self.text_label_email = util.get_text_label(self.register_new_user_window, 'Please, input Parent email:')
        self.text_label_email.place(x=750, y=170)

    def try_again_register_new_user(self):
        self.register_new_user_window.destroy()

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.register_new_user_capture = self.most_recent_capture_arr.copy()

    def accept_register_new_user(self):
        username = self.entry_text_username.get(1.0, "end-1c")
        email = self.entry_text_email.get(1.0, "end-1c")

        # Ensure that both username and email are provided
        if username.strip() == "" or email.strip() == "":
            util.msg_box('Error', 'Please provide both username and email.')
            return

        cv2.imwrite(os.path.join(self.db_dir, '{}.jpg'.format(username)), self.register_new_user_capture)

        # Save the username and email in a text file or a database
        with open(self.log_path, 'a') as log_file:
            log_file.write(f'Username: {username}, Email: {email}\n')

        util.msg_box('Success!', 'User was registered successfully!')

        self.register_new_user_window.destroy()

    def start(self):
        self.main_window.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()
