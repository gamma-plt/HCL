# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import re
import sys
import lexer
import ll_table as LLT

GRAMMAR_PATH = '../../../doc/language/LL_Grammar_Description.txt'

basepath = os.path.dirname(__file__)
GRAMMAR_PATH = os.path.abspath(os.path.join(basepath, GRAMMAR_PATH))

class ParseTree(object):
   def __init__(self, rule):
       self.rule = rule
       self.parent = None
       self.value = None
       self.next = None
       self.children = []
       self.marks = []

   def subs(self, args):
       last = None
       for i, arg in enumerate(args):
           if isinstance(arg, lexer.Token):
              node = ParseTree(arg.token)
           else:
              node = ParseTree(arg)
           if last is not None:
              last.next = node
           self.children.append(node)
           self.marks.append(False)
           node.parent = self
           last = node
       # last.next = self
       return self.children[0]

   def val(self, value):
       self.value = value
       return self.up_node()

   def up_node(self):
       node = self
       root = False
       while node.next is None:
          if node.parent is None:
             root = True
             break
          node = node.parent
       if not root: 
          return node.next
       else:
          return node  

   def __unicode__(self):
       if len(self.children) == 0:
          s = u'Terminal: '+unicode(self.value)
       else:
          s = u'Rule: '+self.rule+u'\n'
          if self.value is not None:
             s += u'Value: '+unicode(self.value)+u'\n'
          s += u'Derivation: '
          for child in self.children:
              if child.rule is None:
                 s += child.value+u' '
              else:
                 s += child.rule+u' '
       return s

   def __str__(self):
       return self.__unicode__().encode('utf-8')

   def __repr__(self):
       return self.__str__()


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

def parse(path, debug=False):
    tokens, status_code = lexer.lex(path)
    if status_code != 0:
       print("Compiler exited with status -1", file=sys.stderr)
       return None, -1
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
    tree = ParseTree('P')
    root = tree
    stack = ['P']
    last_evaluation = None
    while len(stack) > 0:
       if debug:
          output(tokens, stack)
       if isinstance(stack[0], unicode) or isinstance(stack[0], str):
          try:
             trans = tab[stack[0]][tokens[0]]
             stack = trans + stack[1:]
             if len(trans) > 0:
                tree = tree.subs(trans)
             else:
                tree = tree.val('')
          except KeyError:
             status_code = -2
             if debug:
                print(stack[0])
                print(tokens[0])
             print("File: %s - Line: %d:%d\nSyntax Error: Unexpected symbol: %s; Expected: %s" % (path, tokens[0].line, tokens[0].col, tokens[0].value, ', '.join([i.value for i in tab[stack[0]].keys()])), file=sys.stderr)
             break
          except IndexError:
             if last_evaluation is None:
                last_evaluation = lexer.Token(u'', u'')
             status_code = -3
             print("File: %s - Line: %d:%d\nSyntax Error: Missing symbol, expected: %s" % (path, last_evaluation.line, last_evaluation.col+len(last_evaluation.value), ', '.join([i.value for i in tab[stack[0]].keys()])), file=sys.stderr)
             print("Stack: "+stack[0])
             break
       else:
          if tokens[0] == stack[0]:
             last_evaluation = tokens[0]
             tree = tree.val(tokens[0])
             tokens = tokens[1:]
             stack = stack[1:]
          else:
             status_code = -2
             print("File: %s - Line: %d:%d\nSyntax Error: Unexpected symbol: %s; Expected: %s" % (path, tokens[0].line, tokens[0].col, tokens[0].value, stack[0].value), file=sys.stderr)
             break
    return root, status_code

def output(tokens, stack):
    if len(tokens) > 5:
       s = ' '.join([i.value for i in tokens[0:5]]) + ' ... '+tokens[-1].value
    else:
       s = ' '.join([i.value for i in tokens])
    if len(stack) > 5:
       s += '\n'+' '.join([i.value if isinstance(i, lexer.Token) else i for i in stack[0:5]]) + ' ... '+stack[-1].value
    else:
       s += '\n'+' '.join([i.value if isinstance(i, lexer.Token) else i for i in stack])
    print(s+'\n')


