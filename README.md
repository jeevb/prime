# Prime

Python bindings and CLI for [*Services*](https://bitbucket.org/jeevb/services). Currently, it can:

- Send notifications to a Services master.

## Getting started

#### Setting up a virtual environment
`virtualenv` is recommended to set up all the necessary dependencies. You may install it using `pip` as follows:
```
$ pip install virtualenv
```

Next, initiate a fresh virtual enviroment:
```
$ virtualenv env
```

#### Installation
Activate your newly created virtual environment:
```
$ source env/bin/activate
```

and install Prime with all of its dependencies:
```
$ pip install git+ssh://git@bitbucket.org/jeevb/prime.git
```

#### Configuration
Prime sources configuration options from two locations:

- Current user's home folder: `$HOME/.prime.yml`
- Arguments passed to the command:
    - `--host`: Host address of the Services master.
    - `--port`: Port that the Services master will be listening on.
    - `--token`: API key to authenticate with Services master.
    - `--to`: Route to send messages to.

To create and populate a configuration file in the user's home folder:
```
$ prime init
```
and specify the necessary information to communicate with the Services master.


# License

The MIT License (MIT)

Copyright (c) 2015 Sanjeev Balakrishnan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
