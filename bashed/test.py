f = open("test.txt", "w") 
f.write("testing 123!")
f.close

import os

try:
    text = open("../root/root.txt", "r").read()
    z = open("root.txt", "w")
    z.write(str(text)) 
    print("sucess!")
except: 
    print("Could not open root.txt")


