import logging
logging.basicConfig(filename = "macroLogs.log", filemode = "a", format = '%(message)s')

def log(msg):
    logging.warning(str(msg))

