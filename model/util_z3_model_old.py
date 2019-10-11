#-*- coding:utf8 -*-
# z3 version 4.6.x
# By lijian
#coding=utf-8
import itertools
import re
constlist = {}
valuecharlist = []
mathlogic = ['+','-','*','/','>=','<=','<','>','mod']
and_or = ['and','or']

def  z3list(results):             #用来返回z3定理证明器的每一个（define-fun *)
    z3data = []
    item = ''
    #with open('output') as z3output:   #打开z3的输出文件
    #    z3li = z3output.readlines()             #按行读取
    for line in results:
        if ''.join(line.split()) == ")":          #处理最后一行
            item = ' '.join(item.strip().replace('!','').replace('\n','').split())    #剔除感叹号与多余的空格
            z3data.append(item)
            break
        if 'define-fun' in line:
            if '' != item:
                item = ' '.join(item.strip().replace('!','').replace('\n','').split())
                z3data.append(item)
            item = line
        elif not ''.endswith(item):
            item = item + line
    return z3data                             #返回一个列表，每一项是一个（define-fun *)


def nextpart(oneline,index):                      #此方法与z3item(oneline,num)为了把一个括号内容拆分成多项比如（A B C）拆分为三项
    result = ''
    if index >= len(oneline):
        return ''
    if oneline[index] == '(':
        bracket = 1
        result = result + oneline[index]
        while bracket > 0:
            index = index + 1
            if oneline[index] == '(':
                bracket = bracket + 1
            if oneline[index] == ')':
                bracket = bracket - 1
            if 0!= bracket:
                result = result + oneline[index]
        result = result + oneline[index]
    else:
        while index < len(oneline) and oneline[index] != ' ':
            result = result + oneline[index]
            index = index + 1
    return result



def z3item(oneline,num):                #oneline 为需要拆分的内容如（A B C),num为第几项
    oneline = oneline[1:len(oneline)-1]
    index = 0
    for i in range(1,num):
        index = index + len(nextpart(oneline,index)) + 1
    return nextpart(oneline,index)

def parseZ3fun(oneline):                     #把一个define-fun进行分解
    fun = ''
    funname = z3item(oneline,2)                 #第二项为函数名字
    funargs = z3item(oneline,3)                 #第三项为函数的参数列表
    funbody = z3item(oneline,5)                 #第五项为函数体
    if '()' == funargs and not funbody.startswith('('):    #零元函数为常量，存放在一个字典里
        if not funbody.isdigit():
            #print funbody                              #函数体不是数字
            valuecharlist.append(funbody)
            constlist[funname] = funbody
        else:
            constlist[funname] = int(funbody)
    else:
        fun = parsefun(oneline).replace('true',"True").replace('false',"False")        #不是零元函数，进一步分解
        #print(fun)
    return fun

def parsefun(oneline):
    name = z3item(oneline,2)
    argslist = parseArg(z3item(oneline,3))             #分解参数
    args = ','.join(arg for arg in argslist)
    body = parsebody(z3item(oneline,5))             #分解函数体
    return name + "=lambda " + args +": " + body

def parsebody(body):
    num = numberitem(body)        #函数体的项数
    type = z3item(body,1)           #函数体的类型
    if type == 'ite':
        return ite(body)
    if type == 'let':
        return let(body)
    if type in mathlogic:
        if type == 'mod':
            return parsebody(z3item(body,2)) + '%' + parsebody(z3item(body,3))
        elif type == '-':
            if num <= 3:
                return '-' + parsebody(z3item(body,2))
            else:
                return ' - '.join("(" + parsebody(z3item(body,i)) + ")" for i in range(2,num))
        else:
            return (" " + type + " ").join("(" + parsebody(z3item(body,i))+")" for i in range(2,num))
    else:           #其他类型有 ： 不含括号字符串 abx0/123 , (p x) ,p(x y),(p x y z ....)
        if num <= 2:          #不含括号
            return body
        else:
            bodys = z3item(body, 1) + '('
            for i in range(2, num):
                bodys = bodys + parsebody(z3item(body, i)) + ','
            bodys = bodys[0:len(bodys) - 1] + ")"
        return bodys

def ite(body):             #分解(ite (and (= x1 1) (= x2)) 1 2)
    condition = z3item(body,2)           #第二部分为条件
    condition = parsecondition_1(condition)
    valuebody1 = z3item(body,3)          #第三四部分为值
    valuebody2 = z3item(body,4)
    if valuebody1.startswith('('):         #值如果以括号起始，说明是复杂的表达式，需要进一步分解
        valuebody1 = parsebody(valuebody1)
    if valuebody2.startswith('('):
        valuebody2  = parsebody(valuebody2)
    return valuebody1 + ' if ' + condition + ' else ' + valuebody2

