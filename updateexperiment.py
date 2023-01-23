
import os
import requests
import zipfile
from io import BytesIO
import shutil
from distutils.dir_util import copy_tree

def update():
    files = [x for x in os.listdir("./") if x[-2:] ==  "py" and  x!= "update.py" and x!= "updateexperiment.py" ]
    print(files)

    for f in files:
        os.remove("./{}".format(f))

    try:
        shutil.rmtree('./images')
    except:
        pass
    filepath = os.getcwd()
    req = requests.get('https://github.com/existancepy/bss-macro-py-experimental/archive/master.zip')
    zipf= zipfile.ZipFile(BytesIO(req.content))
    zipf.extractall(filepath)

    newfiles = os.listdir("./bss-macro-py-experimental-main")
    for i in newfiles:
        if i != "images":
            shutil.copyfile("./bss-macro-py-experimental-main/{}".format(i), "./{}".format(i))
        else:
            copy_tree("./bss-macro-py-experimental-main/images", "./images")
    shutil.rmtree('./bss-macro-py-main')
