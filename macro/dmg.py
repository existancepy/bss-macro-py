from setuptools import setup

APP = ["e_macro.py"]
DATA_FILES = ['save.txt','discord.log','macroLogs.log','timings.txt','settings.txt','plantertimings.txt','plantersettings.txt','planterdata.txt','nectartimes.txt','natro_ba_config.txt','multipliers.txt','haste.txt','canonfails.txt']
OPTIONS = {
    'argv_emulation':True,

}

setup = (
    app = APP,
    data_files = DATA_FILES
    options = {'py2app':OPTIONS},
    setup_requires=['py2app']
    

)
