import click
from os.path import exists
import importlib
from fdap.prototype.handler import Handler
from fdap.utils.util import camel, is_admin

package_path = 'fdap/prototype'
package_name = 'fdap.prototype'


def query_to_dict(query_str: str):
    if query_str is None:
        return {}
    params = query_str.split('&')
    parameters = {}
    for p in params:
        key, value = p.split('=')
        parameters[key] = value

    return parameters


@click.command()
@click.argument('name', type=click.STRING, required=True)
@click.option('--save/--no-save ', '-s/-ns', type=click.BOOL, required=False, default=False,
              help='save test result as json')
@click.option('--parameters', '-p', type=click.STRING, required=False,
              help='send parameters to test file, must be query string format(p1=aa&p2=bb)')
def main(name: str, save: bool, parameters: str):
    """
    NAME: test file name
    """
    click.echo('NAME: ' + name)
    click.echo('CLASS: ' + camel(name))
    if exists('{package}/{name}.py'.format(package=package_path, name=name)):
        package = importlib.import_module(package_name)
        module = importlib.import_module('{package}.{name}'.format(package=package_name, name=name))

        _class = getattr(module, camel(name))(parameters=query_to_dict(parameters), save_result=save)
        if isinstance(_class, Handler):
            _class.run()
        else:
            print('class: {0} not exists'.format(name))
    else:
        print('{0} is not exists'.format(name))


if __name__ == '__main__':
    if is_admin():
        main()
    else:
        print('ERROR: Please Run Administrator')
