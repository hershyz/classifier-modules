import random

# read data
f = open('cervical_cancer.csv', 'r')
lines = f.readlines()

# get unique cats
cats = []

for i in range(1, len(lines)):
    if len(lines[i]) != 0:
        split = lines[i].split(',')
        cat = split[len(split) - 1].replace('\n', '')
        if cat not in cats:
            cats.append(cat)

# make predictions
def predict(point):

    percents = {}
    totals = {}
    for cat in cats:
        percents[cat] = 0
        totals[cat] = 0

    for i in range(1, len(lines)):
        
        comparison = lines[i].replace('\n', '').split(',')
        comparison_cat = comparison[len(comparison) - 1]

        error = 0
        curr_total = 0
        for j in range(0, len(point) - 1):
            try:
                num = float(point[j])
                comparison_num = float(comparison[j])
                error += abs((comparison_num - num) / num)
                curr_total += 1
            except Exception as e:
                # print(e)
                continue
        percents[comparison_cat] = percents[comparison_cat] + (error / curr_total)
        totals[comparison_cat] = totals[comparison_cat] + 1

    min = percents[cats[0]] / totals[cats[0]]
    min_cat = cats[0]
    for cat in cats:
        curr = percents[cat] / totals[cat]
        if curr < min:
            min = curr
            min_cat = cat
    
    return min_cat





# predict only positive tests
# correct = 0
# total = 0
# for i in range(0, len(lines)):
#     point = lines[i].replace('\n', '').split(',')
#     expected = str(point[len(point) - 1])
#     if expected == '1':
#         prediction = str(predict(point))
#         if prediction == expected:
#             correct +=1
#         total += 1
# print('acc: ' + str(correct / total))
        

# sample acc
# points = []
# for i in range(0, 100):
#     points.append(random.randrange(0, len(lines) - 1))

# entire (population) acc
points = []
for i in range(1, len(lines)):
    points.append(i)

total = 0
correct = 0

for i in range(0, len(points)):
    point = lines[points[i]].replace('\n', '').split(',')
    real = str(point[len(point) - 1])
    prediction = str(predict(point))
    # print(str(real) + ', ' + str(prediction))
    if real == prediction:
        correct += 1
    total += 1

acc = (correct / total) * 100
print('accuracy: ' + str(acc))