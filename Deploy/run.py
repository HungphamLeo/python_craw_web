from internal.controller.controller import ETLController



class Run:
    def __init__(self):
        self.controller = ETLController()

    def run_etl(self):
        self.controller.run()
        