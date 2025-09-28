import stat
import os
import requests
import zipfile
import shutil
from io import BytesIO
from modules.misc.messageBox import msgBox

#merge 2 folders together
#if the item already exists, do not replace it
def merge(scr_path, dir_path):
  files = next(os.walk(scr_path))[2]
  folders = next(os.walk(scr_path))[1]
  for file in files: # Copy the files
    scr_file = scr_path + "/" + file
    dir_file = dir_path + "/" + file
    if not os.path.exists(dir_file):
        shutil.copy(scr_file, dir_file)
  for folder in folders: # Merge again with the subdirectories
    scr_folder = scr_path + "/" + folder
    dir_folder = dir_path + "/" + folder
    if not os.path.exists(dir_folder): # Create the subdirectories if dont already exist
      os.mkdir(dir_folder)
    merge(scr_folder, dir_folder)

def update(t = "e"):
    msgBox("Update in progress", "Updating... Do not close terminal")
    protectedFolders = ["settings"] #folders that should not be replaced
    protectedFiles = [".git"] #files that should not be replaces
    destination = os.getcwd().replace("/src","") #the target folder to replace the files. Should be the parent directory of the /src folder
    
    link = "https://github.com/existancepy/bss-macro-py/archive/master.zip"
    source = f"{destination}/bss-macro-py-main"
    e_macroPath = f"{destination}/e_macro.command"
    
    if t == "e":
        link = "https://github.com/existancepy/bss-macro-py/archive/refs/heads/experimental.zip"
        source = f"{destination}/bss-macro-py-experimental"

    print(os.listdir(destination))
    #delete all files
    for f in os.listdir(destination):
        if f in protectedFolders or f in protectedFiles: continue
        if "." in f:
            os.remove(f"{destination}/{f}")
        else:
            shutil.rmtree(f"{destination}/{f}")

    #download new files
    req = requests.get(link)
    zipf= zipfile.ZipFile(BytesIO(req.content))
    zipf.extractall(destination)
    files = os.listdir(source)
    
    #move the files from the download folder to the source folder
    for file in files: 
        if file in protectedFiles: continue
        file_name = os.path.join(source, file) 
        if file in protectedFolders: #merge the contents of the folders
            merge(file_name, f"{destination}/{file}")
        else:
            shutil.move(file_name, destination) 
    print("Files Moved")
    
    #delete the download folder
    shutil.rmtree(source)
    
    #set execute permission for e_macro.command
    st = os.stat(e_macroPath)
    os.chmod(e_macroPath, st.st_mode | stat.S_IEXEC)
    
    msgBox("Update success", "Update complete. You can now relaunch the macro")
