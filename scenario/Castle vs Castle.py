from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.heroes import HeroInfo
from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.trigger_lists import ObjectAttribute, Operation, Comparison, ObjectType, ObjectClass, \
    ObjectState, ActionType
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.objects.data_objects.player.player import Player
from AoE2ScenarioParser.objects.data_objects.player.player_resources import PlayerResources
from AoE2ScenarioParser.objects.data_objects.trigger import Trigger
from AoE2ScenarioParser.objects.support.trigger_select import TriggerSelect
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario
from AoE2ScenarioParser.datasets.techs import TechInfo
from AoE2ScenarioParser.datasets.trigger_lists.attribute import Attribute
from util import *

class PlayerNum:
    def __init__(self, num: int, army: int):
        self.num = num
        self.army = army

    def __len__(self):
        return 2

    def __getitem__(self, item):
        return [self.num, self.army][item]


scenario_folder = 'C:/Users/User/Games/Age of Empires 2 DE/76561198138036391/resources/_common/scenario'
input_path = f'{scenario_folder}/Castle vs Castle.aoe2scenario'
output_path = f'{scenario_folder}/Castle vs Castle - python.aoe2scenario'

xs_path = '../xs/Castle vs Castle.xs'

scenario = AoE2DEScenario.from_file(input_path)
xs_manager = scenario.xs_manager
xs_manager.xs_check.raise_on_error = True
xs_manager.xs_check.ignores.add('DiscardedFn')
xs_manager.xs_check.ignores.add('NoNumPromo')
xs_manager.initialise_xs_trigger(insert_index=0)
# xs_manager.add_script(xs_path, validate=True)
t_man = scenario.trigger_manager
unit_man = scenario.unit_manager


map_x, map_y = scenario.map_manager.map_width, scenario.map_manager.map_height


players = [PlayerNum(1, 5), PlayerNum(2, 8), PlayerNum(3, 4), PlayerNum(6, 7)]
res_villagers = Attribute.UNUSED_RESOURCE_008

for player, army in players:
    setup_res = t_man.add_trigger(f'Setup Resources (p{player})', enabled=True, looping=False)

    setup_res.new_effect.modify_resource(source_player=player, tribute_list=res_villagers, operation=Operation.SET, quantity=50)
    setup_res.new_effect.modify_resource(source_player=player, tribute_list=res_villagers, operation=Operation.SUBTRACT, quantity=3)

    # Villager Limit
    vil_limit = t_man.add_trigger(f'Villager Limit (p{player})', enabled=True, looping=False)
    for unit in UnitInfo.vils():
        vil_limit.new_effect.change_object_cost(source_player=player, object_list_unit_id=unit.ID,
                                                resource_1=Attribute.FOOD_STORAGE, resource_1_quantity=50,
                                                resource_2=res_villagers, resource_2_quantity=1)
        vil_limit.new_effect.modify_attribute(source_player=player, object_list_unit_id=unit.ID,
                                              object_attributes=ObjectAttribute.DEAD_UNIT_ID, operation=Operation.SET,
                                              quantity=OtherInfo.IMPALED_CORPSE.ID)
    # Villager Dies
    vil_died = t_man.add_trigger(f'Villager Died (p{player})', enabled=True, looping=True)
    vil_died.new_condition.own_objects(source_player=player, object_list=OtherInfo.IMPALED_CORPSE.ID, quantity=1)
    vil_died.new_effect.remove_object(source_player=player, object_list_unit_id=OtherInfo.IMPALED_CORPSE.ID, max_units_affected=1)
    vil_died.new_effect.modify_resource(source_player=player, tribute_list=res_villagers, operation=Operation.ADD, quantity=1)


    # Camp Barracks
    camp_barracks = t_man.add_trigger(f'Camp Barracks (p{player})', enabled=True, looping=False)
    tech_infantry_time = TechInfo.BLANK_TECHNOLOGY_0.ID
    tech_upgrade_swordsman = TechInfo.BLANK_TECHNOLOGY_1.ID
    tech_upgrade_spearman = TechInfo.BLANK_TECHNOLOGY_2.ID
    tech_upgrade_alt_infantry = TechInfo.BLANK_TECHNOLOGY_3.ID
    tech_toggle_swordsman = TechInfo.BLANK_TECHNOLOGY_4.ID
    tech_toggle_spearman = TechInfo.BLANK_TECHNOLOGY_5.ID
    tech_toggle_alt_infantry = TechInfo.BLANK_TECHNOLOGY_6.ID
    barracks_techs = {
        tech_infantry_time: {'name': 'Infantry Training Time', 'icon': TechInfo.SQUIRES.ICON_ID,
                             'description': 'Trains Infantry 10% Faster',
                             'cost': {'resource_1': Attribute.FOOD_STORAGE, 'resource_1_quantity': 250,
                                     'resource_2': Attribute.GOLD_STORAGE, 'resource_2_quantity': 200},
                             'location': 1},
        tech_upgrade_swordsman: {'name': 'Upgrade Swordman Line', 'icon': TechInfo.CHAMPION.ICON_ID,
                                 'description': 'Improves the Swordsman line',
                                 'cost': {'resource_1'}},
        tech_upgrade_spearman: {},
        tech_upgrade_alt_infantry: {},
        tech_toggle_swordsman: {},
        tech_toggle_spearman: {},
        tech_toggle_alt_infantry: {}
    }
    building = 2414
    for tech, attrs in barracks_techs.items():
        camp_barracks.new_effect.change_technology_name(source_player=player, technology=tech, message=attrs['name'])
        camp_barracks.new_effect.change_technology_icon(source_player=player, technology=tech, quantity=attrs['icon'])
        camp_barracks.new_effect.change_technology_research_time(source_player=player, technology=tech, quantity=30)
        camp_barracks.new_effect.change_technology_description(source_player=player, technology=tech, message=attrs['description'])
        camp_barracks.new_effect.change_technology_cost(source_player=player, technology=tech, **attrs['cost'])
        camp_barracks.new_effect.change_technology_location(source_player=player, technology=tech,
                                                            object_list_unit_id_2=building, button_location=attrs['location'])
    barracks_units = {

    }


print(t_man.get_summary_as_string())
q = input('Save?')
if q.lower() == 'y' or q.lower() == 'yes':
    scenario.write_to_file(output_path)
