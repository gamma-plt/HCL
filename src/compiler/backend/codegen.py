# -*- coding: utf-8 -*-

from __future__ import print_function

import vm
import os
import re
import sys
import random

SET = 'set'
MOV = 'mov'
INC = 'inc'
DEC = 'dec'
MUL = 'mul'
DIV = 'div'
ADD = 'add'
SUB = 'sub'
NOT = 'not'
OR = 'or'
AND = 'and'
XOR = 'xor'
MOD = 'mod'
CMP = 'cmp'
PUSH = 'push'
CALL = 'call'
FREE = 'free'
HALT = 'halt'
PRINT = 'print'
POW = 'pow'

DO = 'do'
IF = 'if'
ASSIGNMENT = 'assignment'
READ = 'read'
CLC = 'clc'
GSS = 'gss'
EQU = 'equ'
NEQ = 'neq'
GE = 'ge'
GE_L = 'sgt'
LE = 'le'
LE_L = 'slt'
GEQ = 'geq'
LEQ = 'leq'
ACT = 'act'

SPACE = 'space'
NEWLINE = 'nl'
SPACE_VAL = '100000'
NEWLINE_VAL = '001010'

FALSE = '0000'
TRUE = '0001'

INT = 'integer'
BOOL = 'boolean'
CHAR = 'char'

OP = 'op'
OP1 = 'oper1'
OP2 = 'oper2'
OPER = 'op'
NUM = 'num'
VAR = 'var'
SCOPE = 'scope'
INDEX = 'index'
FUNC = 'func'

RET_INT = '..retint'
RET_BOOL = '..retbol'
RET_CHR = '..retchr'

MINUS = 'minus'
PLUS = 'plus'
TIMES = 'times'
POWER = 'power'
EQ = 'eq'
NEQ = 'neq'

comp_operators = {x:True for x in [EQ, NEQ, GE, LE, GEQ, LEQ]}
conmutative_operators = {x:True for x in [PLUS, TIMES, EQ, NEQ, AND, OR]}
operator_instr = {PLUS:ADD, MINUS:SUB, TIMES:MUL, DIV:DIV, MOD:MOD, AND:AND, OR:OR}
cmp_inst = {EQ:EQU, NEQ:NEQ, GEQ:GEQ, LEQ:LEQ, LE:LE_L, GE:GE_L}
cmp_opposite = {EQ:NEQ, NEQ:EQU, GEQ:LE_L, LEQ:GE_L, GE:LEQ, LE:GEQ}

func_ret_regs = {'int':RET_INT, 'char':RET_CHR, 'boolean':RET_BOOL} 

type_equivalence = {'int':INT, BOOL:BOOL, CHAR:CHAR}

initialization = {}
free_registers = {}
auxiliar_vars = {}

count = {'aux':0, 'do':0, 'if':0}

for _type in ['int', 'chr', 'bol']:
    for i in range(1, 6):
        free_registers['.r%d%s' % (i, _type)] = True
    # free_registers['..ret%s' % (_type)] = True

def code_generation(data):
    stat = 0
    lines = []
    path = data['path']
    folder = os.path.dirname(path)
    file_name = os.path.basename(path)
    output_file = file_name.replace('.hcl', '.vhcl')
    if output_file == file_name:
       output_file += '.vhcl'
    lines.append(';; %s : Autogenerated file by HCL Compiler v1.0\n' % (output_file))
    stat, lines = variable_declaration(data, lines)
    if stat == 0:
       lines.append('\n;; General program execution routine\n')
       lines = program_generation(data, lines)
       lines.append('%s' % (HALT))
       with open(folder+'/'+output_file, 'wb') as fp:
          fp.write('\n'.join(lines))
    return stat, lines

