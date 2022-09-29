import numpy as np
import matplotlib.pyplot as mp


class MeanFrequencies:
    
    def __init__( self, _csvReader, _PlotResults, _numOsc=50):
        
        self.csv_Reader  = _csvReader
        self.PlotResults = _PlotResults
        
        self.numOsc      = 0

    def CalculateMeanFrequencies(self, _t1, _t2, _sigma, _numOsc):
            
        self.t1 = _t1
        self.t2 = _t2
        deltaT  = self.t2-self.t1
            
        initPhases, lastPhases = self.getVectorsOutOfVectorBlock( _t1, _t2, _sigma, _numOsc)
        MeanFrequency = (lastPhases-initPhases)/deltaT
        return MeanFrequency
        
    def getVectorsOutOfVectorBlock(self, _t1, _t2, _sigma, _numOsc):
            
        filename = self.PlotResults.assembleFileName("Phases", _sigma)
        initPhases = self.getSingleVector(filename, _t1, _numOsc)
        lastPhases = self.getSingleVector(filename, _t2, _numOsc)
        return initPhases, lastPhases
            
        
    def getSingleVector(self, _fileName, _t, _vecLen):

        self.csv_Reader.setVectorLength( _vecLen )
        vectorInVector = self.csv_Reader.getVectorBlock(_t-1, _t, _fileName)
        vector = vectorInVector[0]
        return vector

            
if __name__ == '__main__':
        
    import CSV_vectorReader as vr
    import PlotResults      as pr

    myVectorReader = vr.CSV_vectorReader()
    myPlotResults  = pr.PlotResults( myVectorReader )


    t1    = 701
    t2    = 999
    numOsc = 50
        
        
    deltaSigma = 0.01
    StartSigma = 0 
    EndSigma   = 3
        
    myMeanFrequencies = MeanFrequencies(myVectorReader, myPlotResults, numOsc)

    NumOfSigma = round( (EndSigma - StartSigma) / deltaSigma )
    SigmaArray = np.linspace(StartSigma, EndSigma, NumOfSigma+1)
        
    MeanFrequency = True
    if MeanFrequency:
        MeanFrequencyList = []

        for sigma in SigmaArray:

            start = t1
            stop  = t2


            MeanFrequency = myMeanFrequencies.CalculateMeanFrequencies( start,\
                                                                        stop, \
                                                                        sigma,\
                                                                        numOsc)

    
                
            MeanFrequencyList.append(MeanFrequency)
            MeanFrequencyArray = np.asarray(MeanFrequencyList)

    plot_MeanFrequencies = True
    if plot_MeanFrequencies:
        mp.plot(SigmaArray, MeanFrequencyArray, linestyle='-', color='r')
        mp.axis([StartSigma, EndSigma, -1, 0.2])
        mp.show()
                
    
''' END '''
