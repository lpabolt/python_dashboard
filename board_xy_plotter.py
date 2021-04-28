import sys

##  GET THE PASSED INPUT/OUTPUT MEASUREMENTS
if sys.argv[2] == "inches":
    if sys.argv[3] == "inches":
        convert_xy = 1
    else:
        if sys.argv[3] == "mm":
            convert_xy = 25.4
        else:
            if sys.argv[3] == "thou":
                convert_xy = 10000
else:
    if sys.argv[2] == "mm":
        if sys.argv[3] == "inches":
            convert_xy = 0.0039370
        else:
            if sys.argv[3] == "mm":
                convert_xy = 1
            else:
                if sys.argv[3] == "thou":
                    convert_xy = 393.701
    else:
        if sys.argv[2] == "thou":
            if sys.argv[3] == "inches":
                convert_xy = 0.0001
            else:
                if sys.argv[3] == "mm":
                    convert_xy = 0.00254
                else:
                    if sys.argv[3] == "thou":
                        convert_xy = 1
        else:
            if sys.argv[2] == "tenthou":
                if sys.argv[3] == "inches":
                    convert_xy = 0.00001
                else:
                    if sys.argv[3] == "mm":
                        convert_xy = 0.000254
                    else:
                        if sys.argv[3] == "thou":
                            convert_xy = 0.1

##  FUNCTION TO EASILY CHECK IF NUMBER IS IN STRING
def num_there(a):
    return any(i.isdigit() for i in a)

##  sys.argv[1] IS BOARD TYPE
if sys.argv[1] == "single":
    
    ######################################################################################################
    ##################################   SINGLE BOARD CODE STARTS HERE   #################################
    ######################################################################################################
    
    with open ("OUTPUTS/board_xy.asc", "r") as myfile:
        data=myfile.readlines()
    data = [w.replace('\n', '') for w in data]
    data = [w.replace("UNITS","units") for w in data]
    indices = [i for i, s in enumerate(data) if 'units' in s]
    data[indices[0]] = "units " + str(sys.argv[3]) + ";"
    myfile.close
    bottom_all = data

    top = 0
    
    ##  REMOVES NO_PROBE LINES
    for index, no_probe in enumerate(bottom_all):
        if no_probe.find(" NO_PROBE") > 0:
            bottom_all[index] = "~"

    for index, no_probe in enumerate(bottom_all):
        if no_probe.find("TOP") > 0:
            bottom_all[index] = "~"
            top += 1

    ##  GETS RID OF DEVICES
    devices_index = bottom_all.index("DEVICES")
    while bottom_all[devices_index] != "":
        bottom_all[devices_index] = "~"
        devices_index += 1

    ##  CREATES bottom.asc
    file = open("OUTPUTS/bottom_" + str(sys.argv[3]) + ".asc", "w")
    outline_check = 0
    tooling_check = 0
    rest_check = 0
    general_line = 1
    no_tooling = 0
    for line_num,everything in enumerate(bottom_all):
        if everything != "~":
            if everything == "OUTLINE":
                file.write(str(everything))
                outline_check = 1
                general_line = 0
            else:
                if everything == "" and outline_check == 1:
                    file.write(str(";\n"))
                    outline_check = 0
                    general_line = 1
                else:
                    if outline_check == 1:
                        edit = everything.replace(";","")
                        edit = edit.replace(",","")
                        holder = edit.split()
                        x_coor = round(float(holder[0]) * convert_xy,5)
                        y_coor = round(float(holder[1]) * convert_xy,5)
                        file.write("\n      " + str(x_coor) + ",    " + str(y_coor))
                        
            if "TOOLING" in bottom_all:
                if everything == "TOOLING":
                    file.write("\n" + str(everything))
                    tooling_check = 1
                    general_line = 0
                else:
                    if everything == "":
                        if tooling_check == 1:
                            file.write("\n")
                        tooling_check = 0
                        general_line = 1
                    else:
                        if tooling_check == 1:
                            edit = everything.replace("2000","")
                            edit = edit.replace(";","")
                            edit = edit.replace(",","")
                            holder = edit.split()
                            file.write("\n    2000      " + str(round(float(holder[0]) * convert_xy,5)) + ",    " \
                                       + str(round(float(holder[1]) * convert_xy,5)) + ";")
            else:
                no_tooling = 1
                
            if "ALTERNATES" in everything:
                loop_index_alternates = line_num
                file.write("\nOTHER\n" + str(everything))
                rest_check = 1
                general_line = 0
            else:
                if everything == "":
                    rest_check = 0
                    general_line = 1
                else:
                    if rest_check == 1:
                        edit = everything.replace(";","")
                        edit = edit.replace(",","")
                        holder = edit.split()
                        file.write("\n            " + str(round(float(holder[0]) * convert_xy,5)) + ",    " \
                                   + str(round(float(holder[1]) * convert_xy,5)) + "        " + str(holder[2]))
                        if len(holder) > 3:
                           file.write(" " + str(holder[3]) + ";")
                        else:
                           file.write(";")
    file.write("\n\n")
    file.close()

    ##  .scr CREATION
    file = open("OUTPUTS/bottom_" + str(sys.argv[3]) + ".scr", "w")
    with open ("OUTPUTS/bottom_" + str(sys.argv[3]) + ".asc", "r") as myfile:
        data=myfile.readlines()
    data = [w.replace('\n', '') for w in data]
    
    ##  OUTLINE
    loop_index = data.index("OUTLINE") + 1
    outline_lines_x = []
    outline_lines_y = []
##    if no_tooling == 0:
##        while_check = "TOOLING"
##    else:
##        while_check = ""
    while data[loop_index] != "":
        edit = data[loop_index].replace(";","")
        edit = edit.replace(",","")
        holder = edit.split()
        file.write("_CIRCLE\n" + str(holder[0]) + "," + str(holder[1]) + "\nD\n1.0\n")
        outline_lines_x.append(holder[0])
        outline_lines_y.append(holder[1])
        loop_index += 1
