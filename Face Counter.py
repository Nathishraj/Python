import tkinter as tk
from tkinter import *
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
from tkinter import messagebox
import time


class Way2Cam:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("600x480")
        self.window.title("Face Counter")
        self.window.resizable(0,0)
        self.cap = None
        self.entry()

    def entry(self):
        if self.cap is not None:
            self.cap.release()
        self.f1 = Frame(self.window, width=600, height=480, bg="#5cfdf6")
        self.f1.place(x=0, y=0)
        # Label for face detection
        l1 = Label(self.f1, text="Face Counter!!", font=("Segoe Script", 36, "bold"), bg="#5cfdf6")
        l1.place(x=125, y=80)
        l2 = Label(self.f1, text="using Face Detector...", font=("Segoe Script", 14), bg="#5cfdf6",fg="green")
        l2.place(x=180, y=140)
        # Button to start webcam feed
        b1 = Button(self.f1, text="CAMERA", font=("Lato", 17, "bold"),width=14, bg="#e2f80d",command=self.camm)
        b1.place(x=180, y=220)
        b2 = Button(self.f1, text="GALLERY", font=("Lato", 17, "bold"),width=14, bg="#e2f80d",command=self.open_image)
        b2.place(x=180, y=290)
        self.window.mainloop()

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp")])
        if file_path:
            image = cv2.imread(file_path)
            if image is None:
                messagebox.showerror("Error", "Could not open the image file.")
                return
            # Resize image for consistent processing
            resized_image = cv2.resize(image, (600, 480))  # Resize for better scaling (optional)
            # Convert to grayscale
            gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
            # Apply face detection
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(
                gray, 
                scaleFactor=1.1, 
                minNeighbors=7,  # Higher value reduces false positives
                minSize=(30, 30)  # Minimum face size
            )
            num_faces = len(faces)
            # Draw rectangles around detected faces
            for (x, y, w, h) in faces:
                cv2.rectangle(resized_image, (x, y), (x+w, y+h), (255, 0, 0), 2)
            # Display face count to user
            messagebox.showinfo("Face Count", f"Number of Faces Detected: {num_faces}")
            # Show the image with detected faces
            cv2.imshow("Detected Faces", resized_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


    def camm(self):
        self.cap = cv2.VideoCapture(0)
        def count_faces(frame):
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            # Convert frame to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Detect faces
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            # Count the number of faces
            num_faces = len(faces)
            return num_faces

        def update_frame():
            if self.cap is not None and self.cap.isOpened():
                ret, frame = self.cap.read()
                if ret:
                    num_faces = count_faces(frame)
                    self.face_count_label.config(text="Number of Faces: " + str(num_faces))

                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame_pil = Image.fromarray(frame_rgb)
                    frame_tk = ImageTk.PhotoImage(frame_pil)
                    self.label.config(image=frame_tk)
                    self.label.image = frame_tk

                    self.label.after(10, update_frame)
                else:
                    messagebox.showerror("Error", "Failed to read frame")
            else:
                messagebox.showinfo("Exit", "Camera Closed")

        self.f2 = Frame(self.window, width=600, height=480)
        self.f2.place(x=0, y=0)
        # Label to display the webcam feed
        self.label = Label(self.f2)
        self.label.place(x=0, y=0)
        # Label to display the number of faces detected
        self.face_count_label = Label(self.f2, text="Number of Faces: 0", font=("Segoe UI", 12))
        self.face_count_label.place(x=10, y=440)
        # Create a button to capture and save image
        capture_button = Button(self.f2, text="Capture", font=("Lato", 12), command=self.capture_and_save)
        capture_button.place(x=260, y=430)
        self.b2 = Button(self.f2, text="BACK", font=("Lato", 10, "bold"), command=self.entry)
        self.b2.place(x=25, y=25)
        update_frame()

    def capture_and_save(self):
        if self.cap is not None and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                num_faces = self.count_faces_in_frame(frame)
                cv2.putText(frame, f"Number of Faces: {num_faces}", (50, 50), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 1,(255, 255, 0), 2)
                filename = f"{int(time.time())}_with_faces.jpg"
                cv2.imwrite(filename, frame)
                here = f"Image captured and saved as {filename}"
                messagebox.showinfo("Saved", here)
        else:
            messagebox.showerror("Error", "Camera not available or not opened")

    def count_faces_in_frame(self, frame):
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        num_faces = len(faces)
        return num_faces


go = Way2Cam()
