from pydantic import SecretStr, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict, PydanticBaseSettingsSource, JsonConfigSettingsSource


class Secrets(BaseSettings):
    telegram_bot_token: SecretStr

    e621_auth_username: str  # "" for no auth
    e621_auth_api_key: SecretStr  # ^

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


class Config(BaseSettings):
    class TelegramChat(BaseModel):
        # in seconds, up to additional 10 seconds can be added randomly
        interval: float = 60.0

        watching: list[str]
        blacklist: list[str] = []

        add_caption: bool = True
        spoiler_non_safe: bool = False

    e621_user_agent: str

    chats: dict[int, TelegramChat]
    global_blacklist: list[str]

    model_config = SettingsConfigDict(json_file="config.json", json_file_encoding="utf-8")

    @classmethod
    def settings_customise_sources(
            cls,
            settings_cls: type[BaseSettings],
            init_settings: PydanticBaseSettingsSource,
            env_settings: PydanticBaseSettingsSource,
            dotenv_settings: PydanticBaseSettingsSource,
            file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (  # type: ignore
            init_settings,
            JsonConfigSettingsSource(settings_cls),  # type: ignore
            env_settings,
            dotenv_settings,
            file_secret_settings,
        )


secrets = Secrets()  # type: ignore
config = Config()  # type: ignore
