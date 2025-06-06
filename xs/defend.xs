const int var_event_dice = 0;

void roll_dice() {
    for (var = 0; < 10) {
        int sides = 1000;
        if(xsTriggerVariable(var) < 0) {
            sides = xsTriggerVariable(var) * -1;
        }
        int num = xsGetRandomNumberMax(sides) + 1;
        xsChatData("Set Dice "+var+1+" to "+num+" out of "+sides,);
        xsSetTriggerVariable(var, num);
    }
}

void event_roll() {
    xsSetTriggerVariable(var_event_dice, -100); /* Event Chance */

    roll_dice();
    if (xsTriggerVariable(var_event_dice) <= 100) {
        xsResearchTechnology(75, false, true, 4); // Blast Furnace
        xsResearchTechnology(68, false, true, 4); // Blast Furnace
        xsResearchTechnology(67, false, true, 4); // Blast Furnace
    }
}