const int var_event_type_dice = 0;
const int var_player_dice = 1;
const int var_side_dice = 2;
const int var_event_dice = 3;

void roll_all_dice() {
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

int roll_dice(int dice_no, int sides) {
    int num = xsGetRandomNumberMax(sides) + 1;
    xsSetTriggerVariable(dice_no, num);
    return num
}

void event_roll() {
    // xsSetTriggerVariable(var_event_dice, -10000); // Event Chance
    // xsSetTriggerVariable(var_player_dice, -4); // Player select
    // xsSetTriggerVariable(var_side_dice, -2); // Side select

    // roll_dice();
    int event_type = roll_dice(var_event_type_dice, 100);
    if (event_type == 100) {
        do_common_event();
    }
}

void do_common_event() {
    int side = roll_dice(var_player_dice, 3);
    switch(side) {
        case 1 : {
            do_common_attack_event();
        }
        case 2 : {
            do_common_defend_event();
        }
        default : {
            do_common_neutral_event();
        }
    }
}

void do_common_attack_event() {
    int player = roll_dice(var_player_dice, 4);
    int event = roll_dice(var_event_dice, 5);
    switch(event) {
        case 1 : {
            re_melee_attack(player);
        }
        case 2 : {
            re_infantry_armor(player); 
        }
        case 3 : {
            re_cavalry_armor(player);
        }
        case 4 : {
            re_archer_attack(player);
        }
        case 5 : {
            re_archer_armor(player);
        }
    }
}

void do_common_defend_event() {
    int player = roll_dice(var_player_dice, 3);
    int event = roll_dice(var_event_dice, 5);
    switch(event) {
        case 1 : {

        }
    }
}

// ===== Common Defend Events =====
int attack_unique_techs = set_defend_unique_techs();
void set_defend_unique_techs() {
    int list = xsArrayCreateInt(10,);
    xsArraySetInt(list, 0, );
    return list;
}

void re_(int player) {
    xsResearchTechnology(int techID, bool force, bool techAvailable, player);
}

// ===== Common Attack Events =====
void re_cavalry_armor(int player) {
    xsResearchTechnology(80, false, true, player);
    xsResearchTechnology(82, false, true, player); 
    xsResearchTechnology(81, false, true, player); 
}

void re_infantry_armor(int player) {
    xsResearchTechnology(77, false, true, player);
    xsResearchTechnology(76, false, true, player); 
    xsResearchTechnology(74, false, true, player); 
}

void re_archer_armor(int player) {
    xsResearchTechnology(219, false, true, player);
    xsResearchTechnology(212, false, true, player); 
    xsResearchTechnology(211, false, true, player); 
}

void re_archer_attack() {
    xsResearchTechnology(201, false, true, player); // Bracer
    xsResearchTechnology(200, false, true, player); // Bodkin Arrow
    xsResearchTechnology(199, false, true, player); // Fletching
}

void re_melee_attack () {
    xsResearchTechnology(75, false, true, player); // Blast Furnace
    xsResearchTechnology(68, false, true, player); // Iron Casting
    xsResearchTechnology(67, false, true, player); // Forging Furnace
}