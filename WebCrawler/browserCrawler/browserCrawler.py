# -*- coding: utf-8 -*-
"""
Created on 01/20/2019
NSC - AD440 CLOUD PRACTICIUM
@author: Michael Leon

"""
import urllib.request
import re
import os
import json
from bs4 import BeautifulSoup

# This script scrapes a website and pulls specific data.

FOUND_LIST = []
QUEUE = []
OUTPUT = {}
EVENT_BRITE = "https://www.eventbrite.com/d/wa--seattle/disability/?page=1"


def open_url(url):
    # Function opens a url, parses it with Beautifulsoup
    # Finds relevant links and adds them to the global QUEUE
    # Foundlist used to avoid duplicates
    global QUEUE
    body = re.compile(".*body.*")
    response = urllib.request.urlopen(url)
    soup = BeautifulSoup(response, "html.parser")
    scan_page(soup)
    soup = soup.find(attrs={"class": body})

    for row in soup.findAll("a"):
        if row.has_attr("href"):
            if row["href"] not in FOUND_LIST and "eventbrite" in row["href"]:
                print("Unique link found - " + row["href"])
                FOUND_LIST.append(row["href"])
                QUEUE.append(row["href"])
    paginator = re.compile(".*paginator.*")
    max_pages = 0
    page = 1
    # Finds max page number so all events are found
    if url not in FOUND_LIST:
        for row in soup.findAll(attrs={"class": paginator}):
            for anchor in row.findAll('a'):
                if anchor.text.isdigit():
                    max_pages = int(anchor.text)
        while page <= max_pages:
            if page != 1:
                FOUND_LIST.append(url[:-1] + str(page))
                QUEUE.append(url[:-1] + str(page))
            page += 1
    while QUEUE:
        current_url = QUEUE.pop(0)
        print("\n" + str(len(QUEUE)) + " link's remaining in QUEUE!")
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
    global OUTPUT
    event_re = re.compile('.*event.*')
    price_re = re.compile('.*price.*')
    event_data = {"Title": None, "Date": None,
                  "Location": None, "Description": None, "Price": None}
    # Extracts all relevant data from page
    for row in soup.findAll("div", attrs={"class": event_re}):
        for data in row.findAll('h3'):
            if data.text != " " and data.find_next('p'):
                if("date" in data.text.lower() or "location" in data.text.lower() or
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
    # Data is useless if Title, Date, and Location is missing. Catch duplicates.
    if (event_data["Title"] is not None and event_data["Location"] is not None and
            event_data["Date"] is not None and event_data["Title"] not in OUTPUT):
        if event_data["Description"] is None or event_data["Description"] == "":
            event_data["Description"] = "None"
        if event_data["Price"] is None or event_data["Price"] == "":
            event_data["Price"] = "Unknown"
        print(event_data["Title"] + " added to json OUTPUT.")
        OUTPUT[event_data["Title"]] = event_data


def create_json():
    with open('data.json', 'w') as outfile:
        json.dump(OUTPUT, outfile)


def main():
    try:
        open_url(EVENT_BRITE)
        print("Task completed.")
    except Exception as e:
        print("Error gathering URL data, " + str(e))

