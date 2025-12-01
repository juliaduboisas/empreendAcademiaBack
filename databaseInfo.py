import pandas as pd
from fastapi import HTTPException, File

# STUDENT RELATED
def getStudent(id: int):
    try:
        df = pd.read_csv("database.csv")
        result = df.loc[df["aluno_id"] == id]

        if not result.empty:
            return result.iloc[0].to_dict()
        else:
            return None;

    except FileNotFoundError:
        print(f"Error: Database file not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def getAllStudents():
    try:
        df = pd.read_csv("database.csv")
        allStudents = df.to_dict('records')

        return allStudents

    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Data file not found on the server.")
    except pd.errors.EmptyDataError:
        return []
    except Exception as e:
        print(f"An unexpected error occurred during CSV reading: {e}")
        raise HTTPException(status_code=500, detail="Error processing data file.")

def getStudentsByUnit(unit: str):
    try:
        df = pd.read_csv("database.csv")
        studentsInUnit = df.loc[df["unidade"] == unit]

        return studentsInUnit.to_dict('records')

    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Data file not found on the server.")
    except pd.errors.EmptyDataError:
        return []
    except Exception as e:
        print(f"An unexpected error occurred during CSV reading: {e}")
        raise HTTPException(status_code=500, detail="Error processing data file.")

# DATABASE RELATED
async def saveFile(file: File()):
    filePath = "database.csv"
    contents = await file.read()

    try:
        with open(filePath, 'wb') as f:
            f.write(contents)

    except Exception as e:
        print(f"An error occurred: {e}")

    return

# STATISTICS
def getTotalOfStudents():
    try:
        df = pd.read_csv("database.csv")
        totalStudents = df.shape[0]

        return totalStudents

    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Data file not found on the server.")
    except pd.errors.EmptyDataError:
        return []
    except Exception as e:
        print(f"An unexpected error occurred during CSV reading: {e}")
        raise HTTPException(status_code=500, detail="Error processing data file.")

    return

def getObjetiveMode():
    try:
        df = pd.read_csv("database.csv")
        modeSeries = df["Objetivo"].mode()

        if not modeSeries.empty:
            return modeSeries.iloc[0].capitalize()
        return None
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Data file not found on the server.")
    except pd.errors.EmptyDataError:
        return []
    except Exception as e:
        print(f"An unexpected error occurred during CSV reading: {e}")
        raise HTTPException(status_code=500, detail="Error processing data file.")

    return

def getTotalOfStudentsPerUnit():
    try:
        df = pd.read_csv("database.csv")
        studentsInUnit = df["unidade"].value_counts()

        return studentsInUnit.to_dict()
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Data file not found on the server.")
    except pd.errors.EmptyDataError:
        return 0
    except Exception as e:
        print(f"An unexpected error occurred during CSV reading: {e}")
        raise HTTPException(status_code=500, detail="Error processing data file.")

    return

def getStudentsAverageAge():
    try:
        df = pd.read_csv("database.csv")
        averageAge = df["Idade"].mean()

        return averageAge
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Data file not found on the server.")
    except pd.errors.EmptyDataError:
        return []
    except Exception as e:
        print(f"An unexpected error occurred during CSV reading: {e}")
        raise HTTPException(status_code=500, detail="Error processing data file.")
    return

def getAverageTimeAsStudent():
    try:
        df = pd.read_csv("database.csv")
        averageTimeAsStudent = df["TempoComoAluno"].mean()

        return averageTimeAsStudent
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Data file not found on the server.")
    except pd.errors.EmptyDataError:
        return []
    except Exception as e:
        print(f"An unexpected error occurred during CSV reading: {e}")
        raise HTTPException(status_code=500, detail="Error processing data file.")
    return

def getAverageAmountOfCheckInsPerWeek(week: int):
    try:
        df = pd.read_csv("database.csv")
        column_name = f"CheckinsSemana_{week}"
        checkInSum = df[column_name].sum()
        totalStudents = getTotalOfStudents()

        averageCheckins = float(checkInSum) / float(totalStudents)

        return averageCheckins
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Data file not found on the server.")
    except pd.errors.EmptyDataError:
        return []
    except Exception as e:
        print(f"An unexpected error occurred during CSV reading: {e}")
        raise HTTPException(status_code=500, detail="Error processing data file.")
    return

def getAverageAmountOfCheckIns():
    try:
        df = pd.read_csv("database.csv")
        averageCheckins = float(0)
        for i in range(1, 13):
            averageCheckins += getAverageAmountOfCheckInsPerWeek(i)

        return averageCheckins/float(12)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Data file not found on the server.")
    except pd.errors.EmptyDataError:
        return []
    except Exception as e:
        print(f"An unexpected error occurred during CSV reading: {e}")
        raise HTTPException(status_code=500, detail="Error processing data file.")
    return

def getAverageStudentWeightVariation():
    try:
        df = pd.read_csv("database.csv")
        weightVariationSum = df["VariacaoPeso_2m"].sum()
        totalStudents = getTotalOfStudents()

        averageWeightVariation = float(weightVariationSum) / float(totalStudents)

        return averageWeightVariation
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Data file not found on the server.")
    except pd.errors.EmptyDataError:
        return []
    except Exception as e:
        print(f"An unexpected error occurred during CSV reading: {e}")
        raise HTTPException(status_code=500, detail="Error processing data file.")
    return

def getAverageStudentFatVariation():
    try:
        df = pd.read_csv("database.csv")
        fatVariationSum = df["VariacaoGordura_2m"].sum()
        totalStudents = getTotalOfStudents()

        averageFatVariation = float(fatVariationSum) / float(totalStudents)

        return averageFatVariation
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Data file not found on the server.")
    except pd.errors.EmptyDataError:
        return []
    except Exception as e:
        print(f"An unexpected error occurred during CSV reading: {e}")
        raise HTTPException(status_code=500, detail="Error processing data file.")
    return

def getAverageStudentLoadVariation():
    try:
        df = pd.read_csv("database.csv")
        loadVariationSum = df["VariacaoCarga_2m"].sum()
        totalStudents = getTotalOfStudents()

        averageLoadVariation = float(loadVariationSum) / float(totalStudents)

        return averageLoadVariation
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Data file not found on the server.")
    except pd.errors.EmptyDataError:
        return []
    except Exception as e:
        print(f"An unexpected error occurred during CSV reading: {e}")
        raise HTTPException(status_code=500, detail="Error processing data file.")
    return
