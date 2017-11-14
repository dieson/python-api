# coding= utf-8
import json
import platform
import os
from Utils.Util import Util


class JSONDriver(object):
    def __init__(self, file_name):
        self.file_path = os.path.join(Util.get_project_path(), "TestData", file_name)
        self.data = open(self.file_path, 'r')
        self.table = json.loads(self.data.read())
        self.data.close()

        # Get the number of case.
        self.length = self.table.__len__()
        # The current number.
        self.curNO = 0
        # The dictionary key.
        self.key = self.table.keys()

    def next(self, apitype):
        data = []
        while self._has_next():
            if apitype in self.key[self.curNO]:
                data.append(self.table[self.key[self.curNO]])
            self.curNO += 1
        if not self._has_next():
            self.curNO = 0
        return data

    def _has_next(self):
        if self.length == 0 or self.length <= self.curNO:
            return False
        else:
            return True

    # 写入json文件，不指定具体数据
    def write(self, value, baseKey, key):

        baseKey = "%s_0%d" % (baseKey, self.curNO + 1)
        self.write_specfic_data(value, baseKey, key)

    def write_specfic_data(self, value, baseKey, key):
        self.table[baseKey] = self._change_value(self.table[baseKey], value, key)
        os.remove(self.file_path)
        fb = open(self.file_path, 'w')
        fb.write(json.dumps(self.table, ensure_ascii=False, indent=2).encode("utf-8"))
        fb.close()

    # 修改json文件的值,提供write方法调用
    def _change_value(self, data, value, key):
        dictkey = data.keys()
        if key in dictkey:
            data[key] = value
        for dkey in dictkey:
            if type(data[dkey]) is dict:
                self._change_value(data[dkey], value, key)
            elif type(data[dkey]) is list:
                if type(data[dkey][0]) is dict:
                    for listData in data[dkey]:
                        self._change_value(listData, value, key)
        return data
