from core.logging import Logger


class ApiLogger(Logger):
    def __init__(self):
        super().__init__('api')
