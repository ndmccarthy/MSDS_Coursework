import math
import pandas as pd
import operator


# DECISION TREE INDUCTION

def information_gain_target(dataset_file): 
    
#        Input: dataset_file - A string variable which references the path to the dataset file.
#        Output: ig_loan - A floating point variable which holds the information entropy associated with the target variable.
#        
#        NOTE: 
#        1. Return the information gain associated with the target variable in the dataset.
#        2. The Loan attribute is the target variable
#        3. The pandas dataframe has the following attributes: Age, Income, Student, Credit Rating, Loan
#        4. Perform your calculations for information gain and assign it to the variable ig_loan


    df = pd.read_csv(dataset_file)
    ig_loan = 0
    
    # calculate Info(D)
    # D = data
    # m = # of classes
    # Ci = ith class
    # p(Ci) = probability of ith class
    # Info(D) = sum(-p(Ci)log2(p(Ci)))
    
    # calculate p(Ci)
    # grab loan column
    loan = df['Loan']
    # count each entry type
    loan_options = {}
    for decision in loan:
        # check if decision is already in loan_options
        if decision in loan_options:
            # add to value
            loan_options[decision] += 1
        else:
            loan_options[decision] = 1
    total_decisions = len(loan)
    # store p(Ci) in list
    pCi = []
    for key, value in loan_options.items():
        probability = value/total_decisions
        pCi.append(probability)
    # calculate inidividual entries and sum
    for probability in pCi:
        entry = -1 * probability * math.log2(probability)
        ig_loan += entry
    return ig_loan

def information_gain(p_count_yes, p_count_no):
    
#   A helper function that returns the information gain when given counts of number of yes and no values. 
#   Please complete this function before you proceed to the information_gain_attributes function below.
    
    # calculate p(Ci)
    total = p_count_yes + p_count_no
    pyes = p_count_yes/total
    pno = p_count_no/total
    # calculate entry (take care of 0 instance, where log0 is undefined)
    if pyes == 0:
        yes_entry = 0
    else:
        yes_entry = -1 * pyes * math.log2(pyes)
    if pno == 0:
        no_entry = 0
    else:
        no_entry = -1 * pno * math.log2(pno)
    # sum entries
    ig = yes_entry + no_entry
    return ig

def information_gain_attributes(dataset_file, ig_loan, attributes, attribute_values):
    
#        Input: 
#            1. dataset_file - A string variable which references the path to the dataset file.
#            2. ig_loan - A floating point variable representing the information gain of the target variable "Loan".
#            3. attributes - A python list which has all the attributes of the dataset
#            4. attribute_values - A python dictionary representing the values each attribute can hold.
#            
#        Output: results - A python dictionary representing the information gain associated with each variable.
#            1. ig_attributes - A sub dictionary representing the information gain for each attribute.
#            2. best_attribute - Returns the attribute which has the highest information gain.
#        
#        NOTE: 
#        1. The Loan attribute is the target variable
#        2. The pandas dataframe has the following attributes: Age, Income, Student, Credit Rating, Loan
    
    # initialize results
    results = {
        "ig_attributes": {
            "Age": 0,
            "Income": 0,
            "Student": 0,
            "Credit Rating": 0
        },
        "best_attribute": ""
    }
    # read in dataset
    df = pd.read_csv(dataset_file)
    df_count = len(df)
    # loop through each attribute to get info gain
    for attribute in attributes:
        # initialize info gain for attribute
        ig_attribute = 0
        # filter df by attribute and loan
        att_loan_df = df.filter(items = [attribute, 'Loan'], axis=1)
        # calculate Info^A(D)
        for att_value in attribute_values[attribute]:
            # filter df by value
            filtered_att_loan_df = att_loan_df[att_loan_df[attribute] == att_value]
            # calculate first part of equation
            total_att_value_count = len(filtered_att_loan_df)
            first_part = total_att_value_count/df_count
            # calculate Info
            # get counts
            yes_count = len(filtered_att_loan_df[filtered_att_loan_df['Loan'] == 'yes'])
            no_count = len(filtered_att_loan_df[filtered_att_loan_df['Loan'] == 'no'])
            ig = information_gain(yes_count, no_count)
            # multiply both parts
            entry = first_part * ig
            # add entry to attribute's info gain sum
            ig_attribute += entry
        # place ig in results dictionary (remember to subtract attribute ig from total ig)
        results["ig_attributes"][attribute] = ig_loan - ig_attribute
    # find and record best attribute in results dictionary
    results["best_attribute"] = max(results["ig_attributes"].items(), key=operator.itemgetter(1))[0]
    return results




# NAIVE BAYESIAN CLASSIFICATION

def naive_bayes(dataset_file, attributes, attribute_values):
# assumes no dependence between attributes!
#   Input:
#       1. dataset_file - A string variable which references the path to the dataset file.
#       2. attributes - A python list which has all the attributes of the dataset (except "Loan", the target attribute)
#       3. attribute_values - A python dictionary representing the values each attribute can hold.
#        
#   Output: A probabilities dictionary which contains the values of when the input attribute is yes or no
#       depending on the corresponding Loan attribute.
#                
#   Hint: Starter code has been provided to you to calculate the probabilities.
    
    # initialize probabilities dictionary
    probabilities = {
        "Age": { "<=30": {"yes": 0, "no": 0}, "31-40": {"yes": 0, "no": 0}, ">40": {"yes": 0, "no": 0} },
        "Income": { "low": {"yes": 0, "no": 0}, "medium": {"yes": 0, "no": 0}, "high": {"yes": 0, "no": 0}},
        "Student": { "yes": {"yes": 0, "no": 0}, "no": {"yes": 0, "no": 0} },
        "Credit Rating": { "fair": {"yes": 0, "no": 0}, "excellent": {"yes": 0, "no": 0} },
        "Loan": {"yes": 0, "no": 0}
    }
    # read in dataset
    df = pd.read_csv(dataset_file)
    df_count = len(df)
    
    # calculate "Loan" entry for probabilities dictionary (prior likelihood)
    vcount = df["Loan"].value_counts()
    vcount_loan_yes = vcount["yes"]
    vcount_loan_no = vcount["no"]
    probabilities["Loan"]["yes"] = vcount_loan_yes/df_count # P(Ci) -> P(yes)
    probabilities["Loan"]["no"] = vcount_loan_no/df_count # P(Ci) -> P(no)
    
    # filter df by yes and no in Loan for future use
    yes_df = df[df['Loan'] == 'yes']
    no_df = df[df['Loan'] == 'no']
    
    # calculate all other entries for probabilities dictionary
    # work through each attribute
    for attribute in attributes:
        # get counts based on yes/no
        yesUatt_vcount = yes_df[attribute].value_counts()
        noUatt_vcount = no_df[attribute].value_counts()
        # deal with instances where a 0 occurs in yesUatt or noUatt (Laplacian correction)
        if 0 in yesUatt_vcount or 0 in noUatt_vcount:
            for att_value_count in yesUatt_vcount:
                att_value_count += 1
            for att_value_count in noUatt_vcount:
                att_value_count += 1
        # make into frequency and store in probabilities results
        for value, count in yesUatt_vcount.items():
            p_attvalueGyes = count/vcount_loan_yes # P(att_value | yes)
            probabilities[attribute][value]['yes'] = p_attvalueGyes
        for value, count in noUatt_vcount.items():
            p_attvalueGno = count/vcount_loan_no # P(att_value | no)
            probabilities[attribute][value]['no'] = p_attvalueGno
    return probabilities