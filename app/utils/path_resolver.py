import pathlib

class PathResolver(object):
    def __init__(self):
        pass

    @classmethod
    def resolve_by_root(cls, path, *args, **kwargs):
        if not path:
            path = ''
        return cls.get_module_path().parent.parent / path

    @classmethod
    def get_cwd(cls):
        return pathlib.Path.cwd()

    @classmethod
    def get_module_path(cls):
        return pathlib.Path(__file__).resolve().parent
