from character import Character

class sub_stats:
    def initiative(peep: Character):
        return peep.stats["Dexterity"] + peep.stats["Evasion"]

    def leadership(peep: Character):
        return peep.stats["Charisma"] + peep.stats["Intimidation"] + peep.stats["Fear"]

    def acrobatics(peep: Character):
        return peep.stats["Dexterity"] + peep.stats["Strength"]

    def perception(peep: Character):
        return peep.stats["Intellect"] + peep.stats["Evasion"]

    def skirmish(peep: Character):
        return peep.stats["Strength"] + peep.stats["Defense"] + peep.stats["Intimidation"]
    