import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from sc2.constants import PYLON


class HidePylonBot(sc2.BotAI):
  is_pylon_built = False

  def attack_with_workers(self, unit):
    for worker in self.workers:
      self.do(worker.attack(unit))

  def opponent_has_main_building(self):
    return any(s.name == 'Nexus' for s in self.enemy_structures)

  async def on_step(self, iteration: int):
    if self.minerals > 100 and not self.is_pylon_built:
      await self.build(PYLON, near=self.townhalls.first)
      self.is_pylon_built = True


run_game(maps.get("Simple64"), [
  Bot(Race.Protoss, HidePylonBot()),
  Computer(Race.Protoss, Difficulty.Medium)
], realtime=False)