##    THIS BIT DRAWS LINES BETWEEN THE OUTLINE COORDS BUT CAN'T BE USED ON INCHES, AS THE RESIZE OF MULTIPLE LINE TYPES CAN'T BE DONE
##    last_record = len(outline_lines_x)
##    for nums,everything in enumerate(outline_lines_x):
##        if (nums + 1) != last_record:
##            file.write("_LINE\n" + str(outline_lines_x[nums]) + "," + str(outline_lines_y[nums]) + "\n" + str(outline_lines_x[nums + 1]) + "," + str(outline_lines_y[nums + 1]) + "\n\n")
##        else:
##            file.write("_LINE\n" + str(outline_lines_x[nums]) + "," + str(outline_lines_y[nums]) + "\n" + str(outline_lines_x[0]) + "," + str(outline_lines_y[0]) + "\n\n")
        
            

    ##  TOOLING
    ##  REMEMBER TO CHECK IF THIS IS HERE, DOESN'T HAVE TO BE
    if no_tooling == 0:
        loop_index = data.index("TOOLING") + 1
        while data[loop_index] != "":
            edit = data[loop_index].replace("2000","")
            edit = edit.replace(";","")
            edit = edit.replace(",","")
            holder = edit.split()
            file.write("_CIRCLE\n" + str(holder[0]) + "," + str(holder[1]) + "\nD\n1.0\n")
            loop_index += 1

    ##  REST OF FILE
    while data[loop_index_alternates] != "":
        edit = data[loop_index_alternates].replace(";","")
        edit = edit.replace(",","")
        holder = edit.split()
        file.write("_CIRCLE\n" + str(holder[0]) + "," + str(holder[1]) + "\nD\n1.0\n")
        loop_index_alternates += 1

    file.write("\n")

    if top > 0:
        with open ("OUTPUTS/board_xy.asc", "r") as myfile:
            data=myfile.readlines()
        data = [w.replace('\n', '') for w in data]
        indices = [i for i, s in enumerate(data) if 'units' in s]
        data[indices[0]] = "units " + str(sys.argv[3]) + ";"
        for index, no_probe in enumerate(data):
            if no_probe.find(" NO_PROBE") > 0:
                data[index] = "~"
        loop_index = data.index("OUTLINE") + 1
        while data[loop_index] != "":
            edit = data[loop_index].replace(";","")
            edit = edit.replace(",","")
            holder = edit.split()
            if data[loop_index + 1] == "":
                replace_list = "      " + str(round(float(holder[0]) * convert_xy,5)) + ",    " + str(round(float(holder[1]) * convert_xy,5)) + ";"
            else:
                replace_list = "      " + str(round(float(holder[0]) * convert_xy,5)) + ",    " + str(round(float(holder[1]) * convert_xy,5)) + ""
            data[loop_index] = replace_list
            loop_index += 1

        if "TOOLING" in bottom_all:
            loop_index = data.index("TOOLING") + 1
            while data[loop_index] != "":
                edit = data[loop_index].replace("2000","")
                edit = edit.replace(";","")
                edit = edit.replace(",","")
                holder = edit.split()
                replace_list = "    2000      " + str(round(float(holder[0]) * float(convert_xy),5)) + ",    " + str(round(float(holder[1]) * float(convert_xy),5)) + ";"
                data[loop_index] = replace_list
                loop_index += 1
        
        loop_index = data.index("  ALTERNATES")
        for index, aaaa in enumerate(data):
            if index > loop_index:
                if aaaa != "":
                    ##  SORT top.asc CREATION HERE
                    if "TOP" not in aaaa:
                        data[index] = "~"
                    else:
                        edit = aaaa.replace(";","")
                        edit = edit.replace(",","")
                        holder = edit.split()
                        if len(holder) == 4:
                            data[index] = "            " + str(round(float(holder[0]) * float(convert_xy),5)) + ",    " \
                                      + str(round(float(holder[1]) * float(convert_xy),5)) + "        " + str(holder[2]) \
                                      + " " + str(holder[3]) + ";"
                        else:
                            if len(holder) == 5:
                                data[index] = "            " + str(round(float(holder[0]) * float(convert_xy),5)) + ",    " \
                                      + str(round(float(holder[1]) * float(convert_xy),5)) + "        " + str(holder[2]) \
                                      + " " + str(holder[3]) + " " + str(holder[4]) + ";"
                            else:
                                data[index] = "            " + str(round(float(holder[0]) * float(convert_xy),5)) + ",    " \
                                          + str(round(float(holder[1]) * float(convert_xy),5)) + "        " + str(holder[2]) + ";"

        file = open("OUTPUTS/top_" + str(sys.argv[3]) + ".asc", "w")
        for everything in data:
            if everything != "~":
                file.write(str(everything) + "\n")
        file.write("END")
        file.close()

        ##  .scr CREATION
        file = open("OUTPUTS/top_" + str(sys.argv[3]) + ".scr", "w")
        with open ("OUTPUTS/top_" + str(sys.argv[3]) + ".asc", "r") as myfile:
            data=myfile.readlines()
        data = [w.replace('\n', '') for w in data]


        ##  OUTLINE
        loop_index = data.index("OUTLINE") + 1
        while data[loop_index] != "":
            edit = data[loop_index].replace(";","")
            edit = edit.replace(",","")
            holder = edit.split()
            file.write("_DONUT\n0.5\n1.0\n" + str(holder[0]) + "," + str(holder[1]) + "\n\n")
            loop_index += 1

        ##  TOOLING
        ##  REMEMBER TO CHECK IF THIS IS HERE, DOESN'T HAVE TO BE
        if no_tooling == 0:
            loop_index = data.index("TOOLING") + 1
            while data[loop_index] != "":
                edit = data[loop_index].replace("2000","")
                edit = edit.replace(";","")
                edit = edit.replace(",","")
                holder = edit.split()
                file.write("_DONUT\n0.5\n1.0\n" + str(holder[0]) + "," + str(holder[1]) + "\n\n")
                loop_index += 1

        ##  REST OF FILE
        loop_index = data.index("  ALTERNATES") + 1
        while data[loop_index] != "":
            edit = data[loop_index].replace(";","")
            edit = edit.replace(",","")
            holder = edit.split()
            file.write("_CIRCLE\n" + str(holder[0]) + "," + str(holder[1]) + "\nD\n1.0\n")
            loop_index += 1
        
    ######################################################################################################
    ###################################   SINGLE BOARD CODE ENDS HERE   ##################################
    ######################################################################################################
        
