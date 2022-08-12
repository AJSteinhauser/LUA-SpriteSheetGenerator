
import os

from PIL import Image
IMAGE_SIZE = [1024, 1024];


BANNER = "\033[0;36mWelcome to reteach's SpriteSheet Generator...\033[0m"""

class node:
    def __init__(self, position, size):
        self.image = None
        self.size = size; 
        self.position = position;
        self.down = None;
        self.right = None;


def sortImages(images):
    images.sort(key=lambda img: img.size[0] * img.size[1], reverse=True)#Sort all images by total area width * height 

def loadImages(path):
    sprites = [];
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path):
            try:
                print("\033[0;32mLoading: \033[4;34m" + file + "\033[0m")
                sprites.append(Image.open(file_path))
            except:
                raise Exception("Failed to open " + file_path);
    return sprites;

def findTreeSpotHelper(node, img):
    if node.image is not None:
        return findTreeSpotHelper(node.right, img) or findTreeSpotHelper(node.down, img)
    elif (node.size[0] >= img.size[0] and node.size[1] >= img.size[1]):
        return node;
    else:
        return None;

def findTreeSpot(trees, img):
    node = None;
    for tree in trees: 
        node = findTreeSpotHelper(tree, img)
        if node:
            break;
    if node:
        return node;
    else:
        node = node([0,0],image_size[:])
        trees.append(node);
        return node;


def buildTree(trees, sprites):
    for img in sprites:
        if img.size[0] > IMAGE_SIZE[0] or img.size[1] > IMAGE_SIZE[1]:
            raise Exception("All images must be <= 1024 pixels in both axes" + img.filename + " is too big")
        else:
            node = findTreeSpot(trees, img)
            node.image = img;
            node.right = node(
                    [node.img.size[0] + node.position[0],node.position[1]],
                    [IMAGE_SIZE[0] - node.img.size[0] - node.position[0], node.img.size[1]]
            ) 
            node.down = node(
                    [node.position[0], node.img.size[1] + node.position[1]],
                    [ ]
            )

def packSprites(path):
    sprites = loadImages(path)
    sortImages(sprites)

def getName():
    name = input("Enter a name for the output spritesheet(s)\033[0;33m (Leave blank for default)\033[0m: ")
    return name if name != "" else "untitled"

def getImageFolder():
    #spritesFolder = os.path.exists("./Sprites") if 
    while not os.path.exists("./Sprites"):
        print("\033[0;31mSprite folder not found\033[0m")   
        print("Please create a folder named \033[0;31m\"Sprites\"\033[0m in the parent directory \033[0;33m(This folder should contain the images you want on the spritesheet)\033[0m")
        print("\033[0;33m" + os.getcwd() + "\033[0;31m/Sprites\033[0m")
        input("Press \033[0;32mEnter\033[0m to continue...")
    print("\033[0;32mSprite folder found\033[0m")
    return "./Sprites"


def init():
    print(BANNER)
    


def main():
    init()
    getName()
    path = getImageFolder()
    sprites = packSprites(path)
#packSprites("./test_images");:wqq


main()
