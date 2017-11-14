# encoding=utf-8
# @Time    : 2017/10/26 10:32
# @Author  : Zuo Ran
# @File    : Util.py
import os


class Util(object):
    # 获取当前项目路径
    @staticmethod
    def get_project_path():
        path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        return path

    # 校验返回数据
    @staticmethod
    def assert_data(outputdata, responsedata):
        dictkey = outputdata.keys()
        for key in dictkey:
            ouputval = outputdata[key]
            responseval = responsedata[key]
            if type(ouputval) is not list and type(ouputval) is not dict:
                print "Assert: Acutal:%s == Expect:%s" % (
                    responseval, ouputval)
                assert responseval == ouputval
            elif type(ouputval) is dict:
                Util.assert_data(ouputval, responseval)
            elif type(ouputval) is list:
                Util.assert_list(ouputval, responseval)

    # 校验list数据类型
    @staticmethod
    def assert_list(expect, actual):
        print "Assert: Acutal:%s == Expect:%s" % (
            actual, expect)
        flag = 0
        while flag < len(actual):
            if type(actual[flag]) is not list and type(actual[flag]) is not dict:
                if set(actual) >= set(expect):
                    print "Assert: Acutal:%s == Expect:%s" % (
                        actual, expect)
                    assert True
                    break
            elif type(actual[flag]) is dict:
                if Util.assert_dict(expect[0], actual[flag]):
                    assert True
                    break
                else:
                    break
            elif type(actual[flag]) is list:
                Util.assert_list(expect[0], actual[flag])
            flag += 1
        if flag >= len(actual):
            print "Assert: Acutal:%s == Expect:%s" % (
                actual, expect)
            assert False

    # 校验dictionary数据类型
    @staticmethod
    def assert_dict(outputdata, responsedata):
        flag = True
        dictkey = outputdata.keys()
        for key in dictkey:
            ouputval = outputdata[key]
            responseval = responsedata[key]
            if type(ouputval) is not list and type(ouputval) is not dict:
                if responseval == ouputval:
                    print "Assert: Acutal:%s == Expect:%s" % (
                        responseval, ouputval)
                    flag = True
                else:
                    flag = False
            elif type(ouputval) is list:
                if set(responseval) >= set(ouputval):
                    print "Assert: Acutal:%s == Expect:%s" % (
                        responseval, ouputval)
                    flag = True
                else:
                    flag = False
        return flag

    # 通过key校验dict,用于值会变动的情况
    @staticmethod
    def assert_dict_is_contain_keys(keys, dic):
        if type(dic) is dict:
            for key in keys:
                try:
                    dic[key]
                except Exception as e:
                    assert False
            assert True

        else:
            raise "parame type is error !"

    @staticmethod
    def get_dic_value(data, key):
        dictkey = data.keys()
        if key in dictkey:
            return data[key]
        else:
            for k in dictkey:
                if type(data[k]) is dict:
                    Util.get_dic_value(data[k], key)
                elif type(data[k]) is list:
                    for listData in data[k]:
                        Util.get_dic_value(listData, key)

    # sunyu add this method, it can be used to verify data type and its value.
    @staticmethod
    def assert_data_type_value(outputdata, responsedata):

        if type(outputdata) is not unicode:
            assert type(outputdata) == type(responsedata)

        if type(outputdata) is dict:
            dictkeys = outputdata.keys()
            for k in dictkeys:
                # print(k)
                if responsedata.has_key(k):
                    Util.assert_data_type_value(outputdata[k], responsedata[k])
                else:
                    print "Can't find key: " + k
                    assert False
        elif type(outputdata) is list:
            outputdata.sort()
            responsedata.sort()

            i = 0
            while i < len(outputdata):
                Util.assert_data_type_value(outputdata[i], responsedata[i])
                i += 1
        elif type(outputdata) is unicode:
            nstr = outputdata.encode('unicode-escape').decode('string_escape')
            # when no need to check the value, let the output data to be response data
            if len(nstr) == 0 or nstr in ['int', 'float', 'int|float', "boolean"]:
                if nstr == "int":
                    assert type(1) == type(responsedata)
                elif nstr == "float":
                    assert type(1.0) == type(responsedata)
                elif nstr == "boolean":
                    assert type(True) == type(responsedata)
                elif nstr == 'int|float':
                    assert(type(responsedata) is type(1) or type(responsedata) is type(1.0))
                responsedata = outputdata

        if type(outputdata) is not list and type(outputdata) is not dict:
            if type(outputdata) is unicode and len(outputdata) == 0:
                print("\"\"")
            else:
                print(outputdata)
            # print(responsedata)
            assert outputdata == responsedata
