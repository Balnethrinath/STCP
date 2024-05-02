# Importing necessary modules required
from playsound import playsound
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os
from langdetect import detect
from langdetect import DetectorFactory

# Set the maximum reliability for language detection
DetectorFactory.seed = 0

# A dictionary containing language names as keys and their corresponding language codes as values
languages = {
    'afrikaans': 'af', 'albanian': 'sq', 'amharic': 'am', 'arabic': 'ar', 'armenian': 'hy', 'azerbaijani': 'az',
    'basque': 'eu', 'belarusian': 'be', 'bengali': 'bn', 'bosnian': 'bs', 'bulgarian': 'bg', 'catalan': 'ca',
    'cebuano': 'ceb', 'chichewa': 'ny', 'chinese (simplified)': 'zh-cn', 'chinese (traditional)': 'zh-tw',
    'corsican': 'co', 'croatian': 'hr', 'czech': 'cs', 'danish': 'da', 'dutch': 'nl', 'english': 'en',
    'esperanto': 'eo', 'estonian': 'et', 'filipino': 'tl', 'finnish': 'fi', 'french': 'fr', 'frisian': 'fy',
    'galician': 'gl', 'georgian': 'ka', 'german': 'de', 'greek': 'el', 'gujarati': 'gu', 'haitian creole': 'ht',
    'hausa': 'ha', 'hawaiian': 'haw', 'hebrew': 'he', 'hindi': 'hi', 'hmong': 'hmn', 'hungarian': 'hu',
    'icelandic': 'is', 'igbo': 'ig', 'indonesian': 'id', 'irish': 'ga', 'italian': 'it', 'japanese': 'ja',
    'javanese': 'jv', 'kannada': 'kn', 'kazakh': 'kk', 'khmer': 'km', 'korean': 'ko', 'kurdish (kurmanji)': 'ku',
    'kyrgyz': 'ky', 'lao': 'lo', 'latin': 'la', 'latvian': 'lv', 'lithuanian': 'lt', 'luxembourgish': 'lb',
    'macedonian': 'mk', 'malagasy': 'mg', 'malay': 'ms', 'malayalam': 'ml', 'maltese': 'mt', 'maori': 'mi',
    'marathi': 'mr', 'mongolian': 'mn', 'myanmar (burmese)': 'my', 'nepali': 'ne', 'norwegian': 'no',
    'odia': 'or', 'pashto': 'ps', 'persian': 'fa', 'polish': 'pl', 'portuguese': 'pt', 'punjabi': 'pa',
    'romanian': 'ro', 'russian': 'ru', 'samoan': 'sm', 'scots gaelic': 'gd', 'serbian': 'sr', 'sesotho': 'st',
    'shona': 'sn', 'sindhi': 'sd', 'sinhala': 'si', 'slovak': 'sk', 'slovenian': 'sl', 'somali': 'so',
    'spanish': 'es', 'sundanese': 'su', 'swahili': 'sw', 'swedish': 'sv', 'tajik': 'tg', 'tamil': 'ta',
    'telugu': 'te', 'thai': 'th', 'turkish': 'tr', 'ukrainian': 'uk', 'urdu': 'ur', 'uyghur': 'ug', 'uzbek': 'uz',
    'vietnamese': 'vi', 'welsh': 'cy', 'xhosa': 'xh', 'yiddish': 'yi', 'yoruba': 'yo', 'zulu': 'zu'
}


# Capture Voice
# takes command through microphone
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        detected_lang = detect(query)
        detected_lang_name = [k for k, v in languages.items() if v == detected_lang][0]
        print(f"The User said: {query}\nDetected Language: {detected_lang_name}")
    except Exception as e:
        print("Say that again please...")
        return "None", None
    return query, detected_lang


# Input from user
# Make input lowercase
query, detected_language = takecommand()
while query == "None":
    query, detected_language = takecommand()


def destination_language():
    print("Enter the language in which you want to convert: Ex. Hindi, English, etc.")
    print()

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        lang_input = r.recognize_google(audio, language='en-in')
        to_lang = languages.get(lang_input.lower())
        print(f"Destination Language: {lang_input}")
    except Exception as e:
        print("Say that again please...")
        return None

    while to_lang is None:
        print("Invalid language. Please enter a valid language.")
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source)

        try:
            print("Recognizing...")
            lang_input = r.recognize_google(audio, language='en-in')
            to_lang = languages.get(lang_input.lower())
            print(f"Destination Language: {lang_input}")
        except Exception as e:
            print("Say that again please...")
            return None
    
    return to_lang


to_lang = destination_language()

# invoking Translator
translator = Translator()

# Translating from src to dest
text_to_translate = translator.translate(query, dest=to_lang)

text1 = text_to_translate.text

# Using Google-Text-to-Speech ie, gTTS() method
# to speak the translated text into the
# destination language which is stored in to_lang.
# Also, we have given 3rd argument as False because
# by default it speaks very slowly
speak = gTTS(text=text1, lang=to_lang, slow=False)

# Using save() method to save the translated
# speech in capture_voice.mp3
speak.save("captured_voice.mp3")

# Using OS module to run the translated voice.
playsound('captured_voice.mp3')
os.remove('captured_voice.mp3')

# Printing Output
print(text1)
