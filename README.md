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
You can choose one stat you desire to be strong and one you care the least about. This will determine which character you would be given to play as, prioritizing a character with the biggest difference between highest and lowest stat. 

<img width="415" height="672" alt="image" src="https://github.com/user-attachments/assets/91f98091-9392-40d6-9509-0fa2ef1de67f" />

After you get your character, you can see their stat details, who else you obtained based on tied differences, and who you have obtained before.

<img width="320" height="438" alt="image" src="https://github.com/user-attachments/assets/b4be4480-4144-4ad9-a586-72c39632a8ba" />

And finally, you can keep track of which stat combos got you who using the history option.

<img width="255" height="64" alt="image" src="https://github.com/user-attachments/assets/992649e0-708c-4628-8134-870e1976de1b" />

Now you know what character you want to play based on your stat preferences!
