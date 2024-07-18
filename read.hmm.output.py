import sys

species = sys.argv[1]
file_path = sys.argv[2]

#read hmm file
lines = [] 
file = open(file_path, 'r')
while True:
    line = file.readline()
    if not line:
        break
    lines.append(line)
    #print(line)
#read first block, with info on which mito(s) is aligning    
results = {}
over_dict = {}
c = 0
while lines[c] != '\n':
    #print(c)
    if "Query" in lines[c]:
        ref_species = list(filter(None,lines[c].split(" ")))[1]
    if "E-value" in lines[c]:
        try:
            if isinstance(over_dict[list(filter(None,lines[c+2].split(" ")))[8]], str):
                c = c + 2
        except:
            c = c + 3 
        break
    c += 1
while lines[c] != '\n':
    over_dict[list(filter(None,lines[c].split(" ")))[8]] = list(filter(None,lines[c].split(" ")))
    over_dict[list(filter(None,lines[c].split(" ")))[8]][9] = " ".join(list(filter(None,lines[c].split(" ")))[9:])
    over_dict[list(filter(None,lines[c].split(" ")))[8]] = over_dict[list(filter(None,lines[c].split(" ")))[8]][1:9]
    c += 1

for value in [key for key in over_dict]:
    look_for_value = str(">>" + " " + value )
    c = 0
    while c < len(lines):
        if look_for_value in lines[c]:
            c = c +3
            break
        c += 1
    #store each domain alignment for each mitochondrion

    over_dict[value].append({})
    while lines[c] != '\n':
        over_dict[value][-1][(list(filter(None,lines[c].split(" ")))[0])] = list(filter(None,lines[c].split(" ")))
        c += 1
    #get the highest score from the alignement of each mitochondrion
    max_score = 0
    for domain in [key for key in over_dict[value][-1]]:
        if float(over_dict[value][-1][domain][2]) > max_score:
            max_score = float(over_dict[value][-1][domain][2])
            accuracy = float(over_dict[value][-1][domain][15].strip('\n'))
            max_score_domain = domain
    #extract max score domain alignment
    c = 0
    while c < len(lines):
        if str("== domain " + max_score_domain) in lines[c]:
            max_domain_start = c
        c += 1
    #find next domain alignment line
    c = max_domain_start + 1 
    while c < len(lines):
        if "== domain" in lines[c]:
            next_alignment_c = c
            break
        c += 1
    results[value] = {'ref_coor_start':'a','ref_coor_end':'a','species_coor_start':'a','species_coor_end':'a','alignment_len':accuracy}

    while (max_domain_start + 5) < next_alignment_c: 
        ref_c = max_domain_start + 1
        alignment_c = ref_c + 1
        species_c = ref_c + 2
        if results[value]['ref_coor_start'] == 'a':
            results[value]['ref_coor_start'] = int(list(filter(None,lines[ref_c].split(" ")))[1])
        results[value]['ref_coor_end'] = int(list(filter(None,lines[ref_c].split(" ")))[3].strip('\n'))
        if results[value]['species_coor_start'] == 'a':
            results[value]['species_coor_start'] = int(list(filter(None,lines[species_c].split(" ")))[1])
        results[value]['species_coor_end'] = int(list(filter(None,lines[species_c].split(" ")))[3].strip('\n'))
        max_domain_start += 5

#print results
print("missing" + "\t" + "reference" + "\t" + "start_ref" + "\t" + "end_ref" + "\t" + "start_missing" + "\t" + "end_missing" + "\t" + "accuracy") 
for r_keys in results.keys():
    r_values_list = []
    for r_values in results[r_keys].values():
        r_values_list.append(r_values)
    print(species + '\t' + ref_species + '\t' + "\t".join(map(str, r_values_list)))
