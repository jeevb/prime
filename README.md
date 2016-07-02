# Prime

Chatbot, python bindings and CLI for [*Services*](https://bitbucket.org/jeevb/services). Currently, it can:

- Respond to commands on Slack
- Send notifications to a Services master.

## Getting started

#### Setting up a Docker container
Install `docker-compose` if necessary:
```
$ pip install docker-compose
```

Clone Prime into your local directory:
```
$ git clone https://bitbucket.org/jeevb/prime.git
```

Build the Docker image:
```
$ cd prime
$ docker-compose build
```

#### Configuration
Prime sources configuration options from two locations:

- Current user's home folder: `$HOME/.prime/config.yml`
- Arguments passed to the `notify` command:
    - `--host`: Host address of the Services master.
    - `--port`: Port that the Services master will be listening on.
    - `--token`: API key to authenticate with Services master.
    - `--to`: Route to send messages to.
    - `--cert`: Certificate file to use for SSL verification.
- Argument passed to the `slack` command:
    - `--token`: API key to authenticate with the Slack RTM API.

To create and populate a configuration file in the user's home folder:
```
$ docker-compose run --rm prime init
```
and specify the necessary information to communicate with the Services master and Slack RTM API.


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
