a="""Afar
Afrikaans Translator
Albanian Translator
American Sign Language Translator
Amharic
Arabic Translator
Armenian Translator
Assamese
Basque Translator
Bengali Translator
Bosnian Translator
Breton Translator
Bulgarian Translator
Burmese Translator
Canadian French Translator
Castilian Spanish Translator
Catalan Translator
Croatian Translator
Czech Translator
Danish Translator
Dari Translator
Dinka Translator
Dutch Translator
English (UK) Translator
English (US) Translator
English Grammar
English Spelling
Estonian Translator
Filipino Translator
Finnish Translator
French Translator
Game Translation
Georgian Translator
German Translator
Greek Translator
Gujrati Translator
Hebrew Translator
Hindi Translator
Hungarian Translator
Icelandic Translator
Indonesian Translator
Interpreter
Irish Translator
Italian Translator
Japanese Translator
Kannada Translator
Karelian Translator
Kazakh Translator
Korean Translator
Kurdish Translator
Latin Translator
Latvian Translator
Linguistics
Lithuanian Translator
Macedonian Translator
Malay Translator
Malayalam Translator
Maltese Translator
Marathi Translator
Montenegrin Translator
Nepali Translator
Norwegian Translator
Oromo
Pashto Translator
Poet
Polish Translator
Portuguese (Brazil) Translator
Portuguese Translator
Punjabi Translator
Romanian Translator
Russian Translator
Sami Translator
Serbian Translator
Serbo-Croatian Translator
Simplified Chinese Translator
Sinhalese Translator
Slovakian Translator
Slovenian Translator
Somali
Spanish Translator
Subtitles & Captions
Swahili Translator
Swedish Translator
Tajik Translator
Tamil Translator
Technical Translation
Telugu Translator
Thai Translator
Tigrinya
Traditional Chinese (Hong Kong)
Traditional Chinese (Taiwan)
Turkish Translator
Ukrainian Translator
Urdu Translator
Vietnamese Translator
Welsh Translator
Yiddish Translator
Yoruba Translator""".lower().split("\n")
import pandas as pd
df=pd.DataFrame(a).to_csv("translation.csv",header=False,index=False)