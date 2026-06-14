# fse/telegram/auth_guard.py

from fse.config.env_config import EnvConfig


class AuthGuard:
    """
    Simple Telegram authorization guard.
    Supports single or multiple authorized users.
    """

    def __init__(self):
        # Support both single ID or list of IDs
        self.authorized_users = self._normalize_users()

    def _normalize_users(self):
        auth = EnvConfig.AUTHORIZED_USER

        if isinstance(auth, list):
            return set(str(x) for x in auth)

        return {str(auth)}

    def is_authorized(self, user_id: int | str) -> bool:
        """
        Check if Telegram user is allowed to use bot.
        """
        return str(user_id) in self.authorized_users

    def require_auth(self, user_id: int | str):
        """
        Raise exception if user is not authorized.
        Useful for strict command protection.
        """
        if not self.is_authorized(user_id):
            raise PermissionError("❌ Unauthorized user access blocked")
