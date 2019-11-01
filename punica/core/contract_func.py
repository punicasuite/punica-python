from typing import Union, List

from ontology.common.address import Address
from ontology.exception.exception import SDKException


class Func(object):
    def __init__(self, name: str = '', args: Union[str, list] = '', payer: str = '', signers: List[str] = None,
                 pre_exec: bool = False, return_type: str = '', event: List[str] = None):
        self.name = name
        self.args = args
        self.payer = payer
        if signers is None:
            signers = list()
        self.signers = signers
        self.pre_exec = pre_exec
        self.return_type = return_type
        if event is None:
            event = list()
        self.event = event

    def __iter__(self):
        data = dict()
        data[self.name] = self.args
        data['payer'] = self.payer
        data['signers'] = self.signers
        data['preExec'] = self.pre_exec
        data['return'] = self.return_type
        data['event'] = self.event
        for key, value in data.items():
            yield (key, value)

    @classmethod
    def from_dict(cls, data: dict):
        name = list(data.keys())[0]
        return cls(name, data[name], data.get('payer', ''), data.get('signers', list()), data.get('preExec', False),
                   data.get('return', ''), data.get('event', list()))

    @property
    def args_normalized(self):
        return self.__normalize_args(self.args)

    @staticmethod
    def __normalize_args(args: Union[str, list]):
        if not isinstance(args, list):
            return Func.__normalize_arg(args)
        else:
            for index, arg in enumerate(args):
                if isinstance(arg, list):
                    args[index] = Func.__normalize_args(arg)
                else:
                    args[index] = Func.__normalize_arg(arg)
        return args

    @staticmethod
    def __normalize_arg(arg: Union[int, str, bool]):
        if isinstance(arg, str):
            if arg[0] == 'A' and len(arg) == 34:
                try:
                    return Address.b58decode(arg)
                except SDKException:
                    pass
            if arg[0] == 'b' and arg[1] == '\'' and arg[-1] == '\'':
                try:
                    return arg.encode('utf-8')
                except SDKException:
                    pass
        return arg
