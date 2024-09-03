from openai import OpenAI

client = OpenAI()
import requests


# Função para identificar a intenção do usuário
def identificar_intencao(mensagem):
    resposta = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Você é um analista de atendimento ao cliente da empresa ore Crm"},
        {"role": "user", "content": f"Identifique se o usuário deseja registrar uma reclamação ou solicitar um boleto: {mensagem}"}  
    ])
    intencao = resposta.choices[0].message.content.strip().lower()
    return intencao

# Função para coletar informações adicionais
def coletar_informacoes(intencao):
    if 'reclamação' in intencao:
        # Pedir detalhes sobre a reclamação
        return {
            "tipo": "reclamacao",
            "detalhes": input("Por favor, descreva sua reclamação: "),
            "usuario": input("Informe seu nome de usuário ou ID: ")
        }
    elif 'boleto' in intencao:
        # Pedir detalhes para emitir o boleto
        return {
            "tipo": "boleto",
            "usuario": input("Informe seu nome de usuário ou ID: "),
            "mes": input("Para qual mês você deseja emitir o boleto?: ")
        }
    else:
        return None

# Função para chamar as APIs da Core CRM
def chamar_api(dados):
    if dados['tipo'] == 'reclamacao':
        url = 'https://cliente.core/api/CriarChamado'
        response = requests.post(url, json=dados)
    elif dados['tipo'] == 'boleto':
        url = 'https://cliente.core/api/EmitirBoleto'
        response = requests.post(url, json=dados)

    if response.status_code == 200:
        print("Operação realizada com sucesso!")
    else:
        print("Houve um erro ao processar sua solicitação.")

# Fluxo principal do chatbot
def main():
    mensagem = input("Olá! Como posso ajudar você hoje?: ")
    intencao = identificar_intencao(mensagem)

    if intencao:
        dados = coletar_informacoes(intencao)
        if dados:
            chamar_api(dados)
        else:
            print("Não consegui entender sua solicitação.")
    else:
        print("Não foi possível identificar a intenção da mensagem.")

# Execução do chatbot
if __name__ == "__main__":
    main()