def variable_declaration(data, lines):
    stat = 0
    lines.append(';; Auxiliar character defintion')
    lines.append(";; Space character")
    lines.append('%s %s %s' % (SET, SPACE, CHAR))
    lines.append(';; New Line character')
    lines.append('%s %s %s' % (SET, NEWLINE, CHAR))
    lines.append(';; Space character initialization')
    lines.append('%s %s %s' % (MOV, SPACE, SPACE_VAL))
    lines.append(';; New Line character initialization')
    lines.append('%s %s %s\n' % (MOV, NEWLINE, NEWLINE_VAL))
    lines.append(';; General variable defintion')
    
    for scope in sorted(data['definitions'].keys()):
        scope_variables = data['definitions'][scope]
        for variable in scope_variables:
            var_info = scope_variables[variable]
            #Limitation: Number of indices allowed by the VM is restricted to 2
            if len(var_info['size']) > 2:
               stat = -13
               print("File: %s - Line: %d:%d\nVirtual Machine Limitation: Dimensions of array %s must not exceed two" % (data['path'], var_info['tok'].line, var_info['tok'].col, variable), file=sys.stderr)   
               break
            instr = '%s %s%d %s' % (SET, variable, scope, type_equivalence[var_info['type']])
            if len(var_info['size']) > 0:
               instr += '#'+'#'.join(map(str, var_info['size']))
               initialization['%s%d' % (variable, scope)] = True
            else:
               initialization['%s%d' % (variable, scope)] = False
            lines.append(instr)
    return stat, lines

def _ident(lvl):
    return '\t'*lvl

def recover_free_register():
    reg = None
    available = filter(lambda x: free_registers[x], free_registers)
    if len(available) > 0:
       reg = random.choice(available)
    return reg

def free_registers_aux(free, lines, ident):
    for _var in free:
        if _var in free_registers:
           free_registers[_var] = True
        if _var in auxiliar_vars:
           lines.append(_ident(ident)+'%s %s' % (FREE, _var))
           del auxiliar_vars[_var]
    return lines

def alloc_aux_var(_type, lines, ident):
    alloc_reg = '_sysaux%d' % (count['aux'])
    count['aux'] += 1
    auxiliar_vars[alloc_reg] = True
    lines.append(_ident(ident)+'%s %s %s' % (SET, alloc_reg, _type))
    return lines, alloc_reg

def allocate_register_aux(_type, lines, ident):
    reg_alloc = True
    reg = recover_free_register()
    if reg is None:
       reg_alloc = False
       lines, reg = alloc_aux_var(_type, lines, ident)
    return lines, reg_alloc, reg

def program_generation(data, lines, scope=0, ident=0):
    for instruction in data['instructions'][scope]:
        instruction_type = [key for key in instruction if instruction[key] is not None][0]
        if instruction_type == READ:
           lines = read_generation(instruction['read'], data, lines, ident)
        elif instruction_type == ASSIGNMENT:
           lines = assignment_gen(instruction[ASSIGNMENT], data, lines, ident)
        elif instruction_type == DO:
           lines = do_gen(instruction[DO], data, lines, ident)
        elif instruction_type == IF:
           lines = if_gen(instruction[IF], data, lines, ident)
        elif instruction_type == PRINT:
           lines = print_gen(instruction[PRINT], data, lines, ident)
    return lines

def print_gen(addr, data, lines, ident):
    lines, op_reg = process_expression(addr, data, lines, ident)
    lines.append(_ident(ident)+'%s %s' % (PRINT, op_reg['value']))
    lines.append(_ident(ident)+'%s %s' % (PRINT, NEWLINE))
    op_reg['free'].append(op_reg['value'])
    lines = free_registers_aux(op_reg['free'], lines, ident)
    return lines

def if_gen(guard_key, data, lines, ident):
    guards_info = data['guards'][guard_key]
    lines.append(_ident(ident)+'%s:' % (IF))
    ident += 1
    guard_list = []
    for i in range(0, len(guards_info)): 
        guard_name = '_if%dguard%d' % (count['if'], i)
        guard_list.append(guard_name)
    count['if'] += 1
    lines.append(_ident(ident)+'%s %s' % (GSS, ' '.join(guard_list)))
    for guard_name, guard in zip(guard_list, guards_info):
        lines.append(_ident(ident)+';; Calculating %s' % (guard_name))
        lines, guard_reg = process_expression(guard['expr'], data, lines, ident)
        lines.append(_ident(ident)+'%s %s %s' % (MOV, guard_name, guard_reg['value']))
        guard_reg['free'].append(guard_reg['value'])
        lines = free_registers_aux(guard_reg['free'], lines, ident)
    for guard_name, guard in zip(guard_list, guards_info):
        lines.append(_ident(ident)+'%s %s:' % (ACT, guard_name))
        lines = program_generation(data, lines, guard['scope'], ident+1)
    lines = free_registers_aux(guard_reg['free'], lines, ident)
    return lines

