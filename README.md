# GE_notificacao_push

Projeto Python para monitorar um tópico MQTT, analisar valores recebidos e enviar notificações push via FCM (Firebase Cloud Messaging) de acordo com limites definidos.

## Como funciona

- Conecta-se a um broker MQTT e escuta um tópico.
- Quando um valor recebido ultrapassa 80, 85 ou 95, envia uma notificação FCM em intervalos distintos para cada faixa:
  - Valor > 80: notifica a cada 12h
  - Valor > 85: notifica a cada 6h
  - Valor > 95: notifica a cada 1h

## Estrutura do projeto

```
GE_notificacao_push/
├── main.py
├── fcm.py
├── mqtt_listener.py
├── requirements.txt
├── service_account.json  # <--- NÃO SUBA ESTE ARQUIVO PARA O GITHUB!
└── README.md
```

## Como rodar localmente

1. **Clone o repositório**
    ```
    git clone https://github.com/EngRafael35/GE_notificacao_push.git
    cd GE_notificacao_push
    ```

2. **Crie e edite o arquivo `service_account.json`**  
   Baixe o JSON da sua conta de serviço do Firebase e salve como `service_account.json` na pasta do projeto.

3. **Instale as dependências**
    ```
    pip install -r requirements.txt
    ```

4. **Edite as configurações em `main.py` se necessário**  
   (Broker MQTT, tópico, etc.)

5. **Execute**
    ```
    python main.py
    ```


---