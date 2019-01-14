How to get started:

First download Python -
https://www.python.org/downloads/
Keep track of where python is being installed.

Set Path (Windows, I dont have a mac) -

On Windows, go to environmental variables (Windows 10 just type environmental and it should pop up)

Make sure you are in the "Advanced" tab, click environmental variables.

Click path, then edit

Find where the python executable is located for me it was located at -C:\Users\micha\AppData\Local\Programs\Python\Python37-32\

Make sure Python works, type "Python" in a terminal

Next lets download PIP -

https://pip.pypa.io/en/stable/installing/

Open a new terminal - 
type curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

then -
type python get-pip.py

Afterwards go back to environmental variables and add another path value for PIP.

It should have been put into python's script folder - C:\Users\micha\AppData\Local\Programs\Python\Python37-32\Scripts like so.

Add it and open a new terminal and type pip to see if it works.

Finally its time to get beautiful soup! -

https://www.crummy.com/software/BeautifulSoup/

type in a new terminal -
pip install beautifulsoup4

Now clone the repo and attempt to run the crawlerTest.py either in visual studio code or in a terminal (Navigate to directly and simply type the name, crawlerTest.py)

It should create a data.txt file at which point you are ready to program using beautifulsoup for your crawler.

Also if using VSC type pip install pylint in a new terminal. Then open VSC, go to extensions and download the python extension for VSC and you should be ready to go once installed and VSC has refreshed with the new extension.

Slack Mike if you have any problems!