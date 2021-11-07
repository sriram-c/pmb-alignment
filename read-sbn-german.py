import sys

with open(sys.argv[1], 'r') as f:
    cont = f.readlines()

for line in cont:
    if ' % ' in line:
        eng_root = line.split('%')[0].split()[0]

        if(len(line.split('%')[1].strip()) > 0):
            de_root = line.split('%')[1].split('[')[0].strip()
            print([de_root], line.strip())
        else:
            print(line.strip())
    else:
        print(line.strip())