import pytest
import os, pathlib
import sqlite3
import ssl
from Skill_Data_Scraper import assist_scraper, special_scraper, passives_scraper

from bs4 import BeautifulSoup
from urllib.request import  urlopen



ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# connection = sqlite3.connect('../FEH_characters.db')
# cursor = connection.cursor()
#
# name = cursor.execute('SELECT name FROM Character WHERE id == 1').fetchone()
# print(name)



''' WEAPON TESTS
https://feheroes.gamepedia.com/File:Special_Damage_W.png
'''


class Test_Assists:
    ''' TESTS
    https://feheroes.gamepedia.com/Ardent_Sacrifice
    https://feheroes.gamepedia.com/Sacrifice
    https://feheroes.gamepedia.com/Dance
    https://feheroes.gamepedia.com/Martyr%2B

    # cant be used by staff, but has required skill link
    https://feheroes.gamepedia.com/Harsh_Command%2B
    '''


    def test_equipped_by_staff(self):
        ''' Healing assist skills like Martyr+ are labeled as usable by 'Staff' units '''
        url = 'https://feheroes.gamepedia.com/Martyr%2B'
        assist_dict = assist_scraper(url)
        assert (assist_dict['Restrictions'] == 'Staff only')


    def test_assist_is_exclusive(self):
        ''' Non-inheritable skills should be labeled as exclusive '''

        url = 'https://feheroes.gamepedia.com/Sacrifice'
        assist_dict = assist_scraper(url)
        # assert (assist_dict['Exclusive'] == 'Yes')
        assert (assist_dict['Restrictions'] == 'Exclusive')


    def test_assist_is_not_exclusive(self):
        ''' inheritable skills should not be exclusive '''

        url = 'https://feheroes.gamepedia.com/Harsh_Command%2B'
        assist_dict = assist_scraper(url)
        # assert (assist_dict['Exclusive'] == 'No')
        assert (assist_dict['Restrictions'] == 'Staff')


    def test_dance_or_sing(self):
        ''' TODO add value to identify all dance/sing/play assists? '''
        pass


    def test_non_staff_healing_assist(self):
        ''' staff units can only use healing assists used by a 'Staff' '''
        url = 'https://feheroes.gamepedia.com/Ardent_Sacrifice'
        assist_dict = assist_scraper(url)
        assert (assist_dict['Restrictions'] == 'Staff')



class Test_Specials:
    ''' SPECIAL SKILL - TEST CASES
    # Melee/Ranged defense
    https://feheroes.gamepedia.com/Aegis

    # Non-staff
    https://feheroes.gamepedia.com/Glacies

    # Exclusive and multiple req
    https://feheroes.gamepedia.com/Radiant_Aether

    # Staff-only
    https://feheroes.gamepedia.com/Earthfire_Balm%2B

    # hybrid req skill
    https://feheroes.gamepedia.com/Windfire_Balm
    https://feheroes.gamepedia.com/Earthwater_Balm

    # No Dragons or Ranged (Galeforce)
    https://feheroes.gamepedia.com/Galeforce

    # Ruptured Sky
    https://feheroes.gamepedia.com/Ruptured_Sky

    # No owners (umbral skills)
    https://feheroes.gamepedia.com/Umbra_Calamity
    '''


    def test_melee_only_special(self):
        ''' Some skills cannot be used by any of the ranged classes '''
        url = 'https://feheroes.gamepedia.com/Aegis'
        special_dict = special_scraper(url)
        assert (special_dict['Restrictions'] == ['Red bow', 'Red Dagger', 'Red Tome', 'Blue bow', 'Blue Dagger', 'Blue Tome', 'Green bow', 'Green Dagger', 'Green Tome', 'Colorless bow', 'Colorless Dagger', 'Colorless Tome', 'Staff'])


    def test_special_cannot_be_used_by_staff(self):
        ''' Most specials cannot be used by 'Staff' units'''
        url = 'https://feheroes.gamepedia.com/Glacies'
        special_dict = special_scraper(url)
        assert (special_dict['Restrictions'] == ['Staff'])


    def test_specials_with_multiple_usable_prerequisite_skills(self):
        ''' Specials with multiple possible prerequisite skills should be neatly
        separated by a comma, instead of being clumped together in a string'''
        url = 'https://feheroes.gamepedia.com/Radiant_Aether'
        special_dict = special_scraper(url)
        assert (special_dict['Required'] == 'Sol, Luna')


    def test_staff_only_specials(self):
        ''' Some specials can only be used by 'Staff' units '''
        url = 'https://feheroes.gamepedia.com/Earthfire_Balm%2B'
        special_dict = special_scraper(url)
        assert (special_dict['Restrictions'] == 'Staff only')


    def test_exclusive_specials(self):
        ''' Some specials cannot be inherited '''
        url = 'https://feheroes.gamepedia.com/Radiant_Aether'
        special_dict = special_scraper(url)
        # assert (special_dict['Exclusive'] == 'Yes')
        assert (special_dict['Restrictions'] == 'Exclusive')


    def test_galeforce_class_restrictions(self):
        ''' Galeforce cannot be used by Dragon or Ranged units'''
        url = 'https://feheroes.gamepedia.com/Galeforce'
        special_dict = special_scraper(url)
        assert (special_dict['Restrictions'] == ['Red bow', 'Red Dagger', 'Red Tome', 'Red Breath', 'Blue bow', 'Blue Dagger', 'Blue Tome', 'Blue Breath', 'Green bow', 'Green Dagger', 'Green Tome', 'Green Breath', 'Colorless bow', 'Colorless Dagger', 'Colorless Tome', 'Staff', 'Colorless Breath'])


    def test_ruptured_sky_class_restrictions(self):
        ''' Ruptured Sky cannot be used by Beasts or Dragons '''
        url = 'https://feheroes.gamepedia.com/Ruptured_Sky'
        special_dict = special_scraper(url)
        assert (special_dict['Restrictions'] == ['Red Breath', 'Red Beast', 'Blue Breath', 'Blue Beast', 'Green Breath', 'Green Beast', 'Staff', 'Colorless Breath', 'Colorless Beast'])


    def test_specials_with_no_distinct_owners(self):
        ''' Some specials, like the 'Umbral' set, are not owned by any distinct unit.
        Instead, Umbral skills are given to the Rokkr versions of any unit '''
        url = 'https://feheroes.gamepedia.com/Umbra_Calamity'
        special_dict = special_scraper(url)
        assert (special_dict['List of Owners'] is None)


