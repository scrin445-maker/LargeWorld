import os
from PIL import Image
import shutil

# 1. Unpack resourcepacks if .zip files
# 2. Create output resourcepack
# 3. Scan resourcepacks for textures
# 3.5. Ignore certain textures based on an overrides.json
# 4. Create folders for each textures in output resourcepack
# 5. Splice textures into 4 tiles
# 6. Store in matching folder in output
# 6.5. Group folders together based on a group.json file

INPUT_DIR = './src/input'
OUTPUT_DIR = './src/output'


def getResourcepacks(inputDir):
    resourcepacks = []
    for pack in os.listdir(inputDir):
        resourcepacks.append(pack)
        print("Resourcepack", pack, "found.", sep=" ")
    return resourcepacks


def getTextures(resourcepack, inputDir, outputDir):
    textures = []

    pack = inputDir + '/' + resourcepack
    
    for root, dirs, files in os.walk(pack):
        for infile in files:
            if str(infile).endswith(".png"):
                textures.append(infile)
    
    return textures


def generateContinuity(resourcepack, inputDir, outputDir):
    
    # Create output dir
    try:
        os.makedirs(outputDir, exist_ok=False)
        print("Created ./src/output folder.")
    except OSError:
        print("./src/output folder already exists.")

    textures = getTextures(resourcepack, inputDir, outputDir)
    rootDir = "{}/{}/assets/minecraft/textures/block".format(inputDir, resourcepack)
    outputResourcepack = "{}/{}/assets/minecraft/optifine/ctm/".format(outputDir, resourcepack)
    
    for texture in textures:
        texture_name = texture.replace(".png", "")
        texture_file = Image.open(os.path.join(rootDir, texture))
        texture_map = []
        out_folder = outputResourcepack + texture_name
        
        os.makedirs(out_folder, exist_ok=True)
        
        for y in range(2):
            for x in range(2):
                box = [x * 8, y * 8, 8 * (x + 1), 8 * (y + 1)]
                texture_map.append(texture_file.crop(box))
        
        # Continuity starts from the bottom left so name tiles appropriately        
        texture_map[2].save(out_folder + "/0.png")
        texture_map[3].save(out_folder + "/1.png")
        texture_map[0].save(out_folder + "/2.png")
        texture_map[1].save(out_folder + "/3.png")
        
        with open(out_folder + "/{}.properties".format(texture_name), "w") as f:
            f.write("matchTiles={}\nmethod=repeat\nwidth=2\nheight=2\ntiles=0-3\n".format(texture_name))
            f.close()
        
    return


if __name__ == "__main__":

    resourcepacks = getResourcepacks(INPUT_DIR)
    for resourcepack in resourcepacks:
        test = generateContinuity(resourcepack, INPUT_DIR, OUTPUT_DIR)