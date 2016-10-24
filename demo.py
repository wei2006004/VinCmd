from vincmd import command, argument
from vincmd import group, child_command


@command
@argument('-a', '--all', action='store_true')
@argument('-b', '--boot', help='boot text')
@argument('-n', '--name', dest='nick_name')
def hello(all, boot, nick_name):
    print(all)
    print(boot)
    print(nick_name)


@child_command
@argument('-b', '--boot', help='boot text')
@argument('-n', '--name', dest='nick_name')
def demo_apple(boot, nick_name):
    print('apple')
    print(boot)
    print(nick_name)


@child_command
@argument('-b', '--boot', help='boot text')
@argument('-n', '--name', dest='nick_name')
def demo_dog(boot, nick_name):
    print('dog')
    print(boot)
    print(nick_name)


@group(commands=[
    {
        'exec': demo_apple,
        'cmd': 'apple'
    }, {
        'exec': demo_dog,
        'cmd': 'dog'
    }])
def demo_group():
    print('before group')


if __name__ == '__main__':
    # hello(sys_argv=True)
    # hello(True, 'boooo', 'vinson')

    demo_group(sys_argv=True)
