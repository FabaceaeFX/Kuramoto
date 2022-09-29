
''' 
 * CSV_vectorReader.py
 *
 *   Created on:         15.02.2019
 *   Author:             Andrew Jason Bishop
 * 
 * General description:
 *   https://realpython.com/python-csv/
'''

import csv
import numpy as np
from itertools import islice


class CSV_vectorReader:

    def __init__(self):
        pass

    def getVectorBlock(self, _start, _stop, _vectorLength, _fileName):
        
        blockSize = _stop - _start
        vectorBlock = self.getPreparedNumpyArray( blockSize, _vectorLength )

        with open( _fileName, mode='r' ) as in_file:

            reader = csv.reader( in_file, delimiter=',' )
            block  = islice(reader, _start, _stop)

            for i, row in enumerate(block):

                npRow = np.asarray(row)
                npRow = npRow.astype(np.float)
                if npRow.shape[0] > 0:
                    vectorBlock[i] = npRow


        return vectorBlock


    def getPreparedNumpyArray(self, _blockSize, _vectorLength):
        return np.zeros( (_blockSize, _vectorLength) )







''' END '''

