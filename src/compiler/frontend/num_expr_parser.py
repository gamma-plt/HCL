# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import re
import sys
import codecs


regex = {'plus':r'^[+]$', 'minus':r'^[-]$', 'left_parenthesis':r'^[(]$',
          'right_parenthesis':r'^[)]$', 'times':r'^[*]$', 'division':r'^[/]$', 'num':r'^\d+[.]?\d*$',
          'var':r'^[a-zA-Z_]\w*$'}

class Token(object):
   def __init__(self, token, value):
       self.token = token
       self.value = value
   def __unicode__(self):
       return u'<'+self.token+u', '+self.value+u'>'
   def __str__(self):
       return self.__unicode__().encode('utf-8')
   def __repr__(self):
       return self.__str__()


def remove_trailing_spaces(s):
    init_idx = None
    end_idx = 0
    for i,c in enumerate(s):
        if len(re.findall('\s', c)) > 0:
           pass
        else:
           if init_idx is None:
              init_idx = i
           else:
              end_idx = i
    comp = ''
    if init_idx is not None:
       comp = s[init_idx:end_idx+1]
    return comp

def lex(line):
    status_code = 0
    tokens = []
    word = ''
    last_id = None
    i = 0
    while i < len(line):
       c = line[i]
       if len(re.findall(r'\S', c)) > 0:
          word += c
          match_found = False
          for name in regex:
              if len(re.findall(regex[name], word)) > 0:
                 match_found = True
                 break
          if match_found:
             last_id = name
          else:
             if last_id is not None:
                word = word[:-1]
                tokens.append(Token(last_id, word))
                word = ''
                last_id = None
                i -= 1
             else:
                print("Input: %s\nSyntax Error: Unrecognized or invalid symbol: %s at Position : %d" % (line, word, i+1), file=sys.stderr)
                status_code = -1
       else:
          if last_id is not None:
             tokens.append(Token(last_id, word))
          word = ''
          last_id = None
       if i == len(line) - 1:
          if last_id is not None:
             tokens.append(Token(last_id, word))
       i += 1
    return status_code, tokens

def parse(tokens):
    LL = {'E':{'num':lambda x:"TA", 'var':lambda x:"TA", 'left_parenthesis':lambda x:"TA"},
          'T':{'num':lambda x:"FB", 'var':lambda x:"FB", 'left_parenthesis':lambda x:"FB"},
          'F':{'num':lambda x:x, 'var':lambda x:x, 'left_parenthesis':lambda x:"(E)", 'minus':lambda x:'-F'},
          'A':{'plus':lambda x: "+TA", 'minus':lambda x: "-TA", 'left_parenthesis':lambda x:'', 
               'right_parenthesis':lambda x:'', '$':lambda x:''},
          'B':{'times':lambda x:'*FB', 'division':lambda x:'/FB', 'left_parenthesis':lambda x:'', 
               'right_parenthesis':lambda x:'', 'plus':lambda x:'', 'minus':lambda x:'', '$':lambda x:''}}
    state_stack = 'E$'
    while len(tokens) > 0 and state_stack[0] != '$':
       print("%-44s   %-44s" % (reduce(lambda x, y: x+str(y.value), tokens, ''), state_stack))
       rule = state_stack[0]
       tok = tokens[0]
       try:
          subs = LL[rule][tok.token](tok.value)
          if subs == tok.value:
             state_stack = state_stack[1:]
             tokens.pop(0)
          elif subs == '':
             state_stack = state_stack[1:]
          else:
             state_stack = subs + state_stack[1:]
       except KeyError:
          if rule not in LL.keys() and rule == tok.value:
             state_stack = state_stack[1:]
             tokens.pop(0)
             continue
          else:
             print("Input: %s\nSyntax Error: Invalid symbol: %s" % (reduce(lambda x, y: x+str(y.value), tokens, ''), tok.value), file=sys.stderr)








#S  → E
#E → TE'
#E' → + T | - T | epsilon
#T → FT'
#F → -F | (E) | NV
#NV → num | var
