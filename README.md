# scavenger-hunt

OpenStack was founded as a project in 2010. For the occasion of its
tenth anniversary, the Open Telekom Cloud hosts a scavenger hunt. This
repo hosts some code for the server for a website serving the
challenge. It decomposes to three major parts:

1. The server logic, written in Python 3 and based on Flask: `main.py`.

2. A template for the structure and style of the microsite:
   `templates/index.html`.

3. The actual configuration of the questions asked. Obviously, this
   needs to be changed for the _production server_.

## Installation

Requires Python 3. Virtual environment recommended.

Install flask: `pip install flask`.

Configuring the project: All configuration options are listed in `config.yaml`.

Run server: `python main.py`

## Credits

Copyright (c) 2020 by Open Telekom Cloud, T-Systems International GmbH

Written by Nils Magnus (nils.magnus@t-systems.com)
