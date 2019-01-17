
# -*- coding: utf-8 -*-
"""
Created on Tues  01/15/2019

@author: Dao Nguyen
"""

import urllib3

import requests
import json

def main():
    token = "YOUR_FB_TOKEN"
    #graph = facebook.GraphAPI(access_token = token, version = 3.1)
    #pagesdata = requests.get("https://graph.facebook.com/me/accounts?access_token="+token)
    page_id = "https://www.facebook.com/FoxNews/"
    posts_on_page = requests.get("https://graph.facebook.com/"+page_id+"/feed?access_token=" + token)
    posts_data = (posts_on_page.json())
    print(json.dumps(posts_data))


main()