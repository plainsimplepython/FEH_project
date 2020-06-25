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



# TODO skill crawler
## TODO move into passive web crawler code
# table_markers = soup.find_all(class_="mw-headline")
# passive_table = table_markers[0].find_next('table')
#
#
# # print(passive_table)
# passive_rows = passive_table.find_all('tr')
# # print(passive_rows)
#
# # go through passive table gathering each passive url and name
# for i, row in enumerate(passive_rows):
#     if i != 0:
#         passive_data = row.find_all('td')
#         # print(passive_data)
#         for i, column in enumerate(passive_data):
#             if i == 1:
#                 # passive_name = column.text.strip()
#                 # print(passive_name)
#                 passive_link = column.find('a')
#                 print(passive_link)
#                 link = passive_link.get('href')
#                 print(link)
#                 name = passive_link.text.strip()
#                 print(name)



## QUEUE stuff
# passive_list_text_raw = [links.text for links in passive_table.find_all('a', title=True)]
# # print(passive_list_text_raw)
# passive_list = Queue()
#
# filter_list = ['adjacent', 'combat', 'initiates', 'initiates combat', 'during combat', 'cooldown charge', 'follow-up', 'within 2 spaces', 'Sol', 'Special cooldown', 'turn']
# for passive in passive_list_text_raw:
#     if not any(filter_term in passive for filter_term in filter_list):
#         passive_list.put(passive)
#
# print(list(passive_list.queue))
#
# while not passive_list.empty():


## GATHERS UNIQUE PASSIVE LINKS
# passive_set = set([links.get('href') for links in passive_table.find_all('a', href=True) if '/File:' not in links.get('href')])
# # [print(passive) for passive in passive_set]
#
# filtered_list = []
# filter_list = ['/Adjacent', '/Combat', '/Combat_boosts', '/Combat_Buffs', '/Initiates', '/Cooldown', '/Follow-up']
# for passive in passive_set:
#     if not any(filter_term in passive for filter_term in filter_list):
#         filtered_list.append(passive)
#
# [print(passive) for passive in filtered_list]
