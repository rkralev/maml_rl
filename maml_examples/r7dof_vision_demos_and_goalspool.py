
# moving the env_infos/img to observations
import numpy as np
import joblib
from rllab.sampler.utils import joblib_dump_safe


for goal in ["0"]: #,"1","2"]:
    a = joblib.load("/home/rosen/maml_rl/saved_expert_traj/R7DOF/R7-ET-vision-rgb_dummy/raw/%s.pkl" %goal)
    for path in a:
        path['observations']=path['env_infos']['img']
        path['env_infos'] = {}
    joblib_dump_safe(a, "/home/rosen/maml_rl/saved_expert_traj/R7DOF/R7-ET-vision-rgb_dummy/%s.pkl" %goal)


# creating a dummy goals pool


import numpy as np
import joblib
from rllab.sampler.utils import joblib_dump_safe

gp = joblib.load("/home/rosen/maml_rl/saved_expert_traj/R7DOF/R7-ET-vision-rgb_dummy/goals_pool.pkl")

gp_dummy={}
gp_dummy['goals_pool'] = [0]
gp_dummy['idxs_dict'] ={}

for key in gp['idxs_dict'].keys():
    gp_dummy['idxs_dict'][key] = np.zeros_like(gp['idxs_dict'][key])

for i in range(100000):
    gp_dummy['idxs_dict'][i] = np.zeros_like(gp['idxs_dict'][0])


joblib_dump_safe(gp_dummy, "/home/rosen/maml_rl/saved_expert_traj/R7DOF/R7-ET-vision-rgb_dummy/goals_pool.pkl")

## extracting a video from demos

import numpy as np
import joblib
from rllab.sampler.utils import joblib_dump_safe
from PIL import Image
import moviepy.editor as mpy

demos = joblib.load('/home/rosen/maml_rl/saved_expert_traj/R7DOF/R7-ET-vision-rgb_dummy/0.pkl')
# demos = joblib.load('/media/rosen/Evo970/old_dummy/0.pkl')
demos_select = {}
for d in [5,12,221,521,1917]:
    demos_select[d] = demos[d]

demos=[] # releasing all that memory
for d in demos_select.keys():
    demo = demos_select[d]['observations']
    demo_vid = demo[:,:64*64*3]
    images=[]
    for f, frame in enumerate(demo_vid):
        pil_image = Image.frombytes("RGB", (64,64), frame.astype(np.int8).tostring())
        if f == 29:
            pil_image.save("/home/rosen/temp12/new_end_%s" % str(d),"JPEG", quality=80,optimize=True,progressive=True)
        images.append(np.array(pil_image))
    clip = mpy.ImageSequenceClip(images, fps=10)
    clip.write_gif("/home/rosen/temp12/new_demo_%s.gif" % str(d),fps=10)

