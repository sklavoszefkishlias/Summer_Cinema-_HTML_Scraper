import os
import time

from main import get_html_content
from bs4 import BeautifulSoup


'''
path = "cached_page.html"
t = os.path.getmtime(path)
print(t)
time_now = time.time()
print(time_now)
if time_now - t > 604800:
    print("a week have pasted")

'''
response  = get_html_content()
soup = BeautifulSoup(response, "html.parser")
items = soup.find_all("div", class_="item card-item")



for item in items:

    movie_list = item.find_all("div", class_="item schedule-item") #Fetches all the movies from the cinema

    title_list = []
    for movie in movie_list:
        title_list.append(movie.find("h3").text.strip())
        title = movie.find_all("span", class_= "time")
        concated_datetime = ""
        for t in title:
            t = t.text.strip()
            concated_datetime += t
        print(concated_datetime)