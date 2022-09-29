 
import numpy             as np
import matplotlib.pyplot as mp


import Parameter        as par
import Kuramoto         as ku
import InitGenerator    as ig
import CSV_handler      as ch
import CSV_vectorWriter as vw
import CSV_vectorReader as vr
import OrderParameter   as op
import PlotResults      as pr
import MeanFrequencies  as mf


class ProjectKuramoto:

    def __init__(self, _parameters, _kuramoto, _initGenerator, _csvHandler, _meanFrequencies, _plotResults, _numOsc=par.numOsc):
        
        self.parameters       = _parameters
        self.kuramoto         = _kuramoto
        self.init             = _initGenerator
        self.csvHandler       = _csvHandler
        self.mean             = _meanFrequencies
        self.plot             = _plotResults
        

        self.numOsc           = 0
        self.timeSteps        = par.NumOfTimeSteps
        self.allResults       = None

        self.setNumberOfOscillators( _numOsc )


    def setNumberOfOscillators(self, _numOsc):

        self.numOsc   = _numOsc
        self.kuramoto.setNumberOfOscillators( _numOsc )
        self.init.setNumberOfOscillators( _numOsc )
        

        #print("\nNumber of oscillators set to", self.numOsc, "\n")


    def solveMultipleRunsWithSelfFeedingInit(self, _numOsc,
                                                   _StartSigma,
                                                   _NumOfSigma,
                                                   _nextSigma,
                                                   _timeStepsToStore,
                                                   _LastCouplings):
       
         
        if par.randomInit:
            randomInit = self.init.makeRandomInitConditions()
            self.kuramoto.solveKuramoto( self.timeSteps, randomInit )

            PhaseFileName = "/home/fabaceae/Desktop/Physik/Kuramoto/Results/Phases/Phases-sigma-" +\
                       par.NumOfDecimals.format(self.kuramoto.sigma) + '.csv'

            CouplingFileName = "/home/fabaceae/Desktop/Physik/Kuramoto/Results/Couplings/Couplings-sigma-" + \
                   par.NumOfDecimals.format(self.kuramoto.sigma) + '.csv'

        
        if par.chosenInit:
         
            fileNamePhases = self.plot.assembleFileName("Phases", par.LastSigmaLastRun)
            fileNameCouplings = self.plot.assembleFileName("Couplings", par.LastSigmaLastRun)

            chosenInitPhases = self.mean.getSingleVector(fileNamePhases, par.lastTimeStepOfLastRun, _numOsc)
            chosenInitCouplings = self.mean.getSingleVector(fileNameCouplings,_LastCouplings, _numOsc*_numOsc)
            chosenInit = np.concatenate((chosenInitPhases, chosenInitCouplings))
            self.kuramoto.solveKuramoto( self.timeSteps, chosenInit )
            
            PhaseFileName = "/home/usersrw/Philippe/NextPhases/Phases-sigma-" +\
                       par.NumOfDecimals.format(self.kuramoto.sigma) + '.csv'

            CouplingFileName = "/home/user0/Philippe/NextCouplings/Couplings-sigma-" + \
                   par.NumOfDecimals.format(self.kuramoto.sigma) + '.csv'      
                     
                       


        t1_Phases= self.timeSteps - _timeStepsToStore - 1
        t2_Phases = self.timeSteps - 1
        
        FirstCouplingTimeStep = 0
        LastCouplingsTimeStep =  self.timeSteps - 1

        phases = self.kuramoto.getResults('Phases', (t1_Phases, t2_Phases))
        

        self.saveRunInNewFile(phases, PhaseFileName)

        if par.AllCouplings:
                
               self.saveAllCouplingResults(CouplingFileName, t1_Phases, t2_Phases)
 
        else:
                
            self.saveTwoCouplingResults(CouplingFileName, FirstCouplingTimeStep, \
                                                              LastCouplingsTimeStep)


        self.kuramoto.sigma += _nextSigma
        newInitValue = self.getLastTimeStep()



        for i in range(0, _NumOfSigma):

            self.kuramoto.solveKuramoto( self.timeSteps, newInitValue )
            
            if par.randomInit:
                PhaseFileName = "/home/fabaceae/Desktop/Physik/Kuramoto/Results/Phases/Phases-sigma-" + \
                      par.NumOfDecimals.format(self.kuramoto.sigma) + '.csv'
                CouplingFileName = "/home/fabaceae/Desktop/Physik/Kuramoto/Results/Couplings/Couplings-sigma-" + \
                       par.NumOfDecimals.format(self.kuramoto.sigma) + '.csv'

            if par.chosenInit: 
                 PhaseFileName = "/home/fabaceae/Desktop/Physik/Kuramoto/Results/Phases/Phases-sigma-" + \
                       par.NumOfDecimals.format(self.kuramoto.sigma) + '.csv'
                 CouplingFileName = "/home/fabaceae/Desktop/Physik/Kuramoto/Results/Couplings/Couplings-sigma-" + \
                       par.NumOfDecimals.format(self.kuramoto.sigma) + '.csv'
                

            t1_Phases = self.timeSteps - _timeStepsToStore - 1
            t2_Phases = self.timeSteps - 1
            
            
            FirstCouplingTimeStep = 0
            LastCouplingTimeStep =  self.timeSteps - 1



            phases = self.kuramoto.getResults('Phases', (t1_Phases, t2_Phases))

            self.saveRunInNewFile(phases, PhaseFileName)

            if par.AllCouplings:
                
                self.saveAllCouplingResults(CouplingFileName, t1_Phases, t2_Phases)
 
            else:
                
                self.saveTwoCouplingResults(CouplingFileName, FirstCouplingTimeStep, \
                                                              LastCouplingTimeStep)


            self.kuramoto.sigma += _nextSigma
            newInitValue = self.getLastTimeStep()

    def saveTwoCouplingResults(self, _couplingFileName, _FirstCouplingTimeStep, _LastCouplingTimeStep):

        FirstCouplings = self.kuramoto.getCouplingsForOneTimeStep(_FirstCouplingTimeStep)
        LastCouplings  = self.kuramoto.getCouplingsForOneTimeStep(_LastCouplingTimeStep)


        self.saveRunInNewFile(FirstCouplings, _couplingFileName)
        self.saveRunInSameFile(LastCouplings, _couplingFileName)

        

    def saveAllCouplingResults(self, _couplingFileName, _t1_Phases, _t2_Phases ):
        
        couplings = self.kuramoto.getResults('Couplings', (_t1_Phases, _t2_Phases))
        self.saveRunInNewFile(couplings, _couplingFileName)


    def saveRunInNewFile(self, _resultsToSave, _fileName):

        self.csvHandler.writeVectorsToNewFile( _resultsToSave, _fileName )
        
    def saveRunInSameFile(self, _resultsToSave, _fileName):
    
        self.csvHandler.appendVectorsToFile( _resultsToSave, _fileName )


    def getRunFromFile(self, _fileName, _blockSize):
        return self.csvHandler.getVectorBlockFromFile( _fileName, _blockSize )


    def solveKuramotoWithGivenInit(self, _numOfTimeSteps, _init):
        self.kuramoto.solveKuramoto( _numOfTimeSteps, _init )


    def getLastTimeStep(self):

        #FIXME cake slice: getSingleResult vs. getResultTimeInterval
        lastTimeStep = (self.timeSteps - 1, self.timeSteps)
        return self.kuramoto.getResults( "all", lastTimeStep )[0]


    def getPhaseResults(self, _timeIndex=None):
        return self.kuramoto.getPhaseResults( _timeIndex )


    def getCouplingResults(self, _timeIndex=None):
        return self.kuramoto.getCouplingResults( _timeIndex )



