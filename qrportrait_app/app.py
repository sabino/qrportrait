import os
import glob
import threading
from tkinter import Tk, Toplevel, Label, Button, filedialog
from PIL import Image, ImageTk
import cv2
from pyzbar import pyzbar

from . import scripts_runner

class DisplayWindow(Toplevel):
    """Secondary window showing photos on the external display."""

    def __init__(self, master):
        super().__init__(master)
        self.attributes("-fullscreen", True)
        self.labels = [Label(self) for _ in range(4)]
        for i, lbl in enumerate(self.labels):
            lbl.grid(row=i//2, column=i%2, padx=10, pady=10)
        self.images = []
        self.current_index = 0
        self.after_id = None

    def show_images(self, paths):
        self.clear()
        self.images = paths
        self.current_index = 0
        self._display_next()

    def _display_next(self):
        if not self.images:
            return
        for i in range(4):
            idx = self.current_index + i
            if idx < len(self.images):
                img = Image.open(self.images[idx])
                img.thumbnail((600, 600))
                draw = Image.new('RGB', img.size)
                draw.paste(img)
                tkimg = ImageTk.PhotoImage(draw)
                self.labels[i].configure(image=tkimg, text=str(idx+1), compound='top')
                self.labels[i].image = tkimg
            else:
                self.labels[i].configure(image='', text='')
        self.current_index += 4
        if self.current_index >= len(self.images):
            self.current_index = 0
        self.after_id = self.after(5000, self._display_next)

    def clear(self):
        if self.after_id:
            self.after_cancel(self.after_id)
        for lbl in self.labels:
            lbl.configure(image='', text='')
            lbl.image = None

class OperatorApp(Tk):
    """Main application window for the operator."""

    def __init__(self):
        super().__init__()
        self.title("QrPortrait")
        self.geometry("400x200")
        self.photo_dir = ''
        self.display = DisplayWindow(self)
        self.display.withdraw()
        Button(self, text="Select Photo Directory", command=self.select_dir).pack(pady=5)
        Button(self, text="Start Camera", command=self.start_camera).pack(pady=5)
        Button(self, text="Stop Camera", command=self.stop_camera).pack(pady=5)
        Button(self, text="Generate Cards", command=self.generate_cards).pack(pady=5)
        Button(self, text="Sort Photos", command=self.sort_photos).pack(pady=5)
        Button(self, text="Generate Thumbnails", command=self.generate_thumbnails).pack(pady=5)
        self.cap = None
        self.running = False

    def select_dir(self):
        self.photo_dir = filedialog.askdirectory()
        if self.photo_dir:
            self.display.deiconify()

    def start_camera(self):
        if not self.photo_dir:
            return
        if not self.running:
            self.running = True
            self.cap = cv2.VideoCapture(0)
            threading.Thread(target=self._loop, daemon=True).start()

    def stop_camera(self):
        self.running = False
        if self.cap:
            self.cap.release()
            self.cap = None

    def generate_cards(self):
        scripts_runner.generate_cards()

    def sort_photos(self):
        scripts_runner.sort_photos()

    def generate_thumbnails(self):
        scripts_runner.generate_thumbnails()

    def _loop(self):
        while self.running and self.cap:
            ret, frame = self.cap.read()
            if not ret:
                continue
            codes = pyzbar.decode(frame)
            if codes:
                serial = codes[0].data.decode('utf-8')
                folder = os.path.join(self.photo_dir, serial)
                if os.path.isdir(folder):
                    images = sorted(glob.glob(os.path.join(folder, 'img*.jpg')))
                    self.display.show_images(images)
            cv2.waitKey(100)

if __name__ == '__main__':
    app = OperatorApp()
    app.mainloop()
