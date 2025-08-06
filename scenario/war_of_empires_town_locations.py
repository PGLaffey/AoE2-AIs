from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.heroes import HeroInfo
from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.terrains import TerrainId
from AoE2ScenarioParser.datasets.trigger_lists import ObjectAttribute, Operation, Comparison, ObjectType, ObjectClass, \
    ObjectState
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.objects.data_objects.trigger import Trigger
from AoE2ScenarioParser.objects.support.trigger_select import TriggerSelect
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario
from AoE2ScenarioParser.datasets.techs import TechInfo
from AoE2ScenarioParser.datasets.trigger_lists.attribute import Attribute

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

scenario_folder = 'C:/Users/User/Games/Age of Empires 2 DE/76561198138036391/resources/_common/scenario'
input_path = f'{scenario_folder}/war of empires - backup.aoe2scenario'
output_path = f'{scenario_folder}/war of empires.aoe2scenario'

scenario = AoE2DEScenario.from_file(input_path)

t_man = scenario.trigger_manager
u_man = scenario.unit_manager
# print(m_man.map_size) # 240

town_radius = 5
town_locations = [
    # Front Row
    Point(35, 105),
    Point(105, 35),
    # Left Row
    Point(25, 165),
    Point(95, 95),
    Point(165, 25),
    # Middle Row
    Point(15, 225),
    Point(85, 155),
    Point(155, 85),
    Point(225, 15),
    # Right Row
    Point(75, 215),
    Point(145, 145),
    Point(215, 75),
    # Back Row
    Point(135, 205),
    Point(205, 135)
]


for town_num in range(1, len(town_locations) + 1):
    town_i = town_num - 1
    town_center = town_locations[town_i]
    town_area = {'area_x1': town_center.x - town_radius, 'area_x2': town_center.x + town_radius,
                 'area_y1': town_center.y - town_radius, 'area_y2': town_center.y + town_radius}
    u_man.add_unit(player=PlayerId.GAIA, unit_const=OtherInfo.FLAG_A.ID, x=town_center.x + 0.5, y=town_center.y + 0.5)
    area = scenario.new.area()
    area.center(town_center.x, town_center.y).expand(town_radius)
    for tile in area.to_coords(as_terrain=True):
        tile.terrain_id = TerrainId.ROAD_GRAVEL



print(t_man.get_summary_as_string())
q = input('Save?')
if q.lower() == 'y' or q.lower() == 'yes':
    scenario.write_to_file(output_path)