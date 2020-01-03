import pandas as pd
import glob
# Collaborators Carlos S. - file manipulation
# Worked on appendicitis KEEL folder

def main():

    path_to_keel_data = input("please input the path to the specific keel data. Ex. a path including banana-10-fold\n")
    k_value = input('please input K\n')
    k_value = int(k_value)
    # find_attributes(path_to_keel_data)

    training_set = glob.glob(path_to_keel_data + '/*tra.dat')
    test_set = glob.glob(path_to_keel_data + '/*tst.dat')

    training_set.sort()
    test_set.sort()

    # print(training_set)
    # print(test_set)

    cleaned_training_set = []
    cleaned_test_set = []

    #iterates through files and demarcates train v test
    for file in training_set:
        cleaned_training_set.append(clean(file))
    for file in test_set:
        cleaned_test_set.append(clean(file))
    cleaned_test_setsdfsandlabels = []
    cleaned_training_setsdfsandlabels =[]
    for file in cleaned_training_set:
        cleaned_training_set_df = pd.read_csv(file, header=None)
        # print(cleaned_training_set_df)
        cleaned_test_set_df = pd.read_csv(file, header=None)
        #print(cleaned_test_set_df)
        df = cleaned_test_set_df.reset_index()
        df = df.drop('index', axis=1)
        labels = df[df.columns[len(df.columns) - 1]]
        df.drop(df.columns[len(df.columns) - 1], axis=1, inplace=True)
        #print(labels)
        #print(df)
        cleaned_training_setsdfsandlabels.append(df)
        cleaned_training_setsdfsandlabels.append(labels)
    #C:\Users\Anish Prasanna\PycharmProjects\Anish_Prasanna_knn\appendicitis-10-fold
    for file in cleaned_test_set:
        cleaned_test_set_df = pd.read_csv(file, header=None)
        #print(cleaned_test_set_df)
        df = cleaned_test_set_df.reset_index()
        df = df.drop('index', axis=1)
        labels = df[df.columns[len(df.columns) - 1]]
        df.drop(df.columns[len(df.columns) - 1], axis=1, inplace=True)
        #print(labels)
        #print(df)
        cleaned_test_setsdfsandlabels.append(df)
        cleaned_test_setsdfsandlabels.append(labels)

    testandlabel = cleaned_test_setsdfsandlabels
    trainandlabel = cleaned_training_setsdfsandlabels
    #for i in range(20):
        #print(trainandlabel[i])
        #print(testandlabel[i])
    #starts from 10-10
    classificationlabs = []
    j=0
    classlist = list()
    for i in range(0, 20, 2):
        classlist.append(classifytest(trainandlabel[i], trainandlabel[i+1], testandlabel[i], testandlabel[i+1], k_value))

    for i in range(1,20,2):
        testandlabel[i]=testandlabel[i].to_frame(name = 'label')

    for i in range(0,10,1):
        classlist[i]['label'] = classlist[i]['label'].apply(pd.to_numeric)


    #Determines accuracies based on KNN alg for each fold and averages
    accuracytotal = 0
    print("Accuracies below for each fold (10-9)")
    for i in range(1,20,2):
        print(accuracy(testandlabel[i],classlist[j]))
        accuracytotal = accuracytotal + accuracy(testandlabel[i],classlist[j])
        j=j+1
    print("Avg overall accuracy")
    print(accuracytotal/10)

#cleans data
def clean(original_file):
    with open(original_file, "r") as f:
        lines = f.readlines()
    with open(original_file, "w") as f:
        for line in lines:
            if '@' not in line:
                f.write(line)
    return original_file

#finds dis between 2 points
def dis(obj1, obj2):
    squarediff = 0
    for i in range(len(obj1)):
        squarediff = (obj1[i] - obj2[i]) ** 2
    finaldis = squarediff ** .5
    return finaldis

 # finds k neighbors and returns prediction for one point
def classify(unknown, dataset, labels, k_value):
    distances = pd.DataFrame(columns=('Dist', 'label'))
    # Looping through all points in the dataset
    for i in range(len(dataset)):
        distances.loc[i] = list([dis(dataset.iloc[i], unknown), labels[i]])

    distances = distances.sort_values('Dist')
    distances = distances.reset_index()

    kneighbors = distances[0:k_value]


    Op1 = 0
    Op2 = 0
    for i in range(len(kneighbors)):
        if kneighbors.at[i, 'label'] == 1:
            Op1 = Op1 + 1
        else:
            Op2 = Op2 + 1
    # if equal go with Op1
    if Op1 > Op2:
        return 1
    else:
        return 0
#compares label sets and finds decimal
def accuracy(testlabels,classifylabels):
    correct = 0

    for i in range(len(testlabels)):

        if (testlabels.loc[i,'label'].item() == classifylabels.loc[i,'label'].item()):
            correct = correct +1
    return (correct/len(testlabels))

#clasifies every point in test set
def classifytest(train, trainlabels, test, testlabels, k):  # function by Anish Prassana
    predictions = pd.DataFrame(columns=(['label']))
    classifications = []
    for i in range(len(test)):
        predictions.loc[i] = list([classify(test.iloc[i], train, trainlabels, k)])
    return predictions


if __name__ == '__main__':
    main()
