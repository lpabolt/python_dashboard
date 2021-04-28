from re import compile, split

dre = compile(r'(\d+)')

with open('OUTPUTS/drill.asc') as f:
    drill = f.readlines()
drill = [w.replace('\n', '') for w in drill]
drill.append('')

state = 0

tool_names = []
tool_sizes = []

for everything in drill:
    if state == 0 and everything[0] == "X":
        state = 1
    if state == 0:
        if "Ctr" in everything:
            holder = everything.split(",")
            tool_names.append(holder[1])
            tool_sizes.append(holder[3])

##print (tool_names,tool_sizes)

## this gets the non-blinds
for nums,everything in enumerate(tool_names):
    new_file = open("OUTPUTS/" + str(tool_sizes[nums]) + "_thou.scr", "w+")
    line_start = drill.index(everything)
    for numbers,all_things in enumerate(drill):
        if numbers > line_start:
            if all_things[0] == "T":
                break
            else:
                holder = all_things.replace("X","").replace("+","")
                edit = holder.split("Y")
                new_file.write("_CIRCLE\n" + str(float(edit[0])) + "," + str(float(edit[1])) + "\nD\n1.0\n")
    new_file.close()

line_before_blinds = numbers
blinds_file = open("OUTPUTS/blinds_file.asc", "w+")
for nums,everything in enumerate(drill):
    if nums >= line_before_blinds:
        blinds_file.write(str(everything) + "\n")
blinds_file.close()

with open('OUTPUTS/blinds_file.asc') as f:
    blinds = f.readlines()
blinds = [w.replace('\n', '') for w in blinds]
blinds.append('')

## this gets the blinds
for nums,everything in enumerate(tool_names):
    new_file = open("OUTPUTS/" + str(tool_sizes[nums]) + "_thou_blinds.scr", "w+")
    line_start = blinds.index(everything)
    for numbers,all_things in enumerate(blinds):
        if len(all_things) > 0:
            if numbers > line_start:
                if all_things[0] == "T":
                    break
                else:
                    if all_things[0] == "M":
                        continue
                    else:
                        holder = all_things.replace("X","").replace("+","")
                        edit = holder.split("Y")
                        new_file.write("_CIRCLE\n" + str(float(edit[0])) + "," + str(float(edit[1])) + "\nD\n1.0\n")
    new_file.close()
