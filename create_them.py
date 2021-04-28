import sys
from re import compile, split

##sys.argv[1] is the start of the passed variables

with open('OUTPUTS/52823_A-2176-2520-02_Duplication_fix.out') as f:
    original = f.readlines()
original = [w.replace('\n', '') for w in original]
original.append('')

starts = sys.argv[3].split(",")
ends = sys.argv[4].split(",")

hndrd_thou = []
styfv_thou = []
ffty_thou = []
thrtnn_thou = []

for nums,everything in enumerate(starts):
    block_starts = int(everything)
    block_ends = int(ends[nums])
    while block_starts < block_ends:
        holder = original[block_starts].split()
        if holder[4] == "100THOU":
            hndrd_thou.append(original[block_starts])
        else:
            if holder[4] == "75THOU":
                styfv_thou.append(original[block_starts])
        block_starts += 1

excellon = open("OUTPUTS/52823_excellon.asc", "w")

excellon.write("M48\nM47,T01,F090S45S1.4\nM47,T02,F090S45S1.4\nM47,T06,F090S45S1.4\nG92\nMM,TZ\n%")

if len(hndrd_thou) > 0:
    excellon.write("\nT01")
    for everything in hndrd_thou:
        holder = everything.split()
        excellon.write("\nX" + str(holder[0]) + "Y" + str(holder[1]))

if len(styfv_thou) > 0:
    excellon.write("\nT02")
    for everything in styfv_thou:
        holder = everything.split()
        excellon.write("\nX" + str(holder[0]) + "Y" + str(holder[1]))

## OTHER SIZES HERE

excellon.write("\nT00\nM30")
excellon.close()

probexy = open("OUTPUTS/52823_probexy.asc", "w")

inc_int = 1
for nums,everything in enumerate(starts):
    block_starts = int(everything)
    block_ends = int(ends[nums])
    while block_starts < block_ends:
        holder = original[block_starts].split()
        if holder[2] != "T11":
            probexy.write(str(inc_int) + "    " + str(holder[2]) + " " + str(holder[0]) + " " + str(holder[1]) + "\n")
            inc_int += 1
        block_starts += 1

probexy.close()

#################################################################################################################
#################################################################################################################
#################################################################################################################

with open("OUTPUTS/52823_excellon.asc") as f:
    excellon = f.readlines()
excellon = [w.replace('\n', '') for w in excellon]

with open("OUTPUTS/52823_probexy.asc") as f:
    probexy = f.readlines()
probexy = [w.replace('\n', '') for w in probexy]

## FOR NATURAL SORT
dre = compile(r'(\d+)')

t01 = excellon.index("T01") + 1
t02 = excellon.index("T02") + 1

## THIS IS A LIST OF LISTS BUT NOT NESTED FOR EASE. X ARE EVEN AND Y ARE ODD.
xy_list = []

t00 = excellon.index("T00")
##t06 = excellon.index("T06")

file = open("OUTPUTS/52823.scr", "w")

probexy_id = []
probexy_components = []
probexy_x = []
probexy_y = []

list_to_make_dot_numbers_easy = []

initial = 0

## MAKE THIS LOOP SO IT CAPTURES EVERY THOU PROBE

while t01 < (t02 - 1):
    edit = excellon[t01].replace("X","")
    holder = edit.split("Y")
    if initial == 0:
        xy_list.append([holder[0]])
        xy_list.append([holder[1]])
        initial += 1
    else:
        xy_list[0].append(holder[0])
        xy_list[1].append(holder[1])
    search_var = str(holder[0]) + " " + str(holder[1])
    for nums,everything in enumerate(probexy):
        probexy_holder = everything.split()
        if probexy_holder[2] == holder[0]:
            if probexy_holder[3] == holder[1]:
                file.write("_CIRCLE\n" + str(holder[0]) + "," + str(holder[1]) + "\nD\n2.0\n")
                break
    t01 += 1

initial = 0

while t02 < t00:
    edit = excellon[t02].replace("X","")
    holder = edit.split("Y")
    if initial == 0:
        xy_list.append([holder[0]])
        xy_list.append([holder[1]])
        initial += 1
    else:
        xy_list[2].append(holder[0])
        xy_list[3].append(holder[1])
    file.write("_CIRCLE\n" + str(holder[0]) + "," + str(holder[1]) + "\nD\n1.5\n")
    for nums,everything in enumerate(probexy):
        probexy_holder = everything.split()
        if probexy_holder[2] == holder[0]:
            if probexy_holder[3] == holder[1]:
                file.write("_CIRCLE\n" + str(holder[0]) + "," + str(holder[1]) + "\nD\n1.5\n")
                break
    t02 += 1

