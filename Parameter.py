import numpy as np


#GeneralParameters

numOsc = 50
a = 0.9* np.pi
e = 0.01
b = 0.9*np.pi



#Frequency Distribution

SeedNumber = 5
np.random.seed(SeedNumber)
StartOmega = -0.5    
EndOmega   = 0.5
Omega = np.random.uniform(StartOmega, EndOmega, numOsc)
DeltaOmega = EndOmega-StartOmega

#CouplingParameter

deltaSigma = 0.1
StartSigma = 3
EndSigma   = 10

NumOfSigma = round( (EndSigma - StartSigma) / deltaSigma )
SigmaArray = np.linspace(StartSigma, EndSigma, NumOfSigma+1)
OrderSigmaArray = np.linspace(StartSigma, EndSigma, NumOfSigma)

TwoDecimalSigma = True          
if TwoDecimalSigma:
    NumOfDecimals = "{:1.2f}"

ThreeDecimalSigma = False
if ThreeDecimalSigma:
    NumOfDecimals = "{:1.3f}"

#RunSettingsRandomOrChosen

randomInit = True 
chosenInit = False

#HystereseCheck

StartingWithSameFile = False
if  StartingWithSameFile:
    LastSigmaLastRun = StartSigma
else:
    LastSigmaLastRun = StartSigma-deltaSigma
    


#Projekt-Kuramoto

NumOfTimeSteps = 1000

InitTimeStep = 2999
LastTimeStep = NumOfTimeSteps-1
timeStepsToStore = NumOfTimeSteps-1


lastTimeStepsForOrdParam = 300
OrderThreshold = 0.5

AllCouplings = True

lastTimeStepOfLastRun = NumOfTimeSteps-1

LastRunAllCouplings = False
if LastRunAllCouplings:
    FirstCouplings = 1
    LastCouplings = lastTimeStepOfLastRun
else:
    FirstCouplings = 1
    LastCouplings  = 2

SaveMod2Pi = False



#MainSortAndPlotRunAndMeanFrequencies

ChosenSigma = 3

t1_Phases   = 7999
t2_Phases   = 9999
deltaT = t2_Phases-t1_Phases

PresentRunAllCouplingsSaved = False
if PresentRunAllCouplingsSaved:
    FirstCouplings = 1
    LastCouplings = t2_Phases
else:
    FirstCouplings = 1
    LastCouplings  = 2
    

PhasesAndCouplingsOverTime = False

#GeneralPlotSettings

OrderPlot = False
ScatterPlot = True

SigmaPlot  = 3
FirstYAxis = 0
LastYAxis  = 0.4

SeedNumber1 = 36
SeedNumber2 = 42
SeedNumber3 = 63
SeedNumber4 = 79

linewidth  = 0.1
DotSize = 1













