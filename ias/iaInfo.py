from ias.modelResults import modelResults
from fastapi import HTTPException

import ias.iaPipeline as pipe
import pandas as pd

class mockAI():
    results: modelResults
    results = []
    bestResult: modelResults

    def runPipeline():
        this.results = pipe.runAIPipeline()
        return results

    def findBestResults():
        return

    def getIndividualResults(modelName: str):
        try:
            dfPredictions = pd.read_csv("predictions/" + modelName + "_predictions.csv")
            dfStudents = pd.read_csv("database.csv")

            dfIndividualResults = pd.merge(dfPredictions,
                                           dfStudents,
                                           left_on="Original_Synthetic_Row_ID",
                                           right_on="aluno_id",
                                           how="inner")

            columnName = modelName.replace("_", " ")

            columnsToKeep = ["aluno_id", "Nome", "Objetivo", "unidade", columnName + "_Prediction"]
            columnsToDrop = dfIndividualResults.columns.difference(columnsToKeep)

            dfIndividualResultsFiltered = dfIndividualResults.drop(columns=columnsToDrop, axis=1)

            results = dfIndividualResultsFiltered.to_dict('records')

            return results

        except FileNotFoundError:
            raise HTTPException(status_code=500, detail="Data file not found on the server.")
        except pd.errors.EmptyDataError:
            return []
        except Exception as e:
            print(f"An unexpected error occurred during CSV reading: {e}")
            raise HTTPException(status_code=500, detail="Error processing data file.")


