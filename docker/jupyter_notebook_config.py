"""
Jupyter configs
"""
c.ServerApp.allow_origin = '*' # pylint: disable=undefined-variable
c.ServerApp.ip = '0.0.0.0' # pylint: disable=undefined-variable

c.NotebookApp.notebook_dir = '/backend/notebooks' # pylint: disable=undefined-variable
c.NotebookApp.open_browser = False # pylint: disable=undefined-variable
c.ServerApp.allow_root = True # pylint: disable=undefined-variable
c.ServerApp.port = 8888 # pylint: disable=undefined-variable
c.ServerApp.token = u'' # pylint: disable=undefined-variable
c.ServerApp.password = 'sha1:82de3bd8aa97:f27b2f5aa414298a84a0a42c36a596edff7a99c0' # pylint: disable=undefined-variable
c.NotebookApp.default_url = '/lab'
