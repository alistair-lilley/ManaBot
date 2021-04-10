import time
import os

path = "/home/akiahala/.local/share/Cockatrice/Cockatrice/pics/downloadedPics"

while True:
    count = 0
    for d in os.listdir(path):
        count += len(os.listdir(path+'/'+d))
    print(count)
    time.sleep(5)