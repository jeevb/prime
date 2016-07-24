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
        'APScheduler==3.2.0',
        'argh==0.26.2',
        'cffi==1.7.0',
        'cryptography==1.4',
        'gevent==1.1.1',
        'greenlet==0.4.10',
        'idna==2.1',
        'inflection==0.3.1',
        'ndg-httpsclient==0.4.1',
        'peewee==2.8.1',
        'pyasn1==0.1.9',
        'pycparser==2.14',
        'pyOpenSSL==16.0.0',
        'pytz==2016.6.1',
        'PyYAML==3.11',
        'requests==2.10.0',
        'six==1.10.0',
        'slackclient==1.0.0',
        'tzlocal==1.2.2',
        'websocket-client==0.37.0'
    ],
    zip_safe=True
)
