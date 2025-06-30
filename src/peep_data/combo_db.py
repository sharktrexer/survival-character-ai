import sqlite3

from peep_data.char_data import SIMPLE_PEOPLE, STAT_NAMES

def create_db():
    conn = sqlite3.connect('all_combos.db')
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

def get_sorted_combos():
    conn = sqlite3.connect('all_combos.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT name, m_stat_name, l_stat_name, MAX(diff) as diff FROM combos 
                   GROUP BY m_stat_name, l_stat_name
                   ORDER BY m_stat_name, l_stat_name, diff DESC
                   ''')
    max_combos = cursor.fetchall()

    conn.close()

    return max_combos

'''SELECT name, m_stat_name, l_stat_name, MAX(diff) as diff FROM combos 
                   GROUP BY m_stat_name, l_stat_name
                   ORDER BY m_stat_name, l_stat_name, diff DESC
                   '''


def obtain_combos():
    # Every 10 entires represents one stat combo and its permutations
    # Winning stat combo are sorted to be at the beginning of the entry group
    combo_list = get_sorted_combos()
    