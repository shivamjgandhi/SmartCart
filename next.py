from flask import Flask
from flask import request #<-- import 'request'
import requests
from flask_cors import CORS, cross_origin
import json
import urllib2
from bs4 import BeautifulSoup
from HTMLParser import HTMLParser
import re

app = Flask(__name__)
CORS(app)

def getSoup(my_url):
    page = urllib2.urlopen(my_url)
    soup = BeautifulSoup(page, "html.parser")
    soup.prettify()
    return soup

def getImageName(soup):
    title = str(soup.find("h1", class_="recipe-summary__h1").getText())
    image = str(soup.find("img", class_="rec-photo")['src'])
    b = {
        "name" : title,
        "img" : image,
        "stars" : 4
    }
    return b

def stripHTML(raw_html):
  cleanr =re.compile('<.*?>')
  cleantext = re.sub(cleanr,'', raw_html)
  return cleantext

def convertRecipesToStrings(soup):
    a = str(soup.find_all("span", class_="recipe-ingred_txt added"))
    a = a.split('>,')
    for i in range(0,len(a)):
        a[i] = stripHTML(a[i])
        a[i] = re.sub("span","",a[i],count=2)
        a[i] = re.sub("to taste","",a[i],count=2)
        a[i] = a[i].replace("]", "")
        a[i] = re.sub("[/<]","",a[i])
        a[i] = a[i].split(",")[0]
        a[i] = a[i].strip()
    return a

def parseIngredientStringToList(input_string):
    split_vec = list()
    lengths= len(input_string.split(' '))
    if lengths == 2:
        split_vec = input_string.split(' ', 1)
    elif lengths >= 2:
        split_vec = input_string.split(' ', 2)
    return split_vec

def createListOfLists(input_vector):
    final = list()
    for i in range(0, len(input_vector)):
        b = parseIngredientStringToList(input_vector[i])
        final.append(b)
    return final

def return_name_price_image(word):
    r = requests.get('http://api.walmartlabs.com/v1/search?apiKey=9cbtd8j8r9rzzkhw5pw4pj68&lsPublisherId=sjgandhi1998&query=' + word)
    json_dict = r.json()

    trig = False
    food = 'food'
    key = 0

    for i in range (0, 10):
        cat = json_dict['items'][i]['categoryPath']
        n = len(cat)
        for j in range(0, n-3):
            if cat[j: j+3] is 'food':
                trig = True
                key = i
                break
    # print word
    code_payload = {
        "name": word,
        "walmart": json_dict['items'][key]['name'],
        "price": json_dict['items'][key]['salePrice'],
        "img": json_dict['items'][key]['thumbnailImage'],
        "quantity": 10,
        "unit": "unit"
    }  
    return code_payload

def add_shopping_item(item):
    url = 'https://smartcart-72048.firebaseio.com/Current/shopping/.json'
    item = json.dumps(item)
    post_request = requests.post(url, data=item)
    # print post_request.text
    
def add_recipe_item(item):
    url = 'https://smartcart-72048.firebaseio.com/Current/recipes/.json'
    item = json.dumps(item)
    post_request = requests.post(url, data=item)
@cross_origin()
@app.route('/', methods=['POST', 'GET'])
def login():
    # print repr(request.data)
    dataDict = json.loads(request.data)
    soup = getSoup(dataDict['name'])

    #gets a list of lists, containing name, etc. of specific food item
    allIngredients = createListOfLists(convertRecipesToStrings(soup))

    #gets the name of the recipe followed by an image url
    add_recipe_item(getImageName(soup))

    # print allIngredients
    for x in allIngredients:
        if len(x) > 2:
            temp = return_name_price_image(x[2])
            # print return_name_price_image(x[2])
            add_shopping_item(temp)
            # print add_shopping_item(return_name_price_image(x[2]))
    return dataDict['name'], 200, {'Content-Type': 'application/json; charset=utf-8'}


if __name__ == "__main__":
    app.run(debug=True)