if __name__ == '__main__':

    
    myParameter = par
    myKuramoto1 = ku.Kuramoto(par.a, par.e, par.b, par.StartSigma, par.Omega)
    myInitGenerator = ig.InitGenerator()


    myVectorWriter = vw.CSV_vectorWriter()
    myVectorReader = vr.CSV_vectorReader()
    myCSV_handler = ch.CSV_handler(myVectorWriter, myVectorReader)

    myPlotResults = pr.PlotResults(myVectorReader)

    myMeanFrequencies = mf.MeanFrequencies(myVectorReader, myPlotResults, par.numOsc)

    myOrderParameter = op.OrderParameter(par.OrderThreshold, myVectorReader)
    myProjectKuramoto = ProjectKuramoto(myParameter, myKuramoto1, myInitGenerator, myCSV_handler, myMeanFrequencies, myPlotResults, par.numOsc)

    '''timeSteps = myProjectKuramoto.timeSteps = 10000
    randomInit = myProjectKuramoto.init.makeRandomInitConditions()
    myKuramoto1.solveKuramoto(timeSteps, randomInit)
    Results = myKuramoto1.getAllResultsInOneVectorPerTimeStep()'''
    
   

    calculateAndSaveRuns = True
    if calculateAndSaveRuns:
        myProjectKuramoto.solveMultipleRunsWithSelfFeedingInit(par.numOsc,     \
                                                               par.StartSigma, \
                                                               par.NumOfSigma, \
                                                               par.deltaSigma, \
                                                               par.timeStepsToStore,\
                                                               par.LastCouplings)
    
    
        

''' END '''

