# -*- coding: utf-8 -*-
"""
Created on 01/20/2019
NSC - AD440 CLOUD PRACTICIUM
@authors: Nicholas Bennett, Dao Nguyen, Ryan Berry, Kyrrah Nork, Michael Leon

"""
from fbEventCrawl import fbEventCrawler
from browserCrawler import browserCrawler

def main ():
    try:
        fbEventCrawler.main()
    except:
        print("Facebook Crawler failed, check ACCESS_TOKEN")
    try:
        browserCrawler.main()
    except:
        print("Browser Crawler failed, please review.")

main()