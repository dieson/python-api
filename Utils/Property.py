# encoding=utf-8
import os
import configparser as cparser

from Utils.Util import Util


class Property(object):
    # 获取config.ini
    @staticmethod
    def get_conf():
        return Property.get_file("Config", "config.ini")


    # 获取property文件
    @staticmethod
    def get_file(*path):
        filePath = Util.get_project_path()
        for value in path:
            filePath = os.path.join(filePath, value)
        cf = cparser.ConfigParser()
        cf.read(filePath)
        return cf
