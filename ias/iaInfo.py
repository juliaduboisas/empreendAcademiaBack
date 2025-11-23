from ias.modelResults import modelResults
from fastapi import HTTPException

import ias.iaPipeline as pipe
import pandas as pd

def runPipeline():
    results = pipe.runAIPipeline()
    return results

def getDfIndividualResultsFiltered():
    try:
        dfPredictions = pd.read_csv("predictions/predicoes_alunos_academia.csv")
        dfStudents = pd.read_csv("database.csv")

        dfIndividualResults = pd.merge(dfPredictions,
                                       dfStudents,
                                       left_on="aluno_id",
                                       right_on="aluno_id",
                                       how="inner")

        columnsToKeep = ["aluno_id", "Nome", "Objetivo", "unidade", "predicao"]
        columnsToDrop = dfIndividualResults.columns.difference(columnsToKeep)

        dfIndividualResultsFiltered = dfIndividualResults.drop(columns=columnsToDrop, axis=1)

        return dfIndividualResultsFiltered

    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Data file not found on the server.")
    except pd.errors.EmptyDataError:
        return []
    except Exception as e:
        print(f"An unexpected error occurred during CSV reading: {e}")
        raise HTTPException(status_code=500, detail="Error processing data file.")


def getIndividualResults():
    try:
        dfIndividualResultsFiltered = getDfIndividualResultsFiltered()

        results = dfIndividualResultsFiltered.to_dict('records')

        return results

    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Data file not found on the server.")
    except pd.errors.EmptyDataError:
        return []
    except Exception as e:
        print(f"An unexpected error occurred during CSV reading: {e}")
        raise HTTPException(status_code=500, detail="Error processing data file.")

def getStudentPrediction(id: int):
    try:
        df = getDfIndividualResultsFiltered()
        result = df.loc[df["aluno_id"] == id]

        if not result.empty:
            return result.iloc[0].to_dict()
        else:
            return None;

    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Data file not found on the server.")
    except pd.errors.EmptyDataError:
        return []
    except Exception as e:
        print(f"An unexpected error occurred during CSV reading: {e}")
        raise HTTPException(status_code=500, detail="Error processing data file.")

def getStudentEvasionPredictionPercentage():
    try:
        df = pd.read_csv("predictions/predicoes_alunos_academia.csv")

        positiveCount = df["predicao"].sum()

        totalPredictions = df.shape[0]

        positivePercentage = (float(positiveCount) / float(totalPredictions)) * float(100)

        return positivePercentage

    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Data file not found on the server.")
    except pd.errors.EmptyDataError:
        return []
    except Exception as e:
        print(f"An unexpected error occurred during CSV reading: {e}")
        raise HTTPException(status_code=500, detail="Error processing data file.")

def getPredictionPercentagePerUnit(unit: str):
    try:
        df = getDfIndividualResultsFiltered()

        dfFiltered = df.loc[df["unidade"] == unit]

        positiveCount = dfFiltered["predicao"].sum()

        totalPredictions = dfFiltered.shape[0]

        positivePercentage = (float(positiveCount) / float(totalPredictions)) * float(100)

        return positivePercentage

    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Data file not found on the server.")
    except pd.errors.EmptyDataError:
        return []
    except Exception as e:
        print(f"An unexpected error occurred during CSV reading: {e}")
        raise HTTPException(status_code=500, detail="Error processing data file.")
