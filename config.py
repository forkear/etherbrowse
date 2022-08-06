import os
from dotenv import load_dotenv
load_dotenv()

USE_COMPILER = os.getenv('USE_COMPILER','no') == 'yes'
SECRET_KEY   = os.getenv('SECRET_KEY')
PREFIX_URL   = os.getenv('PREFIX_URL')
NODE_URL     = os.getenv("NODE_URL")

