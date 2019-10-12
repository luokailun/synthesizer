#-*- coding:utf8 -*-
# z3 version 4.8.4
# By lijian
#coding=utf-8
import itertools
import re
constlist = {}
mathlogic = ['+','-','*','/','>=','<=','<','>','mod']
and_or = ['and','or']

def  z3list(results):             #用来返回z3定理证明器的每一个（define-fun *)
    z3data = []
    item = ''
    #with open('output') as z3output:   #打开z3的输出文件
    #    z3li = z3output.readlines()             #按行读取
    for line in results:
        #print 'kkk', line
        if ''.join(line.split()) == ")":          #处理最后一行
            item = ' '.join(item.strip().replace('!','').replace('\n','').split())    #剔除感叹号与多余的空格
            z3data.append(item)
            break
        if 'define-fun' in line or 'declare-fun' in line:
            #print '???', line
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




def parsebody(body):
    num = numberitem(body)        #函数体的项数
    type = z3item(body,1)           #函数体的类型
    if type == 'ite':
        #print 'type1'
        #exit(0)
        return ite(body)
    if type == 'let':
        #print 'type2'
        #exit(0)
        return let(body)
    if type in mathlogic: 
        #print 'type3'
        #exit(0)
        if type == 'mod':
            return "(%s)%(%s)"%(parsebody(z3item(body,2)), parsebody(z3item(body,3)))
        elif type == '-':
            if num <= 3:
                return '-' + parsebody(z3item(body,2))
            else:
                return ' - '.join("(" + parsebody(z3item(body,i)) + ")" for i in range(2,num))
        else:
            return (" " + type + " ").join("(" + parsebody(z3item(body,i))+")" for i in range(2,num))
    if type == '=':
        return '(%s) == (%s)'%(parsebody(z3item(body,2)), parsebody(z3item(body,3)))
    if type == 'or':
        return ' or '.join(['( %s )'%parsebody(z3item(body,i)) for i in range(2,num)])
    if type == 'and':
        return ' and '.join(['( %s )'%parsebody(z3item(body,i)) for i in range(2,num)])
    else:  
        #其他类型有 ： 不含括号字符串 abx0/123 , (p x) ,p(x y),(p x y z ....)
        if num <= 2:          #不含括号
            return body
        else:
            bodys = z3item(body, 1) + '('
            for i in range(2, num):
                bodys = bodys + parsebody(z3item(body, i)) + ','
            bodys = bodys[0:len(bodys) - 1] + ")"
        return bodys

'''
body = "(= (ite (= x0 _S1val0) _S1val0 _S1val1) _S1val0)"
print parsebody(body)
'''



def parseArg(args):
    args = args[2:len(args)-2]
    argsli = args.split(") (")
    argsli2 = []
    for a in argsli:
       templi = a.split(' ')
       argsli2.append(templi[0])
    return argsli2



def parsefun(oneline):
    name = z3item(oneline,2)
    argslist = parseArg(z3item(oneline,3))             #分解参数
    args = ','.join(arg for arg in argslist)
    body = parsebody(z3item(oneline,5))             #分解函数体
    return name + "=lambda " + args +": " + body



def parse_declarefun(oneline, valuecharlist):
    fun = ''
    funname = z3item(oneline,2)                 #第二项为函数名字
    funargs = z3item(oneline,3)                 #第三项为函数的参数列表
    #print funbody
    if '()' == funargs: 
        valuecharlist.append(funname)



def parseZ3fun(oneline, valuecharlist):                     #把一个define-fun进行分解
    fun = ''
    funname = z3item(oneline,2)                 #第二项为函数名字
    funargs = z3item(oneline,3)                 #第三项为函数的参数列表
    funbody = z3item(oneline,5)                 #第五项为函数体
    #print funbody
    if '()' == funargs and not funbody.startswith('('):    #零元函数为常量，存放在一个字典里

        if not funbody.isdigit():
            #print funbody                              #函数体不是数字
            valuecharlist.append(funname)
            valuecharlist.append(funbody)
            constlist[funname] = funbody
        else:
            constlist[funname] = int(funbody)
    else:
        fun = parsefun(oneline).replace('true',"True").replace('false',"False")        #不是零元函数，进一步分解
        #print(fun)
    return fun



################################################################################################################################

def get_fun(results):
    funlist = []
    fun_list = []
    valuecharlist = []

    for line in z3list(results):
        if line.find('define-fun')!=-1:
            fun = parseZ3fun(line, valuecharlist)
            if fun!='':
                funlist.append(fun)
        elif line.find('declare-fun')!=-1:
            parse_declarefun(line, valuecharlist)
    charset = set(valuecharlist)
    for fun in funlist:
        for valuechar in charset:
            if valuechar not in ['true','false']:
                #把已经成型的lambda表达式中的字符加引号，如 a 变 ‘a'
               fun = re.sub(r'\b' + valuechar + r'\b',"'" + valuechar + "'",fun)                           
        fun_list.append(fun)
    return fun_list


def get_const(results):
    for line in z3list(results):
        if line.find('define-fun')!=-1:
            parseZ3fun(line, list())
    return constlist

if __name__ == '__main__':
    result = ['sat\n', '(model \n', '  ;; universe for _S1:\n', '  ;;   _S1!val!1 _S1!val!0 \n', '  ;; -----------\n', '  ;; definitions for universe elements:\n', '  (declare-fun _S1!val!1 () _S1)\n', '  (declare-fun _S1!val!0 () _S1)\n', '  ;; cardinality constraint:\n', '  (forall ((x _S1)) (or (= x _S1!val!1) (= x _S1!val!0)))\n', '  ;; -----------\n', '  (define-fun p1 () _S1\n', '    _S1!val!0)\n', '  (define-fun p2 () _S1\n', '    _S1!val!1)\n', '  (define-fun xlen () Int\n', '    2)\n', '  (define-fun ylen () Int\n', '    2)\n', '  (define-fun True () Bool\n', '    false)\n', '  (define-fun False () Bool\n', '    false)\n', '  (define-fun turn ((x!0 _S1)) Bool\n', '    (ite (= x!0 _S1!val!1) false\n', '      true))\n', '  (define-fun Ch ((x!0 Int) (x!1 Int)) Bool\n', '    (let ((a!1 (ite (<= 0 x!0) (ite (<= 1 x!0) (ite (<= 2 x!0) 2 1) 0) (- 1)))\n', '          (a!2 (ite (<= 0 x!1) (ite (<= 1 x!1) (ite (<= 2 x!1) 2 1) 0) (- 1))))\n', '      (or (and (= a!1 0) (= a!2 1))\n', '          (and (= a!1 1) (= a!2 0))\n', '          (and (= a!1 0) (= a!2 0))\n', '          (and (= a!1 1) (= a!2 1)))))\n', ')\n']
    print get_fun(result)

