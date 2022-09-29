
''' 
 * Main-SortAndPlotRun.py
 *
 *   Created on:         02.02.2019
 *   Author:             Philippe Lehmann
 *   Coauthors:          Jan Fialkowski, Andre Meissner
 * 
 * General description:
 *   xxx
'''

import numpy             as np
import matplotlib.pyplot as mp
import scipy.stats

import Parameter        as par
import CSV_vectorWriter as vw
import CSV_vectorReader as vr
import CSV_handler      as ch
import PlotResults      as pr
import SortOscillators  as so

myVectorWriter = vw.CSV_vectorWriter()
myVectorReader = vr.CSV_vectorReader()
myCSV_handler = ch.CSV_handler(myVectorWriter, myVectorReader)
myPlotResults  = pr.PlotResults( myVectorReader )
mySortOscillators = so.SortOscillators(myCSV_handler)




def getRandomGeneratedInitOutOfCSV(_RandomInitPhases = 1):

    PhaseFileName    = myPlotResults.assembleFileName("Phases", par.StartSigma)
    RandomInitPhases = getSingleVector(PhaseFileName, _RandomInitPhases, par.numOsc)

    return RandomInitPhases

def getPhisAndCouplingsOutOfCSV(_t1_Phases, _t2_Phases, _FirstCouplings, _LastCouplings, _sigma, _numOsc):

    PhaseFileName = myPlotResults.assembleFileName("Phases", _sigma)
    initPhases    = getSingleVector(PhaseFileName, _t1_Phases, _numOsc)
    lastPhases    = getSingleVector(PhaseFileName, _t2_Phases, _numOsc)

    CouplingFileName       = myPlotResults.assembleFileName("Couplings", _sigma)
    firstCouplings = getSingleVector(CouplingFileName, _FirstCouplings, _numOsc*_numOsc)
    lastCouplings  = getSingleVector(CouplingFileName, _LastCouplings, _numOsc*_numOsc)
    

    return initPhases, lastPhases, firstCouplings, lastCouplings



def getSingleVector(_fileName, _t, _vecLength):

   
    vectorInVector = myVectorReader.getVectorBlock(_t-1, _t, _vecLength, _fileName)
    vector = vectorInVector[0]
    return vector


if __name__ == '__main__':
    
    import Parameter as par

    initPhases, lastPhases, firstCouplings, lastCouplings = getPhisAndCouplingsOutOfCSV      \
                                                               (par.t1_Phases, par.t2_Phases,\
                                                                par.FirstCouplings,          \
                                                                par.LastCouplings,           \
                                                                par.ChosenSigma, par.numOsc) 
  

    
    
    nodes, SortedCouplings = mySortOscillators.sortOscillators(initPhases, lastPhases, lastCouplings, par.deltaT)
    #nodes, FirstCouplings = mySortOscillators.sortOscillators(initPhases, lastPhases, firstCouplings, par.deltaT)
    SortedNaturalFrequencies = mySortOscillators.sortNaturalFrequenciesForNodeIndex()
    
    
    #PlotPhasesOfEachNode
    
    mp.plot (nodes[:]["phase"])
    mp.ylabel('Phases')
    mp.xlabel('Nodes')
    mp.title('Phase distribution of ' + str(par.numOsc) + ' nodes at timestep: ' + \
                    str(par.t2_Phases) + ' for $\sigma$  = ' + str(par.ChosenSigma))
    mp.show()
    
    #PlotMeanFrequencyOfEachNode

    mp.plot (nodes[:]["frequency"])
    mp.ylabel('Frequencies')
    mp.xlabel('Nodes')
    mp.title('Frequency distribution of ' + str(par.numOsc) + ' nodes at timestep: ' + \
                    str(par.t2_Phases) + ' for $\sigma$  = ' + str(par.ChosenSigma))
    mp.show()
    
    #mp.imshow(FirstCouplings, origin = "lower")
    #mp.colorbar()
    #mp.show()


    #PlotCouplingForEachNode


    mp.imshow(SortedCouplings, origin = "lower")
    mp.ylabel('j', rotation=0)
    mp.xlabel('i')
    colorbar = mp.colorbar()
    colorbar.ax.set_yticklabels(['','','','','','',''])
    mp.title('Coupling strength between ' + str(par.numOsc) + ' nodes at timestep: ' + \
                    str(par.t2_Phases) + ' for $\sigma$ = ' + str(par.ChosenSigma))
    mp.show()
    
    #PlotCouplingsAndPhasesOverTime

     
    if par.PhasesAndCouplingsOverTime:

        myPlotResults.PlotResultsForSpecificSigma("Phases", par.ChosenSigma, par.numOsc)
        myPlotResults.PlotResultsForSpecificSigma("Couplings", par.ChosenSigma, par.numOsc*par.numOsc)

    #PlotNodeSortedFrequencyDistribution
    
    mp.plot (SortedNaturalFrequencies)
    mp.show()
    
    
   

''' END '''

