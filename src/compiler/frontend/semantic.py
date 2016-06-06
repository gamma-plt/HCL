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
INF = u'infty'

NEXPR = u'E'
FEXPR = u'C'

# operators = []
inference = {'single':{}, 'double':{}}
count = {'if':0, 'do':0, 'addr':0, 'lvl':-1, 'index':0, 'func':0}

VM_TYPES = {'INTEGER':INT, 'BOOLEAN':BOOLEAN, 'CHAR':CHAR}

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
    indices = {}
    data = {'path':path, 'scope':scope, 'definitions': definitions,
            'program': program, 'guards':guards, 'instructions':instructions,
            'functions':func, 'addresses':addresses, 'indices':indices}
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
    #Node: Start of Expression 
    stat = 0
    count_e = 0
    typ = None
    last_addr = None
    last_var = None
    shape = [1]
    operators = set(inference['double'].keys()).union(inference['single'].keys())
    operator = {'var':None, 'func':None, 'addr':None, 'index':None, 'type':None, 'num':None}
    op = {'oper1':None, 'op':None, 'oper2':None}
    limit = node.next
    while id(node) != id(limit):
       last_type = typ
       if len(node.children) > 0:
          node = node.children[0]
       else:
          if node.value != '':
             if node.value.token == OP:
                stat, typ, shape, scope = lookup_var(node.value, data, lvl)
                operator['var'] = (scope, node.value)
                operator['type'] = typ
                stat, count_e, last_addr, last_var = process_op(node, data, op, operator, inference, count_e, last_addr, typ, last_type)
             elif node.value.token == NUM:
                operator['num'] = node.value.value
                typ = 'int'
                operator['type'] = typ
                stat, count_e, last_addr, last_var = process_op(node, data, op, operator, inference, count_e, last_addr, typ, last_type)
             elif node.value.token == INF:
                operator['num'] = 'inf'
                typ = 'int'
                operator['type'] = typ
                stat, count_e, last_addr, last_var = process_op(node, data, op, operator, inference, count_e, last_addr, typ, last_type)
             elif node.value.token in operators:
                if last_var == 'oper2':
                   operator = {'var':None, 'func':None, 'addr':last_addr, 'index':None, 'type':None}
                   op = {'oper1':operator, 'op':None, 'oper2':None}
                   operator = {'var':None, 'func':None, 'addr':None, 'index':None, 'type':None}
                   last_var = None
                   count_e = 1
                if op['op'] is not None:
                   op['oper2'] = {'var':None, 'func':None, 'addr':count['addr']+1, 'index':None, 'type':None}
                   data['addresses']["addr%d" % (count['addr'])] = op
                   last_addr = "addr%d" % (count['addr'])
                   op = {'oper1':None, 'op':None, 'oper2':None}
                   op['oper1'] = {'var':None, 'func':None, 'addr':last_addr, 'index':None, 'type':None}
                   count['addr'] += 1
                   operator = {'var':None, 'func':None, 'addr':None, 'index':None, 'type':None}
                   count_e = 1
                   last_var = None
                op['op'] = node.value
                count_e += 1
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
                   stat, node, idx_id = process_indices(node.up_node(), data, opf, lvl)
                   opf['index'] = idx_id
                   operator = {'var':None, 'func':None, 'addr':None, 'index':None, 'type':None}
             elif node.value.token == LRPAREN:
                #Round Parentheses expressions
                stat, node, addr_id, typ = process_expr(node.up_node(), data, lvl)
                operator['type'] = typ
                operator['addr'] = addr_id
                stat, count_e, last_addr, last_var = process_op(node, data, op, operator, inference, count_e, last_addr, typ, last_type)
             elif node.value.token == FUNC:
                stat, node, func_id, typ = process_func(node, data, lvl)
                operator['type'] = typ
                operator['func'] = func_id
                stat, count_e, last_addr, last_var = process_op(node, data, op, operator, inference, count_e, last_addr, typ, last_type)
          node = node.up_node()
       if stat != 0:
          break

