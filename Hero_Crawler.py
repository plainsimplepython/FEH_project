# To run this, download the BeautifulSoup zip file
# http://www.py4e.com/code3/bs4.zip
# and unzip it in the same directory as this file

from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import re


def hero_crawler(url):
    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    # url = input('Enter Url - ')
    html = urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, "html.parser")


    ''' 
    hero info dict keys:
        Name (& title)
        Images (Portrait, Attack, Special, Injured) 3 sizes for each
        Description
        Rarities
        Acquisition
        Effect (blessing type)
        Ally Boost (blessing bonus)
        Duo Skill
        Standard Effect 1: Duel
        Standard Effect 2: Pair Up
        Weapon Type
        Move Type
        Voice Actor EN
        Voice Actor JP
        Release Date
        Appears in
        Internal ID
        Origin
        
        Stats
        Weapons
        Assists
        Specials
        Passives
    '''
    hero_info_table = soup.find('table', class_="wikitable hero-infobox")
    character_data = hero_info_table.find_all('tr')

    character_dict = {}
    for i, data in enumerate(character_data):
        # NAME and TITLE dont have a proper label
        if i is 0:
            name = []
            for element in data.find_all('span'):
                name.append(element.text)

            character_dict['Name'] = name


        ## character IMAGES, also lacks a label
        elif i is 1:
            image_table_data = data.find_all("img")
            # search for image links in each 'img' tag
            image_list = re.findall("https://[^ ]+", str(image_table_data))

            # 3 sizes per image
            character_dict['Images'] = image_list


        ## character RARITY and ACQUISITION text needs to be cleaned up and separated
        elif i is 3:
            # get the key for the rarity row
            if data.find('th'):
                rarity_key = data.find('th').text.strip()

            # get rarity data for the row
            if data.find('td'):
                rarity_data = data.find('td').text.strip()

                # remove random 'Focus' from rarity string
                rarity_data = rarity_data.replace('Focus', '')
                # remove random '*' from rarity string
                rarity_data = rarity_data.replace('*', '')
                # separate hero rarities and acquisition
                rarity_acquisition = rarity_data.split('—')

            # add hero rarities to dict
            character_dict[rarity_key] = rarity_acquisition[0].strip()
            # if hero has special method of being obtained, add hero acquisition to dict
            acquisition = None
            if len(rarity_acquisition) > 1:
                acquisition = rarity_acquisition[1].strip()
            character_dict['Acquisition'] = acquisition


        # get keys and values for the rest of the character data
        else:
            if data.find('th'):
                hero_info_header = data.find('th').text.strip()

            if data.find('td'):
                hero_info_data = data.find('td').text.strip()

            character_dict[hero_info_header] = hero_info_data


    # TODO debug msg
    {print(f"{key}: {value}") for key, value in character_dict.items()}
    print()



    ## character LEVEL 40 STATS
    # locate Level 40 STAT table
    stats_marker = soup.find(id='Level_40_stats')
    print(stats_marker.text)

    # get the stats table after the stat marker
    stats_table = stats_marker.find_next('table')
    stats_rows = stats_table.find_all('tr')

    ## get Level 40 Stat LABELS from first row
    stat_labels = [label.text for label in stats_rows[0].find_all('th')]
    # TODO debug msg
    print(stat_labels)

    ## get Level 40 Stats from last row
    level_40_stats = [stat.text for stat in stats_rows[-1].find_all('td')]
    # TODO debug msg
    print(level_40_stats)


    ''' 
    stats:
        hp
        atk
        spd
        def
        res
        total
    '''
    # add each stat key, value into stats dict
    character_stats = {}
    for key, value in zip(stat_labels, level_40_stats):
        character_stats[key] = value

    # finally add character stats to the dict
    character_dict['Stats'] = character_stats



    ## WEAPONS
    # locate WEAPON table
    weapons_marker = soup.find('span', id="Weapons")
    print()
    print(weapons_marker.text)

    # get weapon table
    weapons_table = weapons_marker.find_next('table')
    weapons = []

    for row in weapons_table.find_all('tr'):
        # weapons_table_header = row.find_all('th')
        weapons_table_data = row.find_all('td')

        ## getting table data by row to display for debugging
        # weapons_header = [data.text.strip() for data in weapons_table_header]
        weapons_data = [data.text.strip() for data in weapons_table_data]

        # getting each weapon data
        # skip first row, only contains headers and no table data
        if len(weapons_data) != 0:
            # weapons.append(weapons_data)  # gets all weapon data
            weapons.append(weapons_data[0]) # we only want to know the names of all weapons the character has


    weapon_labels = [label.text for label in weapons_table.find_all('th')]
    print(weapon_labels)
    [print(weapon) for weapon in weapons]

    # add weapon CSV to character dict
    character_dict['Weapons'] = ', '.join(weapons)


    ## WEAPON UPGRADES
    # TODO will get weapon upgrades from Skill_Crawler
    upgrades = weapons_marker.find_next('p')

    if upgrades:
        upgrade_image_list = upgrades.find_all("img")
        upgrade_images = re.findall("https://[^ ]+", str(upgrade_image_list))

        ## gets all of the upgrade info
        # TODO split upgrade text sentences into list
        # TODO extra spaces in upgrade test are image locations?
        print(upgrades.text.strip())
        print("Weapon Upgrade Icons:", upgrade_images, sep='\n')
    else:
        print("No weapon upgrades.")



    ## ASSISTS
    # locate ASSIST table
    assists_marker = soup.find(id="Assists")
    print()
    print(assists_marker.text)

    # check if hero has ASSIST skills
    assists_table = assists_marker.find_next('div').text
    if assists_table == "This Hero owns no Assist skills.":
        character_dict['Assists'] = None
        print(assists_table)

    # retrieving them if they exist
    else:
        assists_table = assists_marker.find_next('table')
        assists = []

        for row in assists_table.find_all('tr'):
            assists_table_data = row.find_all('td')

            assists_data = [data.text.strip() for data in assists_table_data]

            if len(assists_data) != 0:
                # assists.append(assists_data)  # gets all assist data
                assists.append(assists_data[0])    # we only want the names of character's assists

        # TODO debug msgs
        [print(assist) for assist in assists]

        character_dict['Assists'] = ', '.join(assists)



    ## SPECIALS
    # locate SPECIAL table
    specials_marker = soup.find(id="Specials")
    print()
    print(specials_marker.text)

    # check if hero has SPECIAL skills
    specials_table = specials_marker.find_next('div').text
    if specials_table == "This Hero owns no Special skills.":
        character_dict['Specials'] = None
        print(specials_table)

    # retrieving them if they exist
    else:
        specials_table = specials_marker.find_next('table')
        specials = []

        for row in specials_table.find_all('tr'):
            specials_table_data = row.find_all('td')

            specials_data = [data.text.strip() for data in specials_table_data]

            if len(specials_data) != 0:
                # specials.append(specials_data)  # gets all specials data
                specials.append(specials_data[0])  # we only want the names of the character's specials

        # TODO debug msgs
        specials_label = [label.text for label in specials_table.find_all('th')]
        print(specials_label)
        [print(special) for special in specials]

        character_dict['Specials'] = ', '.join(specials)




    ## PASSIVES
    # locate PASSIVES table
    passives_marker = soup.find(id="Passives")
    print()
    print(passives_marker.text)
    passives_table = passives_marker.find_next('table') # TODO remove?


    # handle no passives case (fuck you masked marth)
    # check if hero has PASSIVE skills
    passives_table = passives_marker.find_next('div').text
    if passives_table == "This hero owns no Passive skills.":   # why is 'Hero' lowercase here?!
        character_dict['Passives'] = None
        print(passives_table)

    # retrieving them if they exist
    else:
        passives_table = passives_marker.find_next('table')

        passives = []
        for row in passives_table.find_all('tr'):
            passives_table_data = row.find_all('td')

            # TODO get passive skill icons?
            # passive_icons_raw = row.find_all("img")
            # passive_icon_images = re.findall("https://[^ ]+", str(passive_icons_raw))
            # print(passive_icon_images)

            # empty 1st element is skill image
            passives_data = [data.text.strip() for data in passives_table_data if data.text is not '']

            if passives_data:
                # passives.append(passives_data)  # gets all passive data
                passives.append(passives_data[0])  # we only want the names of character's skills


        # prints label
        print([label.text for label in passives_table.find_all('th') if label.text is not ''])
        for passive in passives:
            print(passive)

        character_dict['Passives'] = ', '.join(passives)




    # finally add character information to database
    import Create_Database
    Create_Database.create_database(character_dict)



