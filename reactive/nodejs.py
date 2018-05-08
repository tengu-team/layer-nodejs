import os
import wget

from subprocess import run, CalledProcessError, PIPE
from charms.reactive import (
    when,
    when_not,
    set_flag,
    endpoint_from_flag,
)
from charmhelpers.core.hookenv import (
    log,
    status_set,
    config,
    charm_dir,
)

conf = config()


@when_not('nodejs.installed')
def install_layer_nodejs():
    # Install nvm
    try:
        output = run([charm_dir() + "/files/install_nvm.sh"], preexec_fn=demote(1000, 1000))
        output.check_returncode()
    except CalledProcessError as e:
        log(e)
        status_set('blocked', 'Failed to install Nodejs.')
        return
    # Create symb links so root can find nvm / node commands
    os.symlink("/home/ubuntu/bin/nvm", "/usr/local/bin/nvm")
    os.symlink("/home/ubuntu/bin/node", "/usr/local/bin/node")
    # Install the requested node-version if set, by default the 
    # latest version (available to nvm v0.33.11) of NodeJs is installed
    version = conf.get('node-version', "node")
    if version:
        if not install_node_version(version):
            status_set('blocked', 'Could not install node version.')
            return
    status_set('active', 'Node installed({})'.format(get_node_version()))
    set_flag('nodejs.installed')


@when('nodejs.installed',
      'config.changed.node-version')
def node_version_changed():
    version = conf.get('node-version').strip()
    if version:
        install_node_version(version)
        status_set('active', 'Node installed({})'.format(get_node_version()))


def install_node_version(version):
    """
    Installs a node version and make it the active node runtime.
    Returns True on successful install, False on failure.
    """
    try:
        install_output = run(["nvm", "install", version], 
                             preexec_fn=demote(1000, 1000))
        install_output.check_returncode()
        alias_output = run(["nvm", "alias", "default", version], 
                           preexec_fn=demote(1000, 1000))
        alias_output.check_returncode()
    except CalledProcessError as e:
        log(e)
        return False
    return True


def get_node_version():
    """
    Returns currently used Node version or None
    if no node installation is found.
    """
    try:
        output = run(["node", "-v"], stdout=PIPE, preexec_fn=demote(1000, 1000))
        output.check_returncode()
        return output.stdout.decode('utf-8').strip()
    except CalledProcessError as e:
        log(e)
        return None


@when('website.available',
      'config.set.port')
def website_configure():
    endpoint = endpoint_from_flag('website.available')
    endpoint.configure(port=conf.get("port"))


def demote(user_uid, user_gid):
    """Pass the function 'set_ids' to preexec_fn, rather than just calling
    setuid and setgid. This will change the ids for that subprocess only"""

    def set_ids():
        os.setgid(user_gid)
        os.setuid(user_uid)

    return set_ids
