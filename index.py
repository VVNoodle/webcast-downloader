# Allows you to launch/initialise a browser
from selenium import webdriver
#  Allows you to search for things using specific parameters
from selenium.webdriver.common.by import By
# Allows you to wait for a page to load
from selenium.webdriver.support.ui import WebDriverWait
# Specify what you are looking for on a specific page in order to determine that the webpage has loaded
from selenium.webdriver.support import expected_conditions as EC
# Handling a timeout situation
from selenium.common.exceptions import TimeoutException
# Downloader
import urllib
# To get argv
import sys

option = webdriver.ChromeOptions()
option.add_argument("--incognito")
option.add_argument('headless')

# replace chromedriver.exe with your desired driver. Also make sure the path is correct
browser = webdriver.Chrome(executable_path='./chromedriver.exe', chrome_options=option)

browser.get("https://webcast.ucsc.edu/index.php")

# Wait 20 seconds for page to load
timeout = 20

try:
    WebDriverWait(browser, timeout).until(
        EC.visibility_of_element_located((By.ID, "contentHeaderTitle")))
except TimeoutException:
    print("Timed out waiting for page to load")
    browser.quit()

find_links = browser.find_elements_by_link_text('Video List')
find_course_titles = browser.find_elements_by_tag_name('td')
course = []
links = []
i=0
while i < len(find_course_titles):
    course.append(find_course_titles[i].text)
    i+=7

for i in range(len(find_links)):
    links.append(find_links[i].get_attribute("href"))

course_idx = course.index(sys.argv[1])
browser.get(links[course_idx])
username = browser.find_element_by_name("j_username")
password = browser.find_element_by_name("j_password")

username.send_keys(sys.argv[2])
password.send_keys(sys.argv[3])

browser.find_element_by_class_name("submit").click()

find_lecture_links = browser.find_elements_by_class_name('itemtitle')
lecture_links = []
for i in range(len(find_lecture_links)):
    lecture_links.append(find_lecture_links[i].get_attribute("href"))

def get_a_lecture(side, num, videos):
    if side == "L" or side == "LR":
        print(videos[0].get_attribute("src"))
        video_url = videos[0].get_attribute("src")
        urllib.urlretrieve(video_url, str(num)+'_L.mp4')
    if side == "R" or side == "LR":
        print(videos[1].get_attribute("src"))
        video_url = videos[0].get_attribute("src")
        urllib.urlretrieve(video_url, str(num)+'_R.mp4')

def get_lecture(num):
    print("lecture #: "+str(len(lecture_links)))
    lecture_links.pop()
    browser.get(lecture_links.pop())
    try:
        WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "video"))
        )
    except TimeoutException:
        browser.quit()
    finally:
        videos = browser.find_elements_by_tag_name("video")
        get_a_lecture(sys.argv[4], num, videos)           
        if(len(lecture_links)):
            get_lecture(num+1)
        else:
            browser.quit()
        #  Uncomment to write scrapped video section to video.html
        # reload(sys)
        # sys.setdefaultencoding('utf-8')
        # f= open("video.html","w+")
        # f.write(browser.page_source)
        # f.close()

get_lecture(1)
