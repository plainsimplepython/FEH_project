from bs4 import BeautifulSoup
from urllib.request import urlopen
import ssl


# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# TODO merge assist/special after handling multiple 'cannot use' images links
# TODO is 'Can Use' only for 'Staff' units? -> turn into 'Staff Only'?
# TODO create separate categories for Staff and Dancer?
## convert 'Can use' -> 'Staff Skill'?

# weapons
def weapon_scraper():
    # # Ignore SSL certificate errors
    # ctx = ssl.create_default_context()
    # ctx.check_hostname = False
    # ctx.verify_mode = ssl.CERT_NONE

    url = input('Enter weapon url - ')
    html = urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, "html.parser")

    weapon_table = soup.find('table', class_="wikitable default ibox")
    weapon_data = weapon_table.find_all('tr')

    weapon_dict = {}
    for i, data in enumerate(weapon_data):
        # name
        if i == 0:
            weapon_dict['Name'] = data.find('th').text.strip()

        elif i == 1:
            pass

        # weapon type
        elif i == 2:
            weapon_type = data.find('th').text.strip()
            weapon_dict[weapon_type] = data.find('a')['title']

        # might
        # range
        # required?
        # SP?
        # exclusive
        # description
        else:
            key = None
            if data.find('th'):
                key = data.find('th').text.strip()

                # remove random question mark
                if key == 'Exclusive?':
                    key = 'Exclusive'

            value = None
            if data.find('td'):
                value = data.find('td').text.strip()

            weapon_dict[key] = value

            print(f'row {i} - {key}: {value}')



    # upgrades or none case
    upgrades_marker = soup.find(id='Upgrades')
    upgrades = []
    if upgrades_marker:
        upgrades_table = upgrades_marker.find_next('table')

        for upgrade_row in upgrades_table.find_all('tr'):
            # headers = row.find_all('th')
            # if headers:
            #     print([header.text.strip() for header in headers])

            upgrade_data = upgrade_row.find_all('td')
            if upgrade_data:
                # TODO get icon?
                upgrades.append([upgrade.text.strip() for upgrade in upgrade_data])
            weapon_dict['Upgrades'] = upgrades



    # list of owners
    owner_list_marker = soup.find(id='List_of_owners')
    skill_owners = []
    owner_list_table = owner_list_marker.find_next('table')

    for i, owner_list_row in enumerate(owner_list_table.find_all('tr')):
        # skip 1st row
        # create (skill, rarity) tuples
        # TODO identify which is skill question and which are part of the skill chain
        if i != 0:
            temp_list = []
            # print([owner.text.strip() for owner in owner_list_row])
            owner_data = owner_list_row.find_all(text=True)
            temp_list.append(owner_data[0])

            acquisition_tuples = list(zip(owner_data[1:-1:2], owner_data[2::2]))
            for acquisition_tuple in acquisition_tuples:
                temp_list.append(acquisition_tuple)

            skill_owners.append(temp_list)
    # print(skill_owners)
    weapon_dict['List of Owners'] = skill_owners







    # notes?
    # languages?
    print(weapon_dict)
# weapon_scraper()  # TODO for debugging



# assists
def assist_scraper(url):
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
    exclusive = 'No'
    # can_use states weapon/move types that skill limited to
    can_use = ''      # TODO None or ''?
    # cannot_use states weapon/move types that CANT use the skill
    cannot_use = ''   # TODO None or ''?

    # go through skill data table row by row
    for i, row in enumerate(assist_table_rows):
        # row 1 has data labels
        if i == 0:
            table_headers = [row_one_header.text.strip() for row_one_header in row.find_all('th')]
            # print(table_headers)

        # row 2 has skill data
        if i == 1:
            table_data = [row_two_data.text.strip() for row_two_data in row.find_all('td')]
            # print(table_data)

        # row 3 has weapon/move type and exclusive restrictions
        if i == 2:
            if row.find_all('a'):
                cannot_use = row.find_all('a')[0]['title']

            else:
                can_use = row.find('td').text.strip()

                if can_use == 'This skill can only be equipped by its original unit.':
                    can_use = ''
                    exclusive = 'Yes'

                if can_use == 'This skill can only be equipped by staff users.':
                    can_use = 'Staff'

    for key, value in zip(table_headers, table_data):
        assist_dict[key] = value

    assist_dict['Exclusive'] = exclusive
    assist_dict['Can Use'] = can_use
    assist_dict['Cannot Use'] = cannot_use
    # print(assist_dict)



    # list of owners
    owner_list_marker = soup.find(id='List_of_owners')
    skill_owners = []
    owner_list_table = owner_list_marker.find_next('table')

    for i, owner_list_row in enumerate(owner_list_table.find_all('tr')):
        # skip 1st row
        # create (skill, rarity) tuples
        # TODO identify which is skill in question and which are part of the skill chain
        if i != 0:
            temp_list = []
            # print([owner.text.strip() for owner in owner_list_row])
            owner_data = owner_list_row.find_all(text=True)
            temp_list.append(owner_data[0])

            acquisition_tuples = list(zip(owner_data[1:-1:2], owner_data[2::2]))
            for acquisition_tuple in acquisition_tuples:
                temp_list.append(acquisition_tuple)

            skill_owners.append(temp_list)
    # print(skill_owners)
    assist_dict['List of Owners'] = skill_owners


    {print(f'{key}: {value}') for key, value in assist_dict.items()}
    return assist_dict

    # notes?
