import urllib.request
import re
import os
import json
from bs4 import BeautifulSoup

foundList = []
queue = []
output = []
eventBrite = "https://www.eventbrite.com/d/wa--seattle/disability/?page=1"

def openURL(url):
    global queue
    body = re.compile(".*body.*")
    #print("2. Trying - " + url)
    response = urllib.request.urlopen(url)
    soup = BeautifulSoup(response, "html.parser")
    scanPage(soup)
    soup = soup.find(attrs={"class": body})
    #print(soup.getText())
    #f = open("data.txt", "w")
    #f.write(str(soup))
    #print("3. SOUP FOUND! - " + url)
    #if "disab" in soup.getText():
    
    for row in soup.findAll("a"): 
        #print("4.") 
        if row.has_attr("href"):
            if row["href"] not in foundList and "eventbrite" in row["href"]:
                #print("4.Found link - " + row["href"]) 
                foundList.append(row["href"])
                queue.append(row["href"])
            #else:
                #print("URL exists already, skipping!")
    paginator = re.compile(".*paginator.*")
    max_pages = 0
    page = 1
    if url not in foundList:
        for row in soup.findAll(attrs={"class": paginator}):
            for anchor in row.findAll('a'):
                if(anchor.text.isdigit()):
                    max_pages = int(anchor.text)
        while page <= max_pages:
            if page != 1:
                foundList.append(url[:-1] + str(page))
                queue.append(url[:-1] + str(page))
            page += 1
    while(queue):
        currentURL = queue.pop(0)
        print(len(queue))
        try:
            print("1. Opening found link - " + currentURL)
            if "seattle" in currentURL or "/e/" in currentURL:
                openURL(currentURL)
            else:
                print("Ignoring link")
        except:
            try:
                print("1. Fixing link...  " + currentURL)
                openURL(url + currentURL)
            except:
                print("1. Link failed")
    createFile()
    #else:
        #print("99. Disabled not found skipping")
def scanPage(soup):
    global output
    regex = re.compile('.*event.*')
    price = re.compile('.*price.*')
    theData = {}
    for row in soup.findAll("div", attrs={"class": regex}):
        for data in row.findAll('h3'):
            if(data.text != " " and data.find_next('p')):
                if("date" in data.text.lower() or "location" in data.text.lower() or "description" in data.text.lower()):
                    if "date" in data.text.lower():
                        theData["Date"] = data.find_next('p').text
                    if "location" in data.text.lower():
                        theData["Location"] = data.find_next('p').text
                    if "description" in data.text.lower():
                        theData["Description"] = data.find_next('p').text
        for data in row.findAll('h1'):         
            if(data.text != " " and "Title" not in theData):
                print("Added to output - " + data.text)
                theData["Title"] = data.text
    for row in soup.findAll(attrs={"class": price}):
        theData["Price"] = row.text.strip()
    if len(theData) != 0 and theData not in output:
        output.append(theData)
        #print(output)
        

def createFile():
    with open("data.txt", "w") as f:
        f.write("{")
        for data in output:           
            if(len(data) >= 4):
                f.write("\n   {")
                if "Title" in data:
                    f.write("\n      Title: " + data["Title"])
                if "Price" in data:
                    f.write("\n      Price: " + data["Price"])
                if "Date" in data:
                    f.write("\n      Date: " + data["Date"])
                if "Location" in data:
                    f.write("\n      Location: " + data["Location"])
                if "Description" in data:
                    f.write("\n      Description: " + data["Description"])
                f.write("\n   }\n")
        f.write("}")

def main():
    global eventBrite
    try:
        openURL(eventBrite)
    except Exception as e:
        print("Error gathering URL data, Make sure URL is correct / Check your internet connection" + str(e))
    

main()