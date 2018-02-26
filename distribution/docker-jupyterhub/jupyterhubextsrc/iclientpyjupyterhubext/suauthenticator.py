import os
import crypt
from tornado import gen
from jupyterhub.auth import PAMAuthenticator

try:
    import pamela
except Exception as e:
    pamela = None
    _pamela_error = e


class SuAuthenticator(PAMAuthenticator):

    def system_user_exists(username):
        """Check if the user exists on the system"""
        try:
            import pwd
            pwd.getpwnam(username)
        except KeyError:
            return False
        else:
            return True

    @gen.coroutine
    def authenticate(self, handler, data):
        username = data['username']
        password = data['password']
        if not SuAuthenticator.system_user_exists(username):
            encPass = crypt.crypt(password, "22")
            os.system("useradd -p " + encPass + " -d " + "/home/" + username + " -m " + username)
            os.system("cp -r /iclientpy/sample /home/" + username)
        try:
            pamela.authenticate(username, password, service=self.service)
        except pamela.PAMError as e:
            if handler is not None:
                self.log.warning("PAM Authentication failed (%s@%s): %s", username, handler.request.remote_ip, e)
            else:
                self.log.warning("PAM Authentication failed: %s", e)
        else:
            return username
