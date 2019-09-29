


import ispl_translator
import os
import re


result_string = r"Formula number 1:.+?, is (.+?) in the model"
result_pattern = re.compile(result_string)

def interpret_result(result):
	the_result = result_pattern.search(' '.join(result))
	if the_result is None:
		print 'ERROR'
		exit(0)
	elif the_result.group(1).replace(' ','') == 'TRUE':
		return True
	elif the_result.group(1).replace(' ','') == 'FALSE':
		return False
	else:
		print 'unmatch---:', the_result.group(1)
		exit(0)



def check_win(model, goal):
	with open("./input_mcmas/model.ispl","write") as input_file:
		input_file.writelines(ispl_translator.to_ispl(model, goal))
		input_file.close()
		cmd = "./input_mcmas/mcmas ./input_mcmas/model.ispl"
		return os.popen(cmd).readlines()






#M = ({'_S1': ['p2', 'p1'], 'Int': ['1', '0', '3', '2', '4'], 'Bool': ['True', 'False']}, {'turn(p1)': True, 'numStone()': 1, 'turn(p2)': False})

#Goal = "numStone()=0 => !turn(p1)"


