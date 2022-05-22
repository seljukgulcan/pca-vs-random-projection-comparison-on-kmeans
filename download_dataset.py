import urllib
import zipfile
import os
import sys
from pathlib import Path

def download_coco_dataset(dataset_name, *, force_download=False):
    """
    Downloads a COCO dataset into the working directory.
    """
    url = f'http://images.cocodataset.org/zips/{dataset_name}.zip'
    zip_name = f'{dataset_name}.zip'
    
    download = force_download or (not os.path.isdir(dataset_name))
    if not download:
        return
    
    urllib.request.urlretrieve(URL, zip_name)
    
    if not os.path.isdir(dataset_name):
        os.mkdir(dataset_name)
    
    with zipfile.ZipFile(zip_name, 'r') as zip_file:
        zip_file.extractall('./')
    
    os.remove(zip_name)

if __name__ == '__main__':
    dataset_name = sys.argv[1]
    download_coco_dataset(dataset_name, force_download=True)