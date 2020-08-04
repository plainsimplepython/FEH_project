from bs4 import BeautifulSoup
from urllib.request import urlopen
import ssl
import re


# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# TODO reduce redundancy of checking headers then getting them again and assigning them
# TODO merge assist/special after handling multiple 'cannot use' images links
# is 'Can Use' only for 'Staff' units? -> turn into 'Staff Only'?
# TODO create separate categories for Staff and Dancer?
# convert 'Can use' -> 'Staff Skill'?
# merge 'Exclusive' into 'Restrictions'?



# restriction: 'Exclusive' -> ['Exclusive']?
#####################
#####  WEAPONS  #####
#####################
# TODO evolved only skills? (slayer, smasher)
# TODO exclude umbra weapons
# TODO get effectiveness bonuses
def weapon_scraper(weapon_name_and_url):
    '''
    Dict Keys:
            Name:           <string>
            Weapon type:    <string>
            Might:          <string>
            Range:          <string>
            Effectiveness:  TODO
            Required:       <string>
            SP:             <string>
            Restrictions:   <string>
            String ID:      <string>
            Description:    <string>
            Upgrades:       (nested lists)
            List of Owners: (nested lists)
    '''

    weapon_name, weapon_url = weapon_name_and_url

    # # Ignore SSL certificate errors
    # ctx = ssl.create_default_context()
    # ctx.check_hostname = False
    # ctx.verify_mode = ssl.CERT_NONE

    # create url link from weapon name
    base_url = 'https://feheroes.gamepedia.com'
    # name = weapon_name.replace(' ', '_')
    name = weapon_url
    url = base_url + name

    # url = input('Enter weapon url - ')
    html = urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, "html.parser")

    weapon_table = soup.find('table', class_="wikitable default ibox")
    weapon_data = weapon_table.find_all('tr')

    weapon_dict = {}
    for i, data in enumerate(weapon_data):
        # weapon name
        if i == 0:
            weapon_dict['Name'] = data.find('th').text.strip()

        # weapon image, just skip
        elif i == 1:
            pass

        # weapon type
        elif i == 2:
            weapon_type = data.find('th').text.strip()
            weapon_dict[weapon_type] = data.find('a')['title']

        # weapon requirements
        elif data.find('th').text.strip() == 'Required':
            key = data.find('th').text.strip()
            value = []


            requirement_links = data.find_all('a')
            # check if weapon links exists in 'Required' row
            if requirement_links:
                # grab all possible requirements
                for requirement in requirement_links:
                    value.append(requirement.text.strip())

            # if weapon has no requirements return '—' instead
            else:
                value.append(data.find('td').text.strip())

            weapon_dict[key] = value


        # TODO weapon effectiveness bonuses (wait for them to finish the format?)
        # elif data.find('th').text.strip() == 'Effectiveness':
        #     for image in data.find_all("img"):
        #         print(image['src'])
        #         print(re.findall('Move_()\.png', image['src']))

        # weapon exclusive or not?
        elif 'Exclusive' in data.find('th').text.strip():
            # turn exclusive into restrictions and value from 'yes'/'no' -> 'exclusive'/null?
            key = 'Restrictions'
            value = None
            if data.find('td').text.strip() == 'Yes':
                value = 'Exclusive'
            # elif data.find('td').text.strip() == 'No':
            #     value = None

            weapon_dict[key] = value

        # Everything else within info table
        else:
            key = None
            if data.find('th'):
                key = data.find('th').text.strip()

                # # remove random question mark
                # if key == 'Exclusive?':
                #     key = 'Exclusive'


            value = None
            if data.find('td'):
                value = data.find('td').text.strip()

            weapon_dict[key] = value

            # print(f'row {i} - {key}: {value}')




    ######################
    #####  UPGRADES  #####
    ######################
    # if upgrades exist: get Icon, Stats, Description
    upgrades_marker = soup.find(id='Upgrades')
    if upgrades_marker:
        upgrades_table = upgrades_marker.find_next('table')

        upgrades = []
        # go into each row of the table
        for i, upgrade_row in enumerate(upgrades_table.find_all('tr')):
            if i != 0:  # skip 1st row of headers

                # collect data from each column per row
                upgrade_data = upgrade_row.find_all('td')
                upgrade = []
                for i, row in enumerate(upgrade_data):
                    # upgrade images
                    if i == 0:
                        upgrade_image_list = row.find("img")['src']  # 'src' gives 1x size
                        upgrade_images = re.findall("(https://[^ ]*)", str(upgrade_image_list))

                        # upgrade_image_list = row.find("img")['srcset']  # 'srcset' gives 1.5x and 2x
                        # image_size = 1.5
                        # upgrade_images = re.findall(f"(https://[^ ]*) {image_size}x", str(upgrade_image_list))

                        upgrade.append(upgrade_images[0])

                    # upgrade stats
                    if i == 1:
                        upgrade_stats = row.text.strip()
                        upgrade.append(upgrade_stats)

                    # upgrade descriptions
                    if i == 2:
                        upgrade_description = row.text.strip()
                        upgrade.append(upgrade_description)

                upgrades.append(upgrade)


        weapon_dict['Upgrades'] = upgrades




    #######################
    #####  EVOLUTION  #####
    #######################
    evolution_marker = soup.find(id='Evolution')
    if evolution_marker:
        evolution_table = evolution_marker.find_next('table')

        weapon_dict['Evolution'] = evolution_table.find('a')['title']




    ############################
    #####  LIST OF OWNERS  #####
    ############################
    owner_list_marker = soup.find(id='List_of_owners')
    skill_owners = []
    owner_list_table = owner_list_marker.find_next('table')

    for i, owner_list_row in enumerate(owner_list_table.find_all('tr')):
        # skip 1st row of headers
        if i != 0:
            # temp_list = [] TODO remove
            owner_data = owner_list_row.find_all(text=True)
            hero_rarity = tuple()

            # zipping owner data, which is one single list of data that's supposed to be grouped by pairs
            acquisition_tuples = list(zip(owner_data[1:-1:2], owner_data[2::2]))
            for acquisition_tuple in acquisition_tuples:
                # TODO find skill in chain and attach its acquired rarity to each hero
                if acquisition_tuple[0] in weapon_name:
                    hero_rarity = owner_data[0], acquisition_tuple[1]
                    # temp_list.append(hero_rarity) TODO remove

            # leave list of owners empty if none found
            if hero_rarity:
                skill_owners.append(hero_rarity)
            else:
                continue

    # print(skill_owners)
    weapon_dict['List of Owners'] = skill_owners
    print(weapon_dict)

    return weapon_dict


