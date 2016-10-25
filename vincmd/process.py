from functools import wraps
from vincmd.cmd import getParserByFunctionName, ChildCmdMgr, SYS_ARGV_TAG
import sys


def child_command(fun):
    @wraps(fun)
    def wrapper(*args, **kwargs):
        if SYS_ARGV_TAG in kwargs.keys() and kwargs[SYS_ARGV_TAG]:
            parser = getParserByFunctionName(fun.__name__)
            value = parser.parse_args(sys.argv[1:])
            return fun(**value.__dict__)
        return fun(*args, **kwargs)

    return wrapper


class ProcessDecorator:
    def __init__(self, commands):
        self.cmdMgr = ChildCmdMgr(commands)

    def _enterProcessLoop(self, process_name):
        while True:
            cmd = input(process_name + '> ')
            cmdlist = cmd.split(' ')
            if not cmdlist:
                self._printHelpInfo()
                continue
            if cmdlist[0] == 'exit':
                break
            childFun = self.cmdMgr.getChildFunction(cmdlist[0])
            parser = getParserByFunctionName(childFun.__name__)
            if not childFun:
                self._printHelpInfo()
            elif '-h' in cmdlist or '--help' in cmdlist:
                parser.print_help()
            else:
                value = parser.parse_args(cmdlist[1:])
                childFun(**value.__dict__)

    def __call__(self, fun):

        @wraps(fun)
        def wrapper(*args, **kwargs):
            if SYS_ARGV_TAG in kwargs.keys() and kwargs[SYS_ARGV_TAG]:
                parser = getParserByFunctionName(fun.__name__)
                value = parser.parse_args(sys.argv[1:])
                ret = fun(**value.__dict__)
                if ret:
                    self._enterProcessLoop(fun.__name__)
                return ret
            return fun(*args, **kwargs)

        return wrapper

    def _printHelpInfo(self):
        print('hlep info')
