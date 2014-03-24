from distutils.core import setup

DISTNAME='databox'
FULLVERSION='0.1'

setup(
    name=DISTNAME,
    version=FULLVERSION,
    packages=['databox'],
    entry_points={
        'console_scripts':
        ['dbox-module-name = databox.cli.module_name:main',
            ]
    }
      )
