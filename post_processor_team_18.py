from email.mime import image
from enum import Enum
from typing import Counter
from PIL import Image 
import os
from os.path import exists
import asyncio
from minizinc import Instance, Model, Solver

# Session Parameters
rows = 7
cols = 12
numberOfSolutions = 5
shouldGenerateImages = True
shouldShowImages = False
datafile = f"./Instances/main_{rows}_{cols}.dzn"

# Load carcasonne model from file
carcasonne = Model("./carcassonne.mzn")
# Find the MiniZinc solver configuration for Gecode
gecode = Solver.lookup("picat")
# Create an Instance of the carcasonne model for Gecode
instance = Instance(gecode, carcasonne)
# Assign dzn
instance.add_file(datafile, False)
# Run the instance with a specified number of solutions
results = instance.solve(nr_solutions=5)

class TileType(Enum):
    T = "T"
    F = "F"
    P = "P"
    R = "R"
    def __str__(self):
        return self.value
    def __add__(self, x):
        return self.value + x.value

# find corresponding png and compute rotation at runtime
def tileToImage(tileType: list):
    fileName = ""
    for type in tileType:
        fileName += type
    fileName1 = fileName[1:]+fileName[:1]
    fileName2 = fileName[2:]+fileName[:2]
    fileName3 = fileName[3:]+fileName[:3]
    if(exists("./TileImages/"+fileName+".png")):
        img = Image.open("./TileImages/" + fileName + ".png")
        return img
    elif(exists("./TileImages/"+fileName1+".png")):
        img = Image.open("./TileImages/" + fileName1 + ".png")
        img = img.rotate(270)
        return img
    elif(exists("./TileImages/"+fileName2+".png")):
        img = Image.open("./TileImages/" + fileName2 + ".png")
        img = img.rotate(180)
        return img
    elif(exists("./TileImages/"+fileName3+".png")):
        img = Image.open("./TileImages/" + fileName3 + ".png")
        img = img.rotate(90)
        return img
    else:
        return Image.open("./TileImages/FFFF.png")
    
def image_grid(imgs, rows, cols):
    assert len(imgs) == rows*cols
    w, h = imgs[0].size
    grid = Image.new('RGB', size=(cols*w, rows*h))
    for i, img in enumerate(imgs):
        grid.paste(img, box=(i%cols*w, i//cols*h))
    return grid

def generate_images(shouldShow):
    counter = 0
    for r in range(len(results)):
        counter += 1
        mapTiles = results[r, 'Map']
        tile_list = []
        for row in mapTiles:
            for tile in row:
                tile_list.append(tile)
        mapTiles = tile_list
        images = list(map(tileToImage, mapTiles))
        grid = image_grid(images, rows=rows, cols=cols)
        if shouldShow:
            grid.show()
        grid = grid.save(f"./OutputImages/output_{counter}.png", "png")

def show_stats():
    print(f"Number of Solutions: {numberOfSolutions}\nSolving Time: {results.statistics['time']}")

if __name__ == "__main__":
    show_stats()
    if shouldGenerateImages:
        generate_images(shouldShow=shouldShowImages)
