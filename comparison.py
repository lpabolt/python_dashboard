from time import strftime
import itertools
import collections
import sys
from re import compile, split

## FOR NATURAL SORT
dre = compile(r'(\d+)')

flnm = "comparison_report"

with open('OUTPUTS/v1.asc') as f:
    original = f.readlines()
original = [w.replace('\n', '') for w in original]
original.append('')

with open('OUTPUTS/v2.asc') as f:
    new = f.readlines()
new = [w.replace('\n', '') for w in new]
new.append('')

original_slctd_prts = original[2].index('/')
new_slctd_prts = new[2].index('/')

original_bttm = {}
original_top = {}
new_bttm = {}
new_top = {}

top_for_single_pin = []
bottom_for_single_pin = []

original_comp_signal = {}
new_comp_signal = {}
new_comp_signal_set = []

##  ORIGINAL

parts_num = []

while (original[2][original_slctd_prts] != " "):
    parts_num.insert(0, original[2][original_slctd_prts])
    original_slctd_prts = original_slctd_prts - 1
    
parts_num.remove('/')
parts_num = ''.join(str(e) for e in parts_num)
original_parts_num = parts_num

## change this to be flexible
line_pos = 8

x_coords = []
y_coords = []

x_y_signal_list_top = []
x_y_signal_list_bttm = []
component_list = []

old_signal = []
new_signal = []
old_signal_pin_num = []
new_signal_pin_num = []


merged = list(itertools.chain(*original))
joined = ''.join(merged)
outer_inc = (joined.count("Part") - 3)
merged = None
joined = None
not_first_line = 0
initial_add = 0

while (outer_inc > 0):
    if (not_first_line == 0):
        if (original[line_pos][-3:] == "(T)"):
            key_num = str(original[line_pos].strip("(T)").strip("Part "))
            where = 1
        else:
            key_num = original[line_pos].strip("(B)").strip("Part ")
            where = 0
        line_pos += 1
        not_first_line = 1
    else:
        while (original[line_pos] != ""):
            if (where == 0):
                if (initial_add == 0):
                    original_bttm.update({key_num: [original[line_pos].split()]})
                    original_comp_signal.update({key_num: [original[line_pos].split()[5]]})
                    x_coords.append(original[line_pos].split()[2])
                    y_coords.append(original[line_pos].split()[3])
                    old_signal.append(original[line_pos].split()[5])
                    initial_add = 1
                else:
                    original_bttm[key_num].append([original[line_pos].split()])
                    original_comp_signal[key_num].append(original[line_pos].split()[5])
                    x_coords.append(original[line_pos].split()[2])
                    y_coords.append(original[line_pos].split()[3])
                    old_signal.append(original[line_pos].split()[5])
            else:
                if (initial_add == 0):
                    original_top.update({key_num: [original[line_pos].split()]})
                    original_comp_signal.update({key_num: [original[line_pos].split()[5]]})
                    x_coords.append(original[line_pos].split()[2])
                    y_coords.append(original[line_pos].split()[3])
                    old_signal.append(original[line_pos].split()[5])
                    initial_add = 1
                else:
                    original_top[key_num].append([original[line_pos].split()])
                    original_comp_signal[key_num].append(original[line_pos].split()[5])
                    x_coords.append(original[line_pos].split()[2])
                    y_coords.append(original[line_pos].split()[3])
                    old_signal.append(original[line_pos].split()[5])
            line_pos += 1
        else:
            not_first_line = 0
            outer_inc -= 1
            initial_add = 0
            pin_num = 1
    line_pos += 1

original_min_x = min(x_coords)
original_max_x = max(x_coords)
original_min_y = min(y_coords)
original_max_y = max(y_coords)

##  NEW    
parts_num = []

while (new[2][new_slctd_prts] != " "):
    parts_num.insert(0, new[2][new_slctd_prts])
    new_slctd_prts = new_slctd_prts - 1
    
parts_num.remove('/')
parts_num = ''.join(str(e) for e in parts_num)
new_parts_num = parts_num

## change this to be flexible
line_pos = 8

x_coords = []
y_coords = []

merged = list(itertools.chain(*new))
joined = ''.join(merged)
outer_inc = (joined.count("Part") - 3)
merged = None
joined = None
not_first_line = 0
initial_add = 0

while (outer_inc > 0):
    if (not_first_line == 0):
        if (new[line_pos][-3:] == "(T)"):
            key_num = str(new[line_pos].strip("(T)").strip("Part "))
            where = 1
        if (new[line_pos][-3:] == "(B)"):
            key_num = str(new[line_pos].strip("(B)").strip("Part "))
            where = 0
        line_pos += 1
        not_first_line = 1
    else:
        while (new[line_pos] != ""):
            if (where == 0):
                if (initial_add == 0):
                    new_bttm.update({key_num: [new[line_pos].split()]})
                    new_comp_signal.update({key_num: [new[line_pos].split()[5]]})
                    x_coords.append(new[line_pos].split()[2])
                    y_coords.append(new[line_pos].split()[3])
                    new_signal.append(new[line_pos].split()[5])
                    initial_add = 1
                else:
                    new_bttm[key_num].append([new[line_pos].split()])
                    new_comp_signal[key_num].append(new[line_pos].split()[5])
                    x_coords.append(new[line_pos].split()[2])
                    y_coords.append(new[line_pos].split()[3])
                    new_signal.append(new[line_pos].split()[5])
            else:
                if (initial_add == 0):
                    new_top.update({key_num: [new[line_pos].split()]})
                    new_comp_signal.update({key_num: [new[line_pos].split()[5]]})
                    x_coords.append(new[line_pos].split()[2])
                    y_coords.append(new[line_pos].split()[3])
                    new_signal.append(new[line_pos].split()[5])
                    initial_add = 1
                else:
                    new_top[key_num].append([new[line_pos].split()])
                    new_comp_signal[key_num].append(new[line_pos].split()[5])
                    x_coords.append(new[line_pos].split()[2])
                    y_coords.append(new[line_pos].split()[3])
                    new_signal.append(new[line_pos].split()[5])
            line_pos += 1
        else:
            not_first_line = 0
            outer_inc -= 1
            initial_add = 0
    line_pos += 1

new_min_x = min(x_coords)
new_max_x = max(x_coords)
new_min_y = min(y_coords)
new_max_y = max(y_coords)

brand_new_signals = []
new_new_signals = []
removed_signals = []

for all_of_them in new_signal:
    if all_of_them not in old_signal:
        brand_new_signals.append(all_of_them)
brand_new_signals = set(brand_new_signals)

for all_of_them in old_signal:
    if all_of_them not in new_signal:
        removed_signals.append(all_of_them)
removed_signals = set(removed_signals)

#### analysis

original_top_keys = original_top.keys()
new_top_keys = new_top.keys()
original_bttm_keys = original_bttm.keys()
new_bttm_keys = new_bttm.keys()
on_new_not_orig_top = []
on_new_not_orig_bttm = []
rmvd_top = []
rmvd_bttm = []
bttm_check_on_new_not_orig_top = []
changed_to_top = []
changed_to_bottom = []

