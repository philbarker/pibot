#!/usr/bin/python3
from tkinter import Tk, StringVar
from tkinter.ttk import Frame, Button, Label, LabelFrame, OptionMenu
from tkinter.constants import N, S, E, W, SUNKEN
from PIL import ImageTk, Image
from picamera import PiCamera
import signal, sys, random
import RPi.GPIO as GPIO
from time import *
from subprocess import call
 
import os



class PiBot:
    def __init__(self):
        self.camera = PiCamera()
        self.camera.vflip = True
        self.camera.resolution = (320,240)
        self.img_path = '/home/pi/cam.jpg'
        self.status = "Status: ready"
        self.distance = 0
        DEBUG = False
        self.TRIG = 24
        self.ECHO = 23
        self.speed = 40
        self.movetime = 5.0

        if DEBUG != True:
            GPIO.setwarnings(False)

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.TRIG, GPIO.OUT)
        GPIO.setup(self.ECHO, GPIO.IN)

        GPIO.setup(17, GPIO.OUT)
        GPIO.setup(18, GPIO.OUT)
        GPIO.setup(27, GPIO.OUT)
        GPIO.setup(22, GPIO.OUT)
        self.leftforward    = GPIO.PWM(27, 50)
        self.rightbackward  = GPIO.PWM(17, 50)
        self.rightforward   = GPIO.PWM(18, 50)
        self.leftbackward   = GPIO.PWM(22, 50)
        self.findrange()


    def findrange(self):
        return
        GPIO.output(self.TRIG, False)
        sleep(1.5)

        GPIO.output(self.TRIG, True)
        sleep(0.00001)
        GPIO.output(self.TRIG, False)

        while GPIO.input(self.ECHO) == 0:
            pulse_start = time()
        while GPIO.input(self.ECHO) ==1:
            pulse_end = time()
        pulse_duration = pulse_end - pulse_start
        self.distance = pulse_duration * 17150
        self.distance = round(self.distance, 2)

    def stop_(self, event=None):
        self.leftforward.stop()
        self.rightforward.stop()
        self.leftbackward.stop()
        self.rightbackward.stop()
        sleep(0.05)
        self.findrange()
        self.status = "Status: stopped"
        return

    def forward_left(self, event=None):
        self.status= "Status: going forward & left"
        return

    def forward(self, event=None):
        self.leftforward.start(50)
        self.rightforward.start(50)
        self.status = "Status: going forward"
        sleep(self.movetime)
        self.stop_()
        self.status = "Status: stopped"
        return

    def forward_right(self, event=None):
        self.status = "Status: going forward & right"
        return

    def turn_left(self, event=None):
        self.status = "Status: turning left"
        return

    def turn_right(self, event=None):
        self.status = "Status: turning right"
        return

    def backward_left(self, event=None):
        self.status ="Status: going backward & left"
        return

    def backward(self, event=None):
        self.status = "Status: going backward"
        return

    def backward_right(self, event=None):
        self.status = "Status: going backward & right"
        return

    def view(self):
        self.camera.capture( self.img_path )



