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
    def assert_data(expect, actual):
        print "ExpectData:%s" % expect
        print "ActualData:%s" % actual

        if type(expect) is dict:
            Util.assert_dict(expect, actual)
        elif type(expect) is list:
            Util.assert_list(expect, actual)

    # 校验list数据类型
    @staticmethod
    def assert_list(expect, actual):
        print "Assert: Actual:%s == Expect:%s" % (actual, expect)
        flag = 0
        while flag < len(actual):
            if type(actual[flag]) is not list and type(actual[flag]) is not dict:
                if set(actual) >= set(expect):
                    assert True
                    break
            elif type(actual[flag]) is list:
                if Util.assert_list(expect[0], actual[flag]):
                    break
            elif type(actual[flag]) is dict:
                if Util._is_existing_dict(expect[0], actual[flag]):
                    break
            flag += 1
        if flag > len(actual) or len(actual) < len(expect):
            assert False

    # 校验dictionary数据类型
    @staticmethod
    def assert_dict(expect, actual):
        dictkey = expect.keys()
        for key in dictkey:
            expectVal = expect[key]
            actualVal = actual[key]
            if type(expectVal) is not list and type(expectVal) is not dict:
                print "Assert: Actual:%s == Expect:%s" % (
                    actualVal, expectVal)
                assert actualVal == expectVal
            elif type(expectVal) is dict:
                Util.assert_dict(expectVal, actualVal)
            elif type(expectVal) is list:
                Util.assert_list(expectVal, actualVal)

    # 校验list中是否存在期望数据
    @staticmethod
    def _is_existing_dict(expect, actual):
        isContains = True
        dictkey = expect.keys()
        for key in dictkey:
            expectVal = expect[key]
            actualVal = actual[key]
            if type(expectVal) is not list and type(expectVal) is not dict:
                if actualVal != expectVal:
                    isContains = False
            elif type(expectVal) is dict:
                Util._is_existing_dict(expectVal, actualVal)
            elif type(expectVal) is list:
                Util.assert_list(expectVal, actualVal)
        if isContains:
            return True
        else:
            return False

    # 通过key校验dict,用于值会变动的情况
    @staticmethod
    def assert_dict_is_contain_keys(keys, dic):
        if type(dic) is dict:
            for key in keys:
                try:
                    dic[key]
                except Exception as e:
                    print e
                    assert False
            assert True
        else:
            raise TypeError

    # 指定多层key
    @staticmethod
    def get_value(data, *keys):
        first_key = keys[0]
        if type(data) is dict:
            if first_key in data.keys():
                if len(keys) == 1:
                    return data[first_key]
                else:
                    return Util.get_value(data[first_key], *keys[1:])
            else:
                for key in data.keys():
                    value = Util.get_value(data[key], *keys)
                    if value:
                        return value
        elif type(data) is list:
            for valueData in data:
                value = Util.get_value(valueData, *keys)
                if value:
                    return value

    # sunyu add this method, it can be used to verify data type and its value.
    @staticmethod
    def assert_data_type_value(outputdata, responsedata):
        print "ExpectData:%s , ActualData:%s" % (outputdata, responsedata)
        #print type(outputdata), type(responsedata)
        if type(outputdata) is not unicode:
            assert type(outputdata) == type(responsedata)
        if type(outputdata) is dict:
            dictkeys = outputdata.keys()
            if len(dictkeys) == 0:
                assert type(outputdata) == type(responsedata)
            for k in dictkeys:
                if k in responsedata.keys():
                    # print k
                    try:
                        Util.assert_data_type_value(outputdata[k], responsedata[k])
                    except Exception as e:
                        print "Got exception"
                        print "Key: {0}, value: {1} and {2}".format(k, outputdata[k], responsedata[k])
                        raise (e)
                else:
                    print "Can't find key: " + k
                    assert False
        elif type(outputdata) is list:
            outputdata.sort()
            responsedata.sort()
            if len(outputdata) == 0:
                assert type(outputdata) == type(responsedata)
            if len(outputdata) > len(responsedata):
                print("Can not get enough response data")
                assert False
            i = 0
            while i < len(outputdata):
                if type(outputdata[i]) is unicode:
                    assert (outputdata[i] in responsedata)
                else:
                    Util.assert_data_type_value(outputdata[i], responsedata[i])
                i += 1
        elif type(outputdata) is unicode:
            nstr = outputdata.encode('unicode-escape').decode('string_escape')
            # when no need to check the value, let the output data to be response data
            if len(nstr) == 0 or nstr in ['int', 'float', 'int|float', "boolean"]:
                if nstr == "int":
                    assert int == type(responsedata)
                elif nstr == "float":
                    assert float == type(responsedata)
                elif nstr == "boolean":
                    assert bool == type(responsedata)
                elif nstr == 'int|float':
                    assert (type(responsedata) is int or type(responsedata) is float)
                responsedata = outputdata

        if type(outputdata) is not list and type(outputdata) is not dict:
            assert outputdata == responsedata

    @staticmethod
    def assert_data_type(outputdata, responsedata):
        print "ExpectData:%s , ActualData:%s" % (outputdata, responsedata)
        print type(outputdata), type(responsedata)
        if type(outputdata) is not unicode:
            assert type(outputdata) == type(responsedata)
        if type(outputdata) is dict:
            dictkeys = outputdata.keys()
            if len(dictkeys) == 0:
                assert type(outputdata) == type(responsedata)
            for k in dictkeys:
                if k in responsedata.keys():
                    print k
                    Util.assert_data_type(outputdata[k], responsedata[k])
                else:
                    print "Can't find key: " + k
                    assert False
        elif type(outputdata) is list:
            outputdata.sort()
            responsedata.sort()
            if len(outputdata) == 0:
                assert type(outputdata) == type(responsedata)
            if len(outputdata) > len(responsedata):
                print("Can not get enough response data")
                assert False
            i = 0
            while i < len(outputdata):
                Util.assert_data_type(outputdata[i], responsedata[i])
                i += 1
        elif type(outputdata) is unicode:
            nstr = outputdata.encode('unicode-escape').decode('string_escape')
            # when no need to check the value, let the output data to be response data
            if len(nstr) == 0 or nstr in ['int', 'float', 'int|float', "boolean"]:
                if nstr == "int":
                    assert int == type(responsedata)
                elif nstr == "float":
                    assert float == type(responsedata)
                elif nstr == "boolean":
                    assert bool == type(responsedata)
                elif nstr == 'int|float':
                    assert (type(responsedata) is int or type(responsedata) is float)
                responsedata = outputdata
        if type(outputdata) is not list and type(outputdata) is not dict:
            assert outputdata == responsedata
