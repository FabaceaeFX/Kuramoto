
''' 
 * OrderParameter.py
 *
 *   Created on:         07.02.2019
 *   Author:             Philippe Lehmann
 * 
 * General description:
 *   xxx
'''

import numpy as np
import scipy.stats

import Parameter  as par
import CSV_vectorWriter as vw
import CSV_vectorReader as vr
import CSV_handler      as ch




class OrderParameter:

    def __init__(self, _OrderThreshold, _vecRead):

        self.vectorReader = _vecRead
        self.sigmas = None
        self.Orders = None



    def ConcatenateAllOrderParameters(self):
    
        OrderParamList = []

        for sigma in par.SigmaArray:

            start = par.timeStepsToStore - par.lastTimeStepsForOrdParam
            stop = par.timeStepsToStore

            
            PhaseFileName = "/home/user0/Physik/Kuramoto/Results/Phases/Phases-sigma-" +\
                        par.NumOfDecimals.format(sigma) + '.csv'
           

            block = myVectorReader.getVectorBlock( start     ,\
                                                   stop      ,\
                                                   par.numOsc,\
                                                   PhaseFileName )

            orderParameter = self.SumUpOrderMatrix_Elements( block )
            print("Order Parameter of run with sigma ",\
                par.NumOfDecimals.format(sigma), ":", orderParameter)
            OrderParamList.append([sigma, orderParameter])

        OrderParamArray = np.asarray(OrderParamList)


        self.storeOrderParamAndSigmas(OrderParamArray)

        print(OrderParamArray)  
        return OrderParamArray
        

    
    def storeOrderParamAndSigmas(self, _sigmaOrderParam):
        OrderFileName = self.assembleOrderFileName()
        myCSV_handler.appendVectorsToFile( _sigmaOrderParam, OrderFileName )    

    def assembleOrderFileName(self, _seed):
        OrderFileName =  "/home/user0/Physik/Kuramoto/Results/Order("+str(_seed)+")/OrderParam" + '.csv' 
        return OrderFileName   


    def SumUpOrderMatrix_Elements(self, _phases):

        OrderMatrix = self.SumUpOrderMatrixArray( _phases )
        OrderParam = np.sum(OrderMatrix)\
         / (OrderMatrix.shape[0]*OrderMatrix.shape[0])
        return OrderParam


    def SumUpOrderMatrixArray(self, _phases):

        orderMatrixList = self.CreateOrderMatrixArray( _phases )
        orderMatrixShape = orderMatrixList[0].shape
        sumOrderMatrix = np.zeros(orderMatrixShape, dtype=np.complex_)

        for matrix in orderMatrixList:
            sumOrderMatrix += matrix


        sumOrderMatrix = sumOrderMatrix.real
        sumOrderMatrix = sumOrderMatrix / _phases.shape[0]
        sumOrderMatrix[sumOrderMatrix<self.OrderThreshold] = 0
        sumOrderMatrix[sumOrderMatrix>=self.OrderThreshold] = 1

        


        return sumOrderMatrix




    def CreateOrderMatrixArray(self, _phases):

        MatrixArray = []
        timeStepCount = _phases.shape[0]

        for ts in range(0,timeStepCount):
            singleTimeStepPhaseDiff = np.exp(1j*(_phases[ts] - _phases[ts][:, np.newaxis]))
            MatrixArray.append( singleTimeStepPhaseDiff )


        return np.array(MatrixArray, dtype=np.complex_)

if __name__ == '__main__':

    myVectorReader = vr.CSV_vectorReader()
    myVectorWriter = vw.CSV_vectorWriter()
    myCSV_handler = ch.CSV_handler(myVectorWriter, myVectorReader)
    myOrderParameter = OrderParameter(par.OrderThreshold, myVectorReader)
    myOrderParameter.ConcatenateAllOrderParameters()
    

''' END '''

