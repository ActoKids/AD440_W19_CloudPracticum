import urllib.request
import re
import os
import json
from bs4 import BeautifulSoup

foundList = []
queue = []
output = []
eventBrite = "https://www.eventbrite.com/d/wa--seattle/disability/"

def openURL(url):
    global queue
    print("2. Trying - " + url)
    response = urllib.request.urlopen(url)
    soup = BeautifulSoup(response, "html.parser")
    #f = open("data.txt", "w")
    #f.write(str(soup))
    print("3. SOUP FOUND! - " + url)
    if "disab" in soup.getText():
        scanPage(soup)
        for row in soup.findAll("a"): 
            #print("4.") 
            if row.has_attr("href"):
                if url not in foundList:
                    #print("4.Found link - " + row["href"]) 
                    foundList.append(row["href"])
                    queue.append(row["href"])
                #else:
                    #print("URL exists already, skipping!")
        while(queue):
            currentURL = queue.pop(0)
            print(len(foundList))
            try:
                print("1. Opening found link - " + currentURL)
                openURL(currentURL)
            except:
                try:
                    print("1. Fixing link...  " + currentURL)
                    openURL(url + currentURL)
                except:
                    print("1. Link failed")
    else:
        print("99. Disabled not found skipping")
def scanPage(soup):
    global output
    regex = re.compile('.*event.*')
    price = re.compile('.*price.*')
    theData = {}
    for row in soup.findAll("div", attrs={"class": regex}):
        for data in row.findAll('h3'):
            if(data.text != " " and data.find_next('p')):
                if("date" in data.text.lower() or "location" in data.text.lower() or "description" in data.text.lower()):
                    theData[data.text] = data.find_next('p').text
        for data in row.findAll('h1'):
            if(data.text != " "):
                theData["Title"] = data.text
    for row in soup.findAll(attrs={"class": price}):
        theData["Price"] = row.text.strip()
    if len(theData) != 0 and theData not in output:
        output.append(theData)
        print(output)
        createFile()

def createFile():
    with open("data.txt", "w") as f:
        for data in output:
            if "Title" in data:
                f.write("Title: " + data["Title"] + " Price: " + data["Price"] + "\n")

def main():
    global eventBrite
    try:
        openURL(eventBrite)
    except Exception as e:
        print("Error gathering URL data, Make sure URL is correct / Check your internet connection" + str(e))
    

main()