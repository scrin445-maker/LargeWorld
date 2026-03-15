import json
import os
import shutil

CURRENT_WORKING_DIRECTORY = os.getcwd()

if __name__ == '__main__':

    for file in os.scandir(CURRENT_WORKING_DIRECTORY):
        if os.path.isfile(file):
            filename, fileext = os.path.splitext(file.path)

            if fileext != '.json':
                continue
            
            with open(file, 'r+') as f:
                data = json.load(f)
                data["loader"] = "fusion:model"
                data["type"] = "base"
                f.seek(0)
                json.dump(data, f, indent=4)
