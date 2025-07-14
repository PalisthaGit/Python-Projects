from dotenv import load_dotenv
import os
import openai
import re

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Maps emotions to their core need
emotion_to_need = {
    "amazed": ["exploration", "discovery"],
    "amused": ["play", "fun"],
    "compassionate": ["giving", "connecting"],
    "confident": ["challenge", "achievement"],
    "connected": ["socializing", "belonging"],
    "content": ["relaxation", "ease"],
    "curious": ["learning", "exploring"],
    "elated": ["celebration", "joy"],
    "encouraged": ["progress", "support"],
    "energetic": ["movement", "physical-activity"],
    "engaged": ["creativity", "hands-on"],
    "excited": ["adventure", "novelty"],
    "grateful": ["expressing-thanks", "appreciation"],
    "happy": ["enjoyment", "socializing"],
    "hopeful": ["planning", "vision"],
    "inspired": ["creating", "expressing"],
    "interested": ["exploring", "learning"],
    "joyful": ["play", "celebration"],
    "loving": ["connecting", "caring"],
    "optimistic": ["visioning", "future-planning"],
    "peaceful": ["relaxation", "quiet"],
    "relieved": ["comfort", "release"],
    "satisfied": ["completion", "achievement"],
    "thankful": ["expressing-thanks", "sharing"],
    "trusting": ["bonding", "openness"],
    "warm": ["closeness", "connecting"],

    # Negative emotions
    "angry": ["respect", "consideration"],
    "annoyed": ["consideration", "ease"],
    "anxious": ["safety", "reassurance"],
    "ashamed": ["acceptance", "understanding"],
    "bored": ["stimulation", "engagement"],
    "confused": ["clarity", "understanding"],
    "depressed": ["support", "hope"],
    "despair": ["hope", "meaning"],
    "disappointed": ["expectation", "understanding"],
    "discouraged": ["support", "acknowledgment"],
    "disgusted": ["integrity", "consideration"],
    "distant": ["connection", "belonging"],
    "distressed": ["comfort", "reassurance"],
    "embarrassed": ["acceptance", "empathy"],
    "fearful": ["safety", "reassurance"],
    "frustrated": ["effectiveness", "autonomy"],
    "guilty": ["forgiveness", "understanding"],
    "helpless": ["support", "empowerment"],
    "hopeless": ["hope", "support"],
    "hurt": ["empathy", "healing"],
    "impatient": ["ease", "consideration"],
    "irritated": ["consideration", "ease"],
    "jealous": ["belonging", "acceptance"],
    "lonely": ["connection", "belonging"],
    "overwhelmed": ["ease", "support"],
    "pain": ["comfort", "healing"],
    "regretful": ["forgiveness", "understanding"],
    "sad": ["comfort", "support"],
    "scared": ["safety", "reassurance"],
    "shocked": ["safety", "understanding"],
    "tired": ["rest", "ease"],
    "uncomfortable": ["comfort", "ease"],
    "unhappy": ["comfort", "hope"],
    "vulnerable": ["safety", "acceptance"],
    "worried": ["reassurance", "safety"],
}

deep_negative_emotions = [
    "angry", "anxious", "ashamed", "confused", "depressed", "despair", "disappointed",
    "discouraged", "disgusted", "distant", "distressed", "embarrassed", "fearful",
    "frustrated", "guilty", "helpless", "hopeless", "hurt", "jealous", "lonely",
    "overwhelmed", "pain", "regretful", "sad", "scared", "shocked", "uncomfortable",
    "unhappy", "vulnerable", "worried"
]

light_negative_emotions = [
    "bored", "tired", "impatient", "annoyed", "irritated"
]

positive_emotions = [
    "amazed", "amused", "compassionate", "confident", "connected", "content",
    "curious", "elated", "encouraged", "energetic", "engaged", "excited",
    "grateful", "happy", "hopeful", "inspired", "interested", "joyful",
    "loving", "optimistic", "peaceful", "relieved", "satisfied", "thankful",
    "trusting", "warm"
]

DEEP_NEGATIVE_MESSAGE = (
    "Hey, it’s totally okay to feel {emotion}.\n"
    "Your feelings are real and valid, even when they’re tough.\n"
    "You’re not alone, I promise.\n"
    "Be gentle with yourself and take a slow breath.\n"
    "However you’re feeling right now is just fine.\n"
    "You can sit with it as long as you need. You’ve got this."
)

LIGHT_NEGATIVE_MESSAGE = (
    "Hey, feeling {emotion} is totally normal.\n"
    "Everyone hits a lull sometimes.\n"
    "Let’s try to mix things up a bit."
)