else:
    
    ######################################################################################################
    #####################################   PANEL CODE STARTS HERE   #####################################
    ######################################################################################################
    
    if sys.argv[1] == "panel":
        looper = 0
        with open ("OUTPUTS/board_xy.asc", "r") as myfile:
            data=myfile.readlines()
        data = [w.replace('\n', '') for w in data]
        indices = [i for i, s in enumerate(data) if 'units' in s]
        data[indices[0]] = "units " + str(sys.argv[3]) + ";"
        myfile.close
        bottom_all = data

        outer_outline_x = []
        outer_outline_y = []
        outer_tooling_x = []
        outer_tooling_y = []

        inner_outline_x = []
        inner_outline_y = []
        inner_tooling_x = []
        inner_tooling_y = []
        
        loop_index = bottom_all.index("OUTLINE") + 1
        while bottom_all[loop_index] != "":
            edit = bottom_all[loop_index].replace(";","")
            edit = edit.replace(",","")
            holder = edit.split()
            outer_outline_x.append(round(float(holder[0]) * float(convert_xy),5))
            outer_outline_y.append(round(float(holder[1]) * float(convert_xy),5))
            loop_index += 1

        outline_count = 0
        for nums,get_inner_outline in enumerate(bottom_all):
            if get_inner_outline == "OUTLINE":
                outline_count += 1
                if outline_count == 2:
                    inner_outline_loop_index = (nums + 1)
                    break
        
        ##INNER TOOLING HERE

        while bottom_all[inner_outline_loop_index] != "":
            edit = bottom_all[inner_outline_loop_index].replace(";","")
            edit = edit.replace(",","")
            holder = edit.split()
            inner_outline_x.append(round(float(holder[0]) * float(convert_xy),5))
            inner_outline_y.append(round(float(holder[1]) * float(convert_xy),5))
            inner_outline_loop_index += 1

        test_for_outer_tooling = bottom_all.index("BOARDS")
        if "TOOLING" in bottom_all:
            loop_index = bottom_all.index("TOOLING") + 1
            if loop_index < test_for_outer_tooling:
                while bottom_all[loop_index] != "":
                    edit = bottom_all[loop_index].replace("2000","")
                    edit = edit.replace(";","")
                    edit = edit.replace(",","")
                    holder = edit.split()
                    outer_tooling_x.append(round(float(holder[0]) * float(convert_xy),5))
                    outer_tooling_y.append(round(float(holder[1]) * float(convert_xy),5))
                    loop_index += 1

        ##  THERE'S NO WAY OF KNOWING WHETHER THIS IS A SET FORMAT, SO IN THE LOOP MAKE IT LOOK FOR ELEMENTS THAT
        ##  EITHER SAY "BOARDS" OR ARE BLANK, AND THEN INCREMENT
        loop_index = bottom_all.index("BOARDS") + 1
        board_count = 0
        board_name = ""
        boards_x = []
        boards_y = []
        boards_rotation = []
        board_hold = []
        while bottom_all[loop_index] != "":
            board_hold.append(bottom_all[loop_index])
            edit = bottom_all[loop_index].replace(";","")
            edit = edit.replace(",","")
            holder = edit.split()
            board_count += 1
            board_name = holder[1]
            boards_x.append(round(float(holder[2]) * float(convert_xy),5))
            boards_y.append(round(float(holder[3]) * float(convert_xy),5))
            boards_rotation.append(holder[4])
            loop_index += 1

        alternates = []
        test_for_alternates = bottom_all.index("OTHER") + 2
        while bottom_all[test_for_alternates] != "":
            if " TOP" not in bottom_all[test_for_alternates]:
                if "NO_PROBE" not in bottom_all[test_for_alternates]:
                    alternates.append(bottom_all[test_for_alternates])
                    test_for_alternates += 1
                else:
                    test_for_alternates += 1
            else:
                ## append to top here after checking for NO_PROBE
                test_for_alternates += 1

        top = 0

        ##  REMOVES NO_PROBE LINES
        for index, no_probe in enumerate(bottom_all):
            if no_probe.find(" NO_PROBE") > 0:
                bottom_all[index] = "~"

        for index, no_probe in enumerate(bottom_all):
            if no_probe.find("TOP") > 0:
                bottom_all[index] = "~"
                top += 1

        ##  GETS RID OF DEVICES
        devices_index = bottom_all.index("DEVICES")
        while bottom_all[devices_index] != "":
            bottom_all[devices_index] = "~"
            devices_index += 1

        file = open("OUTPUTS/bottom_" + str(sys.argv[3]) + ".asc", "w")
        file.write(str("OUTLINE"))
        for inc,everything in enumerate(outer_outline_x):
            file.write("\n       " + str(everything) + ",    " + str(outer_outline_y[inc]))
        file.write(";\n\n")
        if len(outer_tooling_x) > 0:
            file.write(str("TOOLING"))
            for inc,everything in enumerate(outer_tooling_x):
                file.write("\n       " + str(everything) + ",    " + str(outer_tooling_y[inc]))
            file.write(";\n\n")
        file.write(str("BOARDS"))
        for everything in board_hold:
            edit = everything.replace(";","")
            holder = edit.split()
            file.write("\n        " + str(holder[0]) + "      " + str(holder[1]) + "   " + str(round(float(holder[2]) * float(convert_xy),5)) + "   " + \
                       str(round(float(holder[3]) * float(convert_xy),5)) + "    " + str(holder[4]) + ";")
        file.write("\n\n")
        file.write("BOARD " + str(board_name) + "\n\n")
        if len(inner_outline_x) > 0:
            file.write(str("OUTLINE"))
            for inc,everything in enumerate(inner_outline_x):
                file.write("\n   " + str(everything) + ",  " + str(inner_outline_y[inc]))
            file.write(";\n\n")
        if len(inner_tooling_x) > 0:
            file.write(str("TOOLING"))
            for inc,everything in enumerate(inner_tooling_x):
                file.write("\n    2000      " + str(everything) + ",  " + str(inner_tooling_y[inc]) + ";")
            file.write("\n\n")
        file.write("OTHER\n  ALTERNATES")
        for everything in alternates:
            edit = everything.replace(";","").replace(",","")
            holder = edit.split()
            file.write("\n            " + str(round(float(holder[0]) * float(convert_xy),5)) + ",    " + str(round(float(holder[1]) * float(convert_xy),5)) \
                       + "        " + str(holder[2]))
        file.write("\n\nEND BOARD\n\nEND")
        file.close()

        file = open("OUTPUTS/bottom_" + str(sys.argv[3]) + ".scr", "w")
        for inc,everything in enumerate(outer_outline_x):
            file.write("_CIRCLE\n" + str(everything) + "," + str(outer_outline_y[inc]) + "\nD\n1.0\n")
        if len(outer_tooling_x) > 0:
            for inc,everything in enumerate(outer_tooling_x):
                file.write("_CIRCLE\n" + str(everything) + "," + str(outer_tooling_y[inc]) + "\nD\n1.0\n")
        for inc,everything in enumerate(boards_x):
            for all_things in alternates:
                edit = all_things.replace(";","").replace(",","")
                holder = edit.split()
                if boards_rotation[inc] == "90.00":
                    x = (float(holder[1]) - (float(holder[1]) * 2))
                    y = float(holder[0])
                    file.write("_CIRCLE\n" + str(round(round(float(x) + float(boards_x[inc]),5) * float(convert_xy),5)) \
                                   + "," + str(round(round(float(y) + float(boards_y[inc]),5) * float(convert_xy),5)) + "\nD\n1.0\n")
                else:                                              
                    if boards_rotation[inc] == "180.00":
                        x = (float(holder[0]) - (float(holder[0]) * 2))
                        y = (float(holder[1]) - (float(holder[1]) * 2))
                        file.write("_CIRCLE\n" + str(round(round(float(x) + float(boards_x[inc]),5) * float(convert_xy),5)) \
                                   + "," + str(round(round(float(y) + float(boards_y[inc]),5) * float(convert_xy),5)) + "\nD\n1.0\n")
                    else:
                        if boards_rotation[inc] == "270.00":
##                            rotate_var = boards_rotation[looper][0:3]
##                            rotate_var = int(rotate_var)
                            x = float(holder[0])
                            y = (float(holder[1]) - (float(holder[1]) * 2))
                            file.write("_CIRCLE\n" + str(round(round(float(x) + float(boards_x[inc]),5) * convert_xy,5)) + \
                           "," + str(round(round(float(y) + float(boards_y[inc]),5) * convert_xy,5)) + "\nD\n1.0\n")
                        else:
                            file.write("_CIRCLE\n" + str(round(round(float(holder[0]) + float(everything),5) * convert_xy,5)) + \
                           "," + str(round(round(float(holder[1]) + float(boards_y[inc]),5) * convert_xy,5)) + "\nD\n1.0\n")
