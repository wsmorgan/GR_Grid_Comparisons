"""Contains techniques used for the analysis of the kpoint tests."""

def _isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def _getKey(item):
    return item[1]

def _get_ratios(args):
    """Gets the ratios of the kpoints used in each method."""

    from manipulate import get_ratios

    get_ratios(args["get_ratios"])

def _plot_avg(systems,join):
    """Plots the average ratio of Muller to Froyen or AFLOW
    
    :args systems: which methods will be plotted
    :args join: put them on the same plot?
    """
    
    from plotter import avg
    from os import path

    cases = []
    for sys in systems:
        if sys.lower() == "froyen":
            case = "Froyen"
        elif sys.lower() == "aflow":
            case = "AFLOW"
        else:
            case = sys
        if path.isdir("../data/{}_vs_Mueller".format(case)) or path.isfile("../data/Average_{}_vs_Mueller.csv".format(case)):
            cases.append(case)

    if join:
        avg(cases,joined=True)
    else:
        avg(cases)

def _plot_all(args):
    """Makes a plot of the Mueller vs Froyen or AFLOW data for each test
    case."""

    from os import walk, system
    from matplotlib import pyplot as plt

    elements = ["Ti","W","Al"]
    methads = ["AFLOW","FROYEN","MUELLER"]

    data_M = {}
    data_F = {}
    data_A = {}

    count_F = {"Ti":0,"W":0,"Al":0}
    count_A = {"Ti":0,"W":0,"Al":0}
    count_M = {"Ti":0,"W":0,"Al":0}
    
    for element in elements:
        for method in methads:
            if method == "FROYEN":
                tail = "_Froyen"
            if method == "AFLOW":
                tail = "_AFLOW"
            if method == "MUELLER":
                tail = "_Mueller"

            this_path ="../data/{}{}".format(element,tail)
            files = next(walk(this_path))[2]

            for i in range(len(files)):
                this_file = files[i]
                if '.csv' not in this_file:
                    continue
                if '~' in this_file:
                    system('rm '+this_path+'/'+this_file)
                    continue
                if 'raw' in this_file:
                    continue
                this_data = []
                with open(this_path+'/'+this_file,'r') as f:
                    for line in f:
                        this_data.append([float(t) for t in line.split()])
                if method == "FROYEN":
                    count_F[element] += 1
                    print(element+'_'+this_file.split('.')[0].split('_')[0])
                    data_F[element+'_'+this_file.split('.')[0].split('_')[0]] = this_data
                if method == "MUELLER":
                    count_M[element] += 1
                    data_M[element+'_'+this_file.split('.')[0].split('_')[0]] = this_data
                if method == "AFLOW":
                    count_A[element] += 1
                    data_A[element+'_'+this_file.split('.')[0].split('_')[0]] = this_data


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
    parser.add_argument("-average", nargs ="+",
                        help=("Plot the average of all the speedup runs."))
    parser.add_argument("-joined", action="store_true",
                        help=("If present all data will appear on the same plot."))
    parser.add_argument("-single", action="store_true",
                        help=("Plots each system individually as a function of accuracy."))
    parser.add_argument("-verbose", type=int,
                        help="Specify the verbosity level (1-3) for additional computation info.")
    parser.add_argument("-get_ratios",nargs="+",
                        help=("Get's the averages of the data in the data folder so that they"
                              " can be plotted."))
    vardict = vars(parser.parse_args())
    if phelp or vardict["examples"]:
        _examples()
        exit(0)

    if vardict["verbose"]:
        from enum.msg import set_verbosity
        set_verbosity(vardict["verbose"])
    if vardict["joined"]:
        vardict["joined"] = True
    else:
        vardict["joined"] = False

    return vardict

def script_enum(args):
    """Generates the desired plots of the data.
    """
            
    if args["average"]:
        _plot_avg(args["average"],args["joined"])
    if args["single"]:
        _plot_all(args)
    if args["get_ratios"]:
        _get_ratios(args)
    
if __name__ == '__main__':
    script_enum(_parser_options())
            
