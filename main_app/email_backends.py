import ssl
from django.core.mail.backends.smtp import EmailBackend as SMTPEmailBackend

class UnsafeEmailBackend(SMTPEmailBackend):
    def open(self):
        if self.connection:
            return False
        try:
            self.connection = self.connection_class(self.host, self.port, timeout=self.timeout)
            if self.use_tls:
                # Створюємо контекст, який ігнорує помилки сертифікатів
                ctx = ssl._create_unverified_context()
                self.connection.starttls(context=ctx)
            if self.username and self.password:
                self.connection.login(self.username, self.password)
            return True
        except:
            if not self.fail_silently:
                raise
            return False