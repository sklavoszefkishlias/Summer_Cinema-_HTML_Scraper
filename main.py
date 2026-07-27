import requests
import os
from bs4 import BeautifulSoup
import time
# The URL of the page we want to scrape
URL = "https://www.athinorama.gr/cinema/guide/therinoi/cinemas/"

# A User-Agent makes your script look like a standard web browser
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.6 Safari/605.1.15"
}

CACHE_FILE = "cached_page.html"

def get_html_content():
    # 1. Check if we already have the file saved locally
    if os.path.exists(CACHE_FILE) and (time.time() - os.path.getmtime(CACHE_FILE) < 86400): #Sees if you have relevant info(checks if its today's data)
        print("📁 Found cached HTML file. Loading from disk...")
        with open(CACHE_FILE, "r", encoding="utf-8") as file:
            return file.read()
            
    # 2. If the file doesn't exist, download it from the internet
    print("Requesting from live website...")
    try:
        response = requests.get(URL, headers=HEADERS)
        response.raise_for_status()
        
        # Save the downloaded HTML to our local file for next time
        with open(CACHE_FILE, "w", encoding="utf-8") as file:
            file.write(response.text)
            print(f"💾 Successfully saved webpage to '{CACHE_FILE}'")
            
        return response.text
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to retrieve the webpage: {e}")
        return None


def datetime_title_parser(movie_list):
    title_list = []
    datetime_list = []
    for movie in movie_list:
        title_list.append(movie.find("h3").text.strip())
        title = movie.find_all("span", class_= "time")
        concated_datetime = ""
        for t in title:
            t = t.text.strip()
            concated_datetime += t
        datetime_list.append(concated_datetime)
    return title_list, datetime_list
        
    









def fetch_movie_data():
    try:
        # 1. Download the webpage
        response = get_html_content()

        # 2. Parse the HTML code
        soup = BeautifulSoup(response, "html.parser")

        # 3. Find all item containers on the page
        # (On a movie site, this might be div class="movie-card")
        items = soup.find_all("div", class_="item card-item")
        print(f"--- Found {len(items)} Items ---\n")
        print(type(items))
        flag = 0
        for item in items:
            # Extract text and strip out extra whitespace
            cinema = item.find("h2", class_="item-title").text.strip()
            location = item.find("div", class_= "details").text.strip()

            movie_list = item.find_all("div", class_="item schedule-item") #Fetches all the movies from the cinema

            title_list = []
            date_time_list = []

            title_list, date_time_list = datetime_title_parser(movie_list)

            if len(date_time_list) != len(title_list):
                flag = 1
                
                

            ticket_prices = item.find("p", class_="summary").text.strip()

            print(cinema)
            print(location)
            print(title_list)
            print(date_time_list)

            print(ticket_prices)
        if flag == 1:
            print("somthing bad happand")
        elif flag == 0:
            print("all good") 

            

    except AttributeError:
        print("❌ Error: The website structure might have changed, or a class name is incorrect.")

if __name__ == "__main__":
    fetch_movie_data()