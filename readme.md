### TODO:
[X] Get quantity from craft list
[ ] Fix dropFrom fuction 
[ ] Make custom messages 
[X] Generic getStringAlt -> Can't do, made another function do deal with 
[X] Refactor getCrafingInfo func using:
[ ]
1. Get table
2. find_all('tr')
3. in tr if find("div", class_="version-note note-text small") != 'PC Version'
4. if not continue
5. if yes in tr find('td', class_='ingridients')
6. get href and title
7. qtd = find('span', class_='am').text
8. ikd.

### Steps:
1. Fetches the html code using requests
2. Use bs4 to scrape the info
3. Return a tuple with the info on how to craft and where
4. Transform the tuple information in a usable string
5. Send that string using discord bot api

### Special cases:
1. Bookcase item
2. Things that have diferent crafts in diferent versions.