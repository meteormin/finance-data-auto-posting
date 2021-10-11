# test scripts

import click
from os.path import exists
import importlib
from src.tests.testable import Testable


@click.command()
@click.argument('name', type=click.STRING, required=True, )
@click.option('--save/--no-save ', '-s/-ns', type=click.BOOL, required=False, default=False,
              help='save test result as json')
def main(name, save):
    """ NAME: test file name """
    if exists('src/tests/' + name + '.py'):
        package = importlib.import_module('src.tests')
        module = importlib.import_module('src.tests.' + name)
        test_class = getattr(module, name.title())(save)
        if isinstance(test_class, Testable):
            test_class.run()
        else:
            print('class: {0} not exists'.format(name))
    else:
        print('{0} is not exists'.format(name))


if __name__ == '__main__':
    main()
