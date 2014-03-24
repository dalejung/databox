import argparse
import os

def module_name():
    parser = argparse.ArgumentParser(description="");
    parser.add_argument('path', help="p")

    args = parser.parse_args()
    path = args.path

    print path

if __name__ == '__main__':
    main()
