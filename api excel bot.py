from flask import Flask, request, jsonify
import pandas as pd
import os
from flask_cors import CORS

# Caminho do arquivo Excel
arquivo_excel = "C:\\Users\\lorra\\Desktop\\Linda Joia\\Vendas\\Api python.xlsx"

# Criar API Flask
app = Flask(__name__)
CORS(app)  # Permitir acesso de outras origens (navegador, Postman, etc.)

# TESTE 1️⃣: Verificar se o arquivo existe antes de carregar
if not os.path.exists(arquivo_excel):
    print(f"❌ ERRO: Arquivo não encontrado em {arquivo_excel}")
    exit(1)  # Interrompe a execução

print("✅ Arquivo encontrado! Tentando carregar...")

try:
    # Carregar a planilha do Excel
    df_ref = pd.read_excel(arquivo_excel, sheet_name="Ref")

    # TESTE 2️⃣: Exibir os nomes das colunas
    print("✅ Planilha carregada com sucesso!")
    print("🔍 Nomes das colunas:", df_ref.columns.tolist())

    # TESTE 3️⃣: Mostrar as primeiras 5 linhas
    print("📊 Primeiras linhas da tabela:")
    print(df_ref.head())

    # Limpar espaços extras nos nomes das colunas
    df_ref.columns = df_ref.columns.str.strip()

    # TESTE 4️⃣: Exibir valores únicos antes e depois da conversão
    print("🔍 Valores únicos antes da conversão:")
    print(df_ref["Codigo da Referencia"].unique())

    df_ref["Codigo da Referencia"] = df_ref["Codigo da Referencia"].astype(str).str.strip()

    print("✅ Valores únicos depois da conversão:")
    print(df_ref["Codigo da Referencia"].unique())

except Exception as e:
    print(f"❌ ERRO ao carregar a planilha: {e}")
    exit(1)  # Interrompe a execução


# ✅ TESTE 5️⃣: Endpoint de teste para ver se a API está rodando
@app.route('/ping', methods=['GET'])
def ping():
    print("✅ Requisição recebida no /ping!")
    return jsonify({"mensagem": "API funcionando!"})


# ✅ TESTE 6️⃣: Endpoint para testar conexão e resposta JSON
@app.route('/teste', methods=['GET'])
def teste():
    print("✅ Requisição recebida no /teste!")
    return jsonify({"status": "ok", "descricao": "Este é um teste de resposta"})


# ✅ TESTE 7️⃣: Endpoint para buscar informações por referência
@app.route('/buscar', methods=['GET'])
def buscar_por_referencia():
    referencia = request.args.get('Codigo da Referencia')

    print(f"🔍 Requisição recebida para referência: {referencia}")

    if not referencia:
        return jsonify({"erro": "Informe uma referência"}), 400

    referencia = referencia.strip()

    # TESTE 8️⃣: Exibir o DataFrame antes da busca
    print("📊 DataFrame antes da busca:")
    print(df_ref.head())

    # TESTE 9️⃣: Verificar se a referência existe no DataFrame
    if referencia not in df_ref["Codigo da Referencia"].values:
        print(f"❌ Referência {referencia} não encontrada.")
        return jsonify({"mensagem": "Referência não encontrada"}), 404

    # Realizar a busca
    resultado = df_ref[df_ref["Codigo da Referencia"] == referencia]

    # TESTE 🔟: Exibir o resultado da busca
    print("🔍 Resultado da busca:")
    print(resultado)

    return jsonify(resultado.to_dict(orient="records"))


# ✅ TESTE 1️⃣1️⃣: Rodar a API de forma acessível
if __name__ == '__main__':
    print("🚀 Iniciando API...")
    app.run(host="0.0.0.0", port=8080)        # Porta alterada para evitar bloqueios 
