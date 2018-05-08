# Overview

Installs a NodeJS runtime environment for the ubuntu user.

# Usage

Deploy

`juju deploy ./nodejs`

Configure NodeJs version, defaults to latest available for nvm 0.33.11.

`juju config nodejs "node-version=v8.11.1"`

## Authors
This software was created in the [IDLab research group](https://www.ugent.be/ea/idlab/en) of [Ghent University](https://www.ugent.be/en) in Belgium. This software is used in [Tengu](https://tengu.io), a project that aims to make experimenting with data frameworks and tools as easy as possible.
- Sander Borny <sander.borny@ugent.be>
