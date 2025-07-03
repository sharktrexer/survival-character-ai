import sqlite3
import os.path

from peep_data.char_data import SIMPLE_PEOPLE, STAT_NAMES

DB_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 
                       'all_combos.db')

# Queries to Remember
#ONLY MAX diff results from sorted list
MAX_DIFFS = '''SELECT name, m_stat_name, l_stat_name, MAX(diff) as diff FROM combos 
            GROUP BY m_stat_name, l_stat_name
            ORDER BY m_stat_name, l_stat_name, diff DESC
            '''
# All results sorted desc order by diff
SORTED_BY_DIFF = '''SELECT name, m_stat_name, l_stat_name, diff FROM combos 
                ORDER BY m_stat_name, l_stat_name, diff DESC
                '''

def clear_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

def initialize_combos_db():
    create_db()
    create_max_table()
    create_ties_table()
    alter_table_to_add_tied_with_column()
    update_combos_with_tie_names()
    

def create_db():
    
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
         
def get_all_ties():
    '''
    Gets all rows that have tied max differences in their combos
    Names are in one string separated by commas
    
    Returns:
        list: a list of tuples of the form (diff, m_stat_name, l_stat_name, tied_names)
    '''
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('''SELECT m_stat_name, l_stat_name, GROUP_CONCAT(name) AS tied_names, GROUP_CONCAT(rowid) AS tied_ids
                FROM (
                SELECT rowid, m_stat_name, l_stat_name, diff, name,
                    COUNT(*) OVER (PARTITION BY m_stat_name, l_stat_name, diff) AS count
                    FROM max_combos
                ) AS subquery
                WHERE count > 1
                GROUP BY m_stat_name, l_stat_name, diff
                   ''')

    results = cursor.fetchall()
    conn.close()
    return [dict(row) for row in results] 


def get_count_of_combos_per_char():
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

def get_combos_by_major_stat(m_stat_name:str):
    return get_combos_by("m_stat_name", m_stat_name)

def get_combos_by_lesser_stat(l_stat_name:str):
    return get_combos_by("l_stat_name", l_stat_name)
    
def get_combos_by_name(name:str):
    return get_combos_by("name", name)
        
def print_pretty_results(results:list, do_exclude_ids=True):
    '''
    Parameters:
        results (list): list of dicts representing rows of db to print pretty
    '''
    if do_exclude_ids:
        for r in results:
            del r["rowid"]
    
    for k in results[0].keys():
        print(f"{k:<15}", end="")
    print()
        
    for d in results:
        for v in d.values():
            if not v:
                print(f"{'':<15}", end="")
                continue
            
            print(f"{v:<15}", end="")
        print()
    