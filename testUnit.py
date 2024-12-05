from bs4 import BeautifulSoup as bs
import requests 
import gc # memory managment 
# https://stackoverflow.com/questions/1316767/how-can-i-explicitly-free-memory-in-python

def getHTML(itemName: str) -> bs:
    item = itemName.split(' ')
    item = [(lambda x: x.capitalize() if x != 'of' else x)(i) for i in item]
    item = '_'.join(item)
    url = f"https://terraria.fandom.com/wiki/{item}"
    page = requests.get(url)
    soup = bs(page.content, "html.parser")
    print(url)
    return soup
