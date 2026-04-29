# 🚀 PPP Secret Migration via SSH (MikroTik)

Este script em Python realiza a **migração automática de PPP Secrets** entre dois equipamentos MikroTik utilizando conexão SSH.

Ele exporta os usuários PPP de um roteador (origem), ajusta os comandos e importa no roteador de destino.

---

## 📌 Funcionalidades

* Conexão SSH com equipamentos MikroTik
* Exportação automática de `ppp secret`
* Conversão dos comandos para formato executável
* Importação automática no equipamento de destino
* Sistema de logging completo (arquivo + console)
* Tratamento de erros e exceções

---

## 🧠 Como funciona

O fluxo do script é:

1. Conecta no MikroTik de **origem**
2. Executa:

   ```
   ppp secret export
   ```
3. Ajusta os comandos exportados:

   * Substitui `add` por `/ppp secret add`
4. Conecta no MikroTik de **destino**
5. Executa os comandos tratados
6. Registra tudo em log

---

## 📂 Estrutura do projeto

```
.
├── script.py
├── secrets.py
└── /var/log/scripts/ppp_migracao.log
```

---

## 🔐 Arquivo `secrets.py`

Este arquivo contém as credenciais dos equipamentos:

```python
hostOrigem = "192.168.0.1"
portOrigem = 22
userOrigem = "admin"
passwordOrigem = "senha"

hostDestino = "192.168.0.2"
portDestino = 22
userDestino = "admin"
passwordDestino = "senha"
```

⚠️ **Importante:**
Adicione o `secrets.py` no `.gitignore` para evitar expor credenciais.

---

## ⚙️ Requisitos

Instale a dependência necessária:

```bash
pip install paramiko
```

---

## ▶️ Como executar

```bash
python script.py
```

---

## 📝 Logs

O script gera logs em:

```
/var/log/scripts/ppp_migracao.log
```

E também exibe no terminal em tempo real.

### Níveis de log usados:

* `INFO` → fluxo normal
* `DEBUG` → detalhes técnicos (opcional)
* `ERROR` → erros de execução
* `WARNING` → interrupções (ex: Ctrl+C)

---

## ⚠️ Pontos de atenção

* O script faz um `replace("add", "/ppp secret add")`
* Pode afetar outras partes do texto se houver "add" fora de contexto
* O MikroTik pode não aceitar blocos muito grandes de comandos

---

## 🛑 Segurança

* Nunca suba o `secrets.py` para repositórios públicos
* Considere usar variáveis de ambiente no futuro
* Evite logar senhas

---

## 📄 Licença

Uso interno / livre para adaptação.

---

## 👨‍💻 Autor

Guilherme Feijó - 04/2026