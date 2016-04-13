# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import re
import sys
import parser

VAR = u'VAR'
OP = u'name'
COMMA = u'comma'
ARRAY = u'ARRAY'
NUM = u'number'
COMMA = u'comma'
DO = u'DO'

def analyse(path):
    tree, status_code = parser.parse(path)
    if status_code != 0:
       print("Compiler exited with status %d" % (status_code), file=sys.stderr)
       return None, status_code
    lvl = 0
    scope = {}
    root = tree
    node = tree.children[3]
    status_code, node, scope, lvl = analyse_tree(path, root, node, scope, lvl)

def analyse_tree(path, root, node, scope, lvl):
    stat = 0
    while id(node) != id(root):
       if len(node.children) > 0:
          child = node.children[0]
          if child.value is not None:
             if child.value.token == VAR:
                stat, node, scope = process_var(child.next, scope, lvl, path)
                if stat != 0:
                   break
             elif child.value.token == DO:
                lvl += 1
                stat, node, scope = process_do(child.next, scope, lvl, path)
                lvl -= 1
          else:
             node = child
       else:
          if node.value != '':
             print(node.value)
          node = node.up_node()
    lvl -= 1
    return stat, node.up_node(), scope, lvl

def process_do()

def process_var(child, scope, lvl, path):
    stat = 0
    limit = child.next
    node = child
    variables = []
    while id(node) != id(limit):
       if len(node.children) > 0:
          node = node.children[0]
       else:
          if node.value != '':
             if node.value.token == OP:
                variables.append(node.value)
          node = node.up_node()
    node = limit.next
    node = node.children[0]
    if node.value is not None:
       if node.value.token == ARRAY:
          node = node.next.children[1]
          limit = node.next
          val_1 = None
          val_tok = None
          val_2 = None
          shape = []
          while id(node) != id(limit):
             if len(node.children) > 0:
                node = node.children[0]
             else:
                if node.value != '':
                   if node.value.token == NUM:
                      if val_1 is None:
                         val_1 = int(node.value.value)
                         val_tok = node
                      else:
                         val_2 = int(node.value.value)
                   elif node.value.token == COMMA:
                      length = val_2-val_1+1
                      if length < 0:
                         stat = -5
                         print("File: %s - Line: %d:%d\nIndex Error: Invalid array initialization interval [%d, %d], length must be positive" % (path, val_tok.value.line, val_tok.value.col, val_1, val_2), file=sys.stderr)
                         val_1 = None
                         val_tok = None
                         val_2 = None
                         break
                      else:
                         val_1 = None
                         val_tok = None
                         val_2 = None
                         shape.append(length)
                node = node.up_node()
          if val_1 != None:
             length = val_2-val_1+1
             if length < 0:
                stat = -5
                print("File: %s - Line: %d:%d\nIndex Error: Invalid array initialization interval [%d, %d], length must be positive" % (path, val_tok.value.line, val_tok.value.col, val_1, val_2), file=sys.stderr)   
             else:
                shape.append(length)
          node = node.up_node()
          node = node.next
          type_tok = node.children[0].value
    else:
       type_tok = node.children[0].value
       shape = [1]
    if stat == 0:
       try:
         info = scope[lvl]
       except KeyError:
         info = {}
         scope[lvl] = info
       for var in variables:       
           info[var.value] = {'size':shape, 'type':type_tok, 'tok':var}
    return stat, node.up_node(), scope




