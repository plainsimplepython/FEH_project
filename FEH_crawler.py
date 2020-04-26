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

# TODO debug, looking at html format
# print(soup)


## prints out all <td> fields along with their number in list
# count = 0
# for data in soup.select('td'):
#     print('count:', count , data.text)
#     count += 1


## table list of header/data list elements


# table_contents = []
# for tr in rows:
#     if rows.index(tr) == 0:
#         row_cells = [th.getText().strip() for th in tr.find_all('th') if th.getText().strip() != '']
#     else:
#         row_cells = ([tr.find('th').getText()] if tr.find('th') else []) + [td.getText().strip() for td in
#                                                                             tr.find_all('td') if
#                                                                             td.getText().strip() != '']
#     if len(row_cells) > 1:
#         table_contents += [row_cells]
# # print(table_contents)
#
# for table in table_contents:
#     print(table)

## another way to pull data from tables
# table_data = soup.find('tbody')
# rows = table_data.find_all_next('tr')
# for row in rows:
#     text_header = row.find_all('th')
#     text_data = row.find_all('td')
#
#     text_header = [data.text.strip() for data in text_header]
#     text_data = [data.text.strip() for data in text_data]
#
#     print(text_data)




# print(soup.select("td")[0].text)
# print(soup.select("td")[12].text)
# print(soup.select("td")[13].text)
# print(soup.select("td")[14].text)
# print(soup.select("td")[15].text)
#
# for data in soup.select("td")[85:91]:
#     print(data.text)





hero_info = soup.find(class_="wikitable hero-infobox")
# rows = hero_info.find_all_next('tr')
# for row in rows:
#     table_header = row.find_all('th')
#     table_data = row.find_all('td')
#
#     table_header = [data.text.strip() for data in table_header]
#     table_data = [data.text.strip() for data in table_data]
#
#     print("tr:", row)
#     print("th:", table_header)
#     print("td:", table_data)
#     print()

# ids = soup.find('span', id="Assists")
# print(ids.text)



## pulls character NAME and TITLE - NO LONGER USED
# name = soup.select('h1', class_='firstHeading')
# print(name[0].text)


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
table = soup.find('table', class_="wikitable hero-infobox")
character_data = table.find_all('tr')
# table_size = len(character_data)
# for i in range(table_size):
#     id_row = character_data[i]
#     # for row in id_rows:
#     table_header = id_row.find_all('th')
#     table_data = id_row.find_all('td')
#
#     table_header = [data.text.strip() for data in table_header]
#     table_data = [data.text.strip() for data in table_data]
#
#     print(f"row {i}:")
#     print("tr:", id_row)
#     print("row text:", id_row.text)
#     print("th:", table_header)
#     print("td:", table_data)
#     print()


# get char NAME and TITLE
name_header_list = character_data[0].find_all("span")
name = []
for i in name_header_list:
    name.append(i.text)
print("Name and Title:", name)


## get char DESCRIPTION
description = character_data[2].find('td').text.strip()
print("Description:", description)


## get character IMAGES
image_table_data = character_data[1].find_all("img")
image_list = re.findall("https://[^ ]+", str(image_table_data))
print("Character Portraits:\n", image_list)

# TODO testing
# [print(image) for image in image_table_data]

# test_images = [re.findall("https://[^ ]+", str(image)) for image in image_table_data]
# print(test_images)
# print(image_table_data)


# get RARITY
rarity = character_data[3].find('td').text.strip()
print("Rarity", rarity)


# get Weapon Type
weapon_type = character_data[4].find('td').text.strip()
print(character_data[4].find('th').text.strip(), weapon_type)


# get Movement Type
movement_type = character_data[5].find('td').text.strip()
print(character_data[5].find('th').text.strip(), movement_type)
print('\n')


## pulls character LEVEL 40 STATS
stats = soup.find(id='Level_40_stats')
# header label
print(stats.text)
# retrieving data
stats_table = stats.find_next('table')
stats_rows = stats_table.find_all('tr')
# TODO debug msg
# print(stats_rows)

## TODO debug: displays full stats table data
# table_size = len(stats_rows)
# for i in range(table_size):
#     id_row = stats_rows[i]
#     # for row in id_rows:
#     table_header = id_row.find_all('th')
#     table_data = id_row.find_all('td')
#
#     table_header = [data.text.strip() for data in table_header]
#     table_data = [data.text.strip() for data in table_data]
#
#     print("tr:", id_row)
#     print("row text:", id_row.text)
#     print("th:", table_header)
#     print("td:", table_data)
#     print()
# print(stats)

## get Level 40 Stat LABELS
stat_labels = [label.text for label in stats_rows[0].find_all('th')]
# TODO debug
print(stat_labels)

# TODO make into a dict?
## get Level 40 Stats
level_40_stats = [stat.text for stat in stats_rows[-1].find_all('td')]
# TODO debug
print(level_40_stats)

## pulls character SKILLS
## WEAPON

