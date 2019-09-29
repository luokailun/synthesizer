import re

name = r'[a-zA-Z][a-zA-Z\d\-\_]*'
var = r'\?' + name
name_or_var = r'{}|{}'.format(name, var)
neg = '~'

inequality = re.compile(r'(?<![\w\-])({})\s*=\s*({})(?![\w\-])'.format(name, name))
equality = re.compile(r'(?<![\w\-])({})\s*=\s*\1(?![\w\-])'.format(name_or_var))
# equality = re.compile(r'({}|{})\s*=\s*\1'.format(var, name))
parenthesis = re.compile(r'\(\s*(false|true)\s*\)')
ntrue = re.compile(r'~true')
nfalse = re.compile(r'~false')
nls = ['&', '|', ':', '@', '(', ')'] # non-logic symbol

def after_next_formula(op, s):
	'''return the end position + 1 of the next parenthesis w.r.t s'''
	considered = nls[nls.index(op)+1:]
	for i, l in enumerate(considered):
		considered[i] = '(?:\\%s)'%(l)
	temp = '|'.join(considered)
	np, pos = 0, len(s)
	for op in re.finditer(temp, s):
		if op.group(0) == '(':
			np += 1
		elif op.group(0) == ')':
			np -= 1
			if np < 0:
				pos = op.start()
				break
		else:
			pos = op.start()
			break
	return pos

def before_last_formula(op, s):
	'''return the start position of the last parenthesis w.r.t. s'''
	considered = nls[nls.index(op)+1:]
	for i, l in enumerate(considered):
		considered[i] = '(?:\\%s)'%(l)
	np, pos = 0, len(s)
	temp = '|'.join(considered)
	for op in re.finditer(temp, s[::-1]):
		if op.group(0) == '(':
			np += 1
			if np > 0:
				pos = op.start()
				break
		elif op.group(0) == ')':
			np -= 1
		else:
			pos = op.start()
			break
	return pos

def remove_eq(s, constants=set()):
	for ceq in inequality.finditer(s):
		if ceq.group(1) != ceq.group(2) and ceq.group(1) in constants and ceq.group(2) in constants:
			s = re.sub(r'{}\s*=\s*{}'.format(ceq.group(1), ceq.group(2)), 'false', s)
	return re.sub(equality, 'true', s)

def remove_paren(s):
	s = re.sub(parenthesis, r'\g<1>', s)
	return s

def remove_paren2(s):
	s = re.sub(r'\(\s*(\d+)\s*\)', r'\g<1>', s)
	return s
	# return re.sub(r'\(\s*(?:(\((?:.+)\)))\s*\)', r'\g<1>',s)

def remove_neg(s):
	s = re.sub(r'~\s*~', '', s)
	s = re.sub(ntrue, 'false', s)
	return re.sub(nfalse, 'true', s)

def remove_and(s):
	s = re.sub(r'(?<!\d)(\d+)\s*\&\s*\1(?!\d)', r'\g<1>', s)
	s = re.sub(r'\s*\&\s*true', '', s)
	s = re.sub(r'(?<![\w\-])true\s*\&\s*', '', s)
	p = re.search(r'(?<![\w\-])false\s*\&', s)
	while p != None :
		s = s[:p.start()] + 'false' + s[after_next_formula('&', s[p.end():]) + p.end():]
		p = re.search(r'(?<![\w\-])false\s*\&', s)
	p = re.search(r'\&\s*false', s)
	while p != None :
		s = s[:p.start() - before_last_formula('&', s[:p.start()])] + 'false' + s[p.end():]
		p = re.search(r'\&\s*false', s)
	return s

