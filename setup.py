from setuptools import setup

setup(
    name = 'Monte Carlo Simulator',
    version = '1.0.0',
    url = 'https://github.com/jackburke12/ds5100_final_project.git',
    author = 'Jack Burke',
    author_email='jpb2uj@virginia.edu',
    description = 'Monte Carlo Simulator',
    long_description= open('README.md').read(),
    packages = ['monte_carlo'],
    license='LICENSE',
    install_requires=['numpy','pandas'])
