import secrets
import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

hostOrigem = secrets.hostOrigem
portOrigem = secrets.portOrigem
userOrigem = secrets.userOrigem
passwordOrigem = secrets.passwordOrigem

hostDestino = secrets.hostDestino
portDestino = secrets.portDestino
userDestino = secrets.userDestino
passwordDestino = secrets.passwordDestino

export = "ppp secret export"

def carregar_ssh(host, port, user, password, command):
    
    ssh.connect(host, port=port, username=user, password=password)

    stdin, stdout, stderr = ssh.exec_command(command)

    retorno = stdout.read().decode()

    ssh.close()

    return retorno

def parse_ppp_secrets(export):
    linhas = export.splitlines()
    comandos = []
    buffer = ""

    for linha in linhas:
        linha = linha.strip()

        # ignora comentários e vazio
        if not linha or linha.startswith("#"):
            continue

        # junta linhas quebradas com "\"
        if linha.endswith("\\"):
            buffer += linha[:-1] + " "
            continue
        else:
            buffer += linha

        # só pega comandos add
        if buffer.startswith("add"):
            comandos.append(f"/ppp secret {buffer.strip()}")

        buffer = ""

    return comandos

def main():

    #exporta configuração
    retornoExport = carregar_ssh(hostOrigem, portOrigem, userOrigem, passwordOrigem, export)

    importar=parse_ppp_secrets(retornoExport)

    print("Exportação ok")
    print(importar)

    #importa configuração
    #resultado = carregar_ssh(hostDestino, portDestino, userDestino, passwordDestino, importar)

    #print("Importação")
    #print(resultado)

    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        sys.exit(1)