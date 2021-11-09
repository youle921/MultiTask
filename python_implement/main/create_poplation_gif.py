from PIL import Image
import numpy as np
import pathlib

def create_gif(parent_path, dulation = 200, fixed = False):
    
    p = pathlib.Path(parent_path)
    dirs = p.glob("*design/")
    
    if not fixed:
        key = "gen*pop.png"
        ext = "exploration.gif"
    else:
        key = "gen*fixed.png"
        ext = "exploration_fix_range.gif"

    for d in dirs:
 
        img_files = [*d.glob(key)]

        if len(img_files) > 0:
            
            sorted_imgs = sorted(img_files, key = lambda img: int(str(img).split("gen")[1].split("_")[0]))
            images = list(map(lambda file: Image.open(file), sorted_imgs))
            images[0].save(f'{str(d)}/{ext}', save_all=True, append_images=images[1:], duration=dulation, loop = 1)

names = [f'{alg}/1019' for alg in ["MO-MFEA", "MO-MFEA-II"]]
names.extend([f'{alg}/1017' for alg in ["EMEA", "Island_Model"]])
names.extend(["NSGA-II/1017"])

for n in names:
    create_gif(n)
    create_gif(n, fixed = True)

create_gif(names[-1], fixed = True)
