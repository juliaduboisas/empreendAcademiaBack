import pandas as pd

def getStudent(id: int):
    try:
        df = pd.read_csv("database.csv")
        result = df.loc[df["aluno_id"] == id]

        if not result.empty:
            return result.iloc[0].to_dict()
        else:
            return None;

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
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