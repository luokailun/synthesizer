import os

'''
Ms = [{u'cell(2,2)': u'empty', u'len()': u'2', u'turn(p2)': u'False', u'cell(2,0)': u'empty', u'cell(2,1)': u'p2', u'turn(p1)': u'True', u'cell(1,1)': u'empty', u'cell(1,0)': u'empty', u'cell(0,0)': u'empty', u'cell(1,2)': u'p1', u'cell(0,1)': u'empty', u'turn(empty)': u'False', u'cell(0,2)': u'empty'}, {u'cell(2,2)': u'p2', u'len()': 2, u'turn(p2)': False, u'cell(2,0)': u'empty', u'cell(2,1)': u'p2', u'turn(p1)': True, u'cell(1,1)': u'p1', u'cell(1,0)': u'empty', u'cell(0,0)': u'empty', u'cell(1,2)': u'p1', u'cell(0,1)': u'empty', u'turn(empty)': False, u'cell(0,2)': u'empty'}, {u'cell(2,2)': u'p2', u'len()': u'2', u'turn(p2)': u'False', u'cell(2,0)': u'empty', u'cell(2,1)': u'empty', u'turn(p1)': u'True', u'cell(1,1)': u'p1', u'cell(1,0)': u'empty', u'cell(0,0)': u'empty', u'cell(1,2)': u'empty', u'cell(0,1)': u'empty', u'turn(empty)': u'False', u'cell(0,2)': u'empty'}]
def format_output(M, keyword):
	elems  = [elem for elem in M.keys() if elem.find(keyword)!=-1 and elem.find('0')==-1]
	elems.sort()
	#elems = elems[len(elems)/3:]
	for e, elem in enumerate(elems):
		if e == len(elems)/2:
			print '\n',
		if M[elem] =='empty':
			print '[]',
		else:
			print M[elem],
	print '\n-------\n'
'''

'''
def format_output(M, keyword):
	elems  = [elem for elem in M.keys() if elem.find(keyword)!=-1 and elem.find('0')==-1]
	elems.sort()
	#elems = elems[len(elems)/3:]
	for e, elem in enumerate(elems):
		if M[elem] =='empty':
			print '[]',
		elif M[elem] == 'unknown':
			print '#',
		elif M[elem] == 'red':
			print 'r',
		elif M[elem] == 'blue':
			print 'b',
		else:
			print '------'
	print '\n-------\n'
'''


def format_output(model, keyword):
	universe, M = model
	elems  = [elem for elem in M.keys() if elem.find(keyword)!=-1]
	elems.sort()
	#elems = elems[len(elems)/3:]
	xlen = M['xlen()']
	ylen = M['ylen()']
	#print elems
	for e, elem in enumerate(elems):
		if M[elem]== "True":
			print 'O',
		elif M[elem]== "False":
			print '#',
		if (e+1)%int(ylen)==0:
			print ""
	print '\n-------\n'



