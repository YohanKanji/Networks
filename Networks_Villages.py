#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 12 11:46:20 2020

@author: yohankanji
"""

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import numpy as np
from collections import Counter

df  = pd.read_csv("https://courses.edx.org/asset-v1:HarvardX+PH526x+2T2019+type@asset+block@individual_characteristics.csv", low_memory=False, index_col=0)
df1 = df[(df['village'] == 1)]
df2 = df[(df['village'] == 2)]
df1.head()
df1.resp_gend.head()

sex1      = dict(zip(df1.pid, df1.resp_gend))
caste1    = dict(zip(df1.pid, df1.caste))
religion1 = dict(zip(df1.pid, df1.religion))

sex2      = dict(zip(df2.pid, df2.resp_gend))
caste2    = dict(zip(df2.pid, df2.caste))
religion2 = dict(zip(df2.pid, df2.religion))

def chance_homophily(chars):
    chars_count = Counter(chars.values())
    chars_counts = np.array(list(chars_count.values()))
    chars_props  = chars_counts / sum(chars_counts)
    return sum(chars_props**2)

favorite_colors = {
    "ankit":  "red",
    "xiaoyu": "blue",
    "mary":   "blue"
}

color_homophily = chance_homophily(favorite_colors)
print('')

print('Village 1 - Sex', chance_homophily(sex1))
print('Village 1 - Caste',chance_homophily(caste1))
print('Village 1 - Religion', chance_homophily(religion1))

print('Village 2 - Sex', chance_homophily(sex2))
print('Village 2 - Caste',chance_homophily(caste2))
print('Village 2 - Religion', chance_homophily(religion2))

def homophily(G, chars, IDs):
    """
    Given a network G, a dict of characteristics chars for node IDs,
    and dict of node IDs for each node in the network,
    find the homophily of the network.
    """
    num_same_ties, num_ties = 0, 0
    for n1 in G.nodes():
        for n2 in G.nodes():
            if n1 > n2:   # do not double-count edges!
                if IDs[n1] in chars and IDs[n2] in chars:
                    if G.has_edge(n1, n2):
                        num_ties += 1
                        if chars[IDs[n1]] == chars[IDs[n2]]:
                            num_same_ties += 1
    return (num_same_ties / num_ties)

data_filepath1 = "https://courses.edx.org/asset-v1:HarvardX+PH526x+2T2019+type@asset+block@key_vilno_1.csv"
data_filepath2 = "https://courses.edx.org/asset-v1:HarvardX+PH526x+2T2019+type@asset+block@key_vilno_2.csv"

pid1 = pd.read_csv(data_filepath1)
pid2 = pd.read_csv(data_filepath2)

print('')
person = pid1.loc[100]
print('')

G1 = nx.Graph()
G2 = nx.Graph()

A1 = np.array(pd.read_csv("https://courses.edx.org/asset-v1:HarvardX+PH526x+2T2019+type@asset+block@adj_allVillageRelationships_vilno1.csv", index_col=0))
A2 = np.array(pd.read_csv("https://courses.edx.org/asset-v1:HarvardX+PH526x+2T2019+type@asset+block@adj_allVillageRelationships_vilno2.csv", index_col=0))
G1 = nx.to_networkx_graph(A1)
G2 = nx.to_networkx_graph(A2)

pid1 = pd.read_csv(data_filepath1, dtype=int)['0'].to_dict()
pid2 = pd.read_csv(data_filepath2, dtype=int)['0'].to_dict()

print('Village 1 - Sex', homophily(G1, sex1, pid1))
print('Village 1 - Caste', homophily(G1, caste1, pid1))
print('Village 1 - Religion', homophily(G1, religion1, pid1))

print('Village 2 - Sex', homophily(G2, sex2, pid2))
print('Village 2 - Caste', homophily(G2, caste2, pid2))
print('Village 2 - Religion', homophily(G2, religion2, pid2))

print('')
print('')

# print('Village 1 - Sex', chance_homophily(sex1))
# print('Village 1 - Caste',chance_homophily(caste1))
# print('Village 1 - Religion', chance_homophily(religion1))

# print('Village 2 - Sex', chance_homophily(sex2))
# print('Village 2 - Caste',chance_homophily(caste2))
# print('Village 2 - Religion', chance_homophily(religion2))

print('Village 1 Diff - Sex', homophily(G1, sex1, pid1) - chance_homophily(sex1))
print('Village 1 Diff - Caste', homophily(G1, caste1, pid1) - chance_homophily(caste1))
print('Village 1 Diff - Religion', homophily(G1, religion1, pid1) - chance_homophily(religion1))

print('Village 2 Diff - Sex', homophily(G2, sex2, pid2) - chance_homophily(sex2))
print('Village 2 Diff - Caste', homophily(G2, caste2, pid2) - chance_homophily(caste2))
print('Village 2 Diff - Religion', homophily(G2, religion2, pid2) - chance_homophily(religion2))


#OUTPUT
# Village 1 - Sex 0.5027299861680701
# Village 1 - Caste 0.6741488509791551
# Village 1 - Religion 0.9804896988521925
# Village 2 - Sex 0.5005945303210464
# Village 2 - Caste 0.425368244800893
# Village 2 - Religion 1.0


# Village 1 - Sex 0.5879345603271984
# Village 1 - Caste 0.7944785276073619
# Village 1 - Religion 0.99079754601227
# Village 2 - Sex 0.5622435020519836
# Village 2 - Caste 0.826265389876881
# Village 2 - Religion 1.0


# Village 1 Diff - Sex 0.0852045741591283
# Village 1 Diff - Caste 0.12032967662820682
# Village 1 Diff - Religion 0.010307847160077488
# Village 2 Diff - Sex 0.061648971730937197
# Village 2 Diff - Caste 0.400897145075988
# Village 2 Diff - Religion 0.0
