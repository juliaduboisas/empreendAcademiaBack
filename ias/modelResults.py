import string
import this


def modelResults():
    algorithm: string
    crossValidation: string
    syntheticData: string
    accuracy: float
    precision: float
    recall: float
    f1: float

    def setAlgorithm(algorithm: string):
        this.algorithm = algorithm

    def getAlgorithm():
        return this.algorithm

    def setCrossValidation(crossValidation: string):
        this.crossValidation = crossValidation

    def getCrossValidation():
        return this.crossValidation

    def setSyntheticData(syntheticData: string):
        this.syntheticData = syntheticData

    def getSyntheticData():
        return this.syntheticData

    def setAccuracy(accuracy: float):
        this.accuracy = accuracy

    def getAccuracy():
        return this.accuracy

    def setPrecision(precision: float):
        this.precision = precision

    def getPrecision():
        return this.precision

    def setRecall(recall: float):
        this.recall = recall

    def getRecall():
        return this.recall

    def setF1(f1: float):
        this.f1 = f1

    def getF1():
        return this.f1