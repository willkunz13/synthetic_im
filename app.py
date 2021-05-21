from flask import Flask, render_template, request, send_file
from synthetic_im.models.dino import * 
import os
import zipfile
import sys
from synthetic_im.lib import get_project_root
import torch
from math import floor
from torchvision import datasets, models, transforms

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = './data/input/'

root_path = get_project_root()
sys.path.insert(0, str(root_path/'test_data/models'))
sys.path.insert(0, str(root_path/'synthetic_im'))
model = torch.load(root_path/'test_data/models/dino_small.pt')
data_transforms = transforms.Compose([
        transforms.ToTensor(),
        transforms.Resize((512, 512)),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
            ])
 
@app.route('/', methods=['GET'])
def home():
    return "<h1>Microservice API for DINO model implementation</h1><p>In order to interact with the microservice, send post request to this same address with images.</p>"


@app.route('/', methods=['POST'])
def input():
    if request.method == 'POST':
        images = request.files.to_dict(flat=False)['images']
        for image in images:
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
       
        root_path = get_project_root()
        
        image_datasets = DinoDataset(app.config['UPLOAD_FOLDER'], data_transforms)
                          
        dataloader = torch.utils.data.DataLoader(image_datasets, batch_size=2,
                                                     shuffle=False, num_workers=2)
        
        #predict_images(model = model, dataloader = dataloader, output_dir= 'data/output')
        zipf = zipfile.ZipFile('Name.zip','w', zipfile.ZIP_DEFLATED)
        for file in os.listdir('data/output/'):
            zipf.write('data/output/'+file)
        zipf.close()
        pdb.set_trace()
        return send_file('Name.zip',
                mimetype = 'zip',
                attachment_filename= 'Name.zip',
                as_attachment = True)

if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 80))
    app.run(host='0.0.0.0', port=port, debug=True)
