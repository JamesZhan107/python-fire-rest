# -*- coding: utf-8 -*-
#
# 包装API
# Author: alex
# Created Time: 2018年04月02日 星期一 14时34分24秒
import logging
import types
from flask import Flask, jsonify
from flask_restful import request

__all__ = ['API', 'run', 'output_json']

logger = logging.getLogger()
app = Flask(__name__)

# ctroller action list
action_list = {}

config = {
    "debug": False
}


def API(ctrl):
    """将函数或者类转化为添加Restful API
    Args:
        ctrl function|class 需要转化的函数或者类
    """
    global action_list

    ctrl_name = ctrl.__name__
    if type(ctrl) is types.FunctionType:  # 函数
        key = (ctrl_name)
        action_list[key] = ctrl
        return

    logger.warning(ctrl_name)
    obj = ctrl()

    for func in ctrl.__dict__:
        if func[:1] == "_":
            continue

        key = (ctrl_name, func)
        action_list[key] = getattr(obj, func)


def run(port=20920, debug=False):
    """运行服务"""
    global config
    config["debug"] = debug
    app.run(port=port, debug=debug)
    app.logger.addHandler(logger)


def output_json(data, code=0, messages=None):
    """以json结构返回数据"""
    return jsonify({
        "code": code,
        "messages": messages,
        "data": data
    })


@app.route('/<string:func>', methods=['POST'])
def restFunc(func):
    """函数API入口"""
    params = request.get_json(force=True, silent=True)
    if config["debug"]:
        logger.warning("function: " + func)
        logger.warning(len(action_list))
        logger.warning(params)

    key = (func)
    if key in action_list:
        if params:
            return action_list[key](**request.json)
        return action_list[key]()

    return "not found!", 404


@app.route('/<string:ctrl>/<string:action>', methods=['POST'])
def restClass(ctrl, action):
    """类API入口"""
    params = request.get_json(force=True, silent=True)
    if config["debug"]:
        logger.warning("ctroller: " + ctrl + "  action:" + action)
        logger.warning(len(action_list))
        logger.warning(params)

    key = (ctrl, action)
    if key in action_list:
        if params:
            return action_list[key](**request.json)
        return action_list[key]()

    return "not found!", 404