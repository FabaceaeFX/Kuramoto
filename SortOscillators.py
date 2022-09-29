
''' 
 * SortData.py
 *
 *   Created on:         02.02.2019
 *   Author:             Philippe Lehmann
 *   Coauthors:          Jan Fialkowski, Andre Meissner
 * 
 * General description:
 *   xxx
'''

import numpy as np

import Parameter as par



class SortOscillators:

    def __init__(self, _csvHandler=None):

        self.csvHandler   = _csvHandler
        self.dtype        = [ ('node' , int  ),\
                              ('frequency', float),\
                              ('phase', float) ]

        self.lastPhis     = None
        self.initPhis     = None
        self.deltaT       = None
        self.couplings    = None
        self.SortedCouplings = None
        self.frequencys   = None
        self.nodes        = None
        self.numOsc       = 50

#Natural Frequencies have to be sorted like the sorted nodes in each run!



    

    def sortOscillators(self, _initPhases, _lastPhases, _Couplings, _deltaT):

        self.storeInitValues( _initPhases, _lastPhases, _Couplings, _deltaT )
        self.calculateFrequencys()
        self.createArrayOfEnumeratedFrequencysAndPhis()
        self.sortNodesForFreqAndPhases()
        self.shapeCouplingsAsMatrix()
        self.sortCouplingsForNodeIndex()

        return(self.nodes, self.SortedCouplings)

    def storeInitValues(self, _initPhases, _lastPhases, _Couplings, _deltaT):

        self.lastPhis   = _lastPhases
        self.initPhis   = _initPhases
        self.couplings  = _Couplings
        self.deltaT     = _deltaT
        self.numOsc     = self.lastPhis.shape[0]

    def calculateFrequencys(self):
        self.frequencys = (self.lastPhis - self.initPhis) / self.deltaT


    def createArrayOfEnumeratedFrequencysAndPhis(self):

        enumerates = []
        for i in range(self.numOsc):

            roundedFrequency = self.roundFrequency(i)
            moduloDividedPhi = self.moduloDividePhi(i)
            enumerated       = (i, roundedFrequency, moduloDividedPhi)

            enumerates.append( enumerated )

        self.makeNumpyArrayOfEnumerates( enumerates )


    def roundFrequency(self, _node):
        return round( self.frequencys[_node], 2 )

   
    def moduloDividePhi(self, _node):
        return  np.mod(self.lastPhis[_node], 2*np.pi)
        


    def makeNumpyArrayOfEnumerates(self, _enumerates):
        self.nodes = np.array( _enumerates, dtype=self.dtype )


    def sortNodesForFreqAndPhases(self):
        self.nodes = np.sort(self.nodes, order=['frequency', 'phase'])
       


    def shapeCouplingsAsMatrix(self):
        self.couplings = self.couplings.reshape(self.numOsc, self.numOsc)
       

    def sortCouplingsForNodeIndex(self):
        self.SortedCouplings = self.couplings[:, self.nodes['node']][self.nodes['node']]
        

    def sortNaturalFrequenciesForNodeIndex(self):
        self.SortedNaturalFrequencies = par.Omega[self.nodes['node']]
        return(self.SortedNaturalFrequencies)
        
        
       

''' END '''