##list_inc = 0
##        while (list_inc < len(original_top[key_ids_top[i]])):
##            if (list_inc == 0):
##                if original_top[key_ids_top[i]][0][2] != new_top[key_ids_top[i]][0][2] or \
##                   original_top[key_ids_top[i]][0][3] != new_top[key_ids_top[i]][0][3]:
##                    output_file.write("                " + str('   '.join(original_top[key_ids_top[i]][0])) + "\n")
##            else:
##                if original_top[key_ids_top[i]][list_inc][0][2] != new_top[key_ids_top[i]][list_inc][0][2] or \
##                   original_top[key_ids_top[i]][list_inc][0][3] != new_top[key_ids_top[i]][list_inc][0][3]:
##                    output_file.write("                " + str('   '.join(original_top[key_ids_top[i]][list_inc][0])) + "\n")
##            list_inc += 1

old_nets = []
for everything in original_bttm:
    list_inc = 0
    while list_inc < len(original_bttm[everything]):
        if list_inc == 0:
            old_nets.append(str(original_bttm[everything][0][5]) + "   " + str(everything) + "." + str(list_inc + 1) + "   " + \
                                str(original_bttm[everything][0][2]) + "   " + str(original_bttm[everything][0][3]) + "   (B)")
        list_inc += 1

for everything in original_top:
    list_inc = 0
    while list_inc < len(original_top[everything]):
        if list_inc == 0:
            old_nets.append(str(original_top[everything][0][5]) + "   " + str(everything) + "." + str(list_inc + 1) + "   " + \
                                str(original_top[everything][0][2]) + "   " + str(original_top[everything][0][3]) + "   (T)")
        else:
            old_nets.append(str(original_top[everything][list_inc][0][5]) + "   " + str(everything) + "." + str(list_inc + 1) + "   " + \
                                str(original_top[everything][list_inc][0][2]) + "   " + str(original_top[everything][list_inc][0][3]) + "   (T)")
        list_inc += 1

old_nets.sort(key=lambda l: [int(s) if s.isdigit() else s.lower() for s in split(dre, l)])
old_nets_file = open("OUTPUTS/v1_nets.asc", "w+")
old_nets_dict = {}
for everything in old_nets:
    holder = everything.split()
    if holder[0] not in old_nets_dict.keys():
        old_nets_dict.update({holder[0]: [holder[1]]})
    else:
        old_nets_dict[holder[0]].append(holder[1])
    old_nets_file.write(str(everything) + "\n")
old_nets_file.close()

new_nets = []
for everything in new_bttm:
    list_inc = 0
    while list_inc < len(new_bttm[everything]):
        if list_inc == 0:
            new_nets.append(str(new_bttm[everything][0][5]) + "   " + str(everything) + "." + str(list_inc + 1) + "   " + \
                                str(new_bttm[everything][0][2]) + "   " + str(new_bttm[everything][0][3]) + "   (B)")
        else:
            new_nets.append(str(new_bttm[everything][list_inc][0][5]) + "   " + str(everything) + "." + str(list_inc + 1) + "   " + \
                                str(new_bttm[everything][list_inc][0][2]) + "   " + str(new_bttm[everything][list_inc][0][3]) + "   (B)")
        list_inc += 1
for everything in new_top:
    list_inc = 0
    while list_inc < len(new_top[everything]):
        if list_inc == 0:
            new_nets.append(str(new_top[everything][0][5]) + "   " + str(everything) + "." + str(list_inc + 1) + "   " + \
                                str(new_top[everything][0][2]) + "   " + str(new_top[everything][0][3]) + "   (T)")
        else:
            new_nets.append(str(new_top[everything][list_inc][0][5]) + "   " + str(everything) + "." + str(list_inc + 1) + "   " + \
                                str(new_top[everything][list_inc][0][2]) + "   " + str(new_top[everything][list_inc][0][3]) + "   (T)")
        list_inc += 1

new_nets.sort(key=lambda l: [int(s) if s.isdigit() else s.lower() for s in split(dre, l)])
new_nets_file = open("OUTPUTS/v2_nets.asc", "w+")
new_nets_dict = {}
for everything in new_nets:
    holder = everything.split()
    if holder[0] not in new_nets_dict.keys():
        new_nets_dict.update({holder[0]: [holder[1]]})
    else:
        new_nets_dict[holder[0]].append(holder[1])
    new_nets_file.write(str(everything) + "\n")
new_nets_file.close()

output_file = open("OUTPUTS/" + str(flnm) + ".asc", "w+")

## the below dictionaries hold queries
prospective_new_comp_top_2_pins = {}
prospective_new_comp_top_1_pin = {}
prospective_new_comp_bttm_2_pins = {}
prospective_new_comp_bttm_1_pin = {}
prospective_rmvd_comp_top_2_pins = {}
prospective_rmvd_comp_top_1_pin = {}
prospective_rmvd_comp_bttm_2_pins = {}
prospective_rmvd_comp_bttm_1_pin = {}
prospective_pin_num_top_2_pins = {}
prospective_pin_num_top_1_pin = {}
prospective_pin_num_bttm_2_pins = {}
prospective_pin_num_bttm_1_pin = {}

## the below dictionaries hold verifications
x_y_signal_same_top = {}
x_y_signal_same_bttm = {}

##  CHANGES IN COMPONENT BOARD (TOP)
for everything in original_top_keys:
    if everything in new_bttm_keys:
        changed_to_bottom.append(everything)

##  CHANGES IN COMPONENT BOARD (BOTTOM)
for everything in original_bttm_keys:
    if everything in new_top_keys:
        changed_to_top.append(everything)

for new_comps in new_top_keys:
    if new_comps not in original_top_keys:
        if new_comps not in original_bttm_keys:
            on_new_not_orig_top.append(new_comps)
on_new_not_orig_top.sort()

for new_comps in new_bttm_keys:
    if new_comps not in original_bttm_keys:
        if new_comps not in original_top_keys:
            on_new_not_orig_bttm.append(new_comps)
on_new_not_orig_bttm.sort()

for bttm_not_on_orig in on_new_not_orig_top:
    if bttm_not_on_orig in original_bttm_keys:
        if bttm_not_on_orig in original_top_keys:
            bttm_check_on_new_not_orig_top.append(bttm_not_on_orig)
            on_new_not_orig_top.remove(bttm_not_on_orig)
bttm_check_on_new_not_orig_top.sort()

if (len(on_new_not_orig_top) > 0):
    if (len(on_new_not_orig_top) != 0):
        for otpt in on_new_not_orig_top:
            initial_add_top_new = 0
            if (len(new_top[otpt]) > 1):
                if (initial_add_top_new == 0):
                    prospective_new_comp_top_2_pins.update({otpt: [new_top[otpt]]})
                    initial_add_top_new += 1
                else:
                    prospective_new_comp_top_2_pins[otpt].append([new_top[otpt]])
        for otpt in on_new_not_orig_top:
            initial_add_top_new = 0
            if (len(new_top[otpt]) == 1):
                if initial_add_top_new == 0:
                    prospective_new_comp_top_1_pin.update({otpt: [new_top[otpt]]})
                    initial_add_top_new += 1
                else:
                    prospective_new_comp_top_1_pin[otpt].append([new_top[otpt]])

