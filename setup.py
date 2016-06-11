from setuptools import setup

setup(
    name='DailyExpenses',
    version='0.1a0',
    url='https://github.com/taryk/daily_expenses',
    license='GPL',
    author='Taras Iagniuk',
    author_email='mrtaryk@gmail.com',
    description='A tool to keep track of your daily expenses',
    platforms='any',
    install_requires=[
        'pyqt5>=5.6',
        'sqlalchemy>=1.0.13',
    ],
    setup_requires=['pytest-runner'],
    tests_require=[
        'pytest',
        'pytest-qt>=1.11.0',
        'pytest-mock>=1.1'
    ],
)
