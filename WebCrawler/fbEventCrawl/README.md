
HOW TO CRAWL YOUR OWN FACEBOOK EVENTS WITH FACEBOOK GRAPH API

First download Python -
https://www.python.org/downloads/
Keep track of where python is being installed.

Set Path (Windows, I dont have a mac) -

On Windows, go to environmental variables (Windows 10 just type environmental and it should pop up)

Make sure you are in the "Advanced" tab, click environmental variables.

Click path, then edit

Find where the python executable is located for me it was located at -C:\Users\daong\AppData\Local\Programs\Python\Python37-32\

Make sure Python works, type "Python" in a terminal

Next lets download PIP -

https://pip.pypa.io/en/stable/installing/

Open a new terminal - 
type curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

then -
type python get-pip.py

Afterwards go back to environmental variables and add another path value for PIP.

It should have been put into python's script folder - C:\Users\daong\AppData\Local\Programs\Python\Python37-32\Scripts like so.

Add it and open a new terminal and type pip to see if it works.

Now clone the repo and attempt to run the fbEventCrawl.py either in visual studio code or in a terminal (Navigate to directly and simply type the name, crawlerTest.py)

It should create a data.txt file in the directory with all your facebook events data

Before you run the fbEventCrawl.py, your need to have a Facebook account, an access token, create some facebook events on your facebook account for testing.
  1. you need to go to terminal and install the following libraries:
    pip install facebook-sdk
    pip3 install requests
  2. You need to have a facebook account, if not create one -->
    + Go to link developers.facebook.com, create an account there.
    + Go to link developers.facebook.com/tools/explorer.
      Go to “My apps” drop down in the top right corner and select “add a new app”. Choose a display name and a category and then             “Create App ID”.
    + Again get back to the same link developers.facebook.com/tools/explorer. You will see “Graph API Explorer” below “My Apps” in the         top right corner. From “Graph API Explorer” drop down, select your app.
      Then, select “Get Token”. From this drop down, select “Get User Access Token”. Select permissions from the menu that appears and         then select “Get Access Token.”
    + Go to link developers.facebook.com/tools/accesstoken. Select “Debug” corresponding to “User Token”. Go to “Extend Token Access”.         This will ensure that your token does not expire every two hours.
    + Copy the token and paste it in the fbEventCrawl.py where it says "YOUR_ACCESS_TOKEN"
    + Go to your facebook page and create some events to test out the scrawling of data.
  
  Finally, you can start running the fbEventCrawl.py the see if the output to data.txt matches with your events info you created on your   page.
  
