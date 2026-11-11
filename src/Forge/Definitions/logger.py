from pathlib import Path
import logging.handlers
import os
import sys
from rich.logging import RichHandler 
import datetime
import logging
from enum import IntFlag

class LoggerService:    
    def _resource_path(self, relative_path):
        # If running as a PyInstaller EXE
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            # Running in normal Python
            # base_path = os.path.dirname(os.path.abspath(__file__))
            base_path = os.getcwd()
        return os.path.join(base_path, relative_path)

    def _get_log_path(self, name, start_time):
        _folder =self._get_current_folder()
        return Path(f"{_folder}/NVX_{name.upper()}_{start_time}.log")
    
    def _get_base_folder(self):
        return self._resource_path("Logs")
    
    def _get_current_folder(self):
        return self._resource_path(f"Logs/{datetime.datetime.strftime(datetime.datetime.now(), '%m-%d-%Y-%A')}")

    def _establish_folder(self, location):
        if not Path(location).is_dir():
            Path(location).mkdir()


    def _get_file_handler(self, log_data):
        self._establish_folder(self._get_base_folder()) 
        self._establish_folder(self._get_current_folder())
        log_path = self._get_log_path(log_data.name, log_data.start_time)
        _handler = logging.handlers.RotatingFileHandler(log_path, mode="w", backupCount=10000, delay=True)
        logging.handlers.RotatingFileHandler.doRollover(_handler) # Not sure what rollover is?
        format = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        _handler.setFormatter(format)
        _handler.setLevel(logging.INFO)
        return _handler

    def _get_rich_stream_handler(self):
        _handler = RichHandler(markup=True)
        _handler.setLevel(logging.INFO)
        return _handler
    
    def _get_stream_handler(self):
        _handler = logging.StreamHandler()
        format = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        _handler.setFormatter(format)
        _handler.setLevel(logging.INFO)
        return _handler


    def __init__(self, name:str, pretty:bool = False, file_only:bool = False):
        self.start_time = datetime.datetime.strftime(datetime.datetime.now(), "%m_%d_%Y_%H_%M_%S")
        self.logger = logging.getLogger(f"Log_{name.upper()}_{self.start_time}")
        self.logger.setLevel(logging.INFO)

        self.logger.addHandler(self._get_file_handler(self))
        if file_only:
            return
        if pretty:
            self.logger.addHandler(self._get_rich_stream_handler())
        else:
            self.logger.addHandler(self._get_stream_handler())

    def __call__(self)-> logging.Logger:
        return self.logger
    
class LoggerFlag(IntFlag):
    VERBOSE = 1
    PRETTY  = 2
    FILEONLY = 4

def get_logger(name:str, log_flag:LoggerFlag|int) -> LoggerService:
    """Get the Desired Logger Service

    Args:
        name (str): Name of the Log
        log_flag (LoggerFlag): 1 if Verbose, 2 if Pretty, 4 if File Only

    Returns:
        LoggerService: _description_
    """
    if isinstance(log_flag, int):
        log_flag = LoggerFlag(log_flag)
    return LoggerService(name, LoggerFlag.VERBOSE in log_flag, LoggerFlag.PRETTY in log_flag, LoggerFlag.FILEONLY in LoggerFlag)

