import fileinput
from statistics import fmean, stdev
from random import randint
from math import dist

filein = []
num_features = 0

filename = str(input("Enter the name of the file you would like to use:"))

for line in fileinput.input(filename):
    array = [ float(i) for i in line.split() ]
    filein.append(array)

fileinput.close()   
num_features = len(filein[0]) - 1
data_len = len(filein)

print("This dataset has "+str(num_features)+" features, with "+str(data_len)+" instances.")

def normalize(arrayin, arrayout):
    mean_val = fmean(arrayin)
    stddev_val = stdev(arrayin, mean_val)
    for x in arrayin:
        arrayout.append((x - mean_val) / stdev_val)

def search_feature_space_forward(data_in):
    all_features = range(1,num_features+1) #num_features+1 is not included
    current_set = set()
    max_set = set()
    max_accuracy = 0

    search_level = 1
    while(len(current_set) < num_features):
        print("On search level " + str(search_level))
        max_i = -1
        max_accuracy_i = 0
        for i in all_features:
            if i not in current_set:
                # create temp set of features #'s
                temp_set = current_set.union({i})
                # test temp set of features, get accuracy
                accuracy_i = cross_validation(data_in, temp_set) 
                print("Considering features " + str(temp_set)+": accuracy of " + str(accuracy_i))
                if(accuracy_i > max_accuracy_i):
                    max_accuracy_i = accuracy_i
                    max_i = i
        print("Adding " + str(max_i) + " to the feature set")
        current_set = current_set.union({max_i})
        if(max_accuracy_i > max_accuracy):
            max_set = current_set.copy()
            max_accuracy = max_accuracy_i
            print("Found new max: " + str(max_set)+ " with accuracy: " + str(max_accuracy))
        search_level+=1

    print("Best set was "+str(max_set)+" with accuracy of "+str(max_accuracy))

def search_feature_space_backward(data_in):
    all_features = range(1,num_features+1) #num_features+1 is not included
    current_set = set(all_features)
    max_set = current_set.copy()
    max_accuracy = cross_validation(data_in, current_set) #set max_accuracy equal to accuracy of all features set 
    print("Considering all features: "+str(current_set)+": accuracy of " + str(max_accuracy))

    search_level = 1
    while(len(current_set) > 1):
        print("On search level " + str(search_level))
        max_i = -1
        max_accuracy_i = 0
        for i in all_features:
            if i in current_set:
                # create temp set of features #'s
                temp_set = current_set.difference({i})
                # test temp set of features, get accuracy
                accuracy_i = cross_validation(data_in, temp_set)
                print("Considering features " + str(temp_set)+": accuracy of " + str(accuracy_i))
                if(accuracy_i > max_accuracy_i):
                    max_accuracy_i = accuracy_i
                    max_i = i
        print("Removing " + str(max_i) + " from the feature set")
        current_set = current_set.difference({max_i})
        if(max_accuracy_i > max_accuracy):
            max_set = current_set.copy()
            max_accuracy = max_accuracy_i
            print("Found new max: " + str(max_set)+ " with accuracy: " + str(max_accuracy))
        search_level+=1

    print("Best set was "+str(max_set)+" with accuracy of "+str(max_accuracy))

def cross_validation(data_in, feature_set):
    num_correct = 0

    #only consider features in feature set
    data = []
    for d in data_in:
        row = [ d[f] for f in feature_set ] 
        row.insert(0, d[0])
        data.append(row)

    for i in range(len(data)): # choose an data point to ignore
        correct_label_i = data[i][0]

        nearest_neighbor_dist = float('inf')
        nearest_neighbor_index = float('inf')
        nearest_neighbor_label = -1
        for j in range(len(data)):
            if i != j:
                # find distance
                distance = dist(data[i][1:], data[j][1:])
                #compare to closest so far
                if distance < nearest_neighbor_dist:
                    nearest_neighbor_dist = distance
                    nearest_neighbor_index = j
                    nearest_neighbor_label = data[j][0]

        if nearest_neighbor_label == correct_label_i:
            num_correct+=1

    accuracy = num_correct / len(data)
    return accuracy

alg_choice = int(input("""Which algorithm do you want to use?
        1) Forward Selection
        2) Backward Selection

        """))

if alg_choice == 1:
    search_feature_space_forward(filein)
elif alg_choice == 2:
    search_feature_space_backward(filein)
else:
    print("Input not recognized. Quitting.")

