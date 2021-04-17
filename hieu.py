#!/usr/bin/env python3

from PIL import Image, ImageOps, ImageEnhance    # Image manipulation
import pyautogui                    # Mouse control
import pytesseract                  # OCR
import time
import sys
import re
import ctypes
import mss
import PIL.ImageGrab
import keyboard
from time import sleep
import tempfile
from textblob import TextBlob
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def pos(x, y):
    ctypes.windll.user32.SetCursorPos(x, y)
    
def click():
    ctypes.windll.user32.mouse_event(2, 0, 0, 0,0) # left down
    sleep(0.01)
    ctypes.windll.user32.mouse_event(4, 0, 0, 0,0) # left up
    
def getChampions():
    file = open('champions.txt', 'r')
    champions = { c: c for c in file.read().split('\n') }
    #champions = file.read()
    file.close()

    return champions

allChampions = getChampions()

def getComps(compsName):
    f = open('comps.txt', 'r')
    comps = [ c for c in f.read().split('\n') ]
    compsN = compsName[0]
    f.close()
    indices = (comps.index(compsN)+1) if compsN in comps else -1
    mComps = comps[indices]

    return mComps

def five_box(roi):
	w, h = roi.size
	count = 0
	available = []
	tmp = []
	while(count<5):
		img = roi.crop((count*(w/5),0,(count+1)*(w/5),h))
		tmp = [c for c in re.split(r'([A-Z][a-z]+)', pytesseract.image_to_string(img)) if c and c in allChampions]
		if not tmp:
			available.append("none")
		else:
			available.append(tmp[0])
		count = count + 1
		tmp  = []
	return available

def set_image_dpi(image):
    """
    Rescaling image to 300dpi without resizing
    :param image: An image
    :return: A rescaled image
    """
    image_resize = image
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    temp_filename = temp_file.name
    image_resize.save(temp_filename, dpi=(300, 300))
    return temp_filename

def grabScr(coordinates):
        with mss.mss() as sct:
            sct_img = sct.grab(coordinates)
            # Convert to PIL/Pillow Image
            im = PIL.Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')
            enhancer = ImageEnhance.Contrast(im);
            im_output = enhancer.enhance(1.5)
            return im_output
        
def transformImage(roi):
    # Convert image to grayscale and invert colors
    return ImageOps.invert(roi.convert('L'))

def main():

    selectedComps = sys.argv[1:]
    #selectedComps = ["Songdau"]
    selectedChampions = getComps(selectedComps)
    
    selectedChampions = list(selectedChampions.split())
    
    print("Selected champions: ", selectedChampions)

    # Get screen's width/height
    width, height = pyautogui.size()

    # ROI factors of the champion zone starting top left
    left, top, right, bottom = (int(width * 0.25), int(height * 0.96), int(width * 0.77), int(height * 0.99))
    coordinates = (left, top, right, bottom)

    while (1):
        # Take a screenshot and apply transformations to pixels
        roi = transformImage(grabScr(coordinates))

        # Handles text recognition using PyTesseract and get only correct champions
        text = pytesseract.image_to_string(roi)
        
        availableChampions = [c for c in re.split(r'([A-Z][a-z]+)', text) if c and c in allChampions]
        print("Detected available champions: ", availableChampions)

        # Compare champions found and selected, then mouve mouse and click accordingly
        matches = set(availableChampions).intersection(selectedChampions)

        if matches: 
            print("These champions are on your wishlist: ", matches)
            panelWidth, panelHeight = ((right - left) / 5, bottom - top)

            for match in matches:
                indices = [i for i, mChamp in enumerate(availableChampions) if mChamp == match]
                for hx in indices:
                    x, y = (int(left + panelWidth / 2 + (panelWidth * hx)), int(top - panelHeight / 1.1))
                    print("Moving mouse to location [", x, " ; ", y, "]")
                    pos(x,y)
                    click()
                    sleep(0.02)
       
        else:
            print("No matches found")
    
    return

if __name__ == "__main__":
    main()
