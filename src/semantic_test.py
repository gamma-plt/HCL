from compiler.frontend import parser, semantic

path = '../examples/hcl/example1.hcl'
scope = {}
definitions = {}
indices = {}
program = {}
guards = {}
instructions = {}
func = {}
addresses = {}
data = {'path':path, 'scope':scope, 'definitions': definitions,
        'program': program, 'guards':guards, 'instructions':instructions,
        'functions':func, 'addresses':addresses, 'indices':indices}

data['scope'][0] = {'inside':-1}
lvl = 0
complete = True
debug = False

tree, stat = parser.parse(path)
semantic.analyse(path)
node = tree.children[3].children[0].children[0].children[0].children[1]
stat, node = semantic.process_definition(node, data, 0)
node = node.children[0].children[0].children[1]
stat, node = semantic.process_definition(node, data, 0)
node = node.children[0].children[0].children[1].children[0]
semantic.process_expr(node, data, 0)


# node = tree.children[3].children[0].children[0].children[0].children[1]
# stat, node = semantic.process_var(node, data, lvl)
# node = node.children[0].children[0].children[1]
# stat, node = semantic.process_var(node, data, lvl)
# node = node.children[0].children[0].children[2].children[0]
# stat, node, last_addr, typ = semantic.process_expr(node, data, lvl)
# node = tree.children[3].children[0].children[0].children[0].children[1]
# stat, node = semantic.process_var(node, data, 0)

#(((-(3-c)*(a+8))+(b*(c/(d^6))))>(f[(a*c)%(6^k),b+f,k*abs(h,i*func2(i*k,g%5))]*max(c+1,d-6,m*f[5,6,7])))∧((-g∨(¬even(n)*7))∧¬(a≠b))