POSITIVE_MESSAGE = (
    "Hey, that’s so awesome. I’m really happy for you.\n\n"
    "Let that good energy soak in. Let it carry you through the day.\n\n"
    "You deserve every bit of this, so enjoy it fully."
)

MAX_RETRIES = 5

def get_friendly_activity_suggestion(user_emotion, main_need, previous_suggestions=None):
    # Prepare exclusion list for prompt
    exclude_str = ""
    if previous_suggestions:
        # Show up to the last 3 suggestions for exclusion
        exclusions = "\n".join(f"- {s}" for s in previous_suggestions[-3:])
        exclude_str = (
            "\nDon't suggest the same activity as any of the following. "
            "Here are the last few suggestions to avoid repeating:\n"
            f"{exclusions}\n"
        )
    prompt = (
        f"Suggest one specific, practical activity for someone in a city who feels {user_emotion} "
        f"and whose main emotional need is {main_need}."
        " Make sure this activity is clearly different from previous suggestions."
        " The activity must directly support their need for {main_need}."
        " If the need is safety or reassurance, always suggest things that create comfort and a sense of being protected—like making a cozy space, calling a trusted person, or doing something calming. Never suggest self-defense classes, safety drills, risky activities, or anything stressful or challenging."
        " Never suggest anything dangerous, overwhelming, or requiring leaving the house late at night. Always make safety the top priority."
        " The activity should be doable right now at home or nearby. If you mention a walk, keep it realistic—like a stroll to a nearby park in daylight or sitting on a bench in the sun. Never suggest movies, TV, or anything requiring shopping."
        " Write your answer in short, friendly chunks, not long paragraphs."
        " After the main idea, say: 'If you’re feeling social, invite or message a friend to join you. If you want alone time, enjoy it solo—that’s totally fine.'"
        f"{exclude_str}"
    )
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=220,
        temperature=0.85,
    )
    return response.choices[0].message.content.strip()

def get_unique_activity_suggestion(user_emotion, main_need, previous_suggestions):
    # Try up to MAX_RETRIES to get a unique suggestion
    for _ in range(MAX_RETRIES):
        suggestion = get_friendly_activity_suggestion(user_emotion, main_need, previous_suggestions)
        if suggestion not in previous_suggestions:
            return suggestion
    # If can't find a unique one, just return the last
    return suggestion

print(
    "Hi, I’m here for you.\n"
    "Tell me how you’re feeling right now—anything goes. I’ll help you pick something you can actually do that fits your mood, whether you want comfort, company, or just a little spark.\n"
    "\nDescribe how you're feeling in one word (happy, lonely, sad, anxious, bored—whatever fits.)"
)

# Emotion input loop for retries
while True:
    user_emotion = input("> ").strip().lower()
    if user_emotion in emotion_to_need:
        break
    print("\nSorry, I don't have a suggestion for that feeling yet. Try one of these:\n")
    print(", ".join(sorted(emotion_to_need.keys())))
    print("\nHow are you feeling? (Just type one word from above)")

main_need = emotion_to_need[user_emotion][0]

if user_emotion in deep_negative_emotions:
    print("\n" + DEEP_NEGATIVE_MESSAGE.format(emotion=user_emotion) + "\n")
elif user_emotion in light_negative_emotions:
    print("\n" + LIGHT_NEGATIVE_MESSAGE.format(emotion=user_emotion) + "\n")
elif user_emotion in positive_emotions:
    print("\n" + POSITIVE_MESSAGE + "\n")
else:
    print("\nHey, however you’re feeling, that’s valid. Let’s find something that fits.\n")

while True:
    print("How about I suggest an activity for you?")
    print("Would you like that?")
    print("Type 1 for yes, 2 for no.\n")
    answer = input("> ").strip()
    if answer == "1" or answer == "2":
        break
    print("Sorry, please type 1 for yes or 2 for no.")

if answer != "1":
    print("No worries at all.\nI’m here if you want ideas later.\nTake care of yourself.")
else:
    previous_suggestions = []
    while True:
        suggestion = get_unique_activity_suggestion(user_emotion, main_need, previous_suggestions)
        print("\n" + suggestion)
        previous_suggestions.append(suggestion)
        user_choice = input(
            "\nNot your thing? Type '1' for a new suggestion, or anything else to quit: "
        ).strip().lower()
        if user_choice != "1":
            print("Hope that helps.\nYou can always run me again if you want more ideas.")
            break