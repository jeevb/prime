import sys

from setuptools import setup, find_packages

if sys.version_info < (3, 4):
    sys.exit('Prime requires at least Python 3.4!')

setup(
    name='prime',
    version='1.2.0',
    url='https://bitbucket.org/jeev/prime',
    author='Sanjeev Balakrishnan',
    author_email='me@jeev.io',
    packages=find_packages(),
    scripts=['bin/prime',],
    license='MIT',
    description='Chatbot, python bindings and CLI for Services.',
    install_requires=[
        'APScheduler>=3.3.1',
        'argh>=0.26.2',
        'cffi>=1.9.1',
        'cryptography>=1.7.2',
        'ecdsa>=0.13',
        'Fabric3>=1.13.1.post1',
        'gevent>=1.2.1',
        'greenlet>=0.4.12',
        'idna>=2.2',
        'inflection>=0.3.1',
        'ndg-httpsclient>=0.4.2',
        'paramiko>=2.1.1',
        'peewee>=2.8.5',
        'pyasn1>=0.2.2',
        'pycparser>=2.17',
        'pycrypto>=2.6.1',
        'pyOpenSSL>=16.2.0',
        'pytz>=2016.10',
        'PyYAML>=3.12',
        'requests>=2.13.0',
        'six>=1.10.0',
        'slackclient>=1.0.5',
        'tzlocal>=1.3',
        'websocket-client>=0.40.0'
    ],
    zip_safe=True
)
