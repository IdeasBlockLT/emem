infile = open("static/texts/emem_table.csv","r")

table = []

for line in infile:
    row = line.split(";")
    table.append(row)

print 'DONE '

print table[0][0]
print len(table)
print len(table[0])