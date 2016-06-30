"""Methods for manipulating the data in kpointTests."""

def getKey(item):
    """Gets the key for sorting"""
    
    return item[1]

def get_ratios(elements):
    """Gets the ratios of the Mueller to AFLOW and Froyen tests across the
    accuracy ranges.
    
    :args elements: The list of elements to find the ratios of
    """
    from math import log
    import csv
    cases = ["AFLOW","Froyen","Mueller"]
    # Collect the data in dictionaries for latter use.
    Mueller = {}
    AFLOW = {}
    Froyen = {}
    for case in cases:
        for element in elements:
            el_data = []
            for size in range(1,12):
                with open("../data/{}_{}/{}_atom_convergence.csv".format(element,case,size),"r") as df:
                    data = df.read().split("\n")
                    sdata = []
                    for line in data:
                        if line != "":
                            line = line.split()
                            point = [int(line[0]),float(line[1])]
                            sdata.append(point)
                    if sdata != []:
                        el_data.append(sdata)
                    else:
                        el_data.append([[0.0,0.0]])
            if case == "Mueller":
                Mueller[element] = el_data
            if case == "AFLOW":
                AFLOW[element] = el_data
            if case == "Froyen":
                Froyen[element] = el_data

    # Now that we have the data we need to ananlyse it.
    for element in elements:
        for size in range(11):
            resultsM = []
            resultsF = []
            resultsA = []
            resultsFM = []
            resultsAM = []

            Fi = sorted(Froyen[element][size],key=getKey)
            Mi = sorted(Mueller[element][size],key=getKey)
            Ai = sorted(AFLOW[element][size],key=getKey)

            # sort the errors and the kpoints so that they are in the
            # correct order (we want smaller errors to appear sooner in
            # the list and the errors to be sorted by fewest number of
            # kpoints).
            for dE in [x/1000.0 for x in range(-6000,2001)]:
                savede = log(1E-20,10)
                savedk = 0
                for j in Mi:
                    if j[1] != 0.0:
                        if log(j[1],10) < dE:
                            if log(j[1],10) > savede:
                                savedk = j[0]
                                savede = log(j[1],10)
                resultsM.append([dE,savedk])

                savede = log(1E-20,10)
                savedk = 0
                for j in Fi:
                    if j[1] != 0.0:
                        if log(j[1],10) < dE:
                            if log(j[1],10) > savede:
                                savedk = j[0]
                                savede = log(j[1],10)
                resultsF.append([dE,savedk])

                savede = log(1E-20,10)
                savedk = 0
                for j in Ai:
                    if j[1] != 0.0:
                        if log(j[1],10) < dE:
                            if log(j[1],10) > savede:
                                savedk = j[0]
                                savede = log(j[1],10)
                    
                resultsA.append([dE,savedk])

            # Now that the lists are sorted we can get the ratio of kpoints
            for j in range(len(resultsM)):
                if resultsF[j][1] != 0 and resultsM[j][1] != 0:
                    resultsFM.append([resultsM[j][0],resultsF[j][1]/float(resultsM[j][1])])

                if resultsA[j][1] != 0 and resultsM[j][1] != 0:
                    resultsAM.append([resultsM[j][0],resultsA[j][1]/float(resultsM[j][1])])

            # Now we save the output data
            outF = open("../data/Froyen_vs_Mueller/F_{}_{}.csv".format(element,size),"w+")
            outA = open("../data/AFLOW_vs_Mueller/A_{}_{}.csv".format(element,size),"w+")
            writerF = csv.writer(outF,delimiter='\t')
            writerA = csv.writer(outA,delimiter='\t')
            for d in resultsFM:
                writerF.writerow(d)
            outF.close()
                
            for d in resultsAM:
                writerA.writerow(d)
            outA.close()

