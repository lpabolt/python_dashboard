###  YOU HAVE TO ISOLATE THE .pdf PAGES THEN SAVE THEM AS AN EXCEL FILE
###  TO PROPERLY GET THE DATA OUT

## -----------------------------------------------------------

##with open ("connector_pin_numbers_isolated.txt", "r") as myfile:
##    data=myfile.readlines()
##data = [w.replace('\n', '') for w in data]
##data = [w.replace('--', '-') for w in data]
##data = [w.replace('Number  ', '') for w in data]
##data = [w.replace('Number ', '') for w in data]
##data = [w.replace('Connector ', '') for w in data]
##data = [w.replace('Nail ', '') for w in data]

##connector = []
##nail = []
##sring = ""
##counter = 0
##for everything in data:
##    print (everything[counter])
##    counter += 1

## -----------------------------------------------------------

file = open("dump.txt", "r")

nail = {}
sring = ""
counter = 0
for everything in file:
    holder = everything.split()
    if holder[1] in nail:
        nail[holder[1]].append(holder[0])
    else:
        nail.update({holder[1]: [holder[0]]})

for everything in nail.keys():
    nail[everything].sort()

comparison_nails = []
comparison_sort = []

with open ("48972T.NAE", "r") as myfile:
    data=myfile.readlines()
data = [w.replace('\n', '') for w in data]

for index,lines in enumerate(data):
    if index > 19:
        if lines != "":
            holder = lines.split()
            if holder[0] == "@":
                comparison_nails.append(holder[2])

print ("Filename: 48972T.NAE")
for everything in comparison_nails:
    comparison_sort.append(nail[everything])

comparison_sort.sort()

for  index, everything in enumerate(comparison_sort):
    print (str(comparison_nails[index]) + " ---> " + str(everything))
