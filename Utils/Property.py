# encoding=utf-8
import os
import configparser as cparser

from Utils.Util import Util


class Property(object):
    # 获取config.ini
    @staticmethod
    def get_conf():
        return Property.get_file("Config", "config.ini")

    # Add a method to update a value in config.ini
    @staticmethod
    def write_conf(section, key, value):
        path = ["Config", "config.ini"]
        file_path = Util.get_project_path()
        for item in path:
            file_path = os.path.join(file_path, item)
        cf = cparser.ConfigParser()
        cf.read(file_path)
        cf.set(section, key, value)
        cf.write(open(file_path, "w"))


  # 获取property文件
    @staticmethod
    def get_file(*path):
        filePath = Util.get_project_path()
        for value in path:
            filePath = os.path.join(filePath, value)
        cf = cparser.ConfigParser()
        cf.read(filePath)
        return cf


