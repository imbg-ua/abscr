from requests import request

__all__ = ['DataLoader']


class DataLoader:
    def __init__(self) -> None:
        self.test_data_url = 'https://git.github.com/asdas/asda/test_example.pkl'
        pass

    def load_test_data(self):
        '''
        Download a simple dataset for test
        '''
        return request('GET', self.test_data_url)

    def load(self, image_path: list) -> list:
        '''
        Load images from local storage.

        Params:
        image_path: list of filepathes

        Returns:
        list of images. List of PIL.Image objects.
        '''
        
        imgs = []
        for path in image_path:
            pass
        return
