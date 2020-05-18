import numpy as np
import pandas as pd
from os.path import join
import datetime

def get_cluster(filename, cluster_num):
    df = pd.read_csv(filename)
    fips = df.loc[df['cluster'] == cluster_num, 'FIPS']
    return fips.values

def calculate_rt(r0, alphas, interventions):
    rt = r0 - alphas * covariates
    return rt

def calculate_cases(rt, population, si):
    n = len(rt)
    cases = np.zeros(n) 
    for i in range(2,n):
        case = np.sum(infected[0:i] * si[i-1::-1])
        rt_adj = (population -np.sum(infected)) / population * rt[i]
        cases[i] = rt_adj * case
    return cases

def calculate_deaths(cases, ifr, fatality):
    n = len(rt)
    deaths = np.zeros(n)
    deaths[0] = 1e-15*infected[0]
    for i in range(1,n):
        death = np.sum(cases[0:i] * fatality[i-1::-1])
        deaths[i] = ifr * death
    return deaths    

def get_npis(data_dir):
    interventions_path = join(data_dir, 'us_data/interventions.csv')
    interventions = pd.read_csv(interventions_path)
    id_cols = ['FIPS', 'STATE', 'AREA_NAME']    
    int_cols = [col for col in interventions.columns.tolist() if col not in id_cols]
    interventions.drop(columns=['STATE', 'AREA_NAME'], inplace=True)

    interventions.drop([0], axis=0, inplace=True)
    interventions.fillna(1, inplace=True)
    return interventions

def get_counties_isolated_NPIs(npis, index):
    #print(npis.head())
#    to_keep = []
    num_of_cols = npis.shape[1] - 1
#    for i in range(npis.shape[0]):
#        #print(npis.iloc[i, 1:])
#        iso = [x for x in np.unique(npis.iloc[i, 1:]) if x!=1.0]        
#        if len(iso) >= num_of_cols  - 1:
#            #print(npis.iloc[i, :]['FIPS'])
#            to_keep.append(npis.iloc[i, :]['FIPS'])
    #print(to_keep_)
    npis = npis[npis[index]!=1]
#    print(npis_drop.shape)
    cur_npi_dates = np.array(npis[index].values)
#    print(cur_npi_dates)
    ## assumption: stay at home was implemented last
    dates_diff =  abs(cur_npi_dates - np.array(npis.iloc[:,1:].values).transpose()).transpose()
    ## subtract the stay at home starting dates from all other interventions
#    print(dates_diff.shape)

    dates_diff.sort(axis=1)
    diff_int = (dates_diff[:,1:] != dates_diff[:,:-1]).sum(axis=1)+1 #finds unique values
    all_selected = npis[diff_int>=6]
    return list(all_selected['FIPS'])
#    to_keep = npis[dates_diff[:,1] > 2]
#    return list(to_keep['FIPS'])

    
if __name__ == '__main__':
#    filename = 'data/us_data/clustering.csv'
#    cluster_num = 5
#    fips = get_cluster(filename, cluster_num)
#    print(fips)

    
    data_dir = 'data'
    interventions = get_npis(data_dir)
    counties = get_counties_isolated_NPIs(interventions, 'stay at home')
    print(len(counties))
    print(counties)
