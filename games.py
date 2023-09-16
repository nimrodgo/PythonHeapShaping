class Game:
    def __init__(self, version, settings):
        self.version = version
        self.settings = settings


class BabaIsYou(Game):
    def __init__(self, version, settings):
        self.executable = 'babaisyou.exe'
        super(BabaIsYou, self).__init__(version, settings)


class SlayTheSpire(Game):
    def __init__(self, version, settings):
        self.executable = 'slaythespire.exe'
        super(SlayTheSpire, self).__init__(version, settings)
