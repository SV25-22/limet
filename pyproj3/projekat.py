from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import codecs
import re
from webdriver_manager.chrome import ChromeDriverManager
import text_helper as th

def title_url_lime(txt):
    return "https://limetorrent.xyz/fullsearch?q=" + title_spacing(txt).replace(" ","%20")

def html_text_lime(url):
    options = Options()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME,"odd")))
    html = driver.page_source
    driver.quit()
    return html

def title_url_1377x(txt):
    return "https://www.1377x.to/search/" + title_spacing(txt).replace(" ","%20") + "/1/"

def title_tag(txt):
    return txt.split(" ")[-1]

def title_spacing(txt):
    tmp = txt.split(" ")
    return " ".join(tmp[:-1]) #optionally "%20".join right from the start

def html_text(url):
    return requests.get(url).text

def selenium_lime_access(url,a_tag_text):
    options = Options()
    options.add_argument(r'user-data-dir=C:\\Users\\Admin\\AppData\\Local\\Google\\Chrome\\User Data\\Default') #this part has to be hardcoded in order to by-pass the chrome download pop up
    options.add_argument("--headless=new")
    #options.add_experimental_option("detach",True)
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.get(url)
    print(url)
    print(a_tag_text)
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.LINK_TEXT,a_tag_text)))
    element = driver.find_element(By.LINK_TEXT,a_tag_text)
    driver.execute_script("arguments[0].scrollIntoView();", element)
    driver.execute_script("arguments[0].click();",element)
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,"d")))
    element = driver.find_element(By.LINK_TEXT,"Download Torrent Magnet")
    driver.execute_script("arguments[0].scrollIntoView();", element)
    driver.execute_script("arguments[0].click();",element)
    WebDriverWait(driver,10)
    print("Downloading torrent")
    driver.quit()
    return True

def selenium_1377x_access(url):  # 1377x requires an account, can be by-passed with two additional inputs via selenium
    print(url)
    options = Options()
    options.add_argument(r'user-data-dir=C:\\Users\\Admin\\AppData\\Local\\Google\\Chrome\\User Data\\Default')
    #options.add_argument("--headless=new")
    options.add_experimental_option("detach",True)
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.get(url)
    WebDriverWait(driver,10)
    element = driver.find_element(By.LINK_TEXT,"MAGNET DOWNLOAD")
    driver.execute_script("arguments[0].scrollIntoView();", element)
    driver.execute_script("arguments[0].click();",element)
    WebDriverWait(driver,10)
    print("Downloading torrent")
    #driver.quit()
    return True

def scraping_lime(html_text, tag,url,title):
    soup = BeautifulSoup(html_text,"lxml")
    tv_shows_odd = soup.find_all("tr",class_="odd")
    tv_shows_even = soup.find_all("tr",class_="even")

    time_atm = datetime.now()
    for tv_show_odd in tv_shows_odd:
        tv_show_a_tag = tv_show_odd.find("td",class_="list-item item-name item-title").find("a").text
        tv_show_date= tv_show_odd.find("td",class_="list-item item-uploaded").text #TODO parser
        tv_show_size = tv_show_odd.find("td",class_="list-item item-size").text
        time_parsed = time_parser_lime(tv_show_date)

        tries = 1

        if("o" in tag):
            while(tries>0 and tries<=10):
                try:
                    selenium_lime_access(url, tv_show_a_tag)
                    th.delete_title("naslovi.txt", title)
                    tries = -100
                except Exception as e:
                    print("Unsuccessfull attempt, trying again...")
                    tries+=1
            return

        elif((time_atm - time_parsed) <= timedelta(days=2)): #maybe add size to the if statements

            while(tries>0 and tries<=10):
                try:
                    selenium_lime_access(url, tv_show_a_tag)
                    tries = -100
                except Exception as e:
                    print("Unsuccessfull attempt, trying again...")
                    tries+=1
            return
        else:
            print("Not recent enough")

    for tv_show_even in tv_shows_even:
        tv_show_a_tag = tv_show_even.find("td",class_="list-item item-name item-title").find("a").text
        tv_show_date= tv_show_even.find("td",class_="list-item item-uploaded").text
        tv_show_size = tv_show_even.find("td",class_="list-item item-size").text
        time_parsed = time_parser_lime(tv_show_date)
        tries = 1

        if("o" in tag):
            while(tries>0 and tries<=10):
                try:
                    selenium_lime_access(url, tv_show_a_tag)
                    th.delete_title("naslovi.txt", title)
                    tries = -100
                except Exception as e:
                    print("Unsuccessfull attempt, trying again...")
                    tries+=1
            return

        elif((time_atm - time_parsed) <= timedelta(days=2)): 
            while(tries>0 and tries<=10):
                try:
                    selenium_lime_access(url, tv_show_a_tag)
                    tries = -100
                except Exception as e:
                    print("Unsuccessfull attempt, trying again...")
                    tries+=1
            return
        else:
            print("Not recent enough")

def scraping_1377x(html_text, tag, title):
    soup = BeautifulSoup(html_text,'lxml')

    tv_shows = soup.find("tbody").find_all("tr")
    time_atm = datetime.now()
    for tv_show in tv_shows:
        block_date = tv_show.find('td',class_='coll-date').text
        block_size = tv_show.find('td',class_='coll-4').text
        block_download_site = "https://1377x.to" + tv_show.find("td", class_ = "coll-1").find_all('a')[1]["href"]
        block_time_parsed = time_parser_1337x(block_date)

        if("o" in tag):
            selenium_1377x_access(block_download_site)          #add the tries mechanism like in lime
            #th.delete_title("C:\\Users\\Admin\\Desktop\\Mimi projekat\\naslovi.txt",title)
            return

        elif((time_atm-block_time_parsed) <= timedelta(days=2)):
            selenium_1377x_access(block_download_site)
            return
        else:
            print("Not recent enough")

def time_parser_lime(date):
    return datetime.strptime(date,"%Y-%m-%d")

def time_parser_1337x(time):

    if("am" in time or "pm" in time):
        return datetime.now()

    if( "st" in time):
        time = time.replace("st", "th")
    elif( "nd" in time):
        time = time.replace("nd", "th")
    elif("rd" in time):
        time = time.replace("rd", "th")

    return datetime.strptime(time, "%b. %dth '%y")

def main_1377x():
    file_location = "naslovi.txt"   #"C:\\Users\\Admin\\Desktop\\Mimi projekat\\naslovi.txt"
    titles = th.read_titles(file_location)
    for title in titles:
        url = title_url_1377x(title)
        scraping_1377x(html_text(url), title_tag(title),title[:-2])

def main_lime():
    file_location = "naslovi.txt"
    titles = th.read_titles(file_location)
    for title in titles:
        url = title_url_lime(title)
        scraping_lime(html_text_lime(url), title_tag(title),url,title[:-2])

if __name__ == "__main__":
    file_location = "naslovi.txt"
    titles = th.read_titles(file_location)
    for title in titles:
        print(title)
    #main_lime()
    #main_1377x()
    pass

