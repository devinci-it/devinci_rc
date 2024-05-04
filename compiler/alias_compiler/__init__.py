import dotenv
import os
import sys

path= os.path.dirname(os.path.abspath(__file__))
dotenv.load_dotenv(os.path.join(path,'.env'))
os.sys.path.append(path)
print("ENV_LOADED")


