from bs4 import BeautifulSoup
from queue import Queue
from urllib.request import urlopen
from urllib.parse import quote_plus
import ssl
from Hero_Crawler import hero_crawler


'''
Creates a list of heroes' information we need and sends each of their page
urls to the Hero_Crawler to scrape the information we want.
'''


HERO_LIST_URL = 'https://feheroes.gamepedia.com/List_of_Heroes'
BASE_URL = 'https://feheroes.gamepedia.com/'


# TODO get hero icons
# Ignore SSL certificates errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# url = input('Enter Url - ')   # for debugging
url = HERO_LIST_URL
html = urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, "html.parser")

hero_list_table = soup.find('table')
hero_list_text_raw = [links.text for links in hero_list_table.find_all('a', title=True)]

hero_list = Queue()
# character name text is only labeled by 'href' links,
# but that also includes other links we need to filter
filter_list = ['Fire Emblem', 'Special', 'Story', 'Tempest Trials', 'Grand Hero Battle', 'Mythic', 'Legendary', 'Tokyo Mirage']

# create list of all characters in game
for hero in hero_list_text_raw:
    if not any(filter_term in hero for filter_term in filter_list) and hero is not '':
        hero_list.put(hero)

# TODO debug msg
print(list(hero_list.queue))


while not hero_list.empty():
    ''' 
    go through the entire list of characters:
    creating each character url from base website and character name
    sending the full url to the character(hero) data scraper
    '''

    # website uses '_' for urls instead of spaces or url '+'s
    hero_url = hero_list.get().replace(' ', '_')
    # construct full url
    full_url = BASE_URL + quote_plus(hero_url)
    print(full_url)

    # have hero_crawler scrape the data from the character page
    hero_crawler(full_url)

