import tkinter 
from PIL import Image, ImageTk
import cv2


class GUI:
    def __init__(self):
        self.root = tkinter.Tk()
        self.app = tkinter.Frame(self.root, bg="white")
        self.main = tkinter.Label(self.app)
        img = cv2.imread('Source/Images/1.png')
        self.originalTk = imageToTkPhoto(img)
        self.depthImageTk = imageToTkPhoto(img)

    def setup(self):
        #root = tkinter.Tk()
        #app = tkinter.Frame(root, bg="white")

        self.app.grid()
        self.main = tkinter.Label(self.app)
        self.main.grid()

        self.main.imgtk = self.originalTk
        self.main.configure(image=self.originalTk)
        self.root.after(1, update())
        self.root.mainloop()
        print('finished setting up gui')

    def updateImages(self, original, depthImage):
        print('updating the images')
        self.originalTk = imageToTkPhoto(original)
        self.depthImageTk = imageToTkPhoto(depthImage)

    def update(self):
        print('updating gui')
        self.main.imgtk = self.originalTk
        self.main.configure(image=self.originalTk)

def showImages(original, depthImage, fps):
    originalTk = imageToTkPhoto(original)
    depthImageTk = imageToTkPhoto(depthImage)
    #canvas = Canvas(root, width = 1000, height = 1000)
    #canvas.pack()
    #canvas.create_image(20, 20, anchor=NW, image=original)
    #lmain = tkinter.Label(root, image=originalTk).pack()
    #lmain.grid()
    lmain.imgtk = originalTk
    lmain.configure(image=originalTk)


def imageToTkPhoto(img):
    img = Image.fromarray(img)
    return ImageTk.PhotoImage(image=img)
