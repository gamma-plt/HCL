# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import re
import sys
import lexer
import ll_table as LLT

GRAMMAR_PATH = '../../../doc/language/LL_Grammar_Description.txt'

def equiv(sym, reverse):
    f = True
    try:
      n = lexer.keywords[sym]
    except KeyError:
      f = False
    if not f:
      try:
        n = lexer.regex[sym]
        n = sym
        f = True
      except KeyError:
        f = False
    if not f:
       for r in reverse:
           if len(re.findall(r, sym)) > 0:
              n = reverse[r]
              f = True
              break
    return n

def parse(path):
    tokens, status_code = lexer.lex(path)
    if status_code != 0:
       print("Compiler exited with status -1", file=sys.stderr)
       sys.exit(-1)
    reverse = dict(zip(lexer.regex.values(), lexer.regex.keys()))
    G, FNE, FLL, LL = LLT.LL(GRAMMAR_PATH)
    tab = {}
    for rule in LL:
        tab[rule] = {}
        for sym in LL[rule]:
            f = True
            n = equiv(sym, reverse)
            l = []
            for s in LL[rule][sym]:
                if s in LL.keys():
                   l.append(s)
                else:
                   l.append(lexer.Token(equiv(s, reverse), s))
            tok = lexer.Token(n, sym)
            tab[rule][tok] = l
    status_code = 0
    stack = ['P']
    last_evaluation = None
    while len(stack) > 0:
       if len(tokens) > 5:
          s = ' '.join([i.value for i in tokens[0:5]]) + ' ... '+tokens[-1].value
       else:
          s = ' '.join([i.value for i in tokens])
       if len(stack) > 5:
          s += '\n'+' '.join([i.value if isinstance(i, lexer.Token) else i for i in stack[0:5]]) + ' ... '+stack[-1].value
       else:
          s += '\n'+' '.join([i.value if isinstance(i, lexer.Token) else i for i in stack])
       print(s+'\n')
       if isinstance(stack[0], unicode) or isinstance(stack[0], str):
          try:
             trans = tab[stack[0]][tokens[0]]
             stack = trans + stack[1:]
          except KeyError:
             print("File: %s\nSyntax Error: Unexpected symbol: %s; Expected: %s" % (path, tokens[0].value, ', '.join([i.value for i in tab[stack[0]].keys()])), file=sys.stderr)
             break
       else:
          if tokens[0] == stack[0]:
             last_evaluation = tokens[0].value
             tokens = tokens[1:]
             stack = stack[1:]
          else:
             print("File: %s\nSyntax Error: Unexpected symbol: %s; Expected: %s" % (path, tokens[0].value, stack[0].value), file=sys.stderr)
             break






