import requests
from pathlib import Path
from synthetic_im.lib import get_project_root
import pdb

url = 'http://localhost:80'
multiple_files = []
proj_root = get_project_root()

for file in Path(f'{proj_root}/test_data/bicycles').iterdir():
    multiple_files.append(eval("('images', (file.name, open(file, 'rb'), file.name))"))
r = requests.post(url, files=multiple_files)
pdb.set_trace()
print(0)
