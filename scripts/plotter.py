"""Plotting scripts for the kpointTests"""

def _isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def avg(cases,bottom,joined=False):
    """Plots the average of the speedup test data for the Froyen and the
    AFLOW methods vs the Mueller method.

    :arg cases: The systems that should appear on the plots.
    :arg bottom: The system the others are being compared to.
    :arg joined: True if the systems are to appear on the same plot.
    """

    from os import walk, path
    import csv
    from matplotlib import pyplot as plt

    all_data = {}

    for case in cases:
        get_data = True
        # First we need to get the data for all the trials done.
        if path.isfile("../data/Average_{0}_vs_{1}.csv".format(case,bottom)):
            get_data = False


        if get_data:
            this_path = "../data/"+case+"_vs_"+bottom
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
            with open("../data/Average_{0}_vs_{1}.csv".format(case,bottom),'wb') as out:
                writer = csv.writer(out,delimiter='\t')
                for data_point in avg:
                    writer.writerow(data_point)

            # append all the data to a list for later use.
            all_data[case] = avg

        else:
            avg = []
            with open("../data/Average_{0}_vs_{1}.csv".format(case,bottom),'r') as out:
                for line in out:
                    avg.append([float(t) for t in line.split()])

            # append all the data to a list for later use.
            all_data[case] = avg

    # if we're joining the plots then we plot them all at once
    # otherwise we need to plot them seperately.
    if joined == True:
        # Now that we have the data we need to plot it
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        for case in cases:
            ax.plot(*zip(*all_data[case]), label= case)
        ax.set_yscale('log')
        ax.set_xlim([-6,-1])
        ax.legend(loc="upper left")
        plt.xlabel("Error in energy value Log(eV)")
        plt.ylabel("Ratio of irreducible K-points (Method/{})".format(bottom))
        plt.suptitle("Average speedup of Methods vs {} K-point methods.".format(bottom))
        plt.savefig("../plots/All_vs_{}.pdf".format(bottom))
        plt.clf()
        
    else:
        for case in cases:
            # Now that we have the data we need to plot it
            fig = plt.figure()
            ax = fig.add_subplot(1,1,1)
            ax.plot(*zip(*all_data[case]))
            ax.set_yscale('log')
            ax.set_xlim([-6,-1])
            plt.xlabel("Error in energy value Log(eV)")
            plt.ylabel("Ratio of irreducible K-points ({}/{})".format(case,bottom))
            plt.suptitle("Average speedup of {} vs {} K-point methods.".format(case,bottom))
            plt.savefig("../plots/Average_{}_vs_{}.pdf".format(case,bottom))
            plt.clf()

def plot_elements():
    """Plots the convergence of the methods listed in cases for each cell
    size in cell_sizes.

    Args:
    cell_sizes (list of str): The atoms to be plotted.

    Returns:
    A plot of the convergence vs the number of k-points.
    """

    from glob import glob
    import matplotlib.pyplot as plt
    elements = ["Al","Ti","W"]
    cases = ["Froyen","AFLOW","Mueller"]

    for element in elements:
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        files = []
        if element == "Ti":
            sizes = range(1,8)
        else:
            sizes = range(1,12)
        label_used = {"Mueller":0,"AFLOW":0,"Froyen_sc":0,"Froyen_bcc":0,"Froyen_fcc":0,
                      "Froyen_hcp1":0,"Froyen_hcp2":0,"Froyen_hcp3":0,"Froyen_hcp4":0}
            
        for method in cases:
            if "Froyen" in method:
                tail = "_Froyen"
            if method == "AFLOW":
                tail = "_AFLOW"
                color= "b"
                label = "AFLOW"
            if method == "Mueller":
                tail = "_Mueller"
                color="g"
                label="Mueller"

            for size in sizes:
                this_path ="/Users/wileymorgan/Documents/research/kpointTests/data/{}{}/{}_*".format(element,tail,size)

                files = glob(this_path)
                
                for i in range(len(files)):
                    this_file = files[i]
                    if "Froyen" in this_file:
                        if "sc" in this_file:
                            color = "m"
                            label = "Froyen_sc"
                        elif "bcc" in this_file:
                            color = "c"
                            label = "Froyen_bcc"
                        elif "fcc" in this_file:
                            color="r"
                            label = "Froyen_fcc"
                        elif "hcp1" in this_file:
                            color = "m"
                            label = "Froyen_hcp1"
                        elif "hcp2" in this_file:
                            color = "c"
                            label = "Froyen_hcp2"
                        elif "hcp3" in this_file:
                            color="r"                            
                            label = "Froyen_hcp3"
                        elif "hcp4" in this_file:
                            color = "k"
                            label = "Froyen_hcp4"
                    if '.csv' not in this_file:
                        continue
                    if '~' in this_file:
                        system('rm '+this_file)
                        continue
                    if 'raw' in this_file:
                        continue

                    this_x = []
                    this_y = []
                    this_data = []
                    with open(this_file,'r') as f:
                        for line in f:
                            if float(line.split()[1]) > 1E-9:
                                this_data.append([float(t) for t in line.split()])
                    this_data.sort()
                    for t in this_data:
                        this_x.append(t[0])
                        this_y.append(t[1])
                            # this_y = [float(t) for t in line.split()[0]]
                    if label_used[label] == 0:
                        ax.plot(this_x,this_y,c=color,label=label)
                        label_used[label] += 1
                    else:
                        ax.plot(this_x,this_y,c=color)                        
                    ax.set_yscale('log')
                    ax.set_xscale('log')
                    

        ax.legend(loc="upper right")
        plt.ylabel("Error in energy value Log(eV)")
        plt.xlabel("Number if irreducible kpoints")
        plt.suptitle("{} Convergence with Various k-point Selection Methods.".format(element))
        plt.savefig("/Users/wileymorgan/Documents/research/kpointTests/plots/{}_Convergenc.pdf".format(element))
        plt.show()
            
