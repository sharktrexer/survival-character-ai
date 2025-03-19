from character import Character
from char_data import PEOPLE
from graph_creator import create_char_graph

def show_spider_graph_emotion():
    data = [(p.name,list(p.get_emotional_stats().values())) for p in PEOPLE]
    labels = list(PEOPLE[0].get_emotional_stats().keys())
    title = "Emotional Stats of Characters"
    color = 'b'
    create_char_graph(len(labels), data, labels, title, color)
    
show_spider_graph_emotion()