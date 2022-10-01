import os
os.chdir('C:\Users\jonat\Documents\Geyser Flats Challenge\Quarestra Savannah')

for xnode in range(1,11,1):
    for ynode in range(1,11,1):
        m = open("node"+xnode+"-"+ynode".md","w")
        for x in range(-1,2,1):
            for y in range(-1,2,1):
                m.write("[[node"+(xnode+x)+"-"+(ynode+y)"]]")
    