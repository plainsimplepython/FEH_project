# To run this, download the BeautifulSoup zip file
# http://www.py4e.com/code3/bs4.zip
# and unzip it in the same directory as this file

from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import re

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = input('Enter Url - ')
html = urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, "html.parser")


''' gets hero info table:
 1st row: name and title
 2nd row: portrait art
 3rd row: description
 4th row: rarity
 5th row: weapon type
 6th row: movement type
 7th row: voice actor EN
 8th row: voice actor JP
 9th row: release date
10th row: addition date
11th row: game appearance
12th row: ???
13th row: origin?
'''
hero_info_table = soup.find('table', class_="wikitable hero-infobox")
character_data = hero_info_table.find_all('tr')


## character NAME and TITLE
name = []
for i in character_data[0].find_all('span'):
    name.append(i.text)
# TODO debug msg
print("Name and Title:", name)


## character IMAGES
image_table_data = character_data[1].find_all("img")
# search for image links in each 'img' tag
image_list = re.findall("https://[^ ]+", str(image_table_data))
# 3 sizes per image
# TODO debug msg
print("Character Portraits:", image_list, sep='\n')


## character DESCRIPTION
description_header = character_data[2].find('th').text.strip()
# gets description data text
description = character_data[2].find('td').text.strip()
# TODO debug msg
print(description_header, description, sep=': ')


## RARITY
rarity_header = character_data[3].find('th').text.strip()
# gets which rarities character can be acquired at
rarity = character_data[3].find('td').text.strip()
# TODO debug msg
print(rarity_header, rarity, sep=': ')


## Weapon Type
weapon_type_header = character_data[4].find('th').text.strip()
weapon_type = character_data[4].find('td').text.strip()
# TODO debug msg
print(weapon_type_header, weapon_type, sep=': ')


## Movement Type
movement_type_header = character_data[5].find('th').text.strip()
movement_type = character_data[5].find('td').text.strip()
# TODO debug msg
print(movement_type_header, movement_type, sep=': ', end='\n\n')



## character LEVEL 40 STATS
# find stat file marker
stats_marker = soup.find(id='Level_40_stats')
# stat header label
print(stats_marker.text)
# get the stats table after the stat marker
stats_table = stats_marker.find_next('table')
stats_rows = stats_table.find_all('tr')

## get Level 40 Stat LABELS
stat_labels = [label.text for label in stats_rows[0].find_all('th')]
# TODO debug msg
print(stat_labels)

# TODO make into a dict?
## get Level 40 Stats
level_40_stats = [stat.text for stat in stats_rows[-1].find_all('td')]
# TODO debug msg
print(level_40_stats)



## WEAPONS
''' finds the <span> tag with 'Weapons'
 retrieves the table following 'Weapons' tag 
 gets and prints table row header/data '''
weapons_marker = soup.find('span', id="Weapons")
print()
# weapon header
print(weapons_marker.text)

weapons_table = weapons_marker.find_next('table')
weapons_rows = weapons_table.find_all('tr')

table_size = len(weapons_rows)
weapons = []
# TODO iterate directly over table.find_all('tr')?
for i in range(table_size):
    weapons_row = weapons_rows[i]

    weapons_table_header = weapons_row.find_all('th')
    table_data = weapons_row.find_all('td')

    ## getting table data by row to display for debugging
    table_header = [data.text.strip() for data in weapons_table_header]
    table_data = [data.text.strip() for data in table_data]

    # getting each weapon data
    # skip first row, only contains headers and no table data
    if i is not 0:
        weapons.append(table_data)


weapon_labels = [label.text for label in weapons_table.find_all('th')]
print(weapon_labels)
[print(weapon) for weapon in weapons]



# TODO check for - title="List of evolving weapons"
upgrades = weapons_marker.find_next('p')
# upgrades_exist = upgrades.find("a", title="List of evolving weapons")
# print(upgrades_exist)
if upgrades:
    # upgrade_images = [image['src'] for image in upgrades.find_all('img')]
    # TODO handle case where upgrades exist but no images?
    upgrade_image_list = upgrades.find_all("img")
    upgrade_images = re.findall("https://[^ ]+", str(upgrade_image_list))
    # TODO print each image set in separate rows
    # TODO with image headers?
    ## gets all of the upgrade info
    # TODO split upgrade text sentences into list
    # TODO extra spaces in upgrade test are image locations?
    print(upgrades.text.strip())
    print("Weapon Upgrade Icons:", upgrade_images, sep='\n')
    # print(upgrade_image_list)
else:
    print("No weapon upgrades.")


