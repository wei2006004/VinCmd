from vincmd import argument
from vincmd import process, child_command


class Demo:
    def __init__(self, cat=False, file=''):
        self.cat = cat
        self.file = file

    @child_command
    @argument('-b', '--boot', help='boot text')
    @argument('-n', '--name', dest='nick_name')
    def apple(self, boot, nick_name):
        print('Demo:apple ', self.file)
        print(boot)
        print(nick_name)

    @child_command
    @argument('-b', '--boot', help='boot text')
    @argument('-n', '--name', dest='nick_name')
    def dog(self, boot, nick_name):
        print('Demo:dog ', self.file)
        print(boot)
        print(nick_name)


_demo = Demo()


@process(commands=[
    {
        'exec': _demo.apple,
        'cmd': 'apple'
    }, {
        'exec': _demo.dog,
        'cmd': 'dog'
    }])
@argument('-c', '--cat', action='store_true')
@argument('-f', '--file')
def demo_process(cat, file):
    print(cat)
    print(file)
    _demo.cat = cat
    _demo.file = file
    return True


if __name__ == '__main__':
    demo_process(sys_argv=True)

    demo = Demo(True, 'bbbb')
    demo.apple('sdf', 'vinson')
    demo.dog('fff', 'vinson')
