from os import getcwd


class BaseProject(object):
    def __init__(self, project_dir: str = ''):
        if len(project_dir) == 0:
            project_dir = getcwd()
        self._project_dir = project_dir

    @property
    def project_dir(self):
        return self._project_dir
