from .base import Field, BaseConfig


class MattermostConfig(BaseConfig):
    field_definitions = (
        Field('mattermost_url', 'PRIME_MATTERMOST_URL'),
        Field('mattermost_team', 'PRIME_MATTERMOST_TEAM'),
        Field('mattermost_email', 'PRIME_MATTERMOST_EMAIL'),
        Field('mattermost_password', 'PRIME_MATTERMOST_PASSWORD'),
    )
