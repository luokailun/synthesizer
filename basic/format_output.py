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
import re
num_pattern = re.compile(r"\d+")

def __isbounded(elem, ylen):
	max_num = max([ int(num) for num in num_pattern.findall(elem)]+[-1])
	return max_num < ylen


def format_output(model, keyword):
	universe, M, default_value = model
	xlen = M['xlen()']
	ylen = M['ylen()']
	elems  = [elem for elem in M.keys() if elem.find('Ch')!=-1]
	elems  = [elem for elem in elems if __isbounded(elem, int(ylen))]
	elems.sort()
	#elems = elems[len(elems)/3:]
	format_str = ''
	#print elems
	for e, elem in enumerate(elems):
		if M[elem]== "True":
			format_str = "%sO"%(format_str)
		elif M[elem]== "False":
			format_str = "%s#"%(format_str),
		if (e+1)%int(ylen)==0:
			format_str = "%s\n"%(format_str),
	format_str ='%s-------\n'%format_str
	return format_str


'''
M = ({'_S1': ['p2', 'p1'], 'Int': ['1', '0', '2'], 'Bool': ['True', 'False']}, {'Ch(1,1)': 'False', 'Ch(1,0)': 'False', 'Ch(0,2)': 'False', 'Ch(2,1)': 'False', 'turn(p2)': 'False', 'Ch(0,0)': 'False', 'Ch(0,1)': 'False', 'turn(p1)': 'True', 'Ch(2,0)': 'False', 'Ch(2,2)': 'False', 'ylen()': '2', 'Ch(1,2)': 'False', 'xlen()': '2'}, {})
print format_output(M, 'Ch')
'''


'''
for key, Mlist in L.iteritems():
	print key
	for M in Mlist:
		format_output(M, 'Ch')
	print 
'''