##
##        if top > 0:
##            looper = 0
##            with open ("OUTPUTS/board_xy.asc", "r") as myfile:
##                data=myfile.readlines()
##            data = [w.replace('\n', '') for w in data]
##            indices = [i for i, s in enumerate(data) if 'units' in s]
##            data[indices[0]] = "units " + str(sys.argv[3]) + ";"
##            myfile.close
##            top_all = data
##
##            outer_outline_x = []
##            outer_outline_y = []
##            outer_tooling_x = []
##            outer_tooling_y = []
##            
##            loop_index = bottom_all.index("OUTLINE") + 1
##            while top_all[loop_index] != "":
##                edit = top_all[loop_index].replace(";","")
##                edit = edit.replace(",","")
##                holder = edit.split()
##                outer_outline_x.append(holder[0])
##                outer_outline_y.append(holder[1])
##                loop_index += 1
##
##            test_for_outer_tooling = top_all.index("BOARDS")
##            if "TOOLING" in top_all:
##                loop_index = top_all.index("TOOLING") + 1
##                if loop_index < test_for_outer_tooling:
##                    while top_all[loop_index] != "":
##                        edit = top_all[loop_index].replace("2000","")
##                        edit = edit.replace(";","")
##                        edit = edit.replace(",","")
##                        holder = edit.split()
##                        outer_tooling_x.append(holder[0])
##                        outer_tooling_y.append(holder[1])
##                        loop_index += 1
##
##            ##  THERE'S NO WAY OF KNOWING WHETHER THIS IS A SET FORMAT, SO IN THE LOOP MAKE IT LOOK FOR ELEMENTS THAT
##            ##  EITHER SAY "BOARDS" OR ARE BLANK, AND THEN INCREMENT
##            loop_index = top_all.index("BOARDS") + 1
##            board_count = 0
##            board_name = ""
##            boards_x = []
##            boards_y = []
##            boards_rotation = []
##            while top_all[loop_index] != "":
##                edit = top_all[loop_index].replace(";","")
##                edit = edit.replace(",","")
##                holder = edit.split()
##                board_count += 1
##                board_name = holder[1]
##                boards_x.append(holder[2])
##                boards_y.append(holder[3])
##                boards_rotation.append(holder[4])
##                loop_index += 1
##
##            ##  REMOVES NO_PROBE LINES
##            for index, no_probe in enumerate(top_all):
##                if no_probe.find(" NO_PROBE") > 0:
##                    top_all[index] = "~"
##
##            ##  GETS RID OF DEVICES
##            devices_index = top_all.index("DEVICES")
##            while top_all[devices_index] != "":
##                top_all[devices_index] = "~"
##                devices_index += 1
##
##            alternates_index = top_all.index("  ALTERNATES")
##            for index, no_probe in enumerate(top_all):
##                if index > alternates_index:
##                    if "TOP" not in no_probe:
##                        top_all[index] = "~"
##
##            file = open("OUTPUTS/top_" + str(sys.argv[3]) + ".asc", "w")
##            boards_next = 0
##            output = 0
##            for index,everything in enumerate(top_all):
##                if index > 4:
##                    if everything != "~":
##                        if everything == "BOARDS":
##                            boards_next = 1
##                        else:
##                            if everything == "":
##                                boards_next = 0
##                                if output == 1:
##                                    file.write(";\n")
##                                    output = 0
##                            else:
##                                if output == 1:
##                                    file.write("\n")
##                        if num_there(everything) == True:
##                            if everything[0:5] != "BOARD ":
##                                file.write(str(everything) + "\n")
##                            else:
##                                if boards_next == 0:
##                                    edit = everything.replace(";","")
##                                    edit = edit.replace(",","")
##                                    holder = edit.split()                                
##                                    if len(holder) == 2:
##                                        output = 1
##                                        file.write("      " + str(round(float(holder[0]) * float(convert_xy),5)) + ",   " \
##                                                                  + str(round(float(holder[1]) * float(convert_xy),5)) + "")
##                                        
##                                    else:
##                                        if len(holder) == 3:
##                                            file.write("    2000     " + str(round(float(holder[1]) * float(convert_xy),5)) + ",   " \
##                                                                  + str(round(float(holder[2]) * float(convert_xy),5)) + ";\n")
##                                        else:
##                                            if len(holder) == 4:
##                                                data[index] = "            " + str(round(float(holder[0]) * float(convert_xy),5)) + ",    " \
##                                                          + str(round(float(holder[1]) * float(convert_xy),5)) + "        " + str(holder[2]) \
##                                                          + " " + str(holder[3]) + ";"
##                                            else:
##                                                if len(holder) == 5:
##                                                    data[index] = "            " + str(round(float(holder[0]) * float(convert_xy),5)) + ",    " \
##                                                          + str(round(float(holder[1]) * float(convert_xy),5)) + "        " + str(holder[2]) \
##                                                          + " " + str(holder[3]) + " " + str(holder[4]) + ";"
##                                                else:
##                                                    data[index] = "            " + str(round(float(holder[0]) * float(convert_xy),5)) + ",    " \
##                                                              + str(round(float(holder[1]) * float(convert_xy),5)) + "        " + str(holder[2]) + ";"
##                                else:
##                                    edit = everything.replace(";","")
##                                    edit = edit.replace(",","")
##                                    holder = edit.split()
##                                    file.write("        " + str(holder[0]) + "      " + str(holder[1]) + "      " + str(round(float(holder[2]) \
##                                            * float(convert_xy),5)) + "      " + str(round(float(holder[3]) * float(convert_xy),5)) \
##                                               + "      " + str(holder[4]) + ";\n")
##                        else:
##                            file.write(str(everything) + "\n")
##                else:
##                    file.write(str(everything) + "\n")
##            file.close()
##
##            file = open("OUTPUTS/top_" + str(sys.argv[3]) + ".scr", "w")
##            with open ("OUTPUTS/top_" + str(sys.argv[3]) + ".asc", "r") as myfile:
##                data=myfile.readlines()
##            data = [w.replace('\n', '') for w in data]
##            
##            looper = 0
##            inner_looper = 0
##            alternates = 0
##            while looper < board_count:
##                for everything in data:
##                    if inner_looper == 0:
##                        for index, outline in enumerate(outer_outline_x):
##                            file.write("_CIRCLE\n" + str(round(float(outer_outline_x[index]) * float(convert_xy),5)) + "," \
##                                       + str(round(float(outer_outline_y[index]) * float(convert_xy),5)) + "\nD\n1.0\n")
##                            inner_looper += 1
##                        if len(outer_tooling_x) > 0:
##                            for index, tooling in enumerate(outer_tooling_x):
##                                file.write("_CIRCLE\n" + str(round(float(outer_tooling_x[index]) * float(convert_xy),5)) + "," \
##                                           + str(round(float(outer_tooling_y[index]) * float(convert_xy),5)) + "\nD\n1.0\n")
##                                inner_looper += 1
##                    if alternates == 1:
##                        edit = everything.replace(";","")
##                        edit = edit.replace(",","")
##                        holder = edit.split()
##                        if len(holder) > 0:
##                            if holder[0] != "END":
##                                if boards_rotation[looper] == "90.00":
##                                    x = (float(holder[1]) - (float(holder[1]) * 2))
##                                    y = float(holder[0])
##                                    file.write("_CIRCLE\n" + str(round(round(float(x) + float(boards_x[looper]),5) * float(convert_xy),5)) \
##                                                   + "," + str(round(round(float(y) + float(boards_y[looper]),5) * float(convert_xy),5)) + "\nD\n1.0\n")
##                                else:                                              
##                                    if boards_rotation[looper] == "180.00":
##                                        x = (float(holder[0]) - (float(holder[0]) * 2))
##                                        y = (float(holder[1]) - (float(holder[1]) * 2))
##                                        file.write("_CIRCLE\n" + str(round(round(float(x) + float(boards_x[looper]),5) * float(convert_xy),5)) \
##                                                   + "," + str(round(round(float(y) + float(boards_y[looper]),5) * float(convert_xy),5)) + "\nD\n1.0\n")
##                                    else:
##                                        if boards_rotation[looper] == "270.00":
##                                            rotate_var = boards_rotation[looper][0:3]
##                                            rotate_var = int(rotate_var)
##                                            x = float(holder[0])
##                                            y = (float(holder[1]) - (float(holder[1]) * 2))
##                                            file.write("_CIRCLE\n" + str(round(round(float(x) + float(boards_x[looper]),5) * float(convert_xy),5)) \
##                                                       + "," + str(round(round(float(y) + float(boards_y[looper]),5) * float(convert_xy),5)) + "\nD\n1.0\n")
##                                        else:
##                                            file.write("_CIRCLE\n" + str(round(round(float(holder[0]) + float(boards_x[looper]),5) * \
##                                                        float(convert_xy),5)) + "," + str(round(round(float(holder[1]) + float(boards_y[looper]),5) \
##                                                        * float(convert_xy),5)) + "\nD\n1.0\n")
##                    if everything == "  ALTERNATES":
##                        alternates = 1                         
##                looper += 1
##                everything = ""
##                alternates = 0
            
                

    ######################################################################################################
    ######################################   PANEL CODE ENDS HERE   ######################################
    ######################################################################################################
            
    else:
        
    ######################################################################################################
    ##################################   MULTI BOARD CODE STARTS HERE   ##################################
    ######################################################################################################

        if sys.argv[1] == "multi":
            looper = 0
            with open ("OUTPUTS/board_xy.asc", "r") as myfile:
                data=myfile.readlines()
            data = [w.replace('\n', '') for w in data]
            indices = [i for i, s in enumerate(data) if 'units' in s]
            data[indices[0]] = "units " + str(sys.argv[3]) + ";"
            myfile.close
            bottom_all = data

            outer_outline_x = []
            outer_outline_y = []
            outer_tooling_x = []
            outer_tooling_y = []

            loop_index = bottom_all.index("OUTLINE") + 1
            while bottom_all[loop_index] != "":
                edit = bottom_all[loop_index].replace(";","")
                edit = edit.replace(",","")
                holder = edit.split()
                outer_outline_x.append(holder[0])
                outer_outline_y.append(holder[1])
                loop_index += 1

            test_for_outer_tooling = bottom_all.index("BOARDS")
            if "TOOLING" in bottom_all:
                tooling_count = 1
                loop_index = bottom_all.index("TOOLING") + 1
                if loop_index < test_for_outer_tooling:
                    while bottom_all[loop_index] != "":
                        edit = bottom_all[loop_index].replace("2000","")
                        edit = edit.replace(";","")
                        edit = edit.replace(",","")
                        holder = edit.split()
                        outer_tooling_x.append(holder[0])
                        outer_tooling_y.append(holder[1])
                        loop_index += 1
            else:
                tooling_count = 0

            ##  GET BOARD NAMES
            loop_index = bottom_all.index("BOARDS") + 1
            board_count = 0
            board_name = []
            boards_x = []
            boards_y = []
            boards_rotation = []
            while bottom_all[loop_index] != "":
                edit = bottom_all[loop_index].replace(";","")
                edit = edit.replace(",","")
                holder = edit.split()
                board_count += 1
                board_name.append(holder[1])
                boards_x.append(holder[2])
                boards_y.append(holder[3])
                boards_rotation.append(holder[4])
                loop_index += 1
            top = 0

            ##  REMOVES NO_PROBE LINES
            for index, no_probe in enumerate(bottom_all):
                if no_probe.find(" NO_PROBE") > 0:
                    bottom_all[index] = "~"

            for index, no_probe in enumerate(bottom_all):
                if no_probe.find("TOP") > 0:
                    bottom_all[index] = "~"
                    top += 1
                else:
                    if no_probe.find("TOP") > 0:
                        bottom_all[index] = "~"

            devices_count = bottom_all.count("DEVICES")
            ##  GETS RID OF DEVICES
            while devices_count > 0:
                devices_index = bottom_all.index("DEVICES")
                while bottom_all[devices_index] != "":
                    bottom_all[devices_index] = "~"
                    devices_index += 1
                devices_count -= 1

            file = open("OUTPUTS/bottom_" + str(sys.argv[3]) + ".asc", "w")
            for everything in bottom_all:
                if everything != "~":
                    file.write(str(everything) + "\n")
            file.close()

            file = open("OUTPUTS/bottom_" + str(sys.argv[3]) + ".scr", "w")
            with open ("OUTPUTS/bottom_" + str(sys.argv[3]) + ".asc", "r") as myfile:
                data=myfile.readlines()
            data = [w.replace('\n', '') for w in data]
            looper = 0
            inner_looper = 0
            alternates = 0

            for everything in data:
                    if inner_looper == 0:
                        for index, outline in enumerate(outer_outline_x):
                            file.write("_CIRCLE\n" + str(round(float(outer_outline_x[index]) * float(convert_xy),5)) + "," \
                                       + str(round(float(outer_outline_y[index]) * float(convert_xy),5)) + "\nD\n1.0\n")
                            inner_looper += 1
                        if len(outer_tooling_x) > 0:
                            for index, tooling in enumerate(outer_tooling_x):
                                file.write("_CIRCLE\n" + str(round(float(outer_tooling_x[index]) * float(convert_xy),5)) + "," \
                                           + str(round(float(outer_tooling_y[index]) * float(convert_xy),5)) + "\nD\n1.0\n")
                                inner_looper += 1
            get_outline = []
            get_tooling = []
            get_alternate = []
            for indexes,everything in enumerate(data):
                if everything == "OUTLINE":
                    get_outline.append(indexes)
                if everything == "TOOLING":
                    get_tooling.append(indexes)
                if everything == "  ALTERNATES":
                    get_alternate.append(indexes)

            ##  GET THIS TO CHECK OUTLINE AND TOOLING TO SEE IF THERE ARE OUTER ONES INCLUDED
            get_outline.pop(0)
            
            for index, brd_nms in enumerate(board_name):
                inner_board_outline_x = []
                inner_board_outline_y = []
                inner_board_tooling_x = []
                inner_board_tooling_y = []
                inner_outline = 0
                inner_tooling = 0
                inner_alternates = 0
                for line_num,everything in enumerate(data):
                    if everything == "":
                        inner_outline = 0
                        inner_alternates = 0
                    if inner_outline == 1:
                        edit = everything.replace(";","")
                        edit = edit.replace(",","")
                        holder = edit.split()
                        file.write("_CIRCLE\n" + str(round(round(float(holder[0]) + float(boards_x[index]),5) * float(convert_xy),5)) \
                                               + "," + str(round(round(float(holder[1]) + float(boards_y[index]),5) * float(convert_xy),5)) + "\nD\n1.0\n")
                    if inner_alternates == 1:
                        edit = everything.replace(";","")
                        edit = edit.replace(",","")
                        holder = edit.split()
                        if boards_rotation[looper] == "90.00":
                            x = (float(holder[1]) - (float(holder[1]) * 2))
                            y = float(holder[0])
                            file.write("_CIRCLE\n" + str(round(round(float(x) + float(boards_x[looper]),5) * float(convert_xy),5)) \
                                           + "," + str(round(round(float(y) + float(boards_y[looper]),5) * float(convert_xy),5)) + "\nD\n1.0\n")
                        else:                                              
                            if boards_rotation[looper] == "180.00":
                                x = (float(holder[0]) - (float(holder[0]) * 2))
                                y = (float(holder[1]) - (float(holder[1]) * 2))
                                file.write("_CIRCLE\n" + str(round(round(float(x) + float(boards_x[looper]),5) * float(convert_xy),5)) \
                                           + "," + str(round(round(float(y) + float(boards_y[looper]),5) * float(convert_xy),5)) + "\nD\n1.0\n")
                            else:
                                if boards_rotation[looper] == "270.00":
                                    rotate_var = boards_rotation[looper][0:3]
                                    rotate_var = int(rotate_var)
                                    x = float(holder[0])
                                    y = (float(holder[1]) - (float(holder[1]) * 2))
                                    file.write("_CIRCLE\n" + str(round(round(float(x) + float(boards_x[looper]),5) * float(convert_xy),5)) \
                                               + "," + str(round(round(float(y) + float(boards_y[looper]),5) * float(convert_xy),5)) + "\nD\n1.0\n")
                                else:
                                    file.write("_CIRCLE\n" + str(round(round(float(holder[0]) + float(boards_x[looper]),5) * \
                                                float(convert_xy),5)) + "," + str(round(round(float(holder[1]) + float(boards_y[looper]),5) \
                                                * float(convert_xy),5)) + "\nD\n1.0\n")
                    if line_num == get_outline[index]:
                        inner_outline = 1
                    if line_num == get_alternate[index]:
                        inner_alternates = 1
                looper += 1

            if top > 0:
                looper = 0
                with open ("OUTPUTS/board_xy.asc", "r") as myfile:
                    data=myfile.readlines()
                data = [w.replace('\n', '') for w in data]
                indices = [i for i, s in enumerate(data) if 'units' in s]
                data[indices[0]] = "units " + str(sys.argv[3]) + ";"
                myfile.close
                top_all = data

                outer_outline_x = []
                outer_outline_y = []
                outer_tooling_x = []
                outer_tooling_y = []

                loop_index = top_all.index("OUTLINE") + 1
                while top_all[loop_index] != "":
                    edit = top_all[loop_index].replace(";","")
                    edit = edit.replace(",","")
                    holder = edit.split()
                    outer_outline_x.append(holder[0])
                    outer_outline_y.append(holder[1])
                    loop_index += 1

                test_for_outer_tooling = top_all.index("BOARDS")
                if "TOOLING" in top_all:
                    tooling_count = 1
                    loop_index = top_all.index("TOOLING") + 1
                    if loop_index < test_for_outer_tooling:
                        while top_all[loop_index] != "":
                            edit = top_all[loop_index].replace("2000","")
                            edit = edit.replace(";","")
                            edit = edit.replace(",","")
                            holder = edit.split()
                            outer_tooling_x.append(holder[0])
                            outer_tooling_y.append(holder[1])
                            loop_index += 1
                else:
                    tooling_count = 0

                ##  GET BOARD NAMES
                loop_index = top_all.index("BOARDS") + 1
                board_count = 0
                board_name = []
                boards_x = []
                boards_y = []
                boards_rotation = []
                while top_all[loop_index] != "":
                    edit = top_all[loop_index].replace(";","")
                    edit = edit.replace(",","")
                    holder = edit.split()
                    board_count += 1
                    board_name.append(holder[1])
                    boards_x.append(holder[2])
                    boards_y.append(holder[3])
                    boards_rotation.append(holder[4])
                    loop_index += 1

                ##  REMOVES NO_PROBE LINES
                for index, no_probe in enumerate(top_all):
                    if no_probe.find(" NO_PROBE") > 0:
                        top_all[index] = "~"

                ##  GETS RID OF DEVICES
                devices_index = top_all.index("DEVICES")
                while top_all[devices_index] != "":
                    top_all[devices_index] = "~"
                    devices_index += 1

                alternates_index = top_all.index("  ALTERNATES")
                for index, no_probe in enumerate(top_all):
                    if index > alternates_index:
                        if "TOP" not in no_probe:
                            top_all[index] = "~"

                file = open("OUTPUTS/top_" + str(sys.argv[3]) + ".asc", "w")
                for everything in top_all:
                    if everything != "~":
                        file.write(str(everything) + "\n")
                file.close()

                file = open("OUTPUTS/top_" + str(sys.argv[3]) + ".scr", "w")
                with open ("OUTPUTS/top_" + str(sys.argv[3]) + ".asc", "r") as myfile:
                    data=myfile.readlines()
                data = [w.replace('\n', '') for w in data]
                looper = 0
                inner_looper = 0
                alternates = 0

                for everything in data:
                        if inner_looper == 0:
                            for index, outline in enumerate(outer_outline_x):
                                file.write("_CIRCLE\n" + str(round(float(outer_outline_x[index]) * float(convert_xy),5)) + "," \
                                           + str(round(float(outer_outline_y[index]) * float(convert_xy),5)) + "\nD\n1.0\n")
                                inner_looper += 1
                            if len(outer_tooling_x) > 0:
                                for index, tooling in enumerate(outer_tooling_x):
                                    file.write("_CIRCLE\n" + str(round(float(outer_tooling_x[index]) * float(convert_xy),5)) + "," \
                                               + str(round(float(outer_tooling_y[index]) * float(convert_xy),5)) + "\nD\n1.0\n")
                                    inner_looper += 1
                get_outline = []
                get_tooling = []
                get_alternate = []
                for indexes,everything in enumerate(data):
                    if everything == "OUTLINE":
                        get_outline.append(indexes)
                    if everything == "TOOLING":
                        get_tooling.append(indexes)
                    if everything == "  ALTERNATES":
                        get_alternate.append(indexes)

                ##  GET THIS TO CHECK OUTLINE AND TOOLING TO SEE IF THERE ARE OUTER ONES INCLUDED
                get_outline.pop(0)
                
                for index, brd_nms in enumerate(board_name):
                    inner_board_outline_x = []
                    inner_board_outline_y = []
                    inner_board_tooling_x = []
                    inner_board_tooling_y = []
                    inner_outline = 0
                    inner_tooling = 0
                    inner_alternates = 0
                    for line_num,everything in enumerate(data):
                        if everything == "":
                            inner_outline = 0
                            inner_alternates = 0
                        if inner_outline == 1:
                            edit = everything.replace(";","")
                            edit = edit.replace(",","")
                            holder = edit.split()
                            file.write("_CIRCLE\n" + str(round(round(float(holder[0]) + float(boards_x[index]),5) * float(convert_xy),5)) \
                                                   + "," + str(round(round(float(holder[1]) + float(boards_y[index]),5) * float(convert_xy),5)) + "\nD\n1.0\n")
                        if inner_alternates == 1:
                            edit = everything.replace(";","")
                            edit = edit.replace(",","")
                            holder = edit.split()
                            if boards_rotation[looper] == "90.00":
                                x = (float(holder[1]) - (float(holder[1]) * 2))
                                y = float(holder[0])
                                file.write("_CIRCLE\n" + str(round(round(float(x) + float(boards_x[looper]),5) * float(convert_xy),5)) \
                                               + "," + str(round(round(float(y) + float(boards_y[looper]),5) * float(convert_xy),5)) + "\nD\n1.0\n")
                            else:                                              
                                if boards_rotation[looper] == "180.00":
                                    x = (float(holder[0]) - (float(holder[0]) * 2))
                                    y = (float(holder[1]) - (float(holder[1]) * 2))
                                    file.write("_CIRCLE\n" + str(round(round(float(x) + float(boards_x[looper]),5) * float(convert_xy),5)) \
                                               + "," + str(round(round(float(y) + float(boards_y[looper]),5) * float(convert_xy),5)) + "\nD\n1.0\n")
                                else:
                                    if boards_rotation[looper] == "270.00":
                                        rotate_var = boards_rotation[looper][0:3]
                                        rotate_var = int(rotate_var)
                                        x = float(holder[0])
                                        y = (float(holder[1]) - (float(holder[1]) * 2))
                                        file.write("_CIRCLE\n" + str(round(round(float(x) + float(boards_x[looper]),5) * float(convert_xy),5)) \
                                                   + "," + str(round(round(float(y) + float(boards_y[looper]),5) * float(convert_xy),5)) + "\nD\n1.0\n")
                                    else:
                                        file.write("_CIRCLE\n" + str(round(round(float(holder[0]) + float(boards_x[looper]),5) * \
                                                    float(convert_xy),5)) + "," + str(round(round(float(holder[1]) + float(boards_y[looper]),5) \
                                                    * float(convert_xy),5)) + "\nD\n1.0\n")
                        if line_num == get_outline[index]:
                            inner_outline = 1
                        if line_num == get_alternate[index]:
                            inner_alternates = 1
                    looper += 1
                    

