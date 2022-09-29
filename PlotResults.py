'''
 * Plot_Results.py
 *
 *   Created on:         01.03.2019
 *   Author:             Philippe Lehmann
 *
 * General description:
 *   https://realpython.com/python-csv/
'''
import Parameter  as par
import matplotlib as mp
import matplotlib.pyplot as plt
import numpy      as np

class PlotResults:


    def __init__(self, _csvReader):
    
        self.csvReader = _csvReader
        


    def PlotResultsForSpecificSigma(self, _resultName, _sigma, _vecLen):

        fileName = self.assembleFileName( _resultName, _sigma )
        results  = self.fetchResults( fileName, _vecLen )
        
        #if _resultName == "Phases":
            #results = np.mod(results, 2*np.pi)
            
        plt.plot( results, linewidth=par.linewidth)
        ax = plt.axes()
        plt.subplots_adjust(left=0, bottom=0, right=1, top=1)
        plt.axis('off')
        plt.show()
     
     
     
     
     
    
    def assembleFileName(self, _resultName, _sigma):

        sigmaAsStr= par.NumOfDecimals.format( _sigma )
        folder ="/home"+"/fabaceae"+"/Desktop"+"/Physik"+"/Kuramoto"+"/Results" + "/" + _resultName + "/"
        fileName =  folder + _resultName + "-sigma-" + sigmaAsStr + ".csv"
        return fileName


    def fetchResults(self, _fileName, _vecLen):
    
        return self.csvReader.getVectorBlock( 0, par.timeStepsToStore,_vecLen, _fileName)
        
        
        
        
        
        
        
if __name__ == '__main__':

    import CSV_handler      as ch
    import CSV_vectorWriter as vw
    import CSV_vectorReader as vr

    myVectorWriter = vw.CSV_vectorWriter()
    myVectorReader = vr.CSV_vectorReader()
    myCSV_handler = ch.CSV_handler(myVectorWriter, myVectorReader)

    myPlotResults = PlotResults( myVectorReader )

    sigma = par.SigmaPlot
    myPlotResults.PlotResultsForSpecificSigma("Couplings", sigma, par.numOsc*par.numOsc)
    #myPlotResults.PlotResultsForSpecificSigma("Couplings", sigma)

''' END '''

