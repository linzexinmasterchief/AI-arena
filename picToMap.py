import numpy as np
from PIL import Image

def generateMap(map, size_x, size_y):
    try:
        im = Image.open(map)
    except:
        print("graph not find")
        return
    im = im.transpose(Image.FLIP_TOP_BOTTOM)
    im = im.convert("L")
    data = im.getdata()
    data = np.ndarray.tolist(np.matrix(data).reshape(size_x, size_y))
    
    return data