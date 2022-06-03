from utils.config import AppConfig, ManagerConfig, ServerConfig
from utils.config_utils import AppConfigUtil, EmailConfigUtil, ManagerConfigUtil
from al_utils.logger import Logger
logger = Logger(__file__).logger


class ManagerService:
    def __init__(self) -> None:
        self.app_config = AppConfigUtil()
        self.email_config = EmailConfigUtil()
        self.manager_config = ManagerConfigUtil()

    def init(self, app: AppConfig, server: ServerConfig, manager: ManagerConfig):
        """Initialize project required configurations."""
        if not app:
            raise ValueError('app must be set.')
        if not server:
            raise ValueError('server must be set.')
        if not manager:
            raise ValueError('manager must be set.')
        self.app_config.update(**app)
        logger.info(f'update app configs to {app}')
        for k, v in server:
            self.email_config.server[k] = v
        logger.info(f'update server configs to {server}')
        self.manager_config.update(**manager)
        logger.info(f'update manager configs to {manager}')