def do_gen(guard_key, data, lines, ident):
    # print(guard_key)
    guards_info = data['guards'][guard_key]
    # print(guards_info)
    lines.append(_ident(ident)+'%s:' % (DO))
    ident += 1
    guard_list = []
    for i in range(0, len(guards_info)): 
        guard_name = '_do%dguard%d' % (count['do'], i)
        guard_list.append(guard_name)
    # print(guard_list)
    count['do'] += 1
    lines.append(_ident(ident)+'%s %s' % (GSS, ' '.join(guard_list)))
    lines.append(_ident(ident)+'%s:' % (CLC))
    ident += 1
    for guard_name, guard in zip(guard_list, guards_info):
        # lines.append(_ident(ident)+';; Calculating %s' % (guard_name))
        lines, guard_reg = process_expression(guard['expr'], data, lines, ident)
        lines.append(_ident(ident)+'%s %s %s' % (MOV, guard_name, guard_reg['value']))
        guard_reg['free'].append(guard_reg['value'])
        lines = free_registers_aux(guard_reg['free'], lines, ident)
    ident -= 1
    for guard_name, guard in zip(guard_list, guards_info):
        lines.append(_ident(ident)+'%s %s:' % (ACT, guard_name))
        lines = program_generation(data, lines, guard['scope'], ident+1)
    lines = free_registers_aux(guard_reg['free'], lines, ident)
    return lines

def assignment_gen(assign_key, data, lines, ident):
    assign_info = data['assignments'][assign_key]
    lines, var_reg = process_expression(assign_info['var'], data, lines, ident)
    lines, expr_reg = process_expression(assign_info['value'], data, lines, ident)
    lines.append(_ident(ident)+'%s %s %s' % (MOV, var_reg['value'], expr_reg['value']))
    var_reg['free'] += expr_reg['free']
    var_reg['free'].append(expr_reg['value'])
    lines = free_registers_aux(var_reg['free'], lines, ident)
    initialization[var_reg['value']] = True
    return lines