##        ######################################################################################################
##        ######################################   MULTI CODE ENDS HERE   ######################################
##        ######################################################################################################

        else:

##        ######################################################################################################
##        ##################################   MULTI/PANEL CODE STARTS HERE   ##################################
##        ######################################################################################################
            
            looper = 0
            with open ("OUTPUTS/board_xy.asc", "r") as myfile:
                data=myfile.readlines()
            data = [w.replace('\n', '') for w in data]
            if 'units' in data:
                indices = [i for i, s in enumerate(data) if 'units' in s]
                data[indices[0]] = "units " + str(sys.argv[3]) + ";"
            else:
                if 'UNITS' in data:
                    indices = [i for i, s in enumerate(data) if 'UNITS' in s]
                    data[indices[0]] = "UNITS " + str(sys.argv[3]) + ";"
            myfile.close
            bottom_all = data

            outer_outline_x = []
            outer_outline_y = []
            outer_tooling_x = []
            outer_tooling_y = []
            
            for nums,everything in enumerate(bottom_all):
                if "OUTLINE" in everything:
                    loop_index = nums + 1
                    break
            while bottom_all[loop_index] != "":
                edit = bottom_all[loop_index].replace(";","")
                edit = edit.replace(",","")
                holder = edit.split()
                outer_outline_x.append(holder[0])
                outer_outline_y.append(holder[1])
                loop_index += 1

