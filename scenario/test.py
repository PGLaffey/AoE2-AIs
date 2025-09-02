from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.heroes import HeroInfo
from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.trigger_lists import ObjectType, ObjectClass, ObjectAttribute, Operation, GarrisonType, \
    ActionType, ButtonLocation
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

# scenario_folder = 'C:/Users/plaff/Games/Age of Empires 2 DE/76561198138036391/resources/_common/scenario'
scenario_folder = 'C:/Users/User/Games/Age of Empires 2 DE/76561198138036391/resources/_common/scenario'
input_path = f'{scenario_folder}/test.aoe2scenario'
output_path = f'{scenario_folder}/test - python.aoe2scenario'

scenario = AoE2DEScenario.from_file(input_path)
t_man = scenario.trigger_manager

trade_workshop_trigger = t_man.add_trigger("Trade Workshop")
trade_workshop_trigger.new_effect.enable_disable_object(source_player=PlayerId.ONE, enabled=False,
                                                        object_list_unit_id=BuildingInfo.FARM.ID)
trade_workshop_trigger.new_effect.enable_disable_object(source_player=PlayerId.ONE, enabled=True,
                                                        object_list_unit_id=BuildingInfo.TRADE_WORKSHOP.ID)
trade_workshop_trigger.new_effect.enable_disable_object(source_player=PlayerId.ONE, enabled=True,
                                                        object_list_unit_id=BuildingInfo.FEITORIA.ID)
for vil in UnitInfo.vils():
    trade_workshop_trigger.new_effect.change_train_location(source_player=PlayerId.ONE,
                                                            object_list_unit_id=BuildingInfo.TRADE_WORKSHOP.ID,
                                                            object_list_unit_id_2=vil.ID,
                                                            button_location=6)

# Teleport Trigger
def teleport_units():
    teleport_trigger = t_man.add_trigger('Teleport Test')
    teleport_trigger.new_condition.timer(3)
    teleport_trigger.new_effect.modify_variable_by_attribute(source_player=PlayerId.ONE,
                                                             object_list_unit_id=HeroInfo.GENGHIS_KHAN.ID,
                                                             object_attributes=ObjectAttribute.UNIT_SIZE_Y,
                                                             operation=Operation.SET,
                                                             variable=0,
                                                             message='Hero Unit Size Y')
    teleport_trigger.new_effect.modify_attribute(source_player=PlayerId.ONE,
                                                 object_list_unit_id=HeroInfo.GENGHIS_KHAN.ID,
                                                 object_attributes=ObjectAttribute.UNIT_SIZE_Y,
                                                 operation=Operation.SET,
                                                 quantity=0
                                                 )
    teleport_trigger.new_effect.teleport_object(source_player=PlayerId.ONE,
                                               area_x1=8, area_x2=10,
                                               area_y1=0, area_y2=1,
                                               location_x=10, location_y=10,
                                               object_type=ObjectType.MILITARY, #object_group=ObjectClass.HERO
                                               )
    teleport_trigger.new_effect.modify_attribute_by_variable(source_player=PlayerId.ONE,
                                                             object_list_unit_id=HeroInfo.GENGHIS_KHAN.ID,
                                                             object_attributes=ObjectAttribute.UNIT_SIZE_Y,
                                                             operation=Operation.SET,
                                                             variable=0)
    teleport_trigger.new_effect.task_object(source_player=PlayerId.ONE,
                                            area_x1=10, area_x2=10, area_y1=10, area_y2=10, location_x=11, location_y=11,
                                            object_type=ObjectType.MILITARY, action_type=ActionType.MOVE)
    teleport_trigger.new_effect.send_chat(source_player=PlayerId.ONE, message="Teleport")

# Setup Unlimited Resources
def unlimited_resources():
    gaia_resources = [OtherInfo.GOLD_MINE, OtherInfo.STONE_MINE, OtherInfo.FORAGE_BUSH, OtherInfo.TREE_OAK_FOREST,
                      OtherInfo.FRUIT_BUSH, OtherInfo.TREE_BAMBOO_FOREST, OtherInfo.TREE_PINE_FOREST]
    player_resources = [BuildingInfo.FARM]
    for res_obj in gaia_resources:
        try:
            res = res_obj.ID
            res_name = res_obj.name.capitalize()
        except AttributeError:
            res = res_obj[0]
            res_name = res_obj[1].capitalize()
        trigger = t_man.add_trigger(f'Resource {res_name}')
        trigger.new_effect.modify_attribute(operation=Operation.SET, source_player=PlayerId.GAIA, object_list_unit_id=res,
                                            object_attributes=ObjectAttribute.DEAD_UNIT_ID, quantity=res)

    for res_obj in player_resources:
        try:
            res = res_obj.ID
            res_name = res_obj.name.capitalize()
        except AttributeError:
            res = res_obj[0]
            res_name = res_obj[1].capitalize()
        trigger = t_man.add_trigger(f'Resource {res_name}')
        trigger.new_effect.modify_attribute(operation=Operation.SET, source_player=PlayerId.ONE, quantity=res,
                                            object_list_unit_id=res, object_attributes=ObjectAttribute.DEAD_UNIT_ID)

print(t_man.get_summary_as_string())
# q = input('Save?')
# if q.lower() == 'y' or q.lower() == 'yes':
#     scenario.write_to_file(output_path)

scenario.write_to_file(output_path)