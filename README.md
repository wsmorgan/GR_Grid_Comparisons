# kpointTests

The data and scripts used to create the plots and discussion for the
paper Efficiency of Generalized Regular k-point Grids. This repository
is organized as follows:

# Scripts folder

This folder contains a single ipython notebook and a single R code
that can be used to reproduce the figures in the paper. To use the
scripts just open the ipython notebook and follow the prompts.

# Data folder

This folder contains the data taken from the VASP runs. Some of this
data was used to generate the plots while some of it wasn't. The data
is organized as follows:

## The Al_by_grid and Si_by_grid folders

These two folder were store the data used to generate figures 6 and
7. Each folder contains a three csv files `bcc_conv.csv`,
`fcc_conv.csv`, `sc_conv.csv` which contain the convergence rates for
the different k-point grids use.

## The R_workspace folder

This folder contains files needed for the R script to perform a loess
fit and the resulting output files.

## The GR, SC, and MP folders

These folders contain data from the VASP runs performed using each
method. All three folders contain sub folders `*_conv` for each
element studied. Within each of these subfolders the MP and GR contain
csv files that contain the convergence data in various formats. The
formats are:

`*_atom_IBZKPTS.csv` Contains a two column table in which the first
column is the number of irreducible k-points ande second is the final
energy from the VASP run.

`*_atom_IBZKPTS_dese_conv.csv` Contains a two column table in which
the first column is the irreduciblk k-point density and the second is
the error in the energy from the VASP calculation.

`*_atom_TKPTS.csv` Contains a two column table in which the first
column is the total number of k-points used and the second is the
final energy from the VASP run.

`*_atom_kpd_conv.csv` Contains a two column table in which the first
column is the total number of k-points used and the second is the
error in the energy from the VASP calculation.

`*_atom_each_conv.csv` Contains a datatable of the davidson cycles for
each calculation performed (this is best viewed in a web browser or
pandas dataframe of a jupyter notebook).

The SC folder contains similar files except with an addition
identifier in the name that identifiers the grid type, i.e., bcc,
fcc,... for example:

`SC/Al_conv/10_bcc_atom_IBZKPTS.csv`.