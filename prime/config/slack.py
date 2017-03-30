from .base import Field, BaseConfig


class SlackConfig(BaseConfig):
    field_definitions = (
        Field('slack_token', 'PRIME_SLACK_TOKEN'),
    )
