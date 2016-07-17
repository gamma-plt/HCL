from compiler.backend import codegen
from compiler.frontend import semantic

path = '../examples/hcl/collatz.hcl'

stat, tree, data = semantic.analyse(path)
stat, lines = codegen.code_generation(data)
