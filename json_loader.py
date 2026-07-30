import requests
import os
from bs4 import BeautifulSoup
import time
import json


# The URL of the page we want to scrape
URL = "https://www.athinorama.gr/cinema/guide/therinoi/cinemas/"

# A User-Agent makes your script look like a standard web browser
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.6 Safari/605.1.15"
}

CACHE_FILE = "cached_page.html"

TIME_FILE = "time.txt"

DATA_FILE = "data.json"

def is_data_uptodate():
    with open("time.txt") as f:
        GOGO = f.read()
    last_pull = float(GOGO)

    if time.time() - last_pull < 86400 :
        return 1
    else:
        return 0



def get_html_content():


    if os.path.exists(CACHE_FILE) and os.path.exists(TIME_FILE):
        if is_data_uptodate():
            with open(CACHE_FILE, "r", encoding="utf-8") as file:
                return file.read()
        else:
            #Requestes from webserver
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
    else:
        #Inititalises the time.txt file with the current time
        with open("time.txt", "w", encoding="utf-8") as file:
            file.write(str(time.time()))

        #Requests from the web server
        print("Requesting from live website for the first time...")
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

        json_list = []
        id = 0


        
        for item in items:
            # Extract text and strip out extra whitespace
            cinema = item.find("h2", class_="item-title").text.strip()
            location = item.find("div", class_= "details").text.strip()

            movie_list = item.find_all("div", class_="item schedule-item") #Fetches all the movies from the cinema

            title_list = []
            date_time_list = []

            title_list, date_time_list = datetime_title_parser(movie_list)

            if len(date_time_list) != len(title_list): #Checks if the number of datetimes and movie titles are the same for each cinema
                flag = 1
                
                

            ticket_prices = item.find("p", class_="summary").text.strip()


            json_dict = {
                    "id": id,
                    "cinema": cinema,
                    "location": location,
                    "movies": title_list,
                    "datetime": date_time_list
            }
            json_list.append(json_dict)
            id += 1

        print(json_list[0]["movies"][0])
        

        json_string = json.dumps(json_list, ensure_ascii=False)
        with open(DATA_FILE, mode="w",encoding="utf-8") as file:
            json.dump(json_string, file,indent = 2, ensure_ascii=False)
        file.close()

        '''if flag == 1: #Checks 
            print("somthing bad happand")
        elif flag == 0:
            print("all good") '''



            

    except AttributeError:
        print("❌ Error: The website structure might have changed, or a class name is incorrect.")

if __name__ == "__main__":
    fetch_movie_data()