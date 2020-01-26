import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from sc2.constants import transforming


class WorkerRushBot(sc2.BotAI):
  structure_to_attack = None

  def attack_with_workers(self, unit):
    for worker in self.workers:
      self.do(worker.attack(unit))

  def opponent_has_main_building(self):
    return any(s.name == 'Nexus' for s in self.enemy_structures)

  async def on_step(self, iteration: int):
    if iteration == 0:
      self.attack_with_workers(self.enemy_start_locations[0])

    # if self.structure_to_attack is not None:
    #   self.attack_with_workers(self.structure_to_attack)

    enemy_structures_len = len(self.enemy_structures)
    opponent_has_main_building = self.opponent_has_main_building()

    if iteration % 100 == 0:
      print(enemy_structures_len)
      print(opponent_has_main_building)
      print(self.workers.idle)

    if enemy_structures_len > 0 and not opponent_has_main_building and not self.workers.idle.empty:
      self.attack_with_workers(self.enemy_structures[0])

    # if u for u in self.enemy_structures:

    # if len(self.enemy_structures) > 0 and len(self.enemy_units) == 0:
    #     for worker in self.workers:
    #       self.do(worker.attack(self.enemy_structures[0]))
    # if len(self.enemy_units) > 0:
    #     for worker in self.workers:
    #       self.do(worker.attack(self.enemy_start_locations[0]))

    if iteration % 100 == 0:
      print(self.enemy_structures)
      print(self.enemy_units)
      print('---------------- ')


run_game(maps.get("Simple64"), [
  Bot(Race.Zerg, WorkerRushBot()),
  Computer(Race.Protoss, Difficulty)
], realtime=False)
