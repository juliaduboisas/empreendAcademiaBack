from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
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

# GENERAL REQUESTS
@app.get("/get-gym-name")
async def getGymName():
    return "AcadeMais"

# DATABASE REQUESTS
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

@app.get("/get-statistics/number-of-students")
async def getNumberOfStudents():
    data = databaseInfo.getTotalOfStudents()

    if data is None:
        raise HTTPException(status_code=404, detail=f"Students not found.")

    return data

@app.get("/get-statistics/objective-mode")
async def getMostCommonObjective():
    data = databaseInfo.getObjetiveMode()

    if data is None:
        raise HTTPException(status_code=404, detail=f"Students not found.")

    return data

@app.get("/get-statistics/number-of-students-per-unit")
async def getNumberOfStudentsPerUnit():
    data = databaseInfo.getTotalOfStudentsPerUnit()

    if data is None:
        raise HTTPException(status_code=404, detail=f"Students not found.")

    return data


@app.get("/get-statistics/average-age")
async def getAverageAge():
    data = databaseInfo.getStudentsAverageAge()

    if data is None:
        raise HTTPException(status_code=404, detail=f"Students not found.")
    return data

@app.get("/get-statistics/average-time-as-student")
async def getAverageTimeAsStudent():
    data = databaseInfo.getAverageTimeAsStudent()

    if data is None:
        raise HTTPException(status_code=404, detail=f"Students not found.")
    return data

@app.get("/get-statistics/average-checkins")
async def getAverageCheckins(week: int):
    if week == 0 or week > 12:
        data = databaseInfo.getAverageAmountOfCheckIns()
    else:
        data = databaseInfo.getAverageAmountOfCheckInsPerWeek(week)

    if data is None:
        raise HTTPException(status_code=404, detail=f"Students not found.")
    return data

@app.get("/get-statistics/average-weight-variation")
async def getAverageWeightVariation():
    data = databaseInfo.getAverageStudentWeightVariation()

    if data is None:
        raise HTTPException(status_code=404, detail=f"Students not found.")
    return data

@app.get("/get-statistics/average-body-fat-variation")
async def getAverageFatVariation():
    data = databaseInfo.getAverageStudentFatVariation()

    if data is None:
        raise HTTPException(status_code=404, detail=f"Students not found.")
    return data

@app.get("/get-statistics/average-load-variation")
async def getAverageLoadVariation():
    data = databaseInfo.getAverageStudentLoadVariation()

    if data is None:
        raise HTTPException(status_code=404, detail=f"Students not found.")
    return data


@app.get("/get-students-by-unit")
async def getStudentsByUnit(unit: str):
    data = databaseInfo.getStudentsByUnit(unit)

    if data is None:
        raise HTTPException(status_code=404, detail=f"Students not found.")

    return data

# AI-RELATED REQUESTS
@app.get("/get-students-predictions")
async def getStudentsPredictions():
    data = iaInfo.getIndividualResults()

    if data is None:
        raise HTTPException(status_code=404, detail=f"Students not found.")
    return data

@app.get("/get-student-prediction")
async def getStudentPrediction(id: int):
    data = iaInfo.getStudentPrediction(id)

    if data is None:
        raise HTTPException(status_code=404, detail=f"Students not found.")
    return data

@app.get("/get-student-evasion-percentage")
async def getStudentPrediction():
    data = iaInfo.getStudentEvasionPredictionPercentage()

    if data is None:
        raise HTTPException(status_code=404, detail=f"Students not found.")
    return data

@app.get("/get-student-evasion-percentage-per-unit")
async def getStudentEvasionPercentagePerUnit(unit: str):
    data = iaInfo.getPredictionPercentagePerUnit(unit)

    if data is None:
        raise HTTPException(status_code=404, detail=f"Students not found.")
    return data

@app.post("/run-pipeline")
async def runPipeline():
    data = iaInfo.runAIPipeline()
    return JSONResponse(status_code=200, content={"message": "Pipeline executed successfully"})

@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Please upload a CSV file."
        )

    try:
        await databaseInfo.saveFile(file)

        await runPipeline()

        return JSONResponse(status_code=200, content={"message": "File uploaded and AI processed successfully"})
    except Exception as e:
        # Catch errors during reading/processing
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
