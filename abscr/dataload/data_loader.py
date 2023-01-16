from requests import request

__all__ = [ 'DataLoader']

class DataLoader:
    def __init__(self) -> None:
        self.test_data_url = 'https://git.github.com/asdas/asda/test_example.pkl'
        pass

    def load_test_data(self):
        '''
        Download a simple dataset
        '''
        return request('GET', self.test_data_url)