##            test_for_outer_tooling = bottom_all.index("BOARDS")
            for nums,everything in enumerate(bottom_all):
                if "TOOLING" in everything:
                    tooling_count = 1
                    loop_index = nums + 1
                    break
                else:
                    tooling_count = 0
            while bottom_all[loop_index] != "":
                edit = bottom_all[loop_index].replace("2000","")
                edit = edit.replace(";","")
                edit = edit.replace(",","")
                holder = edit.split()
                outer_tooling_x.append(holder[0])
                outer_tooling_y.append(holder[1])
                loop_index += 1
                
            ##  GET BOARD NAMES
            for nums,everything in enumerate(bottom_all):
                if "BOARDS" in everything:
                    tooling_count = 1
                    loop_index = nums + 1
                    break
            board_count = 0
            board_name = []
            boards_x = []
            boards_y = []
            boards_rotation = []
            while bottom_all[loop_index] != "":
                edit = bottom_all[loop_index].replace(";","")
                edit = edit.replace(",","")
                holder = edit.split()
                board_count += 1
                board_name.append(holder[1])
                boards_x.append(holder[2])
                boards_y.append(holder[3])
                boards_rotation.append(holder[4])
                loop_index += 1

            board_names = list(set(board_name))
            board_loops = []
            for everything in board_names:
                board_loops.append(board_name.count(everything))

            top = 0

            ##  REMOVES NO_PROBE LINES
            for index, no_probe in enumerate(bottom_all):
                if no_probe.find(" NO_PROBE") > 0:
                    bottom_all[index] = "~"

            for index, no_probe in enumerate(bottom_all):
                if no_probe.find("TOP") > 0:
                    bottom_all[index] = "~"
                    top += 1
                else:
                    if no_probe.find("TOP") > 0:
                        bottom_all[index] = "~"

                devices_count = bottom_all.count("DEVICES")
            ##  GETS RID OF DEVICES
            while devices_count > 0:
                devices_index = bottom_all.index("DEVICES")
                while bottom_all[devices_index] != "":
                    bottom_all[devices_index] = "~"
                    devices_index += 1
                devices_count -= 1

