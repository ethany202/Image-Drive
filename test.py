from PIL import Image
import os


rel = "static\personalImages\MemeYaranaika.png"
dir = os.path.dirname(__file__)

complete_path = os.path.join(dir, str(rel))
im = Image.open(complete_path)

im.show()

