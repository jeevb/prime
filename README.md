# Prime

Chatbot.

Currently works with the following platforms:

- Slack
- Mattermost (v3.4, v3.7)

## Getting started

There are two ways to install Prime:

- virtualenv
- Docker

#### Setting up a virtual environment
`virtualenv` is recommended to set up all the necessary dependencies. You may install it using `pip` as follows:
```
$ pip install virtualenv
```

Next, initiate a fresh virtual enviroment:
```
$ virtualenv env
```

Activate your newly created virtual environment:
```
$ source env/bin/activate
```

and install Prime with all of its dependencies:
```
(env)$ pip install git+https://jeevb@bitbucket.org/jeevb/prime.git
```

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
- Argument passed to the `slack` command:
    - `--token`: API key to authenticate with the Slack RTM API.
- Arguments passed to the `mattermost` command:
    - `--mattermost-url`: URL of Mattermost server.
    - `--mattermost-team`: Mattermost team to connect to.
    - `--mattermost-email`: Email account to log in to Mattermost server with.
    - `--mattermost-password`: Password of account to log in to Mattermost server with.

To create and populate a configuration file in the user's home folder with the necessary information to communicate with the Mattermost or Slack RTM APIs:

**With virtualenv**:
```
(env)$ prime init
```
**With Docker**:
```
$ docker-compose run --rm prime init
```

# License

The MIT License (MIT)

Copyright (c) 2017 Sanjeev Balakrishnan

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