'''
fail
Mlist = [{u'Ch(1,1)': u'True', u'Ch(1,0)': u'False', u'Ch(0,2)': u'False', u'Ch(2,1)': u'False', u'turn(p2)': u'False', u'lasty()': u'1', u'Ch(0,0)': u'False', u'xlen()': u'2', u'turn(p1)': u'True', u'lastx()': u'2', u'Ch(2,0)': u'False', u'Ch(2,2)': u'False', u'ylen()': u'2', u'Ch(1,2)': u'True', u'Ch(0,1)': u'False'}, {u'Ch(1,1)': u'False', u'Ch(1,0)': u'False', u'Ch(0,2)': u'False', u'Ch(2,1)': u'False', u'turn(p2)': u'False', u'lasty()': u'1', u'Ch(0,0)': u'False', u'xlen()': u'2', u'turn(p1)': u'True', u'lastx()': u'1', u'Ch(2,0)': u'False', u'Ch(2,2)': u'False', u'ylen()': u'1', u'Ch(1,2)': u'False', u'Ch(0,1)': u'False'}, {u'Ch(1,1)': u'False', u'Ch(1,0)': u'False', u'Ch(0,2)': u'False', u'Ch(2,1)': u'False', u'turn(p2)': u'False', u'lasty()': u'1', u'Ch(0,0)': u'False', u'xlen()': u'2', u'turn(p1)': u'True', u'lastx()': u'1', u'Ch(2,0)': u'False', u'Ch(2,2)': u'False', u'ylen()': u'2', u'Ch(1,2)': u'False', u'Ch(0,1)': u'False'}, {u'Ch(1,1)': u'True', u'Ch(1,0)': u'False', u'Ch(0,2)': u'False', u'Ch(2,1)': u'True', u'turn(p2)': u'False', u'lasty()': u'2', u'Ch(0,0)': u'False', u'xlen()': u'2', u'turn(p1)': u'True', u'lastx()': u'1', u'Ch(2,0)': u'False', u'Ch(2,2)': u'False', u'ylen()': u'2', u'Ch(1,2)': u'False', u'Ch(0,1)': u'False'}]

L ={u'q_3': [{u'Ch(1,1)': u'True', u'Ch(1,0)': u'False', u'Ch(0,2)': u'False', u'Ch(2,1)': u'False', u'turn(p2)': u'False', u'lasty()': u'1', u'Ch(0,0)': u'False', u'xlen()': u'2', u'turn(p1)': u'True', u'lastx()': u'2', u'Ch(2,0)': u'False', u'Ch(2,2)': u'False', u'ylen()': u'2', u'Ch(1,2)': u'True', u'Ch(0,1)': u'False'}, {u'Ch(1,1)': u'False', u'Ch(1,0)': u'False', u'Ch(0,2)': u'False', u'Ch(2,1)': u'False', u'turn(p2)': u'False', u'lasty()': u'1', u'Ch(0,0)': u'False', u'xlen()': u'2', u'turn(p1)': u'True', u'lastx()': u'1', u'Ch(2,0)': u'False', u'Ch(2,2)': u'False', u'ylen()': u'2', u'Ch(1,2)': u'False', u'Ch(0,1)': u'False'}, {u'Ch(1,1)': u'True', u'Ch(1,0)': u'False', u'Ch(0,2)': u'False', u'Ch(2,1)': u'True', u'turn(p2)': u'False', u'lasty()': u'2', u'Ch(0,0)': u'False', u'xlen()': u'2', u'turn(p1)': u'True', u'lastx()': u'1', u'Ch(2,0)': u'False', u'Ch(2,2)': u'False', u'ylen()': u'2', u'Ch(1,2)': u'False', u'Ch(0,1)': u'False'}], u'q_2': [{u'Ch(1,1)': u'True', u'Ch(1,0)': u'False', u'Ch(0,2)': u'False', u'Ch(2,1)': u'True', u'turn(p2)': u'True', u'lasty()': u'2', u'Ch(0,0)': u'False', u'xlen()': u'2', u'turn(p1)': u'False', u'lastx()': u'2', u'Ch(2,0)': u'False', u'Ch(2,2)': u'False', u'ylen()': u'2', u'Ch(1,2)': u'True', u'Ch(0,1)': u'False'}, {u'Ch(1,1)': u'True', u'Ch(1,0)': u'False', u'Ch(0,2)': u'False', u'Ch(2,1)': u'False', u'turn(p2)': u'True', u'lasty()': u'1', u'Ch(0,0)': u'False', u'xlen()': u'2', u'turn(p1)': u'False', u'lastx()': u'2', u'Ch(2,0)': u'False', u'Ch(2,2)': u'False', u'ylen()': u'2', u'Ch(1,2)': u'False', u'Ch(0,1)': u'False'}, {u'Ch(1,1)': u'True', u'Ch(1,0)': u'False', u'Ch(0,2)': u'False', u'Ch(2,1)': u'False', u'turn(p2)': u'True', u'lasty()': u'2', u'Ch(0,0)': u'False', u'xlen()': u'2', u'turn(p1)': u'False', u'lastx()': u'1', u'Ch(2,0)': u'False', u'Ch(2,2)': u'False', u'ylen()': u'2', u'Ch(1,2)': u'False', u'Ch(0,1)': u'False'}], u'q_1': [{'Ch(1,1)': True, 'Ch(1,0)': False, 'Ch(0,2)': False, 'Ch(2,1)': True, 'turn(p2)': False, 'lasty()': 1, 'Ch(0,0)': False, 'xlen()': 2, 'turn(p1)': True, 'lastx()': 1, 'Ch(2,0)': False, 'Ch(2,2)': True, 'ylen()': 2, 'Ch(1,2)': True, 'Ch(0,1)': False}]}

for key, Mlist in L.iteritems():
	print key
	for M in Mlist:
		format_output(M, 'Ch')
	print 
	
'''


