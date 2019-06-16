infile = open("emem_table.csv","r")

table = []

for line in infile:
    row = line.split(";")
    table.append(row)
    # print row
    for item in row:
    	print item

print 'DONE '

print table[0][0]
print len(table)
print len(table[0])