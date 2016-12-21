from PIL import Image, ImageTk
from tkinter import Tk
from tkinter.ttk import Frame, Label
import threading
import picamera
import picamera.array
import cv2
from time import sleep

class VidPanel(Frame):
    def __init__(self, master):
        # intialize the TKinter Frame and panel
        Frame.__init__(self, master)
        self.master = master
        self.panel = None
        # initialize the video stream and allow the camera sensor to warmup
        print("[INFO] warming up camera...")
        self.camera = picamera.PiCamera()
        self.camera.resolution = (320, 240)
        self.camera.exposure_mode = 'auto'
        sleep(2.0)
        self.stream = picamera.array.PiRGBArray(self.camera)
        # initialize the most recently read img, thread for reading frames,
        # and the thread stop event
        self.image = None
        self.thread = None
        self.stopEvent = None
        # Get the first imaage and display it in panel
        self.image = self.getImage()
        self.panel = Label(image=self.image)
        self.panel.image = self.image
        self.panel.pack(side="left", padx=10, pady=10)
        # start a thread that constantly pools the video sensor for
        # the most recently read image and displays it in panel
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()
        # set a callback to handle when the window is closed
        self.master.wm_protocol("WM_DELETE_WINDOW", self.onClose)

    def getImage(self):
        image = None # temp image used for procesing
        # grab the frame from the video stream 
        self.camera.capture(self.stream, format='bgr')
        image = self.stream.array
        self.stream.truncate(0)
        # OpenCV represents images in BGR order; however PIL
        # represents images in RGB order, so we need to swap
        # the channels, then convert to PIL and ImageTk format
        image = image[:, :, ::-1]
        image = Image.fromarray(image)
        return(ImageTk.PhotoImage(image))
        
    def videoLoop(self):
        # This try/except statement is a pretty ugly hack to get around
        # a RunTime error that Tkinter throws due to threading
        try:
            # keep looping over frames until we are instructed to stop
            while not self.stopEvent.is_set():
                # grab the frame from the video stream 
                # OpenCV represents images in BGR order; however PIL
                # represents images in RGB order, so we need to swap
                # the channels, then convert to PIL and ImageTk format
                self.image = self.getImage()
                self.panel.configure(image=self.image)
                self.panel.image = self.image
        except RuntimeError:
            print("[INFO] caught a RuntimeError")

    def onClose(self):
        # set the stop event, cleanup the camera, and allow the rest of
        # the quit process to continue
        print("[INFO] closing...")
        self.stopEvent.set()
        self.master.quit()

if __name__ == "__main__":
    # start the app
    root = Tk()
    root.title('PiBot Camera View')
    VidPanel(master=root).mainloop()
