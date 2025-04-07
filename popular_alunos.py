import requests
import random
import time
from cassandra.cluster import Cluster
from adicionar_alunos import calcular_media, status_aluno

def gerar_nome():
    try:
        response = requests.get("https://randomuser.me/api/?nat=br")
        data = response.json()
        nome = data['results'][0]['name']
        return f"{nome['first'].capitalize()} {nome['last'].capitalize()}"
    except Exception as e:
        print("Erro ao gerar nome:", e)
        return f"Aluno{random.randint(1000, 9999)}"


def popular_dados(duracao_segundos=60):
    cluster = Cluster(["host.docker.internal"])
    session = cluster.connect("banco_cassandra")

    inicio = time.time()
    contador = 0
    grupo_atual = 1

    nota_grupo = {
        "projeto1": round(random.uniform(4, 13), 2),
        "projeto2": round(random.uniform(4, 13), 2),
        "seminario": round(random.uniform(4, 13), 2)
    }

    while time.time() - inicio < duracao_segundos:
        nome = gerar_nome()
        matricula = f"2025{contador:04d}"
        prova = round(random.uniform(0, 12), 2)

        if prova > 10:
            prova = round(random.uniform(9, 10), 2)

        if contador % 4 == 0 and contador != 0:
            grupo_atual += 1
            nota_grupo = {
                "projeto1": round(random.uniform(3, 13), 2),
                "projeto2": round(random.uniform(3, 13), 2),
                "seminario": round(random.uniform(3, 13), 2),
            }

            if nota_grupo['projeto1'] > 10:
                nota_grupo['projeto1'] = round(random.uniform(9, 10), 2)
            if nota_grupo['projeto2'] > 10:
                nota_grupo['projeto2'] = round(random.uniform(9, 10), 2)
            if nota_grupo['seminario'] > 10:
                nota_grupo['seminario'] = round(random.uniform(9, 10), 2)
            
        media = calcular_media(prova, nota_grupo["projeto1"], nota_grupo["projeto2"], nota_grupo["seminario"])
        status = status_aluno(media)

        query = """
        INSERT INTO IF976 (
            matricula, nome, grupo, prova, projeto1, projeto2, seminario, media, status
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        session.execute(query, (
            matricula, nome, int(grupo_atual),
            prova, nota_grupo["projeto1"], nota_grupo["projeto2"], nota_grupo["seminario"],
            media, status
        ))

        print(f"✅ Inserido: {nome} | Grupo {grupo_atual} | Média: {media} | Status: {status}")
        contador += 1
        time.sleep(1)

    cluster.shutdown()
    print("\n🏁 População finalizada!")


if __name__ == "__main__":
    popular_dados(100)
