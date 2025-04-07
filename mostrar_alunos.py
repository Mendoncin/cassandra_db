from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from rich.console import Console
from rich.table import Table

# CASSANDRA_HOSTS = ["127.0.0.1"]
CASSANDRA_HOSTS = ["host.docker.internal"]
KEYSPACE = "banco_cassandra"  
USERNAME = "cassandra"
PASSWORD = "cassandra"

auth_provider = PlainTextAuthProvider(USERNAME, PASSWORD)
cluster = Cluster(CASSANDRA_HOSTS, auth_provider=auth_provider)
session = cluster.connect(KEYSPACE)

query = "SELECT * FROM IF976"

rows = session.execute(query)

console = Console()
table = Table(title="📚 Alunos de Banco de Dados", title_style="bold cyan", header_style="bold white on dark_blue")

table.add_column("📌 Matrícula", style="bold yellow", justify="center", no_wrap=True)
table.add_column("👤 Nome", style="bold green", justify="left")
table.add_column("📝 Prova", style="cyan", justify="center")
table.add_column("👥 Grupo", style="magenta", justify="center")
table.add_column("📁 Projeto 1", style="blue", justify="center")
table.add_column("📁 Projeto 2", style="blue", justify="center")
table.add_column("🎤 Seminário", style="bold red", justify="center")
table.add_column("📊 Média", style="bold white", justify="center")
table.add_column("✅ Status", style="bold green", justify="center")

for row in rows:
    table.add_row(
        str(row.matricula),
        row.nome,
        f"{row.prova:.2f}",
        str(row.grupo),
        f"{row.projeto1:.2f}",
        f"{row.projeto2:.2f}",
        f"{row.seminario:.2f}",
        f"{row.media:.2f}",
        row.status
    )


console.print(table)
