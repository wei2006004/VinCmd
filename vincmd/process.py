from functools import wraps
from vincmd.cmd import getParserByFunction, SYS_ARGV_TAG
from collections import OrderedDict
import sys


class _ChildCmdMgr:
    def __init__(self):
        self.cmds = []

    def registerChildCommand(self, fun):
        self.cmds.append(fun)

    def getCmdsByClass(self, clazz):
        clsName = clazz.__qualname__
        size = len(clsName)
        result = []
        for fun in self.cmds:
            if fun.__qualname__[0:size] == clsName:
                result.append((clazz, fun))
        return result


_childCmdMgr = _ChildCmdMgr()


def child_command(fun):
    _childCmdMgr.registerChildCommand(fun)

    @wraps(fun)
    def wrapper(*args, **kwargs):
        return fun(*args, **kwargs)

    return wrapper


class ProcessDecorator:
    def __init__(self, classes):
        self.cmds = []
        for clazz in classes:
            self.cmds.extend(_childCmdMgr.getCmdsByClass(clazz))
        self.objects = OrderedDict()
        self.classes = classes

    def getObjectByClass(self, clazz):
        if not clazz:
            return None
        if clazz.__qualname__ not in self.objects.keys():
            return None
        return self.objects[clazz.__qualname__]

    def _enterProcessLoop(self, process_name):
        while True:
            cmd = input(process_name + '> ')
            cmdlist = cmd.split(' ')
            if not cmdlist:
                self._printHelpInfo()
                continue
            if cmdlist[0] == 'exit':
                break
            clazz, childFun = self.findCmdByName(cmdlist[0])
            if not childFun:
                self._printHelpInfo()
            elif '-h' in cmdlist or '--help' in cmdlist:
                parser = getParserByFunction(childFun)
                parser.print_help()
            else:
                parser = getParserByFunction(childFun)
                value = parser.parse_args(cmdlist[1:])
                obj = self.getObjectByClass(clazz)
                if obj:
                    childFun(obj, **value.__dict__)
                else:
                    childFun(**value.__dict__)

    def __call__(self, fun):

        @wraps(fun)
        def wrapper(*args, **kwargs):
            if SYS_ARGV_TAG in kwargs.keys() and kwargs[SYS_ARGV_TAG]:
                parser = getParserByFunction(fun)
                value = parser.parse_args(sys.argv[1:])
                vdict = value.__dict__
                import inspect
                for clazz in self.classes:
                    args = inspect.getargspec(clazz.__init__).args[1:]
                    argdict = dict((key, vdict[key]) for key in args)
                    self.objects[clazz.__name__] = clazz(**argdict)
                ret = fun(*self.objects.values(), **vdict)
                if ret:
                    self._enterProcessLoop(fun.__name__)
                return ret
            return fun(*args, **kwargs)

        return wrapper

    def _printHelpInfo(self):
        print('hlep info')

    def findCmdByName(self, name):
        for clazz, fun in self.cmds:
            if name == fun.__name__:
                return clazz, fun
        return None,None
