# -*- coding: utf-8 -*-
#
# 使用测试
# Author: alex
# Created Time: 2018年04月02日 星期一 14时53分50秒
from flask import request
from fireRest import API, app, APIException, ErrCodeBase


class Example:
    def hello(self, name='world'):
        """这是函数的注释"""
        if name == 'exception':
            # 可以简单的抛出异常（此时错误码为1）
            raise Exception('演示异常输出')
        # 可以返回字典
        return {
            "msg": 'Hello {name} in Example!'.format(name=name)
        }


class Example2:
    def hello(self, name='world'):
        """这是函数的注释"""
        if name == 'exception':
            # 可以使用自定义的错误码
            raise APIException('演示错误处理的使用方式', code=10)
        # 可以返回列表
        return ['Hello {name} in Example2!'.format(name=name)]


def hello(name='world'):
    """这是函数的注释"""
    if name == 'exception':
        # 可以使用系统定义的错误码
        raise APIException('演示错误处理的使用方式',
                           code=ErrCodeBase.err_param)
    # 可以返回简单类型，如字符串等
    return 'Hello {name} in func!'.format(name=name)


def upload():
    """上传文件
    注意：上传文件时，不能在函数名upload增加参数，否则会报错
    """
    ufile = request.files.get('file')
    return {
        "file": ufile.filename,
    }


if __name__ == '__main__':
    API(Example)
    print("==> curl -XPOST localhost:5000/Example/hello -d '{\"name\": \"IBBD\"}'")

    API(Example2)
    print("==> curl -XPOST localhost:5000/Example2/hello -d '{\"name\": \"IBBD\"}'")

    API(hello)
    print("==> curl -XPOST localhost:5000/hello -d '{\"name\": \"IBBD\"}'")

    API(upload)
    print("==> curl -XPOST localhost:5000/upload -F 'file=@README.md'")

    app.run(debug=True)
