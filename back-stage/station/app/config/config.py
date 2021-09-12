import configparser
import os


config_ini = configparser.ConfigParser()
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.ini")
config_ini.read(path)