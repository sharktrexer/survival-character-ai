import os
import json
import google.generativeai as genai
import typing_extensions as typing

from dotenv import load_dotenv

from peep.char_data import STAT_NAMES

load_dotenv()

KEY = os.environ['API_KEY']

NUMBER_Q_PER_STAT = 2

STAT_DESCRIPTIONS = {
    "Strength": "How good you are at feats of strength, like attacking or working out.",
    "Defense": ("How much general resistance you have to direct damage/attacks"
                " Example questions: Do you feel a sense of inner strength and stability?"
                "Would you describe yourself as resilient and able to withstand significant challenges?"),
    "Evasion": "How elusive you are and how well you can dodge strikes.",
    "Dexterity": "How good and accuract you are at using items and ranged actions like throwing or shooting.",
    "Recovery": "How well you heal others and resist negative effects.",
    "Intellect": "How perceptive and well-informed you are.",
    "Creativity": "How skillful you are at coming up with new ideas and crafting stuff.",
    "Fear": "How afraid you are of dealing with danger or disadvantageous odds.",
    "Intimidation": "How strong your prescence is or how little you care about other's opinions.",
    "Charisma": "How social and pursuasive you are.",
    "Stress": "How easily overwhelmed you get. Lower is worse",
    "Health": "How many small, lower damage hits you can take before getting knocked down, and your regenitive effect",
    "Hunger": "How much food you have to consume to survive. Healthiness of the food is irrelevant.",
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
     + stringified_stat_desc +
     "\nThe questions should only be answered with yes or no, 1-2 sentences long, don't include the name of the characteristic, "
     "and ask the user about their personality and lifestyle preferences. "
     "Answering yes to the question should mean they attribute themself to that characteristic. "
     f"Generate {NUMBER_Q_PER_STAT} questions per characteristic. Don't repeat questions."
     ),
    generation_config=genai.GenerationConfig(
        response_mime_type="application/json", response_schema=list[Question]
    ))

# Parse json reponse string into dictionary
data = json.loads(response.text)

# Format dictionary into pretty string
json_resp = json.dumps(data, indent=4)

print(json_resp)