from bs4 import BeautifulSoup as bs 
import requests 
# will not comment everything, running on hopes and dreams 

def getHTML(itemName: str) -> bs:
    item = itemName.split(' ')
    item = [i.capitalize() for i in item]
    item = '_'.join(item)
    url = f"https://terraria.fandom.com/wiki/{item}"
    page = requests.get(url)
    soup = bs(page.content, "html.parser")
    print(url)
    return soup

def getCraftingListAlt(soup: bs) -> dict:
    craftingInfo = {}
    # get the crafting modes that the item have 
    h3s = soup.find_all("h3")
    span_tag = [h.find_all('span', {'class': 'mw-headline'}) for h in h3s]
    usedIn = []
    for s in span_tag:
        if s!= []:
            ids = s[0].get("id")
            usedIn.append(ids) 


    tables = soup.find_all('table', class_ = 'recipes')
    i = 0
    for t in tables:
        #print([f"\n{x}\n" for x in t.find_all('tr')])
        tr = t.find('tbody')
        #all right
        for tr in t.find_all('tr'):

            # Gets crafting station
            if tr.find('td',class_='station') != None: 
                stations = [x.get('title') for x in tr.find('td',class_='station').find_all('a', href=True)]
                stations = list(set(stations))
                #print(tr.find('td',class_='station').find_all('a', href=True))
                #print(crafings)

            # Handles diferent tables for diferent game versions 
            #print(tr.find('div',class_='version-note').find('a', href=True).get('title'))
            if (tr.find('div', class_='version-note')) != None and (tr.find('div', class_='version-note').find('a', href = True).get('title')) != 'Old-gen console version':
                #print('here1')
                itemCrafted = tr.find('td', class_='result').get('data-sort-value')
                li = tr.find('td', class_='ingredients').find_all('li')
                am = [li.find('span', class_='am') for li in li]
                ingredients = [(l.find('a',href = True).get('title')) for l in li]
                itemQtds = [(lambda x: 1 if x == None else x.text)(x) for x in am]
                

            elif tr.find('span', class_='eico') != None and tr.find('span', class_='eico').get('title')== "PC, Console, Mobile and tModLoader versions":
                itemCrafted = tr.find('a', href=True).get('title')
                #print('here2')
                li = tr.find('td', class_='ingredients').find_all('li')
                am = [li.find('span', class_='am') for li in li]
                ingredients = [(l.find('a',href = True).get('title')) for l in li]
                itemQtds = [(lambda x: 1 if x == None else x.text)(x) for x in am]

        craftingInfo[usedIn[i]] = [itemCrafted, ingredients, itemQtds, stations]
        i += 1
    return craftingInfo 

# Bad function
def getCraftingList(soup: bs) -> tuple:
    h3s = soup.find_all("h3")
    span_tag = [h.find_all('span', {'class': 'mw-headline'}) for h in h3s]
    usedIn = []
    for s in span_tag:
        if s!= []:
            ids = s[0].get("id")
            usedIn.append(ids) 

    crafitings = [[] for x in usedIn]
    i = 0
    for table in soup.find_all("table", class_ = "recipes"):
        stations = table.find_all('td', class_ = 'station')
        stations = list(set([s.get('title') for s in stations[0].find_all("a", href=True)]))
  
        shit = table.find_all('a', href=True)
        things = ([s.get('title') for s in shit])      
        #black magick 
        try:
            things = list(things[things.index("PC version")+4::])
        except:
            things = list(things[things.index("Crafting station")+1::])
        print(things)
        comp = []
        [comp.append(t) for t in things if t not in comp and t not in stations]
        things = comp

        crafitings[i] = [things,stations]
        i+=1 
    
    return usedIn, crafitings
    
def getDropInfo(soup: bs) -> dict:
    dropFrom = {}
    table = (soup.find('table', class_ = "drop-noncustom")).find('tbody')
    #print(table)
    for t in table.find_all('tr')[1::]:
        #print(f'\n{t}\n')
        #dropRate = t.find_all('td')[2].text
        
        mob = t.find('a', href = True).get('title')

        dropRate = t.find_all('td')[2].text
        try:
            dropRate = dropRate[:dropRate.index('*')] + "%"
        except:
            dropRate = dropRate
        dropQtd = t.find_all('td')[1].text
        dropFrom[mob] = [dropRate, dropQtd]
            
    #print(f'{table[0].find_all("tr", class_ ="")}\n')
    return dropFrom


#print(getHTML('bee keeper'))
#print((getCraftingListAlt(getHTML("Copper Shortsword"))))
#print(getDropInfo(getHTML('Bee keeper')))
