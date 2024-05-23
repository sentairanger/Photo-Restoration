import cv2
import os
import matplotlib.pyplot as plt
import numpy as np
from openvino.runtime import Core

model_dir = "model"
model_name = "colorization-v2.xml"
model_path = os.path.join(model_dir, model_name)
data_directory = "data"

ie = Core()
model = ie.read_model(model=model_path)
compiled_model = ie.compile_model(model=model, device_name = "CPU")
input_layer = compiled_model.input(0)
output_layer = compiled_model.output(0)
N, C, H, W = list(input_layer.shape)


def read_image(impath: str) -> np.ndarray:
    raw_image = cv2.imread(impath)
    if raw_image.shape[2] > 1:
        image = cv2.cvtColor(cv2.cvtColor(raw_image, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2RGB)
    else:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    return image

def colorize(gray_img: np.ndarray) -> np.ndarray:
    # preprocess
    h_in, w_in, _ = gray_img.shape
    img_rgb = gray_img.astype(np.float32) / 255
    img_lab = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2Lab)
    img_l_rs = cv2.resize(img_lab.copy(), (W,H))[:, :, 0]
    # inference
    inputs = np.expand_dims(img_l_rs, axis=[0,1])
    res = compiled_model([inputs])[output_layer]
    update_res = np.squeeze(res)
    # Post process
    out = update_res.transpose((1, 2, 0))
    out = cv2.resize(out,  (w_in, h_in))
    img_lab_out = np.concatenate((img_lab[:, :, 0][:, :, np.newaxis], out), axis=2)
    img_bgr_out = np.clip(cv2.cvtColor(img_lab_out, cv2.COLOR_Lab2RGB), 0, 1)
    colorized_image = (cv2.resize(img_bgr_out, (w_in, h_in)) * 255).astype(np.uint8)
    return colorized_image

def read_images_from_directory(directory_path: str) -> list:
    images = []
    for filename in os.listdir(directory_path):
        if filename.lower().endswith(('.jpg')):
            impath = os.path.join(directory_path, filename)
            try:
                image = read_image(impath)
                colorized_image = colorize(image)
                images.append(colorized_image)
            except ValueError as e:
                print(e)
    return images

def display_images(image_array):
    for i, image in enumerate(image_array):
        plt.imshow(image)
        plt.axis('off')
        plt.title(f'Image {i+1}')
        plt.savefig(f'static/gallery/image_{i+1}.jpg')

images = read_images_from_directory(data_directory)

