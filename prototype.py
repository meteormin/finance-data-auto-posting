import click
from os.path import exists
import importlib
from prototype.handler import Handler
from fdap.app.utils.util import camel

package_name = 'prototype'


@click.command()
@click.argument('name', type=click.STRING, required=True, )
@click.option('--save/--no-save ', '-s/-ns', type=click.BOOL, required=False, default=False,
              help='save test result as json')
def main(name, save):
    """ NAME: test file name """
    click.echo('NAME: ' + name)
    click.echo('CLASS: ' + camel(name))
    if exists('{package}/{name}.py'.format(package=package_name, name=name)):
        package = importlib.import_module(package_name)
        module = importlib.import_module('{package}.{name}'.format(package=package_name, name=name))
        _class = getattr(module, camel(name))(save)
        if isinstance(_class, Handler):
            _class.run()
        else:
            print('class: {0} not exists'.format(name))
    else:
        print('{0} is not exists'.format(name))


if __name__ == '__main__':
    main()
