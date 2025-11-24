import logging
import os

# Define o nome e o nível do arquivo de log
LOG_FILE_NAME = 'controle_financeiro.log'
LOG_LEVEL = logging.INFO

def setup_logging():
    """Configura o logger raiz do sistema."""
    # Garante que a configuração básica só seja executada uma vez
    if not logging.getLogger().handlers:
        logging.basicConfig(
            level=LOG_LEVEL,
            format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
            filename=LOG_FILE_NAME,
            filemode='a'
        )
        # Exemplo de logging para confirmar a inicialização
        logging.info(f"Sistema de Logging configurado. Arquivo: {os.path.abspath(LOG_FILE_NAME)}")

def get_logger(name):
    """
    Retorna uma instância de logger com um nome específico.
    """
    return logging.getLogger(name)

# Garante que o logging seja configurado assim que o módulo for importado
setup_logging()