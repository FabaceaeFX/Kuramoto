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
            
        
    def getSingleVector(self, _fileName, _t, _numOsc):

        vectorInVector = self.csv_Reader.getVectorBlock(_t-1, _t, _numOsc, _fileName)
        vector = vectorInVector[0]
        return vector

            
if __name__ == '__main__':
    import Parameter        as par   
    import CSV_vectorReader as vr
    import PlotResults      as pr

    myVectorReader = vr.CSV_vectorReader()
    myPlotResults  = pr.PlotResults( myVectorReader )



        
    myMeanFrequencies = MeanFrequencies(myVectorReader, myPlotResults, par.numOsc)

    NumOfSigma = round( (par.EndSigma - par.StartSigma) / par.deltaSigma )
    print("NumOfSigma", NumOfSigma)
    SigmaArray = par.SigmaArray
    print(SigmaArray.shape)
    SigmaArray = 1/par.deltaSigma*SigmaArray
    print("SigmaArray", SigmaArray.shape)
        
    MeanFrequency = True
    if MeanFrequency:
        MatrixShape = (NumOfSigma+1, par.numOsc)
        
        MeanFrequencyMatrix = np.zeros(MatrixShape)
        

        for sigma in SigmaArray:

            start = par.t1_Phases
            stop  = par.t2_Phases


            MeanFrequency = myMeanFrequencies.CalculateMeanFrequencies( start,\
                                                                        stop, \
                                                                        par.deltaSigma*sigma,\
                                                                        par.numOsc)


            ZerosMatrix = np.zeros(MatrixShape)
            ZerosMatrix[int(sigma),:] += MeanFrequency
            MeanFrequencyMatrix += ZerosMatrix




            
            

        SigmaArray = par.deltaSigma*SigmaArray
        print(SigmaArray)
        
            
            
    
    plot_MeanFrequencies = True
    if plot_MeanFrequencies:
        print(SigmaArray.shape, MeanFrequencyMatrix.shape)
        mp.plot(SigmaArray, MeanFrequencyMatrix, linestyle='-', color='r')
        mp.ylabel('Mean frequencies')
        mp.xlabel('Coupling strength')
        mp.axis([par.StartSigma, par.EndSigma, par.FirstYAxis, par.LastYAxis])
        ax = mp.subplot(111)
        #mp.title('Mean frequencies during the last ' + str(par.deltaT) + ' timesteps of ' \
                           # + str(par.numOsc) + ' Oszillators for increasing coupling strength')
        mp.show()
                
    
''' END '''
