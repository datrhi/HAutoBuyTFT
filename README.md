# HAutoBuyTFT
Auto Buy TFT LOL using OCR
Grab screen method : py mss
OCR : py tesseract

five_box: better but using 5 times tesseract instead of 1 time per a scanning

processing image before using py tesseract: convert to grayscale -> enhance contrast

champions.txt: contain all champions belong to a set (in this project is set 4.5)

comps.txt: contain comps with format: 
comps1name \n champion1 champion2 ... \n comps2name \n champion1 champion2 ... ...

hieu.py: Run as admin command prompt 
py hieu.py (comps name)

hieuui.py (GUI version): Run as admin command prompt
py hieuui.py

install dependencies: 
cd (folder contain this repo)
py -m pip install -r requirements.txt