if (len(on_new_not_orig_bttm) > 0):
    if (len(on_new_not_orig_bttm) != 0):
        for otpt in on_new_not_orig_bttm:
            initial_add_bottom_new = 0
            if (len(new_bttm[otpt]) > 1):
                if (initial_add_bottom_new == 0):
                    prospective_new_comp_bttm_2_pins.update({otpt: new_bttm[otpt]})
                    initial_add_bottom_new += 1
                else:
                    prospective_new_comp_bttm_2_pins[otpt].append(new_bttm[otpt])
            else:
                prospective_new_comp_bttm_1_pin.update({otpt: new_bttm[otpt]})
        
        for otpt in on_new_not_orig_bttm:
            if (len(new_bttm[otpt]) == 1):
                if (initial_add_bottom_new == 0):
                    if otpt not in prospective_new_comp_bttm_1_pin:
                        prospective_new_comp_bttm_1_pin.update({otpt: new_bttm[otpt]})
                        initial_add_bottom_new += 1
                else:
                    prospective_new_comp_bttm_1_pin[otpt].append(new_bttm[otpt])

for removed_top in original_top_keys:
    if removed_top not in new_top_keys:
        if removed_top not in new_bttm_keys:
            rmvd_top.append(removed_top)
rmvd_top.sort()

for removed_bottom in original_bttm_keys:
    if removed_bottom not in new_bttm_keys:
        if removed_bottom not in new_top_keys:
            rmvd_bttm.append(removed_bottom)
rmvd_bttm.sort()

## REMOVED TOP
if (len(rmvd_top) != 0):
    for otpt in rmvd_top:
        initial_add_top_rmv = 0
        if (len(original_top[otpt]) > 1):
            if (initial_add_top_rmv == 0):
                prospective_rmvd_comp_top_2_pins.update({otpt: original_top[otpt]})
                initial_add_top_rmv += 1
            else:
                prospective_rmvd_comp_top_2_pins[otpt].append([original_top[otpt].split()])
    for otpt in rmvd_top:
        initial_add_top_rmv = 0
        if (len(original_top[otpt]) == 1):
            if (initial_add_top_rmv == 0):
                prospective_rmvd_comp_top_1_pin.update({otpt: original_top[otpt]})
                initial_add_top_rmv += 1
            else:
                prospective_rmvd_comp_top_1_pin[otpt].append([original_top[otpt].split()])

## *****REMOVED BOTTOM
if (len(rmvd_bttm) != 0):
    for otpt in rmvd_bttm:
        initial_add_bttm_rmv = 0
        if (len(original_bttm[otpt]) > 1):
            if (initial_add_bttm_rmv == 0):
                prospective_rmvd_comp_bttm_2_pins.update({otpt: original_bttm[otpt]})
                initial_add_bttm_rmv += 1
            else:
                prospective_rmvd_comp_bttm_2_pins[otpt].append([original_bttm[otpt].split()])
    for otpt in rmvd_bttm:
        initial_add_bttm_rmv = 0
        if (len(original_bttm[otpt]) == 1):
            if (initial_add_bttm_rmv == 0):
                prospective_rmvd_comp_bttm_1_pin.update({otpt: original_bttm[otpt]})
                initial_add_bttm_rmv += 1
            else:
                prospective_rmvd_comp_bttm_1_pin[otpt].append([original_bttm[otpt].split()])

## vvvvvvvvvvvvvvvvvvvvvvvvvvvv PARTS DIFFERENCE OUTPUT vvvvvvvvvvvvvvvvvvvvvvvvvvvv

##if (original_parts_num != new_parts_num):
##    if (original_parts_num > new_parts_num):
##        diff_num = "-" + str(int(original_parts_num) - int(new_parts_num))
##    else:
##        diff_num = "+" + str(int(new_parts_num) - int(original_parts_num))
##    output_file.write("DIFFERENCE IN PARTS: " + str (diff_num) + "\n")
##    output_file.write("    ORIGINAL: " + str (original_parts_num) + "\n    NEW: " + str(new_parts_num) + "\n\n")
                

## PARTS DIFFERENCE OUTPUT ENDS
    

## vvvvvvvvvvvvvvvvvvvvvvvvvvvv MOVED INPUT vvvvvvvvvvvvvvvvvvvvvvvvvvvv

key_ids_top = []
key_ids_bttm = []
key_ids_top_not_found = []
key_ids_bttm_not_found = []
inc = 0

for moved_xy in new_top_keys:
    list_inc = 0
    while (list_inc < len(new_top[moved_xy])):
        if (list_inc == 0):
            new_x_coord = new_top[moved_xy][0][2]
            new_y_coord = new_top[moved_xy][0][3]
        else:
            new_x_coord = new_top[moved_xy][list_inc][0][2]
            new_y_coord = new_top[moved_xy][list_inc][0][3]
        if moved_xy in original_top_keys:
            if (list_inc == 0):
                old_x_coord = original_top[moved_xy][0][2]
                old_y_coord = original_top[moved_xy][0][3]
                if (new_x_coord != old_x_coord):
                    key_ids_top.append(moved_xy)
                if (new_y_coord != old_y_coord):
                    key_ids_top.append(moved_xy)
            else:
                old_x_coord = original_top[moved_xy][list_inc][0][2]
                old_y_coord = original_top[moved_xy][list_inc][0][3]
                if (new_x_coord != old_x_coord):
                    key_ids_top.append(moved_xy)
                if (new_y_coord != old_y_coord):
                    key_ids_top.append(moved_xy)
            list_inc += 1
        else:
            list_inc += 1
key_ids_top = list(set(key_ids_top))

for moved_xy in new_bttm_keys:
    list_inc = 0
    while (list_inc < len(new_bttm[moved_xy])):
        if (list_inc == 0):
            new_x_coord = new_bttm[moved_xy][0][2]
            new_y_coord = new_bttm[moved_xy][0][3]
        else:
            new_x_coord = new_bttm[moved_xy][list_inc][0][2]
            new_y_coord = new_bttm[moved_xy][list_inc][0][3]
        if moved_xy in original_bttm_keys:
            if (list_inc == 0):
                old_x_coord = original_bttm[moved_xy][0][2]
                old_y_coord = original_bttm[moved_xy][0][3]
                if (new_x_coord != old_x_coord):
                    key_ids_bttm.append(moved_xy)
                if (new_y_coord != old_y_coord):
                    key_ids_bttm.append(moved_xy)
            else:
                old_x_coord = original_bttm[moved_xy][list_inc][0][2]
                old_y_coord = original_bttm[moved_xy][list_inc][0][3]
                if (new_x_coord != old_x_coord):
                    key_ids_bttm.append(moved_xy)
                if (new_y_coord != old_y_coord):
                    key_ids_bttm.append(moved_xy)
            list_inc += 1
        else:
            list_inc += 1