''' finds the <span> tag with 'Weapons'
 retrieves the table following 'Weapons' tag 
 gets and prints table row header/data '''
ids = soup.find('span', id="Weapons")
# weapon header
print()
print(ids.text)
table = ids.find_next('table')
rows = table.find_all('tr')
# TODO debug msg
# print(rows)

table_size = len(rows)
weapons = []
# TODO iterate directly over table.find_all('tr')?
for i in range(table_size):
    id_row = rows[i]
    # for row in id_rows:
    table_header = id_row.find_all('th')
    table_data = id_row.find_all('td')

    ## getting table data by row to display for debugging
    table_header = [data.text.strip() for data in table_header]
    table_data = [data.text.strip() for data in table_data]

    # getting each weapon data
    # TODO skip first row
    if i is not 0:
        weapons.append(table_data)

    # TODO debug msgs
#     print("tr:", id_row)
#     print("row text:", id_row.text)
#     print("th:", table_header)
#     print("td:", table_data)
#     print()
# print(rows)
weapon_labels = [label.text for label in table.find_all('th')]
# weapons = [weapon.text for weapon in table.find_all('td')]
print(weapon_labels)
print(weapons)



# upgrades = ids.find_next('p')
## gets all of the upgrade info
# print(upgrades.text)


# TODO trying to get the weapon upgrade from the <a> "title="
# tags = upgrades.find_all('a')
# [print(tag) for tag in tags]
# print(tags)


# for a_tag in upgrades.find_all('a'):
#     print(a_tag)
#     print(a_tag.text)
#     print(a_tag.nextSibling)
#     print()


## pulls characters ASSISTS
## ASSISTS

''' finds the <span> tag with 'Assists'
 retrieves the table following 'Assists' tag 
 gets and prints table row header/data '''
# TODO handle no assist skill case
assists_marker = soup.find(id="Assists")

# print("ASSISTS: ")
# assist_table = assists.find_next('table', class_="wikitable default unsortable skills-table")
assists_table = assists_marker.find_next('div')
# print(assists_table.text)
if assists_table == "This Hero owns no Assist skills.":
    print(assists_table)
else:
    # print('assist table found')


    table = assists_marker.find_next('table')
    rows = table.find_all('tr')
    assists = [] # TODO change overlapping variable names?
    table_size = len(rows)
    for i in range(table_size):
        id_row = rows[i]
        # for row in id_rows:
        table_header = id_row.find_all('th')
        table_data = id_row.find_all('td')

        table_header = [data.text.strip() for data in table_header]
        table_data = [data.text.strip() for data in table_data]

        if i is not 0:
            assists.append(table_data)
    #
    #     print("tr:", id_row)
    #     print("row text:", id_row.text)
    #     print("th:", table_header)
    #     print("td:", table_data)
    #     print()
    # print(rows)

    print()
    print(assists_marker.text)
    assists_label = [label.text for label in table.find_all('th')]
    print(assists_label)
    print(assists)


## pulls characters SPECIALS
## SPECIALS

''' finds the <span> tag with 'Specials'
 retrieves the table following 'Specials' tag 
 gets and prints table row header/data '''
# TODO handle no specials skills case
specials_marker = soup.find(id="Specials")
table = specials_marker.find_next('table')
rows = table.find_all('tr')

# TODO lots of optimization needed
specials = []
table_size = len(rows)
for i in range(table_size):
    id_row = rows[i]

    table_header = id_row.find_all('th')
    table_data = id_row.find_all('td')

    table_header = [data.text.strip() for data in table_header]
    table_data = [data.text.strip() for data in table_data]

    if i is not 0:
        specials.append(table_data)

    # TODO debug msgs
    # print("tr:", id_row)
    # print("row text:", id_row.text)
    # print("th:", table_header)
    # print("td:", table_data)
    # print()
# print(rows)

print()
print(specials_marker.text)
specials_label = [label.text for label in table.find_all('th')]
print(specials_label)
print(specials)




## pulls characters PASSIVES
## PASSIVES

''' finds the <span> tag with 'Passives'
 retrieves the table following 'Passives' tag 
 gets and prints table row header/data '''
# TODO handle no passive skills case?
passives_marker = soup.find(id="Passives")
table = passives_marker.find_next('table')
rows = table.find_all('tr')

passives = []
table_size = len(rows)
for i in range(table_size):
    id_row = rows[i]
    # for row in id_rows:
    table_header = id_row.find_all('th')
    table_data = id_row.find_all('td')

    table_header = [data.text.strip() for data in table_header]
    table_data = [data.text.strip() for data in table_data]

    if i is not 0:
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
print([label.text for label in table.find_all('th')])
print(passives)









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


https://gamepress.gg/feheroes/robots.txt
https://gamepress.gg/feheroes/heroes
https://gamepress.gg/feheroes/passive-skills
https://gamepress.gg/feheroes/special-skills
https://gamepress.gg/feheroes/support-skills
https://gamepress.gg/feheroes/weapon-skills

'''