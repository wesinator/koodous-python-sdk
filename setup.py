#!/usr/bin/env python
import pip
from setuptools import setup

REQUIREMENTS_FILE = 'requires.txt'

setup(name='koodous-py',
      packages=['koodous'],
      version='0.8',
      description='Module to interact with Koodous API',
      author='Antonio Sanchez',
      author_email='asanchez@koodous.com',
      license='Apache Version 2',
      url='https://koodous.com/',
      download_url='https://github.com/Koodous/python-sdk/archive/master.zip',
      keywords=['koodous', 'api', 'sdk', 'python', 'android', 'apk', 'malware'],
      install_requires=["click",
                        "coloredlogs",
                        "humanfriendly",
                        "Pygments",
                        "requests",
                        "androguard",
                        "certifi"],
      entry_points='''
        [console_scripts]
        koocli=koodous.cli:cli
      '''
      )
