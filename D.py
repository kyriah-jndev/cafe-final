import os
import tempfile
import random
randomray = []
for numn in range(10):
  randomray.append(numn)
filename = tempfile.mktemp("text.txt")
file = open(filename, "w")
for values in randomray:
  file.write(str(values) + "\n")
file.close()
os.startfile(filename, "print")
print (randomray)
