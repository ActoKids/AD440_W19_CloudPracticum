import urllib.request
import re
import os
import json
from bs4 import BeautifulSoup

found_list = []
queue = []
output = {}
event_brite = "https://www.eventbrite.com/d/wa--seattle/disability/?page=1"


def open_url(url):
    global queue
    body = re.compile(".*body.*")
    response = urllib.request.urlopen(url)
    soup = BeautifulSoup(response, "html.parser")
    scan_page(soup)
    soup = soup.find(attrs={"class": body})

    for row in soup.findAll("a"):
        if row.has_attr("href"):
            if row["href"] not in found_list and "eventbrite" in row["href"]:
                print("Unique link found - " + row["href"])
                found_list.append(row["href"])
                queue.append(row["href"])
    paginator = re.compile(".*paginator.*")
    max_pages = 0
    page = 1
    if url not in found_list:
        for row in soup.findAll(attrs={"class": paginator}):
            for anchor in row.findAll('a'):
                if anchor.text.isdigit():
                    max_pages = int(anchor.text)
        while page <= max_pages:
            if page != 1:
                found_list.append(url[:-1] + str(page))
                queue.append(url[:-1] + str(page))
            page += 1
    while queue:
        current_url = queue.pop(0)
        print("\n" + str(len(queue)) + " link's remaining in queue!")
        try:
            print("\nOpening found link - " + current_url)
            if "seattle" in current_url or "/e/" in current_url:
                open_url(current_url)
            else:
                print("Ignoring link")
        except Exception as a:
            try:
                print(a)
                open_url(url + current_url)
            except:
                print("Link failed")
    create_json()

def scan_page(soup):
    global output
    event_re = re.compile('.*event.*')
    price_re = re.compile('.*price.*')
    event_data = {"Title": None, "Date": None,
                  "Location": None, "Description": None, "Price": None}

    for row in soup.findAll("div", attrs={"class": event_re}):
        for data in row.findAll('h3'):
            if data.text != " " and data.find_next('p'):
                if("date" in data.text.lower() or
                        "location" in data.text.lower() or
                        "description" in data.text.lower()):
                    if "date" in data.text.lower():
                        event_data["Date"] = data.find_next('p').text
                    if "location" in data.text.lower():
                        location = " "
                        for tag in data.find_next('div').findAll("p"):
                            if not tag.find("a"):
                                location = location + tag.text + " "
                        if "seattle" in location.lower():
                            event_data["Location"] = location
                        else:
                            break                   
                    if "description" in data.text.lower():
                        event_data["Description"] = data.find_next(
                            'p').text.replace('\n', " ")
        for title in row.findAll('h1'):
            if title.text != " " and event_data["Title"] is None:
                event_data["Title"] = title.text
    for price in soup.findAll(attrs={"class": price_re}):
        event_data["Price"] = price.text.strip()
    if (event_data["Title"] is not None and
            event_data["Location"] is not None and
            event_data["Date"] is not None and
            event_data["Title"] not in output):
        if event_data["Description"] is None or event_data["Description"] == "":
            event_data["Description"] = "None"
        if event_data["Price"] is None or event_data["Price"] == "":
            event_data["Price"] = "Unknown"
        print(event_data["Title"] + " added to json output.")
        output[event_data["Title"]] = event_data


def create_json():
    with open('data.json', 'w') as outfile:
        json.dump(output, outfile)


def main():
    global event_brite
    try:
        open_url(event_brite)
    except Exception as e:
        print("Error gathering URL data, Make sure URL is correct / Check your internet connection" + str(e))


print("This script crawls a website and creates a data file.")
main()
print("Task completed.")
