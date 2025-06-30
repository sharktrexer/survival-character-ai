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

ALL_MAX_N_TIE_COMBOS = []

def clear_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

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

    conn.close()
           


def obtain_combos():
    # Comprises of all max diff combos, inluding ties
    # Thus per stat permutation, if the next entry is the same, it is a tie
    pass
    