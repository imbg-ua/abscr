import logging


class Segmentor:
    def __init__(self) -> None:
        self.models = ['cellpose']
        logging.INFO(f'Available models:\n{self.models}')
        pass

    def predict(self):
        return