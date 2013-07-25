import os

os.chdir("./csvdumps")

execfile('load_images_category.py')

execfile('load_images.py')

execfile('load_images_voyage.py')

os.chdir("./..")