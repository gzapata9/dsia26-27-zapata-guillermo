"""Módulo con deuda deliberada para practicar IA asistida."""

# mal: nombres pobres, función larga, side effects mezclados

def f(a):
    # a es un dict con keys u, p
    r=[]
    for i in a:
        u=a[i].get('u')
        p=a[i].get('p')
        if u==None: 
            continue
        if p==None:
            continue
        if u<=0: 
            continue
        if p<=0:
            continue
        r.append(u*p)
    s=0
    for x in r:
        s=s+x
    print('total', s)  # side effect
    return s


def load_and_run(path):
    import json
    data=json.load(open(path))
    return f(data)
