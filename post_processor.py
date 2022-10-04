from email.mime import image
from enum import Enum
from PIL import Image 

class TileType(Enum):
    T = "T"
    F = "F"
    P = "P"
    R = "R"

    def __str__(self):
        return self.value

    def __add__(self, x):
        return self.value + x.value

mapTiles = [[TileType.F, TileType.F, TileType.F, TileType.R], [TileType.F, TileType.F, TileType.F, TileType.T], [TileType.F, TileType.F, TileType.F, TileType.F],
          [TileType.F, TileType.R, TileType.F, TileType.F], [TileType.F, TileType.T, TileType.T, TileType.F], [TileType.T, TileType.F,TileType.F, TileType.F]]

def tileToImage(tileType: list):
    fileName = ""
    for type in tileType:
        fileName += type.value
    img = Image.open("./TileImages/" + fileName + ".png")
    return img


# Got it from StackOverflow (proper ref TODO)
def image_grid(imgs, rows, cols):
    assert len(imgs) == rows*cols

    w, h = imgs[0].size
    grid = Image.new('RGB', size=(cols*w, rows*h))
    grid_w, grid_h = grid.size
    
    for i, img in enumerate(imgs):
        grid.paste(img, box=(i%cols*w, i//cols*h))
    return grid

if __name__ == "__main__":
    images = list(map(tileToImage, mapTiles))
    grid = image_grid(images, 2, 3)
    grid.show()
