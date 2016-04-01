import os
import codecs

def LL(path):
    with codecs.open(path, 'rb', 'utf-8') as fp:
         lines = fp.readlines()
    lines = map(lambda x: x.strip('\n'), lines)
    lines = filter(lambda x: x != '', lines)
    start_rule = lines[0].split(' -> ')[0]
    G = {i.split(' -> ')[0]:map(lambda x: filter(lambda y: y != '',x.split(' ')), i.split(' -> ')[1].split('|')) for i in lines}
    fne = FNE(G)
    F = {}
    for rule in fne:
        F[rule] = list(set([i[1] for i in fne[rule]]))
    fll = follow(G, F, start_rule)
    ll = {}
    for rule in fne:
        ll[rule] = {}
        for pred in fne[rule]:
            if pred[1] != u'EPSILON':
               ll[rule][pred[1]] = pred[2]
            else:
               for sym in fll[rule]:
                   ll[rule][sym] = []
    return G, fne, fll, ll

def FNE(G):
    fne = {}
    rules = list(G.keys())
    for rule in rules:
        fne = first(G, rule, fne)
    return fne

def first(G, rule, fne):
    s = []
    try:
      s = fne[rule]
    except KeyError:
      for prod in G[rule]:
          pos = 0
          ep_f = True
          while ep_f and pos < len(prod):
             if prod[pos] not in G.keys():
                s.append((rule, prod[pos], prod))
                ep_f = False
             else:
                num_ep = 0
                fne = first(G, prod[pos], fne)
                for t in fne[prod[0]]:
                    if t[1] != u'EPSILON':
                       s.append((rule, t[1], prod))
                    else:
                       num_ep += 1
                if num_ep == 0:
                   ep_f = False
             pos += 1
          if ep_f:
             s.append((rule, u'EPSILON', prod))
      fne[rule] = s
    return fne

def follow(G, fne, S):
    fll = {}
    pos = {}
    fll[S] = ['$']
    rules = G.keys()
    for r1 in rules:
        pos[r1] = []
        for r2 in rules:
            if r1 != r2:
               for i, p in enumerate(G[r2]):
                   for j, v in enumerate(p):
                       if v == r1:
                          pos[r1].append((r2, i, j))
    for rule in rules:
        fll = _follow(G, fne, rule, fll, pos, S)
    return fll

def _follow(G, fne, rule, fll, pos, S):
    s = []
    try:
      s = fll[rule]
      if rule == S:
         raise KeyError
    except KeyError:
      for p in pos[rule]:
          prod = G[p[0]][p[1]]
          if p[2] < len(prod)-1:
             if prod[p[2]+1] in G.keys():
                s += filter(lambda x: x != u'EPSILON', fne[prod[p[2]+1]])
                if u'EPSILON' in fne[prod[p[2]+1]]:
                   fll = _follow(G, fne, p[0], fll, pos, S)
                   s += fll[p[0]]
             else:
                s.append(prod[p[2]+1])
          else:
             fll = _follow(G, fne, p[0], fll, pos, S)
             s += fll[p[0]]
    fll[rule] = list(set(s))
    return fll





