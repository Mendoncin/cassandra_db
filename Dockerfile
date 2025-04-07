# Usa uma imagem Python oficial
FROM python:3.10-slim

# Define diretório de trabalho
WORKDIR /app

# Copia os arquivos do projeto
COPY . .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Comando para rodar o script
CMD ["python3", "mostrar_alunos.py"]
