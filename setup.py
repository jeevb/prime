from setuptools import setup, find_packages

setup(
    name='prime',
    version='0.1.0',
    url='https://bitbucket.org/jeev/prime',
    author='Sanjeev Balakrishnan',
    author_email='me@jeev.io',
    packages=find_packages(),
    scripts=['bin/prime',],
    license='MIT',
    description='Python bindings and CLI for Services.',
    install_requires=[
    ],
    zip_safe=True
)
