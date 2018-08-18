
CHEETAH_GOALS_LOCATION = '/home/rosen/maml_rl/saved_goals/cheetah/goals_pool1.pkl'
CHEETAH_GOALS_LOCATION_EC2 = '/root/code/rllab/saved_goals/cheetah/goals_pool1.pkl'
CHEETAH_GOALS_LOC_INCREMENTAL = '/home/rosen/maml_rl/saved_expert_traj/cheetah_sparse/incremental_vels/goals_pool.pkl'

ENV_OPTIONS = {
    '':'half_cheetah.xml',

}

default_cheetah_env_option = ''

EXPERT_TRAJ_LOCATION_DICT = {
    "_local": "/home/rosen/maml_rl/saved_expert_traj/cheetah/CH-ET4-individual/",
    "_local_sparse": "/home/rosen/maml_rl/saved_expert_traj/cheetah_sparse/main_1/",
    "_local_incremental": "/home/rosen/maml_rl/saved_expert_traj/cheetah_sparse/incremental_vels/",
    "_ec2": "/root/code/rllab/saved_expert_traj/cheetah/CH-ET4-individual/",
    "_local.noise0.1": "/home/rosen/maml_rl/saved_expert_traj/cheetah/CH-ET-E1.6-noise0.1/",
    "_ec2.noise0.1": "/root/code/rllab/saved_expert_traj/cheetah/CH-ET-E1.6-noise0.1/",
    "_local.noise0.1.small": "/home/rosen/maml_rl/saved_expert_traj/cheetah/CH-ET-E1.7-noise0.1-small/",
    "_ec2.noise0.1.small": "/root/code/rllab/saved_expert_traj/cheetah/CH-ET-E1.7-noise0.1-small/",
}

