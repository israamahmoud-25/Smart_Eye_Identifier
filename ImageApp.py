"""
_summary_
this is a simple program that is used to take images with name on it then save it in 
images folder. 

_requirements_
sudo apt install python3-pip
pip install tkinter |(or) pip3 install tkinter
pip install pillow
"""
import tkinter as tk
from tkinter import messagebox
import cv2
import pandas as pd
from PIL import Image, ImageTk
import os

class CameraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Camera App")
        self.root.geometry("800x600")
        # Initialize variables
        self.save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images')
        self.camera = cv2.VideoCapture(0)
        self.frame = None  # To store captured frame
        
        self.canvas = tk.Canvas(self.root, width=640, height=480)
        self.canvas.pack(pady=5)

        # Create GUI elements
        # self.label = tk.Label(self.root, text="Camera App")
        # self.label.pack(pady=10)

        self.btn_capture = tk.Button(self.root, text="Capture Image", command=self.capture_image)
        self.btn_capture.pack(pady=5)

        self.btn_exit = tk.Button(self.root, text="Exit", command=self.exit_app)
        self.btn_exit.pack(pady=5)
    
        self.update_frame()
        
    def update_frame(self):
        ret, frame = self.camera.read()
        if ret:
            self.frame = frame
            # Convert the image from OpenCV BGR to RGB
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image_pil = Image.fromarray(image_rgb)
            # Convert to ImageTk format to display in Tkinter
            self.image_tk = ImageTk.PhotoImage(image=image_pil)
            # Update the Canvas with the new image
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)
        # around 30 fps
        self.root.after(30, self.update_frame)

    def capture_image(self):
        # Capture image and display in a new window
        if self.frame is not None:
            sub_gui_window = tk.Toplevel(self.root)
            sub_gui = SubGUI(sub_gui_window, self, self.frame)

    def save_image(self, frame, name):
        if os.path.isdir(self.save_path):
            try:
                cv2.imwrite(f"{self.save_path}\\{name}.jpg", frame)
                messagebox.showinfo("Done")
            except Exception as e:
                messagebox.showerror("Error", f"Error saving image: {str(e)}")
        else:
            messagebox.showwarning("Warning", "save path is not a directory in your system\n revise the save path name and existance")


    def exit_app(self):
        self.camera.release()
        self.root.destroy()
###### this is a class to show the image in a seperate GUI
class SubGUI:
    def __init__(self, master, app_instance, frame):
        self.master = master
        self.app_instance = app_instance
        self.master.title("Capture Image")

        self.frame = frame

        self.name = None
        
        self.label = tk.Label(self.master, text="Captured!", font=("Arial", 15))
        self.label.pack(pady=20)
        # show the frame
        self.show_captured_image()
        
        self.label = tk.Label(self.master, text="Please type your name:")
        self.label.pack(side=tk.LEFT, padx=10, pady=5)
        
        self.name = tk.Entry(self.master, width=30)  # Define the entry widget
        self.name.pack(side=tk.LEFT, padx=10, pady=5)
        
        
        self.btn_save = tk.Button(self.master, text="Save Image", command=self.save_image)
        self.btn_save.pack(side=tk.LEFT, padx=10, pady=5)

        self.btn_cancel = tk.Button(self.master, text="Cancel", command=self.cancel_capture)
        self.btn_cancel.pack(side=tk.LEFT, padx=10, pady=5)

    def show_captured_image(self):
        image_rgb = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)

        image_pil = Image.fromarray(image_rgb)
        # Convert to ImageTk format to display in Tkinter
        self.image_tk = ImageTk.PhotoImage(image=image_pil)
        # Display the image on a Label widget
        self.image_label = tk.Label(self.master, image=self.image_tk)
        self.image_label.pack(pady=10)
            
    def save_image(self):
        # Save image using CameraApp instance
        name = self.name.get().strip()
        if len(name) < 1: 
            messagebox.showwarning("Please enter your name first!")
            self.master.focus_force()
            
        elif name.lower().startswith("unknown") :
            messagebox.showwarning("Your name can't start with Unknown")
            self.master.focus_force()
        else:
            self.app_instance.save_image(self.frame, name)
            self.master.destroy()  # Close sub GUI after saving
            
    def cancel_capture(self):
        # Cancel capture action
        self.master.destroy()  # Close sub GUI


            
if __name__ == "__main__":
    root = tk.Tk()
    app = CameraApp(root)
    root.mainloop()