key_ids_bttm = list(set(key_ids_bttm))

output_file.write("MOVED COMPONENTS: " + str(len(key_ids_top) + len(key_ids_bttm)) + "\n")

for everything in key_ids_top:
    original_moved = []
    new_moved = []
    for all_things in original_top[everything]:
        original_moved.append(all_things)
    for all_things in new_top[everything]:
        new_moved.append(all_things)
    for nums,third_things in enumerate(original_moved):
        if nums == 0:
            output_file.write("   Was #" + str(everything) + "-" + str(third_things[1]) + ",   X" + str(third_things[2]) + ",   Y" + str(third_things[3]) + "   (T)\n")
            output_file.write("   Now #" + str(everything) + "-" + str(new_moved[nums][1]) + ",   X" + str(new_moved[nums][2]) + ",   Y" + str(new_moved[nums][3]) + "   (T)\n")
        else:
            output_file.write("   Was #" + str(everything) + "-" + str(third_things[0][1]) + ",   X" + str(third_things[0][2]) + ",   Y" + str(third_things[0][3]) + "   (T)\n")
            output_file.write("   Now #" + str(everything) + "-" + str(new_moved[nums][0][1]) + ",   X" + str(new_moved[nums][0][2]) + ",   Y" + str(new_moved[nums][0][3]) + "   (T)\n")
    output_file.write("\n")

for everything in key_ids_bttm:
    original_moved = []
    new_moved = []
    for all_things in original_bttm[everything]:
        original_moved.append(all_things)
    for all_things in new_bttm[everything]:
        new_moved.append(all_things)
    for nums,third_things in enumerate(original_moved):
        if nums == 0:
            output_file.write("   Was #" + str(everything) + "-" + str(third_things[1]) + ",   X" + str(third_things[2]) + ",   Y" + str(third_things[3]) + "   (B)\n")
            output_file.write("   Now #" + str(everything) + "-" + str(new_moved[nums][1]) + ",   X" + str(new_moved[nums][2]) + ",   Y" + str(new_moved[nums][3]) + "   (B)\n")
        else:
            output_file.write("   Was #" + str(everything) + "-" + str(third_things[0][1]) + ",   X" + str(third_things[0][2]) + ",   Y" + str(third_things[0][3]) + "   (B)\n")
            output_file.write("   Now #" + str(everything) + "-" + str(new_moved[nums][0][1]) + ",   X" + str(new_moved[nums][0][2]) + ",   Y" + str(new_moved[nums][0][3]) + "   (B)\n")
    output_file.write("\n")


## str(len(new_bttm[key_ids_bttm[i]]))  FOR NUMBER OF PINS

##key_ids_top.sort()
##key_ids_bttm.sort()
##
##for everything in key_ids_top:
##    for nums,all_things in enumerate(original_top[everything]):
##        line_num = 0
##        if line_num == 0:
##            output_file.write("   Was #" + str(everything) + "-" + str(nums + 1) + ",   X" + str(all_things[2]) + ",   Y" + str(all_things[3]) + "\n")
##            for nums_other,all_other_things in enumerate(new_top[everything]):
##                print (all_other_things[1])
####                if all_other_things[1] == str(line_num + 1):
####                    output_file.write("   Now #" + str(everything) + "-" + str(nums + 1) + ",   X" + str(all_other_things[2]) + ",   Y" + str(all_other_things[3]) + "\n")
####            line_num += 1
####        else:
####            output_file.write("   Was #" + str(everything) + "-" + str(nums + 1) + ",   X" + str(all_things[0][2]) + ",   Y" + str(all_things[0][3]) + "\n")
####            for nums_other,all_other_things in enumerate(new_top[everything]):
####                if all_other_things[1] == str(nums + 1):
####                    output_file.write("   Now #" + str(everything) + "-" + str(nums + 1) + ",   X" + str(all_other_things[0][2]) + ",   Y" + str(all_other_things[0][3]) + "\n")
##            line_num += 1
##    output_file.write("\n")

##original_moved = []
##new_moved = []
##
##if (len(key_ids_top) > 0):
##    if inc == 0:
##        None
##        ##output_file.write("    TOP OF BOARD: " + str(len(key_ids_top)) + "\n")
##    for i in range(0,len(key_ids_top)):
##        output_file.write("        " + str(key_ids_top[i]) + "\n            ORIGINAL:\n")
##        list_inc = 0
##        while (list_inc < len(original_top[key_ids_top[i]])):
##            if (list_inc == 0):
##                if original_top[key_ids_top[i]][0][2] != new_top[key_ids_top[i]][0][2] or \
##                   original_top[key_ids_top[i]][0][3] != new_top[key_ids_top[i]][0][3]:
##                    original_moved.append("   Was #" + str('   '.join(original_top[key_ids_top[i]][0])))
##            else:
##                if original_top[key_ids_top[i]][list_inc][0][2] != new_top[key_ids_top[i]][list_inc][0][2] or \
##                   original_top[key_ids_top[i]][list_inc][0][3] != new_top[key_ids_top[i]][list_inc][0][3]:
##                    original_moved.append("   Was #" + str('   '.join(original_top[key_ids_top[i]][list_inc][0])) + "\n")
##            list_inc += 1
##        list_inc = 0
##        output_file.write("            NEW:\n")
##        while (list_inc < len(new_top[key_ids_top[i]])):
##            if (list_inc == 0):
##                if original_top[key_ids_top[i]][0][2] != new_top[key_ids_top[i]][0][2] or \
##                   original_top[key_ids_top[i]][0][3] != new_top[key_ids_top[i]][0][3]:
##                    print (new_top[key_ids_top[i]][0])
##                    ##new_moved.append("   Now #" + str('   '.join(new_top[key_ids_top[i]][0])) + "\n")
##            else:
##                if original_top[key_ids_top[i]][list_inc][0][2] != new_top[key_ids_top[i]][list_inc][0][2] or \
##                   original_top[key_ids_top[i]][list_inc][0][3] != new_top[key_ids_top[i]][list_inc][0][3]:
##                    print (new_top[key_ids_top[i]][list_inc][0])
##                    ##new_moved.append("   Now #" + str('   '.join(new_top[key_ids_top[i]][list_inc][0])) + "\n")
##            list_inc += 1

##print (new_moved)

