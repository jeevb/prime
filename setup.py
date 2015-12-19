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
        'argh==0.26.1',
        'cffi==1.4.1',
        'cryptography==1.1.2',
        'idna==2.0',
        'ndg-httpsclient==0.4.0',
        'pyasn1==0.1.9',
        'pycparser==2.14',
        'pyOpenSSL==0.15.1',
        'PyYAML==3.11',
        'requests==2.9.0',
        'six==1.10.0',
    ],
    zip_safe=True
)
