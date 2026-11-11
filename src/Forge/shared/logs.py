from Forge.Definitions.logger import get_logger, LoggerService
import logging
 
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    
class RenderLogs(Singleton):
    def __init__(self):
        if not hasattr(self, 'logger'):
            self.service: LoggerService = get_logger("RenderLogs")
            self.logger: logging.Logger = self.service()
            


class DebugLogs(Singleton):
    def __init__(self):
        if not hasattr(self, 'logger'):
            self.service: LoggerService = get_logger("DebugLogs")
            self.logger: logging.Logger = self.service()


class ErrorLogs(Singleton):
    def __init__(self):
        if not hasattr(self, 'logger'):
            self.service: LoggerService = get_logger("RenderLogs")
            self.logger: logging.Logger = self.service()