def process_func(node, data, lvl):
    #Node: Function call
    stat = 0
    single_arg = False
    check = True
    typ = None
    func_id = None
    _func = node
    func_n = node.value.value.split('(')[0]
    if func_n == READ:
       single_arg = True
       check = False
    node = node.next
    limit = node.next
    _types_ = []
    args = []
    if check:
       try:
         func_description = vm.atomic.TYPES[vm.hardware.ATOMIC[func_n]]
       except KeyError:
         stat = -11
         print("File: %s - Line: %d:%d\nUnknown Function: Function %s is undefined" % (data['path'], _func.value.line, _func.value.col, func_n), file=sys.stderr)
    while id(node) != id(limit):
       if len(node.children) > 0:
          if node.rule == FEXPR:
             stat, node, addr_id, typ = process_expr(node, data, lvl)
             _types_.append(typ)
             args.append(addr_id)
          else:
             node = node.children[0]
       else:
          node = node.up_node()
       if stat != 0:
          break
    if stat == 0:
       __func__ = {'call':None, 'args':args}
       if not check:
          #If processing read function
          if len(args) > 1:
             stat = -12
             print("File: %s - Line: %d:%d\nIllegal Number of Arguments: Function %s, must have only one input argument, got %d arguments instead" % (data['path'], _func.value.line, _func.value.col, func_n, len(args)), file=sys.stderr)
          else:
             if typ == INT or typ == BOOLEAN:
                __func__['call'] = 'readint'
             elif typ == CHAR:
                __func__['call'] = 'readchr'
             func_id = 'func%d' % count['func']
             data['functions'] = __func__
             count['func'] += 1
       else:
          #The function expects only singleton return value per function
          #TODO: Extend to multiple return values (Broadcast arguments)
          vm_func = [[map(lambda x: map(lambda y: VM_TYPES[y], x), func_arg[0]), VM_TYPES[func_arg[1]]] for func_arg in func_description]
          t_types = None
          impl_f = False
          for impl in vm_func:
              idx = 0
              if len(impl[0]) == len(_types_):
                 for arg in _types_:
                     if impl[0][idx] == arg:
                        idx += 1
                     else:
                        break
              if idx == len(_types_)-1:
                 impl_f = True
                 t_types = impl
                 break
          if impl_f:
             typ = impl[1]
             func_id = 'func%d' % count['func']
             data['functions'] = __func__
             count['func'] += 1
          else:
             stat = -13
             err_s = map(lambda x: reduce(lambda u, v: u+' '+str(v), x[0], ''), vm_func)
             print("File: %s - Line: %d:%d\nIllegal Function Arguments: Function %s is not defined for arguments %s, expects: %s" % (data['path'], _func.value.line, _func.value.col, func_n, str(_types_), err_s), file=sys.stderr)
    return stat, node, func_id, typ             


def process_indices(node, data, lvl):
    #Node: Start of expression 
    stat = 0
    limit = node.next
    index_l = []
    idx_indices = None
    while id(node) != id(limit):
       if len(node.children) > 0:
          if node.rule == NEXPR:
             stat, node, addr_id, typ = process_expr(node, data, lvl, _type = INT) 
             if stat != 0:
                break
             index_l.append(addr_id)
          else:
             node = node.children[0]
       else:       
          node = node.up_node()
    if stat == 0:
       idx_indices = 'index%d' % (count['indices'])
       data['indices'][idx_indices] = index_l
       count['indices'] += 1
    return stat, node, idx_indices 

def process_op(node, data, op, operator, inference, count_e, last_addr, typ, last_type):
    stat = 0
    if op['oper1'] is None:
       if op['op'] is not None:
          op['oper2'] = operator
          try:
            #Unary Operators processing
            typ = inference['single'][op['op'].token][typ]
            data['addresses']["addr%d" % (count['addr'])] = op
            last_addr = "addr%d" % (count['addr'])
            count['addr'] += 1
            last_var = 'oper2'     
          except KeyError:
            stat = -7
            print("File: %s - Line: %d:%d\nOperand Type Mismatch: Operand %s is undefined for arguments of type: %s" % (data['path'], node.value.line, node.value.col, op['op'].value, typ), file=sys.stderr) 
       else:
          op['oper1'] = operator
          count_e += 1
          last_var = 'oper1'
    elif op['oper2'] is None:                              
       #Binary Operators processing
       try:
          typ = inference['double'][op['op'].token][last_type][typ]
       except KeyError:
          stat = -9
          print("File: %s - Line: %d:%d\nOperand Type Mismatch: Cannot perform operation %s over arguments of type %s, %s" % (data['path'], op['op'].line, op['op'].col, op['op'].value, op['oper1']['type'], op['oper2']['type']), file=sys.stderr)    
       op['oper2'] = operator
       data['addresses']["addr%d" % (count['addr'])] = op
       last_addr = "addr%d" % (count['addr'])
       count['addr'] += 1
       last_var = 'oper2'
       count_e += 1
    return stat, count_e, last_addr, last_var

def lookup_var(tok, data, lvl):
    stat = 0
    inf = None
    name = tok.value
    typ = None
    shp = -1
    while lvl != -1:
       try:
         inf = data['definitions'][lvl][name]
         break
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
    #Child: Sibling of VAR
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
          type_tok = node.children[0].value.value
    else:
       type_tok = node.children[0].value.value
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




