import pytest
import os, pathlib
import sqlite3
import ssl
from Skill_Data_Scraper import weapon_scraper, assist_scraper, special_scraper, passives_scraper

from bs4 import BeautifulSoup
from urllib.request import  urlopen



ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# connection = sqlite3.connect('../FEH_characters.db')
# cursor = connection.cursor()
#
# name = cursor.execute('SELECT name FROM Character WHERE id == 1').fetchone()
# print(name)


class Test_Weapons:
    ''' WEAPON TESTS
    https://feheroes.gamepedia.com/List_of_evolving_weapons
    https://feheroes.gamepedia.com/List_of_upgradable_weapons
    # get basic weapon stats
        # Weapon Type
        # Might
        # Range
        # Effectiveness - wait until images are links?
        # required
        # Exclusive
        # Description
        # list of owners


    # are there multiple requirement weapons
    https://feheroes.gamepedia.com/Armorsmasher%2B

    # TODO no requirements
    ('Iron_Lance',"/Iron_Lance")

    #  evolved weapons - upgrades, no owners
    https://feheroes.gamepedia.com/Armorsmasher%2B

    # TODO evolved only weapons?

    # weapons that can be evolved
    https://feheroes.gamepedia.com/Armorslayer%2B
    https://feheroes.gamepedia.com/Naga_(tome)

    # weapons with overlapping names
    https://feheroes.gamepedia.com/Naga_(tome)
    https://feheroes.gamepedia.com/Falchion_(Awakening)
    https://feheroes.gamepedia.com/Falchion_(Gaiden)
    https://feheroes.gamepedia.com/Falchion_(Mystery)
    https://feheroes.gamepedia.com/Laevatein_(weapon)
    https://feheroes.gamepedia.com/Missiletainn_(tome)
    https://feheroes.gamepedia.com/Missiletainn_(sword)

    # standard name
    https://feheroes.gamepedia.com/Naga_(tome)
    https://feheroes.gamepedia.com/Alondite

    # exclusive
    https://feheroes.gamepedia.com/Naga_(tome)
    # inheritable
    https://feheroes.gamepedia.com/Slaying_Edge%2B
    '''

    def test_weapon_name(self):
        ''' weapon scraper should retrieve weapon name even if link is for overlapping weapon names '''

        skill_name_and_url = ('Naga', '/Naga_(tome)')
        weapon_dict = weapon_scraper(skill_name_and_url)
        assert (weapon_dict['Name'] == 'Naga')


    def test_weapon_might(self):
        ''' weapon scraper should retrieve weapon might '''

        skill_name_and_url = ('Naga', '/Naga_(tome)')
        weapon_dict = weapon_scraper(skill_name_and_url)
        assert (weapon_dict['Might'] == '14')


    def test_weapon_range(self):
        ''' weapon scraper should retrieve weapon range '''

        skill_name_and_url = ('Naga', '/Naga_(tome)')
        weapon_dict = weapon_scraper(skill_name_and_url)
        assert (weapon_dict['Range'] == '2')


    def test_single_weapon_requirement(self):
        ''' even if there's only one requirement, it should be returned as a list
        of one element '''

        skill_name_and_url = ('Naga', '/Naga_(tome)')
        weapon_dict = weapon_scraper(skill_name_and_url)
        assert (weapon_dict['Required'] == ['Rexcalibur'])


    def test_no_weapon_requirement(self):
        ''' TODO '''
        pass
        # skill_name_and_url = ('Naga', '/Naga_(tome)')
        # weapon_dict = weapon_scraper(skill_name_and_url)
        # assert (weapon_dict['Required'] == ['Rexcalibur'])


    def test_multiple_weapon_requirements(self):
        ''' some weapons have multiple requirements '''

        skill_name_and_url = ('Armorsmasher+', '/Armorsmasher+')
        weapon_dict = weapon_scraper(skill_name_and_url)
        assert (weapon_dict['Required'] == ['Armorsmasher', 'Armorslayer+'])


    def test_weapon_is_exclusive(self):
        ''' weapons that cannot be inherited should be labeled as exclusive

        weapon scraper should retrieve weapon exclusivity as 'Restrictions',
        so we can easily grab all exclusive or non-exclusive skills from our Unit Planner
        '''

        skill_name_and_url = ('Naga', '/Naga_(tome)')
        weapon_dict = weapon_scraper(skill_name_and_url)
        assert (weapon_dict['Restrictions'] == 'Exclusive')


    def test_weapon_is_not_exclusive(self):
        ''' inheritable weapons should be labeled as 'None' under restrictions

        weapon scraper should retrieve weapon exclusivity as 'Restrictions',
        so we can easily grab all exclusive or non-exclusive skills from our Unit Planner
        '''

        skill_name_and_url = ('Armorslayer+', '/Armorslayer%2B')
        weapon_dict = weapon_scraper(skill_name_and_url)
        assert (weapon_dict['Restrictions'] is None)


    def test_weapon_description(self):
        ''' weapon scraper should retrieve weapon description '''

        skill_name_and_url = ('Naga', '/Naga_(tome)')
        weapon_dict = weapon_scraper(skill_name_and_url)
        assert (weapon_dict['Description'] == 'Effective against dragon foes. If foe initiates combat, grants Def/Res+2 during combat.')


    def test_weapon_evolutions(self):
        ''' weapon scraper should retrieve weapon evolution if it exists '''

        skill_name_and_url = ('Naga', '/Naga_(tome)')
        weapon_dict = weapon_scraper(skill_name_and_url)
        assert (weapon_dict['Evolution'] == 'Divine Naga')


    def test_weapon_upgrades(self):
        ''' weapon scraper should retrieve weapon upgrades if it exists '''

        skill_name_and_url = ('Naga', '/Naga_(tome)')
        weapon_dict = weapon_scraper(skill_name_and_url)
        assert (weapon_dict['Upgrades'] == [['https://gamepedia.cursecdn.com/feheroes_gamepedia_en/thumb/8/83/Naga_tome_W.png/24px-Naga_tome_W.png?version=781176fd1d1f5d7ae3b7d1c7a4fdebf6', '—', 'Effective against dragon foes. If foe initiates combat, grants Def/Res+4 during combat.In combat against a dragon foe, disables foe\'s skills that "calculate damage using the lower of foe\'s Def or Res" and unit can counterattack regardless of foe\'s range.'],
                                            ['https://gamepedia.cursecdn.com/feheroes_gamepedia_en/thumb/2/20/Attack_Plus_W.png/24px-Attack_Plus_W.png?version=03eb92be2c1c09baf211f36e03e917d8', '+2 HP, +1 Mt', 'Effective against dragon foes. If foe initiates combat, grants Def/Res+4 during combat.'],
                                            ['https://gamepedia.cursecdn.com/feheroes_gamepedia_en/thumb/0/02/Speed_Plus_W.png/24px-Speed_Plus_W.png?version=0660f5eb80f8f28a4cbd84a1ea3869ac', '+2 HP, +2 Spd', 'Effective against dragon foes. If foe initiates combat, grants Def/Res+4 during combat.'],
                                            ['https://gamepedia.cursecdn.com/feheroes_gamepedia_en/thumb/c/cd/Defense_Plus_W.png/24px-Defense_Plus_W.png?version=792ea3dd75399cb3579b94d8a30bd823', '+2 HP, +3 Def', 'Effective against dragon foes. If foe initiates combat, grants Def/Res+4 during combat.'],
                                            ['https://gamepedia.cursecdn.com/feheroes_gamepedia_en/thumb/5/50/Resistance_Plus_W.png/24px-Resistance_Plus_W.png?version=892af87aa5d6e4ba6cbcb1921bbcd310', '+2 HP, +3 Res', 'Effective against dragon foes. If foe initiates combat, grants Def/Res+4 during combat.']])


    def test_list_of_owners(self):
        ''' weapon scraper should retrieve weapon owners and at what rarity skill is learned
        as a tuple (name, rarity) '''

        skill_name_and_url = ('Naga', '/Naga_(tome)')
        weapon_dict = weapon_scraper(skill_name_and_url)
        assert (weapon_dict['List of Owners'] == [("Julia: Naga's Blood", '5')])


    def test_weapon_has_no_owners(self):
        ''' some weapons dont come with owners (evolved only, umbral) '''

        skill_name_and_url = ('Armorsmasher%2B', "/Armorsmasher%2B")
        weapon_dict = weapon_scraper(skill_name_and_url)
        assert (weapon_dict['List of Owners'] == [])



