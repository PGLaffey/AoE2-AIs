from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.heroes import HeroInfo
from AoE2ScenarioParser.datasets.techs import TechInfo
from AoE2ScenarioParser.datasets.trigger_lists import Comparison, Operation, ButtonLocation, ObjectAttribute, ActionType
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.objects.data_objects.variable import Variable
from AoE2ScenarioParser.objects.support.enums.group_by import GroupBy
from AoE2ScenarioParser.objects.support.trigger_select import TriggerSelect
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario
from AoE2ScenarioParser.datasets.trigger_lists.attribute import Attribute

input_path = 'C:/Users/User/Games/Age of Empires 2 DE/76561198138036391/resources/_common/scenario/Defend.aoe2scenario'
output_path = 'C:/Users/User/Games/Age of Empires 2 DE/76561198138036391/resources/_common/scenario/Defend - Python.aoe2scenario'

scenario = AoE2DEScenario.from_file(input_path)

t_man = scenario.trigger_manager

xs_manager = scenario.xs_manager
xs_manager.xs_check.raise_on_error = False
xs_manager.xs_check.ignores.add('DiscardedFn')
xs_manager.xs_check.ignores.add('NoNumPromo')
xs_manager.initialise_xs_trigger(insert_index=0)
xs_manager.add_script(xs_file_path='../xs/defend.xs', validate=True)


trigger_data = scenario.actions.load_data_triggers()
trigger_objects = trigger_data.objects

ATTACK_CASTLES = [trigger_objects.P4CASTLE, trigger_objects.P5CASTLE, trigger_objects.P6CASTLE, trigger_objects.P7CASTLE]

attacker_ais = [PlayerId.FOUR.value, PlayerId.FIVE.value, PlayerId.SIX.value, PlayerId.SEVEN.value]
players = [PlayerId.ONE.value, PlayerId.TWO.value, PlayerId.THREE.value]

