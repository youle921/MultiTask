from PIL import Image
import glob
import os
import numpy as np
import pathlib

def create_gif(parent_path, dulation = 200):
    p = pathlib.Path(parent_path)
    dirs = p.glob("*design/")

    for d in dirs:

        img_files = [*d.glob("gen*.png")]

        time = [img.stat().st_mtime for img in img_files]

        sorted_imgs = []
        for idx in np.argsort(time)[:5]:
            sorted_imgs.append(img_files[idx])

        images = list(map(lambda file: Image.open(file), sorted_imgs))

        images[0].save(f'{str(d)}/exploration.gif', save_all=True, append_images=images[1:], duration=dulation, loop = 0)

names = [f'{alg}/1019' for alg in ["MO-MFEA", "MO-MFEA-II"]]
names.extend([f'{alg}/1017' for alg in ["EMEA", "Island_Model"]])
names.extend(["NSGA-II/1017"])

for n in names:
    create_gif(n)
