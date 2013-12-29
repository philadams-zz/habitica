from distutils.core import setup

with open('README.txt') as f:
    readme = f.read()

setup(
    name='hrpg',
    version='0.0.4',
    author='Phil Adams',
    author_email='philadams.net@gmail.com',
    url='https://github.com/philadams/hrpg',
    license='LICENSE.txt',
    description='Commandline interface to HabitRPG (http://habitrpg.com)',
    long_description=readme,
    packages=['hrpg'],
    scripts=['bin/hrpg'],
)
