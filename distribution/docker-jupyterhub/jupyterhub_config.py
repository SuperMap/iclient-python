c.JupyterHub.authenticator_class = 'iclientpyjupyterhubext.suauthenticator.SuAuthenticator'
c.JupyterHub.services = [
    {
        'name': 'cull-idle',
        'admin': True,
        'command': 'python -m iclientpyjupyterhubext.cull_idle_servers --timeout=360'.split(),
    }
]
c.JupyterHub.spawner_class = 'jupyterhub.spawner.LocalProcessSpawner'
c.Spawner.cmd = ['jupyterhub-singleuser']
c.JupyterHub.logo_file = '/srv/jupyterhub/supermap_logo.png'