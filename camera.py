import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
import time

class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source

        self.vid = MyVideoCapture(self.video_source)
        if not self.vid.is_open():
            messagebox.showerror("Error", "Unable to open video source.")
            self.window.destroy()
            return

        self.canvas = tk.Canvas(window, width=self.vid.width, height=self.vid.height)
        self.canvas.pack()

        self.btn_frame = tk.Frame(window, bg="black")
        self.btn_frame.pack(side="bottom", fill="x")

        self.btn_snapshot = tk.Button(self.btn_frame, text="Snapshot", width=20, bg="black", fg="white", command=self.snapshot)
        self.btn_snapshot.pack(side="left", padx=10, pady=10)

        self.update()

    def update(self):
        ret, frame = self.vid.get_frame()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame)
            self.photo = ImageTk.PhotoImage(image)
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.window.after(10, self.update)

    def snapshot(self):
        ret, frame = self.vid.get_frame()
        if ret:
            filename = f'snapshot_{int(time.time())}.png'
            cv2.imwrite(filename, frame)
            messagebox.showinfo("Snapshot", f"Snapshot saved as {filename}")
        else:
            messagebox.showerror("Error", "Unable to take snapshot.")

class MyVideoCapture:
    def __init__(self, video_source=0):
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError(f"Unable to open video source {video_source}")
        
        self.height = int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.width = int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH))

    def is_open(self):
        return self.vid.isOpened()

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                return ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                return ret, None
        else:
            return False, None

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

def cam():
    root = tk.Tk()
    App(root, "Camera")
    root.mainloop()
