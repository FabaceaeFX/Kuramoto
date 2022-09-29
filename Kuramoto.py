
''' 
 * Kuramoto.py
 *
 *   Created on:         08.01.2019
 *   Author:             Philippe Lehmann
 * 
 * General description:
 *   xxx
'''

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as mp
from numpy import diff

import Parameter        as par
import InitGenerator    as ig

class Kuramoto:

    def __init__(self,_a, _e, _b, _sigma,_omega):

        self.a = _a
        self.e = _e
        self.b = _b
        self.sigma = _sigma
        self.omega = _omega


        self.dydt    = None
        self.results = {}
        self.x_init  = None
        self.t       = None
        self.N       = 0
        self.dkdt    = None
        self.Phis    = None



    def setNumberOfOscillators(self, _numOsc):
        self.N = _numOsc


    def solveKuramoto(self, _numOfTimeSteps, _initCond):

        self.x_init = _initCond

        self.makeTimeLine( _numOfTimeSteps )

        results = odeint( self.kuramotoderiv, self.x_init, self.t )
        if par.SaveMod2Pi:
            results = np.mod(results, 2*np.pi)
        self.storeResultsAsDict( results )


    def makeTimeLine(self, _numOfTimeSteps):

        startTime       = 0
        endTime         = _numOfTimeSteps
        numOfIntervalls = _numOfTimeSteps

        self.t = np.linspace( startTime, endTime, numOfIntervalls )


    def storeResultsAsDict(self, _results):

        self.results['Phases']    = _results[: , :self.N]
        self.results['Couplings'] = _results[: , self.N:self.N**2+self.N]


    def kuramotoderiv(self, _x, _t):
        Phis = _x[:self.N]
        Kappas = _x[self.N:].reshape(self.N, self.N)
        DelPhis = (Phis - Phis[:, np.newaxis]).T
        DKappa = -self.e * (np.sin(DelPhis + self.b) + Kappas)
        DelPhis += self.a
        DelPhis = Kappas * np.sin(DelPhis)
        DPhis = self.omega-self.sigma*DelPhis.sum(axis=1) / Phis.shape[0]
        self.dydt = np.concatenate((DPhis, DKappa.flatten()))

        return self.dydt


    def getResults(self, _resultName, _timeIntervall=None):

        results = None

        if _resultName in self.results:
            results = self.results[_resultName]
        else:
            results = self.getAllResultsInOneVectorPerTimeStep()


        if _timeIntervall:
            return self.selectResultsInTimeInterval( results, _timeIntervall )
        else:
            return results

    def getPhasesForOneTimeStep(self, _TimeStep):

        Phases = self.results['Phases']

        PhasesForOneTimeStep = Phases[_TimeStep,:]
        return(PhasesForOneTimeStep)

    def getCouplingsForOneTimeStep(self, _TimeStep):

        Couplings = self.results['Couplings']

        CouplingsForOneTimeStep = Couplings[_TimeStep, :]
        return(CouplingsForOneTimeStep)




    def getAllResultsInOneVectorPerTimeStep(self):

        phases = self.results['Phases']
        couplings = self.results['Couplings']

        resultsAsOneVectorPerTimeStep = np.concatenate((phases, couplings), axis=1)
        return resultsAsOneVectorPerTimeStep


    def selectResultsInTimeInterval(self, _results, _timeIntervall):

            t1 = _timeIntervall[0]
            t2 = _timeIntervall[1]
            return _results[t1:t2]



    

''' END '''

