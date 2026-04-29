import secrets
import paramiko
import sys
import logging

# ===== LOGGING =====
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("ppp_migracao.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)
# ===================


# === SSH CLIENT === 
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# ================== 


# ===== DADOS DE ORIGEM =====
hostOrigem = secrets.hostOrigem
portOrigem = secrets.portOrigem
userOrigem = secrets.userOrigem
passwordOrigem = secrets.passwordOrigem

# ===== DADOS DE DESTINO =====
hostDestino = secrets.hostDestino
portDestino = secrets.portDestino
userDestino = secrets.userDestino
passwordDestino = secrets.passwordDestino


# Comando de export
export = "ppp secret export"


def carregar_ssh(host, port, user, password, command):
    try:
        logger.info(f"Conectando em {host}:{port} com usuário {user}")

        ssh.connect(host, port=port, username=user, password=password)

        logger.info(f"Executando comando em {host}")
        stdin, stdout, stderr = ssh.exec_command(command)

        retorno = stdout.read().decode()
        erro = stderr.read().decode()

        if erro:
            logger.error(f"Erro ao executar comando em {host}: {erro}")

        logger.info(f"Comando executado com sucesso em {host}")

        ssh.close()

        return retorno

    except Exception as e:
        logger.exception(f"Falha na conexão/comando em {host}")
        raise


def main():
    logger.info("===== INÍCIO DA MIGRAÇÃO PPP =====")

    # ===== EXPORTAÇÃO =====
    logger.info("Exportando PPP Secrets do equipamento de origem")
    retornoExport = carregar_ssh(
        hostOrigem,
        portOrigem,
        userOrigem,
        passwordOrigem,
        export
    )

    logger.debug(f"Export bruto:\n{retornoExport}")

    # ===== TRATAMENTO =====
    logger.info("Ajustando comandos para importação")
    importar = retornoExport.replace("add", "/ppp secret add")

    logger.debug(f"Comandos tratados:\n{importar}")

    # ===== IMPORTAÇÃO =====
    logger.info("Importando PPP Secrets no equipamento de destino")
    resultado = carregar_ssh(
        hostDestino,
        portDestino,
        userDestino,
        passwordDestino,
        importar
    )

    logger.debug(f"Resultado da importação:\n{resultado}")

    logger.info("===== MIGRAÇÃO FINALIZADA COM SUCESSO =====")

    return 0


# ===== PONTO DE ENTRADA =====
if __name__ == "__main__":
    try:
        sys.exit(main())

    except KeyboardInterrupt:
        logger.warning("Execução interrompida pelo usuário")
        sys.exit(0)

    except Exception as e:
        logger.exception("Erro fatal na execução")
        sys.exit(1)