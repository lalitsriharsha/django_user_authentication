from cassandra.cluster import Cluster

KEYSPACE = 'django_user_auth'

cluster = Cluster()
session = cluster.connect()

# Create keyspace and table if not exists
session.execute(f"""
    CREATE KEYSPACE IF NOT EXISTS {KEYSPACE}
    WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': 1 }}
""")
session.set_keyspace(KEYSPACE)

session.execute("""
    CREATE TABLE IF NOT EXISTS django_users_detail (
        username TEXT PRIMARY KEY,
        firstname TEXT,
        lastname TEXT,
        age INT,
        password TEXT,
        security_question TEXT,
        security_answer TEXT
    )
""")