#Compilador A-LISON 
#Main
#Arturo Rojas Ortiz
#Eduardo Mancilla de la Cruz

import ply.lex as lex
import ply.yacc as yacc
from objects import Structs
import re
import codecs
import os
import sys
import csv



flagCompiles = True

reserved = {
	'startprog' 	: 'STARTPROG',
	'endprog' 		: 'ENDPROG',
	'routine' 		: 'ROUTINE',
	'vars' 			: 'VARS',
	'endvars' 		: 'ENDVARS',
	'main' 			: 'MAIN',
	'report' 		: 'REPORT',
	'loop' 			: 'LOOP',
	'if' 			: 'IF',
	'else'			: 'ELSE',
	'int' 			: 'INT',
	'double' 		: 'DOUBLE',
	'char' 			: 'CHAR',
	'string' 		: 'STRING',
	'input'			: 'INPUT',
	'output'		: 'OUTPUT',
	# 'sum'			: 'SUM',
	# 'min'			: 'MIN',
	# 'max'			: 'MAX',
	# 'txtcol'		: 'TXTCOL',
	# 'match'			: 'MATCH',
	 'return'		: 'RETURN',
	# 'addcol'		: 'ADDCOL',
	# 'delcol'		: 'DELCOL',
	# 'modcol'		: 'MODCOL',
	# 'exportcsv'	: 'EXPORTCSV',
	# 'importcsv'	: 'IMPORTCSV',
	'int' 			: 'INT',
	'double' 		: 'DOUBLE',
	'bool' 			: 'BOOL',
	'char' 			: 'CHAR',
	'string' 		: 'STRING'
}

tokens = ['COMMA', 'NOT', 'SEMICOLON', 'ASSIGN', 'L_PAREN', 'R_PAREN', 'L_CURLY', 'R_CURLY', 'L_BRKT', 'R_BRKT', 'PLUS', 'MINUS', 'MULT', 'DIV', 'GREATER', 'LESS', 'EQUAL', 'GREATEREQUAL', 'LESSEQUAL', 'NOTEQUAL', 'AND', 'OR', 'V_INT', 'V_DOUBLE', 'V_BOOL', 'V_CHAR', 'ID']  + list(reserved.values())


t_ignore = " \t"

t_COMMA = r','
t_SEMICOLON = r';'
t_NOT = r'!'
t_L_PAREN = r'\('
t_R_PAREN = r'\)'
t_L_CURLY = r'\{'
t_R_CURLY = r'\}'
t_L_BRKT = r'\['
t_R_BRKT = r'\]'
t_ASSIGN = r'\=' 
t_PLUS = r'\+'
t_MINUS = r'-'
t_DIV = r'\/'
t_MULT = r'\*'
t_GREATER = r'>'
t_LESS = r'<'
t_EQUAL = r'=='
t_GREATEREQUAL = r'>='
t_LESSEQUAL = r'<='
t_NOTEQUAL = r'!='
t_AND = r'&&'
t_OR = r'\$\$'
t_V_INT = r'[0-9]+'
t_V_DOUBLE = r'[0-9]+\.[0-9]+'
t_V_CHAR = r'\'[a-zA-Z0-9 ]\''

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value,'ID')
    return t

def t_COMMENT(t):
	r'\#.*'
	pass

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
	print ("Illegal token '%s'" % t.value[0])
	flagCompiles = False
	t.lexer.skip(1)

lexer = lex.lex()

def p_program(p):
	'program : r1 STARTPROG vars r4 routines main ENDPROG'

def p_r1(p):
	'r1 : '
	Structs.scope = "global"
	Structs.routine = {
						"name" : "startprog",
						"params" : 0,
						"paramTypes" : [],
						"return" : "void"
 	}

def p_r4(p):
	'r4 : '
	Structs.scope = "local"
	Structs.routine["symTable"] = Structs.symbolTable
	Structs.symbolTable
	Structs.dirRoutines.append(Structs.routine)

def p_vars(p):
	'vars : VARS decvars ENDVARS'

def p_decvars(p): 
	'''decvars : type r2 dim1array decassign SEMICOLON r3 decvars
			   | empty'''

def p_r2(p):
	'r2 : ID'
	name = p[1]
	Structs.var = {
					"name" : p[1],
					"scope" : Structs.scope,
					"value" : None
	}
	a= 2

def p_r3(p):
	'r3 : '
	Structs.symbolTable.append(Structs.var)
	Structs.var = {}

def p_dim1array(p):
	'''dim1array : L_BRKT V_INT R_BRKT dim2array
				 | empty'''

def p_dim2array(p):
	'''dim2array : L_BRKT V_INT R_BRKT
				 | empty'''

def p_decassign(p):
	'''decassign : ASSIGN assignvalue
				 | empty'''

