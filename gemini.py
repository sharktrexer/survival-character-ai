import os
import google.generativeai as genai
import typing_extensions as typing

from dotenv import load_dotenv

from preset_characters import STAT_NAMES

load_dotenv()

KEY = os.environ['API_KEY']

STAT_DESCRIPTIONS = {
    "Strength": "How good you are at feats of strength, like attacking or working out.",
    "Defense": "How much physical damage you are resistant to.",
    "Evasion": "How good you are at avoiding attacks or escaping bad situations.",
    "Dexterity": "How good you are at using items, like weapons or tools.",
    "Recovery": "How well you heal others and resist negative effects.",
    "Intellect": "How perceptive you are.",
    "Creativity": "How skillful you are at coming up with new ideas and making stuff.",
    "Fear": "How afriad you are of dealing with danger.",
    "Intimidation": "How strong your prescence is.",
    "Charisma": "How social you are and how much social power you have",
    "Stress": "How easily overwhelmed you get. Lower is worse",
    "Health": "How much of a beating you can take.",
    "Hunger": "How much food you have to consume to live.",
    "Energy": "How many activities you can do before needing to rest.",
}

stringified_stat_desc = ", ".join("=".join(_) for _ in STAT_DESCRIPTIONS.items())

class Question(typing.TypedDict):
    question: str
    associated_stat: str

genai.configure(api_key=KEY)
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content(
    ("Generate yes/no questions relating to each of these characteristics and their descriptions: "
     + stringified_stat_desc
     + "\n The questions should be short and focused, able to be answered with yes or no, "
     "and ask the user about their personality and lifestyle preferences. "
     "Answering yes to the question means they attribute themself to that characteristic, "
     "Generate 2 questions per characteristic. Don't repeat questions."
     ),
    generation_config=genai.GenerationConfig(
        response_mime_type="application/json", response_schema=list[Question]
    ))
print(response.text)