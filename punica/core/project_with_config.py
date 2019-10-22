import json

from os import path

from punica.core.base_project import BaseProject
from punica.exception.punica_exception import PunicaException, PunicaError


class ProjectWithConfig(BaseProject):
    def __init__(self, project_dir: str = ''):
        super().__init__(project_dir)
        pj_config_file_path = path.join(self.project_dir, 'punica.json')
        old_pj_config_file_path = path.join(self.project_dir, 'punica-config.json')
        if path.exists(pj_config_file_path):
            self._pj_config_file_path = pj_config_file_path
        elif path.exists(old_pj_config_file_path):
            self._pj_config_file_path = old_pj_config_file_path
        else:
            raise PunicaException(PunicaError.config_file_not_found)
        try:
            with open(self._pj_config_file_path, 'r')as f:
                self._pj_config = json.load(f)
        except FileNotFoundError:
            raise PunicaException(PunicaError.config_file_not_found)

    @property
    def pj_config(self):
        return self._pj_config

    @property
    def default_network(self):
        return self.pj_config.get('defaultNet', '')

    def get_rpc_address(self, network: str = ''):
        try:
            if len(network) == 0:
                network = self.pj_config['defaultNet']
            networks = self.pj_config['networks']
            host = networks[network]['host']
            port = networks[network]['port']
            return f'{host}:{port}'
        except KeyError:
            raise PunicaException(PunicaError.invalid_network_config)
