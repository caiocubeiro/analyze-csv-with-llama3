# Analisando CSV com Llama3

Projeto web básico para estudos de LLM, utilizando o modelo Llama3 localmente (Offline)

## Bibliotecas utilizadas:

- **Flask**
- **dotenv**
- **pandas**
- **ollama**
- **Jinja**


Para rodar este projeto localmente em Ubuntu, siga os passos abaixo:
```bash
    git clone https://github.com/caiocubeiro/analyze-csv-with-llama3
    cd analyze-csv-with-llama3

    sudo apt install python3
    sudo apt install python3.11-venv

    python3 -m venv .venv
    source .venv/bin/activate
```

Crie um arquivo .venv com as credenciais:
```bash
    SECRET_KEY = ""
```

Install das [bibliotecas](#Bibliotecas) utilizadas:
```bash
    pip install -r requirements.txt
```

Inicie a aplicação:
```bash
    python wsgi.py     
```

Siga esse medium para instalar e utilizar o llama3 local
```bash
    https://medium.com/@sealteamsecs/local-llm-installation-guide-install-llama3-using-ollama-ef8cf68bb461
```

Para novos commits sempre aplicar formatação e verificação bandit
```bash
    black .
    bandit . 
```



