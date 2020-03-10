from selenium import webdriver
import time
import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.reddit.com/r/Fairytail_hentai/"

driver = webdriver.Chrome()
driver.get(url)
print("sleep 1...")
time.sleep(3)
print("wake 1...")
yes_btn = driver.find_elements_by_xpath("""/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div/div[2]/a[2]""")[0]
print(yes_btn)
yes_btn.click()

SCROLL_PAUSE_TIME = 5
last_height = driver.execute_script("return document.body.scrollHeight")

print("sleep 2...")
time.sleep(5)
print("wake 2...")

end_time = int(time.time() + (10 * 60))
while (int(time.time()) <= end_time):
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    print(f"going to sleep...{str(int(time.time()))[-4:]} of {str(end_time)[-4:]} ")
    time.sleep(SCROLL_PAUSE_TIME)
    print(f"woke up...{str(int(time.time()))[-4:]} of {str(end_time)[-4:]} ")

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        print("page end reached!")
        break
    last_height = new_height

print("final sleep...10 sec")
time.sleep(10)
print("woke up...")
res = driver.execute_script("return document.documentElement.outerHTML")
print("-- over --")

soup = BeautifulSoup(res,'lxml')
divs = soup.findAll("div",{"tabindex":"-1"})
post_list = []
#scrpae elements using bs4
counter = 0
for div in divs:
    #print("div element")
    #print(counter)
    post = Post()
        
    try:        
        title = div.find("h3",{"class":"_eYtD2XCVieq6emjKBH3m"})
        post.title = title.text
    except:
        pass
    
    try:
        user_name = div.find("a",class_="_2tbHP6ZydRpjI44J3syuqC _23wugcdiaj44hdfugIAlnX oQctV4n0yUb0uiHDdGnmE")
        post.user = user_name.text
    except:
        pass
    
    try:        
        upvotes = div.find("div",{"class":"_1rZYMD_4xY3gRcSS3p8ODO"})
        post.upvotes = upvotes.text
    except:
        pass
    
    try:
        date = div.find("a",{"class":"_3jOxDPIQ0KaOWpzvSQo-1s"})
        post.date = date.text
    except:
        pass
    
    try:    
        comment = div.find("span",class_="FHCV02u6Cp2zYL0fhQPsO")
        comm = comment.text.split()[0]
        #print(comm)
        if(comm.lower() == 'comment'):
            post.comments = 0
            #print("0")
        else:
            post.comments = comm
            #print(f'comment: {post.comments}')
    except:
        pass
    
    try:
        img_src = div.find("img",{"class":["_2_tDEnGMLxpM6uOa2kaDB3","_2c1ElNxHftd8W_nZtcG9zf"]})
        #img_src = div.find("img",{"alt":"Post image"})
        post.imgsrc = img_src['src']
    except:
        pass
    
    post_list.append(post)    
    counter = counter + 1

print("loop end")
print(len(post_list))
for post in post_list:
    print(f'title: {post.title}')
    print(f'user: {post.user}')
    print(f'upvotes: {post.upvotes}')
    print(f'comments: {post.comments}')
    print(f'src: {post.imgsrc}')
    print(f'date: {post.date}')
    print("")

counter = 0
for post in post_list:
    if(post.imgsrc == 'NOT FOUND'):
        counter = counter + 1

print(f"{counter} out of {len(post_list)} don't have img-src")

import re
erza_list =[]
for post in post_list:
    title = post.title.lower()
    if(re.search('erza',title)):
        erza_list.append(post)
print(len(erza_list))
print("done")

for post in erza_list:
    if(post.imgsrc != 'NOT FOUND'):
        print(post.title)
        print(post.imgsrc)
        print(f"{post.upvotes} upvotes")
        print(f"{post.comments} comments")
        print(post.date)
        print()

#create a csv file and store info.
data_rows = []
for post in post_list:
    title = post.title.encode('ascii',errors='ignore').decode('utf-8')    
    data_rows.append([title,post.user,post.imgsrc,post.upvotes,post.comments,post.date])
data_rows.insert(0,['title','posted_by','img_src','upvotes','comments','date'])
with open('subredditData.csv','w',newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data_rows)
print("done")