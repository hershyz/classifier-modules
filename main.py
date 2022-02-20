# read data
f = open('water_potability.csv', 'r')
lines = f.readlines()

# get unique cats
cats = []

for i in range(1, len(lines)):
    if len(lines[i]) != 0:
        split = lines[i].split(',')
        cat = split[len(split) - 1].replace('\n', '')
        if cat not in cats:
            cats.append(cat)

