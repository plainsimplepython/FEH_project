import sqlite3
import Skill_Data_Scraper


def get_skills(skill_names_and_url_list, skill_type):
    # TODO insert skill data here or in Create_Database?
    # connection = sqlite3.connect('./test_skills.db')
    connection = sqlite3.connect('./FEH_characters')
    cursor = connection.cursor()
    search_list = []



    # create weapons table if it doesnt exist
    try:
        cursor.execute('''CREATE TABLE Weapons (id INTEGER PRIMARY KEY,
                                                name TEXT,
                                                weapon_type TEXT,
                                                might TEXT,
                                                range TEXT,
                                                effectiveness TEXT,
                                                required TEXT,
                                                restrictions TEXT,
                                                description TEXT,
                                                upgrades TEXT,
                                                evolution TEXT,
                                                owners TEXT) ''')
    except sqlite3.OperationalError:
        pass



    # create assists table if it doesnt exist
    try:
        cursor.execute('''CREATE TABLE Assists (id INTEGER PRIMARY KEY,
                                                name TEXT,
                                                range TEXT,
                                                description TEXT,
                                                required TEXT,
                                                restrictions TEXT,
                                                owners TEXT) ''')
    except sqlite3.OperationalError:
        pass



    # create specials table if it doesnt exist
    try:
        cursor.execute('''CREATE TABLE Specials (id INTEGER PRIMARY KEY,
                                                name TEXT,
                                                cooldown TEXT,
                                                description TEXT,
                                                required TEXT,
                                                restrictions TEXT,
                                                owners TEXT) ''')
    except sqlite3.OperationalError:
        pass



    # create 'A' passives table if it doesnt exist
    try:
        cursor.execute('''CREATE TABLE A_Passives (id INTEGER PRIMARY KEY,
                                                   type TEXT,
                                                   icon TEXT, 
                                                   name TEXT,
                                                   required TEXT,
                                                   description TEXT,
                                                   restrictions TEXT,
                                                   owners TEXT) ''')
    except sqlite3.OperationalError:
        pass



    # create 'B' passives table if it doesnt exist
    try:
        cursor.execute('''CREATE TABLE B_Passives (id INTEGER PRIMARY KEY,
                                                   type TEXT,
                                                   icon TEXT, 
                                                   name TEXT,
                                                   required TEXT,
                                                   description TEXT,
                                                   restrictions TEXT,
                                                   owners TEXT) ''')
    except sqlite3.OperationalError:
        pass



    # create 'C' passives table if it doesnt exist
    try:
        cursor.execute('''CREATE TABLE C_Passives (id INTEGER PRIMARY KEY,
                                                   type TEXT,
                                                   icon TEXT, 
                                                   name TEXT,
                                                   required TEXT,
                                                   description TEXT,
                                                   restrictions TEXT,
                                                   owners TEXT) ''')
    except sqlite3.OperationalError:
        pass



    for skill in skill_names_and_url_list:
        skill_name = skill[0]

        cursor.execute(f"SELECT EXISTS (SELECT * FROM {skill_type} WHERE name = ? )", (skill_name,))
        # cursor.execute("SELECT * FROM Weapons WHERE name = ? ", (skill_name,))

        # print(cursor.fetchone())
        result = cursor.fetchone()
        # if skill isn't already in database, add to search list
        if result[0] == 0:   # use list index, because fetchone returns a 1 tuple for some reason
            search_list.append(skill)
        else:
            print(f'\n{skill[0]} already present in database')

    # cursor.close()
    # connection.close()



    skill_data_list = []    # TODO use to pass skill data back to Hero_Crawler

    # get weapon data
    if skill_type == 'Weapons':
        for weapon in search_list:
            skill_data_list.append(Skill_Data_Scraper.weapon_scraper(weapon)) # TODO use to pass skill data back to Hero_Crawler

            # # gather weapon data
            # weapon_data = Skill_Data_Scraper.weapon_scraper(weapon)
            #
            # # Name
            # weapon_name = weapon_data.get('Name')
            #
            # # Weapon Type
            # weapon_type = weapon_data.get('Weapon type')
            #
            # # Might
            # weapon_might = weapon_data.get('Might')
            #
            # # Range
            # weapon_range = weapon_data.get('Range')
            #
            # # TODO Weapon Effectiveness
            # weapon_effectiveness = None
            # # if weapon_effectiveness:
            # #     pass
            #
            # # Description
            # if weapon_description := weapon_data.get('Description'):
            #     pass
            #
            # # Required
            # weapon_required = ', '.join(weapon_data.get('Required'))
            #
            # # Restrictions
            # weapon_restrictions = weapon_data.get('Restrictions')
            #
            # # Upgrades
            # # TODO split into upgrade_icon, upgrade_stats, upgrade_description?
            # # TODO or only store the unique effect upgrade?
            # # TODO or store as separate upgrade columns or in another table?
            # if weapon_upgrades := weapon_data.get('Upgrades'):
            #     # Flattening inner tuple into strings, but keeping them in a list so we can use the join() again to get a single string
            #     weapon_upgrades = ' || '.join([' :: '.join(upgrade) for upgrade in weapon_upgrades])
            #     # weapon_upgrades = ', '.join(weapon_upgrades)
            #
            # # Evolution
            # if weapon_evolution := weapon_data.get('Evolution'):
            #     pass
            #
            # # Owners
            # # Flattening inner tuple into strings, but keeping them in a list so we can use the join() again to get a single string
            # weapon_owners = ', '.join([' - '.join(owner_tuple) for owner_tuple in weapon_data.get('List of Owners')])
            #
            #
            #
            # # add weapon information to database
            # cursor.execute('''INSERT INTO Weapons (name,
            #                                        weapon_type,
            #                                        might,
            #                                        range,
            #                                        effectiveness,
            #                                        required,
            #                                        restrictions,
            #                                        description,
            #                                        upgrades,
            #                                        evolution,
            #                                        owners)
            # VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            #                                       (weapon_name,
            #                                        weapon_type,
            #                                        weapon_might,
            #                                        weapon_range,
            #                                        weapon_effectiveness,
            #                                        weapon_required,
            #                                        weapon_restrictions,
            #                                        weapon_description,
            #                                        weapon_upgrades,
            #                                        weapon_evolution,
            #                                        weapon_owners))



    # get assist data
    elif skill_type == 'Assists':
        for assist in search_list:
            skill_data_list.append(Skill_Data_Scraper.assist_scraper(assist)) # TODO use to pass skill data back to Hero_Crawler

            # assist_data = Skill_Data_Scraper.assist_scraper(assist)
            #
            # # Name
            # assist_name = assist_data.get('Name')
            #
            # # Range
            # assist_range = assist_data.get('Range')
            #
            # # Description
            # assist_description = assist_data.get('Description')
            #
            # # Required
            # assist_required = assist_data.get('Required')
            #
            # # Restrictions
            # assist_restrictions = assist_data.get('Restrictions')
            #
            # # Owners
            # # Flattening inner tuple into strings, but keeping them in a list so we can use the join() again to get a single string
            # assist_owners = ', '.join([' - '.join(owner_tuple) for owner_tuple in assist_data.get('List of Owners')])
            #
            #
            #
            # cursor.execute('''INSERT INTO Assists (name,
            #                                        range,
            #                                        description,
            #                                        required,
            #                                        restrictions,
            #                                        owners)
            #                     VALUES (?, ?, ?, ?, ?, ?)''',
            #                                        (assist_name,
            #                                         assist_range,
            #                                         assist_description,
            #                                         assist_required,
            #                                         assist_restrictions,
            #                                         assist_owners))



    # get special data
    elif skill_type == 'Specials':
        for special in search_list:
            skill_data_list.append(Skill_Data_Scraper.special_scraper(special)) # TODO use to pass skill data back to Hero_Crawler

            # special_data = Skill_Data_Scraper.special_scraper(special)
            #
            # # Name
            # special_name = special_data.get('Name')
            #
            # # Cooldown
            # special_cooldown = special_data.get('Cooldown')
            #
            # # Description
            # special_description = special_data.get('Description')
            #
            # # Required
            # special_required = special_data.get('Required')
            #
            # # Restrictions
            # special_restrictions = special_data.get('Restrictions')
            #
            # # Owners
            # # Flattening inner tuple into strings, but keeping them in a list so we can use the join() again to get a single string
            # special_owners = ', '.join([' - '.join(owner_tuple) for owner_tuple in special_data.get('List of Owners')])
            #
            #
            #
            # cursor.execute('''INSERT INTO Specials (name,
            #                                         cooldown,
            #                                         description,
            #                                         required,
            #                                         restrictions,
            #                                         owners)
            #                         VALUES (?, ?, ?, ?, ?, ?)''',
            #                                        (special_name,
            #                                         special_cooldown,
            #                                         special_description,
            #                                         special_required,
            #                                         special_restrictions,
            #                                         special_owners))



    # get A passive data
    elif skill_type == 'A_Passives':
        for passive in search_list:
            skill_data_list.append(Skill_Data_Scraper.passives_scraper(passive)) # TODO use to pass skill data back to Hero_Crawler

            # # gather 'A' Passive data
            # a_passive_data = Skill_Data_Scraper.passives_scraper(passive)
            #
            # # Type
            # a_passive_type = a_passive_data.get('Type')
            #
            # # Icon
            # a_passive_icon = a_passive_data.get('Icon')
            #
            # # Name
            # a_passive_name = a_passive_data.get('Name')
            #
            # # Required
            # a_passive_required = a_passive_data.get('Required')
            #
            # # Description
            # a_passive_description = a_passive_data.get('Description')
            #
            # # Restrictions
            # a_passive_restrictions = a_passive_data.get('Restrictions')
            #
            # # Owners
            # # Flattening inner tuple into strings, but keeping them in a list so we can use the join() again to get a single string
            # a_passive_owners = ', '.join([' - '.join(owner_tuple) for owner_tuple in a_passive_data.get('List of Owners')])
            #
            #
            #
            # cursor.execute('''INSERT INTO A_Passives (type,
            #                                           icon,
            #                                           name,
            #                                           required,
            #                                           description,
            #                                           restrictions,
            #                                           owners)
            #                         VALUES (?, ?, ?, ?, ?, ?, ?)''',
            #                                          (a_passive_type,
            #                                           a_passive_icon,
            #                                           a_passive_name,
            #                                           a_passive_required,
            #                                           a_passive_description,
            #                                           a_passive_restrictions,
            #                                           a_passive_owners))




    # get B passive data
    elif skill_type == 'B_Passives':
        for passive in search_list:
            skill_data_list.append(Skill_Data_Scraper.passives_scraper(passive)) # TODO use to pass skill data back to Hero_Crawler

            # # gather 'B' Passive data
            # b_passive_data = Skill_Data_Scraper.passives_scraper(passive)
            #
            # # Type
            # b_passive_type = b_passive_data.get('Type')
            #
            # # Icon
            # b_passive_icon = b_passive_data.get('Icon')
            #
            # # Name
            # b_passive_name = b_passive_data.get('Name')
            #
            # # Required
            # b_passive_required = b_passive_data.get('Required')
            #
            # # Description
            # b_passive_description = b_passive_data.get('Description')
            #
            # # Restrictions
            # b_passive_restrictions = b_passive_data.get('Restrictions')
            #
            # # Owners
            # # Flattening inner tuple into strings, but keeping them in a list so we can use the join() again to get a single string
            # b_passive_owners = ', '.join([' - '.join(owner_tuple) for owner_tuple in b_passive_data.get('List of Owners')])
            #
            #
            #
            # cursor.execute('''INSERT INTO B_Passives (type,
            #                                           icon,
            #                                           name,
            #                                           required,
            #                                           description,
            #                                           restrictions,
            #                                           owners)
            #                         VALUES (?, ?, ?, ?, ?, ?, ?)''',
            #                                          (b_passive_type,
            #                                           b_passive_icon,
            #                                           b_passive_name,
            #                                           b_passive_required,
            #                                           b_passive_description,
            #                                           b_passive_restrictions,
            #                                           b_passive_owners))




    # get C passive data
    elif skill_type == 'C_Passives':
        for passive in search_list:
            skill_data_list.append(Skill_Data_Scraper.passives_scraper(passive)) # TODO use to pass skill data back to Hero_Crawler

            # # gather 'C' Passive data
            # c_passive_data = Skill_Data_Scraper.passives_scraper(passive)
            #
            # # Type
            # c_passive_type = c_passive_data.get('Type')
            #
            # # Icon
            # c_passive_icon = c_passive_data.get('Icon')
            #
            # # Name
            # c_passive_name = c_passive_data.get('Name')
            #
            # # Required
            # c_passive_required = c_passive_data.get('Required')
            #
            # # Description
            # c_passive_description = c_passive_data.get('Description')
            #
            # # Restrictions
            # c_passive_restrictions = c_passive_data.get('Restrictions')
            #
            # # Owners
            # # Flattening inner tuple into strings, but keeping them in a list so we can use the join() again to get a single string
            # c_passive_owners = ', '.join([' - '.join(owner_tuple) for owner_tuple in c_passive_data.get('List of Owners')])
            #
            #
            #
            # cursor.execute('''INSERT INTO C_Passives (type,
            #                                           icon,
            #                                           name,
            #                                           required,
            #                                           description,
            #                                           restrictions,
            #                                           owners)
            #                                     VALUES (?, ?, ?, ?, ?, ?, ?)''',
            #                                          (c_passive_type,
            #                                           c_passive_icon,
            #                                           c_passive_name,
            #                                           c_passive_required,
            #                                           c_passive_description,
            #                                           c_passive_restrictions,
            #                                           c_passive_owners))




    # connection.commit()
    cursor.close()
    connection.close()


    # [print(skill_data) for skill_data in skill_data_list]
    return skill_data_list  # TODO use to pass skill data back to Hero_Crawler

# skill_tuple = [('Holy Vestments', '/Holy_Vestments'), ('Aegis', '/Aegis')]
# get_skills(skill_tuple, 'Specials')
''' TESTS
['Iron Sword', 'Steel Sword', 'Killing Edge', 'Killing Edge+', 'Nameless Blade']
Weapons
[('Iron Sword', '/Iron_Sword'), ('Steel Sword', '/Steel_Sword'), ('Killing Edge', '/Killing_Edge'), ('Killing Edge+', '/Killing_Edge%2B'), ('Nameless Blade', '/Nameless_Blade')]
Assists
[('Ardent Sacrifice','/Ardent_Sacrifice'), ('Sacrifice', '/Sacrifice')]

Specials
[('Radiant Aether', '/Radiant_Aether')]
[('Holy Vestments', /Holy_Vestments), ('Aegis', '/Aegis')]

'''