##            for index,everything in enumerate(outer_outline_x):
##                print (round(float(outer_outline_x[index]) * float(convert_xy),5),round(float(outer_outline_y[index]) * float(convert_xy),5))

##            if top > 0:
##                None
##            else:
##                None
            
            file = open("OUTPUTS/bottom_" + str(sys.argv[3]) + ".asc", "w")
            outline_check = 0
            tooling_check = 0
            boards_check = 0
            rest_check = 0
            general_line = 1
            no_tooling = 0
            for everything in bottom_all:
                if everything != "~":
                    if "OUTLINE" in everything:
                        file.write(str("OUTLINE"))
                        outline_check = 1
                        general_line = 0
                    else:
                        if everything == "" and outline_check == 1:
                            outline_check = 0
                            general_line = 1
                            file.write(";\n")
                        else:
                            if outline_check == 1:
                                edit = everything.replace(";","")
                                edit = edit.replace(",","")
                                holder = edit.split()
                                x_coor = round(float(holder[0]) * float(convert_xy),5)
                                y_coor = round(float(holder[1]) * float(convert_xy),5)
                                file.write("\n  " + str(x_coor) + ",    " + str(y_coor))
                                
                    if "TOOLING" in bottom_all:
                        if "TOOLING" in everything:
                            file.write("TOOLING")
                            tooling_check = 1
                            general_line = 0
                        else:
                            if tooling_check == 1 and everything == "":
                                tooling_check = 0
                                general_line = 1
                                file.write("\n")
                            else:
                                if tooling_check == 1:
                                    edit = everything.replace("2000","")
                                    edit = edit.replace(";","")
                                    edit = edit.replace(",","")
                                    holder = edit.split()
                                    file.write("\n    2000      " + str(round(float(holder[0]) * float(convert_xy),5)) + ",    " \
                                               + str(round(float(holder[1]) * float(convert_xy),5)) + ";")
                    else:
                        no_tooling = 1
                    if boards_check == 1 and everything == "":
                        boards_check = 0
                        general_line = 1
                        file.write("\n")
                    if boards_check == 1:
                        edit = everything.replace(";","")
                        edit = edit.replace(",","")
                        holder = edit.split()
                        file.write("\n   " + str(holder[0]) + "     " + str(holder[1]) + "     " + str(round(float(holder[2]) * float(convert_xy),5)) + ",    " \
                                   + str(round(float(holder[3]) * float(convert_xy),5)) + "        " + str(holder[4]) + ";")
                        
                    if "BOARDS" in everything:
                        file.write("BOARDS")
                        boards_check = 1
                        general_line = 0

                    if "ALTERNATES" in everything:
                        file.write("  ALTERNATES")
                        rest_check = 1
                        general_line = 0
                    else:
                        if everything == "":
                            rest_check = 0
                            general_line = 1
                        else:
                            if rest_check == 1:
                                edit = everything.replace(";","")
                                edit = edit.replace(",","")
                                holder = edit.split()
                                file.write("\n            " + str(round(float(holder[0]) * float(convert_xy),5)) + ",    " \
                                           + str(round(float(holder[1]) * float(convert_xy),5)) + "        " + str(holder[2]))
                                if len(holder) > 3:
                                   file.write(" " + str(holder[3]) + ";")
                                else:
                                   file.write(";")
                    if general_line == 1:
                        if everything != "":
                            file.write(str(everything) + "\n")
                        else:
                            file.write("\n")
            file.close()

            file = open("OUTPUTS/bottom_" + str(sys.argv[3]) + ".scr", "w")
            with open ("OUTPUTS/bottom_" + str(sys.argv[3]) + ".asc", "r") as myfile:
                data=myfile.readlines()
            data = [w.replace('\n', '') for w in data]

            outline_inc = 0
            outline_count = data.count("OUTLINE")
            alternates_inc = 0
            alternates_count = data.count("  ALTERNATES")
            
            looper = 0
            inner_looper = 0
            alternates = 0
            outline_inc = 0
            add_to = 0
            tooling_add_to = 0
            alternates_add_to = 0
            outline_hold = []
            tooling_hold = []
            alternates_hold = {}
