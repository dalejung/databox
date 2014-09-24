import argparse
import os
import pkgutil

def main():
    parser = argparse.ArgumentParser(description="");
    parser.add_argument('path', help="path to python file")
    parser.add_argument('-f', '--flag', help="Will output -m flag if path is importable",
                        action="store_true")

    args = parser.parse_args()
    path = os.path.abspath(args.path)
    flag = args.flag

    output = gen_output(path, flag)
    print(output)

def gen_output(path, flag):
    try:
        module_ns = get_module_name(path)
    except:
        module_ns = None

    if module_ns is None:
        return repr(path)
    if flag:
        return "-m " + repr(module_ns)
    return module_ns

def get_module_name(path):
    orig_path = path
    path, fn = os.path.split(path)
    if not fn.endswith('.py'):
        return None
    module_name = os.path.splitext(fn)[0]
    names = [module_name]

    while path:
        if not is_package(path):
            break
        path, name = path.rsplit(os.path.sep, 1)
        names.append(name)

    # means that file was not within a package
    if len(names) == 1:
        return None

    module_ns = '.'.join(reversed(names))
    loader = pkgutil.get_loader(module_ns)
    # make sure that the generated ns exists and points to original file
    if loader and loader.get_filename() == orig_path:
        return module_ns
    return None

def is_package(path):
    init_file = os.path.join(path, '__init__.py')
    return os.path.isfile(init_file)
