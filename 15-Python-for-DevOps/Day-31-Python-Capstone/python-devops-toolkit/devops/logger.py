import logging
from pathlib import Path

def setup_logger():
    log_directory = Path('logs')
    log_directory.mkdir(exist_ok=True)
    logging.basicConfig(filename=log_directory / 'devops-tool.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    return logging.getLogger('devops-tool')