# weapon_scraper(('Armorsmasher%2B',"/Armorsmasher%2B"))  # TODO for debugging
'''TESTS 
('Falchion',"/Falchion_(Awakening)")
('Killing Edge+',"/Killing_Edge+")
('Slaying Edge+',"/Slaying_Edge+")
('Naga',"/Naga_(tome)")
('Armorsmasher%2B',"/Armorsmasher%2B")
'''


# TODO restriction: 'Exclusive' -> ['Exclusive']?
# TODO fix list of owners
#####################
#####  ASSISTS  #####
#####################
def assist_scraper(assist_name_and_url):
    assist_name, assist_url = assist_name_and_url

    # create base url link
    base_url = 'https://feheroes.gamepedia.com'
    # clean up weapon name format?
    # name = assist_name.replace(' ', '_')
    name = assist_url
    # join with weapon name
    url = base_url + name

    # url = input('Enter assist url - ')
    html = urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, "html.parser")

    assist_table = soup.find('table', class_="wikitable skills-table")
    assist_table_rows = assist_table.find_all('tr')
    # looking at all table headers and data
    # print(assist_table.find_all('th'))
    # print(assist_table.find_all('td'))



    # name
    # range
    # description
    # sp?
    # required?
    # legendary skill
    # restrictions
    assist_dict = {}
    table_headers = []
    table_data = []
    # exclusive tells if skill can be inherited or not
    # exclusive = 'No'
    # what class restrictions apply to skill
    restrictions = ''


    # go through skill data table row by row
    for i, row in enumerate(assist_table_rows):
        # row 1 has data labels
        if i == 0:
            table_headers = [row_one_header.text.strip() for row_one_header in row.find_all('th')]
            # print(table_headers)

        # row 2 has skill data
        if i == 1:
            # table_data = [row_two_data.text.strip() for row_two_data in row.find_all('td')]

            for assist_data in row.find_all('td'):
                # multiple requirement skills lead to two different skills and are stored as links
                if assist_data.find_all('a'):
                    required_list = [required_links.text for required_links in assist_data.find_all('a')]
                    table_data.append(', '.join(required_list))
                # required skills from the same skill chain are plain text
                else:
                    table_data.append(assist_data.text.strip())

            # print(table_data)

        # row 3 has weapon/move type and exclusive restrictions
        if i == 2:
            if row.find_all('a'):
                restrictions = row.find_all('a')[0]['title']

            else:
                restrictions = row.find('td').text.strip()

                if restrictions == 'This skill can only be equipped by its original unit.':
                    restrictions = 'Exclusive'
                    # exclusive = 'Yes'

                elif restrictions == 'This skill can only be equipped by staff users.':
                    restrictions = 'Staff only'

                elif restrictions == 'No restrictions.':
                    restrictions = None

    for key, value in zip(table_headers, table_data):
        assist_dict[key] = value

    # assist_dict['Exclusive'] = exclusive
    assist_dict['Restrictions'] = restrictions
    # print(assist_dict)


    ####################################
    #####  ASSIST: LIST OF OWNERS  #####
    ####################################
    owner_list_marker = soup.find(id='List_of_owners')
    skill_owners = []
    owner_list_table = owner_list_marker.find_next('table')

    for i, owner_list_row in enumerate(owner_list_table.find_all('tr')):
        # skip 1st row
        # create (skill, rarity) tuples
        # TODO identify which is skill in question and which are part of the skill chain
        if i != 0:
            # temp_list = [] # TODO remove
            # print([owner.text.strip() for owner in owner_list_row])
            owner_data = owner_list_row.find_all(text=True)
            hero_rarity = tuple()
            # temp_list.append(owner_data[0])   # TODO remove

            # skip first element, the character's name
            acquisition_tuples = list(zip(owner_data[1:-1:2], owner_data[2::2]))
            for acquisition_tuple in acquisition_tuples:
                if acquisition_tuple[0] in assist_name:
                    hero_rarity = owner_data[0], acquisition_tuple[1]
                # temp_list.append(acquisition_tuple)

            # leave list of owners empty if none found
            if hero_rarity:
                skill_owners.append(hero_rarity)
            else:
                continue
            # skill_owners.append(temp_list)

    assist_dict['List of Owners'] = skill_owners


    {print(f'{key}: {value}') for key, value in assist_dict.items()}
    return assist_dict

