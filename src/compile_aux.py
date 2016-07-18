import sys

from compiler.backend import codegen
from compiler.frontend import semantic

path = '../examples/hcl/final/'

stat, tree, data = semantic.analyse(path + sys.argv[1])
stat, lines = codegen.code_generation(data)