class ControlPanel(Frame):
    def __init__(self, master, bot:PiBot):
        Frame.__init__(self, master)
        self.master = master

        btn_forward_left = Button(self, text="\\", 
                                  command=bot.forward_left)
        btn_forward_left.grid(column=1, row=1, sticky=(N, W))
        btn_forward = Button(self, text="^", 
                                  command=bot.forward)
        btn_forward.grid(column=2, row=1, sticky=(N))
        btn_forward_right = Button(self, text="/", 
                                  command=bot.forward_right)
        btn_forward_right.grid(column=3, row=1, sticky=(N, E))
        btn_turn_left = Button(self, text="<", 
                                  command=bot.turn_left)
        btn_turn_left.grid(column=1, row=2, sticky=(W))
        btn_stop = Button(self, text="o", 
                                  command=bot.stop_)
        btn_stop.grid(column=2, row=2, sticky=())
        btn_turn_right = Button(self, text=">", 
                                  command=bot.turn_right)
        btn_turn_right.grid(column=3, row=2, sticky=(E))
        btn_backward_left = Button(self, text="/", 
                                  command=bot.backward_left)
        btn_backward_left.grid(column=1, row=3, sticky=(S, W))
        btn_backward = Button(self, text="v", 
                                  command=bot.backward)
        btn_backward.grid(column=2, row=3, sticky=(S))
        btn_backward_right = Button(self, text="\\", 
                                  command=bot.backward_right)
        btn_backward_right.grid(column=3, row=3, sticky=(S, E))

        control_buttons = []

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)
            control_buttons.append(child)

        btn_stop.focus()

        master.bind('<KP_7>', bot.forward_left)
        master.bind('<KP_8>', bot.forward)
        master.bind('<KP_9>', bot.forward_right)
        master.bind('<KP_4>', bot.turn_left)
        master.bind('<KP_5>', bot.stop_)
        master.bind('<KP_6>', bot.turn_right)
        master.bind('<KP_1>', bot.backward_left)
        master.bind('<KP_2>', bot.backward)
        master.bind('<KP_3>', bot.backward_right)

        speed = StringVar(self)
        speed.set("50")
        speed_options = {"10": 10, "20": 20, "30": 30, "40": 40, "50": 50,
                         "60": 60, "70": 70, "80": 80, "90": 90, "100": 100}
        Label(self, text="set speed: ", padding="6 0 0 0").grid(column=1, row=4,
                                                           columnspan=2)
        OptionMenu(self, speed, *speed_options.keys()).grid(column=3, row=4)
        bot.speed = speed_options[speed.get()]
        #bot.speed = 50
        


class StatusPanel(LabelFrame):
    def update_status(self, bot):
        self.tvr_status.set(bot.status)
        self.tvr_range.set("Range: "+str(bot.distance))
        root.after(50, self.update_status, bot)

    def __init__(self, master, bot:PiBot):
        LabelFrame.__init__(self, master, relief=SUNKEN, text="Status Panel")
        self.master = master

        self.tvr_status = StringVar()
        lbl_status = Label(self, textvariable=self.tvr_status, padding="6 0 0 0")
        lbl_status.grid(column=1, row=1, sticky=W,in_=self)
        self.tvr_range = StringVar()
        lbl_range = Label(self, textvariable=self.tvr_range, padding="6 0 0 0")
        lbl_range.grid(column=1, row=2, sticky=W,in_=self)

        self.update_status(bot)

class ImagePanel(Frame):
    def update_image(self, bot:PiBot, lbl:Label):
        bot.view()
        self.img = ImageTk.PhotoImage(Image.open(bot.img_path))
        lbl.configure(image = self.img)
        root.after(500, self.update_image, bot, lbl)

    def __init__(self, master, bot:PiBot):
        Frame.__init__(self, master)
        self.master = master
        bot.view()
        self.img = ImageTk.PhotoImage(Image.open(bot.img_path))
        lbl_img = Label(self, image = self.img, padding="6 12 6 6")
        lbl_img.grid(column=1, row=0, sticky=W, in_=self)
        self.update_image(bot, lbl_img)


class PibotControlGUI(Frame):
    def __init__(self, master, bot):
        Frame.__init__(self, master)
        self.master = master
        frm_left = Frame(self, padding="3 3 3 3")
        frm_left.grid(column=1, row=1, sticky=(N))
        frm_right = Frame(self, padding="3 3 3 3")
        frm_right.grid(column=2, row=1, sticky=(N, S, E, W))
        
        control_panel = ControlPanel(frm_left, bot)
        control_panel.grid(column=1, row=1, sticky=(N, W, E, S))
        status_panel = StatusPanel(frm_left, bot)
        status_panel.grid(column=1, row=2, sticky=(N, W, E, S))
        view_panel = ImagePanel(frm_right, bot)
        view_panel.grid(column=1, row=1, sticky=(N, W, E, S))
        


if __name__ == '__main__':
    bot = PiBot()
    root = Tk()
    root.title("PiBot Control Centre")
    PibotControlGUI(root, bot).grid(column=0, row=0, sticky=(N, S, E, W))
    root.mainloop()



"""


















"""

