import logging


logger_request = logging.getLogger(__name__)
logger_request.setLevel(logging.INFO)
handler = logging.FileHandler('app_requests.log', encoding='utf=8', mode='w')
formater = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formater)
logger_request.addHandler(handler)
