import yaml
from time import sleep
from pathlib import Path

from ATRI.log import log

from .models import BotConfig, ConfigModel, WithGoCQHTTP, RuntimeConfig


_DEFAULT_CONFIG_PATH = Path(".") / "ATRI" / "configs" / "default_config.yml"


class Config:
    def __init__(self, config_path: Path):
        if not config_path.is_file():
            try:
                with open(config_path, "w", encoding="utf-8") as w:
                    w.write(_DEFAULT_CONFIG_PATH.read_text("utf-8"))

                log.warning("未检测到 config.yml, 已于当前目录生成, 请参照文档进行填写并重新启动")
                log.warning("文档地址: https://atri.imki.moe/install/configuration-bot/")
                sleep(3)
                exit(0)
            except Exception as err:
                log.error(f"写入文件 config.yml 失败, 请确认是否给足权限: {err}")
                sleep(3)
                exit(-1)
        else:
            with open(config_path, "r", encoding="utf-8") as r:
                if "BotSelfConfig" in r.read():
                    log.warning("你的 config.yml 文件已废弃, 请删除并重新启动")
                    sleep(3)
                    exit(-1)

        self.config_path = config_path
        with open(self.config_path, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)

    def parse(self) -> ConfigModel:
        return ConfigModel.parse_obj(self.config)

    def get_runtime_conf(self) -> dict:
        bot_conf = BotConfig.parse_obj(self.config["BotConfig"])
        gocq_conf = WithGoCQHTTP.parse_obj(self.config["WithGoCQHTTP"])

        return RuntimeConfig(
            host=bot_conf.host,
            port=bot_conf.port,
            debug=bot_conf.debug,
            superusers=bot_conf.superusers,
            nickname=bot_conf.nickname,
            command_start=bot_conf.command_start,
            command_sep=bot_conf.command_sep,
            session_expire_timeout=bot_conf.session_expire_timeout,
            gocq_accoutns=gocq_conf.accounts,
            gocq_download_domain=gocq_conf.download_version,
            gocq_version=gocq_conf.download_version,
        ).dict()
