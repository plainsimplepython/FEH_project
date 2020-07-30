import sqlite3


# TODO remove drop table clauses
# TODO add fail safe for skills don't have descriptions
# TODO find cleaner way to insert data
def create_database(data):
    '''
    Takes a character data dict and enters all character info into a database entry
    '''

    connection = sqlite3.connect('./FEH_characters.db')
    cursor = connection.cursor()

    # cursor.execute('DROP TABLE IF EXISTS Character')
    try:
        cursor.execute('''CREATE TABLE Character (id INTEGER PRIMARY KEY,
                                                  name TEXT,
                                                  title TEXT,
                                                  image_id INT UNIQUE,
                                                  description TEXT,
                                                  rarity TEXT,
                                                  acquisition TEXT,
                                                  blessing_type TEXT,
                                                  blessing_boost TEXT,
                                                  duo_skill TEXT,
                                                  duel TEXT,
                                                  pair_up TEXT,
                                                  weapon_type TEXT,
                                                  move_type TEXT,
                                                  hp TEXT,
                                                  atk TEXT,
                                                  spd TEXT,
                                                  def TEXT,
                                                  res TEXT,
                                                  total TEXT,
                                                  weapons TEXT,
                                                  assists TEXT,
                                                  specials TEXT,
                                                  passives TEXT,
                                                  FOREIGN KEY (image_id) REFERENCES Character_Images (image_id))''')
    except sqlite3.OperationalError:
        pass


    # cursor.execute('DROP TABLE IF EXISTS Character_Images')
    try:    # TODO compress image table into CSV string?
        cursor.execute('''CREATE TABLE Character_Images (image_id INTEGER PRIMARY KEY,
                                                      portrait TEXT,
                                                      attack TEXT, 
                                                      special TEXT,
                                                      injured TEXT)''')
    except sqlite3.OperationalError:
        pass



    # Name and Title
    name = data.get('Name')[0]
    title = data.get('Name')[1]

    # Images
    portrait = data.get('Images')[2]    # getting the largest size of each image type
    attack = data.get('Images')[5]      # 3 size per images type:
    special = data.get('Images')[8]     # portrait, attack, special, injured
    injured = data.get('Images')[11]

    # Description
    description = data.get('Description')

    # Rarity and Acquisition
    rarity = data.get('Rarities')
    acquisition = data.get('Acquisition')

    # Blessing data
    blessing_type = None
    if data.get('Effect'):
        blessing_type = data.get('Effect')

    blessing_boost = None
    if data.get('Ally Boost'):
        blessing_boost = data.get('Ally Boost')

    # Duo Skill
    duo_skill = None
    if data.get('Duo Skill'):
        duo_skill = data.get('Duo Skill')

    # Duel bonus
    duel = None
    if data.get('Standard Effect 1: Duel'):
        duel = data.get('Standard Effect 1: Duel')     # TODO change key to just 'Duel'?

    # Pair-Up
    pair_up = None
    if data.get('Standard Effect 2: Pair Up'):
        pair_up = data.get('Standard Effect 2: Pair Up')  # TODO change key to just 'Pair Up'?

    # Weapon and Movement classifications
    weapon_type = data.get('Weapon Type')
    move_type = data.get('Move Type')

    # Stats
    stats = data.get('Stats')
    char_hp = stats.get('HP')
    char_atk = stats.get('Atk')
    char_spd = stats.get('Spd')
    char_def = stats.get('Def')
    char_res = stats.get('Res')
    char_total = stats.get('Total')

    # Skills
    weapons = data.get('Weapons')
    assists = data.get('Assists')
    specials = data.get('Specials')
    passives = data.get('Passives')



    # add character images
    cursor.execute('''INSERT INTO Character_Images (portrait,
                                                    attack, 
                                                    special,
                                                    injured)
                                       VALUES (?, ?, ?, ?)''',
                                                   (portrait,
                                                    attack,
                                                    special,
                                                    injured))


    ## retrieve PK of last entry
    image_id = cursor.lastrowid


    # add character information to database
    cursor.execute('''INSERT INTO Character (name, 
                                             title,
                                             image_id,
                                             description, 
                                             rarity, 
                                             acquisition, 
                                             blessing_type,
                                             blessing_boost,
                                             duo_skill,
                                             duel,
                                             pair_up, 
                                             weapon_type, 
                                             move_type,
                                             hp, 
                                             atk, 
                                             spd, 
                                             def, 
                                             res, 
                                             total, 
                                             weapons,
                                             assists,
                                             specials,
                                             passives)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                                            (name,
                                             title,
                                             image_id,
                                             description,
                                             rarity,
                                             acquisition,
                                             blessing_type,
                                             blessing_boost,
                                             duo_skill,
                                             duel,
                                             pair_up,
                                             weapon_type,
                                             move_type,
                                             char_hp,
                                             char_atk,
                                             char_spd,
                                             char_def,
                                             char_res,
                                             char_total,
                                             weapons,
                                             assists,
                                             specials,
                                             passives))

    connection.commit()
    cursor.close()
    connection.close()


# def update_skill():
#     connection = sqlite3.connect('./FEH_characters2.db')
#     cursor = connection.cursor()
#
#     cursor.execute('''SELECT * FROM Character''')
#     result = cursor.fetchall()
#     print('Total rows are:', len(result))
#     for i in result:
#         print(i)
#
# update_skill()