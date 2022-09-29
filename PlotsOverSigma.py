import numpy as np
import matplotlib.pyplot as mp

import Parameter        as par
import OrderParameter   as op
import CSV_vectorReader as vr

myVectorReader   = vr.CSV_vectorReader()
myOrderParameter = op.OrderParameter(par.OrderThreshold, myVectorReader)

class PlotsOverSigma:

    def __init__(self):
        
        pass

    def getOrderParamOutOfCSV(self, _seed):
        
        
        OrderFileName = myOrderParameter.assembleOrderFileName(_seed)
        VectorLength  = 2
        sigmasAndOrders = myVectorReader.getVectorBlock( 0, par.NumOfSigma, VectorLength, OrderFileName )
        Orders     = sigmasAndOrders[:,[1]]
        Orders  = np.reshape(Orders[:,:1],(par.NumOfSigma))
       
        
        return Orders


if __name__ == '__main__':
    
    myPlotsOverSigma = PlotsOverSigma()

    if par.OrderPlot:

        OrderParamArray = myPlotsOverSigma.getOrderParamOutOfCSV(par.SeedNumber)
        plotOrderResults = mp.plot(par.OrderSigmaArray, OrderParamArray, linestyle='-', color='r')
        mp.ylabel('Rc')
        mp.xlabel('Sigma')
        mp.axis([par.StartSigma, par.EndSigma, par.FirstYAxis, par.LastYAxis])
        ax = mp.subplot(111)
        ax.plot(par.OrderSigmaArray, OrderParamArray, label='Order Parameter')
        '''mp.title('Order Parameter of ' + str(par.numOsc) + ' Oszillators, \
                    with parameters $\alpha$ = ' + str(par.a/np.pi) + ' and $\beta$ = ' + \
                     str(par.b/np.pi) + ' with $\Delta\omega$ = '+ str(par.DeltaOmega) + 'for increasing coupling strength')'''
        ax.legend()
        mp.show()

    
    #ScatterPlotForDifferentDistributions
    
    if par.ScatterPlot:

        OrderParamArray1 = myPlotsOverSigma.getOrderParamOutOfCSV(par.SeedNumber1)
        OrderParamArray2 = myPlotsOverSigma.getOrderParamOutOfCSV(par.SeedNumber2)
        OrderParamArray3 = myPlotsOverSigma.getOrderParamOutOfCSV(par.SeedNumber3)
        #OrderParamArray4 = myPlotsOverSigma.getOrderParamOutOfCSV(par.SeedNumber4)

        plotOrderResults1 = mp.scatter(par.OrderSigmaArray, OrderParamArray1, par.DotSize)
        plotOrderResults2 = mp.scatter(par.OrderSigmaArray, OrderParamArray2, par.DotSize)
        plotOrderResults3 = mp.scatter(par.OrderSigmaArray, OrderParamArray3, par.DotSize)
        #plotOrderResults4 = mp.scatter(par.OrderSigmaArray, OrderParamArray4)

        mp.ylabel('Rc')
        mp.xlabel('Sigma')
        mp.axis([par.StartSigma, par.EndSigma, par.FirstYAxis, par.LastYAxis])
        
        
        mp.show()

   

    
