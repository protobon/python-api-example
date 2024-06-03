from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import uvicorn
import time
from os import getenv

from app.router.api import api_router
from app.common.constants import Env


def run():
    try:
        app = FastAPI(
            title=getenv(Env.APP.name)
        )

        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        app.include_router(api_router)

        @app.middleware("http")
        async def add_process_time_header(request, call_next):
            start_time = time.time()
            response = await call_next(request)
            process_time = time.time() - start_time
            response.headers["X-Process-Time"] = str(f'{process_time:0.4f} sec')
            return response

        uvicorn.run(app,
                    host=getenv(Env.APP.host),
                    port=int(getenv(Env.APP.port)),
                    log_level="info")
    except Exception as e:
        raise e
