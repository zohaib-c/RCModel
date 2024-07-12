import subprocess

def runOpenDC(scenarioPath):

    opendc_run = f"OpenDC/scenario/bin/scenario --scenario-path {scenarioPath}"

    subprocess.run(opendc_run, shell=True, check=True)