"""Plotting techniques used for the analysis of the kpoint tests."""
import matplotlib.pyplot as plt
from pylab import *

def _isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def _plot_avg():
    """Plots the average of the speedup test data for the Froyen and the
    AFLOW methods vs the Mueller method."""

    from os import walk, path
    import csv
    
    cases = ["AFLOW_vs_Mueller","Froyen_vs_Mueller"]

    for case in cases:
        get_data = True
        # First we need to get the data for all the trials done.
        if path.isfile("../data/AVerage_{}.csv".format(case)):
            get_data = False

        if get_data:
            this_path = "../data/"+case
        
            files = next(walk(this_path))[2]

            data = {}
            for this_file in files:
                this_data = []
                if '~' in this_file:
                    os.system('rm '+this_path+'/'+this_file+'~')
                    continue
                with open(this_path+'/'+this_file,'r') as f:
                    for line in f:
                        this_data.append([float(i) for i in line.split()])

                data[this_file.split('.')[0]] = this_data

            # Now we need to average the data.
            avg = []
            import numpy as np
            from tqdm import tqdm
            pbar = tqdm(np.arange(-6.0,2.001,0.001).tolist())
            for i in pbar:
                new_point = 0
                count = 0
                for key in data:
                    for point in data[key]:
                        if _isclose(i,point[0],rel_tol=0.0001,abs_tol=0.0):
                            new_point += point[1]
                            count += 1
                        
                if count > 0:
                    avg.append([i,new_point/count])

            # Save the averaged data
            with open("../data/Average_{}.csv".format(case),'wb') as out:
                writer = csv.writer(out,delimiter='\t')
                for data_point in avg:
                    writer.writerow(data_point)

        else:
            avg = []
            with open("../data/Average_{}.csv".format(case),'r') as out:
                for line in out:
                    avg.append([float(t) for t in line.split()])
                
        # Now that we have the data we need to plot it
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        ax.plot(*zip(*avg))
        ax.set_yscale('log')
        plt.xlabel("Error in energy value Log(eV)")
        plt.ylabel("Ration of irreducible K-points ({}/Mueller)".format(case.split('_')[0]))
        plt.suptitle("Average speedup of {} vs Mueller K-point methods.".format(case.split('_')[0]))
        ax.set_yscale("log")
        plt.savefig("../plots/Average_{}.pdf".format(case))
        plt.clf()

def _plot_all():
    """Makes a plot of the Mueller vs Froyen or AFLOW data for each test
    case."""

    from os import walk, system

    elements = ["Co","W","V"]
    methads = ["AFLOW","FROYEN","MUELLER"]

    data_M = {}
    data_F = {}
    data_A = {}

    count_F = {"Co":0,"W":0,"V":0}
    count_A = {"Co":0,"W":0,"V":0}
    count_M = {"Co":0,"W":0,"V":0}
    
    for element in elements:
        for method in methads:
            if method == "FROYEN":
                tail = "_Froyen"
            if method == "AFLOW":
                tail = "_AFLOW"
            if method == "MUELLER":
                tail = "_Mueller"

            this_path ="../data/"+element+tail
            files = next(walk(this_path))[2]

            for i in range(len(files)):
                this_file = files[i]
                if '.csv' not in this_file:
                    continue
                if '~' in this_file:
                    system('rm '+this_path+'/'+this_file)
                    continue
                if element in this_file:
                    continue
                this_data = []
                with open(this_path+'/'+this_file,'r') as f:
                    for line in f:
                        this_data.append([float(t) for t in line.split()])

                if method == "FROYEN":
                    count_F[element] += 1
                    data_F[element+'_'+this_file.split('.')[0].split('_')[1]] = this_data
                if method == "MUELLER":
                    count_M[element] += 1
                    data_M[element+'_'+this_file.split('.')[0].split('_')[1]] = this_data
                if method == "AFLOW":
                    count_A[element] += 1
                    data_A[element+'_'+this_file.split('.')[0].split('_')[1]] = this_data


    # Now that we have the data we can make the plots
    for element in elements:
        #First we'll make the froyen plots-
        for i in range(1,min(count_M[element],count_F[element],count_A[element])+1):
            fig = plt.figure()
            ax = fig.add_subplot(1,1,1)
            ax.plot(*zip(*data_F[element+"_"+str(i)]),label="Froyen")
            ax.plot(*zip(*data_M[element+"_"+str(i)]),label="Mueller")
            ax.plot(*zip(*sorted(data_A[element+"_"+str(i)])),label="AFLOW")
            plt.xlabel("Number of irreducible kpoints")
            plt.ylabel("Error in converged energy value (eV)")
            plt.suptitle("Error in energy for a {} system of {} atoms.".format(element,str(i)))
            ax.set_yscale("log")
            ax.legend(loc="upper right")
            plt.savefig("../plots/single_runs/{}_{}.pdf".format(element,str(i)))
            plt.clf()

def _examples():
    """Print some examples on how to use this python version of the code."""
    egs = [("Plot the average of the speedup runs.",
            "The code below plots the average of the speedup (# of irreducible "
            "K-pointsused/# of Mueller irreducible K-points) for the "
            "different methods over all the test cases",
            "python analysys.py -average"),
           ("Plot the data from all the runs.",
            "This code plots the difference in the energy compared "
            "to the converged value for each system and cell size. "
            "Each plot has each K-point method displayed on it."
            , "python analysis.py -single")]

    print("Plotting functions for the K-point tests\n")
    for eg in egs:
        title, desc, code = eg
        print("--" + title + '--\n')
        print(desc + '\n')
        print('  ' + code + '\n')

def _parser_options(phelp=False):
    """Parses the options and arguments from the command line."""
    import argparse
    parser = argparse.ArgumentParser(description="Partial Superstructure Enumeration Code")
    parser.add_argument("-debug", action="store_true",
                        help="Print verbose calculation information for debugging.")
    parser.add_argument("-examples", action="store_true",
                        help="Print some examples for how to use the enumeration code.")
    parser.add_argument("-average", action="store_true",
                        help=("Plot the average of all the speedup runs."))
    parser.add_argument("-single", action="store_true",
                        help=("Plots each system individually as a function of accuracy."))
    parser.add_argument("-verbose", type=int,
                        help="Specify the verbosity level (1-3) for additional computation info.")
    vardict = vars(parser.parse_args())
    if phelp or vardict["examples"]:
        _examples()
        exit(0)

    if vardict["verbose"]:
        from enum.msg import set_verbosity
        set_verbosity(vardict["verbose"])

    return vardict

def script_enum(args):
    """Generates the 'polya.out' or 'enum.out' files depending on the script arguments.
    """
            
    if args["average"]:
        _plot_avg()
    if args["single"]:
        _plot_all(args)
    
if __name__ == '__main__':
    script_enum(_parser_options())
            
