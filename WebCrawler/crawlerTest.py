import urllib.request
import re
import os
from bs4 import BeautifulSoup

foundList = {}

def openURL():
   url = 'https://www.eventbrite.com/d/wa--seattle/disability/'
   response = urllib.request.urlopen(url)
   soup = BeautifulSoup(response, "html.parser")
   currentPage = 1
   max_pages = 1
   if soup.findAll("div", {"class": "paginator"}) != "":
       page = soup.findAll("div", {"class": "paginator"})

   for div in page:
       anchor = div.findAll('a')
       for text in anchor:
            if(text.text.isdigit()):
                max_pages = int(text.text)

   while currentPage <= max_pages:
        response = urllib.request.urlopen(url)
        soup = BeautifulSoup(response, "html.parser")
        soup = soup.findAll("section", {"class:", "eds-media-card-content"})
        #print(soup)
        for row in soup:
            value = row.text.split(",")
            for title in row.findAll("div", {"eds-is-hidden-accessible"}):
                write(value, title)

        currentPage += 1
        url = 'https://www.eventbrite.com/d/wa--seattle/disability/?page='+str(currentPage)
    
def write(value, title):
    global foundList
    if not foundList.get(title.text) :
        if "Free" not in value[0]:
            check = False
            for  s in value:
                if "$" in s:
                    foundList[title.text] = re.findall('\d+(?:[.,]\d*)?', s)[0]
                    check = True
                    break
            if not check:
                foundList[title.text] = "Unknown"
                    
        else:
            foundList[title.text] = "Free"
        #print(foundList)
    #else:
        #print("Skipping")

def toFile():
    global foundList
    f = open("data.txt", "w")
    #print(foundList)
    for row in foundList:
        f.write("Name: " + row + "\nCost: " + foundList[row] + "\n\n")
    

def main():
    try:
        openURL()
        try: 
            #error()
            toFile()
            print("Data file successfully created")
        except Exception as e:
            print("Error creating file, " + str(e))
    except Exception as e:
        print("Error gathering URL data, Make sure URL is correct / Check your internet connection" + str(e))
    

main()