#!/bin/bash
python3 -m venv openvino-env
source openvino-env/bin/activate
pip install openvino-dev>=2024.0.0
git clone https://github.com/openvinotoolkit/open_model_zoo.git
cd open_model_zoo/tools/model_tools
pip install .
omz_downloader --name colorization-v2 --output_dir models --cache_dir models
pip install onnx torch
omz_converter --name colorization-v2 --download_dir models --precisions FP32
cd models/public/colorization-v2
mv FP32 ~/flask-colorization/model