# TODO trying to get the weapon upgrade from the <a> "title="
# tags = upgrades.find_all('a')
# [print(tag) for tag in tags]
# print(tags)


# for a_tag in upgrades.find_all('a'):
#     print(a_tag)
#     print(a_tag.text)
#     print(a_tag.nextSibling)
#     print()



## ASSISTS
''' finds the <span> tag with 'Assists'
 retrieves the table following 'Assists' tag 
 gets and prints table row header/data '''

assists_marker = soup.find(id="Assists")
print()
print(assists_marker.text)

# check if hero has ASSIST skills or not
assists_table = assists_marker.find_next('div').text
if assists_table == "This Hero owns no Assist skills.":
    print(assists_table)
else:
    assists_table = assists_marker.find_next('table')
    assists = []

    for row in assists_table.find_all('tr'):
        table_header = row.find_all('th')
        table_data = row.find_all('td')

        table_header = [data.text.strip() for data in table_header]
        table_data = [data.text.strip() for data in table_data]

        if len(table_data) != 0:
            assists.append(table_data)

    # TODO debug msgs
    assists_label = [label.text for label in assists_table.find_all('th')]
    print(assists_label)
    [print(assist) for assist in assists]



## SPECIALS
''' finds the <span> tag with 'Specials'
 retrieves the table following 'Specials' tag 
 gets and prints table row header/data '''

specials_marker = soup.find(id="Specials")
print()
print(specials_marker.text)


specials_table = specials_marker.find_next('div').text
if specials_table == "This Hero owns no Special skills.":
    print(specials_table)
else:
    specials_table = specials_marker.find_next('table')
    specials = []

    for row in specials_table.find_all('tr'):
        table_header = row.find_all('th')
        table_data = row.find_all('td')

        table_header = [data.text.strip() for data in table_header]
        table_data = [data.text.strip() for data in table_data]

        if len(table_data) != 0:
            specials.append(table_data)

    # TODO debug msgs
    specials_label = [label.text for label in specials_table.find_all('th')]
    print(specials_label)
    [print(special) for special in specials]



## PASSIVES
''' finds the <span> tag with 'Passives'
 retrieves the table following 'Passives' tag 
 gets and prints table row header/data '''

# TODO get passive images, empty 1st element is skill image
passives_marker = soup.find(id="Passives")
table = passives_marker.find_next('table')
rows = table.find_all('tr')

passives = []
table_size = len(rows)
for i in range(table_size):
    id_row = rows[i]

    table_header = id_row.find_all('th')
    table_data = id_row.find_all('td')

    table_header = [data.text.strip() for data in table_header]

    # TODO get passive skill icons
    passive_icons_raw = id_row.find_all("img")
    passive_icon_images = re.findall("https://[^ ]+", str(passive_icons_raw))
    # TODO incomplete, fix for passives
    # print(upgrades.text.strip())
    # print("Weapon Upgrade Icons:", upgrade_images, sep='\n')

    # TODO change to check either for img or text
    table_data = [data.text.strip() for data in table_data if data.text is not '']

    if len(table_data) != 0:
        # TODO if text table data is empty get images and append to passives
    #     # TODO append skill icon first
    #     passives.append(passive_icon_images)
    # else:
        passives.append(table_data)

#     print("tr:", id_row)
#     print("row text:", id_row.text)
#     print("th:", table_header)
#     print("td:", table_data)
#     print()
# print(rows)

print()
print(passives_marker.text)
# prints label
print([label.text for label in table.find_all('th') if label.text is not ''])
for element in passives:
    print(element)
# [print(passive) for passive in passives]









''' Useful Project Links:
https://feheroes.gamepedia.com/Fir:_Sword_Student
https://feheroes.gamepedia.com/Micaiah:_Queen_of_Dawn
Special Summon test:
https://feheroes.gamepedia.com/Fir:_Student_of_Spring
GHB test:
https://feheroes.gamepedia.com/Berkut:_Prideful_Prince
TT test:
https://feheroes.gamepedia.com/Black_Knight:_Sinister_General

https://feheroes.gamepedia.com/Hero_skills_table
https://feheroes.gamepedia.com/Level_40_stats_table
https://feheroes.gamepedia.com/List_of_Heroes
https://feheroes.gamepedia.com/Passives

Web App:
https://github.com/feh-stuff/feh-stuff.github.io


Gamepress:
https://gamepress.gg/feheroes/robots.txt
https://gamepress.gg/feheroes/heroes
https://gamepress.gg/feheroes/passive-skills
https://gamepress.gg/feheroes/special-skills
https://gamepress.gg/feheroes/support-skills
https://gamepress.gg/feheroes/weapon-skills

'''