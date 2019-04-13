import logging


class DecorateLogging(object):
    def __init__(self, *args):
        self.conditions = []
        for arg in args:
            self.conditions.append(arg)

    def __call__(self, func):
        def wrapper(*args):
            for cond in self.conditions:
                if cond[0] is 0:
                    self.log_item(cond[1], cond[2], cond[3])
            func(*args)
            for cond in self.conditions:
                if cond[0] is 1:
                    self.log_item(cond[1], cond[2], cond[3])
        return wrapper

    def log_item(self, name, msg_type, msg):
        if msg_type is "info":
            logging.getLogger(name).info(msg)
        elif msg_type is "warning":
            logging.getLogger(name).warning(msg)
        elif msg_type is "error":
            logging.getLogger(name).error(msg)
        else:
            raise ValueError
