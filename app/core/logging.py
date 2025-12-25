import logging
import sys
import inspect
import os
from typing import Optional

class Logger:
    _loggers = {}
    
    def __init__(self, level: int = logging.INFO):
        self.level = level
        self._setup_root_logger()
    
    def _setup_root_logger(self):
        root_logger = logging.getLogger()
        root_logger.setLevel(self.level)
        
        if not root_logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter(
                '%(levelname)s - %(asctime)s - %(filename)s:%(lineno)d - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            handler.setFormatter(formatter)
            root_logger.addHandler(handler)
    
    def _get_caller_info(self) -> tuple[str, int]:
        """Get the filename and line number of the actual caller"""
        frame = inspect.currentframe()
        try:
            # Skip the current frame and the logger method frame
            frame = frame.f_back.f_back
            while frame:
                if frame.f_code.co_filename != __file__:
                    filename = os.path.basename(frame.f_code.co_filename)
                    line_no = frame.f_lineno
                    return filename, line_no
                frame = frame.f_back
        finally:
            del frame
        return "unknown", 0
    
    def _get_logger(self) -> logging.Logger:
        caller_filename, _ = self._get_caller_info()
        
        if caller_filename not in self._loggers:
            self._loggers[caller_filename] = logging.getLogger(caller_filename)
        
        return self._loggers[caller_filename]
    
    def _log_with_caller_info(self, level: int, message: str, *args, **kwargs):
        """Log message with correct caller information"""
        logger = self._get_logger()
        filename, line_no = self._get_caller_info()
        
        # Create a custom log record with correct file info
        if logger.isEnabledFor(level):
            record = logger.makeRecord(
                logger.name, level, filename, line_no, message, args, None
            )
            logger.handle(record)
    
    def debug(self, message: str, *args, **kwargs):
        self._log_with_caller_info(logging.DEBUG, message, *args, **kwargs)
    
    def info(self, message: str, *args, **kwargs):
        self._log_with_caller_info(logging.INFO, message, *args, **kwargs)
    
    def warning(self, message: str, *args, **kwargs):
        self._log_with_caller_info(logging.WARNING, message, *args, **kwargs)
    
    def error(self, message: str, *args, **kwargs):
        self._log_with_caller_info(logging.ERROR, message, *args, **kwargs)
    
    def critical(self, message: str, *args, **kwargs):
        self._log_with_caller_info(logging.CRITICAL, message, *args, **kwargs)

# Create the logger instance
logger = Logger()