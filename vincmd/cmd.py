from argparse import ArgumentParser
from functools import wraps
import sys

_parsers = {}


def _getParserByFunctionName(name):
    if name not in _parsers.keys():
        _parsers[name] = ArgumentParser()
    return _parsers[name]


class CommandDecorator:
    def __init__(self, is_child=False):
        self.is_child = is_child

    def __call__(self, fun):
        @wraps(fun)
        def wrapper():
            parser = _getParserByFunctionName(fun.__name__)
            value = parser.parse_args(sys.argv[1:])
            return fun(**value.__dict__)

        return wrapper


class ArgumentDecorator:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __call__(self, fun):
        parser = _getParserByFunctionName(fun.__name__)
        parser.add_argument(*self.args, **self.kwargs)

        @wraps(fun)
        def wrapper(*args, **kwargs):
            return fun(*args, **kwargs)

        return wrapper


_processes = {}


def _addProcessCmds(process_name, commands):
    if process_name not in _processes.keys():
        _processes[process_name] = commands
    else:
        cmds = _processes[process_name]
        cmds.append(commands)


def _getProcessCmds(process_name):
    if process_name not in _processes.keys():
        return []
    else:
        return _processes[process_name]


def _enterProcessLoop(process_name):
    while True:
        cmd = input('>>')
        # todo
    pass


class ProcessDecorator:
    def __init__(self, commands):
        if not isinstance(commands, list):
            raise TypeError('Child commands must be list.')
        self.commands = commands

    def __call__(self, fun):
        _addProcessCmds(fun.__name__, self.commands)

        @wraps(fun)
        def wrapper():
            parser = _getParserByFunctionName(fun.__name__)
            ret = fun(**parser.__dict__)
            if ret:
                _enterProcessLoop(fun.__name__)
            return ret

        return wrapper
