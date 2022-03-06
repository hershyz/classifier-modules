from copy import deepcopy
import math

def percent_classifier_model(path):
    
    # read lines and find unique categories
    f = open(path, 'r')
    lines = f.readlines()
    cats = []
    for i in range(1, len(lines)):
        split = lines[i].split(',')
        cat = split[len(split) - 1].replace('\n', '')
        if cat not in cats:
            cats.append(cat)
    
    # populate init quantity totals
    model = {}
    n_features = len(lines[0].split(',')) - 1
    init_arr = []
    for i in range(0, n_features):
        init_arr.append(0)
    for cat in cats:
        model[cat] = init_arr

    # populate init category frequencies
    freq = {}
    for cat in cats:
        freq[cat] = 0

    # add feature totals
    for i in range(1, len(lines)):
        data = lines[i].replace('\n', '').split(',')
        cat = data[len(data) - 1]
        arr = model[cat]
        for j in range(0, len(arr)):
            try:
                arr[j] += float(data[j])
            except:
                continue
        model[cat] = deepcopy(arr)
        freq[cat] = freq[cat] + 1
    
    # calculate averages
    for cat in cats:
        arr = model[cat]
        n = freq[cat]
        for i in range(0, len(arr)):
            arr[i] /= n
        model[cat] = deepcopy(arr)

    return model


def predict(model, point):

    distances = {}
    for cat in model:
        cat_distance = 0
        cat_arr = model[cat]
        for i in range(0, len(cat_arr)):
            try:
                cat_distance += (abs(cat_arr[i] - point[i]) ** 2)
                distance_total += 1
            except:
                continue
        cat_distance = math.sqrt(cat_distance)
        distances[cat] = cat_distance
    
    min_distance = 1000000000000
    min_cat = ''
    for cat in distances:
        if distances[cat] < min_distance:
            min_distance = distances[cat]
            min_cat = cat

    return min_cat


# training
dataset = 'cervical_cancer.csv'
model = percent_classifier_model(dataset)
'''
model:
{
    '0': [26.696139476961395, 2.4495641344956414, 16.841843088418432, 2.12079701120797, 0.14072229140722292, 1.1362361403810708, 0.43212134018792037, 0.5541718555417185, 1.8802296401519307, 0.0921544209215442, 0.4264881693648817, 0.08343711083437111, 0.14072229140722292, 0.0460772104607721, 0.0, 0.0049813200498132005, 0.0448318804483188, 0.0224159402241594, 0.0012453300124533001, 0.0, 0.0012453300124533001, 0.0, 0.0161892901618929, 0.0012453300124533001, 0.0024906600249066002, 0.07970112079701121, 0.47198007471980075, 0.44333748443337484, 0.014943960149439602, 0.007471980074719801, 0.014943960149439602, 0.021170610211706103, 0.012453300124533, 0.0323785803237858, 0.0323785803237858],
    '1': [28.963636363636365, 2.5454545454545454, 17.345454545454544, 2.2363636363636363, 0.18181818181818182, 2.1503085983454544, 0.6529673114127272, 0.6545454545454545, 3.3179999999999996, 0.16363636363636364, 0.7090909090909091, 0.21818181818181817, 0.36363636363636365, 0.12727272727272726, 0.0, 0.0, 0.12727272727272726, 0.0, 0.0, 0.01818181818181818, 0.0, 0.0, 0.09090909090909091, 0.0, 0.0, 0.2, 1.0363636363636364, 1.0363636363636364, 0.10909090909090909, 0.05454545454545454, 0.10909090909090909, 0.12727272727272726, 0.45454545454545453, 0.8727272727272727, 0.32727272727272727]
}
'''


# prediction sequence
f = open(dataset, 'r')
lines = f.readlines()
points = []
for i in range(1, len(lines)):
    arr = lines[i].split(',')
    point = []
    for elem in arr:
        try:
            point.append(float(elem))
        except:
            point.append('?')
    points.append(point)


# overall accuracy
total = 0
correct = 0
for point in points:
    real = str(point[len(point) - 1])
    real = real.replace('.0', '')
    prediction = predict(model, point)
    if real == prediction:
        correct += 1
    total += 1

print('accuracy: ' + str(correct / total))


# positive test accuracy
total = 0
correct = 0
for point in points:
    real = str(point[len(point) - 1])
    real = real.replace('.0', '')
    if real == '1':
        if predict(model, point) == real:
            correct += 1
        total += 1

print('positive test accuracy: ' + str(correct / total))