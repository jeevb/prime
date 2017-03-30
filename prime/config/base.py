import os
import yaml

from .exceptions import ConfigError
from prime.storage.local_storage import CONFIG_FILE_PATH


class Field(object):
    def __init__(self,
                 name,
                 env_var=None,
                 required=True,
                 default=None,
                 err_msg=None):
        super(Field, self).__init__()
        self.name = name
        self.env_var = env_var
        self.required = required
        self.default = default

        self._value = self.default
        self._err_msg = (
            err_msg or
            'No value specified for config option %r.' % self.name
        )

    @property
    def value(self):
        if self.required and self._value is None:
            raise ConfigError(self._err_msg)
        return self._value

    @value.setter
    def value(self, val):
        self._value = val


class BaseConfig(object):
    field_definitions = None

    @classmethod
    def from_user_settings(cls, **kwargs):
        return cls.from_yaml(CONFIG_FILE_PATH, **kwargs)

    @classmethod
    def from_yaml(cls, cfg_file, **kwargs):
        with open(cfg_file, 'r') as handle:
            cfg = yaml.load(handle)
            return cls.from_dict(cfg, **kwargs)

    @classmethod
    def from_dict(cls, cfg, **kwargs):
        instance = cls()
        override = cfg or {}

        # Update from keyword arguments
        for k, v in kwargs.items():
            if v is not None:
                override[k] = v

        for f in cls.get_field_definitions():
            new_val = override.get(f.name)

            # No value specified in override dict,
            # try to retrieve from an environment variable
            if new_val is None:
                new_val = os.getenv(f.env_var)

            # If a value was retrieved, update it.
            if new_val is not None:
                f.value = new_val

            # Set the attribute for this config instance
            setattr(instance, f.name, f.value)

        return instance

    @classmethod
    def get_field_definitions(cls):
        assert cls.field_definitions is not None, (
            '%r should either include a `field_definitions` attribute, '
            'or override the `get_field_definitions()` method.'
            % cls.__name__
        )

        assert isinstance(cls.field_definitions, (list, tuple)), (
            'The `field_definitions` attribute in %r '
            'must be a list or tuple.'
            % cls.__name__
        )

        return cls.field_definitions
