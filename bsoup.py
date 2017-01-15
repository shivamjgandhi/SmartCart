import urllib2
from bs4 import BeautifulSoup
from HTMLParser import HTMLParser
import re

def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

m_url = 'http://allrecipes.com/recipe/218773/goya-easy-arroz-con-pollo/?internalSource=rotd&referringContentType=home%20page&clickId=cardslot%201'

page = urllib2.urlopen(m_url)
soup = BeautifulSoup(page, "html.parser")
soup.prettify()
#a = soup.findAll("span", { "class" : "recipe-ingred_txt added" })
a = str(soup.find_all("span", class_="recipe-ingred_txt added"))
a = striphtml(a)

print a