##inc = 0
##if (len(key_ids_bttm) > 0):
##    if inc == 0:
##        output_file.write("    BOTTOM OF BOARD: " + str(len(key_ids_bttm)) + "\n")
##    for i in range(0,len(key_ids_bttm)):
##        output_file.write("        " + str(key_ids_bttm[i]) + "\n            ORIGINAL:\n")
##        list_inc = 0
##        while (list_inc < len(original_bttm[key_ids_bttm[i]])):
##            if (list_inc == 0):
##                if original_bttm[key_ids_bttm[i]][0][2] != new_bttm[key_ids_bttm[i]][0][2] or \
##                   original_bttm[key_ids_bttm[i]][0][3] != new_bttm[key_ids_bttm[i]][0][3]:
##                    output_file.write("                " + str('   '.join(original_bttm[key_ids_bttm[i]][0])) + "\n")
##            else:
##                if original_bttm[key_ids_bttm[i]][list_inc][0][2] != new_bttm[key_ids_bttm[i]][list_inc][0][2] or \
##                   original_bttm[key_ids_bttm[i]][list_inc][0][3] != new_bttm[key_ids_bttm[i]][list_inc][0][3]:
##                    output_file.write("                " + str('   '.join(original_bttm[key_ids_bttm[i]][list_inc][0])) + "\n")
##            list_inc += 1
##        list_inc = 0
##        output_file.write("            NEW:\n")
##        while (list_inc < len(new_bttm[key_ids_bttm[i]])):
##            if (list_inc == 0):
##                if original_bttm[key_ids_bttm[i]][0][2] != new_bttm[key_ids_bttm[i]][0][2] or \
##                   original_bttm[key_ids_bttm[i]][0][3] != new_bttm[key_ids_bttm[i]][0][3]:
##                    output_file.write("                " + str('   '.join(new_bttm[key_ids_bttm[i]][0])) + "\n")
##            else:
##                if original_bttm[key_ids_bttm[i]][list_inc][0][2] != new_bttm[key_ids_bttm[i]][list_inc][0][2] or \
##                   original_bttm[key_ids_bttm[i]][list_inc][0][3] != new_bttm[key_ids_bttm[i]][list_inc][0][3]:
##                    output_file.write("                " + str('   '.join(new_bttm[key_ids_bttm[i]][list_inc][0])) + "\n")
##            list_inc += 1
output_file.write("\n")


## !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!MOVED INPUT ENDS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            


## vvvvvvvvvvvvvvvvvvvvvvvvvvvv PINS COUNT OUTPUT vvvvvvvvvvvvvvvvvvvvvvvvvvvv

## *****THE COUNT OF EACH COMPONENT'S NUMBER OF PINS GOES HERE

key_ids_top = []
key_ids_bttm = []
diff_top = 0
diff_bttm = 0
inc = 0

for diff_pins in new_top_keys:
    if diff_pins in original_top_keys:
        if (len(new_top[diff_pins]) != len(original_top[diff_pins])):
            key_ids_top.append(diff_pins)
            diff_top += 1

for diff_pins in new_bttm_keys:
    if diff_pins in original_bttm_keys:
        if (len(new_bttm[diff_pins]) != len(original_bttm[diff_pins])):
            key_ids_bttm.append(diff_pins)
            diff_bttm += 1

output_file.write("PIN COUNT CHANGES: " + str(diff_top + diff_bttm) + "\n")

for everything in key_ids_top:
    output_file.write("   " + str(everything) + " was " + str(len(original_top[everything])) + "pins now " + str(len(new_top[everything])) + "pin.\n")
for everything in key_ids_bttm:
    output_file.write("   " + str(everything) + " was " + str(len(original_bttm[everything])) + "pins now " + str(len(new_bttm[everything])) + "pin.\n")
output_file.write("\n")
##if (len(key_ids_top) > 0):
##    if inc == 0:
##        output_file.write("    TOP OF BOARD: " + str(diff_top) + "\n")
##    for i in range(0,len(key_ids_top)):
##        output_file.write("        " + str(key_ids_top[i]) + "\n            ORIGINAL: " + str(len(original_top[key_ids_top[i]])) + " pin(s)\n")
##        list_inc = 0
##        while (list_inc < len(original_top[key_ids_top[i]])):
##            if (list_inc == 0):
##                output_file.write("                " + str('   '.join(original_top[key_ids_top[i]][0])) + "\n")
##                list_inc += 1
##            else:
##                output_file.write("                " + str('   '.join(original_top[key_ids_top[i]][list_inc][0])) + "\n")
##                list_inc += 1
##        list_inc = 0
##        output_file.write("            NEW: " + str(len(new_top[key_ids_top[i]])) + " pin(s)\n")
##        while (list_inc < len(new_top[key_ids_top[i]])):
##            if (list_inc == 0):
##                output_file.write("                " + str('   '.join(new_top[key_ids_top[i]][0])) + "\n")
##                list_inc += 1
##            else:
##                output_file.write("                " + str('   '.join(new_top[key_ids_top[i]][list_inc][0])) + "\n")
##                list_inc += 1DIFFERENT NUMBER OF PINS
##
##inc = 0
##if (len(key_ids_bttm) > 0):
##    if inc == 0:
##        output_file.write("    BOTTOM OF BOARD: " + str(diff_top) + "\n")
##    for i in range(0,len(key_ids_bttm)):
##        output_file.write("        " + str(key_ids_bttm[i]) + "\n            ORIGINAL: " + str(len(original_bttm[key_ids_bttm[i]])) + " pin(s)\n")
##        list_inc = 0
##        while (list_inc < len(original_bttm[key_ids_bttm[i]])):
##            if (list_inc == 0):
##                output_file.write("                " + str('   '.join(original_bttm[key_ids_bttm[i]][0])) + "\n")
##                list_inc += 1
##            else:
##                output_file.write("                " + str('   '.join(original_bttm[key_ids_bttm[i]][list_inc][0])) + "\n")
##                list_inc += 1
##        list_inc = 0
##        output_file.write("            NEW: " + str(len(new_bttm[key_ids_bttm[i]])) + " pin(s)\n")
##        while (list_inc < len(new_bttm[key_ids_bttm[i]])):
##            if (list_inc == 0):
##                output_file.write("                " + str('   '.join(new_bttm[key_ids_bttm[i]][0])) + "\n")
##                list_inc += 1
##            else:
##                output_file.write("                " + str('   '.join(new_bttm[key_ids_bttm[i]][list_inc][0])) + "\n")
##                list_inc += 1
##output_file.write("\n")


## PINS COUNT OUTPUT ENDS


## vvvvvvvvvvvvvvvvvvvvvvvvvvvv NEW OUTPUT vvvvvvvvvvvvvvvvvvvvvvvvvvvv


output_file.write("ADDED COMPONENTS: " + str(len(on_new_not_orig_top) \
                                                  + len(on_new_not_orig_bttm)) + "\n")

for everything in on_new_not_orig_top:
    if everything in prospective_new_comp_top_2_pins.keys():
        output_file.write("   " + str(everything) + "   Layer=TOP,   Pins=" + str(len(new_top[everything])) + "\n")
    else:
        if everything in prospective_new_comp_top_1_pin.keys():
            output_file.write("   " + str(everything) + "   Layer=TOP,   Pins=" + str(len(new_top[everything])) + "\n")
for everything in on_new_not_orig_bttm:
    if everything in prospective_new_comp_bttm_2_pins.keys():
        output_file.write("   " + str(everything) + "   Layer=BOTTOM,   Pins=" + str(len(new_bttm[everything])) + "\n")
    else:
        if everything in prospective_new_comp_bttm_1_pin.keys():
            output_file.write("   " + str(everything) + "   Layer=BOTTOM,   Pins=" + str(len(new_bttm[everything])) + "\n")
