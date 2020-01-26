from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl import app
import numpy

from pysc2.agents import base_agent
from pysc2.lib import actions, features, units
from pysc2.env import sc2_env, run_loop


class WorkerRushBot(base_agent.BaseAgent):
  def __init__(self):
    super(WorkerRushBot, self).__init__()
    self.reward = 0
    self.episodes = 0
    self.steps = 0
    self.obs_spec = None
    self.action_spec = None

  def setup(self, obs_spec, action_spec):
    self.obs_spec = obs_spec
    self.action_spec = action_spec

  def reset(self):
    self.episodes += 1

  def get_my_units_by_type(self, obs, unit_type):
    # print(obs.feature_units)
    if "raw_units" in obs.observation:
      return [unit for unit in obs.observation.raw_units
              if unit.unit_type == unit_type
              and unit.alliance == features.PlayerRelative.SELF]

  def step(self, obs):
    super(WorkerRushBot, self).step(obs)

    probes = self.get_my_units_by_type(obs, units.Protoss.Probe)
    # if self.step == 0:
    #   print(probes[0])
    print('---------------------------------------')
    print(probes[0])

    return actions.RAW_FUNCTIONS.no_op()

def main(unused_argv):
  agent = WorkerRushBot()
  try:
    while True:
      with sc2_env.SC2Env(
          realtime=True,
          map_name="Simple64",
          players=[sc2_env.Agent(sc2_env.Race.protoss),
                   sc2_env.Bot(sc2_env.Race.protoss,
                               sc2_env.Difficulty.easy)],
          agent_interface_format=features.AgentInterfaceFormat(
            action_space=actions.ActionSpace.RAW,
            use_raw_units=True,
            raw_resolution=64,
          ),
      ) as env:
        run_loop.run_loop([agent], env)
  except KeyboardInterrupt:
    pass


if __name__ == "__main__":
  app.run(main)
