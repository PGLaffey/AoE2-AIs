from AoE2ScenarioParser.objects.data_objects.trigger import Trigger
from AoE2ScenarioParser.objects.support.trigger_select import TriggerSelect
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario
from AoE2ScenarioParser.datasets.techs import TechInfo

scenario_folder = 'C:/Users/User/Games/Age of Empires 2 DE/76561198138036391/resources/_common/scenario'
input_path = f'{scenario_folder}/war of empires.aoe2scenario'
output_path = f'{scenario_folder}/war of empires - python.aoe2scenario'

xs_path = 'C:/Program Files (x86)/Steam/steamapps/common/AoE2DE/resources/_common/xs/war_of_empires.xs'

scenario = AoE2DEScenario.from_file(input_path)
t_man = scenario.trigger_manager

player_list = [
    {'player': 1, 'eco': 3, 'army': 5},
    {'player': 2, 'eco': 4, 'army': 8}
]

archery_upgrades = [TechInfo.CROSSBOWMAN, TechInfo.ARBALESTER, TechInfo.ELITE_SKIRMISHER, TechInfo.IMPERIAL_SKIRMISHER,
                    TechInfo.HEAVY_CAVALRY_ARCHER, TechInfo.ELITE_ELEPHANT_ARCHER, TechInfo.ELITE_GENITOUR,
                    TechInfo.THUMB_RING, TechInfo.PARTHIAN_TACTICS]
barrack_upgrades = [TechInfo.MAN_AT_ARMS, TechInfo.LONG_SWORDSMAN, TechInfo.TWO_HANDED_SWORDSMAN, TechInfo.CHAMPION,
                    TechInfo.LEGIONARY, TechInfo.ARSON, TechInfo.GAMBESONS, TechInfo.PIKEMAN, TechInfo.HALBERDIER,
                    TechInfo.EAGLE_WARRIOR, TechInfo.ELITE_EAGLE_WARRIOR, (982, 'Elite Fire Lancer'), # Elite Fire Lancer
                    TechInfo.SQUIRES]
stable_upgrades = [TechInfo.LIGHT_CAVALRY, TechInfo.HUSSAR, TechInfo.WINGED_HUSSAR, TechInfo.BLOODLINES,
                   TechInfo.ELITE_SHRIVAMSHA_RIDER, TechInfo.CAVALIER, TechInfo.PALADIN, TechInfo.SAVAR,
                   TechInfo.ELITE_STEPPE_LANCER, TechInfo.HEAVY_CAMEL_RIDER, TechInfo.IMPERIAL_CAMEL_RIDER,
                   TechInfo.ELITE_BATTLE_ELEPHANT, TechInfo.HUSBANDRY, (1033, 'Heavy Hei Guang Cavalry') # Heavy Hei Guang Cavalry
                   ]
siege_upgrades = [TechInfo.CAPPED_RAM, TechInfo.SIEGE_RAM, TechInfo.SIEGE_ELEPHANT, TechInfo.ONAGER,
                  TechInfo.SIEGE_ONAGER, TechInfo.HEAVY_SCORPION, TechInfo.HOUFNICE, (980, 'Heavy Rocket Cart') # Heavy Rocket Cart
                  ]
other_upgrades = [TechInfo.BALLISTICS, TechInfo.CHEMISTRY, TechInfo.SIEGE_ENGINEERS, TechInfo.SPIES_AND_TREASON,
                  TechInfo.FEUDAL_AGE, TechInfo.CASTLE_AGE, TechInfo.IMPERIAL_AGE, TechInfo.TREADMILL_CRANE]

# Add Eco Upgrades
eco_upgrades = TechInfo.eco_techs() + other_upgrades
for player in player_list:
    for tech_obj in eco_upgrades:
        try:
            tech = tech_obj.value[0]
            tech_name = tech_obj.name.capitalize()
        except AttributeError:
            tech = tech_obj[0]
            tech_name = tech_obj[1].capitalize()
        trigger = t_man.add_trigger(f'Research {tech_name} (p{player["player"]})')
        trigger.new_condition.research_technology(source_player=player['player'], technology=tech)
        trigger.new_effect.research_technology(source_player=player['eco'], technology=tech, force_research_technology=True)

# Add Army Upgrades
army_upgrades = (TechInfo.blacksmith_techs() + archery_upgrades + barrack_upgrades + stable_upgrades + siege_upgrades +
                 other_upgrades)
for player in player_list:
    for tech_obj in army_upgrades:
        try:
            tech = tech_obj.value[0]
            tech_name = tech_obj.name.capitalize()
        except AttributeError:
            tech = tech_obj[0]
            tech_name = tech_obj[1].capitalize()
        trigger = t_man.add_trigger(f'Research {tech_name} (p{player["player"]})')
        trigger.new_condition.research_technology(source_player=player['player'], technology=tech)
        trigger.new_effect.research_technology(source_player=player['army'], technology=tech, force_research_technology=True)




print(t_man.get_summary_as_string())
q = input('Save?')
if q.lower() == 'y' or q.lower() == 'yes':
    scenario.write_to_file(output_path)