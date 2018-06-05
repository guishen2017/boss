#-*- coding:utf-8 -*-
import hashlib

def get_md5(url):
    m = hashlib.md5()
    m.update(url.encode("utf-8"))
    return m.hexdigest()