##            getting outline into list
            for everything in data:
                if add_to == 1:
                    if everything == "":
                        add_to = 0
                        outline_hold.append(outline_collate)
                    else:
                        outline_collate.append(everything)
                if tooling_add_to == 1:
                    if everything == "":
                        tooling_add_to = 0
                        tooling_hold.append(tooling_collate)
                    else:
                        tooling_collate.append(everything)
                if alternates_add_to == 1:
                    if everything == "":
                        alternates_add_to = 0
                        alternates_hold.update({dict_key: alternates_collate})
                        alternates_inc += 1
                    else:
                        alternates_collate.append(everything)
                if "OUTLINE" in everything:
                    outline_collate = []
                    add_to = 1
                if "TOOLING" in everything:
                    tooling_collate = []
                    tooling_add_to = 1
                if "ALTERNATES" in everything:
                    alternates_add_to = 1
                    dict_key = board_names[alternates_inc]
                    alternates_collate = []
            for each in outline_hold[0]:
                edit = each.split(",")
                file.write("_CIRCLE\n" + str(float(edit[0].replace(" ","").replace(";",""))) + "," + \
                           str(float(edit[1].replace(" ","").replace(";",""))) + "\nD\n1.0\n")
            if len(tooling_hold) > 0:
                for each in tooling_hold[0]:
                    edit = each.replace(" 2000  ","").replace(";","").replace(" ","")
                    edit = edit.split(",")
                    file.write("_CIRCLE\n" + str(float(edit[0])) + "," + str(float(edit[1])) + "\nD\n1.0\n")

            outline_count += 1
            ## this gets the board coordinates into a dictionary keyed with the board id. iterate over it. dead easy
            ## board_name FOR ALL BOARD NAMES IN ORDER
            ## board_rotation HOLDS ALL ROTATIONS IN THE SAME ORDER

            cad_xy_board_x = []
            cad_xy_board_y = []

            ## GETS THE BOARD OFFSETS INTO THE CORRECT CONVERSION UNIT
            for each_x in boards_x:
                cad_xy_board_x.append(round(float(each_x) * convert_xy,5))
            for each_y in boards_y:
                cad_xy_board_y.append(round(float(each_y) * convert_xy,5))

            offset_num = 0

            for every_board_name in board_name:
                ## THIS IS JUST TO GET THE INITIAL EMERSON JOB DONE. CHANGE THIS TO BE FLEXIBLE
                if offset_num < 8:
                    for each_inner_outline in outline_hold[1]:
                        edit = each_inner_outline.replace(" ","").replace(";","")
                        edit = edit.split(",")
                        file.write("_CIRCLE\n" + str(round(float(edit[0]) + float(cad_xy_board_x[offset_num]),5)) + "," + \
                                   str(round(float(edit[1]) + float(cad_xy_board_y[offset_num]),5)) + "\nD\n1.0\n")
                    if len(tooling_hold) > 0:
                        for each in tooling_hold[1]:
                            edit = each.replace(" 2000  ","").replace(";","").replace(" ","")
                            edit = edit.split(",")
                            file.write("_CIRCLE\n" + str(round(float(edit[0]) + float(cad_xy_board_x[offset_num]),5)) + "," + \
                                   str(round(float(edit[1]) + float(cad_xy_board_y[offset_num]),5)) + "\nD\n1.0\n")
                else:
                    for each_inner_outline in outline_hold[2]:
                        edit = each_inner_outline.replace(" ","").replace(";","")
                        edit = edit.split(",")
                        file.write("_CIRCLE\n" + str(round(float(edit[0]) + float(cad_xy_board_x[offset_num]),5)) + "," + \
                                   str(round(float(edit[1]) + float(cad_xy_board_y[offset_num]),5)) + "\nD\n1.0\n")
                holding = alternates_hold[every_board_name]
                for inner in holding:
                    edit = inner.replace(",","")
                    edit = edit.replace(";","")
                    holder = edit.split()
                    file.write("_CIRCLE\n" + str(round(float(holder[0]) + float(cad_xy_board_x[offset_num]),5)) \
                                                 + "," + str(round(float(holder[1]) + float(cad_xy_board_y[offset_num]),5)) + "\nD\n1.0\n")
                offset_num += 1
            file.close()
            
##            for nums,each_one in enumerate(board_name):
##                if nums == 0:
##                    checker = each_one
##                if each_one != checker:
##                    checker = each_one
                    
                ##edit = alternates_hold[each_one].split(",")
                ##alternates_hold[each_one]
                ##print (alternates_hold[each_one])
            
##            TOOLING WILL GO HERE

##            for index,everything in enumerate(data):
##                if outline == 1:
##                    edit = everything.replace(";","")
##                    edit = edit.replace(",","")
##                    holder = edit.split()
##                    file.write("_CIRCLE\n" + str(holder[0]) + "," + str(holder[1]) + "\nD\n1.0\n")
##                if everything == "" and outline == 1:
##                    outline = 0
##                if everything == "OUTLINE":
##                    outline = 1
                    
##                    file.write("_CIRCLE\n" + str(outer_outline_x[index]) + "," + str(outer_outline_y[index]) + "\nD\n1.0\n")
##            get_outline = []
##            get_tooling = []
##            get_alternate = []
##            for indexes,everything in enumerate(data):
##                if everything == "OUTLINE":
##                    get_outline.append(indexes)
##                if everything == "TOOLING":
##                    get_tooling.append(indexes)
##                if everything == "  ALTERNATES":
##                    get_alternate.append(indexes)
##
##            ##  GET THIS TO CHECK OUTLINE AND TOOLING TO SEE IF THERE ARE OUTER ONES INCLUDED
##            get_outline.pop(0)
##            
##            for index, brd_nms in enumerate(board_name):
##                inner_board_outline_x = []
##                inner_board_outline_y = []
##                inner_board_tooling_x = []
##                inner_board_tooling_y = []
##                inner_outline = 0
##                inner_tooling = 0
##                inner_alternates = 0
##                for line_num,everything in enumerate(data):
##                    if everything == "":
##                        inner_outline = 0
##                        inner_alternates = 0
##                    if inner_outline == 1:
##                        edit = everything.replace(";","")
##                        edit = edit.replace(",","")
##                        holder = edit.split()
##                        file.write("_CIRCLE\n" + str(round(round(float(holder[0]) + float(boards_x[index]),5) * float(convert_xy),5)) \
##                                               + "," + str(round(round(float(holder[1]) + float(boards_y[index]),5) * float(convert_xy),5)) + "\nD\n1.0\n")
##                    if inner_alternates == 1:
##                        edit = everything.replace(";","")
##                        edit = edit.replace(",","")
##                        holder = edit.split()
##                        if boards_rotation[looper] == "180.00":
##                            x = (float(holder[0]) - (float(holder[0]) * 2))
##                            y = (float(holder[1]) - (float(holder[1]) * 2))
##                            file.write("_CIRCLE\n" + str(round(round(float(x) + float(boards_x[looper]),5) * float(convert_xy),5)) \
##                                       + "," + str(round(round(float(y) + float(boards_y[looper]),5) * float(convert_xy),5)) + "\nD\n1.0\n")
##                        else:
##                            file.write("_CIRCLE\n" + str(round(round(float(holder[0]) + float(boards_x[index]),5) * float(convert_xy),5)) \
##                                           + "," + str(round(round(float(holder[1]) + float(boards_y[index]),5) * float(convert_xy),5)) + "\nD\n1.0\n")
##                    if line_num == get_outline[index]:
##                        inner_outline = 1
##                    if line_num == get_alternate[index]:
##                        inner_alternates = 1
