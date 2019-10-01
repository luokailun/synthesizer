

from basic import Util
from basic import context_operator
import re
import itertools
var_pattern_str = r"(?:\b[A-Z][\d]+\b)"
var_pattern = re.compile(var_pattern_str)



##############################################################################################################################################################


def find_var(pred):
	var_list =[ var for var in var_pattern.findall(pred) if var not in context_operator.get_predicates() ]
	return (var_list, pred)


def is_var(pred):
	if var_pattern.search(pred):
		return True
	else:
		return False

def find_var_sort(var_list, sort_consts):
	return [ sort for var in var_list for sort, consts in sort_consts.iteritems() if var in consts ]
	

##############################################################################################################################################################



def __compress(xlist, ylist):
	#print xlist, ylist
	mxlist, mylist = list(),list()
	for e in range(0,len(xlist)):
		if xlist[e] not in mxlist:
			mxlist.append(xlist[e])
			mylist.append(ylist[e])
	#print mxlist,mylist
	return (mxlist, mylist)



def __replace_var(var_str, t, var):
	for new_var in t:
		var_str = re.sub(var+r'\b',new_var, var_str, 1)
	return var_str


def __replace_body(old_list, new_list, body):
	old_list = [ r'\b'+elem+r'\b' for elem in old_list]
	return Util.repeat_do_function(lambda x,y: re.sub(y[0],y[1],x,1), zip(old_list, new_list),body)


def ____recolour(mtuple, colors,var):
	n = 0
	mdict = dict()
	mlist = list()
	for e,elem in enumerate(mtuple):
		if elem in mdict.keys():
			mlist.append(var+str(mdict[elem]))
		else:
			mlist.append(var+str(colors[n]))
			mdict[elem] = colors[n]
			n+=1
	return tuple(mlist)


def __gen_template(num, var):
	var = var.replace('X','Y')
	templates =  list(itertools.product(range(0,num), repeat=num))
	templates = [ ____recolour(elem,range(0,num),var) for elem in templates]
	return list(set(templates))


def devars(pred):
	var_list, sort_list, body  = pred
	if var_list == list():
		return [pred]
	visited = list()
	var_template_list = ['#'.join(var_list)]

	for var in var_list:
		num = var_list.count(var)
		if var in visited or num ==1:
			continue
		else:
			visited.append(var)
			templates = __gen_template(num, var)
			var_template_list = [ __replace_var(var_str, t, var) for var_str in var_template_list for t in templates ]
	temp_pred_list = [(t.split('#'), sort_list, body) for t in var_template_list ]
	temp_pred_list = [( __compress(new_var_list, sort_list), __replace_body(var_list, new_var_list,body)) for (new_var_list, sort_list,body) in temp_pred_list ]
	
	return [ (var_list, sorts, body) for (var_list, sorts),body in temp_pred_list]

#print 'final!!!!',__devars((['X','X','X'], ['Int','Int','Int'], 'hello'))


##############################################################################################################################################################