for player in players:
    # Reset Hero Tree
    reset_hero_trigger = t_man.add_trigger(f'Reset Heroes (p{player})')
    reset_hero_trigger.new_effect.change_technology_location(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_10.ID,
                                                             object_list_unit_id_2=BuildingInfo.HALL_OF_HEROES.ID,
                                                             button_location=ButtonLocation.r3c1)
    reset_hero_trigger.new_effect.change_technology_icon(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_10.ID,
                                                         quantity=TechInfo.ILLUMINATION.ICON_ID)
    reset_hero_trigger.new_effect.change_technology_name(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_10.ID,
                                                         message='Reset Hero Tree')
    reset_hero_trigger.new_effect.change_technology_description(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_10.ID,
                                                                message='Reset Hero Tree <cost>')
    reset_hero_trigger.new_effect.enable_technology_stacking(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_10.ID,
                                                             quantity=1000)
    reset_hero_trigger.new_effect.enable_disable_technology(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_10.ID,
                                                            enabled=True)

    # Research Defense Tech
    defense_tech_count = 10
    defense_tech_trigger = t_man.add_trigger(f'Setup Defense Tech (p{player})')
    defense_tech_trigger.new_effect.change_technology_location(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_11.ID,
                                                               object_list_unit_id_2=BuildingInfo.HALL_OF_HEROES.ID,
                                                               button_location=ButtonLocation.r2c1)
    defense_tech_trigger.new_effect.change_technology_cost(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_11.ID,
                                                           resource_1=Attribute.STONE_STORAGE, resource_1_quantity=500,
                                                           resource_2=Attribute.WOOD_STORAGE, resource_2_quantity=500)
    defense_tech_trigger.new_effect.change_technology_icon(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_11.ID,
                                                           quantity=TechInfo.MURDER_HOLES.ICON_ID)
    defense_tech_trigger.new_effect.change_technology_name(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_11.ID,
                                                           message='Research Defense Technology')
    defense_tech_trigger.new_effect.change_technology_description(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_11.ID,
                                                                  message='Research Defense Technology <cost>')
    defense_tech_trigger.new_effect.enable_technology_stacking(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_11.ID,
                                                               quantity=defense_tech_count)
    defense_tech_trigger.new_effect.enable_disable_technology(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_11.ID,
                                                              enabled=True)

    do_defense_tech_trigger = t_man.add_trigger(f'Research Defense Tech (p{player})', looping=True)
    do_defense_tech_trigger.new_condition.research_technology(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_11.ID)
    do_defense_tech_trigger.new_effect.enable_disable_technology(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_11.ID,
                                                              enabled=True)
    do_defense_tech_trigger.new_effect.script_call(message=f'p{player}_research_defend_defense_tech();')


    # Research Unit Tech
    unit_tech_count = 10
    unit_tech_trigger = t_man.add_trigger(f'Setup unit Tech (p{player})')
    unit_tech_trigger.new_effect.change_technology_location(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_12.ID,
                                                               object_list_unit_id_2=BuildingInfo.HALL_OF_HEROES.ID,
                                                               button_location=ButtonLocation.r2c2)
    unit_tech_trigger.new_effect.change_technology_cost(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_12.ID,
                                                           resource_1=Attribute.FOOD_STORAGE, resource_1_quantity=500,
                                                           resource_2=Attribute.GOLD_STORAGE, resource_2_quantity=500)
    unit_tech_trigger.new_effect.change_technology_icon(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_12.ID,
                                                           quantity=TechInfo.SQUIRES.ICON_ID)
    unit_tech_trigger.new_effect.change_technology_name(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_12.ID,
                                                           message='Research Unit Technology')
    unit_tech_trigger.new_effect.change_technology_description(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_12.ID,
                                                                  message='Research Unit Technology <cost>')
    unit_tech_trigger.new_effect.enable_technology_stacking(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_12.ID,
                                                               quantity=unit_tech_count)
    unit_tech_trigger.new_effect.enable_disable_technology(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_12.ID,
                                                              enabled=True)

    do_unit_tech_trigger = t_man.add_trigger(f'Research Unit Tech (p{player})', looping=True)
    do_unit_tech_trigger.new_condition.research_technology(source_player=player,
                                                              technology=TechInfo.BLANK_TECHNOLOGY_12.ID)
    do_unit_tech_trigger.new_effect.enable_disable_technology(source_player=player,
                                                                 technology=TechInfo.BLANK_TECHNOLOGY_12.ID,
                                                                 enabled=True)
    do_unit_tech_trigger.new_effect.script_call(message=f'p{player}_research_defend_unit_tech();')

    # Research Eco Tech
    eco_tech_count = 10
    eco_tech_trigger = t_man.add_trigger(f'Setup Eco Tech (p{player})')
    eco_tech_trigger.new_effect.change_technology_location(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_13.ID,
                                                               object_list_unit_id_2=BuildingInfo.HALL_OF_HEROES.ID,
                                                               button_location=ButtonLocation.r2c3)
    eco_tech_trigger.new_effect.change_technology_cost(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_13.ID,
                                                           resource_1=Attribute.FOOD_STORAGE, resource_1_quantity=500,
                                                           resource_2=Attribute.WOOD_STORAGE, resource_2_quantity=500)
    eco_tech_trigger.new_effect.change_technology_icon(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_13.ID,
                                                           quantity=TechInfo.HERBAL_MEDICINE.ICON_ID)
    eco_tech_trigger.new_effect.change_technology_name(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_13.ID,
                                                           message='Research Eco Technology')
    eco_tech_trigger.new_effect.change_technology_description(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_13.ID,
                                                                  message='Research eco Technology <cost>')
    eco_tech_trigger.new_effect.enable_technology_stacking(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_13.ID,
                                                               quantity=eco_tech_count)
    eco_tech_trigger.new_effect.enable_disable_technology(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_13.ID,
                                                              enabled=True)

    do_eco_tech_trigger = t_man.add_trigger(f'Research Eco Tech (p{player})', looping=True)
    do_eco_tech_trigger.new_condition.research_technology(source_player=player,
                                                           technology=TechInfo.BLANK_TECHNOLOGY_13.ID)
    do_eco_tech_trigger.new_effect.enable_disable_technology(source_player=player,
                                                              technology=TechInfo.BLANK_TECHNOLOGY_13.ID,
                                                              enabled=True)
    do_eco_tech_trigger.new_effect.script_call(message=f'p{player}_research_defend_eco_tech();')

# La Hire Voicelines
# Play_j6g
# La Hire's sword is not bloody enough.
# Play_j6i
# It is a good day for La Hire to die!
# Play_j3j
# Do your worst, you English fop!
# Play_j3h
# The blood on La Hire's sword is almost dry.
# Play_j3i
# Them English can't make a castle stronger than La Hire!
# Play_j3m
# La Hire wishes to kill something.
la_hire_voicelines = ['Play_j6g', 'Play_j6i', 'Play_j3j', 'Play_j3h', 'Play_j3i', 'Play_j3m']
for player in players:
    la_hire_voiceline_var = t_man.add_variable(f'La Hire Voiceline (p{player})', 20 + player)
    la_hire_roll_voice_trigger = t_man.add_trigger(f'La Hire Roll Voiceline (p{player})', looping=True)
    la_hire_roll_voice_trigger.new_condition.timer(20)
    la_hire_roll_voice_trigger.new_condition.own_objects(source_player=player, object_list=HeroInfo.LA_HIRE.ID,
                                                         quantity=1)
    la_hire_roll_voice_trigger.new_effect.script_call(message=f'la_hire_roll_voiceline_p{player}();')
    for voiceline_i in range(len(la_hire_voicelines)):
        la_hire_voice_trigger = t_man.add_trigger(f'La Hire Voiceline {voiceline_i + 1} (p{player})', enabled=False)
        la_hire_voice_trigger.new_condition.own_objects(source_player=player, object_list=HeroInfo.LA_HIRE.ID,
                                                        quantity=1)
        la_hire_voice_trigger.new_condition.timer(20)
        la_hire_voice_trigger.new_condition.variable_value(variable=la_hire_voiceline_var.variable_id,
                                                           comparison=Comparison.EQUAL, quantity=voiceline_i)
        la_hire_voice_trigger.new_effect.display_instructions(source_player=player, display_time=10, message='La Hire',
                                                              sound_name=la_hire_voicelines[voiceline_i])
        # la_hire_voice_trigger.new_effect.activate_trigger(la_hire_roll_voice_trigger.trigger_id)
        #
        la_hire_roll_voice_trigger.new_effect.activate_trigger(la_hire_voice_trigger.trigger_id)



