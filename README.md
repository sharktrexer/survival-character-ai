# Survival Character AI

An in progress LLM-AI-wrapper and game that assists in creating your survival character to fight and survive in a terminal. LLM will require your own Gemini API key, but won't be required to play.

1. Answer generated questions to determine your character stats, from Strength to Creativity to Energy.
2. Work with other simulated characters to survive in the terminal by growing, harvesting, and cooking food; building barricades, and fending off attacks.
3. Fight creatures with your team using turn based combat while leveraging your statistical advantages.

This project will comprise of multiple modular systems, from printing simple data, to full on survival simulation.

# Current Systems
This is a growing list of what simulations are currently finished.

## Spider Charts
For each of the characters and their stats, spider/radar charts can be generated to visualize stat distribution using Matplotlib. Below is an example that show every character and their 14 stat distribution.
![all_char_spiders](https://github.com/user-attachments/assets/a80f4162-a15d-40db-98ef-525e756a1d02)

You can also view the character's stats organized into different collections, such as below where only "emotional" stats are visualized.
![emo_char_spiders](https://github.com/user-attachments/assets/eb5f19e7-8069-4e39-b937-ff42921fa454)

And finally, something I am proud of, is that you can see each of the differently organized stats visualized for one character, with different spider charts displayed on the same figure.
![chris_spider](https://github.com/user-attachments/assets/21b37626-c748-49ab-a47d-227048452a9d)


## Who are you?
You can choose one stat you desire to be strong and one you care less about. This will determine which character you play as, prioritizing a character with the highest desired stat and the biggest difference between highest and lowest stat. For devleopers you can inspect which characters have a higher chance of being picked than others based on the 2 questions.
