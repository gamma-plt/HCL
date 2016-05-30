# -*- coding: utf-8 -*-

from __future__ import print_function

import vm
import os
import re
import sys
import parser

basepath = os.path.dirname(__file__)
INFERENCE_PATH = '../../../doc/language/Inference_Rules.txt'
INFERENCE_PATH = os.path.abspath(os.path.join(basepath, INFERENCE_PATH))

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
LSPAREN = u'left_sparen'
LRPAREN = u'left_rparen'

# operators = []
inference = {'single':{}, 'double':{}}
count = {'if':0, 'do':0, 'addr':0, 'lvl':-1, 'index':0}

types = {INT:'INTEGER', BOOLEAN:'BOOLEAN', CHAR:'CHAR'}

def analyse(path):
    # global operators
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
    func = {}
    addresses = {}
    data = {'path':path, 'scope':scope, 'definitions': definitions,
            'program': program, 'guards':guards, 'instructions':instructions,
            'functions':func, 'addresses':addresses}
    root = tree
    node = tree.children[3]

    with open(INFERENCE_PATH, 'rb') as fp:
         lines = fp.readlines()

    for line in lines:
        line = line.strip('\n')
        op,args = line.split(' : ')
        ty,res = args.split(' -> ')
        t = ty.split(' x ')
        if len(t) > 1:
           t1, t2 = t
           ops = inference['double']
        elif len(t) == 1:
           ops = inference['single']
        try:
          info = ops[op]
        except KeyError:
          info = {}
          ops[op] = info
        if len(t) > 1:
           try:
             op_res = info[t1]
           except KeyError:
             op_res = {}
             info[t1] = op_res
           op_res[t2] = res
           try:
             op_res = info[t2]
           except KeyError:
             op_res = {}
             info[t2] = op_res
           op_res[t2] = res
        else:
           info[t[0]] = res
        # operators.append(op)
    # operators = list(set(operators)) 

    # status_code, node = analyse_tree(node, root, data)



def process_expr(node, data, lvl, _type=None):
    stat = 0
    count = 0
    typ = None
    last_addr = None
    last_var = None
    shape = [1]
    operators = set(inference['double'].keys()).union(inference['single'].keys())
    operator = {'var':None, 'func':None, 'addr':None, 'index':None}
    op = {'oper1':None, 'op':None, 'oper2':None}
    limit = node.up_node()
    while id(node) != id(limit):
       last_type = typ
       if len(node.children) > 0:
          node = node.children[0]
       else:
          if node.value != '':
             if node.value.token == OP:
                stat, typ, shape, scope = lookup_var(node.value, data, lvl)
                operator['var'] = (scope, node.value, typ)
                if op['oper1'] is None:
                   if op['op'] is not None:
                      op['oper2'] = operator
                      try:
                        #Unary Operators processing
                        typ = inference['single'][op['op'].token][typ]
                        data['addresses']["addr%d" % (count['addr'])] = op
                        last_addr = "addr%d" % (count['addr'])
                        count['addr'] += 1     
                      except KeyError:
                        stat = -7
                        print("File: %s - Line: %d:%d\nOperand Type Mismatch: Operand %s is undefined for arguments of type: %s (Variable: %s)" % (data['path'], node.value.line, node.value.col, op['op'].value, typ, node.value.value), file=sys.stderr) 
                   else:
                      op['oper1'] = operator
                      count += 1
                      last_var = 'oper1'
                elif op['oper2'] is None:                              
                   #Binary Operators processing
                   try:
                      typ = inference['double'][op['op'].token][last_type][typ]
                   except KeyError:
                      stat = -9
                      print("File: %s - Line: %d:%d\nOperand Type Mismatch: Cannot perform operation %s over arguments of type %s, %s (variables: %s, %s)" % (data['path'], op['op'].line, op['op'].col, op['op'].value, op['oper1']['var'][2], op['oper2']['var'][2], op['oper1']['var'][1].value, op['oper2']['var'][1].value), file=sys.stderr)    
                   op['oper2'] = operator
                   data['addresses']["addr%d" % (count['addr'])] = op
                   last_addr = "addr%d" % (count['addr'])
                   count['addr'] += 1
                   last_var = 'oper2'
             elif node.value.token in operators:
                op['op'] = node.value
                if len(shape) > 1:
                   if op['oper1']['index'] is None:
                      stat = -8
                      print("File: %s - Line: %d:%d\nBroadcasting Error: Cannot perform operations over complete or partial arrays (Variable: %s)" % (data['path'], op['oper1']['var'][1].line, op['oper1']['var'][1].col, op['oper1']['var'][1].value), file=sys.stderr)
             elif node.value.token == LSPAREN:
                #Array Index Referencing
                #TODO: process_idx
                opf = op[last_var]
                if len(shape) == 1:
                   stat = -10
                   print("File: %s - Line: %d:%d\nIndex Error: Cannot reference indices over scalar variables (Variable: %s)" % (data['path'], opf['var'][1].line, opf['var'][1].col, opf['var'][1].value), file=sys.stderr)
                else:
                   stat, node, idx_id = process_indices(node, data, opf)
                   opf['index'] = idx_id
             elif node.value.token == LRPAREN:
                #Round Parentheses expressions
                #TODO:
                stat, node, addr_id, typ = process_expr(node.up_node(), data, lvl)
             #TODO: Functions
          node = node.up_node()
       if stat != 0:
          break


def lookup_var(tok, data, lvl):
    stat = 0
    inf = None
    name = tok.value
    typ = None
    shp = -1
    while lvl != -1:
       try:
         inf = data['definitions'][lvl][name]
       except KeyError:
         lvl = data['scope'][lvl]['inside']
    if not inf:
       stat = -6
       print("File: %s - Line: %d:%d\nUndefined Variable: Variable %s must be defined" % (data['path'], tok.line, tok.col, name), file=sys.stderr)
    else:
       typ = inf['type']
       shp = inf['size']
    return stat, typ, shp, lvl


def process_var(child, data, lvl):
    scope = data['definitions']
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
                         print("File: %s - Line: %d:%d\nIndex Error: Invalid array initialization interval [%d, %d], length must be positive" % (data['path'], val_tok.value.line, val_tok.value.col, val_1, val_2), file=sys.stderr)
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
                print("File: %s - Line: %d:%d\nIndex Error: Invalid array initialization interval [%d, %d], length must be positive" % (data['path'], val_tok.value.line, val_tok.value.col, val_1, val_2), file=sys.stderr)   
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




