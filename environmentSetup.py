'''environment setup file
This should be run at first to install all necessary packages.
A python file is better than a shell script because it has not OS limitation.
'''

import os

os.system("pip install Flask")
os.system("pip install bcrypt")
os.system("pip install faker")
