"""setup.py: setuptools control."""

from setuptools import setup

PROJECT_NAME = "teamcity_memory_map"

setup(
    name=PROJECT_NAME,
    packages=[PROJECT_NAME],
    entry_points={
        "console_scripts": ['{0} = {0}.{0}:main'.format(PROJECT_NAME)]
    },
    install_requires=[
        'teamcity-messages>=1.17.0'
    ],
    version='1.0',
    description='Run GNU size utility and report to TeamCity via service messages',
    author='Alexander Lunegov',
    author_email='alunegov@gmail.com',
    url='https://github.com/alunegov/teamcity_memory_map',
    license='MIT'
)
