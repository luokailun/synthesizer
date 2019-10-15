



#from basic import context_operator




from parser import BATparser
from model import util_model
from basic import format_output
from prover import mcmas


M = ({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2', '3'], 'Bool': ['True', 'False']}, {'Ch(1,1)': 'False', 'Ch(1,0)': 'True', 'Ch(0,2)': 'False', 'Ch(0,3)': 'False', 'Ch(3,3)': 'False', 'turn(p2)': 'True', 'Ch(0,0)': 'True', 'xlen()': '3', 'turn(p1)': 'False', 'Ch(3,1)': 'False', 'Ch(2,3)': 'False', 'Ch(2,0)': 'False', 'Ch(3,0)': 'False', 'Ch(2,1)': 'False', 'Ch(2,2)': 'False', 'ylen()': '3', 'Ch(3,2)': 'False', 'Ch(1,3)': 'False', 'Ch(1,2)': 'False', 'Ch(0,1)': 'True'}, {'Ch\\(\\d+,\\d+\\)': 'False'})
BATparser.parser('chompNN.sc')

#print format_output(M,'Ch')
newMs = mcmas.get_init_models_with_universe(M)

print format_output.format_outputs(newMs,'Ch')
