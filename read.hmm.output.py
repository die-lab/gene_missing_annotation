import sys

species = sys.argv[1]
file_path = sys.argv[2]


lines = [] 
file = open(file_path, 'r')
while True:
    line = file.readline()
    if not line:
        break
    lines.append(line)
    print(line)
    
over_dict = {}
c = 6
while lines[c] != '\n':
    over_dict[list(filter(None,lines[6].split(" ")))[8]] = list(filter(None,lines[6].split(" ")))
    over_dict[list(filter(None,lines[6].split(" ")))[9]] = " ".join(over_dict[list(filter(None,lines[6].split(" ")))[9:]])
    c += 1 


for value in [key for key in over_dict]:
    look_for_value = str(">>" + " " + value )
    c = 0
    
    while c < len(lines):
        if look_for_value in lines[c]:
            print(lines[c])
        c += 1
            
    
