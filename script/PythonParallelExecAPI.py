# Python Parallelism API 
# Author : Sreejith Menon
# Email : smenon8@uic.edu

import os
from urllib.request import urlretrieve

def download_link(directory,url): # Add logic for exception handling
    flName = str(directory + str(os.path.basename(url)))
    urlretrieve(url, flName)

 
