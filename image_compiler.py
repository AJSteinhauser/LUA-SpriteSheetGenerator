
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
                loadedImage = Image.open(file_path)
                sprites.append(loadedImage)
            except:
                print("\033[0;31mFailed to open:\033[0;34m " + file + " \033[0;33m(PNG files work best with this program) \033[0m")
    return sprites;

def findTreeSpotHelper(node, img):
    if node.image is not None:
        return findTreeSpotHelper(node.right, img) or findTreeSpotHelper(node.down, img)
    elif (node.size[0] >= img.size[0] and node.size[1] >= img.size[1]):
        return node;
    else:
        return None;

def findTreeSpot(trees, img):
    found = None;
    for tree in trees: 
        found = findTreeSpotHelper(tree, img)
        if found:
            break;
    if found:
        return found;
    else:
        found = node([0,0],IMAGE_SIZE[:])
        trees.append(found)
        return found

def getImageSize(current):
    if current is None:
        return [0,0]
    if current.image is None:
        return [0,0]
    right = getImageSize(current.right)
    down = getImageSize(current.down)
    
    curExtent = [current.image.size[0] + current.position[0], current.image.size[1] + current.position[1]];
    return [max(curExtent[0],right[0],down[0]), max(curExtent[1],right[1],down[1])]


def packImagesRecursive(current, spriteSheet):
    if current is None:
        return
    if current.image is None:
        return
    spriteSheet.paste(current.image, box=(current.position[0],current.position[1]))
    packImagesRecursive(current.right, spriteSheet);
    packImagesRecursive(current.down, spriteSheet);


def packImages(trees,name):
    for idx,tree in enumerate(trees):
       size = getImageSize(tree)
       print("Spritesheet " + str(idx) + " will be " + str(size) + " pixels")
       spriteSheet = Image.new(mode="RGBA", size=(size[0],size[1]))
       packImagesRecursive(tree,spriteSheet)
       if len(trees) == 1:
           idx = ""
       spriteSheet.save(os.path.abspath(".") + "/"  + name + str(idx) + ".png")
       print("\033[0;32m Image wrote to: \033[0;34m" + os.path.abspath(".") + "/"  + name + str(idx) + ".png\033[0m")
       spriteSheet.show();


def buildTree(trees, sprites):
    print("Building tree...")
    for img in sprites:
        if img.size[0] > IMAGE_SIZE[0] or img.size[1] > IMAGE_SIZE[1]:
            raise Exception("All images must be <= 1024 pixels in both axes" + img.filename + " is too big")
        else:
            foundNode = findTreeSpot(trees, img)
            foundNode.image = img;
            foundNode.right = node(
                    [foundNode.position[0] + img.size[0], foundNode.position[1]], #Position
                    [foundNode.size[0] - img.size[0], img.size[1]] #Size
            ) 
            foundNode.down = node(
                    [foundNode.position[0], foundNode.position[1] + img.size[1]],#Position
                    [foundNode.size[0], foundNode.size[1] - img.size[1]] #Size
            )

def loadSprites(path):
    sprites = loadImages(path)
    sortImages(sprites)
    return sprites

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
    name = getName()
    path = getImageFolder()
    sprites = loadSprites(path)
    trees = []
    buildTree(trees,sprites)
    packImages(trees,name)

#packSprites("./test_images");:wqq


main()