for nums,everything in enumerate(probexy):
    probexy_holder = everything.split()
    probexy_id.append(probexy_holder[0])
    probexy_components.append(probexy_holder[1])
    probexy_x.append(probexy_holder[2])
    probexy_y.append(probexy_holder[3])

## ADD IN THE TOOLING (T06) HERE

list_to_make_xy_detection_easier = []

component_dict = {}

for nums,everything in enumerate(probexy):
    holder = everything.split()
    component_dict.update({holder[1]: []})
    for numberssss,these_things in enumerate(probexy_y):
        if holder[1] != probexy_components[numberssss]:
            if (abs((float(probexy_y[numberssss]) - 1.1) - float(holder[3]))) < 3:
                if (abs(float(probexy_x[numberssss]) - float(holder[2]))) < 3:
                    component_dict[holder[1]].append(probexy_components[numberssss])

already_done = []

test = 0
counter = 0
while len(component_dict) > 0:
    if test == 2:
        test = 0
    for nums,everything in enumerate(probexy_components):
        if everything in component_dict.keys():
            if len(component_dict[everything]) == counter:
                already_done.append(everything)
                if test == 0:
                    file.write("_LINE\n" + str(probexy_x[nums]) + "," + str(probexy_y[nums]) + "\n" + str(float(probexy_x[nums]) + float(0)) + "," \
                       + str(round(float(probexy_y[nums]) + float(1.2),5)) + "\n\n")
                    file.write("_TEXT\n" + str(round(float(probexy_x[nums]) - ((len(everything) * 0.5) / 1.25),5)) + "," + str(round(float(probexy_y[nums]) + float(1.2),5)) + ",0.0\n1.0\n0.0\n" + str(everything) + "\n")
                else:
                    file.write("_LINE\n" + str(probexy_x[nums]) + "," + str(probexy_y[nums]) + "\n" + str(float(probexy_x[nums]) + float(1.2)) + "," \
                       + str(round(float(probexy_y[nums]) + float(0),5)) + "\n\n")
                    file.write("_TEXT\n" + str(round(float(probexy_x[nums]) - ((len(everything) * 0.5) / 1.25),5)) + "," + str(round(float(probexy_y[nums]) + float(1.2),5)) + ",0.0\n1.0\n0.0\n" + str(everything) + "\n")
    print (test)
    test += 1
    counter += 1
    ##  DELETE THE COMPONENTS ALREADY MAPPED
    delete_this = []
    for everything in component_dict.keys():
        if everything in already_done:
            delete_this.append(everything)
    for everything in delete_this:
        component_dict.pop(everything, None)

##for nums,everything in enumerate(probexy_components):
##    if everything in component_dict.keys():
##        if len(component_dict[everything]) == 0:
##            already_done.append(everything)
##            if test == 0:
##                file.write("_LINE\n" + str(probexy_x[nums]) + "," + str(probexy_y[nums]) + "\n" + str(float(probexy_x[nums]) + float(0)) + "," \
##                   + str(round(float(probexy_y[nums]) + float(1.2),5)) + "\n\n")
##                file.write("_TEXT\n" + str(round(float(probexy_x[nums]) - ((len(everything) * 0.5) / 1.25),5)) + "," + str(round(float(probexy_y[nums]) + float(1.2),5)) + ",0.0\n1.0\n0.0\n" + str(everything) + "\n")
##            else:
##                file.write("_LINE\n" + str(probexy_x[nums]) + "," + str(probexy_y[nums]) + "\n" + str(float(probexy_x[nums]) + float(1.2)) + "," \
##                   + str(round(float(probexy_y[nums]) + float(0),5)) + "\n\n")
##                file.write("_TEXT\n" + str(round(float(probexy_x[nums]) - ((len(everything) * 0.5) / 1.25),5)) + "," + str(round(float(probexy_y[nums]) + float(1.2),5)) + ",0.0\n1.0\n0.0\n" + str(everything) + "\n")
##
####  DELETE THE COMPONENTS ALREADY MAPPED
##delete_this = []
##for everything in component_dict.keys():
##    if everything in already_done:
##        delete_this.append(everything)
##for everything in delete_this:
##    component_dict.pop(everything, None)

file.close()



