import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime
import time
import seaborn as sns

def plot_freeway_heatmap(metrics, _title, myfigy, threshold_alldays):
    index_fields = ['timeOfDay', 'Abs_PM']
    metric_names = set([a[0] for a in metrics.columns if a[0] not in index_fields])
    
    vmaxmin= {}
    for a in threshold_alldays.iteritems():
        name = "".join(a[0]).replace(" ", "")
        vmaxmin[name] = [
                        threshold_alldays[a[0]][0], 
                        threshold_alldays[a[0]][1]
                        ]
        
        #vmaxmin[name] =  [min(threshold_alldays[a[0]][0] + #3*threshold_alldays[a[0]][1], 900),
        #                  min(x for x in [threshold_alldays[a[0]][0] - 2*threshold_alldays[a[0]][1], 
        #                               threshold_alldays[a[0]][0] - threshold_alldays[a[0]][1], 
        #                               threshold_alldays[a[0]][0]*.25] 
        #                           if x >= 0)
        #                 ]
    
    number_stations = len(metrics['Abs_PM'].unique())
    
    # Set up the matplotlib figure
    f, axes = plt.subplots(3, 3, figsize=(15, myfigy), sharey=True)
    f.suptitle(_title)
    sns.despine(left=True)
    sns.set(context="paper", font="monospace")
    
    cmap = sns.diverging_palette(h_neg=0, h_pos=260, s=99, l=10,as_cmap=True, center='light')
 
    i=0
    j=0
    for a in sorted(metric_names):
        base_metric = a.split("+")[0]
        base_metric = base_metric.split("-")[0][:-5]
        sns.heatmap(metrics.pivot("Abs_PM", "timeOfDay", a), 
                    vmin=vmaxmin[base_metric][1], 
                    vmax=vmaxmin[base_metric][0],
                    xticklabels=12, 
                    cmap=cmap,
                    ax=axes[i, j],
                    cbar=True,
                    cbar_kws = {'orientation': 'horizontal'})
        axes[i, j].set_title(a)
        
        i += 1
        if i > 2:
            i = 0
            j += 1
                   
    f.savefig('../images/'+_title+'.pdf', bbox_inches='tight')
    return threshold_alldays