output_file.write("      (See 'added_deleted_more_detail.asc')\n\n")


## vvvvvvvvvvvvvvvvvvvvvvvvvvvv NEW SIGNALS vvvvvvvvvvvvvvvvvvvvvvvvvvvv

##output_file.write("\nNEW SIGNAL NAMES: " + str(len(brand_new_signals)) + "\n   Please see 'new_signals.asc'")
##
##new_signals = ""
##
##for all_things in brand_new_signals:
##    new_signals += str(str(all_things) + "\n")
##    for k in new_top:
##        new_index = 0
##        for v in new_top[k]:
##            if new_index == 0:
##                if all_things in v:
##                    new_signals += str("   " + str (k) + "." + str(new_index + 1) + "\n")
##                    ##output_file.write("\n        " + str (k) + "." + str(new_index + 1))
##            else:
##                if all_things in v[0]:
##                    new_signals += str("   " + str (k) + "." + str(new_index + 1) + "\n")
##                    ##output_file.write("\n        " + str (k) + "." + str(new_index + 1))
##            new_index += 1
##    for k in new_bttm:
##        new_index = 0
##        for v in new_bttm[k]:
##            if new_index == 0:
##                if all_things in v:
##                    new_signals += str("   " + str (k) + "." + str(new_index + 1) + "\n")
##                    ##output_file.write("\n        " + str (k) + "." + str(new_index + 1))
##            else:
##                if all_things in v[0]:
##                    new_signals += str("   " + str (k) + "." + str(new_index + 1) + "\n")
##                    ##output_file.write("\n        " + str (k) + "." + str(new_index + 1))
##            new_index += 1
##
##output_file.write("\n\n")

## ^^^^^^^^^^^^^^^^^^^^^^^^^^^ NEW SIGNALS ENDS ^^^^^^^^^^^^^^^^^^^^^^^^


## vvvvvvvvvvvvvvvvvvvvvvvvvvvv REMOVED SIGNALS vvvvvvvvvvvvvvvvvvvvvvvvvvvv

##output_file.write("REMOVED SIGNAL NAMES: " + str(len(removed_signals)))
##
##for all_things in removed_signals:
##    output_file.write("\n    " + str(all_things))
##    for k in original_top:
##        original_index = 0
##        for v in original_top[k]:
##            if original_index == 0:
##                if all_things in v:
##                    output_file.write("\n        " + str (k) + "." + str(original_index + 1))
##            else:
##                if all_things in v[0]:
##                    output_file.write("\n        " + str (k) + "." + str(original_index + 1))
##            original_index += 1
##    for k in original_bttm:
##        original_index = 0
##        for v in original_bttm[k]:
##            if original_index == 0:
##                if all_things in v:
##                    output_file.write("\n        " + str (k) + "." + str(original_index + 1))
##            else:
##                if all_things in v[0]:
##                    output_file.write("\n        " + str (k) + "." + str(original_index + 1))
##            original_index += 1
##
##output_file.write("\n\n")

## ^^^^^^^^^^^^^^^^^^^^^^^^^^^ REMOVED SIGNALS ENDS ^^^^^^^^^^^^^^^^^^^^^^^^


## vvvvvvvvvvvvvvvvvvvvvvvvvvvv CHANGED SIGNALS vvvvvvvvvvvvvvvvvvvvvvvvvvvv

old_nets_comps = []
new_nets_comps = []

for everything in old_nets:
    holder = everything.split()
    old_nets_comps.append(holder[1])
for everything in new_nets:
    holder = everything.split()
    new_nets_comps.append(holder[1])

was = []
now = []
changes_count = 0

for nums,everything in enumerate(old_nets_comps):
    holder = old_nets[nums].split()
    if everything in new_nets_comps:
        second_holder = new_nets[new_nets_comps.index(everything)].split()
        if holder[1] == second_holder[1]:
            if holder[0] != second_holder[0]:
                changes_count += 1
                was.append("   Was #" + str(holder[0]) + ",   " + str(holder[1]) + "\n")
                now.append("   Now #" + str(second_holder[0]) + ",   " + str(second_holder[1]) + "\n\n")

output_file.write("CONNECTIVITY CHANGES: " + str(changes_count) + "\n")

for nums,everything in enumerate(was):
    output_file.write(everything)
    output_file.write(now[nums])

##one_to_check = []
##
##with open('OUTPUTS/v2_nets.asc') as f:
##    new_nets_file = f.readlines()
##new_nets_file = [w.replace('\n', '') for w in new_nets_file]
##
##new_nets_list = []
##
##for everything in new_nets_file:
##    holder = everything.split()
##    new_nets_list.append(holder[0])
##    new_nets_list.append(holder[1])
##
##for everything in old_nets_dict.keys():
##    delete_from = len(old_nets_dict[everything])
##    changed_net = []
##    for all_things in old_nets_dict[everything]:
##        if everything not in new_nets_dict.keys():
##            if all_things in new_nets_list:
##                changed_net.append(new_nets_list[new_nets_list.index(all_things) - 1])
##        else:
##            delete_from -= 1
##    if delete_from == len(old_nets_dict[everything]):
##        None
####        print (set(changed_net))
##
##for everything in old_nets_dict:
####    print (everything)
##    if all_things in third_things:
##        holder = third_things.split()
##    else:
##        one_to_check.append(holder[0])
##
##changed_signal_comp_names = []
##
##for all_things in new_comp_signal.keys():
##    if all_things in original_comp_signal.keys():
##        if set(original_comp_signal[all_things]) != set(new_comp_signal[all_things]):
####            print (set(original_comp_signal[all_things]),set(new_comp_signal[all_things]))
##            orig_signal_list = []
##            new_signal_list = []
##            for numbers,everything in enumerate(original_comp_signal[all_things]):
##                if everything not in new_comp_signal[all_things]:
##                    orig_signal_list.append(original_comp_signal[all_things])
##                    new_signal_list.append(new_comp_signal[all_things][numbers])
####            print (orig_signal_list)
##            for index,everything in enumerate(original_comp_signal[all_things]):
##                if original_comp_signal[all_things][index] != new_comp_signal[all_things][index]:
##                    if new_comp_signal[all_things][index] in brand_new_signals:
##                        changed_signal_comp_names.append(str(all_things) + "." + str(index + 1) + "      WAS: " + \
##                            str(original_comp_signal[all_things][index]) + "   ---   NOW: " + str(new_comp_signal[all_things][index]) + "    <<< NEW NET")
##                    else:
##                        changed_signal_comp_names.append(str(all_things) + "." + str(index + 1) + "      WAS: " + \
##                            str(original_comp_signal[all_things][index]) + "   ---   NOW: " + str(new_comp_signal[all_things][index]))
##
##changed_signal_comp_names.sort(key=lambda l: [int(s) if s.isdigit() else s.lower() for s in split(dre, l)])
##
####output_file.write("\nCHANGED SIGNAL NAMES: " + str(len(changed_signal_comp_names)) + "\n   Please see 'changed_signals.asc'")
##
##changed_signal_str = ""
##changed_signal_list = []
##both_none = []
####print
##for all_things in changed_signal_comp_names:
##    if all_things.count("NONE") != 2:
##        changed_signal_str += str(str(all_things) + "\n")
##        changed_signal_list.append(all_things)
##    else:
##        both_none.append(all_things)
####output_file.write("\n\n")
##
##print (changed_signal_list)

