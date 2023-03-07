from configparser import ConfigParser


class ReadConfig:
    def __init__(self):
        self.configur = ConfigParser()
        self.section_name = 'DATABASE'
        self.configur.read("config.ini")

    def get_hostname(self):
        return self.configur.get(self.section_name, 'host')

    def get_database(self):
        return self.configur.get(self.section_name, 'database')

    def get_password(self):
        return self.configur.get(self.section_name, 'password')

    def get_port(self):
        return self.configur.get(self.section_name, 'port')