def remove_or(s):
	s = re.sub(r'(?<![\w\-])false\s*\|\s*', '', s)
	s = re.sub(r'\s*\|\s*false', '', s)
	p = re.search(r'(?<![\w\-])true\s*\|', s)
	while p != None :
		s = s[:p.start()] + 'true' + s[after_next_formula('|', s[p.end():]) + p.end():]
		p = re.search(r'(?<![\w\-])true\s*\|', s)
	p = re.search(r'\|\s*true', s)
	while p != None :
		s = s[:p.start() - before_last_formula('|', s[:p.start()])] + 'true' + s[p.end():]
		p = re.search(r'\|\s*true', s)
	return s

def remove_imply(s):
	s = re.sub(r'(?<![\w\-])true\s*\:', '', s)
	s = re.sub(r'(?<![\w\-])false\s*\:', neg, s)
	p = re.search(r'\:\s*false', s)
	while p != None:
		lastStart = p.start() - before_last_formula('|', s[:p.start()])
		s = s[:lastStart] + neg + s[lastStart:p.start()] + s[p.end():]
		p = re.search(r'\:\s*false', s)
	p = re.search(r'\:\s*true', s)
	while p != None:
		s = s[:p.start() - before_last_formula('|', s[:p.start()])] + 'true' + s[p.end():]
		p = re.search(r'\:\s*true', s)
	return s

def remove_equiv(s):
	s = re.sub(r'(?<![\w\-])true\s*@', '', s)
	s = re.sub(r'@\s*true', '', s)
	s = re.sub(r'(?<![\w\-])false\s*@\s*', neg, s)
	p = re.search(r'\s*@\s*false', s)
	while p != None:
		lastStart = p.start() - before_last_formula('|', s[:p.start()])
		s = s[:lastStart] + neg + s[lastStart:p.start()] + s[p.end():]
		p = re.search(r'\s*@\s*false', s)
	return s

def reduce(s, times=1, constants=set()):
	s = re.sub(r'(?<![\w\-])True(?![\w\-])', 'true', s)
	s = re.sub(r'(?<![\w\-])False(?![\w\-])', 'false', s)
	l = s
	s = remove_eq(s, constants)
	s = remove_paren(s)
	s = remove_neg(s)
	s = remove_and(s)
	s = remove_or(s)
	s = remove_imply(s)
	# s = remove_equiv(s) 
	i = 0
	while l != s and i < times:
		i += 1
		l = s
		s = remove_paren(s)
		s = remove_neg(s)
		s = remove_and(s)
		s = remove_or(s)
		s = remove_imply(s)
		# s = remove_equiv(s)
	return s

def reduce2(s, times=1, constants=set(), simple=False):
	l = s
	s = remove_eq(s, constants)
	s = remove_paren2(s)
	s = remove_neg(s)
	s = remove_and(s)
	s = remove_or(s)
	if not simple:
		s = remove_imply(s)
		s = remove_equiv(s) 
	i = 0
	while l != s and i < times:
		i += 1
		l = s
		s = remove_paren2(s)
		s = remove_neg(s)
		s = remove_and(s)
		s = remove_or(s)
		if not simple:
			s = remove_imply(s)
		# s = remove_equiv(s)
	return s

def transform(s):
	if s != None:
		s = re.sub(r'\!', '~', s)
		s = re.sub(r'\(\)', '', s)
		s = re.sub(r'([^\w])and([^\w])', r'\g<1>&\g<2>', s)
		s = re.sub(r'([^\w])or([^\w])', r'\g<1>|\g<2>', s)
		s = re.sub(r'([^<])=>', r'\g<1>:', s)
		return re.sub(r'<=>', '@', s)


def simplify(s):
	s = transform(s)
	return reduce(s, 3)


if __name__ == '__main__':
	s  = '( next(N2,N1) and source(C,G) and moving() and robot-pos(C) and remaining-cells(G,N1)  ) and (( false  ))'
	#from tools import transform
	s = transform(s)
	print(reduce(s, 3))
	# with open('groundOutput.txt', 'r') as f:
	# 	with open('bddInput.txt', 'w') as f2:
	# 		f2.write(reduce(f.read(), 5))