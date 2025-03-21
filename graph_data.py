from character import Character
from char_data import PEOPLE
from graph_creator import create_char_graph, create_multiple_spider_types

def show_spider_emotion():
    data = [(p.name,list(p.get_emotional_stats().values())) for p in PEOPLE]
    labels = list(PEOPLE[0].get_emotional_stats().keys())
    title = "Emotional Stats of Characters"
    color = 'b'
    create_char_graph(len(labels), data, labels, title, color)
 
def show_spider_physical():
    data = [(p.name,list(p.get_physical_stats().values())) for p in PEOPLE]
    labels = list(PEOPLE[0].get_physical_stats().keys())
    title = "Physical Stats of Characters"
    color = 'r'
    create_char_graph(len(labels), data, labels, title, color)
    
def show_spider_all():
    data = [(p.name, list(p.stats.values())) for p in PEOPLE]
    labels = list(PEOPLE[0].stats.keys())
    title = "All Stats of Characters"
    color = 'g'
    create_char_graph(len(labels), data, labels, title, color)
    
def show_spider_specific(peep_name: str):
    peep: Character = [p for p in PEOPLE if p.name == peep_name][0]
    emo = peep.get_emotional_stats()
    phy = peep.get_physical_stats()
    all = peep.stats
    data = [("Emotional", list(emo)), ("Physical", list(phy)), 
            ("All", list(all.values()))] # emotion data, physical data, and all data
    labels = [list(emo.keys()), list(phy.keys()), list(all.keys())] # emotion labels, physical labels, and all labels
    Ns = [len(emo), len(phy), len(all)]
    title = peep_name.upper()
    colors = ['b', 'r', 'g']
    # call new func that takes in a list of above and makes different graphs in one plot
    create_multiple_spider_types(N_lst=Ns, data_lst=data, labels_lst=labels, header=title, colors=colors)
    
#show_spider_emotion()
#show_spider_physical()
#show_spider_all()
show_spider_specific("Adan")