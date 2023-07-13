# Import libraries
import requests
import urllib.request
import time
import os.path
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urlparse
from urllib.parse import parse_qs

# Set the URL you want to webscrape from
url = 'http://52.32.1.180:8080/SPLOT/SplotAnalysesServlet?action=select_model&enableSelection=false&&showModelDetails=true'

# Connect to the URL
response = requests.get(url)

# Parse HTML and save to BeautifulSoup object¶
soup = BeautifulSoup(response.text, "html.parser")

# To download the whole data set, let's do a for loop through all a tags
for i in range(0,len(soup.findAll('a'))): #'a' tags are for links
    one_a_tag = soup.findAll('a')[i]
    if 'modelFile' in str(one_a_tag):
        link = one_a_tag['href']
        url = urlparse(link).query
        modelName=parse_qs(url)['modelFile']
        if modelName[0].endswith('.xml') and not os.path.exists('./splot-xml/'+modelName[0]): #to make it sure that we do not follow bizzare models and avoid redownloading already present models
            download_url = 'http://52.32.1.180:8080/SPLOT/models/'+ modelName[0]
            print(download_url)
            urllib.request.urlretrieve(download_url,'./splot-xml/'+modelName[0]) 
            time.sleep(10) #pause the code for a sec, this time seems appropiated. But more testing is needed