# assist_scraper(('Rally Atk/Res', '/Rally_Atk_Res')) # TODO for debugging



# TODO restriction: 'Exclusive' -> ['Exclusive']?
# TODO exclude umbra specials
# TODO fix list of owners
######################
#####  SPECIALS  #####
######################
def special_scraper(special_name_and_url):
    '''
    Dict Keys:
            Name:
            Cooldown:
            Description:
            SP:
            Required:
            # Exclusive:
            Restrictions: (String, List, or None)
            List of Owners: (nested lists)
    '''

    special_name, special_url = special_name_and_url

    # create base url link
    base_url = 'https://feheroes.gamepedia.com'
    # clean up weapon name format?
    # name = special_name.replace(' ', '_')
    name = special_url
    # join with weapon name
    url = base_url + name

    # url = input('Enter special url - ') # for testing purposes
    html = urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, "html.parser")

    special_table = soup.find('table', class_="wikitable skills-table")
    special_table_rows = special_table.find_all('tr')


    special_dict = {}
    table_headers = []
    table_data = []
    # exclusive tells if skill can be inherited or not
    # exclusive = 'No'
    # what class restrictions apply to skill
    restrictions = ''

    # name
    # cd
    # description
    # sp
    # required?
    # legendary skill (cannot be inherited text)
    # restrictions
    # go through skill data table row by row
    for i, row in enumerate(special_table_rows):
        # row 1 has data labels
        if i == 0:
            table_headers = [row_one_header.text.strip() for row_one_header in row.find_all('th')]
            # print(table_headers)

        # row 2 has skill data
        # separate multiple required skills (aethers, hybrid balms)
        if i == 1:
            # table_data = [row_two_data.text.strip() for row_two_data in row.find_all('td')]

            for row_two_data in row.find_all('td'):
                # multiple requirement skills lead to two different skills and are stored as links
                if row_two_data.find_all('a'):
                    required_list = [required_links.text for required_links in row_two_data.find_all('a')]
                    table_data.append(', '.join(required_list))
                # required skills from the same skill chain are plain text
                else:
                    table_data.append(row_two_data.text.strip())
                # print(table_data)

        # row 3 has weapon/move type and exclusive restrictions
        if i == 2:
            if row.find_all('a'):
                # cannot_use = row.find_all('a')[0]['title']
                restrictions = [restriction['title'] for restriction in row.find_all('a')]

            else:
                restrictions = row.find('td').text.strip()

                if restrictions == 'This skill can only be equipped by its original unit.':
                    restrictions = 'Exclusive'
                    # exclusive = 'Yes'

                elif restrictions == 'This skill can only be equipped by staff users.':
                    restrictions = 'Staff only'

                elif restrictions == 'No restrictions.':
                    restrictions = None

    for key, value in zip(table_headers, table_data):
        special_dict[key] = value

    # for key, value in zip(table_headers, table_data):
    #     special_dict[key] = value

    # special_dict['Exclusive'] = exclusive
    special_dict['Restrictions'] = restrictions


    # {print(f'{key}: {value}') for key, value in special_dict.items()}

    #####################################
    #####  SPECIAL: LIST OF OWNERS  #####
    #####################################
    owner_list_marker = soup.find(id='List_of_owners')

    # TODO exclude umbra skills
    # check if skill has any owners, by checking if there's <p> text (having to strip extra spaces) saying there's no owners
    skill_has_no_owners = owner_list_marker.find_next('p')
    if skill_has_no_owners:
        # special_has_owners.text.strip() == "This skill is currently not owned by any unit.":
        skill_owners = None

    # otherwise retrieving owners table
    else:
        skill_owners = []
        owner_list_table = owner_list_marker.find_next('table')

        for i, owner_list_row in enumerate(owner_list_table.find_all('tr')):
            # skip 1st row
            # TODO if skill owner rarity is null go to character page and retrieve it
            # TODO identify which is skill in question and which are part of the skill chain
            if i != 0:
                temp_list = []
                # print([owner.text.strip() for owner in owner_list_row])
                owner_data = owner_list_row.find_all(text=True)
                temp_list.append(owner_data[0])

                hero_rarity = tuple()
                acquisition_tuples = list(zip(owner_data[1:-1:2], owner_data[2::2]))
                for acquisition_tuple in acquisition_tuples:
                    if acquisition_tuple[0] in special_name:
                        hero_rarity = owner_data[0], acquisition_tuple[1]
                    # temp_list.append(acquisition_tuple)

                skill_owners.append(hero_rarity)
                # skill_owners.append(temp_list)


    special_dict['List of Owners'] = skill_owners

    {print(f'{key}: {value}') for key, value in special_dict.items()}
    return special_dict

    # notes?
