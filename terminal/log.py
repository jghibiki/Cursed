import sys
import logging

class LogWriter:
    loggers = {}
    def __init__(self, logger_name, log_file_name, default_level=logging.DEBUG, log_level=logging.INFO):
        self.logger = logging.getLogger(logger_name)
        self.default_level = default_level

        ch = logging.FileHandler(log_file_name)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
        self.logger.setLevel(log_level)

        LogWriter.loggers[logger_name] = self

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.default_level, line.rstrip())

    def log(self, message, level=None):
        lvl = level if level is not None else self.default_level
        self.logger.log(lvl, message)

    def debug(self, message):
        self.log(message, logging.DEBUG)

    def info(self, message):
        self.log(message, logging.INFO)

    def warn(self, message):
        self.log(message, logging.WARN)

    def error(self, message):
        self.log(message, logging.ERROR)

    def getLogger(self, logger_name):
        return LogWriter.loggers[logger_name]


logger = LogWriter("cursed_log", "default.log", log_level=logging.INFO)

