# -*- coding: iso-8859-15 -*-

import re
import os
import sys

regex = {'if':r'^if$', 'fi':'^fi$' 'begin':r'^begin$', 'end':r'^end$', 
         'do':'do', 'od':'od', 'for':'^for$', 'rof':'^rof$', 'abort':'^abort$', 'skip':'^skip$', 
         'array':'^array$', 'of':'^of$', 'name':r'^[a-zA-Z_]\w*$',
         'number':r'-?\d+(.\d+)?', 'eq':r'^[=]$', 'leq':r'^≤$', 'geq':u'^≥$',
         'le':r'^[<]$', 'ge':r'^>$', 'plus':r'^[+]$', 'minus':'^[-]$', 'times':'^[*]$',
         'div':'^[/]$', 'neq':u'^≠$', 'not':u'^¬$' 'and':u'^∧$', 'or':u'^∨$', 'in':u'^∈$', 
         'not_in':u'^∉$', 'union':u'^∪$', 'intersection':u'∩', 'infty':u'^∞$',
         'empty':u'^∅$', 'guard_sep':u'^□$', 'left_rparen':r'^[(]$',
         'right_rparen':r'^[)]$', 'left_rparen':r'^[[]$', 'right_rparen':r'^[]]$'}

keywords = ['begin', 'end', 'if', 'fi', 'do', 'od', 'in', 'for', 'rof']

class Token(object):
   def __init__(self, token, value):
       self.token = token
       self.value = value

   def __str__(self):
       return self.__repr__()

   def __repr__(self):
       return '<%s, %s>' % (self.token, self.value)

def lex()

if __name__ == '__main__':
   


