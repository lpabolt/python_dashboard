with open ("OUTPUTS/Parts.asc", "r") as myfile:

    data_file=myfile.readlines()

    #myfile.close not required when using with statement.
    #myfile is closed as soon as  you unindent
    
    #myfile is still open
#myfile is now closed
    ## thanks!

data_file = (line.strip() for line in data_file)

data_arr = []

line_count = 0
for line_count,everything in enumerate(data_file):
    holder = ""
    if line_count > 6:
        for c in everything:
            if c != " ":
                holder += c
            else:
                break
        data_arr.append(holder)
    
#could line_count by calculated as len(data_file)?

file = open ("OUTPUTS/Parts.asc", "w")
for everything in data_arr:
    file.write(str(everything) + "\n")
