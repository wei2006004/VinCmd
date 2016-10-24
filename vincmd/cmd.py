from argparse import ArgumentParser
from functools import wraps
import sys

_parsers = {}

SYS_ARGV_TAG = 'sys_argv'


def getParserByFunctionName(name):
    if name not in _parsers.keys():
        _parsers[name] = ArgumentParser()
    return _parsers[name]


def command(fun):
    @wraps(fun)
    def wrapper(*args, **kwargs):
        if SYS_ARGV_TAG in kwargs.keys() and kwargs[SYS_ARGV_TAG]:
            parser = getParserByFunctionName(fun.__name__)
            value = parser.parse_args(sys.argv[1:])
            return fun(**value.__dict__)
        return fun(*args, **kwargs)

    return wrapper


def child_command(fun):
    @wraps(fun)
    def wrapper(*args, **kwargs):
        if SYS_ARGV_TAG in kwargs.keys() and kwargs[SYS_ARGV_TAG]:
            parser = getParserByFunctionName(fun.__name__)
            value = parser.parse_args(sys.argv[1:])
            return fun(**value.__dict__)
        return fun(*args, **kwargs)

    return wrapper


class ChildCmdMgr:
    EXEC_TAG = 'exec'
    CMD_TAG = 'cmd'

    def __init__(self, commands):
        if not isinstance(commands, list):
            raise TypeError('Child commands must be list.')

        for command in commands:
            if self.EXEC_TAG not in command.keys():
                raise SyntaxError('wrong group commands')
        self.commands = commands

    def getChildFunction(self, cmd):
        for command in self.commands:
            if self.CMD_TAG in command.keys():
                if cmd == command[self.CMD_TAG]:
                    return command[self.EXEC_TAG]
                else:
                    continue
            else:
                if cmd == command[self.EXEC_TAG].__name__:
                    return command[self.EXEC_TAG]
        return None


class GroupDecorator:
    def __init__(self, commands):
        self.cmdMgr = ChildCmdMgr(commands)

    def __call__(self, fun):

        @wraps(fun)
        def wrapper(sys_argv=False):
            if not sys_argv:
                fun()
                return None
            if len(sys.argv) <= 1:
                self.printUsage()
                return None
            childFun = self.cmdMgr.getChildFunction(sys.argv[1])
            if not childFun:
                raise SyntaxError('wrong cmd')
            fun()
            parser = getParserByFunctionName(childFun.__name__)
            value = parser.parse_args(sys.argv[2:])
            return childFun(**value.__dict__)

        return wrapper

    def printUsage(self):
        print('no agrv')


class ArgumentDecorator:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __call__(self, fun):
        parser = getParserByFunctionName(fun.__name__)
        parser.add_argument(*self.args, **self.kwargs)

        @wraps(fun)
        def wrapper(*args, **kwargs):
            return fun(*args, **kwargs)

        return wrapper
