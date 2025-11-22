import pandas as pd

def getStudent(id: int):
    try:
        df = pd.read_csv("base_academia_3m_completa.csv")
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