#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

This script visalises the results of the matching algorithm generated by the previous script.

"""

__author__ = "Manuel Linsenmeier"
__email__ = "m.linsenmeier@lse.ac.uk"
__version__ = "0.9"

import sys
import os
import copy
from copy import deepcopy

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns

## ==============================================
## visualise results
## ==============================================

sectornames = {
	'electricity_and_heat_production': 'energy',
	'transport': 'transport',
	'buildings': 'buildings',
	'industry': 'industry'
}

colors = ['#1C363E',
			'#3A6867',
			'#8AAA8A',
			'#BDC78F',
			'#A79B73']

def get_averages(sector):

	bt_results1 = pd.read_csv('./results/matching_random_ATE_{0:s}.csv'.format(sector))
	bt_results2 = pd.read_csv('./results/matching_random_ATE-placebo_{0:s}.csv'.format(sector))

	average_treated = bt_results1['average_treated'].mean()
	average_control = bt_results1['average_control'].mean()

	return(average_treated, average_control)

def get_ate_ci(sector, alpha):

	bt_results1 = pd.read_csv('./results/matching_random_ATE_{0:s}.csv'.format(sector))
	bt_results2 = pd.read_csv('./results/matching_random_ATE-placebo_{0:s}.csv'.format(sector))

	average_treated = bt_results1['average_treated'].mean()
	average_control = bt_results1['average_control'].mean()

	ate = bt_results1['ATE'].mean()
	ci_lower = bt_results2['ATE'].quantile(alpha/2.)
	ci_upper = bt_results2['ATE'].quantile(1. - alpha/2.)

	return(ate, ci_lower, ci_upper)

# get p-value
#ate + bt_results2['ATE'].quantile(0.064)

fig, ax = plt.subplots(figsize=(4,3))
average_treated, average_control = get_averages('priced')
ax.bar(1., average_treated, width=0.8, color='k')
ax.bar(2., average_control, width=0.8, color='k')

ate, ci_lower90, ci_upper90 = get_ate_ci('priced', 0.1)
ate, ci_lower95, ci_upper95 = get_ate_ci('priced', 0.05)
print(ate)
ax.plot(4., ate, 'o', color='k', label='Difference', markersize=8.)
ax.bar(4., ci_lower95, bottom=ate, width=0.2, color='#D8D8D8')
ax.bar(4., ci_upper95, bottom=ate, width=0.2, color='#D8D8D8')
ax.bar(4., ci_lower90, bottom=ate, width=0.2, color='#808080')
ax.bar(4., ci_upper90, bottom=ate, width=0.2, color='#808080')

for i, sector in enumerate(['electricity_and_heat_production', 'transport', 'buildings', 'industry']):
	ate, ci_lower90, ci_upper90 = get_ate_ci(sector, 0.1)
	ate, ci_lower95, ci_upper95 = get_ate_ci(sector, 0.05)
	print(sector, ate)
	#ax.plot(5. + i, ate, 'o', color='k', label='Difference ({0:s})'.format(sectornames[sector]), markersize=8.)
	ax.plot(5. + i, ate, 'o', color='k', markersize=8.)
	ax.bar(5. + i, ci_lower95, bottom=ate, width=0.2, color='#D8D8D8')
	ax.bar(5. + i, ci_upper95, bottom=ate, width=0.2, color='#D8D8D8')
	ax.bar(5. + i, ci_lower90, bottom=ate, width=0.2, color='#808080')
	ax.bar(5. + i, ci_upper90, bottom=ate, width=0.2, color='#808080')

ax.plot([0., 5. + 5.], [0., 0.], 'k-')
ax.plot([3.2, 3.2], [-0.5, 4.], 'k:')

ax.set_xticks([1., 2., 4., 5, 6, 7, 8])
ax.set_xticklabels([])
ax.set_ylabel('Length of policy sequence')
ax.set_xlim(0.1, 5.2 + 4.)
ax.set_ylim(-2.5, 7.)
ax.annotate(s="Countries "+ r"$\bf{with}$" + "\ncarbon price", xy=(0.5, 6.7), xycoords='data', ha='left', va='top', size='x-small')
ax.annotate(s="Countries "+ r"$\bf{without}$" + "\ncarbon price", xy=(1.5, 5.5), xycoords='data', ha='left', va='top', size='x-small')
import matplotlib.patches as mpatches
patch1 = mpatches.Patch(color='#808080', label='90% CI')
patch2 = mpatches.Patch(color='#D8D8D8', label='95% CI')
handles, labels = ax.get_legend_handles_labels()
handles.append(patch1)
handles.append(patch2)
ax.legend(handles=handles, loc='upper right', ncol=1, fontsize='x-small')
sns.despine(ax=ax, offset=1., right=True, left=False, top=True)
fig.savefig('./figures/matching_result.pdf', bbox_inches='tight', dpi=200)