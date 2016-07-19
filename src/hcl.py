#!/usr/bin/env python

from __future__ import print_function

import os
import sys
import codecs
import compiler.backend as backend
import compiler.frontend as frontend


if __name__ == '__main__':
   if len(sys.argv) > 1:
      filename = sys.argv[1]
      try:
        with codecs.open(filename, 'rb', 'utf-8') as fp:
             lines = fp.readlines()
      except IOError:
        print("Error: File %s does not exist, compiler exited with status code 1" % (filename))
        sys.exit(1)
      except ValueError:
        print("Encoding Error: Unexpected error while trying to read file %s, compiler exited with status 2" % (filename))
        sys.exit(2)
   else:
      print("Usage: hcl.py name_of_file")
      sys.exit(3)

   stat, tokens = frontend.lexer.lex(lines, filename) 
   if stat != 0:
      print("Compiler exited with status %d" % (stat), file=sys.stderr)
      sys.exit(stat)

   stat, tree = frontend.parser.parse(tokens, filename)
   if stat != 0:
      print("Compiler exited with status %d" % (stat), file=sys.stderr)
      sys.exit(stat)
   
   stat, data = frontend.semantic.analyse(tree, filename)
   if stat != 0:
      print("Compiler exited with status %d" % (stat), file=sys.stderr)
      sys.exit(stat)
   
   stat, lines, output_file = backend.codegen.code_generation(data)     
   if stat != 0:
      print("Compiler exited with status %d" % (stat), file=sys.stderr)
      sys.exit(stat)

   with open(output_file, 'wb') as fp:
      fp.write('\n'.join(lines))
   
   sys.exit(0)