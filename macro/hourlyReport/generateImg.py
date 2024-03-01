'''
from html2image import Html2Image
hti = Html2Image()
hti.screenshot(
    html_file='index.html', save_as='page2.png'
)
'''

with open("index.html") as f:
    data = [x.strip() for x in f.read().split("\n")]
    print(data)
f.close()
