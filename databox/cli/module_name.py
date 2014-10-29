import argparse
import os
import pkgutil
import imp

def main():
    parser = argparse.ArgumentParser(description="");
    parser.add_argument('path', help="path to python file")
    parser.add_argument('-f', '--flag', help="Will output -m flag if path is importable",
                        action="store_true")
    parser.add_argument('-d', '--debug', help="Debug",
                        action="store_true")

    args = parser.parse_args()
    path = os.path.abspath(args.path)
    flag = args.flag
    debug = args.debug

    output = gen_output(path, flag, debug)
    print(output)

def gen_output(path, flag, debug):
    try:
        module_ns = get_module_name(path, debug)
    except Exception as e:
        if debug:
            print(str(e))
        module_ns = None

    if module_ns is None:
        return repr(path)
    if flag:
        return "-m " + repr(module_ns)
    return module_ns

def get_module_name(path, debug):
    orig_path = path
    path, fn = os.path.split(path)
    if not fn.endswith('.py'):
        if debug:
            print(path, 'is not python file')
        return None
    module_name = os.path.splitext(fn)[0]
    names = [module_name]

    while path:
        if not is_package(path, debug):
            if debug:
                print(path, 'is not a package')
                print('names=', names)
            break
        path, name = path.rsplit(os.path.sep, 1)
        names.append(name)

    # means that file was not within a package
    if len(names) == 1:
        return None

    module_ns = '.'.join(reversed(names))
    root_package = names[-1]
    bits = imp.find_module(root_package)
    root_path = bits[1]

    # instead of loading, we use simple heuristic. if root package
    # exists and in same location as orig_path, then we're good
    orig_path = os.path.realpath(orig_path)
    root_path = os.path.realpath(root_path)
    if orig_path.startswith(root_path):
        return module_ns
    return None

def is_package(path, debug):
    init_file = os.path.join(path, '__init__.py')
    return os.path.isfile(init_file)
