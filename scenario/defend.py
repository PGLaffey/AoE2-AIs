from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.heroes import HeroInfo
from AoE2ScenarioParser.objects.support.enums.group_by import GroupBy
from AoE2ScenarioParser.objects.support.trigger_select import TriggerSelect
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

input_path = 'C:/Users/User/Games/Age of Empires 2 DE/76561198138036391/resources/_common/scenario/Defend.aoe2scenario'
output_path = 'C:/Users/User/Games/Age of Empires 2 DE/76561198138036391/resources/_common/scenario/Defend - Python.aoe2scenario'

scenario = AoE2DEScenario.from_file(input_path)

trigger_manager = scenario.trigger_manager

hoh_trigger = trigger_manager.get_trigger(23)
trigger_manager.copy_trigger_tree_per_player(
    from_player=PlayerId.ONE,
    trigger_select=23,
    create_copy_for_players=[PlayerId.TWO, PlayerId.THREE],
    group_triggers_by=GroupBy.PLAYER,
    include_player_source=True,
    include_player_target=True
)

print(trigger_manager.get_summary_as_string())
q = input('Save?')
if q.lower() == 'y' or q.lower() == 'yes':
    scenario.write_to_file(output_path)