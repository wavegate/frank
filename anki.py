from anki_export import ApkgReader
import pyexcel_xlsxwx
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import csv
import re
from difflib import SequenceMatcher

with ApkgReader('franka.apkg') as apkg:
    pyexcel_xlsxwx.save_data('test.xlsx', apkg.export(), config={'format': None})

df = pd.read_excel("test.xlsx", sheet_name='Basic')

df['edited'] = df['Front'].map(str)+df['Back']

"""
df['edited'] = df['Text'].map(lambda x: x.replace('&nbsp;',' '))
df['edited'] = df['edited'].map(lambda x: x.replace('&amp;;','&'))
df['edited'] = df['edited'].map(lambda x: x.replace('{{',''))
df['edited'] = df['edited'].map(lambda x: x.replace('}}',''))
df['edited'] = df['edited'].map(lambda x: x.replace('c1::',''))
df['edited'] = df['edited'].map(lambda x: x.replace('c2::',''))
df['edited'] = df['edited'].map(lambda x: x.replace('&nbsp;',' '))
df['edited'] = df['edited'].map(lambda x: x.replace('<b>',''))
df['edited'] = df['edited'].map(lambda x: x.replace('</b>',''))
df['edited'] = df['edited'].map(lambda x: x.replace('<u>',''))
df['edited'] = df['edited'].map(lambda x: x.replace('</u>',''))
df['edited'] = df['edited'].map(lambda x: x.replace('<i>',''))
df['edited'] = df['edited'].map(lambda x: x.replace('</i>',''))
df['edited'] = df['edited'].map(lambda x: x.replace('{{',''))
df['edited'] = df['edited'].map(lambda x: x.replace('}}',''))
df['edited'] = df['edited'].map(lambda x: x.replace('c1::',''))
df['edited'] = df['edited'].map(lambda x: x.replace('</div>',''))
df['edited'] = df['edited'].map(lambda x: x.replace('</sub>',''))
df['edited'] = df['edited'].map(lambda x: x.replace('<sub>',''))
df['edited'] = df['edited'].map(lambda x: x.replace('<br />',''))
df['edited'] = df['edited'].map(lambda x: x.replace('<sup>',''))
df['edited'] = df['edited'].map(lambda x: x.replace('</sup>',''))

df['edited'] = df['edited'].map(lambda x: re.sub('<.*?>','', x))
"""
print(df['edited'])

writer = pd.ExcelWriter('output.xlsx')
df.to_excel(writer,'Sheet1')
writer.save()

#search = "misoprostol"
#print(df['edited'][df['edited'].str.lower().str.contains(search)])
#print(df['edited'][df['edited'].str.contains("Misoprostol")])

question = "A 58-year-old male with a history of congestive heart failure and hypertension comes to you with the chief complaint of new-onset cough as well as increased serum potassium in the setting of a new medication. Which of the following medications is most likely responsible for these findings?"
question = "cough"
choices = ["Furosemide", "Metoprolol", "Amiodarone", "Digoxin", "Lisinopril"]

connections = 0

for choice in choices:
	print("Search term: " + choice)
	cards = df['edited'][df['edited'].str.lower().str.contains(choice.lower(), na=False)]
	#print(cards)
	totalSimilar = 0
	cardCount = 0
	for card in cards:
		#print(card)
		s = SequenceMatcher(None, card, question)
		print(s.ratio())
		totalSimilar = s.ratio() + totalSimilar
		cardCount = cardCount + 1
	choiceScore = totalSimilar/cardCount
	print("Choice score: " + str(choiceScore))