def parsecondition_1(condition):
    conditions = ''
    type = z3item(condition,1)
    if type in and_or:
       number = numberitem(condition)
       for i in range(2,number):
           conditions = conditions + parsecondition_2(z3item(condition,i)) + ' ' + type + ' '
       if type == 'and':
           conditions = conditions[0:len(conditions)-5]
       else:
           conditions = conditions[0:len(conditions) - 4]
    else:
       conditions = parsecondition_2(condition)
    return conditions

def parsecondition_2(condition):
    num = numberitem(condition)
    if num <= 3:
        if z3item(condition,1) == 'not':
            return 'not ' + parsecondition_2(z3item(condition,2))
        elif num == 3:
            return z3item(condition,1) + '(' + z3item(condition,2) + ')'
        elif num == 0 :
            return condition + '()'
    elif num == 4:
        if z3item(condition,1) == '=':
            return parsebody(z3item(condition,2)) + ' == ' + parsebody(z3item(condition,3))
        elif z3item(condition,1) in mathlogic:
            return parsebody(z3item(condition,2)) + " " +z3item(condition,1) + " " + parsebody(z3item(condition,3))
        else:
            return z3item(condition,1) + '(' + parsebody(z3item(condition,2)) + ' , ' + parsebody(z3item(condition,3)) + ' )'
    else:
        conditions = z3item(condition,1) + '('
        for i in range(2,num):
            conditions = conditions + parsebody(z3item(condition,i)) + ','
        conditions = conditions[0:len(conditions)-1] + ')'
        return conditions


def numberitem(content):
    number = 0
    while z3item(content,number) != '':
        number = number + 1
    return number

def let(body):
    letfun = z3item(body, 2)
    letfunbody = z3item(body, 3)
    letsize = numberitem(letfun)
    for i in range(1, letsize):
        tempfun = z3item(letfun, i)
        funname = z3item(tempfun, 1)
        funbody = z3item(tempfun, 2)
        #funbody = '( ' + parsebody(funbody) + ' )'
        #letfunbody = letfunbody.replace(funname, funbody)
        letfunbody = re.sub(r"\b%s\b"%funname, funbody, letfunbody)
    return parsebody(letfunbody)

def parseArg(args):
    args = args[2:len(args)-2]
    argsli = args.split(") (")
    argsli2 = []
    for a in argsli:
       templi = a.split(' ')
       argsli2.append(templi[0])
    return argsli2

def get_fun(results):
    funlist = []
    fun_list = []
    for line in z3list(results):
        #print line
        if parseZ3fun(line) != '':
            funlist.append(parseZ3fun(line))
    charset = set(valuecharlist)
    for fun in funlist:
        for valuechar in charset:
            if valuechar not in ['true','false']:
               fun = re.sub(r'\b' + valuechar + r'\b',"'" + valuechar + "'",fun)                           #把已经成型的lambda表达式中的字符加引号，如 a 变 ‘a'
        fun_list.append(fun)
    return fun_list

def get_const(results):
    for line in z3list(results):
        parseZ3fun(line)
    return constlist

'''
with open("2",'read') as mflie:
    print parsebody(mflie.readlines())
'''

#for fun in get_fun(results):
#   exec(fun)

'''
def get_small_models(fun_list,preds_list,const_list,results):
    conslists = get_const(results)
    funAndarg = {}
    initN = 3 #conslists['initN']
    initN_num = [str(i) for i in range(1,initN+1)]
    funlist = get_fun(results)
    #用来存储给函数变量赋值之后的函数形式如：[f(1,1)=a,f(1,2)=b,f(2,1)=c,f(2,2)=d]
    for fun in funlist:
       exec(fun)
    dic = {}
    for fun in funlist:
        fun = fun[0:fun.find(':')].replace('=lambda', '')
        funtemp = fun.split(' ')
        funAndarg[funtemp[0]] = funtemp[1].split(',')
    for funname in funAndarg.keys():
        if funname in fun_list or funname in preds_list:
            length  = len(funAndarg[funname])
            num_list_per = list(itertools.product(initN_num,repeat = length))
            num_list_per = [list(temp) for temp in num_list_per]
            for num_list in num_list_per:
                #funAndarg[funname] = num_list
                funvalue = funname + "(" + ','.join(arg for arg in num_list) + ")"
                dic[funvalue] = eval(funvalue)
    #return dict(dic.items() + conslists.items())
    return dic

fun_list = ['numStone']
preds_list = ['turn']
const_list = ['p2','p1','numStone']

def get_fun_dict(fun_list,preds_list,const_list,results):
    fun_dict = get_small_models(fun_list,preds_list,const_list,results)
    const_dict = get_const(results)
    for fun_key in fun_dict.keys():
        for const_key in const_dict.keys():
            if fun_dict[fun_key] == const_dict[const_key] and type(fun_dict[fun_key]) == str and const_key in const_list:
                fun_dict[fun_key] = const_key
    return fun_dict
'''
#print get_fun_dict(fun_list,preds_list,const_list)
#print get_const()