import os
import time
path = "cached_page.html"
t = os.path.getmtime(path)
print(t)
time_now = time.time()
print(time_now)
if time_now - t > 604800:
    print("a week have pasted")
