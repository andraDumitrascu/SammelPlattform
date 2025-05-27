 
from ldap3 import Server, Connection, SUBTREE

from getpass import getpass
 
# === 1. Read-Only Bind-Zugang ===

LDAP_SERVER = 'ldaps.htlwy.at'

LDAP_PORT = 636

LDAP_USE_SSL = True

BIND_DN = 'cn=ldap-ro,ou=services,dc=schule,dc=local'

BIND_PASSWORD = '8b6d0aa2-ee34-412e-a50b-9ba991c512bd'

BASE_DN = 'ou=users,dc=schule,dc=local'
 
# === 2. Schüler-Login über Eingabe ===

print("🔐 Benutzer-Login testen")

uid = input("Benutzername (uid): ")

user_password = getpass("Passwort: ")
 
# === 3. Verbindung mit Read-Only Account herstellen ===

server = Server(LDAP_SERVER, port=LDAP_PORT, use_ssl=LDAP_USE_SSL)
 
print("🌐 Verbinde mit LDAPS...")

conn = Connection(server, user=BIND_DN, password=BIND_PASSWORD, auto_bind=True)

print("✅ Read-only Bind erfolgreich.")
 
# === 4. Benutzer-DN suchen ===

search_filter = f'(uid={uid})'

conn.search(

    search_base=BASE_DN,

    search_filter=search_filter,

    search_scope=SUBTREE,

    attributes=['cn', 'mail', 'uid']

)
 
if not conn.entries:

    print("❌ Benutzer nicht gefunden.")

    conn.unbind()

else:

    entry = conn.entries[0]

    user_dn = entry.entry_dn

    print(f"✅ Benutzer gefunden: {user_dn}")

    print("📄 LDAP-Daten:")

    print(entry.entry_attributes_as_dict)
 
    # === 5. Authentifizierung mit Benutzerpasswort testen ===

    print("🔐 Versuche Benutzer-Login...")

    user_conn = Connection(server, user=user_dn, password=user_password, auto_bind=True)

    if user_conn.bound:

        print("✅ Login erfolgreich!")

        user_conn.unbind()

    else:

        print("❌ Login fehlgeschlagen – Passwort falsch?")
 
    conn.unbind()