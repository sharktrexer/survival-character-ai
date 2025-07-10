import sqlite3
import os.path

from peep_data.char_data import SIMPLE_PEOPLE, STAT_NAMES

DB_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 
                       'all_combos.db')

def clear_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

# TODO: create cursor and pass it to the queries to prevent constant db connection and closure
def initialize_combos_db():
    create_db()
    create_max_table()
    create_ties_table()
    alter_table_to_add_tied_with_column()
    update_combos_with_tie_names()
    

def create_db():
    
    # prevent inserting copies of combo data
    if os.path.exists(DB_PATH):
        print("Database already exists. Please clear if you want the db to update.")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS combos (
                name TEXT,
                m_stat_name TEXT,
                m_apt INTEGER,
                l_stat_name TEXT,
                l_apt INTEGER,
                diff INTEGER
            )
        ''')

    for p in SIMPLE_PEOPLE:
        for m_stat in STAT_NAMES:
            for l_stat in STAT_NAMES:
                if m_stat == l_stat:
                    continue
                cursor.execute(('INSERT INTO combos' 
                                '(name, m_stat_name, m_apt, l_stat_name, l_apt, diff)' 
                                'VALUES (?, ?, ?, ?, ?, ?)'), 
                            (p.name, 
                                m_stat, p.stat_apts[m_stat], 
                                l_stat, p.stat_apts[l_stat], 
                                p.stat_apts[m_stat] - p.stat_apts[l_stat]))
                
    conn.commit()
    conn.close()

def create_max_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    #Max diff results including ties
    MAX_DIFFS_N_TIES = '''CREATE TABLE IF NOT EXISTS max_combos AS
                    SELECT name, m_stat_name, l_stat_name, diff
                    FROM combos
                    WHERE (m_stat_name, l_stat_name, diff) IN (
                        SELECT m_stat_name, l_stat_name, MAX(diff)
                        FROM combos
                        GROUP BY m_stat_name, l_stat_name
                        )
                    ORDER BY m_stat_name, l_stat_name
                   '''     

    cursor.execute(MAX_DIFFS_N_TIES)

    conn.commit()
    conn.close()
 
def alter_table_to_add_tied_with_column():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute(''' ALTER TABLE max_combos ADD COLUMN tied_with TEXT
                      ''')
    except sqlite3.OperationalError:
        print("Column already exists. Skipping...")
    
    conn.commit()
    conn.close()
  
def update_combos_with_tie_names():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''UPDATE max_combos
                    SET tied_with = (
                        SELECT GROUP_CONCAT(name, ', ')
                        FROM ties
                        WHERE ties.m_stat_name = max_combos.m_stat_name
                        AND ties.l_stat_name = max_combos.l_stat_name
                        AND ties.diff = max_combos.diff
                        AND ties.name <> max_combos.name
                        )
                    ''')

    conn.commit()
    conn.close()
  
  
def create_ties_table():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS ties AS
                   SELECT rowid, *
                    FROM max_combos
                    WHERE (m_stat_name, l_stat_name, diff) IN (
                        SELECT m_stat_name, l_stat_name, diff
                        FROM max_combos
                        GROUP BY m_stat_name, l_stat_name, diff
                        HAVING COUNT(*) > 1
                    )
                   ''')

    results = cursor.fetchall()
    conn.close()
    return [dict(row) for row in results]
         
''' END OF TABLE CREATION '''





def get_specific_combo_n_runner_ups(m_stat_name:str, l_stat_name:str):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(f'''SELECT * FROM combos 
                   WHERE m_stat_name = ? AND l_stat_name = ?
                   ORDER BY diff DESC''', (m_stat_name, l_stat_name))

    results = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in results]

def get_count_of_combos_per_peep():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('''SELECT name, COUNT(name) as count FROM max_combos GROUP BY name''')

    results = cursor.fetchall()

    conn.close()
    
    return [dict(row) for row in results] 


def get_combos_by(column_name: str, value_name:str):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute(f"SELECT rowid, * FROM max_combos WHERE {column_name} = ?", (value_name,))

    results = cur.fetchall()
    conn.close()
    
    return [dict(row) for row in results] 

 
def print_pretty_results(results:list, do_exclude_ids=True, do_print_count=True):
    '''
    Parameters:
        results (list): list of dicts representing rows of db to print pretty
        do_exclude_ids (bool): to print rowid
        do_print_count (bool): to print count of rows at end of print
    '''
    
    PAD = 15
    
    for k in results[0].keys():
        if k == "rowid" and do_exclude_ids:
            continue
        print(f"{k:<{PAD}}", end="")
    print()
        
    for d in results:
        for k, v in d.items():
            if k == "rowid" and do_exclude_ids:
                continue
            if v == None:
                v = ' '

            print(f"{v:<{PAD}}", end="")
        print()
       
    if do_print_count: 
        print("\n" + "Count: " + str(len(results)))


''' UNUSED but may serve a future purpose'''
def get_all_ties():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('''SELECT * FROM ties''')

    results = cursor.fetchall()
    conn.close()
    return [dict(row) for row in results] 

def get_combos_by_major_stat(m_stat_name:str):
    return get_combos_by("m_stat_name", m_stat_name)

def get_combos_by_lesser_stat(l_stat_name:str):
    return get_combos_by("l_stat_name", l_stat_name)
    
def get_combos_by_name(name:str):
    return get_combos_by("name", name)
''' END OF UNUSED '''    