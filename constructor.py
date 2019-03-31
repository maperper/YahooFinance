# File python
inserting_text = '        dataset = {\n        "children":['
concat_text = ''

dicc = dict()

dicc['hola'] = 10
dicc['adiós'] = 23
ii = 1

for key, value in dicc.items():
	if ii == 1:
		concat_text = concat_text + '{"Name":"%s", "Count":%s },' % (key, str(value))
		ii += 1
	else:
		concat_text = concat_text + '\n                {"Name":"%s", "Count":%s },' % (key, str(value))

concat_text = inserting_text + concat_text + ']\n        };'

with open('texto1.txt', 'r') as file:
	texto1 = file.read()

with open('texto2.txt', 'r') as file:
	texto2 = file.read()

texto_final = texto1 + concat_text + texto2

with open('index_final.html', 'w') as file:
	file.write(texto_final)
