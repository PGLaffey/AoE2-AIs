from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.techs import TechInfo
from AoE2ScenarioParser.datasets.trigger_lists import Attribute
from AoE2ScenarioParser.objects.data_objects.trigger import Trigger


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class CustomTech:
    def __init__(self, override_tech: TechInfo.ID, name: str = None, icon: TechInfo.ICON_ID = None,
                 description: str = None, cost: list[tuple[Attribute, int]] = None, research_time: int = None,
                 stacking: int = None):
        self.override_tech = override_tech
        self.name = name or 'Placeholder'
        self.icon = icon or TechInfo.SUPREMACY.ICON_ID
        self.description = f'<cost> {description or self.name}'
        self.cost = cost
        self.research_time = research_time or 30
        self.stacking = stacking
        self._applications = {}

    def add_to_building(self, player: int, building: BuildingInfo.ID, location: int, trigger: Trigger):
        params = {'source_player': player, 'technology': self.override_tech}
        trigger.new_effect.enable_disable_technology(**params, enabled=True)
        trigger.new_effect.change_technology_name(**params, message=self.name)
        trigger.new_effect.change_technology_icon(**params, quantity=self.icon)
        trigger.new_effect.change_technology_research_time(**params, quantity=self.research_time)
        trigger.new_effect.change_technology_description(**params, message=self.description)
        if self.cost is not None:
            cost = {}
            for i, resource, amount in enumerate(self.cost):
                cost[f'resource_{i}'] = resource
                cost[f'resource_{i}_quantity'] = amount
            trigger.new_effect.change_technology_cost(**params, **cost)
        trigger.new_effect.change_technology_location(**params, object_list_unit_id_2=building,
                                                      button_location=location)
        if self.stacking:
            trigger.new_effect.enable_technology_stacking(**params, quantity=self.stacking)
        if self._applications[player]:
            self._applications[player].append((building, location))
        else:
            self._applications[player] = [(building, location)]

    def update(self, player: int, trigger: Trigger, name: str = None, icon: TechInfo.ICON_ID = None,
               description: str = None, cost: list[tuple[Attribute, int]] = None, research_time: int = None,
               stacking: int = None):
        self.name = name or self.name
        self.icon = icon or self.icon
        if description:
            self.description = f'<cost> {description}'
        self.cost = cost or self.cost
        self.research_time = research_time or self.research_time
        self.stacking = stacking or self.stacking
        for building, location in self._applications[player]:
            self.add_to_building(player, building, location, trigger)