# Set Hero Stats
PIERCE_ARMOR = (ObjectAttribute.ARMOR, 3)
MELEE_ARMOR = (ObjectAttribute.ARMOR, 4)
PIERCE_ATTACK = (ObjectAttribute.ATTACK, 3)
MELEE_ATTACK = (ObjectAttribute.ATTACK, 4)
heroes = {
    HeroInfo.LA_HIRE: {ObjectAttribute.HIT_POINTS: 1500, ObjectAttribute.ATTACK_RELOAD_TIME: 0.5,
                       MELEE_ARMOR: 5, PIERCE_ARMOR: 5, ObjectAttribute.BLAST_WIDTH: 1,
                       ObjectAttribute.BLAST_ATTACK_LEVEL: 4, MELEE_ATTACK: 20}, # God
    HeroInfo.WILLIAM_WALLACE: {}, # T1 Sword
    HeroInfo.ROBIN_HOOD: {ObjectAttribute.HIT_POINTS: 200, ObjectAttribute.MAX_RANGE: 10}, # T1 Bow
    HeroInfo.HROLF_THE_GANGER: {ObjectAttribute.HIT_POINTS: 250}, # T1 Axe
    UnitInfo.ROYAL_JANISSARY: {ObjectAttribute.HIT_POINTS: 200, ObjectAttribute.ATTACK_RELOAD_TIME: 3,
                               ObjectAttribute.HERO_STATUS: 1}, # T1 Gun
    HeroInfo.BAYINNAUNG: {ObjectAttribute.HIT_POINTS: 1000, MELEE_ARMOR: 5, PIERCE_ARMOR: 5}, # T2 Sword Elephant
    HeroInfo.DAGNAJAN: {ObjectAttribute.HIT_POINTS: 1000, ObjectAttribute.ATTACK_RELOAD_TIME: 2}, # T2 Bow Elephant
    HeroInfo.ABRAHA_ELEPHANT: {ObjectAttribute.HIT_POINTS: 1000, ObjectAttribute.ATTACK_RELOAD_TIME: 1}, # T2 Axe Elephant
    HeroInfo.SUN_QUAN: {ObjectAttribute.HIT_POINTS: 750}, # T2 Gun Elephant
    HeroInfo.ULRICH_VON_JUNGINGEN: {ObjectAttribute.HIT_POINTS: 750}, # T2 Sword Horse
    HeroInfo.GENGHIS_KHAN: {ObjectAttribute.HIT_POINTS: 500, ObjectAttribute.ATTACK_RELOAD_TIME: 1}, # T2 Bow Horse
    HeroInfo.BOHEMOND: {ObjectAttribute.HIT_POINTS: 750, ObjectAttribute.ATTACK_RELOAD_TIME: 1,
                        MELEE_ARMOR: 4, PIERCE_ARMOR: 4}, # T2 Axe Horse
    HeroInfo.FRANCISCO_DE_ORELLANA: {ObjectAttribute.HIT_POINTS: 500, ObjectAttribute.ATTACK_RELOAD_TIME: 2,
                                     PIERCE_ATTACK: 50}, # T2 Gun Horse
    HeroInfo.DARIUS: {ObjectAttribute.HIT_POINTS: 750, ObjectAttribute.ATTACK_RELOAD_TIME: 1,
                      MELEE_ARMOR: 4, PIERCE_ARMOR: 4, ObjectAttribute.BLAST_WIDTH: 2}, # T2 Sword Cart
    HeroInfo.LIU_BIAO: {ObjectAttribute.HIT_POINTS: 500, ObjectAttribute.ATTACK_RELOAD_TIME: 2}, # T2 Bow Cart
    HeroInfo.TSAR_KONSTANTIN: {ObjectAttribute.HIT_POINTS: 750, ObjectAttribute.ATTACK_RELOAD_TIME: 1,
                               MELEE_ARMOR: 8}, # T2 Axe Cart
    HeroInfo.JEAN_DE_LORRAIN: {ObjectAttribute.HIT_POINTS: 200, ObjectAttribute.TOTAL_MISSILES: 10,
                               ObjectAttribute.ATTACK_RELOAD_TIME: 3, ObjectAttribute.ATTACK_DISPERSION: 0.5,
                               ObjectAttribute.ACCURACY_PERCENT: 10, ObjectAttribute.MAX_TOTAL_MISSILES: 10}, # T2 Gun Cart
    HeroInfo.MINAMOTO: {ObjectAttribute.HIT_POINTS: 500, ObjectAttribute.ATTACK_RELOAD_TIME: 0.25,
                        MELEE_ARMOR: 5, PIERCE_ARMOR: 5}, # T2 Sword Cape
    HeroInfo.SU_DINGFANG: {ObjectAttribute.ATTACK_RELOAD_TIME: 1, ObjectAttribute.MAX_RANGE: 10}, # T2 Bow Cape
    HeroInfo.HARALD_HARDRADA: {ObjectAttribute.HIT_POINTS: 300, ObjectAttribute.ATTACK_RELOAD_TIME: 0.25,
                               MELEE_ARMOR: 5, PIERCE_ARMOR: 5}, # T2 Axe Cape
    HeroInfo.MUSTAFA_PASHA: {ObjectAttribute.HIT_POINTS: 300, ObjectAttribute.ATTACK_RELOAD_TIME: 1,
                             PIERCE_ARMOR: 2} # T2 Gun Cape
}
for player in players:
    setup_heroes = t_man.add_trigger(f'Setup Heroes p({player})')
    for hero, attributes in heroes.items():
        attributes[ObjectAttribute.REGENERATION_RATE] = 100
        for attribute, value in attributes.items():
            if isinstance(attribute, tuple):
                setup_heroes.new_effect.modify_attribute(
                    source_player=player, object_list_unit_id=hero.ID, object_attributes=attribute[0],
                    operation=Operation.SET, armour_attack_class=attribute[1], armour_attack_quantity=value)
            elif isinstance(value, str):
                setup_heroes.new_effect.modify_attribute(
                    source_player=player, object_list_unit_id=hero.ID, object_attributes=attribute,
                    operation=Operation.SET, message=value)
            else:
                setup_heroes.new_effect.modify_attribute(
                    source_player=player, object_list_unit_id=hero.ID, object_attributes=attribute,
                    operation=Operation.SET, quantity=value)

