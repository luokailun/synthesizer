

# for rules

import re

str_rule4 = r"(?<=(Poss\b|Init\b))\((.*?)\)\s*<=>(.+?)(?=Poss\b|SSA\b|Init\b|End\b|Win\b|;|Basic\b)"
str_rule3 = r"(?<=(Win\b|SSA\b|End\b))\((.*?)\)\s*<=>(.+?)(?=Poss\b|SSA\b|Init\b|End\b|Win\b|;|Basic\b)"
str_rule5 = r"(?<=(Basic\b))\((.* ?)\)\s*<=>(.+?)(?=Poss\b|SSA\b|Init\b|End\b|Win\b|;|Basic\b)"


str_const_name = r"(?:[a-z\d][\w]*)"    
str_var_name = r"(?:[A-Z][\d]*)"
str_pred_name = r"(?:[A-Z][\w]*)"
str_symbol = r"(?P<name>"+ str_const_name+"|"+str_var_name+"|"+str_pred_name+")"


str_eqfunction = r"(%s)\(((?:%s|%s|,)*)\)\s*=\s*((?:%s|%s))"%(str_const_name,str_const_name,str_var_name,str_const_name,str_var_name)
str_predicate = r"(%s)\(((?:%s|%s|,)*)\)"%(str_pred_name,str_const_name,str_var_name)
str_fluent = r"(?:%s|%s)"%(str_eqfunction,str_predicate)

str_action = r"(%s)\(((?:%s|%s|,)*)\)"%(str_const_name,str_const_name,str_var_name)




str_inner_parenth = r"\([^\(\)]*\)"




rule4 = re.compile(str_rule4)
rule3 = re.compile(str_rule3)
rule5 = re.compile(str_rule5)

##
symbol = re.compile(str_symbol)
var = re.compile(str_var_name)


fluent = re.compile(str_fluent)
action = re.compile(str_action)


inner_parenth = re.compile(str_inner_parenth)


#print action.match('eat(P,I,J)').groups()

#notlogic_pattern_str = r"(?:(?:(?<!&)(?<!|)(?<!=>).(?!&)(?!|)(?!=>))+)"
#function_pattern_str = r"([\w\d]+?)\(((?:(?<!=).)*)\)(?:=(" +notlogic_pattern_str + "))?"
#function_pattern = re.compile(function_pattern_str)

