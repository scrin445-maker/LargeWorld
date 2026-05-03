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



if __name__ == "__main__":

    # Create output resourcepack
    for pack in os.listdir("./src/input"):
        output = "./src/output/{}/assets/optifine/ctm/".format(pack)
        os.makedirs(output, exist_ok=True)
    
        # Walk input folder for resourcepacks
        for root, dirs, files in os.walk("./src/input/{}".format(pack)):
            
            # Look for textures
            for infile in files:
                if infile.endswith(".png"):
                    
                    texture_name = infile.replace(".png", "")
                    texture = Image.open(os.path.join(root, infile))
                    output += texture_name
                    texturemap = []

                    os.makedirs(output)

                    # Crop starting from the upper left
                    for y in range(2):
                        for x in range(2):
                            box = [x * 8, y * 8, 8 * (x + 1), 8 * (y + 1)]
                            texturemap.append(texture.crop(box))
                    
                    # Continuity starts from the bottom left so name tiles appropriately        
                    texturemap[2].save(output + "/0.png")
                    texturemap[3].save(output + "/1.png")
                    texturemap[0].save(output + "/2.png")
                    texturemap[1].save(output + "/3.png")
                    
                    with open(output + "/{}.properties".format(texture_name), "w") as f:
                        f.write("matchTiles={}\nmethod=repeat\ntiles=0-4\n".format(texture_name))
                        f.close()
