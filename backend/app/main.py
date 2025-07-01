import time
import datetime

from fastapi import FastAPI

from .schemas import HealthCheck

start_time = time.time()

description = """
board api serves as the backend to the board app, a dashboard for monitoring  energy consumption.
"""

app = FastAPI(
    title="board api",
    description=description,
    summary="A dashboard app for smart home energy usage monitoring.",
    version="0.0.1",
)


@app.get(
    "/health",
    summary="Check on the status of the API",
    response_model=HealthCheck,
    response_description="Some useful stats ",
)
def get_health():
    uptime = round(time.time() - start_time)
    return HealthCheck(uptime=str(datetime.timedelta(seconds=uptime)))
