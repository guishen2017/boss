#-*- coding:utf-8 -*-
from datetime import datetime, timedelta


class ProxyModel(object):
    def __init__(self, data):
        self.ip = data['ip']
        self.port = data['port']
        self.proxy = "https://{}:{}".format(self.ip, self.port)
        self.is_block = False
        expire_str = data['expire_time']
        year, month, day = expire_str.split(" ")[0].split("-")
        hour, minute, second = expire_str.split(" ")[1].split(":")
        self.expire_time = datetime(int(year), int(month),int(day), int(hour), int(minute), int(second))

    @property
    def is_expiring(self):
        now = datetime.now()
        if (self.expire_time - now)<timedelta(seconds=5):
            return True
        else:
            return False


