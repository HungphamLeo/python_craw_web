from internal.controller.controller import ETLController



class Run:
    def __init__(self):
        self.controller = ETLController()
        # any Run funtion service
        

    def run_etl(self):
        
        self.controller.run()
        