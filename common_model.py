from copy import deepcopy
from distutils.log import error
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


def predict_sqrt_distances(model, point):

    distances = {}
    for cat in model:
        cat_distance = 0
        cat_arr = model[cat]
        for i in range(0, len(cat_arr)):
            try:
                cat_distance += ((cat_arr[i] - point[i]) ** 2) # calculating distance between average features vs point features instead of calculating distance between each point in a dataset (higher by-classification accuracies)
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


def predict_abs_distances(model, point):

    distances = {}
    for cat in model:
        cat_distance = 0
        cat_arr = model[cat]
        for i in range(0, len(cat_arr)):
            try:
                cat_distance += abs(cat_arr[i] - point[i]) # calculating raw abs distance between average feature and point feature
            except:
                continue
        distances[cat] = cat_distance
    
    min_distance = 1000000000000
    min_cat = ''
    for cat in distances:
        if distances[cat] < min_distance:
            min_distance = distances[cat]
            min_cat = cat

    return min_cat


def predict_percent_error(model, point): # this model is basically useless

    distances = {}
    for cat in model:
        cat_error = 0
        cat_arr = model[cat]
        for i in range(0, len(cat_arr)):
            try:
                cat_error += (abs(cat_arr[i] - point[i]) / cat_arr[i])
            except:
                continue
        distances[cat] = cat_error
    
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


# parse raw data
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


print('FORMAT: {class: [correct, total]}')


# predict_sqrt_distances
accs = {}
for cat in model:
    accs[cat] = [0, 0] # [correct, total]
for point in points:
    real = str(point[len(point) - 1])
    real = real.replace('.0', '')
    prediction = predict_sqrt_distances(model, point)
    arr = accs[real]
    if real == prediction:
        arr[0] += 1
    arr[1] += 1
    accs[real] = deepcopy(arr)
print('predict_sqrt_distances: ' + str(accs))


# predict_abs_distances
accs = {}
for cat in model:
    accs[cat] = [0, 0] # [correct, total]
for point in points:
    real = str(point[len(point) - 1])
    real = real.replace('.0', '')
    prediction = predict_abs_distances(model, point)
    arr = accs[real]
    if real == prediction:
        arr[0] += 1
    arr[1] += 1
    accs[real] = deepcopy(arr)
print('predict_abs_distances: ' + str(accs))


# predict_percent_error
accs = {}
for cat in model:
    accs[cat] = [0, 0] # [correct, total]
for point in points:
    real = str(point[len(point) - 1])
    real = real.replace('.0', '')
    prediction = predict_percent_error(model, point)
    arr = accs[real]
    if real == prediction:
        arr[0] += 1
    arr[1] += 1
    accs[real] = deepcopy(arr)
print('predict_percent_error: ' + str(accs))