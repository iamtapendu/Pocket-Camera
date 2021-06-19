from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
from datetime import datetime
import cv2 as cv
import os

class VideoRecorder:
    def __init__(self, window, source=0):
        self.window = window
        self.cap = cv.VideoCapture(source)
        self.time_now = datetime.now()

        # Configure Window
        self.window.rowconfigure(0, weight=9)
        self.window.columnconfigure(0, weight=1)

        self.window.rowconfigure(1, weight=1)


        # Checking for video source is currectly open or not
        if self.cap.isOpened():

            # Assigning the essential values
            self.width = self.cap.get(cv.CAP_PROP_FRAME_WIDTH)
            self.height = self.cap.get(cv.CAP_PROP_FRAME_HEIGHT)
            self.fps = self.cap.get(cv.CAP_PROP_FPS)
            self.delay = int(1000/self.fps)

            self.save_flag = False
            self.fourcc = cv.VideoWriter_fourcc(*'XVID')
            self.path = os.path.join(os.getcwd(),'Media','')
            self.file_name = str(self.path+'video_'+self.time_now.strftime('%d-%m-%y_%X')+'.avi')
            self.record = cv.VideoWriter(self.file_name, self.fourcc, self.fps, (1024, 768), True)


            # defining two frame for the canvas and placed it
            self.canvas_frame = Frame(self.window, bg='#111', pady=10, padx=10, bd=0)
            self.canvas_frame.grid(row=0, column=0, sticky=NSEW)

            self.button_frame = Frame(self.window, bg='#222', padx=10, pady=10, bd=0)
            self.button_frame.grid(row=1, column=0, sticky=NSEW)

            # Configure frame
            # Canvas Frame
            self.canvas_frame.rowconfigure(0, weight=1)
            self.canvas_frame.columnconfigure(0, weight=1)

            # Button frame
            self.button_frame.columnconfigure(0,weight=1)
            self.button_frame.columnconfigure(1,weight=1)
            self.button_frame.columnconfigure(2,weight=1)

            # Defining the Canvas and placed it on the frame
            self.canvas = Canvas(self.canvas_frame,
                                 width=self.width,
                                 height=self.height,
                                 bg='#111',
                                 highlightbackground='#111',
                                 highlightthickness=2,
                                 bd=0)
            self.canvas.grid(row=0, column=0, sticky=NSEW)

            # Creating Snapshot Button
            self.snap_btn, self.snap_img = self.createButton(self.button_frame,
                                                             'Icons/snapshot.png',
                                                             self.snapshot)
            self.snap_btn.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)

            # Creating Play Button
            self.play_pause_btn, self.play_img = self.createButton(self.button_frame,
                                                                   'Icons/play.png',
                                                                   self.save)
            self.play_pause_btn.grid(row=0, column=1, padx=10, pady=10, sticky=NSEW)

            self.pause_img = Image.open('Icons/pause.png')
            self.pause_img = ImageTk.PhotoImage(self.pause_img.resize((64, 64), Image.ANTIALIAS))

            # Creating Stop Button
            self.stop_btn, self.stop_img = self.createButton(self.button_frame,
                                                             'Icons/stop.png',
                                                             self.stop)
            self.stop_btn.grid(row=0, column=2, padx=10, pady=10, sticky=NSEW)

            # Calling the updateFrame for showing the video feed continuously
            self.updateFrame()
        else:
            # Show the error
            messagebox.showerror('No Video Feed', 'Program can\'t open the camera or the video file :(')

            # destroy the main window and exit from the program
            self.window.destroy()

    def updateFrame(self):
        # taking the each frame numpy array mode
        ret, self.img_arr = self.cap.read()
        # Create time stamp
        self.time_now = datetime.now()

        # Updating width and height
        self.width = 640 if self.window.winfo_width() < 1100 else 752
        self.height = 480 if self.window.winfo_width() < 1100 else 564

        # updating canvas
        self.canvas.config(width=self.width, height=self.height)

        # Checking if frame is available or not
        if ret:
            self.image = cv.cvtColor(self.img_arr, cv.COLOR_BGR2RGB)
            self.image = cv.resize(self.image, (self.width, self.height))
            self.image = Image.fromarray(self.image)
            self.image = ImageTk.PhotoImage(self.image)

            self.canvas.create_image(int(self.window.winfo_width()/2), 0, image=self.image, anchor=N)

            if self.save_flag :
                self.img_arr = cv.resize(self.img_arr,(1024,768))
                self.record.write(self.img_arr)

            self.window.after(self.delay, self.updateFrame)
        else:
            # destroy the main window and exit from the program
            self.window.destroy()

    def onEnter(self, e):
        e.widget['background'] = '#333'

    def onLeave(self, e):
        e.widget['background'] = '#222'

    def createButton(self, window, logo, command, color='#222'):
        # Loading and resize the button logo
        logo = Image.open(logo)
        logo = logo.resize((64, 64), Image.ANTIALIAS)
        logo = ImageTk.PhotoImage(logo)

        # Defining and placing the snapshot button
        btn = Button(window,
                     image=logo,
                     relief=FLAT,
                     bg=color,
                     bd=0,
                     highlightbackground=color,
                     activebackground='#333',
                     command=command,
                     )
        # Binding Enter and leave event for Hover effect
        btn.bind("<Enter>", self.onEnter)
        btn.bind("<Leave>", self.onLeave)

        return btn, logo

    def snapshot(self):
        snap_file = str(self.path+'snapshot_'+self.time_now.strftime('%d-%m-%y_%X')+'.png')
        cv.imwrite(snap_file,self.img_arr)

    def save(self):
        self.save_flag = not(self.save_flag)
        if self.save_flag:
            self.play_pause_btn.config(image=self.pause_img)
        else:
            self.play_pause_btn.config(image=self.play_img)

    def stop(self):
        self.save_flag = False
        self.file_name = str(self.path+'video_'+self.time_now.strftime('%d-%m-%y_%X')+'.avi')
        self.play_pause_btn.config(image=self.play_img)


if __name__ == '__main__':
    root = Tk()
    root.config(bg='#222')
    root.iconphoto(False,PhotoImage(file='Icons/camera.png'))
    root.title('Video Recoder')
    root.geometry('1000x600')
    try:
        os.mkdir(os.path.join(os.getcwd()+'Media'))
    except OSError:
        pass
    app = VideoRecorder(root,)

    root.mainloop()