# AI Player Setup
for ai in attacker_ais:
    setup_ai_trigger = t_man.add_trigger(f'Setup P{ai}')
    setup_ai_trigger.new_effect.modify_attribute(source_player=ai, object_list_unit_id=BuildingInfo.CASTLE.ID,
                                                 object_attributes=ObjectAttribute.GARRISON_TYPE,
                                                 operation=Operation.SET, quantity=127)
    setup_ai_trigger.new_effect.modify_attribute(source_player=ai, object_list_unit_id=BuildingInfo.CASTLE.ID,
                                                 object_attributes=ObjectAttribute.GARRISON_CAPACITY,
                                                 operation=Operation.SET, quantity=500)


# In game events
TRIGGER_EVENT_VAR_ID = 10
EVENT_NUMBER_LIST = [
    'Zero Index',
    'Neutral Event - Wolves',
    'Attack Event - Flaming Camels'
]

# Attack Event - Flaming Camels
event_flaming_camels = t_man.add_trigger(f'Attack Event - Flaming Camels', looping=True)
event_flaming_camels.new_condition.variable_value(variable=TRIGGER_EVENT_VAR_ID, comparison=Comparison.EQUAL,
                                                  quantity=EVENT_NUMBER_LIST.index(event_flaming_camels.name))
event_flaming_camels.new_effect.change_variable(variable=TRIGGER_EVENT_VAR_ID, operation=Operation.SET,
                                                quantity=0)
for ai in attacker_ais:
    castle = ATTACK_CASTLES[attacker_ais.index(ai)]
    for i in range(33):
        event_flaming_camels.new_effect.create_garrisoned_object(source_player=ai, object_list_unit_id=UnitInfo.FLAMING_CAMEL.ID,
                                                                 object_list_unit_id_2=BuildingInfo.CASTLE.ID, max_units_affected=3)
        event_flaming_camels.new_effect.task_object(source_player=ai, object_list_unit_id=BuildingInfo.CASTLE.ID,
                                                    action_type=ActionType.UNGARRISON)


print(t_man.get_summary_as_string())
q = input('Save?')
if q.lower() == 'y' or q.lower() == 'yes':
    scenario.write_to_file(output_path)