"""Methods for manipulating the data in kpointTests."""

def getKey(item):
    """Gets the key for sorting"""
    
    return item[1]

def get_ratios(elements,bottom="Mueller",combine_Froyen=False):
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
    Froyen_sc = {}
    Froyen_bcc = {}
    Froyen_fcc = {}
    Froyen_hcp1 = {}
    Froyen_hcp2 = {}
    Froyen_hcp3 = {}
    Froyen_hcp4 = {}

    tolerance = 0.0
    
    for element in elements:
        if element in ["Ti","Re","Y"]:
            sub_cases = ["hcp1","hcp2","hcp3","hcp4"]
            sizes = range(1,8)
            if element == "Ti":
                tolerance = 0.001028
            if element == "Re":
                tolerance = 0.018982
            if element == "Y":
                tolerance = 0.002030
        else:
            sub_cases = ["sc","bcc","fcc"]
            sizes = range(1,12)
            tolerance = 0.0

        for case in cases:    
            el_data = []
            if case != "Froyen":
                for size in sizes:
                    with open("../data/{}_{}/{}_atom_convergence.csv".format(element,case,size),"r") as df:
                        data = df.read().split("\n")
                        sdata = []
                        for line in data:
                            if line != "":
                                line = line.split()
                                if float(line[1]) > tolerance:
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
            else:
                for sub in sub_cases:
                    el_data = []
                    for size in sizes:
                        with open("../data/{0}_{1}/{2}_{3}_atom_convergence.csv".format(element,case,size,sub),"r") as df:
                            data = df.read().split("\n")
                            sdata = []
                            for line in data:
                                if line != "":
                                    line = line.split()
                                    if float(line[1]) > tolerance:
                                        point = [int(line[0]),float(line[1])]
                                        sdata.append(point)
                            if sdata != []:
                                el_data.append(sdata)
                            else:
                                el_data.append([[0.0,0.0]])
                    if sub == "sc":
                        Froyen_sc[element] = el_data
                    if sub == "bcc":
                        Froyen_bcc[element] = el_data
                    if sub == "fcc":
                        Froyen_fcc[element] = el_data
                    if sub == "hcp1":
                        Froyen_hcp1[element] = el_data
                    if sub == "hcp2":
                        Froyen_hcp2[element] = el_data
                    if sub == "hcp3":
                        Froyen_hcp3[element] = el_data
                    if sub == "hcp4":
                        Froyen_hcp4[element] = el_data

    # Now that we have the data we need to ananlyse it.
    for element in elements:
        cases = {}
        cases["Mueller"] = Mueller
        cases["AFLOW"] = AFLOW
        if element in ["Ti","Re", "Y"]:
            cases["Froyen_hcp1"] = Froyen_hcp1
            cases["Froyen_hcp2"] = Froyen_hcp2
            cases["Froyen_hcp3"] = Froyen_hcp3
            cases["Froyen_hcp4"] = Froyen_hcp4
            sizes = range(1,8)
        else:
            cases["Froyen_sc"] = Froyen_sc
            cases["Froyen_bcc"] = Froyen_bcc
            cases["Froyen_fcc"] = Froyen_fcc
            sizes = range(1,12)

        if bottom in cases:
            for key in cases:
                if key != bottom:
                    _get_ratios_of_two(cases[key],cases[bottom],element,[key,bottom])

def _get_ratios_of_two(top,bottom,element,names):
    """Gets the ratio of the top case and the bottom case for the
    specified element.

    :arg top: The array that will form the numerator.
    :arg bottom: The array that will form the denominator.
    :arg element: The element that the data is for.
    :arg names: A list of the method names."""

    from math import log
    import csv
    from os import path, mkdir
            
    if element in ["Ti","Re","Y"]:
        sizes = range(0,7)
    else:
        sizes = range(0,11)

    for size in sizes:
        resultsT = []
        resultsB = []

        resultsTB = []
        Topi = sorted(top[element][size],key=getKey)
        Bottomi = sorted(bottom[element][size],key=getKey)

        # sort the errors and the kpoints so that they are in the
        # correct order (we want smaller errors to appear sooner in
        # the list and the errors to be sorted by fewest number of
        # kpoints).
        for dE in [x/1000.0 for x in range(-6000,2001)]:
            savede = log(1E-20,10)
            savedk = 0
            for j in Topi:
                if j[1] != 0.0:
                    if log(j[1],10) < dE:
                        if log(j[1],10) > savede:
                            savedk = j[0]
                            savede = log(j[1],10)
            resultsT.append([dE,savedk])

            savede = log(1E-20,10)
            savedk = 0
            for j in Bottomi:
                if j[1] != 0.0:
                    if log(j[1],10) < dE:
                        if log(j[1],10) > savede:
                            savedk = j[0]
                            savede = log(j[1],10)
            resultsB.append([dE,savedk])

        # Now that the lists are sorted we can get the ratio of kpoints
        for j in range(len(resultsB)):
            if resultsT[j][1] != 0 and resultsB[j][1] != 0:
                resultsTB.append([resultsB[j][0],resultsT[j][1]/float(resultsB[j][1])])

        # Now we save the output data
        if not path.isdir("../data/{0}_vs_{1}/".format(names[0],names[1])):
            mkdir("../data/{0}_vs_{1}/".format(names[0],names[1]))
        outT = open("../data/{0}_vs_{1}/{2}_{3}_{4}.csv".format(names[0],names[1],names[0][0],element,size),"w+")
        writerT = csv.writer(outT,delimiter='\t')
        for d in resultsTB:
            writerT.writerow(d)
        outT.close()
