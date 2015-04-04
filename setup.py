from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name='hrpg',
    version='0.0.10',
    author='Phil Adams',
    author_email='philadams.net@gmail.com',
    url='https://github.com/philadams/hrpg',
    license='LICENSE.txt',
    description='Commandline interface to HabitRPG (http://habitrpg.com)',
    long_description=readme,
    packages=find_packages(exclude=('dist', 'tests')),
    install_requires=[
        'docopt',
        'requests',
    ],
    scripts=['bin/hrpg'],
)
