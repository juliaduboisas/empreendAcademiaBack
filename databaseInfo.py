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
        mode = df["Objetivo"].mode()

        return mode
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Data file not found on the server.")
    except pd.errors.EmptyDataError:
        return []
    except Exception as e:
        print(f"An unexpected error occurred during CSV reading: {e}")
        raise HTTPException(status_code=500, detail="Error processing data file.")

    return

def getTotalOfStudentsPerUnit(unit: str):
    try:
        df = pd.read_csv("database.csv")
        studentsInUnit = df.loc[df["unidade"] == unit]
        totalStudents = studentsInUnit.shape[0]

        return totalStudents
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Data file not found on the server.")
    except pd.errors.EmptyDataError:
        return []
    except Exception as e:
        print(f"An unexpected error occurred during CSV reading: {e}")
        raise HTTPException(status_code=500, detail="Error processing data file.")

    return

def getStudentsMedianAge():
    try:
        df = pd.read_csv("database.csv")
        medianAge = df["Idade"].median()

        return medianAge
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Data file not found on the server.")
    except pd.errors.EmptyDataError:
        return []
    except Exception as e:
        print(f"An unexpected error occurred during CSV reading: {e}")
        raise HTTPException(status_code=500, detail="Error processing data file.")
    return

def getMedianTimeAsStudent():
    try:
        df = pd.read_csv("database.csv")
        medianTimeAsStudent = df["TempoComoAluno"].median()

        return medianTimeAsStudent
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Data file not found on the server.")
    except pd.errors.EmptyDataError:
        return []
    except Exception as e:
        print(f"An unexpected error occurred during CSV reading: {e}")
        raise HTTPException(status_code=500, detail="Error processing data file.")
    return

def getMedianAmountOfCheckInsPerWeek(week: int):
    try:
        df = pd.read_csv("database.csv")
        column_name = f"CheckinsSemana_{week}"
        checkInSum = df[column_name].sum()
        totalStudents = getTotalOfStudents()

        medianCheckins = float(checkInSum) / float(totalStudents)

        return medianCheckins
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Data file not found on the server.")
    except pd.errors.EmptyDataError:
        return []
    except Exception as e:
        print(f"An unexpected error occurred during CSV reading: {e}")
        raise HTTPException(status_code=500, detail="Error processing data file.")
    return

def getMedianAmountOfCheckIns():
    try:
        df = pd.read_csv("database.csv")
        medianCheckins = float(0)
        for i in range(1, 13):
            medianCheckins += getMedianAmountOfCheckInsPerWeek(i)

        return medianCheckins/float(12)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Data file not found on the server.")
    except pd.errors.EmptyDataError:
        return []
    except Exception as e:
        print(f"An unexpected error occurred during CSV reading: {e}")
        raise HTTPException(status_code=500, detail="Error processing data file.")
    return

def meanWeightVariation():
    try:
        df = pd.read_csv("database.csv")
        weightVariationSum = df["VariacaoPeso_2m"].sum()
        totalStudents = getTotalOfStudents()

        meanWeightVariation = float(weightVariationSum) / float(totalStudents)

        return meanWeightVariation
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Data file not found on the server.")
    except pd.errors.EmptyDataError:
        return []
    except Exception as e:
        print(f"An unexpected error occurred during CSV reading: {e}")
        raise HTTPException(status_code=500, detail="Error processing data file.")
    return

def meanFatVariation():
    try:
        df = pd.read_csv("database.csv")
        fatVariationSum = df["VariacaoGordura_2m"].sum()
        totalStudents = getTotalOfStudents()

        meanFatVariation = float(fatVariationSum) / float(totalStudents)

        return meanFatVariation
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Data file not found on the server.")
    except pd.errors.EmptyDataError:
        return []
    except Exception as e:
        print(f"An unexpected error occurred during CSV reading: {e}")
        raise HTTPException(status_code=500, detail="Error processing data file.")
    return

def meanLoadVariation():
    try:
        df = pd.read_csv("database.csv")
        loadVariationSum = df["VariacaoCarga_2m"].sum()
        totalStudents = getTotalOfStudents()

        meanLoadVariation = float(loadVariationSum) / float(totalStudents)

        return meanLoadVariation
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Data file not found on the server.")
    except pd.errors.EmptyDataError:
        return []
    except Exception as e:
        print(f"An unexpected error occurred during CSV reading: {e}")
        raise HTTPException(status_code=500, detail="Error processing data file.")
    return
