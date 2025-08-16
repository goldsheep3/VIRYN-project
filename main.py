import uvicorn

from api.app import app
from core.logging import Logger

API_HOST = "127.0.0.1"
API_PORT = 8000


class MainLogger(Logger):
    def __init__(self):
        super().__init__('main')


logger = MainLogger()

if __name__ == '__main__':
    [logger.info(line) for line in [
        "                                         ",
        " ======================================= ",
        " ██╗   ██╗██╗██████╗ ██╗   ██╗███╗   ██╗ ",
        " ██║   ██║██║██╔══██╗╚██╗ ██╔╝████╗  ██║ ",
        " ██║   ██║██║██████╔╝ ╚████╔╝ ██╔██╗ ██║ ",
        " ╚██╗ ██╔╝██║██╔══██╗  ╚██╔╝  ██║╚██╗██║ ",
        "  ╚████╔╝ ██║██║  ██║   ██║   ██║ ╚████║ ",
        " ======================================= ",
        "                                         ",
    ]]

    uvicorn.run(app, host=API_HOST, port=API_PORT)
