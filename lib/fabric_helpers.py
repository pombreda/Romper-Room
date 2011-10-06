import os
import string
from fabric.api import env

_conf_root = os.path.join(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))), 'conf')

_conf_dirs = [x for x in os.listdir(_conf_root)
              if os.path.isdir(os.path.join(_conf_root, x))
              and x != 'base']

def _mk_sethost_fn(host_dicts):
    def inner():
        """ (Autogenerated host connection function.) """
        hoststrings = []
        if env.key_filename == None: env.key_filename = []
        for host in host_dicts:
            hostname = host.get('hostname', '')
            user = host.get('user', '')
            port = host.get('port', '')
            hoststring = '%s%s%s' % (user and user + '@',
                                   hostname,
                                   port and ':' + str(port),
                                  )
            hoststrings.append(hoststring)
            key_filename = host.get('key_filename')
            if key_filename:
                env.key_filename.append(key_filename)
        env.hosts = hoststrings
    return inner

for x in _conf_dirs:
    try:
        module_name = string.join(('conf', x, 'hosts'), '.')
        module = __import__(module_name, fromlist=['hosts',])
        locals()[x] = _mk_sethost_fn(module.hosts)
    except ImportError:
        pass