# assist_scraper() # TODO for debugging



# specials
def special_scraper(url):
    ''' Dict Keys:
            Name:
            Cooldown:
            Description:
            SP:
            Required:
            Exclusive:
            Can Use: (string?)
            Cannot Use: (list)
            List of Owners: (nested lists)
    '''
    # url = input('Enter special url - ') # for testing purposes
    html = urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, "html.parser")

    special_table = soup.find('table', class_="wikitable skills-table")
    special_table_rows = special_table.find_all('tr')


    special_dict = {}
    table_headers = []
    table_data = []
    # exclusive tells if skill can be inherited or not
    exclusive = 'No'
    # can_use states weapon/move types that skill limited to
    can_use = ''  # TODO None or ''?
    # cannot_use states weapon/move types that CANT use the skill
    cannot_use = ''  # TODO None or ''?

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
                if row_two_data.find_all('a'):
                    required_list = [required_links.text for required_links in row_two_data.find_all('a')]
                    table_data.append(', '.join(required_list))
                else:
                    table_data.append(row_two_data.text.strip())
                # print(table_data)

        # row 3 has weapon/move type and exclusive restrictions
        if i == 2:
            if row.find_all('a'):
                # cannot_use = row.find_all('a')[0]['title']
                cannot_use = [restriction['title'] for restriction in row.find_all('a')]

            else:
                can_use = row.find('td').text.strip()

                if can_use == 'This skill can only be equipped by its original unit.':
                    can_use = ''
                    exclusive = 'Yes'

                if can_use == 'This skill can only be equipped by staff users.':
                    can_use = 'Staff'

    for key, value in zip(table_headers, table_data):
        special_dict[key] = value

    # for key, value in zip(table_headers, table_data):
    #     special_dict[key] = value

    special_dict['Exclusive'] = exclusive
    special_dict['Can Use'] = can_use
    special_dict['Cannot Use'] = cannot_use

    # {print(f'{key}: {value}') for key, value in special_dict.items()}

    # list of owners
    # TODO handle no owners case (umbral)
    owner_list_marker = soup.find(id='List_of_owners')

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
            # create (skill, rarity) tuples
            # TODO identify which is skill in question and which are part of the skill chain
            if i != 0:
                temp_list = []
                # print([owner.text.strip() for owner in owner_list_row])
                owner_data = owner_list_row.find_all(text=True)
                temp_list.append(owner_data[0])

                acquisition_tuples = list(zip(owner_data[1:-1:2], owner_data[2::2]))
                for acquisition_tuple in acquisition_tuples:
                    temp_list.append(acquisition_tuple)

                skill_owners.append(temp_list)


    special_dict['List of Owners'] = skill_owners

    {print(f'{key}: {value}') for key, value in special_dict.items()}
    return special_dict

    # notes?
# special_scraper() # TODO for debugging

'''
# classify specials similar to table at bottom of page? 
https://feheroes.gamepedia.com/Galeforce
'''


from queue import Queue