def compress_tree(node):
    obj_node = None
    if len(node.children) == 1:
       obj_node = node.children[0]
       while len(obj_node.children) == 1:
          obj_node = obj_node.children[0]
       if len(obj_node.children) == 0:
          if obj_node.value is not None:
             node.value = obj_node.value
          node.children = []
       else:
          node.children = obj_node.children
          for child in node.children:
              child.parent = node
    # for child in node.children:
    #    compress_tree(child)

def remove_useless_productions(node):
    for child in node.children:
        remove_useless_productions(child)
    if len(node.children) == 0:
       if node.value is None:
          idx = node.parent.children.index(node)
          del node.parent.children[idx]

def process_expr_tree(node, debug=False):
    last_lvl = 0
    node.lvl = 0
    queue = [node]
    f_term = False
    while len(queue) > 0:
       current_node = queue.pop(0)
       lvl = current_node.lvl
       if lvl != last_lvl:
          if debug:
             print("--------------------")
             print("Level %d" % (lvl))
          last_lvl = lvl
       if debug:
          print(current_node)
       if current_node.value is not None:
          if current_node.value.token == u'left_rparen':
             idx = queue.index(current_node.next.next)
             del queue[idx]
             current_node.parent.children = current_node.parent.children[1:-1]
             current_node.parent.children[0].next = None
          else:   
            f_term = True
            break
       for child in current_node.children:
           child.lvl = current_node.lvl + 1
       queue += current_node.children
    if id(current_node) != id(node):
       if f_term:
          node.value = current_node.value
          idx = current_node.parent.children.index(current_node)
          del current_node.parent.children[idx]
       remove_useless_productions(node)
       compress_tree(node)
    for child in node.children:
       process_expr_tree(child, debug)

def remove_epsilon_productions(node, debug=False):
   last_lvl = 0
   node.lvl = 0
   queue = [node]
   while len(queue) > 0:
      current_node = queue.pop(0)
      lvl = current_node.lvl
      if lvl != last_lvl:
         if debug:
            print("--------------------")
            print("Level %d" % (lvl))
         last_lvl = lvl
      if debug:
         print(current_node)
      if current_node.value is not None:
         if current_node.value == '':
            parent = current_node.parent
            idx = parent.children.index(current_node)
            del parent.children[idx]
            parent.children[idx-1].next = current_node.next
      for child in current_node.children:
          child.lvl = current_node.lvl + 1
      queue += current_node.children

def remove_parentheses(node, debug=False):
   last_lvl = 0
   node.lvl = 0
   queue = [node]
   while len(queue) > 0:
      current_node = queue.pop(0)
      lvl = current_node.lvl
      if lvl != last_lvl:
         if debug:
            print("--------------------")
            print("Level %d" % (lvl))
         last_lvl = lvl
      if debug:
         print(current_node)
      if current_node.value is not None:
         if current_node.value.token == u'left_sparen' or current_node.value.token == u'right_sparen' or current_node.value.token == u'right_rparen':
            parent = current_node.parent
            idx = parent.children.index(current_node)
            del parent.children[idx]
            if idx > 0:
               parent.children[idx-1].next = current_node.next
      for child in current_node.children:
          child.lvl = current_node.lvl + 1
      queue += current_node.children

def comma_detection(node, debug=False):
   last_lvl = 0
   node.lvl = 0
   queue = [node]
   while len(queue) > 0:
      current_node = queue.pop(0)
      lvl = current_node.lvl
      if lvl != last_lvl:
         if debug:
            print("--------------------")
            print("Level %d" % (lvl))
         last_lvl = lvl
      if debug:
         print(current_node)
      if current_node.value is not None:
         if current_node.value.token == u'comma':
            current_node.parent.children = comma_collection(current_node, [])
            children = current_node.parent.children
            for i in range(0, len(children)-1):
                children[i].parent = current_node.parent
                children[i].next = children[i+1]
            children[-1].next = None
            children[-1].parent = current_node.parent
            queue = children + queue
         else:
            for child in current_node.children:
                child.lvl = current_node.lvl + 1
            queue += current_node.children 

def comma_collection(node,_list=[]):
   if node.value.token != u'comma':
      _list.append(node)
   else:
      for child in node.children:
          _list = comma_collection(child,_list)
   return _list
