# kpointTests
Data that shows how different K-point selection methods impact the convergence of VASP calculations.

# Plots Folder
The plots folder contains plots of the data. The main directory contains global plots. The single_runs folder contains plots of the individual runs.

The most significant of these plots are the average speedup (i.e. the ratio of the number of irreducible K-points per method) of the Froyen and the AFLOW K-point methods vs the Mueller method. Thes plots are shown below:
![AFLOW](plots/Average_AFLOW_vs_Mueller.pdf "Average speedup of Mueller method vs AFLOW")
![Froyen](plots/Average_Froyen_vs_Mueller.pdf "Average speedup of Mueller method vs Froyen")


# Scripts Folder
The scripts folder contains the scripts used to generate the data. To generate the plots either run analysis.py in the scripts folder. For the averaged plots use:
```
python analysis.py -average
```
For the individual plots use:
```
python analysis.py -single
```

# Data Folder
The data folder contains the data used to generate the plots.