def p_assignvalue(p): 
	'''assignvalue : constant
				   | assignarray
				   | empty'''

def p_assignarray(p):
	'''assignarray : L_BRKT assignarray2 R_BRKT
				   | empty'''

def p_assignarray2(p):
	'''assignarray2 : assignarray3
				    | assignarray5'''

def p_assignarray3(p):
	'''assignarray3 : constant assignarray4
				    | empty'''

def p_assignarray4(p):
	'''assignarray4 : COMMA assignarray3
				    | empty'''

def p_assignarray5(p):
	'''assignarray5 : L_BRKT assignarray6 R_BRKT assignarray8'''

def p_assignarray6(p):
	'''assignarray6 : assignarray7
					| empty'''

def p_assignarray7(p):
	'''assignarray7 : COMMA assignarray6
					| empty'''

def p_assignarray8(p):
	'''assignarray8 : COMMA assignarray5
					| empty'''
def p_routines(p):
	'''routines : decroutine routines
				| empty'''

def p_decroutine(p):
	'decroutine : ROUTINE dectype ID L_PAREN params R_PAREN L_CURLY vars block R_CURLY'
	Structs.scope = "global"
	Structs.routine = {
						"name" : p[3],
						"params" : 0,
						"paramTypes" : [],
						"return" : p[3]
    }
	Structs.dirRoutines.append(Structs.routine)
def p_routinecall(p):
	'routinecall : ID L_PAREN paramcall R_PAREN'

def p_paramcall(p):
	'''paramcall : expression paramcall2
				 | empty'''

def p_paramcall2(p):
	'''paramcall2 : COMMA paramcall
				  | empty'''

def p_dectype(p):
	'''dectype : type
			   | empty'''

def p_params(p):
	'''params : type ID params2
			  | empty'''

def p_pararms2(p):
	'''params2 : COMMA type ID params2
			   | empty'''

def p_main(p):
	'main : MAIN L_CURLY vars block R_CURLY'


def p_constant(p):
	'''constant : V_INT
				| V_DOUBLE
				| V_CHAR
				| V_BOOL'''
	value = p[1]
	Structs.var["value"] = value

def p_decid(p):
	'decid : ID decid2'

def p_decid2(p):
	'''decid2 : L_BRKT expression R_BRKT decid3
			  | empty'''

def p_decid3(p):
	'''decid3 : L_BRKT expression R_BRKT 
			  | empty'''

def p_type(p):
	'''type : INT
			| DOUBLE
			| CHAR
			| BOOL
			| STRING'''



def p_block(p):	
	'''block : loop 
			 | condition
			 | assignvalue SEMICOLON
			 | input SEMICOLON
			 | output SEMICOLON
			 | return SEMICOLON
			 | empty
''' 

def p_loop(p):
	'loop : LOOP L_PAREN expression R_PAREN'

def p_condition(p):
	'condition : IF L_PAREN expression R_PAREN L_CURLY block R_CURLY else' 

def p_else(p):
	'''else : ELSE L_CURLY block R_CURLY
		  | empty'''

def p_input(p):
	'input : INPUT L_PAREN expression R_PAREN'

def p_output(p):
	'output : OUTPUT L_PAREN expression R_PAREN'

def p_return(p):
	'return : RETURN expression'
def p_expression(p):
	'expression : relational addlogic'

def p_addlogic(p):
	'''addlogic : AND expression
				| OR expression
				| empty'''

def p_relational(p):
	'relational : mathsum addrelational'

def p_addrelational(p):
	'''addrelational : GREATER
					 | LESS
					 | EQUAL
					 | GREATEREQUAL
					 | LESSEQUAL
					 | NOTEQUAL
					 | empty'''

def p_mathsum(p):
	'mathsum : mathmult addmathsum'

def p_addmathsum(p):
	'''addmathsum : PLUS
				  | MINUS
				  | empty'''

def p_mathmult(p):
	'mathmult : prefactor addmathmult'

def p_addmathmult(p):
	'''addmathmult : MULT
				  | DIV
				  | empty'''

def p_prefactor(p):
	'prefactor : negativefactor factor'

def p_negativefactor(p):
	'''negativefactor : NOT
					  | empty'''

def p_factor(p):
		'''factor : decid
				  | constant
				  | L_PAREN expression R_PAREN
				  | routinecall'''

def p_empty(p):
	'empty :'
	pass


parser = yacc.yacc()

filename = "testfiles/prueba2.txt"
fp = codecs.open(filename,"r")
nextline = fp.read()
fp.close()
lexer.input(nextline)

parser.parse(nextline)


while True:
	tok = lexer.token()
	if not tok : break
	print(tok)

if flagCompiles == False: 
	print("No compila")

print(Structs.dirRoutines)

	