import fileinput
from statistics import fmean, stdev
from random import randint

filein = []
num_features = 0

filename = str(input("Enter the name of the file you would like to use:"))

for line in fileinput.input(filename):
    array = [ float(i) for i in line.split() ]
    filein.append(array)

fileinput.close()   
num_features = len(filein[0]) - 1

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
                accuracy_i = randint(0,1000) / 1000 
                print("Considering features " + str(temp_set)+": accuracy of " + str(accuracy_i))
                if(accuracy_i > max_accuracy_i):
                    max_accuracy_i = accuracy_i
                    max_i = i
        print("Adding " + str(max_i) + " to the feature set")
        current_set = current_set.union({max_i})
        if(max_accuracy_i > max_accuracy):
            max_set = current_set.copy()
            max_accuracy = max_accuracy_i
            print("Found new max: " + str(max_set)+":"+str(current_set) + " with accuracy: " + str(max_accuracy)+":"+str(max_accuracy_i))
        search_level+=1

    print("Best set was "+str(max_set)+" with accuracy of "+str(max_accuracy))

def search_feature_space_backward(data_in):
    all_features = range(1,num_features+1) #num_features+1 is not included
    current_set = set(all_features)
    max_set = current_set.copy()
    max_accuracy = randint(0,1000) / 1000 #set max_accuracy equal to accuracy of all features set 
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
                accuracy_i = randint(0,1000) / 1000 
                print("Considering features " + str(temp_set)+": accuracy of " + str(accuracy_i))
                if(accuracy_i > max_accuracy_i):
                    max_accuracy_i = accuracy_i
                    max_i = i
        print("Removing " + str(max_i) + " from the feature set")
        current_set = current_set.difference({max_i})
        if(max_accuracy_i > max_accuracy):
            max_set = current_set.copy()
            max_accuracy = max_accuracy_i
            print("Found new max: " + str(max_set)+":"+str(current_set) + " with accuracy: " + str(max_accuracy)+":"+str(max_accuracy_i))
        search_level+=1

    print("Best set was "+str(max_set)+" with accuracy of "+str(max_accuracy))



search_feature_space_backward(filein)
