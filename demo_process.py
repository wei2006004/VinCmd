from vincmd import argument
from vincmd import process, child_command


class DemoOne:
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


class DemoTwo:
    def __init__(self, path):
        self.path = path

    @child_command
    def orange(self):
        print('DemoTwo:orange ', self.path)


@process(classes=[DemoOne, DemoTwo])
@argument('-c', '--cat', action='store_true')
@argument('-f', '--file')
@argument('-p', '--path')
def demo_process(demoOne, demoTwo, cat, file, path):
    print(demoOne.cat)
    print(demoOne.file)
    print(demoTwo.path)
    print(cat)
    print(file)
    print(path)
    return True


if __name__ == '__main__':
    demo_process(sys_argv=True)

    demo = DemoOne(True, 'bbbb')
    demo.apple('sdf', 'vinson')
    demo.dog('fff', 'vinson')