# TODO passives
def passives_scraper(name):
    url = input('Enter passive url - ')
    # url = 'https://feheroes.gamepedia.com/Passives'
    html = urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, "html.parser")

    passive_table = soup.find(class_="wikitable default skills-table")
    # print(passive_table)

    passive_skill_dict = {}


    ## get following from Passives table
    # type
    # TODO icon
    # name
    # description
    # sp
    # required
    ## info found from individual skill links
    # skill chain?
    # get table headers
    passive_table_headers = passive_table.find_all('th')
    passive_table_headers_list = [header.text.strip() for header in passive_table_headers[1:-1]]
    # [print(header.text.strip()) for header in passive_table_headers]
    print(passive_table_headers_list)
    print()

    passive_skill_dict[passive_table_headers[0].text.strip()] = passive_table_headers[-1].text.strip()

    passive_table_rows = passive_table.find_all('tr')
    # print(passive_table_rows[1:-1])
    skill_data = []
    for row in passive_table_rows[1:-1]:
        skill_data.append([row_data.text.strip() for row_data in row.find_all('td')])
    # print(skill_data)

    for skill in skill_data:
        if skill[1] == name:
            for key, value in zip(passive_table_headers_list, skill):
                passive_skill_dict[key] = value
            print(skill)





    # getting headers from table
    # passive_table_headers = passive_table_rows[0].find_all('th')
    # passive_table_headers = passive_table.find_all('th')
    # [print(header.text.strip()) for header in passive_table_headers]
    # print()

    # get passive slot type (A, B, C)
    # passive_table_headers = passive_table_rows[1].find_all('th')
    # passive_table_headers = passive_table.find_all('th')
    # [print(header.text.strip()) for header in passive_table_headers]
    # print()

    passive_table_data = passive_table.find_all('td')
    passive_data_list = passive_table_data[1:-1]
    # print(passive_data_list)
    # get individual passive data
    # passive_data_list = passive_table.find_all('td')[1:-1]
    # TODO hybrid requirements need to be split
    passive_skills = [data.text.strip() for data in passive_data_list if data.text.strip() != '']
    # print(passive_skills)

    # TODO last row has any class restrictions of this group of passives
    # get passive class restrictions
    passive_restrictions = passive_table_data[-1]
    print()
    print(passive_restrictions.text)

    # TODO restrictions
    # TODO exclusive
        # TODO handle 'No restrictions.'
    # exclusive tells if skill can be inherited or not
    exclusive = 'No'
    # can_use states weapon/move types that skill limited to
    can_use = ''  # TODO None or ''?
    # cannot_use states weapon/move types that CANT use the skill
    cannot_use = ''  # TODO None or ''?


    if passive_restrictions.find_all('a'):
        # cannot_use = row.find_all('a')[0]['title']
        cannot_use = [restriction['title'] for restriction in passive_restrictions.find_all('a')]

    else:
        can_use = passive_restrictions.text.strip()

        if can_use == 'This skill can only be equipped by its original unit.':
            can_use = ''
            exclusive = 'Yes'

        if can_use == 'This skill can only be equipped by staff users.':
            can_use = 'Staff'

    passive_skill_dict['Exclusive'] = exclusive
    passive_skill_dict['Can Use'] = can_use
    passive_skill_dict['Cannot Use'] = cannot_use


    # list of owners
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

    for i, owner_list_row in enumerate(owner_list_table.find_all('tr')):
        # skip 1st row
        # create (skill, rarity) tuples
        # TODO identify which is skill in question and which are part of the skill chain
        if i != 0:
            temp_list = []
            # print([owner.text.strip() for owner in owner_list_row])
            owner_data = owner_list_row.find_all(text=True)
            temp_list.append(owner_data[0])

            acquisition_tuples = list(zip(owner_data[1:-1:2], owner_data[2::2]))
            for acquisition_tuple in acquisition_tuples:
                temp_list.append(acquisition_tuple)

            skill_owners.append(temp_list)

    print(skill_owners)
    passive_skill_dict['List of Owners'] = skill_owners


    print(passive_skill_dict)
    # notes?

    # TODO TEST
    ## TODO dance/sing skill?
    ## TODO regular skill
    ## TODO single skill in skill line
    ## skill that only has itself in skill line
    ## exclusive skill
    ## TODO skill with multiple restrictions
    ## TODO skill with one restriction
    ## TODO staff only skill
    '''TEST LINKS
    # regular skill/picking out single skill in skill line
    https://feheroes.gamepedia.com/Atk_Def_Form
    
    # exclusive skill/skill with only one skill in skill line
    https://feheroes.gamepedia.com/Ostian_Counter
    
    # single restrictions
    https://feheroes.gamepedia.com/Life_and_Death
    
    # multiple restrictions
    https://feheroes.gamepedia.com/Flashing_Blade
    
    # staff only
    https://feheroes.gamepedia.com/Live_to_Serve'''
passives_scraper("Atk/Def Form 1")
# passives_scraper("Ostian Counter")

