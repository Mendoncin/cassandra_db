from cassandra.cluster import Cluster
from rich.prompt import Prompt
from rich import print

def calcular_media(prova, projeto1, projeto2, seminario):
    pesos = {
        'prova': 1/6,
        'projeto1': 1/6,
        'projeto2': 1/3,
        'seminario': 1/3
    }


    return round(
        (prova * pesos['prova']) +
        (projeto1 * pesos['projeto1']) +
        (projeto2 * pesos['projeto2']) +
        (seminario * pesos['seminario']),
        2
    )

def status_aluno(media):
    if media >= 7:
        return "Aprovado"
    elif media >= 6:
        return "Recuperação"
    else:
        return "Reprovado"

def inserir_aluno():
    print("[bold cyan]📘 Cadastro de Aluno - Disciplina IF976[/bold cyan]")

    matricula = Prompt.ask("🎓 Matrícula do Aluno")
    nome = Prompt.ask("👤 Nome do Aluno")
    grupo = Prompt.ask("👥 Grupo")
    prova = float(Prompt.ask("📝 Nota da Prova"))
    projeto1 = float(Prompt.ask("📁 Nota Projeto 1"))
    projeto2 = float(Prompt.ask("📁 Nota Projeto 2"))
    seminario = float(Prompt.ask("🎤 Nota do Seminário"))

    media = calcular_media(prova, projeto1, projeto2, seminario)
    status = status_aluno(media)

    cluster = Cluster(["host.docker.internal"])
    session = cluster.connect("banco_cassandra")

    query = """
    INSERT INTO IF976 (
        matricula, nome, grupo, prova, projeto1, projeto2, seminario, media, status
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    session.execute(query, (
        matricula, nome, grupo, prova, projeto1, projeto2, seminario, media, status
    ))

    cluster.shutdown()

    print(f"\n[green]✅ Aluno {nome} inserido com sucesso! Média: {media} | Status: {status}[/green]")

if __name__ == "__main__":
    inserir_aluno()