# special_scraper(('Radiant Aether', '/Radiant_Aether')) # TODO for debugging

'''
# classify specials similar to table at bottom of page? 
https://feheroes.gamepedia.com/Galeforce
'''



######################
###### PASSIVES ######
######################
def passives_scraper(passive_name_and_url):
    '''
    Dict Keys:
            Type:
            Icon:
            Name:
            SP:
            Required:
            Description:
            # Exclusive:
            Restrictions: (String, List, or None)
            List of Owners: (nested lists)
    '''

    passive_name, passive_url = passive_name_and_url

    # create base url link
    base_url = 'https://feheroes.gamepedia.com'
    name = passive_url
    # join with weapon name
    url = base_url + name

    # url = input('Enter passive url - ')
    # url = 'https://feheroes.gamepedia.com/Passives'
    html = urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, "html.parser")

    passive_table = soup.find(class_="wikitable default skills-table")

    passives_dict = {}


    # get table headers
    passive_table_headers = passive_table.find_all('th')
    passive_table_headers_list = [header.text.strip() for header in passive_table_headers[1:-1]]
    # [print(header.text.strip()) for header in passive_table_headers]
    # print(passive_table_headers_list)
    # print()
    passives_dict[passive_table_headers[0].text.strip()] = passive_table_headers[-1].text.strip()

    passive_table_rows = passive_table.find_all('tr')
    skill_list = []
    # go through each row of skills of the skill table, first row  is skill headers, last row is skill restrictions
    for row in passive_table_rows[1:-1]:
        skill_data = []
        # collect column data of each skill row
        row_data = [column for column in row.find_all('td')]
        for i, column in enumerate(row_data):
            # first column has skill icon
            if i == 0:
                skill_data.append(row.find('img')['src'])

            # skill requirements need to be handled differently for single req vs multiple req
            elif i == 3:
                # multiple requirement skills lead to two different skills and are stored as links
                if column.find_all('a'):
                    required_list = [required_links.text.strip() for required_links in column.find_all('a')]
                    skill_data.append(', '.join(required_list))
                # required skills from the same skill chain are plain text
                else:
                    skill_data.append(column.text.strip())

            else:
                skill_data.append(column.text.strip())

        skill_list.append(skill_data)


    # skill list contains data of ALL skills of the skill chain, we only want the one passed to the function
    for skill in skill_list:
        # 2nd element has skill name, which we're going to use to identify the skill we're searching for
        if skill[1] == passive_name:
            for key, value in zip(passive_table_headers_list, skill):
                passives_dict[key] = value


    passive_table_data = passive_table.find_all('td')
    passive_data_list = passive_table_data[1:-1]
    # print(passive_data_list)
    # get individual passive data
    # passive_data_list = passive_table.find_all('td')[1:-1]
    passive_skills = [data.text.strip() for data in passive_data_list if data.text.strip() != '']
    # print(passive_skills)

    # last row has any class restrictions of this group of passives
    passive_restrictions = passive_table_data[-1]
    # print()
    # print(passive_restrictions.text)


    # labels any restrictions that apply to skill
    restrictions = ''


    if passive_restrictions.find_all('a'):
        restrictions = [restriction['title'] for restriction in passive_restrictions.find_all('a')]

    else:
        restrictions = passive_restrictions.text.strip()

        if restrictions == 'This skill can only be equipped by its original unit.':
            restrictions = 'Exclusive'
            # exclusive = 'Yes'

        elif restrictions == 'This skill can only be equipped by staff users.':
            restrictions = 'Staff only'

        elif restrictions == 'No restrictions.':
            restrictions = None

    # passive_skill_dict['Exclusive'] = exclusive
    passives_dict['Restrictions'] = restrictions



    #####################################
    #####  PASSIVE: LIST OF OWNERS  #####
    #####################################
    owner_list_marker = soup.find(id='List_of_owners')

    # check if skill has any owners, by checking if there's <p> text (having to strip extra spaces) saying there's no owners
    # skill_has_no_owners = owner_list_marker.find_next('p')
    # if skill_has_no_owners:
    #     # special_has_owners.text.strip() == "This skill is currently not owned by any unit.":
    #     skill_owners = None
    #
    # # otherwise retrieving owners table
    # else:
    skill_owners = []
    owner_list_table = owner_list_marker.find_next('table')

    for i, owner_list_row in enumerate(owner_list_table.find_all('tr')): # TODO string slice instead of enumerate?
        # skip 1st row
        # create (skill, rarity) tuples
        # TODO identify which is skill in question and which are part of the skill chain
        if i != 0:
            temp_list = []
            # print([owner.text.strip() for owner in owner_list_row])
            owner_data = owner_list_row.find_all(text=True)
            temp_list.append(owner_data[0])

            hero_rarity = tuple()
            acquisition_tuples = list(zip(owner_data[1:-1:2], owner_data[2::2]))
            for acquisition_tuple in acquisition_tuples:
                if acquisition_tuple[0] in passive_name:
                    hero_rarity = owner_data[0], acquisition_tuple[1]
                    # temp_list.append(acquisition_tuple)

                    skill_owners.append(hero_rarity)
            # skill_owners.append(temp_list)

    # print(skill_owners)
    passives_dict['List of Owners'] = skill_owners


    # print(passives_dict)
    # print()
    # {print(f'{key}: {value}') for key, value in passives_dict.items()}
    return passives_dict


# passives_scraper(('Atk/Res Push 3', '/Atk_Res_Push'))
# passives_scraper("Atk/Def Form 2")
# passives_scraper("Ostian Counter")

