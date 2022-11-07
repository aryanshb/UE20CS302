'''
Assume df is a pandas dataframe object of the dataset given
'''

import numpy as np
import pandas as pd
import random


#Calculate the entropy of the enitre dataset
# input:pandas_dataframe
# output:int/float
def get_entropy_of_dataset(df):
    total_row = df.shape[0]
    total_entropy = 0

    for i in df['play'].unique():
        p = df['play'].value_counts()[i]/total_row
        total_entropy += -p*np.log2(p)
    return total_entropy
'''Return avg_info of the attribute provided as parameter'''
# input:pandas_dataframe,str   {i.e the column name ,ex: Temperature in the Play tennis dataset}
# output:int/float
def get_avg_info_of_attribute(df, attribute):
    total_row = df.shape[0]
    total_avg_info = 0
    for i in df[attribute].unique():
        p = df[attribute].value_counts()[i]/total_row
        total_avg_info += p*get_entropy_of_dataset(df[df[attribute] == i])
    return total_avg_info
    


'''Return Information Gain of the attribute provided as parameter'''
# input:pandas_dataframe,str
# output:int/float
def get_information_gain(df, attribute):
    return get_entropy_of_dataset(df) - get_avg_info_of_attribute(df, attribute)


#input: pandas_dataframe
#output: ({dict},'str')
def get_selected_attribute(df):
    '''
    Return a tuple with the first element as a dictionary which has IG of all columns 
    and the second element as a string with the name of the column selected

    example : ({'A':0.123,'B':0.768,'C':1.23} , 'C')
    '''
    IG = {}
    for i in df.columns[:-1]:
        IG[i] = get_information_gain(df, i)
    return (IG, max(IG, key=IG.get))

    
