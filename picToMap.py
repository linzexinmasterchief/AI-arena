import numpy as np
from PIL import Image

def generateMap(map):
    im = Image.open(map)
    im = im.transpose(Image.FLIP_TOP_BOTTOM)
    im = im.convert("L")
    data = im.getdata()
    data = np.ndarray.tolist(np.matrix(data).reshape(100,100))
    
    return data