class Test_Assists:
    ''' TESTS
    https://feheroes.gamepedia.com/Ardent_Sacrifice
    https://feheroes.gamepedia.com/Sacrifice
    https://feheroes.gamepedia.com/Dance
    https://feheroes.gamepedia.com/Martyr%2B

    # TODO no assists
    https://feheroes.gamepedia.com/Marth:_Enigmatic_Blade

    # TODO no requirements -> ['-']
    https://feheroes.gamepedia.com/Rally_Attack

    # TODO single requirement should be an one element list
    https://feheroes.gamepedia.com/Rally_Up_Atk

    # TODO handle multiple requirements
    https://feheroes.gamepedia.com/Rally_Atk_Res

    # cant be used by staff, but has required skill link
    https://feheroes.gamepedia.com/Harsh_Command%2B
    '''

    def test_assist_with_multiple_requirements(self):
        ''' TODO ('Rally Atk/Res', '/Rally_Atk_Res') '''
        pass


    def test_equipped_by_staff(self):
        ''' Healing assist skills like Martyr+ are labeled as usable by 'Staff' units '''
        skill_name_and_url = ('Martyr%2B', '/Martyr%2B')
        assist_dict = assist_scraper(skill_name_and_url)
        assert (assist_dict['Restrictions'] == 'Staff only')


    def test_assist_is_exclusive(self):
        ''' Non-inheritable skills should be labeled as exclusive '''

        skill_name_and_url = ('Sacrifice', '/Sacrifice')
        assist_dict = assist_scraper(skill_name_and_url)
        # assert (assist_dict['Exclusive'] == 'Yes')
        assert (assist_dict['Restrictions'] == 'Exclusive')


    def test_assist_is_not_exclusive(self):
        ''' inheritable skills should not be exclusive '''

        skill_name_and_url = ('Harsh_Command%2B', '/Harsh_Command%2B')
        assist_dict = assist_scraper(skill_name_and_url)
        # assert (assist_dict['Exclusive'] == 'No')
        assert (assist_dict['Restrictions'] == 'Staff')


    def test_dance_or_sing(self):
        ''' TODO add value to identify all dance/sing/play assists? '''
        pass


    def test_non_staff_healing_assist(self):
        ''' staff units can only use healing assists used by a 'Staff' '''
        skill_name_and_url = ('/Ardent_Sacrifice', '/Ardent_Sacrifice')
        assist_dict = assist_scraper(skill_name_and_url)
        assert (assist_dict['Restrictions'] == 'Staff')



