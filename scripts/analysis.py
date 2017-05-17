"""Contains techniques used for the analysis of the kpoint tests."""

def _isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def _getKey(item):
    return item[1]

def _plot_elements(args):
    """Plots the convergence for each element."""

    from plotter import plot_elements

    plot_elements()

def _get_ratios(args):
    """Gets the ratios of the kpoints used in each method."""

    from manipulate import get_ratios

    get_ratios(args["get_ratios"],bottom=args["ratio_base"])

def _plot_avg(systems,join,bottom="Mueller"):
    """Plots the average ratio of Muller to Froyen or AFLOW
    
    :args systems: which methods will be plotted
    :arg bottom: The system the others are being compared to.
    :args join: put them on the same plot?
    """
    
    from plotter import avg
    from os import path

    cases = []
    for sys in systems:
        if sys != bottom:
            if path.isdir("../data/{0}_vs_{1}".format(sys,bottom)) or path.isfile("../data/Average_{0}_vs_{1}.csv".format(sys,bottom)):
                cases.append(sys)

    if join:
        avg(cases,bottom,joined=True)
    else:
        avg(cases,bottom)

def _plot_all(args):
    """Makes a plot of the Mueller vs Froyen or AFLOW data for each test
    case."""

    from os import walk, system
    from matplotlib import pyplot as plt

    elements = ["Ti","W","Al","Pd","V","K","Cu","Re","Y"]
    methods = ["AFLOW","Froyen_sc","Froyen_bcc","Froyen_fcc","Froyen_hcp1","Froyen_hcp2","Froyen_hcp3","Froyen_hcp4","MUELLER"]

    data_F_sc = {}
    data_F_bcc = {}
    data_F_fcc = {}
    data_F_hcp1 = {}
    data_F_hcp2 = {}
    data_F_hcp3 = {}
    data_F_hcp4 = {}
    data_M = {}
    data_A = {}

    count_F_sc = {"Ti":0,"W":0,"Al":0,"Pd":0,"V":0,"K":0,"Cu":0,"Re":0,"Y":0}
    count_F_bcc = {"Ti":0,"W":0,"Al":0,"Pd":0,"V":0,"K":0,"Cu":0,"Re":0,"Y":0}
    count_F_fcc = {"Ti":0,"W":0,"Al":0,"Pd":0,"V":0,"K":0,"Cu":0,"Re":0,"Y":0}
    count_F_hcp1 = {"Ti":0,"W":0,"Al":0,"Pd":0,"V":0,"K":0,"Cu":0,"Re":0,"Y":0}
    count_F_hcp2 = {"Ti":0,"W":0,"Al":0,"Pd":0,"V":0,"K":0,"Cu":0,"Re":0,"Y":0}
    count_F_hcp3 = {"Ti":0,"W":0,"Al":0,"Pd":0,"V":0,"K":0,"Cu":0,"Re":0,"Y":0}
    count_F_hcp4 = {"Ti":0,"W":0,"Al":0,"Pd":0,"V":0,"K":0,"Cu":0,"Re":0,"Y":0}
    count_A = {"Ti":0,"W":0,"Al":0,"Pd":0,"V":0,"K":0,"Cu":0,"Re":0,"Y":0}
    count_M = {"Ti":0,"W":0,"Al":0,"Pd":0,"V":0,"K":0,"Cu":0,"Re":0,"Y":0}
    
    for element in elements:
        for method in methods:
            if "Froyen" in method:
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
                if method == "Froyen_sc":
                    if "sc" in this_file:
                        count_F_sc[element] += 1
                        data_F_sc[element+'_'+this_file.split('.')[0].split('_')[0]] = this_data
                if method == "Froyen_bcc":
                    if "bcc" in this_file:
                        count_F_bcc[element] += 1
                        data_F_bcc[element+'_'+this_file.split('.')[0].split('_')[0]] = this_data
                if method == "Froyen_fcc":
                    if "fcc" in this_file:
                        count_F_fcc[element] += 1
                        data_F_fcc[element+'_'+this_file.split('.')[0].split('_')[0]] = this_data
                if method == "Froyen_hcp1":
                    if "hcp1" in this_file:
                        count_F_hcp1[element] += 1
                        data_F_hcp1[element+'_'+this_file.split('.')[0].split('_')[0]] = this_data
                if method == "Froyen_hcp2":
                    if "hcp2" in this_file:
                        count_F_hcp2[element] += 1
                        data_F_hcp2[element+'_'+this_file.split('.')[0].split('_')[0]] = this_data
                if method == "Froyen_hcp3":
                    if "hcp3" in this_file:
                        count_F_hcp3[element] += 1
                        data_F_hcp3[element+'_'+this_file.split('.')[0].split('_')[0]] = this_data
                if method == "Froyen_hcp4":
                    if "hcp4" in this_file:
                        count_F_hcp4[element] += 1
                        data_F_hcp4[element+'_'+this_file.split('.')[0].split('_')[0]] = this_data
                if method == "MUELLER":
                    count_M[element] += 1
                    data_M[element+'_'+this_file.split('.')[0].split('_')[0]] = this_data
                if method == "AFLOW":
                    count_A[element] += 1
                    data_A[element+'_'+this_file.split('.')[0].split('_')[0]] = this_data

    # Now that we have the data we can make the plots
    for element in elements:
        if element != "Ti":
            #First we'll make the froyen plots-
            for i in range(1,min(count_M[element],count_F_sc[element],count_F_bcc[element],count_F_bcc[element],count_A[element])+1):
                fig = plt.figure()
                ax = fig.add_subplot(1,1,1)
                ax.plot(*zip(*data_F_sc[element+"_"+str(i)]),label="Froyen sc")
                ax.plot(*zip(*data_F_bcc[element+"_"+str(i)]),label="Froyen bcc")
                ax.plot(*zip(*data_F_fcc[element+"_"+str(i)]),label="Froyen fcc")
                ax.plot(*zip(*data_M[element+"_"+str(i)]),label="Mueller")
                ax.plot(*zip(*sorted(data_A[element+"_"+str(i)])),label="AFLOW")
                plt.xlabel("Number of irreducible kpoints")
                plt.ylabel("Error in converged energy value (eV)")
                plt.suptitle("Error in energy for a {} system of {} atoms.".format(element,str(i)))
                ax.set_yscale("log")
                ax.set_xscale("log")
                ax.legend(loc="upper right")
                plt.savefig("../plots/single_runs/{}_{}.pdf".format(element,str(i)))
                plt.clf()
        else:
            for i in range(1,min(count_M[element],count_F_hcp1[element],count_F_hcp2[element],count_F_hcp3[element],count_A[element])+1):
                fig = plt.figure()
                ax = fig.add_subplot(1,1,1)
                ax.plot(*zip(*data_F_hcp1[element+"_"+str(i)]),label="Froyen hcp1")
                ax.plot(*zip(*data_F_hcp2[element+"_"+str(i)]),label="Froyen hcp2")
                ax.plot(*zip(*data_F_hcp3[element+"_"+str(i)]),label="Froyen hcp3")
                ax.plot(*zip(*data_F_hcp3[element+"_"+str(i)]),label="Froyen hcp4")
                ax.plot(*zip(*data_M[element+"_"+str(i)]),label="Mueller")
                ax.plot(*zip(*sorted(data_A[element+"_"+str(i)])),label="AFLOW")
                plt.xlabel("Number of irreducible kpoints")
                plt.ylabel("Error in converged energy value (eV)")
                plt.suptitle("Error in energy for a {} system of {} atoms.".format(element,str(i)))
                ax.set_yscale("log")
                ax.set_xscale("log")
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
    parser.add_argument("-elements", action="store_true",
                        help=("Plots the convergence for each element for all methods and "
                              "cell sizes."))
    parser.add_argument("-single", action="store_true",
                        help=("Plots each system individually as a function of accuracy."))
    parser.add_argument("-verbose", type=int,
                        help="Specify the verbosity level (1-3) for additional computation info.")
    parser.add_argument("-get_ratios",nargs="+",
                        help=("Get's the averages of the data in the data folder so that they"
                              " can be plotted."))
    parser.add_argument("-ratio_base",type=str,
                        help=("The method to be used for comparisons."))
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

    if vardict["average"] != None and vardict["average"][0].lower() == "all":
        vardict["average"] = ["Mueller","AFLOW","Froyen_sc","Froyen_bcc","Froyen_fcc","Froyen_hcp1","Froyen_hcp2","Froyen_hcp3","Froyen_hcp4"]

    if not vardict["ratio_base"]:
        vardict["ratio_base"] = "Mueller"

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
    if args["elements"]:
        _plot_elements(args)
    
if __name__ == '__main__':
    script_enum(_parser_options())
            
