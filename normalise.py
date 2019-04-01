''' 
	This script normalises the prizes among different companies and save them in a
	json file in order to analise their movements (ups and downs) measuring their 
	differences using the cuadratic media error. So, for each company the maximun 
	value that can reach will be one and the minimum zero.
'''

def generating_prize_file():
	import os
	import pandas as pd
	import json

	list_of_files = os.listdir('csv')
	dicc = dict()

	for file in list_of_files:
		df = pd.read_csv('csv/' + file)
		prizes = df.Close
		norm_prizes = (prizes - prizes.min())/(prizes.max() - prizes.min())
		dicc[file.split('date')[0]] = list(norm_prizes)
		
	with open('list_of_prizes.json','w') as file:
		json.dump(dicc, file)
    
