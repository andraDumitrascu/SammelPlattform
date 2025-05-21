from django.core.management.base import BaseCommand
from ldap3 import Server, Connection, ALL, SUBTREE, Tls
import ssl
import os
from dotenv import load_dotenv
load_dotenv()
print("DEBUG: BIND_DN =", os.getenv("LDAP_BIND_DN"))
print("DEBUG: BIND_PW =", os.getenv("LDAP_BIND_PASSWORD"))
print("DEBUG: LDAP_HOST =", os.getenv('LDAP_HOST'))
class Command(BaseCommand):
    help = "Zeigt alle Schüler-Logins aus dem LDAP-Verzeichnis an"

    def handle(self, *args, **options):
        ldap_host = os.getenv("LDAP_HOST")
        bind_dn = os.getenv("LDAP_BIND_DN")
        bind_pw = os.getenv("LDAP_BIND_PASSWORD")
        user_search_base = os.getenv("LDAP_USER_SEARCH")

        if not all([ldap_host, bind_dn, bind_pw, user_search_base]):
            self.stderr.write("Fehlende LDAP Umgebungsvariablen.")
            return

        # TLS-Konfiguration zum Ignorieren von Zertifikaten (nicht für Prod)
        tls_config = Tls(validate=ssl.CERT_NONE)
        server = Server(ldap_host, use_ssl=True, get_info=ALL, tls=tls_config)
        conn = Connection(server, bind_dn, bind_pw, auto_bind=True)

        # Beispiel: Schüler gehören zur Gruppe "cn=Schueler,..."
        search_filter = "(memberOf=cn=Schueler,ou=Gruppen,dc=Schule,dc=lokal)"
        attributes = ["uid", "givenName", "sn", "mail"]

        self.stdout.write("📚 Schüler-Logins aus LDAP:\n")

        conn.search(
            search_base=user_search_base,
            search_filter=search_filter,
            search_scope=SUBTREE,
            attributes=attributes
        )

        if not conn.entries:
            self.stdout.write("⚠️ Keine Schüler gefunden.")
        else:
            for entry in conn.entries:
                uid = entry.uid.value
                name = f"{entry.givenName.value} {entry.sn.value}"
                email = entry.mail.value
                self.stdout.write(f"👤 {uid} | {name} | {email}")

        conn.unbind()
