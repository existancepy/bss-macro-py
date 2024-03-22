
import os
import requests
import zipfile
import shutil
from io import BytesIO

def update(t = "m"):
    destination = os.getcwd().replace("/macro","")
    
    link = "https://github.com/existancepy/bss-macro-py/archive/master.zip"
    source = f"{destination}/bss-macro-py-main"
    
    if t == "e":
        link = "https://github.com/existancepy/bss-macro-py-experimental/archive/master.zip"
        source = f"{destination}/bss-macro-py-experimental-main"

    print(os.listdir(destination))
    for f in os.listdir(destination):
        if "." in f:
            os.remove(f"{destination}/{f}")
        else:
            shutil.rmtree(f"{destination}/{f}")
    req = requests.get(link)
    zipf= zipfile.ZipFile(BytesIO(req.content))
    zipf.extractall(destination)
    files = os.listdir(source) 
    for file in files: 
        file_name = os.path.join(source, file) 
        shutil.move(file_name, destination) 
    print("Files Moved")
    shutil.rmtree(source)
    print("Update complete. You can now relaunch the macro")
