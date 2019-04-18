import ply.yacc as yacc
import os
import codecs
import re
import sys
from lexer import tokens

#precedence = ()

def p_program(p):
	'program : R_STARTPROG vars ROUTINES main R_ENDPROG'

def vars(p):
	'''vars : var R_VARS
			| e'''

def routines(p):
	''' routines : routine R_ROUTINE
			| e'''

def main(p):
	'main : R_MAIN T_LBRKT block T_RBRKT'

def var(p):
	'var : R_VAR type declareArray id'

def declareArray(p): 
	'declareArray : L'
def routine(p):

def parameters(p):

def block(p):

def type(p):





def p_error(p):

filename = "pruebas/prueba1.txt"
fp = codecs.open(filename,"r","utf-8")
nextline = fp.read()
fp.close()

parser = yacc.yacc()
result = parser.parse(nextline)

print result





