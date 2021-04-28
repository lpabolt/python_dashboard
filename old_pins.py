with open ("@oldnail.asc", "r") as myfile:
    data=myfile.readlines()
data = [w.replace('\n', '') for w in data]
data.append("")

top_1 = 0
top_2 = 0
top_3 = 0
top_4 = 0
bottom_1 = 0
bottom_2 = 0
bottom_3 = 0
bottom_4 = 0

for index,everything in enumerate(data):
    if index > 6:
        if everything != "":
            holder = everything.split()
            if holder[5] == "(T)":
                if holder[3] == '4':
                    top_4 += 1
                else:
                    if holder[3] == '3':
                        top_3 += 1
                    else:
                        if holder[3] == '2':
                            top_2 += 1
                        else:
                            top_1 += 1
            else:
                if holder[3] == '4':
                    bottom_4 += 1
                else:
                    if holder[3] == '3':
                        bottom_3 += 1
                    else:
                        if holder[3] == '2':
                            bottom_2 += 1
                        else:
                            bottom_1 += 1
print("BOTTOM\n\n100thou: " + str(bottom_1) + "\n75thou: " + str(bottom_2) + "\n50thou: " + str(bottom_3) \
                + "\n39thou: " + str(bottom_4) + "\n\nTOP\n\n100thou: " + str(top_1) +"\n75thou: " + str(top_2) \
                + "\n50thou: " + str(top_3) + "\n39thou: " + str(top_4))
        
