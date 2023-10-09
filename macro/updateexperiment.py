
import os
import requests
import zipfile
from io import BytesIO
import shutil
from distutils.dir_util import copy_tree

def update():
    files = [x for x in os.listdir("./") if x[-2:] ==  "py" and x!= "updateexperiment.py" ]

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
        if i not in ['images','theme']:
            shutil.copyfile("./bss-macro-py-experimental-main/{}".format(i), "./{}".format(i))
        else:
            copy_tree("./bss-macro-py-experimental-main/{}".format(i), "./{}".format(i))
    shutil.rmtree('./bss-macro-py-experimental-main')
    print('Experimental Update complete. You can now relaunch the macro. To return to the main macro, click the "update" button')
