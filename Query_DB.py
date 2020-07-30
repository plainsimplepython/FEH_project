import sqlite3

import Skill_Data_Scraper


def get_skills(skill_names_and_url_list):
    # TODO update Weapons table
    connection = sqlite3.connect('./test_skills.db')
    # connection = sqlite3.connect('./FEH_characters')
    cursor = connection.cursor()
    search_list = []

    for skill in skill_names_and_url_list:
        skill_name = skill[0]

        cursor.execute("SELECT EXISTS (SELECT * FROM Weapons WHERE name = ? )", (skill_name,))
        # cursor.execute("SELECT * FROM Weapons WHERE name = ? ", (skill_name,))

        # print(cursor.fetchone())
        result = cursor.fetchone()
        # if skill isn't already in database, add to search list
        if result[0] == 0:   # use list index, because fetchone returns a 1 tuple for some reason
            search_list.append(skill)

    # print(search_list)

    ## gets multiple searches
    # result = cursor.fetchall()
    # print('Total rows are:', len(result))
    # for i in result:
    #     print(i)

    # TODO return search_list
    cursor.close()
    connection.close()

    skill_data_list= []
    for weapon in search_list:
        skill_data_list.append(Skill_Data_Scraper.weapon_scraper(weapon))

    # [print(skill_data) for skill_data in skill_data_list]
    return skill_data_list


# get_skills([('Iron Sword', '/Iron_Sword'), ('Steel Sword', '/Steel_Sword'), ('Killing Edge', '/Killing_Edge'), ('Killing Edge+', '/Killing_Edge%2B'), ('Nameless Blade', '/Nameless_Blade')])
''' TESTS
['Iron Sword', 'Steel Sword', 'Killing Edge', 'Killing Edge+', 'Nameless Blade']
[('Iron Sword', '/Iron_Sword'), ('Steel Sword', '/Steel_Sword'), ('Killing Edge', '/Killing_Edge'), ('Killing Edge+', '/Killing_Edge%2B'), ('Nameless Blade', '/Nameless_Blade')]
'''