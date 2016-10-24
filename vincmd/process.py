from functools import wraps
from vincmd.cmd import getParserByFunctionName, ChildCmdMgr, SYS_ARGV_TAG
import sys


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
            if not childFun:
                self._printHelpInfo()
                continue
            parser = getParserByFunctionName(childFun.__name__)
            if '-h' in cmdlist or '--help' in cmdlist:
                parser.print_help()
                continue
            value = parser.parse_args(cmdlist[1:])
            childFun(**value.__dict__)

    def __call__(self, fun):

        @wraps(fun)
        def wrapper(*args,**kwargs):
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