def read_generation(read_info, data, lines, ident):
    var_tok = read_info['var']
    scope = read_info['scope']
    read_func = read_info['read']
    size = data['definitions'][scope][var_tok.value]['size']
    # lines.append(';; Reading variable %s (Scope %d) of size %s' % (var_tok.value, scope, 'x'.join(map(str,size))))
    if len(size) == 0:
       lines.append(_ident(ident)+'%s %s%d' % (read_func, var_tok.value, scope))
    elif len(size) == 1:
       lines.append(_ident(ident)+'%s %s %s' % (SET, '_sysidx1', INT))
       lines.append(_ident(ident)+'%s %s %s' % (MOV, '_sysidx1', FALSE))
       lines.append(_ident(ident)+'%s:' % (DO))
       ident += 1
       lines.append(_ident(ident)+'%s %s' % (GSS, '_sysguard1'))
       lines.append(_ident(ident)+'%s:' % (CLC))
       ident += 1
       bin_size = bin(size[0])[2:]
       lines.append(_ident(ident)+'%s %s %s' % (CMP, '_sysidx1', bin_size))
       lines.append(_ident(ident)+'%s:' % (LE_L))
       ident += _L1
       lines.app_Lend(_ident(ident)+'%s %s %s' % (MOV, '_sysguard1', TRUE))
       ident -= 2
       lines.append(_ident(ident)+'%s %s:' % (ACT, '_sysguard1'))
       ident += 1
       lines.append(_ident(ident)+'%s %s%d[%s]' % (read_func, var_tok.value, scope, '_sysidx1'))
       lines.append(_ident(ident)+'%s %s' % (INC, '_sysidx1'))
       ident -= 2
       lines.append(_ident(ident)+'%s %s' % (FREE, '_sysidx1'))
    else:
       lines.append(_ident(ident)+'%s %s %s' % (SET, '_sysidx1', INT))
       lines.append(_ident(ident)+'%s %s %s' % (SET, '_sysidx2', INT))
       lines.append(_ident(ident)+'%s %s %s' % (MOV, '_sysidx1', FALSE))
       lines.append(_ident(ident)+'%s %s %s' % (MOV, '_sysidx2', FALSE))
       lines.append(_ident(ident)+'%s:' % (DO))
       ident += 1
       lines.append(_ident(ident)+'%s %s' % (GSS, '_sysguard1'))
       lines.append(_ident(ident)+'%s:' % (CLC))
       dim_1 = bin(size[0])[2:]
       ident += 1
       lines.append(_ident(ident)+'%s %s %s' % (CMP, '_sysidx1', dim_1))
       lines.append(_ident(ident)+'%s:' % (LE_L))
       ident += _L1
       lines.app_Lend(_ident(ident)+'%s %s %s' % (MOV, '_sysguard1', TRUE))
       ident -= 2
       lines.append(_ident(ident)+'%s %s:' % (ACT, '_sysguard1'))
       ident += 1
       lines.append(_ident(ident)+'%s %s %s' % (MOV, '_sysidx2', FALSE))
       lines.append(_ident(ident)+'%s:' % (DO))
       ident += 1
       lines.append(_ident(ident)+'%s %s' % (GSS, '_sysguard2'))
       lines.append(_ident(ident)+'%s:' % (CLC))
       dim_2 = bin(size[1])[2:]
       ident += 1
       lines.append(_ident(ident)+'%s %s %s' % (CMP, '_sysidx2', dim_2))
       lines.append(_ident(ident)+'%s:' % (LE_L))
       ident += _L1
       lines.app_Lend(_ident(ident)+'%s %s %s' % (MOV, '_sysguard2', TRUE))
       ident -= 2
       lines.append(_ident(ident)+'%s %s:' % (ACT, '_sysguard2'))
       ident += 1
       lines.append(_ident(ident)+'%s %s%d[%s][%s]' % (read_func, var_tok.value, scope, '_sysidx1', '_sysidx2'))
       lines.append(_ident(ident)+'%s %s' % (INC, '_sysidx2'))
       ident -= 2
       lines.append(_ident(ident)+'%s %s' % (INC, '_sysidx1'))
       ident -= 2
       lines.append(_ident(ident)+'%s %s' % (FREE, '_sysidx1'))
       lines.append(_ident(ident)+'%s %s' % (FREE, '_sysidx2'))
    initialization['%s%d' % (var_tok.value, scope)] = True
    return lines

def process_expression(addr, data, lines, ident, index=False):
    #Return: {'value':reg, 'register':reg_alloc, 'free':free}
    addr_info = data['addresses'][addr]
    if addr_info[OPER] is None:
       #Case 1: Single Variable/Number/Function Call
       # print(addr)
       var_info = addr_info[OP1]
       lines, expr_reg = process_simple_operand(var_info, data, lines, ident, index)
    else:
       if addr_info[OP1] is None:
          #Case 2: Negative/Negated Single Variable/Number/Function Call
          var_info = addr_info[OP2]
          if var_info['addr'] is not None:
             lines, expr_reg = process_expression(var_info['addr'], data, lines, ident)
          else:
             lines, expr_reg = process_simple_operand(var_info, data, lines, ident, index)
          _reg = expr_reg['value']
          if not expr_reg['register']:
             if expr_reg['value'] not in auxiliar_vars:
                _aux = recover_free_register()
                if _aux is None:
                   _aux = alloc_aux_var(type_equivalence[addr_info['type']], lines, ident)
                lines.append(_ident(ident)+'%s %s %s' % (MOV, _aux, _reg))
                lines = free_registers_aux(expr_reg['free'], lines, ident)
                expr_reg['free'] = []
                _reg = _aux
                expr_reg['value'] = _reg
          lines.append(_ident(ident)+'%s %s' % (NOT, _reg))
          lines.append(_ident(ident)+'%s %s' % (INC, _reg))
       else:
          #Case 3: General 3AC operations
          lines, expr_reg = process_general_operation(addr_info, data, lines, ident)
    return lines, expr_reg


