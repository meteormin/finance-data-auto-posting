# test scripts

import click
from os.path import exists
import importlib
from src.tests.testable import Testable


@click.command()
@click.option('--test', type=click.STRING, required=True, help='executable test python script')
def main(test):
    if exists('src/tests/' + test + '.py'):
        package = importlib.import_module('src.tests')
        module = importlib.import_module('src.tests.' + test)
        test_class = getattr(module, test.title())()
        if isinstance(test_class, Testable):
            test_class.run()
        else:
            print('class: {0} not exists'.format(test))
    else:
        print('test: {0} not exists'.format(test))


if __name__ == '__main__':
    main()