class Test_Specials:
    ''' SPECIAL SKILL - TEST CASES
    # TODO no specials
    https://feheroes.gamepedia.com/Marth:_Enigmatic_Blade

    # Melee/Ranged defense
    https://feheroes.gamepedia.com/Aegis

    # Non-staff
    https://feheroes.gamepedia.com/Glacies

    # Exclusive and multiple req
    https://feheroes.gamepedia.com/Radiant_Aether

    # TODO no requirements
    https://feheroes.gamepedia.com/Holy_Vestments

    # TODO single requirement should be an one element list
    https://feheroes.gamepedia.com/Aegis

    # Staff-only
    https://feheroes.gamepedia.com/Earthfire_Balm%2B

    # hybrid req skill
    https://feheroes.gamepedia.com/Windfire_Balm
    https://feheroes.gamepedia.com/Earthwater_Balm

    # No Dragons or Ranged (Galeforce)
    https://feheroes.gamepedia.com/Galeforce

    # Ruptured Sky
    https://feheroes.gamepedia.com/Ruptured_Sky

    # TODO exclude No owners (umbral skills)
    https://feheroes.gamepedia.com/Umbra_Calamity
    '''


    def test_melee_only_special(self):
        ''' Some skills cannot be used by any of the ranged classes '''
        skill_name_and_url = ('Aegis', '/Aegis')
        special_dict = special_scraper(skill_name_and_url)
        assert (special_dict['Restrictions'] == ['Red bow', 'Red Dagger', 'Red Tome', 'Blue bow', 'Blue Dagger', 'Blue Tome', 'Green bow', 'Green Dagger', 'Green Tome', 'Colorless bow', 'Colorless Dagger', 'Colorless Tome', 'Staff'])


    def test_special_cannot_be_used_by_staff(self):
        ''' Most specials cannot be used by 'Staff' units'''
        skill_name_and_url = ('Glacies', '/Glacies')
        special_dict = special_scraper(skill_name_and_url)
        assert (special_dict['Restrictions'] == ['Staff'])


    def test_specials_with_multiple_usable_prerequisite_skills(self):
        ''' Specials with multiple possible prerequisite skills should be neatly
        separated by a comma, instead of being clumped together in a string '''
        skill_name_and_url = ('Radiant_Aether', '/Radiant_Aether')
        special_dict = special_scraper(skill_name_and_url)
        assert (special_dict['Required'] == 'Sol, Luna')


    def test_staff_only_specials(self):
        ''' Some specials can only be used by 'Staff' units '''
        skill_name_and_url = ('Earthfire_Balm%2B', '/Earthfire_Balm%2B')
        special_dict = special_scraper(skill_name_and_url)
        assert (special_dict['Restrictions'] == 'Staff only')


    def test_exclusive_specials(self):
        ''' Some specials cannot be inherited '''
        skill_name_and_url = ('Radiant_Aether', '/Radiant_Aether')
        special_dict = special_scraper(skill_name_and_url)
        # assert (special_dict['Exclusive'] == 'Yes')
        assert (special_dict['Restrictions'] == 'Exclusive')


    def test_galeforce_class_restrictions(self):
        ''' Galeforce cannot be used by Dragon or Ranged units'''
        skill_name_and_url = ('Galeforce', '/Galeforce')
        special_dict = special_scraper(skill_name_and_url)
        assert (special_dict['Restrictions'] == ['Red bow', 'Red Dagger', 'Red Tome', 'Red Breath', 'Blue bow', 'Blue Dagger', 'Blue Tome', 'Blue Breath', 'Green bow', 'Green Dagger', 'Green Tome', 'Green Breath', 'Colorless bow', 'Colorless Dagger', 'Colorless Tome', 'Staff', 'Colorless Breath'])


    def test_ruptured_sky_class_restrictions(self):
        ''' Ruptured Sky cannot be used by Beasts or Dragons '''
        skill_name_and_url = ('Ruptured_Sky', '/Ruptured_Sky')
        special_dict = special_scraper(skill_name_and_url)
        assert (special_dict['Restrictions'] == ['Red Breath', 'Red Beast', 'Blue Breath', 'Blue Beast', 'Green Breath', 'Green Beast', 'Staff', 'Colorless Breath', 'Colorless Beast'])


    def test_specials_with_no_distinct_owners(self):
        ''' Some specials, like the 'Umbral' set, are not owned by any distinct unit.
        Instead, Umbral skills are given to the Rokkr versions of any unit '''
        skill_name_and_url = ('/Umbra_Calamity', '/Umbra_Calamity')
        special_dict = special_scraper(skill_name_and_url)
        assert (special_dict['List of Owners'] is None)


