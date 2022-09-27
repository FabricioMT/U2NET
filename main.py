import asyncio
import logging
import uvicorn
from app.utils import check_model

from api import app as app_fastapi
from cli import app as app_rocketry

class Server(uvicorn.Server):
    """Customized uvicorn.Server
    
    Uvicorn server overrides signals and we need to include
    Rocketry to the signals."""
    def handle_exit(self, sig: int, frame) -> None:
        app_rocketry.session.shut_down()
        return super().handle_exit(sig, frame)


async def main():
    #host="10.3.152.115"
    "Run Rocketry and FastAPI"
    server = Server(config=uvicorn.Config(app_fastapi, host="0.0.0.0", port=8000, workers=1, loop="asyncio"))

    api = asyncio.create_task(server.serve())
    sched = asyncio.create_task(app_rocketry.serve())

    await asyncio.wait([sched, api])

if __name__ == "__main__":
    # Print Rocketry's logs to terminal
    check_model()
    logger = logging.getLogger("rocketry.task")
    logger.addHandler(logging.StreamHandler())
    # Run both applications
    asyncio.run(main())