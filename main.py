from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import databaseInfo
from ias import iaInfo

app = FastAPI()

origins = [
    "http://localhost:5173",     
    "http://127.0.0.1:5173",      
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,    
    allow_credentials=True,
    allow_methods=["*"],      
    allow_headers=["*"],      
)

@app.get("/get-gym-name")
async def getGymName():
    return "AcadeMais"

@app.get("/get-student-info")
async def getStudentInfo(id: int):
    data = databaseInfo.getStudent(id);

    if data is None:
        raise HTTPException(status_code=404, detail=f"Student with ID '{id}' not found.")

    return data

@app.get("/get-students")
async def getStudents():
    data = databaseInfo.getAllStudents()

    if data is None:
        raise HTTPException(status_code=404, detail=f"Students not found.")

    return data

@app.get("/get-students-by-unit")
async def getStudentsByUnit(unit: str):
    data = databaseInfo.getStudentsByUnit(unit)

    if data is None:
        raise HTTPException(status_code=404, detail=f"Students not found.")

    return data

@app.get("/run-pipeline")
async def runPipeline():
    data = iaInfo.runPipeline()

    if data is None:
        raise HTTPException(status_code=404, detail=f"Pipeline not found.")
    return data

@app.get("/get-students-predictions")
async def getStudentsPredictions(modelName: str):
    data = iaInfo.getIndividualResults(modelName)

    if data is None:
        raise HTTPException(status_code=404, detail=f"Students not found.")
    return data

@app.get("/get-student-prediction")
async def getStudentPrediction(id: int, modelName: str):
    data = iaInfo.getStudentPrediction(id, modelName)

    if data is None:
        raise HTTPException(status_code=404, detail=f"Students not found.")
    return data

@app.get("/get-student-evasion-percentage")
async def getStudentPrediction(modelName: str):
    data = iaInfo.getStudentEvasionPredictionPercentage(modelName)

    if data is None:
        raise HTTPException(status_code=404, detail=f"Students not found.")
    return data