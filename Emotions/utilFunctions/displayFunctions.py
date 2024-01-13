import os
import re
from PIL import Image, ImageSequence
from luma.core.sprite_system import framerate_regulator
from time import sleep

class DisplayFunctions:

    def __init__(self,device):
        self.device = device

    def gif_display(self,path):
        # get gif from path
        regulator = framerate_regulator(fps=30)
        img_path = str(path)
        banana = Image.open(img_path)
        while True:
            for frame in ImageSequence.Iterator(banana):
                with regulator:
                    # invert colors
                    frame = Image.eval(frame, lambda x: 255 - x)
                    self.device.display(frame.convert(self.device.mode))

                    
                    


    def pngs_display(self,path,frame_rate=0):
        # display all png in the path according to the order of the file name (e.g. blink (1).png, blink (2).png)
        assets_dir = str(path)
        # get all png in the path in sorted order
        files = sorted([os.path.join(assets_dir, file) for file in os.listdir(assets_dir) if re.match(r'.*\.png', file)])
        for file in files:
            # print(file)
            img = Image.open(file)
            # invert colors
            img = Image.eval(img, lambda x: 255 - x)
            self.device.display(img.convert(self.device.mode))
            sleep(frame_rate)
    
    def pngs_display_rev(self,path,frame_rate=0):
        # display all png in the path according to the order of the file name (e.g. blink (1).png, blink (2).png)
        assets_dir = str(path)
        # get all png in the path in sorted order
        files = sorted([os.path.join(assets_dir, file) for file in os.listdir(assets_dir) if re.match(r'.*\.png', file)])
        for file in files:
            # print(file)
            img = Image.open(file)
            # invert colors
            img = Image.eval(img, lambda x: 255 - x)
            self.device.display(img.convert(self.device.mode))
            sleep(frame_rate)
            
        files.reverse()
        for file in files:
            # print(file)
            img = Image.open(file)
            # invert colors
            img = Image.eval(img, lambda x: 255 - x)
            self.device.display(img.convert(self.device.mode))
            sleep(frame_rate)
        

    def png_display(self,path):
        # display a single png
        img_path = str(path)
        img = Image.open(img_path)
        # invert colors
        img = Image.eval(img, lambda x: 255 - x)
        self.device.display(img.convert(self.device.mode))