######################################################################################
## vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv BELOW DONE vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv ###
######################################################################################

##file = open("OUTPUTS/" + str(sys.argv[2]) + ".NAE", "w")
##file.write(str("; Syntax of Nae File\n;\n;@  Nail_no Node_nam     Temp_no    Connector  Second_name\n;\n;\n;X  ") \
##           + str("CNLSCT *Compon.pin  Compon_typ    SMD/NoSMD  X_pos  Y_pos\n;|  |||||| |\n;|  |||||| +----- Ic_Output Flag\n;|  ||||||\n") \
##           + str(";|  |||||+--------  Side (T)op, (B)ottom\n;|  ||||+--------  (C)rown, (P)eak, (W)affle\n") \
##           + str(";|  |||+--------  Wire (S)low, (F)ast (twisted pair)\n;|  ||+--------  Probelength (L)ong, (M)edium, (S)hort\n") \
##           + str(";|  |+--------  Probesize (N)ormal, (M)edium, (S)mall (X) too small\n;|  +--------  Hole (C)omplete, (U)ncomplete, (N)o,\n") \
##           + str(";|                  (M)ultinail, (P)ower/GND-nail, (A)dapternail\n;|                  (Y) disabled Adapter, (Z) disabled Uncomplete\n") \
##           + str(";|                  (Q) Power and Complete, (H) necessary Bridgeelement\n;+-----  Mark for manuell changes \n") \
##           + str(";!-----  Mark for unusable nails  \n;"))
##for nums,everything in enumerate(probexy_id):
##    if probexy_components.count(probexy_components[nums]) == 1:
##        file.write("\n@   F" + str(everything) + "      " + str(probexy_components[nums]) + "        F0     ---    ---              ")
##        file.write("\n    CNSSCT  " + str(everything) + ".1              TESTPAD      NoSMD    " + str(probexy_x[nums]) + "  " + str(probexy_y[nums]) + "\n")
##    else:
##        list_to_make_dot_numbers_easy.append(probexy_components[nums])
##        if list_to_make_dot_numbers_easy.count(probexy_components[nums]) == 1:
##            file.write("\n@   F" + str(everything) + "      " + str(probexy_components[nums]) + "        F0     ---    ---              ")
##        else:
##            file.write("\n@   F" + str(everything) + "      " + str(probexy_components[nums]) + "." \
##                       + str(list_to_make_dot_numbers_easy.count(probexy_components[nums])) + "      F0     ---    ---              ")
##        file.write("\n    CNSSCT  " + str(everything) + ".1              TESTPAD      NoSMD    " \
##                                       + str(probexy_x[nums]) + "  " + str(probexy_y[nums]))
##        for inner,all_things in enumerate(probexy_components):
##            if all_things == probexy_components[nums]:
##                if probexy_id[inner] != everything:
##                    file.write("\n    MNSSCT  " + str(probexy_id[inner]) + ".1              TESTPAD      NoSMD    " \
##                               + str(probexy_x[inner]) + "  " + str(probexy_y[inner]))
##        file.write("\n")
##file.write("\n\n")
##file.close()
##
##file = open("OUTPUTS/" + str(sys.argv[2]) + ".D11", "w")
##holder_to_sort = []
##dls_dupes = 0
##for nums,everything in enumerate(probexy_id):
##    if " X   " + str(probexy_x[nums]) + " Y  " + str(probexy_y[nums]) not in holder_to_sort:
##        holder_to_sort.append(" X   " + str(probexy_x[nums]) + " Y  " + str(probexy_y[nums]))
##    else:
##        dls_dupes += 1
##holder_to_sort.sort(key=lambda l: [int(s) if s.isdigit() else s.lower() for s in split(dre, l)])
##for everything in holder_to_sort:
##    file.write(str(everything) + "\n")
##file.close()
##
##file = open("OUTPUTS/" + str(sys.argv[2]) + ".DLS","w")
##file.write(str("*** Drillfiles Generation Report ***\n====================================\n\nSummary of Drill Files :\n") \
##           + str("\nFilename  Description                Number of holes\n\n*.D11   Normal complete nails                      " + str(len(probexy_id))) \
##           + str("\n-----------------------------------------\nSummary of board holes             : " + str(len(probexy_id)) + "\n") \
##           + str("\n-----------------------------------------\nSummary of adapter interface holes : 0\n\n\n") \
##           + str(str(dls_dupes) + " - double existing coordinates deleted\n\n*** End of Report ***"))
##file.close()
