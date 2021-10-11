import os
from definitions import MODULE_PATH

path = MODULE_PATH + '/tests'
file_list = os.listdir(path)

module_list = []
for file in file_list:
    module_list.append(file.split('.')[0])

__all__ = module_list