from vincmd import command, argument
from vincmd import process


@command()
@argument('-a', '--all', action='store_true')
@argument('-b', '--boot', help='boot text')
@argument('-n', '--name', dest='nick_name')
def hello(all, boot, nick_name):
    print(all)
    print(boot)
    print(nick_name)


@command(is_child = True)
@argument('-b', '--boot', help='boot text')
@argument('-n', '--name', dest='nick_name')
def apple(boot, nick_name):
    print('apple')
    print(boot)
    print(nick_name)


@command(is_child = True)
@argument('-b', '--boot', help='boot text')
@argument('-n', '--name', dest='nick_name')
def dog(boot, nick_name):
    print('apple')
    print(boot)
    print(nick_name)


@process(commands=[apple, dog])
@argument('-c', '--cat', action='store_true')
@argument('-f', '--file')
def demo(cat, file):
    print(cat)
    print(file)
    return True


if __name__ == '__main__':
    hello()
