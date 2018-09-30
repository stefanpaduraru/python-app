import configparser

# get config options
class Config:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('/home/pi/assistant/config.ini')
        self.config.sections()

    def getSection(self, section):
        dict1 = {}
        options = self.config.options(section)
        for option in options:
            try:
                dict1[option] = self.config.get(section, option)
            except:
                dict1[option] = None
        return dict1

    
