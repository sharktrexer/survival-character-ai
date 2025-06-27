from peep_data.character import Character
from peep_data.char_data import SIMPLE_PEOPLE
from visualization.graph_creator import create_char_graph, create_multiple_char_spider_types

''' Shows every character's spidar chart of emotional stats '''
def show_spider_emotion():
    data = [(p.name,list(p.get_emotional_stats().values())) for p in SIMPLE_PEOPLE]
    labels = list(SIMPLE_PEOPLE[0].get_emotional_stats().keys())
    title = "Emotional Stats of Characters"
    color = 'b'
    create_char_graph(len(labels), data, labels, title, color)
 
''' Shows every character's spidar chart of physical stats '''
def show_spider_physical():
    data = [(p.name,list(p.get_physical_stats().values())) for p in SIMPLE_PEOPLE]
    labels = list(SIMPLE_PEOPLE[0].get_physical_stats().keys())
    title = "Physical Stats of Characters"
    color = 'r'
    create_char_graph(len(labels), data, labels, title, color)
    
''' Shows every character's spidar chart of all stats '''
def show_spider_all():
    data = [(p.name, list(p.stat_aps.values())) for p in SIMPLE_PEOPLE]
    labels = list(SIMPLE_PEOPLE[0].stat_aps.keys())
    title = "All Stats of Characters"
    color = 'g'
    create_char_graph(len(labels), data, labels, title, color)

''' Shows a specific character's stats of the 3 types of spider chart (Emotional, Physical, All) '''   
def show_spider_specific(peep_name: str):
    
    # specified peep
    peep: Character = [p for p in SIMPLE_PEOPLE if p.name == peep_name][0]
    
    # dicts
    emo = peep.get_emotional_stats()
    phy = peep.get_physical_stats()
    all = peep.stat_apts
    
    # values of stats
    data = [("Emotional", list(emo.values())), ("Physical", list(phy.values())), 
            ("All", list(all.values()))] 
    # names of stats
    labels = [list(emo.keys()), list(phy.keys()), list(all.keys())] 
    # number of stats
    Ns = [len(emo), len(phy), len(all)]
    
    # graph display
    title = peep_name.upper()
    colors = ['b', 'r', 'g']
    
    # create graph func
    create_multiple_char_spider_types(N_lst=Ns, data_lst=data, labels_lst=labels, header=title, colors=colors)
    
#show_spider_emotion()
#show_spider_physical()
#show_spider_all()
#show_spider_specific("Adan")