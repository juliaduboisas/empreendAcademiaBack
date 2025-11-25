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

@app.get("/get-statistics/objetive-mode")
async def getMostCommonObjective():
    data = databaseInfo.getObjetiveMode()

    if data is None:
        raise HTTPException(status_code=404, detail=f"Students not found.")

    return data

@app.get("/get-statistics/number-of-students-per-unit")
async def getNumberOfStudentsPerUnit(unit: str):
    data = databaseInfo.getTotalOfStudentsPerUnit(unit)

    if data is None:
        raise HTTPException(status_code=404, detail=f"Students not found.")

    return data


@app.get("/get-statistics/median-age")
async def getMedianAge():
    data = databaseInfo.getStudentsMedianAge()

    if data is None:
        raise HTTPException(status_code=404, detail=f"Students not found.")
    return data

@app.get("/get-statistics/median-time-as-student")
async def getMedianTimeAsStudent():
    data = databaseInfo.getMedianTimeAsStudent()

    if data is None:
        raise HTTPException(status_code=404, detail=f"Students not found.")
    return data

@app.get("/get-statistics/median-checkins")
async def getMedianCheckins(week: int):
    if week == 0 or week > 12:
        data = databaseInfo.getMedianAmountOfCheckIns()
    else:
        data = databaseInfo.getMedianAmountOfCheckInsPerWeek(week)

    if data is None:
        raise HTTPException(status_code=404, detail=f"Students not found.")
    return data

@app.get("/get-statistics/mean-weight-variation")
async def getMeanWeightVariation():
    data = databaseInfo.meanWeightVariation()

    if data is None:
        raise HTTPException(status_code=404, detail=f"Students not found.")
    return data

@app.get("/get-statistics/mean-fat-variation")
async def getMeanFatVariation():
    data = databaseInfo.meanFatVariation()

    if data is None:
        raise HTTPException(status_code=404, detail=f"Students not found.")
    return data

@app.get("/get-statistics/mean-load-variation")
async def getMeanLoadVariation():
    data = databaseInfo.meanLoadVariation()

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
