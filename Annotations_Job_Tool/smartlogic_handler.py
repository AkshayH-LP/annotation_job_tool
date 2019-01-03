import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def get_data(path):
    ### Load data from Hierarchal report with details
    df = pd.read_csv(path)
    df = df[['level1', 'level2', 'metadata_definition_en_displayName']]
    df = df.iloc[1:]
    df = df.rename({'metadata_definition_en_displayName': 'summary'}, axis = 'columns')
    regex_parser = re.compile(r'<.*?>')
    df = df.replace(np.NAN, 'None')
    df['summary'] = df['summary'].apply(lambda x: regex_parser.sub('', x)).apply(lambda x: x.replace("'",""))
    return df


def get_fig8_data(df, levels = 3):
    ## Reformat the data in the order of levels for every intent 
    def recursive_rw_check(prev, idx, row, level):
        for i in range(len(level)):
            if row['level' + str(i+1)] == 'None' and prev == False:
                df.loc[idx, 'level' + str(i+1)] = level[i]
            else:
                if row['level' + str(i+1)] != 'None':
                    level[i] = row['level' + str(i + 1)] 
                    prev = True
    
    level = [None]*(levels - 1)
    for idx, row in df.iterrows():
        prev = False
        recursive_rw_check(prev, idx, row, level)
    return df

def csv_to_js(df, levels = 2):
    ### Convert the contents of the csv to the js file
    cols = df.columns
    top_level = []
    taxonomy_items = {}
    
    
    for idx, row in df.iterrows():
        hierarchy = [None] * (levels)
        prop = {}
        for i in range(levels):
            if row['level'+str(i+1)] != 'None': hierarchy[i] = row['level'+str(i+1)]
        while None in hierarchy: hierarchy.remove(None)
        
        if len(hierarchy) == 1:
            prop["title"] = hierarchy[-1]
            prop["children"] = []
            prop["summary"] = row["summary"]
            taxonomy_items[str(idx)] = prop
            top_level += [str(idx)]
        
        else:
            prop["title"] = hierarchy[-1]
            prop["parent"] = hierarchy[-2]
            prop["summary"] = row["summary"]
            taxonomy_items[str(idx)] = prop
            
            parent = hierarchy[len(hierarchy) - 2]
            child = hierarchy[len(hierarchy) - 1]
            for idx3, prop in taxonomy_items.items():
                if prop["title"] == parent:
                    prop['children'] += [idx]
                    break
    js_dict = {"topLevel": top_level, "taxonomyItems": taxonomy_items}     
    return js_dict

def create_tax_js(path, name):
    ### Create .js file of the taxonomy

    js_dict = csv_to_js(get_fig8_data(get_data(path), 2), 2)
    with open(str(name) + '.js', 'a') as outfile: 
        outfile.write("var "+ str(name) +" = " + str(json.dumps(js_dict))+";")