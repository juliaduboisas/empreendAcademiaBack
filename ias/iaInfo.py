from ias.modelResults import modelResults
from fastapi import HTTPException

import ias.iaPipeline as pipe
import pandas as pd

def runPipeline():
    results = pipe.runAIPipeline()
    return results

def getDfIndividualResultsFiltered(modelName: str):
    try:
        dfPredictions = pd.read_csv("predictions/" + modelName + "_predictions.csv")
        dfStudents = pd.read_csv("database.csv")

        dfIndividualResults = pd.merge(dfPredictions,
                                       dfStudents,
                                       left_on="Original_Synthetic_Row_ID",
                                       right_on="aluno_id",
                                       how="inner")

        columnName = modelName.replace("_", " ") + "_Prediction"

        columnsToKeep = ["aluno_id", "Nome", "Objetivo", "unidade", columnName]
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


def getIndividualResults(modelName: str):
    try:
        dfIndividualResultsFiltered = getDfIndividualResultsFiltered(modelName)

        results = dfIndividualResultsFiltered.to_dict('records')

        return results

    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Data file not found on the server.")
    except pd.errors.EmptyDataError:
        return []
    except Exception as e:
        print(f"An unexpected error occurred during CSV reading: {e}")
        raise HTTPException(status_code=500, detail="Error processing data file.")

def getStudentPrediction(id: int, modelName: str):
    try:
        df = getDfIndividualResultsFiltered(modelName)
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

def getStudentEvasionPredictionPercentage(modelName: str):
    try:
        df = pd.read_csv("predictions/" + modelName + "_predictions.csv")

        predictionColumn = modelName.replace("_", " ") + "_Prediction"
        positiveCount = df[predictionColumn].sum()

        totalPredictions = df.shape[0]

        positivePercentage = float(positiveCount) / float(totalPredictions)

        return positivePercentage

    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Data file not found on the server.")
    except pd.errors.EmptyDataError:
        return []
    except Exception as e:
        print(f"An unexpected error occurred during CSV reading: {e}")
        raise HTTPException(status_code=500, detail="Error processing data file.")
