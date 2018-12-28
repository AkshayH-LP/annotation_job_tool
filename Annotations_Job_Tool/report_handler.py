import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def annotations_and_score(index, df, maximum_annotators, mode = 'random', seed = 1):
    """
    Calucalte the aggregate label randomly or in time or by trust
    
    args: 
        df: Dataframe of full results with True_lables
        Columns that must exist:
            id: id for sample - in this case 'Message_id' please check for your dataframe
            True_intent: True_label for the sample
            _intent: label chosen by the current annotator
            _trust: trust score for the annotator
            if in time: _created_at: To sort the annotations in time
        
        maximum_annotators: Maximum number of annotators involved 
        mode: 
            1. random: n random picks from all made by annotators per sample
            2. time: Sequential picks in order of n to decide early stopping
            3. trust: Based on decreasing order of trust score for an annotator
            
    returns:
        Pandas DataFrame containing for a sample the label and confidence
        for  2 to 'maximum' number of annotators
        columns = ['message_id', 'True_intent', '_label', '_confidence', 'n_ann']
    """
    
    ## Group - By 'uid'
    groups = df.groupby(index)

    ## Output DataFrame
    cols = [index, 'True_intent', '_label', '_confidence', 'n_ann']
    output = pd.DataFrame(columns = cols)
    
    ## Dividing all the message groups into bunch of 20 each for better CPU runtime
    mini_group = np.array_split(list(groups.groups), 20)
    
    ## Unique Labels in the input DataFrame
    outputs = df['True_intent'].unique()
    
    ## Setting the seed
    if mode == 'random': np.random.seed(seed)
    
    ## Find annotations label and confidence score in random, time or based on trust and calculate the confidence score
    for batch in tqdm(mini_group):
        ## mini_group = A subset of groups, groups divided into min_group
        for group in batch:
            message_group = groups.get_group(group)
            
            if mode == 'time':
                message_group = message_group.sort_values(by = '_created_at')
            
            if mode == 'trust':
                message_group = message_group.sort_values(by = '_trust')
            
            for num_annotators in range(2, maximum_annotators):
                if num_annotators > len(message_group): break
                    
                if mode == 'random':
                    full_df = message_group.sample(n = num_annotators, random_state = seed)
                if mode == 'time':
                    full_df = message_group[:num_annotators]
                
                ## Dictionary to store chosen label and it's confidence score
                cur = {}
                
                ## Message/Sample id in consideration
                uid = full_df[index].iloc[0]
                
                ## True_intent of the Message/Sample
                true_intent = full_df['True_intent'].iloc[0]
                
                ## Denominator for the weighted sum calculation
                weighted_sum_denom = sum(full_df['_trust'])
                
                ## For each choice on label, calculate it's weighted confidence score
                for chosen_intent in full_df['_intent'].unique():
                    df_ = full_df[full_df['_intent'] == chosen_intent]
                    confidence_intent = sum(df_['_trust'])/ weighted_sum_denom
                    cur[chosen_intent] = confidence_intent
                
                ### Sort all the labels and their confidence score in decreasing order of confidence
                cur = list(sorted(cur.items(), key = lambda x: x[1], reverse = True))                
                
                ### Update output dataFrame with all choices of labels and confidence scores in n_annotators
                for n in range(len(cur)):
                    df = pd.DataFrame([[uid, true_intent, cur[n][0], cur[n][1], num_annotators]], columns = cols)
                    output = output.append(df, ignore_index = True)
    return output