def process_general_operation(addr_info, data, lines, ident):
    #TODO: Implement cases 3.1 - 3.4
    free = []
    reg = ''
    reg_alloc = False
    expr_reg = {'value':reg, 'register':reg_alloc, 'free':free}

    op1_addr = addr_info[OP1]['addr']
    op2_addr = addr_info[OP2]['addr']
    op_name = addr_info[OP].token
    _type = addr_info['type']

    lines, expr1_reg = process_expression(op1_addr, data, lines, ident)
    lines, expr2_reg = process_expression(op2_addr, data, lines, ident)
    
    free += expr1_reg['free']
    free += expr2_reg['free']

    if expr1_reg['register'] or expr1_reg['value'] in auxiliar_vars:
       #Case 1: Op1 is a Register/Auxiliar Variable
       reg_alloc = expr1_reg['register']
       reg = expr1_reg['value']
       if expr2_reg['value'] in auxiliar_vars:
          #Op2 is an auxiliar variable      
          free.append(expr2_reg['value'])
    elif expr2_reg['register'] or expr2_reg['value'] in auxiliar_vars:
       #Case 2: Op2 is a Register/Auxiliar Variable
       if op_name in conmutative_operators:
          #2.1 Operator is conmutative, switch arguments
          reg_alloc = expr2_reg['register']
          reg = expr2_reg['value']
          if expr1_reg['value'] in auxiliar_vars:      
             free.append(expr1_reg['value'])
          expr1_reg, expr2_reg = expr2_reg, expr1_reg
       else:
          #2.2 Operator is non conmutative, allocate new register
          lines, reg_alloc, reg = allocate_register_aux(_type, lines, ident)
          free.append(expr2_reg['value'])
          free.append(expr1_reg['value'])
    else:
       #Case 3: Op1 and Op2 are simple operands
       lines, reg_alloc, reg = allocate_register_aux(_type, lines, ident)    
    
    lines = process_operation(expr1_reg, expr2_reg, op_name, reg, lines, ident)
    lines = free_registers_aux(free, lines, ident)

    expr_reg['value'] = reg
    expr_reg['register'] = reg_alloc
      
    return lines, expr_reg 

def process_operation(expr1_reg, expr2_reg, op_name, reg, lines, ident):
    if op_name == POWER:
       lines = process_pow(expr1_reg, expr2_reg, reg, lines, ident)
    elif op_name in comp_operators:
       lines = process_comp(expr1_reg, expr2_reg, op_name, reg, lines, ident)
    else:
       lines = process_conventional_op(expr1_reg, expr2_reg, op_name, reg, lines, ident)
    return lines

def process_comp(expr1_reg, expr2_reg, op_name, reg, lines, ident):
    lines.append(_ident(ident)+'%s %s %s' % (CMP, expr1_reg['value'], expr2_reg['value']))
    lines.append(_ident(ident)+'%s:' % (cmp_inst[op_name]))
    ident += 1
    lines.append(_ident(ident)+'%s %s %s' % (MOV, reg, TRUE))
    ident -= 1
    lines.append(_ident(ident)+'%s:' % (cmp_opposite[op_name]))
    ident += 1
    lines.append(_ident(ident)+'%s %s %s' % (MOV, reg, FALSE))
    ident -= 1
    return lines