class Test_Passives:
    ''' PASSIVES - TEST CASES
    # hybrid requirements
    https://feheroes.gamepedia.com/Chill_Spd_Def

    # staff only
    https://feheroes.gamepedia.com/Dazzling_Staff
    https://feheroes.gamepedia.com/Live_to_Serve

    # not usable by staff/single restriction
    https://feheroes.gamepedia.com/Life_and_Death

    # regular skill/picking out single skill in skill line
    https://feheroes.gamepedia.com/Atk_Def_Form

    # exclusive skill/skill with only one skill in skill line
    https://feheroes.gamepedia.com/Ostian_Counter

    # multiple restrictions
    https://feheroes.gamepedia.com/Flashing_Blade
    '''


    def test_hybrid_requirements(self):
        url = 'https://feheroes.gamepedia.com/Chill_Spd_Def'
        skill_name = 'Chill Spd/Def 1'
        passives_dict = passives_scraper(url, skill_name)
        assert (passives_dict['Required'] == 'Chill Spd 1, Chill Def 1')    # TODO change from string into list?


    def test_staff_only_passives(self):
        url = 'https://feheroes.gamepedia.com/Dazzling_Staff'
        skill_name = 'Dazzling Staff 2'
        passives_dict = passives_scraper(url, skill_name)
        assert (passives_dict['Restrictions'] == 'Staff only')


    def test_non_staff_passives(self):
        url = 'https://feheroes.gamepedia.com/Life_and_Death'
        skill_name = 'Life and Death 3'
        passives_dict = passives_scraper(url, skill_name)
        assert (passives_dict['Restrictions'] == ['Staff'])


    def test_passive_skill_line_with_multiple_passives(self):
        url = 'https://feheroes.gamepedia.com/Atk_Def_Form'
        skill_name = 'Atk/Def Form 2'
        passives_dict = passives_scraper(url, skill_name)
        # assert (passives_dict['Type'] == 'A')
        # assert (passives_dict['Name'] == 'Atk/Def Form 2')
        # assert (passives_dict['Description'] == 'Grants Atk/Def+X to unit during combat. (X = number of allies within 2 spaces + 2; max 5.)')
        # assert (passives_dict['SP'] == '120')
        # assert (passives_dict['Required'] == 'Atk/Def Form 1')
        # assert (passives_dict['Restrictions'] is None)
        assert (passives_dict['List of Owners'] == [['Eyvel: Mistress of Fiana', ('Atk/Def Form 1', '5'), ('Atk/Def Form 2', '5'), ('Atk/Def Form 3', '5')], ['Oboro: Fierce Bride-to-Be', ('Atk/Def Form 1', '5'), ('Atk/Def Form 2', '5'), ('Atk/Def Form 3', '5')]])

    def test_passive_skill_line_with_one_passive(self):
        url = 'https://feheroes.gamepedia.com/Ostian_Counter'
        skill_name = 'Ostian Counter'
        passives_dict = passives_scraper(url, skill_name)
        # assert (passives_dict['Restrictions'] == 'Exclusive')  # TODO are all single skill lines exclusive?
        # assert (passives_dict['Required'] == '—')
        assert (passives_dict['List of Owners'] == [['Hector: Brave Warrior', ('Ostian Counter', '5')]])


    def test_passive_with_multiple_restrictions(self):
        url = 'https://feheroes.gamepedia.com/Flashing_Blade'
        skill_name = 'Flashing Blade 3'
        passives_dict = passives_scraper(url, skill_name)
        assert (passives_dict['Restrictions'] == ['Cavalry', 'Flying', 'Staff'])



'''
adds 'tests' folder to file path?
>>> python -m pytest tests/

to run unit tests
>>> pytest -q test.py
'''