class Test_Passives:
    ''' PASSIVES - TEST CASES
    # TODO no passives case
    https://feheroes.gamepedia.com/Marth:_Enigmatic_Blade

    # hybrid requirements
    https://feheroes.gamepedia.com/Chill_Spd_Def

    # TODO no requirements -> ['-']

    # TODO single requirement should be an one element list

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
        skill_name_and_url = ('Chill Spd/Def 1', '/Chill_Spd_Def')
        # skill_name = 'Chill Spd/Def 1'
        passives_dict = passives_scraper(skill_name_and_url)
        assert (passives_dict['Required'] == 'Chill Spd 1, Chill Def 1')    # TODO change from string into list?


    def test_staff_only_passives(self):
        skill_name_and_url = ('Dazzling Staff 2', '/Dazzling_Staff')
        skill_name = 'Dazzling Staff 2'
        passives_dict = passives_scraper(skill_name_and_url)
        assert (passives_dict['Restrictions'] == 'Staff only')


    def test_non_staff_passives(self):
        skill_name_and_url = ('Life and Death 3', '/Life_and_Death')
        # skill_name = 'Life and Death 3'
        passives_dict = passives_scraper(skill_name_and_url)
        assert (passives_dict['Restrictions'] == ['Staff'])


    def test_passive_skill_line_with_multiple_passives(self):
        skill_name_and_url = ('Atk/Def Form 2', '/Atk_Def_Form')
        # skill_name = 'Atk/Def Form 2'
        passives_dict = passives_scraper(skill_name_and_url)
        # assert (passives_dict['Type'] == 'A')
        # assert (passives_dict['Name'] == 'Atk/Def Form 2')
        # assert (passives_dict['Description'] == 'Grants Atk/Def+X to unit during combat. (X = number of allies within 2 spaces + 2; max 5.)')
        # assert (passives_dict['SP'] == '120')
        # assert (passives_dict['Required'] == 'Atk/Def Form 1')
        # assert (passives_dict['Restrictions'] is None)
        assert (passives_dict['List of Owners'] == [('Eyvel: Mistress of Fiana', '5'), ('Oboro: Fierce Bride-to-Be', '5')])

    def test_passive_skill_line_with_one_passive(self):
        skill_name_and_url = ('Ostian Counter', '/Ostian_Counter')
        # skill_name = 'Ostian Counter'
        passives_dict = passives_scraper(skill_name_and_url)
        # assert (passives_dict['Restrictions'] == 'Exclusive')  # TODO are all single skill lines exclusive?
        # assert (passives_dict['Required'] == '—')
        assert (passives_dict['List of Owners'] == [('Hector: Brave Warrior', '5')])


    def test_passive_with_multiple_restrictions(self):
        skill_name_and_url = ('Flashing Blade 3', '/Flashing_Blade')
        # skill_name = 'Flashing Blade 3'
        passives_dict = passives_scraper(skill_name_and_url)
        assert (passives_dict['Restrictions'] == ['Cavalry', 'Flying', 'Staff'])



    # TODO TEST
    ## TODO dance/sing skill?
    ## TODO regular skill
    ## TODO single skill in skill line
    ## skill that only has itself in skill line
    ## exclusive skill
    ## TODO skill with multiple restrictions
    ## TODO skill with one restriction
    ## TODO staff only skill
    # noinspection PyUnreachableCode
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


'''
adds 'tests' folder to file path?
>>> python -m pytest tests/

to run unit tests
>>> pytest -q test.py
'''