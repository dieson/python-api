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
    def write(self, value, baseKey, *key):
        baseKey = "%s%d" % (baseKey, self.curNO + 1)
        self.write_specfic_data(value, baseKey, *key)

    def write_specfic_data(self, value, baseKey, *key):
        self.table[baseKey] = self._change_value(self.table[baseKey], value, *key)
        os.remove(self.file_path)
        fb = open(self.file_path, 'w')
        fb.write(json.dumps(self.table, ensure_ascii=False, indent=2).encode("utf-8"))
        fb.close()

    def add(self, value, baseKey, *keys):
        baseKey = "%s%d" % (baseKey, self.curNO + 1)
        self.add_specfic_data(value, baseKey, *keys)

    def add_specfic_data(self, value, baseKey, *keys):
        self.table[baseKey] = self._add_value(self.table[baseKey], value, *keys)
        os.remove(self.file_path)
        fb = open(self.file_path, 'w')
        fb.write(json.dumps(self.table, ensure_ascii=False, indent=2).encode("utf-8"))
        fb.close()

    def _add_value(self, data, value, *keys):
        if len(keys) == 1:
            data[keys[0]] = value
        else:
            self._add_value(data[keys[0]], value, *keys[1:])
        return data

    def delete(self, baseKey, *keys):
        baseKey = "%s%d" % (baseKey, self.curNO + 1)
        self.delete_specfic_data(baseKey, *keys)

    def delete_specfic_data(self, baseKey, *keys):
        self.table[baseKey] = self._delete_value(self.table[baseKey], *keys)
        os.remove(self.file_path)
        fb = open(self.file_path, 'w')
        fb.write(json.dumps(self.table, ensure_ascii=False, indent=2).encode("utf-8"))
        fb.close()

    def _delete_value(self, data, *keys):
        if len(keys) == 1:
            try:
                del data[keys[0]]
            except KeyError:
                pass
        else:
            self._delete_value(data[keys[0]], *keys[1:])
        return data

    # 修改json文件的值,提供write方法调用
    def _change_value(self, data, value, *keys):
        firstKey = keys[0]
        if firstKey in data.keys():
            if len(keys) == 1:
                if type(data[firstKey]) is list:
                    if type(value) is list:
                        data[firstKey] = value
                    elif value is None:
                        data[firstKey] = value
                    elif type(value) is not list:
                        del data[firstKey][:]
                        data[firstKey].append(value)
                elif type(data[firstKey]) is dict:
                    data[firstKey].clear()
                    data[firstKey].update(value)
                elif type(data[firstKey]) is not list and type(data[firstKey]) is not dict:
                    data[firstKey] = value
            else:
                self._change_value(data[firstKey], value, *keys[1:])
        else:
            for dataKey in data.keys():
                if type(data[dataKey]) is dict:
                    # if firstKey in data[dataKey].keys():
                    self._change_value(data[dataKey], value, *keys)
                elif type(data[dataKey]) is list:
                    for ar in data[dataKey]:
                        if type(ar) is dict:
                            self._change_value(ar, value, *keys)
        return data