## BOTH NONE SIGNALS FILE WRITE IS DOWN THE BOTTOM AFTER OUTPUT_FILE HAS BEEN CLOSED ##


## ^^^^^^^^^^^^^^^^^^^^^^^^^^^ CHANGED SIGNALS ENDS ^^^^^^^^^^^^^^^^^^^^^^^^


## vvvvvvvvvvvvvvvvvvvvvvvvvv CONNECTIVITY OUTPUT vvvvvvvvvvvvvvvvvvvvvvvvv

connectivity_changes = 0

##old_nets_dict
##new_nets_dict

for everything in old_nets_dict.keys():
    if everything in new_nets_dict.keys():
        if len(old_nets_dict[everything]) != len(new_nets_dict[everything]):
            connectivity_changes += 1
            for all_things in old_nets_dict[everything]:
                None
##print (new_nets_dict.values())

##for everything in new_nets:
    

## ^^^^^^^^^^^^^^^^^^^^^^^^^^^^ CONNECTIVITY ENDS ^^^^^^^^^^^^^^^^^^^^^^^^^


## vvvvvvvvvvvvvvvvvvvvvvvvvvvv REMOVED OUTPUT vvvvvvvvvvvvvvvvvvvvvvvvvvvv

output_file.write("\nREMOVED COMPONENTS: " + str(len(rmvd_top) + len(rmvd_bttm)) + "\n")
removed_top_to_order = []
removed_bttm_to_order = []
largest_name = 0
spaces = "  "
for everything in prospective_rmvd_comp_top_2_pins:
    removed_top_to_order.append("   " + str(everything) + "   Layer=TOP,   Pins=" + str(len(prospective_rmvd_comp_top_2_pins[everything])))
for everything in prospective_rmvd_comp_top_1_pin:
    removed_top_to_order.append("   " + str(everything) + "   Layer=TOP,   Pins=" + str(len(prospective_rmvd_comp_top_1_pin[everything])))
for everything in prospective_rmvd_comp_bttm_2_pins:
    removed_bttm_to_order.append("   " + str(everything) + "   Layer=BOTTOM,   Pins=" + str(len(prospective_rmvd_comp_bttm_2_pins[everything])))
for everything in prospective_rmvd_comp_bttm_1_pin:
    removed_bttm_to_order.append("   " + str(everything) + "   Layer=BOTTOM,   Pins=" + str(len(prospective_rmvd_comp_bttm_1_pin[everything])))

removed_top_to_order.sort(key=lambda l: [int(s) if s.isdigit() else s.lower() for s in split(dre, l)])
removed_bttm_to_order.sort(key=lambda l: [int(s) if s.isdigit() else s.lower() for s in split(dre, l)])

for everything in removed_top_to_order:
    output_file.write(str(everything) + "\n")
for everything in removed_bttm_to_order:
    output_file.write(str(everything) + "\n")
output_file.write("      (See 'added_deleted_more_detail.asc')\n")

removed_top_to_order = None
removed_bttm_to_order = None

## ^^^^^^^^^^^^^^^^^^^^^^^^^^^^ REMOVED OUTPUT ENDS ^^^^^^^^^^^^^^^^^^^^^^^^


output_file.write("\nLAYER CHANGES: " + str(len(changed_to_bottom) + len(changed_to_top)) + "\n")

for everything in changed_to_top:
    output_file.write("   " + str(everything) + " was BOTTOM now TOP.\n")
for everything in changed_to_bottom:
    output_file.write("   " + str(everything) + " was TOP now BOTTOM.\n")
output_file.write("\n")

##line_inc = 0
##
##if (len(changed_to_bottom) + len(changed_to_top)) > 0:
##    for otpt in changed_to_bottom:
##        output_file.write("        " + str(otpt) + "\n            ORIGINAL (TOP):\n")
##        line_inc = 0
##        while line_inc < len(original_top[otpt]):
##            if line_inc == 0:
##                output_file.write("                " + str("   ".join(map(str, original_top[otpt][0]))) + "\n")
##            else:
##                output_file.write("                " + str("   ".join(map(str, original_top[otpt][line_inc][0]))) + "\n")
##            line_inc += 1
##        line_inc = 0
##        output_file.write("            NEW (BOTTOM):\n")
##        while line_inc < len(new_bttm[otpt]):
##            if line_inc == 0:
##                output_file.write("                " + str("   ".join(map(str, new_bttm[otpt][0]))) + "\n")
##            else:
##                output_file.write("                " + str("   ".join(map(str, new_bttm[otpt][line_inc][0]))) + "\n")
##            line_inc += 1
##output_file.write("    BOTTOM TO TOP: " + str(len(changed_to_top)) + "\n")
##
##if (len(changed_to_bottom) + len(changed_to_top)) > 0:
##    for otpt in changed_to_top:
##        output_file.write("        " + str(otpt) + "\n            ORIGINAL (BOTTOM):\n")
##        line_inc = 0
##        while line_inc < len(original_bttm[otpt]):
##            if line_inc == 0:
##                output_file.write("                " + str("   ".join(map(str, original_bttm[otpt][0]))) + "\n")
##            else:
##                output_file.write("                " + str("   ".join(map(str, original_bttm[otpt][line_inc][0]))) + "\n")
##            line_inc += 1
##        line_inc = 0
##        output_file.write("            NEW (TOP):\n")
##        while line_inc < len(new_top[otpt]):
##            if line_inc == 0:
##                output_file.write("                " + str("   ".join(map(str, new_top[otpt][0]))) + "\n")
##            else:
##                output_file.write("                " + str("   ".join(map(str, new_top[otpt][line_inc][0]))) + "\n")
##            line_inc += 1


##     THIS GETS ALL SIGNAL NAMES AND PUTS THEM INTO A FILE.
##     YOU'LL NEED TO ASSIGN WHAT COMPONENTS THEY COME UNDER.
##connections_file = open("connections.asc", "w+")
##
##signals_2_pins = list(set(signals_2_pins))
##signals_2_pins.sort()
##
##for line in signals_2_pins:
##    connections_file.write(str(line) + "\n    COMPONENTS GO HERE\n")

## vvvvvvvvvvvvvvvvvvvvvvvvvvvv RENAMED OUTPUT vvvvvvvvvvvvvvvvvvvvvvvvvvvv

## *****YOU NEED TO CHECK THE NEW AND REMOVED INITIALLY TO SEE IF THEY'VE JUST BEEN RENAMED
## AND REMOVE THEM FROM THE NEW AND REMOVED DICTIONARIES

## IT COULD BE WORTH CREATING A NEW DICTIONARY 

## *****BOTTOM, 2 PINS

