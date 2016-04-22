# -*- coding: utf-8 -*-

from __future__ import print_function

import vm
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
GUARD_SEP = u'guard_sep'
GUARD_EXEC = u'guard_exec'
INT = u'int'
BOOLEAN = u'boolean'
CHAR = u'char'
FUNC = u'func'
READ = u'read'


cond_count = {'if':0, 'do':0}
instr_count = 0
lvl_count = -1

types = {INT:'INTEGER', BOOLEAN:'BOOLEAN', CHAR:'CHAR'}

def analyse(path):
    tree, status_code = parser.parse(path)
    if status_code != 0:
       print("Compiler exited with status %d" % (status_code), file=sys.stderr)
       return None, status_code
    lvl = -1
    scope = {}
    definitions = {}
    program = {}
    guards = {}
    instructions = {}
    root = tree
    node = tree.children[3]
    status_code, node = analyse_tree(path, root, node, scope, program, guards, instructions, lvl)

def analyse_tree(path, root, node, scope, definitions, program, guards, instructions, lvl):
    stat = 0
    lvl_count += 1
    cur_lvl = lvl_count
    scope[cur_lvl] = {'inside':lvl}
    try:
       _ = instructions[lvl]
    except IndexError:
       instructions[lvl] = []
    while id(node) != id(root):
       if len(node.children) > 0:
          child = node.children[0]
          if child.value is not None:
             if child.value.token == VAR:
                stat, node = process_var(child.next, definitions, cur_lvl, path)
                if stat != 0:
                   break
             elif child.value.token == DO:
                stat, node = process_cond(child.next, scope, definitions, program, guards, instructions, cur_lvl, path, 'do')
                if stat != 0:
                   break
             elif child.value.token == IF:
                stat, node = process_cond(child.next, scope, definitions, program, guards, instructions, cur_lvl, path, 'if')
                if stat != 0:
                   break
          else:
             node = child
       else:
          if node.value != '':
             print(node.value)
          node = node.up_node()
    return stat, node

def process_cond(child, scope, definitions, program, guards, instructions, lvl, path, _type):
    stat = 0
    limit = child.next
    node = child
    key = _type+'_'+str(cond_count[_type])
    instruction = {'type':_type.upper(), 'set':None, 'guards':key}
    guards[key] = []
    while id(node) != id(limit):
       if len(node.children) > 0:
          try:
             if node.children[1].value is not None:
                if node.children[1].value.token == guard_exec:
                   stat, node, instr_list = process_expr(node.children[0], scope, definitions, lvl, path)
                   if stat != 0:
                      break
                   instructions['instr_'+str(instr_count)] = instr_list
                   g = {'eval':'instr_'+str(instr_count), 'scope':lvl}
                   instr_count += 1
                   guards[key].append(g)
                   node = node.up_node()
                   stat, node = analyse_tree(path, node.up_node(), node, scope, program, guards, instructions, lvl)
                   if stat != 0:
                      break
          except IndexError:
             node = node.children[0]
       else:
          node = node.up_node()
    cond_count[_type] += 1
    return stat, node.up_node()


def process_expr(_type, node, scope, definitions, lvl, path):
    stat = 0
    limit = node.next
    type_ = None
    while id(node) != id(limit):
       if len(node.children) > 0:
          node = node.children[0]
       else:
          if node.value != '':
             if node.value.token == FUNC:
                stat, node, type_ = process_func(type_, node, scope, definitions, lvl, path)
                
def process_func(_type, node, scope, definitions, lvl, path):
    stat = 0
    func = node.value.value.split('(')[0]
    if func == READ and _type is None:
       
    try:
       params = vm.atomic.TYPES[vm.hardware.ATOMIC[func]]
    except KeyError:
       stat = -5
       return stat, node, _type
    node = node.next


                

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
    return stat, node.up_node()




