# AUTOGENERATED! DO NOT EDIT! File to edit: notebooks/ImgImporter.ipynb (unless otherwise specified).

__all__ = ['ImgImporter']

# Cell
#skip
import os
from google_images_search import GoogleImagesSearch

class ImgImporter():
    def __init__(self, outfp = 'data'):
        self.gis = GoogleImagesSearch(os.getenv('GCS_DEVELOPER_KEY'), os.getenv('GCS_CX'))
        self.outfp = outfp
    def search(self, num = 10):
        _search_params = {
            'q': 'bicycle',
            'num': num,
            'safe': 'medium',
            'fileType': 'jpg',
            'imgSize': 'MEDIUM',
            'rights': 'cc_publicdomain|cc_attribute|cc_sharealike|cc_noncommercial|cc_nonderived'
        }

        self.gis.search(search_params=_search_params)
        for image in gis.results():
          image.download(path_to_dir=self.outfp)
    def next_page(self):
        self.gis.next_page()
        for image in gis.results():
            image.download(path_to_dir=self.outfp)