orig_x_y_sig_bttm = []
orig_comp_name_bttm = []
orig_x_y_sig_top = []
orig_comp_name_top = []

for index,everything in enumerate(original_bttm):
    if len(original_bttm[everything]) == 1:
        orig_x_y_sig_bttm.append(original_bttm[everything][0][2])
        orig_x_y_sig_bttm.append(original_bttm[everything][0][3])
        orig_x_y_sig_bttm.append(original_bttm[everything][0][5])
        orig_comp_name_bttm.append(everything)
        orig_comp_name_bttm.append(everything)
        orig_comp_name_bttm.append(everything)
for index,everything in enumerate(original_top):
    if len(original_top[everything]) == 1:
        orig_x_y_sig_top.append(original_top[everything][0][2])
        orig_x_y_sig_top.append(original_top[everything][0][3])
        orig_x_y_sig_top.append(original_top[everything][0][5])
        orig_comp_name_top.append(everything)
        orig_comp_name_top.append(everything)
        orig_comp_name_top.append(everything)

##print (orig_x_y_sig_top)

##original_top = {}
##new_bttm = {}
##new_top

##if ((len(prospective_rmvd_comp_bttm_2_pins) + len(prospective_rmvd_comp_bttm_1_pin)) > 0):
##    ## use the keys from both the original file (already assigned above) and the prospective list
##    renamed_bttm_2_pins = prospective_rmvd_comp_bttm_2_pins.keys()
##    for rnm_bttm_2 in original_bttm_keys:
##        starting_inc = 0
##        for two_pin_keys in bottom_2_keys:
##            for rnm_bttm_cycle_2 in new_bttm[two_pin_keys]:
##                if (starting_inc == 0):
##                    rmv_id = rnm_bttm_cycle_2[0]
##                    rmv_x_coord = rnm_bttm_cycle_2[2]
##                    rmv_y_coord = rnm_bttm_cycle_2[3]
##                    rmv_signal = rnm_bttm_cycle_2[5]
##                    starting_inc += 1
##                else:
##                    rmv_id = rnm_bttm_cycle_2[0][0]
##                    rmv_x_coord = rnm_bttm_cycle_2[0][2]
##                    rmv_y_coord = rnm_bttm_cycle_2[0][3]
##                    rmv_signal = rnm_bttm_cycle_2[0][5]
##                for rnm_bttm_cycle_3 in new_bttm:
##                    print (rnm_bttm_cycle_3)

## x_y_signal_same_top = {}
##x_y_signal_same_bttm = {}


output_file.write("\nRENAMED: " + str(len(x_y_signal_same_top) + len(x_y_signal_same_bttm)) + "\n\n")

## ^^^^^^^^^^^^^^^^^^^^^^^^^^ RENAMED OUTPUT ENDS ^^^^^^^^^^^^^^^^^^^^^^^^^^

output_file.close()

output_file = open("OUTPUTS/added_deleted_more_detail.asc", "w+")
output_file.write("_______ADDED COMPONENTS IN MORE DETAIL_______\n\n")
for everything in on_new_not_orig_top:
    output_file.write("* DEVICE DATA IN V2, BUT NOT IN V1 - " + str(everything) + "\n")
    line_num = 0
    for nums,all_things in enumerate(new_top[everything]):
        if line_num == 0:
            output_file.write("    #" + str(all_things[5]) + ", " + str(everything) + "-" + str(nums + 1) + ", X" + str(all_things[2]) + ", Y" + str(all_things[3]) + "\n")
            line_num += 1
        else:
            output_file.write("    #" + str(all_things[0][5]) + ", " + str(everything) + "-" + str(nums + 1) + ", X" + str(all_things[0][2]) + ", Y" + str(all_things[0][3]) + "\n")
            line_num += 1
    output_file.write("\n\n")
    
output_file.write("\n**********************************************************\n\n\n_______REMOVED COMPONENTS IN MORE DETAIL_______\n\n")
for everything in rmvd_top:
    output_file.write("* DEVICE DATA IN V1, BUT NOT IN V2 - " + str(everything) + "\n")
    line_num = 0
    for nums,all_things in enumerate(original_top[everything]):
        if line_num == 0:
            output_file.write("    #" + str(all_things[5]) + ", " + str(everything) + "-" + str(nums + 1) + ", X" + str(all_things[2]) + ", Y" + str(all_things[3]) + "\n")
            line_num += 1
        else:
            output_file.write("    #" + str(all_things[0][5]) + ", " + str(everything) + "-" + str(nums + 1) + ", X" + str(all_things[0][2]) + ", Y" + str(all_things[0][3]) + "\n")
            line_num += 1
    output_file.write("\n\n")
for everything in rmvd_bttm:
    output_file.write("* DEVICE DATA IN V1, BUT NOT IN V2 - " + str(everything) + "\n")
    line_num = 0
    for nums,all_things in enumerate(original_bttm[everything]):
        if line_num == 0:
            output_file.write("    #" + str(all_things[5]) + ", " + str(everything) + "-" + str(nums + 1) + ", X" + str(all_things[2]) + ", Y" + str(all_things[3]) + "\n")
            line_num += 1
        else:
            output_file.write("    #" + str(all_things[0][5]) + ", " + str(everything) + "-" + str(nums + 1) + ", X" + str(all_things[0][2]) + ", Y" + str(all_things[0][3]) + "\n")
            line_num += 1
    output_file.write("\n\n")

##print (rmvd_top)
##rmvd_bttm





##    if everything in prospective_new_comp_top_2_pins.keys():
##        output_file.write("   " + str(everything) + "   Layer=TOP,   Pins=" + str(len(new_top[everything])) + "\n")
##    else:
##        if everything in prospective_new_comp_top_1_pin.keys():
##            output_file.write("   " + str(everything) + "   Layer=TOP,   Pins=" + str(len(new_top[everything])) + "\n")
##for everything in on_new_not_orig_bttm:
##    if everything in prospective_new_comp_bttm_2_pins.keys():
##        output_file.write("   " + str(everything) + "   Layer=BOTTOM,   Pins=" + str(len(new_bttm[everything])) + "\n")
##    else:
##        if everything in prospective_new_comp_bttm_1_pin.keys():
##            output_file.write("   " + str(everything) + "   Layer=BOTTOM,   Pins=" + str(len(new_bttm[everything])) + "\n")
##output_file.write("      (See 'added_deleted_more_detail.asc')\n")

##if len(both_none) > 0:
##    both_none_file = open("OUTPUTS/both_signals_none.asc", "w+")
##    both_none_file.write("LINES IN FILE: " + str(len(both_none)) + "\n\n\n")
##    for both in both_none:
##        both_none_file.write(str(both) + "\n")
##    both_none_file.close()
##
##if new_signals != "":
##    new_signals_file = open("OUTPUTS/new_signals.asc", "w+")
##    new_signals_file.write(new_signals)
##    new_signals_file.close()
##
##if changed_signal_str != "":
##    changed_signals_file = open("OUTPUTS/changed_signals.asc", "w+")
##    changed_signals_file.write(changed_signal_str)
##    changed_signals_file.close()

