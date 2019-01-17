import urllib.request
import re
import os
import json
from bs4 import BeautifulSoup

foundList = []
queue = []
output = {}
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
        print("\n"+ str(len(queue)) + " link's remaining in queue!")
        try:
            print("1. Opening found link - " + currentURL)
            if "seattle" in currentURL or "/e/" in currentURL:
                openURL(currentURL)
            else:
                print("Ignoring link")
        except Exception as a:
            try:
                print(a)
                openURL(url + currentURL)
            except:
                print("1. Link failed")
    #createFile()
    createJson()
    #else:
        #print("99. Disabled not found skipping")
def scanPage(soup):
    global output
    event = re.compile('.*event.*')
    price = re.compile('.*price.*')
    theData = {"Title": None, "Date": None, "Location": None, "Description": None, "Price": None}

    for row in soup.findAll("div", attrs={"class": event}):
        for data in row.findAll('h3'):
            if(data.text != " " and data.find_next('p')):
                if("date" in data.text.lower() or "location" in data.text.lower() or "description" in data.text.lower()):
                    if "date" in data.text.lower():
                        theData["Date"] = data.find_next('p').text
                    if "location" in data.text.lower():
                        location = " "
                        for tag in data.find_next('div').findAll("p"):
                            #print(tag)
                            if not tag.find("a"):
                                #print(tag.text)
                                location = location + tag.text + " "
                        #print(location)
                        theData["Location"] = location
                    if "description" in data.text.lower():
                        theData["Description"] = data.find_next('p').text.replace('\n', " ")
        for data in row.findAll('h1'):         
            if(data.text != " " and theData["Title"] is None):
                print("Added to output - " + data.text)
                theData["Title"] = data.text
    for row in soup.findAll(attrs={"class": price}):
        theData["Price"] = row.text.strip()
    #print(str(theData))
    if theData["Title"] is not None and theData["Location"] is not None and theData["Date"] is not None and theData["Title"] not in output:
        #print(theData)
        if theData["Description"] is None:
            theData["Description"] = "None"
        if theData["Price"] is None:
            theData["Price"] = "Unknown"
            
        output[theData["Title"]] = theData
        
        #print(output)
        
def createJson():
    with open('data.json', 'w') as outfile:
        json.dump(output, outfile)
def createFile():
    with open("data.txt", "w") as f:
        f.write("{")
        for data in output:           
            f.write("\n   {")
            if data["Title"] is not None:
                f.write("\n      Title: " + data["Title"])
            else:
                f.write("\n      Title: " + "Unknown")
            if data["Price"] is not None:
                f.write("\n      Price: " + data["Price"])
            else:
                f.write("\n      Price: " + "Unknown")
            if data["Date"] is not None:
                f.write("\n      Date: " + data["Date"])
            else:
                f.write("\n      Date: " + "Unknown")
            if data["Location"] is not None:
                f.write("\n      Location: " + data["Location"])
            else:
                f.write("\n      Location: " + "Unknown")
            if data["Description"] is not None:
                f.write("\n      Description: " + data["Description"])
            else:
                f.write("\n      Description: " + "Unknown")
            f.write("\n   }\n")
        f.write("}")

def main():
    global eventBrite
    try:
        openURL(eventBrite)
    except Exception as e:
        print("Error gathering URL data, Make sure URL is correct / Check your internet connection" + str(e))
    
print("This script crawls a website and creates a data file.")
main()
print("Task completed.")