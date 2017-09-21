import numpy as np
from gym import utils
from rllab.core.serializable import Serializable
#from gym.envs.mujoco import mujoco_env  # this was originally here
from rllab.envs.mujoco.mujoco_env import MujocoEnv
from rllab.misc.overrides import overrides
from rllab.envs.base import Step

from rllab.envs.base import Env
from rllab.spaces import Box
from rllab.envs.env_spec import EnvSpec
from maml_examples.reacher_vars import ENV_OPTIONS

class ReacherEnv(MujocoEnv, Serializable):
    def __init__(self, option="", *args, **kwargs):
        self.goal = None
        #utils.EzPickle.__init__(self)
        MujocoEnv.__init__(self, file_path=ENV_OPTIONS[option]) #,frame_skip=2)
       # MujocoEnv.__init__(self, file_path='/home/rosen/gym/gym/envs/mujoco/assets/reacher.xml') #,frame_skip=2)
        Serializable.__init__(self, *args, **kwargs)

    def get_current_obs(self):
        return np.concatenate([
            self.model.data.qpos.flat[:2],
            self.model.data.qvel.flat[:2]
        ])

    def step(self, action):
        self.frame_skip = 5
        vec = self.get_body_com("fingertip") - self.get_body_com("target")
 #       vel = self.get_body_comvel("fingertip")
 #       vel1 = self.get_body_comvel("body1")
        reward_dist = - np.linalg.norm(vec)
  #      reward_vel = - np.square(vel).sum()
  #      reward_vel1 = - np.square(vel1).sum()
        reward_ctrl = - np.square(action).sum()
        reward = reward_dist + reward_ctrl # + reward_vel + reward_vel1

        self.forward_dynamics(action)
        next_obs = self.get_current_obs()

        done = False
        return Step(next_obs, reward, done)

    # @overrides
    # def reset(self, init_state=None, **kwargs):
    #     self.reset_mujoco(init_state, **kwargs)
    #     self.model.forward()
    #     self.current_com = self.model.data.com_subtree[0]
    #     self.dcom = np.zeros_like(self.current_com)
    #     return self.get_current_obs()


    def _step(self, a):
        vec = self.get_body_com("fingertip")-self.get_body_com("target")
        reward_dist = - np.linalg.norm(vec)
        reward_ctrl = - np.square(a).sum()
        reward = reward_dist + reward_ctrl
        self.do_simulation(a, self.frame_skip)
        ob = self._get_obs()
        done = False
        return ob, reward, done, dict(reward_dist=reward_dist, reward_ctrl=reward_ctrl)

    def viewer_setup(self):
        self.viewer.cam.trackbodyid = 0

    def reset_model(self):
        qpos = self.np_random.uniform(low=-0.1, high=0.1, size=self.model.nq) + self.init_qpos # TODO, this seems to add a horizontal and vertical vector, resulting in a 4x4 matrix
        while True:
            self.goal = self.np_random.uniform(low=-.2, high=.2, size=2)
            if np.linalg.norm(self.goal) < 2:
                break
        qpos[-2:] = self.goal
        qvel = self.init_qvel # no noise in velocities + self.np_random.uniform(low=-.005, high=.005, size=self.model.nv)
        qvel[-2:] = 0
        self.set_state(qpos, qvel)


        return self._get_obs()



    # @overrides
    # def reset(self, init_state=None, **kwargs):
    #     # Here, we generate a new, random goal to reset the environment with
    #     # We also unpack any noise parameter that may have been passed in reset_args
    #     if init_state is not None:
    #         self.reset_mujoco(init_state=init_state, **kwargs)
    #     else:
    #         assert len(kwargs) > 0, "debug 25 no kwargs passed" # TODO: we should take this off once we're confident in the functionality
    #         reset_args = kwargs.get('reset_args', None)
    #         if type(reset_args) is dict:
    #             assert False, "reset_args shouldn't be a dictionary for ReacherEnv"
    #         else:
    #             task = reset_args
    #         if task is None:
    #             print("debug23 WARNING", kwargs)
    #             task = self.sample_goals(1)[0]
    #         self.reset_mujoco(init_state, reset_args=task)
    #   #  print("debug26")
    #     self.model.forward()
    #     self.current_com = self.model.data.com_subtree[0]
    #     self.dcom = np.zeros_like(self.current_com)
    #     return self.get_current_obs()




    def _get_obs(self):
        theta = self.model.data.qpos.flat[:2]
        return np.concatenate([
            np.cos(theta),
            np.sin(theta),
            self.model.data.qpos.flat[2:],
            self.model.data.qvel.flat[:2],
            self.get_body_com("fingertip") - self.get_body_com("target")
        ])


    def sample_goals(self, num_goals):  # this actually samples whole initial qpos states
        goals_list = []
        for _ in range(num_goals):
            while True:
                newgoal = self.np_random.uniform(low=-.2, high=.2, size=(2, 1))
                if np.linalg.norm(newgoal) < 2:
                    break
            state_and_goal = np.concatenate([
                np.zeros(np.shape(self.init_qpos[:-2])),
                newgoal
            ])
            goals_list.append(state_and_goal)
        return np.array(goals_list)

    @property
    def spec(self):
        return EnvSpec(
            observation_space=self.observation_space,
            action_space=self.action_space,
        )

def fingertip(obs):
    a,b  = obs
    elbow = np.array([np.cos(a),np.sin(a)]) * 0.1
    fingertip = elbow + np.array([np.cos(a+b), np.sin(a+b)]) * 0.11
    return fingertip