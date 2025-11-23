import papermill as pm

def runJupyterPipeline():
    inputNotebook = "ias/iaPipeline.ipynb"
    outputNotebook = "ias/iaPipelineOutput.ipynb"

    print(f"Executing notebook: {inputNotebook}...")

    pm.execute_notebook(
        inputNotebook,
        outputNotebook
    )

    print(f"Execution complete. Results saved to: {outputNotebook}")