def process_conventional_op(expr1_reg, expr2_reg, op_name, reg, lines, ident):
    if expr1_reg['value'] == reg:
       lines.append(_ident(ident)+'%s %s %s' % (operator_instr[op_name], expr1_reg['value'], expr2_reg['value']))
    else:
       lines.append(_ident(ident)+'%s %s %s' % (MOV, reg, expr1_reg['value']))
       lines.append(_ident(ident)+'%s %s %s' % (operator_instr[op_name], reg, expr2_reg['value']))
    return lines

def process_pow(expr1_reg, expr2_reg, reg, lines, ident):
    lines.append(_ident(ident)+'%s %s' % (PUSH, expr1_reg['value']))
    lines.append(_ident(ident)+'%s %s' % (PUSH, expr2_reg['value']))
    lines.append(_ident(ident)+'%s %s' % (CALL, POW))
    lines.append(_ident(ident)+'%s %s %s' % (MOV, reg, RET_INT))
    return lines

def process_simple_operand(var_info, data, lines, ident, index):
    # print(var_info)
    if var_info[NUM] is not None:
       expr_reg = process_single_constant(var_info, index)
    elif var_info[VAR] is not None:
       lines, expr_reg = process_single_var(var_info, data, lines, ident)
    elif var_info[FUNC] is not None:         
       lines, expr_reg = process_single_func(var_info, data, lines, ident)
    return lines, expr_reg

def process_single_constant(var_info, index):
    free = []
    reg = ''
    reg_alloc = False
    expr_reg = {'value':reg, 'register':reg_alloc, 'free':free}
    if index:
       reg = str(var_info[NUM].value)
    else:
       reg = bin(int(var_info[NUM].value))[2:]
    expr_reg['value'] = reg
    return expr_reg

def process_single_var(var_info, data, lines, ident):
    free = []
    reg = ''
    reg_alloc = False
    expr_reg = {'value':reg, 'register':reg_alloc, 'free':free}
    
    var_d = var_info[VAR]
    var_name = var_d[VAR]
    scope = var_d[SCOPE]
    reg = '%s%d' % (var_name.value, scope)
    if var_info[INDEX] is None:
       if not initialization[reg]:
          print("File: %s - Line: %d:%d\nWarning: Variable %s (Scope %d) has not been initialized" % (data['path'], var_name.line, var_name.col, var_name.value, scope), file=sys.stderr)
          # lines.append(_ident(ident)+';;Warning - Variable %s%d without initialization, using default values' % (var_name.value, scope))
    else:
       index_key = var_info[INDEX]
       for ad in data['indices'][index_key]:
           lines, reg_i = process_expression(ad, data, lines, ident, index=True)
           if reg_i['register']:
              free.append(reg_i['value'])
           if reg_i['value'] in auxiliar_vars:
              free.append(reg_i['value'])
           reg += '[%s]' % (reg_i['value'])
    expr_reg['value'] = reg
    expr_reg['free'] = free
    return lines, expr_reg


def process_single_func(var_info, data, lines, ident):
    free = []
    reg = ''
    reg_alloc = False
    expr_reg = {'value':reg, 'register':reg_alloc, 'free':free}

    func_key = var_info[FUNC]
    func_info = data['functions'][func_key]
    func_call = func_info['call']
    func_type = func_info['type']
    for arg in func_info['args']:
        lines, arg_calc = process_expression(arg, data, lines, ident)
        lines.append(_ident(ident)+'%s %s' % (PUSH, arg_calc['value']))
        if arg_calc['register']:
           free.append(arg_calc['value'])
        free += arg_calc['free']
    lines.append(_ident(ident)+'%s %s' % (CALL, func_call))
    ret_reg = func_ret_regs[func_type]
    alloc_reg = recover_free_register()
    reg_alloc = True
    if alloc_reg is None:
       reg_alloc = False
       lines, alloc_reg = alloc_aux_var(type_equivalence[func_type], lines, ident)
    lines.append(_ident(ident)+'%s %s %s' % (MOV, alloc_reg, ret_reg))
    lines = free_registers_aux(free, lines, ident)
    free = []
    expr_reg['value'] = alloc_reg
    expr_reg['register'] = reg_alloc
    expr_reg['free'] = free 
    return lines, expr_reg   
