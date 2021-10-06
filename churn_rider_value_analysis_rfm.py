# -*- coding: utf-8 -*-
"""churn rider value analysis_RFM.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qnzP0Bcm4QmcqJd9ov2gdiM4KVXM1rC8
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt

new_df2 = pd.read_csv('new_df2.csv')
new_df2 = new_df2[new_df2['status'] == 1]
new_df2 = new_df2[['F_quantile','M_quantile']]

F_avg = new_df2['F_quantile'].mean()
M_avg = new_df2['M_quantile'].mean()

def segment(row):
  if row['F_quantile'] < F_avg and row['M_quantile'] < M_avg:
    cat = 'F1M1'
  elif row['F_quantile'] < F_avg and row['M_quantile'] > M_avg:
    cat = 'F1M2'
  elif row['F_quantile'] > F_avg and row['M_quantile'] < M_avg:
    cat = 'F2M1'
  else:
    cat = 'F2M2'
  return cat

new_df2['Churn_Segment'] = new_df2.apply(segment, axis = 1)

new_df2.info()
new_df2.head()

segment = pd.DataFrame(new_df2.Churn_Segment.value_counts().reset_index().values, columns=['Churn_Segment', 'Quantity'])
segment = segment.sort_index(axis = 0, ascending=True)
segment['Rate(%)'] = 100*segment['Quantity']/segment['Quantity'].sum()
print(segment)