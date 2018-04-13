# Revision History for kpointTests

## Revision 1.0.1
- Major database restructure.
- Removed the no longer used data and data2_old folders, renamed data2
  to data.
- Removed the old paper directory.
- Removed the HCP comparison notebook.
- Removed output files from enumlib.
- Removed unrelated grid generation folder.

## Revision 1.0.0
- Final datasets are now present.
- Final plots have been created.
- Notebooks have been developed.

## Revision 0.7.2
- Created full convergence data instead of just the truncated ones
  currently available.
- Created new plotting function to make binning more traditional.

## Revision 0.7.1
- Changed how the ratio plots were constructed and updated plots
  accordingly.

## Revision 0.7.0
- Refactored the plotting scripts so that they use subroutines instead
  of repeated code blocks.
- Added an ipython notebook for converting the raw data files into
  convergence data files.
- Added Dr. Hess's data to the repo.

## Revision 0.6.2
- Updated the data files to reflect recent calculations and
  reconstructed the main plot at plots/All_vs_Mueller_corrected.pdf

## Revision 0.6.1
- Implemented a new ipython notebook to investigate if the plots being
  generated were averaging the data properly.
- Removed some old data that is no longer is use (the Co system data).
-Created a new plot.

## Revision 0.6.0
- Added data for additional elemnts to the repo as well as an updated
  plot that uses the Mueller grids that don't have the gamma point.
- Added directory for writeup of findings.

## Revision 0.5.0
- Added plots of the time scaling for generating the complete list of HNFs.

## Revision 0.4.0
- Added a mathematica file to the scripts folder that computes the
  number of cells needed to fill a sphere of a given cutoff radius. It
  then finds the number of HNFs for that number of cells.

## Revision 0.3.0

- Added a new mode that plots the convergence of all runs for each element on a single plot.
- Added figures produced from the new mode.

## Revision 0.2.1

- Fixed a typo on the axis labels.
- Made the individual plots log log.
- Changed default plot range on *_vs_Mueller plots.

## Revision 0.2.0

- Added 3 atom cells back to the models.
- Fixed some errors that had occured in the Froyen tests.
- Added an additional hcp test case to the Fropen tests.

## Revision 0.1.0

- Updated scripts for multiple Froyen grids {i.e. sc, bcc, fcc, hcp}.
- Added new data for multiple Froyen grids.
- Updated all figures.

## Revision 0.0.1

Inital commit to the repo of the data and the scripts.