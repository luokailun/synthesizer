

M = ({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2', '3', '4'], 'Bool': ['True', 'False']}, {'Ch(1,0)': 'True', 'Ch(2,1)': 'True', 'turn(p2)': 'False', 'Ch(2,3)': 'False', 'Ch(1,4)': 'False', 'Ch(3,1)': 'False', 'ylen()': '4', 'Ch(3,3)': 'False', 'Ch(1,2)': 'False', 'Ch(0,2)': 'True', 'Ch(0,0)': 'True', 'Ch(4,2)': 'False', 'Ch(4,3)': 'False', 'Ch(4,1)': 'False', 'Ch(4,4)': 'False', 'Ch(3,4)': 'False', 'Ch(1,1)': 'True', 'Ch(2,0)': 'True', 'Ch(2,2)': 'False', 'turn(p1)': 'True', 'Ch(2,4)': 'False', 'Ch(3,0)': 'False', 'Ch(0,4)': 'False', 'Ch(3,2)': 'False', 'Ch(1,3)': 'False', 'Ch(0,3)': 'True', 'xlen()': '4', 'Ch(4,0)': 'False', 'Ch(0,1)': 'False'}, {'Ch\\(\\d+,\\d+\\)': 'False'})

def get_goal(player):
	lambda_fun, para_list = context_operator.find_axiom_with_feature('win', Util.generate_function_feature(player+'()'))
	Win = lambda_fun(para_list)
	End = context_operator.get_axioms()['end']['']
	return "( %s ) => ( %s )"%(End, Win)


from parser import BATparser
from basic import context_operator
from basic import Util
from algorithm import algorithm3 
from strategy import strategy_translator

BATparser.parser('chompNN.sc')
Goal = get_goal('p1')


result = ['************************************************************************\n', '                       MCMAS v1.3.0 \n', '\n', ' This software comes with ABSOLUTELY NO WARRANTY, to the extent\n', ' permitted by applicable law. \n', '\n', ' Please check http://vas.doc.ic.ac.uk/tools/mcmas/ for the latest release.\n', ' Please send any feedback to <mcmas@imperial.ac.uk>\n', '************************************************************************\n', '\n', 'Command line: ./input_mcmas/mcmas -c 1 -l 1 -f 1 ./input_mcmas/win.ispl\n', '\n', './input_mcmas/win.ispl has been parsed successfully.\n', 'Global syntax checking...\n', '1\n', '1\n', '1\n', 'Done\n', 'Encoding BDD parameters...\n', 'Building partial transition relation...\n', 'Building BDD for initial states...\n', 'Building reachable state space...\n', 'Checking formulae...\n', 'Verifying properties...\n', '  Formula number 1: (<g1>G goal), is TRUE in the model\n', '  The following is a witness for the formula: \n', '   < 0 1 > \n', '   < 0 1 > \n', '   < 0 1 > \n', '   < 0 1 > \n', '   < 1 2 > \n', '   < 1 2 > \n', '   < 1 2 > \n', '   < 1 2 > \n', '   < 1 2 > \n', '   < 1 2 > \n', '   < 1 2 > \n', '   < 1 2 > \n', '   < 1 2 > \n', '   < 1 2 > \n', '   < 1 2 > \n', '   < 1 2 > \n', '   < 1 3 > \n', '   < 1 3 > \n', '   < 1 3 > \n', '   < 1 3 > \n', '   < 1 4 > \n', '   < 1 4 > \n', '   < 1 4 > \n', '   < 1 4 > \n', '   < 1 4 > \n', '   < 1 4 > \n', '   < 1 4 > \n', '   < 1 4 > \n', '   < 1 5 > \n', '   < 1 5 > \n', '   < 1 5 > \n', '   < 1 5 > \n', '   < 1 5 > \n', '   < 1 5 > \n', '   < 1 5 > \n', '   < 1 5 > \n', '   < 1 6 > \n', '   < 1 6 > \n', '   < 1 6 > \n', '   < 1 6 > \n', '   < 1 3 > \n', '   < 1 3 > \n', '   < 1 3 > \n', '   < 1 3 > \n', '   < 1 3 > \n', '   < 1 3 > \n', '   < 1 3 > \n', '   < 1 3 > \n', '   < 1 4 > \n', '   < 1 4 > \n', '   < 1 4 > \n', '   < 1 4 > \n', '   < 1 5 > \n', '   < 1 5 > \n', '   < 1 5 > \n', '   < 1 5 > \n', '   < 1 6 > \n', '   < 1 6 > \n', '   < 1 6 > \n', '   < 1 6 > \n', '   < 1 4 > \n', '   < 1 4 > \n', '   < 1 4 > \n', '   < 1 4 > \n', '   < 1 3 > \n', '   < 1 3 > \n', '   < 1 3 > \n', '   < 1 3 > \n', '   < 1 6 > \n', '   < 1 6 > \n', '   < 1 6 > \n', '   < 1 6 > \n', '   < 1 5 > \n', '   < 1 5 > \n', '   < 1 5 > \n', '   < 1 5 > \n', '   < 1 2 > \n', '   < 1 2 > \n', '   < 1 2 > \n', '   < 1 2 > \n', '   < 1 6 > \n', '   < 1 6 > \n', '   < 1 6 > \n', '   < 1 6 > \n', '   < 5 5 > \n', '   < 5 5 > \n', '   < 5 5 > \n', '   < 2 7 > \n', '   < 6 7 > \n', '   < 6 7 > \n', '   < 2 7 > \n', '   < 6 7 > \n', '   < 6 7 > \n', '   < 2 7 > \n', '   < 2 7 > \n', '   < 6 7 > \n', '   < 6 7 > \n', '   < 6 7 > \n', '   < 2 7 > \n', '   < 6 7 > \n', '   < 2 7 > \n', '   < 2 7 > \n', '   < 2 7 > \n', '   < 3 8 > \n', '   < 3 8 > \n', '   < 4 8 > \n', '   < 4 8 > \n', '   < 3 8 > \n', '   < 4 8 > \n', '   < 3 8 > \n', '   < 4 8 > \n', '   < 3 8 > \n', '   < 3 8 > \n', '   < 4 8 > \n', '   < 3 8 > \n', '   < 4 8 > \n', '   < 4 8 > \n', '   < 3 8 > \n', '   < 4 8 > \n', '   < 2 7 > \n', '   < 6 7 > \n', '   < 6 7 > \n', '   < 2 7 > \n', '   < 2 7 > \n', '   < 6 7 > \n', '   < 6 7 > \n', '   < 2 7 > \n', '   < 3 8 > \n', '   < 3 8 > \n', '   < 4 8 > \n', '   < 4 8 > \n', '   < 4 8 > \n', '   < 4 8 > \n', '   < 3 8 > \n', '   < 3 8 > \n', '   < 4 8 > \n', '   < 4 8 > \n', '   < 3 8 > \n', '   < 4 8 > \n', '   < 3 8 > \n', '   < 3 8 > \n', '   < 3 8 > \n', '   < 4 8 > \n', '   < 2 7 > \n', '   < 2 7 > \n', '   < 6 7 > \n', '   < 6 7 > \n', '   < 6 7 > \n', '   < 6 7 > \n', '   < 2 7 > \n', '   < 2 7 > \n', '   < 5 5 > \n', '   < 7 9 > \n', '   < 7 9 > \n', '   < 7 9 > \n', '   < 7 9 > \n', '   < 7 10 > \n', '   < 7 10 > \n', '   < 7 10 > \n', '   < 7 10 > \n', '   < 7 5 > \n', '   < 7 5 > \n', '   < 8 5 > \n', '   < 8 5 > \n', '   < 8 5 > \n', '   < 7 5 > \n', '   < 8 5 > \n', '   < 7 5 > \n', '   < 7 10 > \n', '   < 7 10 > \n', '   < 7 10 > \n', '   < 7 10 > \n', '   < 7 5 > \n', '   < 8 5 > \n', '   < 8 5 > \n', '   < 8 5 > \n', '   < 7 5 > \n', '   < 8 5 > \n', '   < 7 5 > \n', '   < 7 5 > \n', '   < 7 9 > \n', '   < 7 9 > \n', '   < 7 9 > \n', '   < 7 9 > \n', '   < 7 10 > \n', '   < 7 10 > \n', '   < 7 10 > \n', '   < 7 10 > \n', '   < 7 9 > \n', '   < 7 9 > \n', '   < 7 9 > \n', '   < 7 9 > \n', '   < 7 9 > \n', '   < 7 9 > \n', '   < 7 9 > \n', '   < 7 9 > \n', '   < 8 5 > \n', '   < 8 5 > \n', '   < 7 5 > \n', '   < 8 5 > \n', '   < 7 5 > \n', '   < 7 5 > \n', '   < 7 5 > \n', '   < 8 5 > \n', '   < 7 5 > \n', '   < 8 5 > \n', '   < 7 5 > \n', '   < 7 5 > \n', '   < 8 5 > \n', '   < 8 5 > \n', '   < 7 5 > \n', '   < 8 5 > \n', '   < 7 10 > \n', '   < 7 10 > \n', '   < 7 10 > \n', '   < 7 10 > \n', '   < 9 8 > \n', '   < 10 8 > \n', '   < 9 8 > \n', '   < 10 8 > \n', '   < 10 8 > \n', '   < 9 8 > \n', '   < 9 8 > \n', '   < 10 8 > \n', '   < 9 8 > \n', '   < 10 8 > \n', '   < 10 8 > \n', '   < 9 8 > \n', '   < 9 8 > \n', '   < 10 8 > \n', '   < 9 8 > \n', '   < 10 8 > \n', '   < 10 8 > \n', '   < 9 8 > \n', '   < 9 8 > \n', '   < 9 8 > \n', '   < 9 8 > \n', '   < 10 8 > \n', '   < 10 8 > \n', '   < 10 8 > \n', '   < 10 8 > \n', '   < 9 8 > \n', '   < 9 8 > \n', '   < 9 8 > \n', '   < 10 8 > \n', '   < 10 8 > \n', '   < 9 8 > \n', '   < 10 8 > \n', '  States description: \n', '------------- State: 0 -----------------\n', 'Agent Environment\n', '  Ch_0_0 = true\n', '  Ch_0_1 = true\n', '  Ch_0_2 = true\n', '  Ch_0_3 = false\n', '  Ch_0_4 = false\n', '  Ch_1_0 = true\n', '  Ch_1_1 = true\n', '  Ch_1_2 = true\n', '  Ch_1_3 = false\n', '  Ch_1_4 = false\n', '  Ch_2_0 = true\n', '  Ch_2_1 = true\n', '  Ch_2_2 = true\n', '  Ch_2_3 = false\n', '  Ch_2_4 = false\n', '  Ch_3_0 = false\n', '  Ch_3_1 = false\n', '  Ch_3_2 = false\n', '  Ch_3_3 = false\n', '  Ch_3_4 = false\n', '  Ch_4_0 = false\n', '  Ch_4_1 = false\n', '  Ch_4_2 = false\n', '  Ch_4_3 = false\n', '  Ch_4_4 = false\n', '  turn_p1 = true\n', '  turn_p2 = false\n', '  xlen_ = 3\n', '  ylen_ = 3\n', 'Agent Player1\n', '  state = none\n', 'Agent Player2\n', '  state = none\n', '----------------------------------------\n', '------------- State: 1 -----------------\n', 'Agent Environment\n', '  Ch_0_0 = true\n', '  Ch_0_1 = true\n', '  Ch_0_2 = true\n', '  Ch_0_3 = false\n', '  Ch_0_4 = false\n', '  Ch_1_0 = true\n', '  Ch_1_1 = false\n', '  Ch_1_2 = false\n', '  Ch_1_3 = false\n', '  Ch_1_4 = false\n', '  Ch_2_0 = true\n', '  Ch_2_1 = false\n', '  Ch_2_2 = false\n', '  Ch_2_3 = false\n', '  Ch_2_4 = false\n', '  Ch_3_0 = false\n', '  Ch_3_1 = false\n', '  Ch_3_2 = false\n', '  Ch_3_3 = false\n', '  Ch_3_4 = false\n', '  Ch_4_0 = false\n', '  Ch_4_1 = false\n', '  Ch_4_2 = false\n', '  Ch_4_3 = false\n', '  Ch_4_4 = false\n', '  turn_p1 = false\n', '  turn_p2 = true\n', '  xlen_ = 3\n', '  ylen_ = 3\n', 'Agent Player1\n', '  state = none\n', 'Agent Player2\n', '  state = none\n', '----------------------------------------\n', '------------- State: 2 -----------------\n', 'Agent Environment\n', '  Ch_0_0 = true\n', '  Ch_0_1 = true\n', '  Ch_0_2 = false\n', '  Ch_0_3 = false\n', '  Ch_0_4 = false\n', '  Ch_1_0 = true\n', '  Ch_1_1 = false\n', '  Ch_1_2 = false\n', '  Ch_1_3 = false\n', '  Ch_1_4 = false\n', '  Ch_2_0 = true\n', '  Ch_2_1 = false\n', '  Ch_2_2 = false\n', '  Ch_2_3 = false\n', '  Ch_2_4 = false\n', '  Ch_3_0 = false\n', '  Ch_3_1 = false\n', '  Ch_3_2 = false\n', '  Ch_3_3 = false\n', '  Ch_3_4 = false\n', '  Ch_4_0 = false\n', '  Ch_4_1 = false\n', '  Ch_4_2 = false\n', '  Ch_4_3 = false\n', '  Ch_4_4 = false\n', '  turn_p1 = true\n', '  turn_p2 = false\n', '  xlen_ = 3\n', '  ylen_ = 3\n', 'Agent Player1\n', '  state = none\n', 'Agent Player2\n', '  state = none\n', '----------------------------------------\n', '------------- State: 3 -----------------\n', 'Agent Environment\n', '  Ch_0_0 = true\n', '  Ch_0_1 = false\n', '  Ch_0_2 = false\n', '  Ch_0_3 = false\n', '  Ch_0_4 = false\n', '  Ch_1_0 = true\n', '  Ch_1_1 = false\n', '  Ch_1_2 = false\n', '  Ch_1_3 = false\n', '  Ch_1_4 = false\n', '  Ch_2_0 = true\n', '  Ch_2_1 = false\n', '  Ch_2_2 = false\n', '  Ch_2_3 = false\n', '  Ch_2_4 = false\n', '  Ch_3_0 = false\n', '  Ch_3_1 = false\n', '  Ch_3_2 = false\n', '  Ch_3_3 = false\n', '  Ch_3_4 = false\n', '  Ch_4_0 = false\n', '  Ch_4_1 = false\n', '  Ch_4_2 = false\n', '  Ch_4_3 = false\n', '  Ch_4_4 = false\n', '  turn_p1 = true\n', '  turn_p2 = false\n', '  xlen_ = 3\n', '  ylen_ = 3\n', 'Agent Player1\n', '  state = none\n', 'Agent Player2\n', '  state = none\n', '----------------------------------------\n', '------------- State: 4 -----------------\n', 'Agent Environment\n', '  Ch_0_0 = true\n', '  Ch_0_1 = true\n', '  Ch_0_2 = true\n', '  Ch_0_3 = false\n', '  Ch_0_4 = false\n', '  Ch_1_0 = false\n', '  Ch_1_1 = false\n', '  Ch_1_2 = false\n', '  Ch_1_3 = false\n', '  Ch_1_4 = false\n', '  Ch_2_0 = false\n', '  Ch_2_1 = false\n', '  Ch_2_2 = false\n', '  Ch_2_3 = false\n', '  Ch_2_4 = false\n', '  Ch_3_0 = false\n', '  Ch_3_1 = false\n', '  Ch_3_2 = false\n', '  Ch_3_3 = false\n', '  Ch_3_4 = false\n', '  Ch_4_0 = false\n', '  Ch_4_1 = false\n', '  Ch_4_2 = false\n', '  Ch_4_3 = false\n', '  Ch_4_4 = false\n', '  turn_p1 = true\n', '  turn_p2 = false\n', '  xlen_ = 3\n', '  ylen_ = 3\n', 'Agent Player1\n', '  state = none\n', 'Agent Player2\n', '  state = none\n', '----------------------------------------\n', '------------- State: 5 -----------------\n', 'Agent Environment\n', '  Ch_0_0 = false\n', '  Ch_0_1 = false\n', '  Ch_0_2 = false\n', '  Ch_0_3 = false\n', '  Ch_0_4 = false\n', '  Ch_1_0 = false\n', '  Ch_1_1 = false\n', '  Ch_1_2 = false\n', '  Ch_1_3 = false\n', '  Ch_1_4 = false\n', '  Ch_2_0 = false\n', '  Ch_2_1 = false\n', '  Ch_2_2 = false\n', '  Ch_2_3 = false\n', '  Ch_2_4 = false\n', '  Ch_3_0 = false\n', '  Ch_3_1 = false\n', '  Ch_3_2 = false\n', '  Ch_3_3 = false\n', '  Ch_3_4 = false\n', '  Ch_4_0 = false\n', '  Ch_4_1 = false\n', '  Ch_4_2 = false\n', '  Ch_4_3 = false\n', '  Ch_4_4 = false\n', '  turn_p1 = true\n', '  turn_p2 = false\n', '  xlen_ = 3\n', '  ylen_ = 3\n', 'Agent Player1\n', '  state = none\n', 'Agent Player2\n', '  state = none\n', '----------------------------------------\n', '------------- State: 6 -----------------\n', 'Agent Environment\n', '  Ch_0_0 = true\n', '  Ch_0_1 = true\n', '  Ch_0_2 = true\n', '  Ch_0_3 = false\n', '  Ch_0_4 = false\n', '  Ch_1_0 = true\n', '  Ch_1_1 = false\n', '  Ch_1_2 = false\n', '  Ch_1_3 = false\n', '  Ch_1_4 = false\n', '  Ch_2_0 = false\n', '  Ch_2_1 = false\n', '  Ch_2_2 = false\n', '  Ch_2_3 = false\n', '  Ch_2_4 = false\n', '  Ch_3_0 = false\n', '  Ch_3_1 = false\n', '  Ch_3_2 = false\n', '  Ch_3_3 = false\n', '  Ch_3_4 = false\n', '  Ch_4_0 = false\n', '  Ch_4_1 = false\n', '  Ch_4_2 = false\n', '  Ch_4_3 = false\n', '  Ch_4_4 = false\n', '  turn_p1 = true\n', '  turn_p2 = false\n', '  xlen_ = 3\n', '  ylen_ = 3\n', 'Agent Player1\n', '  state = none\n', 'Agent Player2\n', '  state = none\n', '----------------------------------------\n', '------------- State: 7 -----------------\n', 'Agent Environment\n', '  Ch_0_0 = true\n', '  Ch_0_1 = true\n', '  Ch_0_2 = false\n', '  Ch_0_3 = false\n', '  Ch_0_4 = false\n', '  Ch_1_0 = true\n', '  Ch_1_1 = false\n', '  Ch_1_2 = false\n', '  Ch_1_3 = false\n', '  Ch_1_4 = false\n', '  Ch_2_0 = false\n', '  Ch_2_1 = false\n', '  Ch_2_2 = false\n', '  Ch_2_3 = false\n', '  Ch_2_4 = false\n', '  Ch_3_0 = false\n', '  Ch_3_1 = false\n', '  Ch_3_2 = false\n', '  Ch_3_3 = false\n', '  Ch_3_4 = false\n', '  Ch_4_0 = false\n', '  Ch_4_1 = false\n', '  Ch_4_2 = false\n', '  Ch_4_3 = false\n', '  Ch_4_4 = false\n', '  turn_p1 = false\n', '  turn_p2 = true\n', '  xlen_ = 3\n', '  ylen_ = 3\n', 'Agent Player1\n', '  state = none\n', 'Agent Player2\n', '  state = none\n', '----------------------------------------\n', '------------- State: 8 -----------------\n', 'Agent Environment\n', '  Ch_0_0 = true\n', '  Ch_0_1 = false\n', '  Ch_0_2 = false\n', '  Ch_0_3 = false\n', '  Ch_0_4 = false\n', '  Ch_1_0 = false\n', '  Ch_1_1 = false\n', '  Ch_1_2 = false\n', '  Ch_1_3 = false\n', '  Ch_1_4 = false\n', '  Ch_2_0 = false\n', '  Ch_2_1 = false\n', '  Ch_2_2 = false\n', '  Ch_2_3 = false\n', '  Ch_2_4 = false\n', '  Ch_3_0 = false\n', '  Ch_3_1 = false\n', '  Ch_3_2 = false\n', '  Ch_3_3 = false\n', '  Ch_3_4 = false\n', '  Ch_4_0 = false\n', '  Ch_4_1 = false\n', '  Ch_4_2 = false\n', '  Ch_4_3 = false\n', '  Ch_4_4 = false\n', '  turn_p1 = false\n', '  turn_p2 = true\n', '  xlen_ = 3\n', '  ylen_ = 3\n', 'Agent Player1\n', '  state = none\n', 'Agent Player2\n', '  state = none\n', '----------------------------------------\n', '------------- State: 9 -----------------\n', 'Agent Environment\n', '  Ch_0_0 = true\n', '  Ch_0_1 = true\n', '  Ch_0_2 = false\n', '  Ch_0_3 = false\n', '  Ch_0_4 = false\n', '  Ch_1_0 = false\n', '  Ch_1_1 = false\n', '  Ch_1_2 = false\n', '  Ch_1_3 = false\n', '  Ch_1_4 = false\n', '  Ch_2_0 = false\n', '  Ch_2_1 = false\n', '  Ch_2_2 = false\n', '  Ch_2_3 = false\n', '  Ch_2_4 = false\n', '  Ch_3_0 = false\n', '  Ch_3_1 = false\n', '  Ch_3_2 = false\n', '  Ch_3_3 = false\n', '  Ch_3_4 = false\n', '  Ch_4_0 = false\n', '  Ch_4_1 = false\n', '  Ch_4_2 = false\n', '  Ch_4_3 = false\n', '  Ch_4_4 = false\n', '  turn_p1 = true\n', '  turn_p2 = false\n', '  xlen_ = 3\n', '  ylen_ = 3\n', 'Agent Player1\n', '  state = none\n', 'Agent Player2\n', '  state = none\n', '----------------------------------------\n', '------------- State: 10 -----------------\n', 'Agent Environment\n', '  Ch_0_0 = true\n', '  Ch_0_1 = false\n', '  Ch_0_2 = false\n', '  Ch_0_3 = false\n', '  Ch_0_4 = false\n', '  Ch_1_0 = true\n', '  Ch_1_1 = false\n', '  Ch_1_2 = false\n', '  Ch_1_3 = false\n', '  Ch_1_4 = false\n', '  Ch_2_0 = false\n', '  Ch_2_1 = false\n', '  Ch_2_2 = false\n', '  Ch_2_3 = false\n', '  Ch_2_4 = false\n', '  Ch_3_0 = false\n', '  Ch_3_1 = false\n', '  Ch_3_2 = false\n', '  Ch_3_3 = false\n', '  Ch_3_4 = false\n', '  Ch_4_0 = false\n', '  Ch_4_1 = false\n', '  Ch_4_2 = false\n', '  Ch_4_3 = false\n', '  Ch_4_4 = false\n', '  turn_p1 = true\n', '  turn_p2 = false\n', '  xlen_ = 3\n', '  ylen_ = 3\n', 'Agent Player1\n', '  state = none\n', 'Agent Player2\n', '  state = none\n', '----------------------------------------\n', 'done, 1 formulae successfully read and checked\n', 'execution time = 0.487\n', 'number of reachable states = 152\n', 'BDD memory in use = 11267840\n']
M = ({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2', '3', '4'], 'Bool': ['True', 'False']}, {'Ch(1,0)': 'True', 'Ch(2,1)': 'True', 'turn(p2)': 'False', 'Ch(2,3)': 'False', 'Ch(1,4)': 'False', 'Ch(3,1)': 'False', 'ylen()': '3', 'Ch(3,3)': 'False', 'Ch(1,2)': 'True', 'Ch(0,2)': 'True', 'Ch(0,0)': 'True', 'Ch(4,2)': 'False', 'Ch(4,3)': 'False', 'Ch(4,1)': 'False', 'Ch(4,4)': 'False', 'Ch(3,4)': 'False', 'Ch(1,1)': 'True', 'Ch(2,0)': 'True', 'Ch(2,2)': 'True', 'turn(p1)': 'True', 'Ch(2,4)': 'False', 'Ch(3,0)': 'False', 'Ch(0,4)': 'False', 'Ch(3,2)': 'False', 'Ch(1,3)': 'False', 'Ch(0,3)': 'False', 'xlen()': '3', 'Ch(4,0)': 'False', 'Ch(0,1)': 'True'}, {'Ch\\(\\d+,\\d+\\)': 'False'})


#print algorithm3.__decide_update_model(M, 'E', Goal, 'p1', list())

print strategy_translator.construct_strategy(result, M)