''' Useful Project Links:
https://feheroes.gamepedia.com/Fir:_Sword_Student
https://feheroes.gamepedia.com/Micaiah:_Queen_of_Dawn

Special Summon test:
https://feheroes.gamepedia.com/Fir:_Student_of_Spring
https://feheroes.gamepedia.com/Rafiel:_Blessed_Wings

GHB test:
https://feheroes.gamepedia.com/Berkut:_Prideful_Prince

TT test:
https://feheroes.gamepedia.com/Black_Knight:_Sinister_General

Duo Unit test:
https://feheroes.gamepedia.com/Micaiah:_Dawn_Wind%27s_Duo

pre Pair-Up Legendary test:
https://feheroes.gamepedia.com/Hector:_Marquess_of_Ostia

Pair-Up Legendary test:
https://feheroes.gamepedia.com/Celica:_Queen_of_Valentia

Mythic:
https://feheroes.gamepedia.com/Yune:_Chaos_Goddess

Additional tables:
https://feheroes.gamepedia.com/Hero_skills_table
https://feheroes.gamepedia.com/Level_40_stats_table
https://feheroes.gamepedia.com/List_of_Heroes
https://feheroes.gamepedia.com/Weapons
https://feheroes.gamepedia.com/Weapons_(full)
https://feheroes.gamepedia.com/Assists
https://feheroes.gamepedia.com/Specials
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