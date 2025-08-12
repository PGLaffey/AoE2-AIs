const int var_event_type_dice = 0;
const int var_player_dice = 1;
const int var_side_dice = 2;
const int var_event_dice = 3;
const int var_quantity_dice = 4;

const int var_trigger_event = 10;

int test = 0;
int defend_unique_techs = 0;
int defend_unique_techs_desc = 0;
int defend_unique_techs_status = 0;

int defend_defense_techs = 0;
int defend_defense_techs_desc = 0;
int defend_defense_techs_status = 0;

int defend_eco_techs = 0;
int defend_eco_techs_desc = 0;
int defend_eco_techs_status = 0;

int defend_unit_techs = 0;
int defend_unit_techs_desc = 0;
int defend_unit_techs_status = 0;

void roll_all_dice() {
    for (var = 0; < 10) {
        int sides = 1000;
        if(xsTriggerVariable(var) < 0) {
            sides = xsTriggerVariable(var) * -1;
        }
        int num = xsGetRandomNumberMax(sides) + 1;
        xsChatData("Set Dice "+var+1+" to "+num+" out of "+sides);
        xsSetTriggerVariable(var, num);
    }
}

int roll_dice(int dice_no = 0, int sides = 1) {
    int num = xsGetRandomNumberMax(sides) + 1;
    xsSetTriggerVariable(dice_no, num);
    return (num);
}

void roll_dice_unused(int dice_no = 0) {
    int sides = 1000;
    if(xsTriggerVariable(dice_no) < 0) {
        sides = xsTriggerVariable(dice_no) * -1;
    }
    int num = xsGetRandomNumberMax(sides) + 1;
    xsSetTriggerVariable(dice_no, num);
}

// ===== Common Defend Events =====
int set_defend_unique_techs() {
    int list = xsArrayCreateInt(54, 0, "defend_unique_techs");
    xsArraySetInt(list, 0, 912); // Feteters
    xsArraySetInt(list, 1, 460); // Atlatl
    xsArraySetInt(list, 2, 24); // Garland Wars
    xsArraySetInt(list, 3, 834); // Mahayana
    xsArraySetInt(list, 4, 578); // Kabash
    xsArraySetInt(list, 5, 3); // Yeomen
    xsArraySetInt(list, 6, 685); // Stirrups
    xsArraySetInt(list, 7, 686); // Bagains
    xsArraySetInt(list, 8, 754); // Burgundian Vineyards
    xsArraySetInt(list, 9, 627); // Manipur Cavalry
    xsArraySetInt(list, 10, 482); // Stronghold
    xsArraySetInt(list, 11, 5); // Furor Celtica
    xsArraySetInt(list, 12, 462); // Great Wall
    xsArraySetInt(list, 13, 690); // Cuman Mercenaries
    xsArraySetInt(list, 14, 832); // Wootz Steel
    xsArraySetInt(list, 15, 923); // Svan Towers
    xsArraySetInt(list, 16, 924); // Aznauri Cavalry
    xsArraySetInt(list, 17, 835); // Kshatriyas
    xsArraySetInt(list, 18, 506); // Grant Trunk Road
    xsArraySetInt(list, 19, 507); // Shatangi
    xsArraySetInt(list, 20, 516); // Andean Sling
    xsArraySetInt(list, 21, 499); // Silk Road
    xsArraySetInt(list, 22, 494); // Pirotechnia
    xsArraySetInt(list, 23, 484); // Yasama
    xsArraySetInt(list, 24, 996); // Fortified Bastions
    xsArraySetInt(list, 25, 1006); // Lamellar Armor
    xsArraySetInt(list, 26, 1007); // Ordo Cavalry
    xsArraySetInt(list, 27, 486); // Eupseong
    xsArraySetInt(list, 28, 692); // Tower Shields
    xsArraySetInt(list, 29, 515); // Recurve Bow
    xsArraySetInt(list, 30, 625); // Forced Levy
    xsArraySetInt(list, 31, 577); // Farimba
    xsArraySetInt(list, 32, 485); // Hulche Javelineers
    xsArraySetInt(list, 33, 7); // Citadels
    xsArraySetInt(list, 34, 783); // Lechitic Legacy
    xsArraySetInt(list, 35, 573); // Arquebus
    xsArraySetInt(list, 36, 883); // Ballistas
    xsArraySetInt(list, 37, 884); // Comitatenses
    xsArraySetInt(list, 38, 28); // Birmaristan
    xsArraySetInt(list, 39, 1070); // Coiled Serpent Array
    xsArraySetInt(list, 40, 1069); // Bolt Magazine
    xsArraySetInt(list, 41, 757); // Hauberk
    xsArraySetInt(list, 42, 455); // Detinets
    xsArraySetInt(list, 43, 513); // Druzhina
    xsArraySetInt(list, 44, 440); // Supremacy
    xsArraySetInt(list, 45, 687); // Silk Armor
    xsArraySetInt(list, 46, 11); // Crenellations
    xsArraySetInt(list, 47, 491); // Sipahi
    xsArraySetInt(list, 48, 10); // Artillery
    xsArraySetInt(list, 49, 629); // Paper Money
    xsArraySetInt(list, 50, 463); // Chieftains
    xsArraySetInt(list, 51, 49); // Bigsveigar
    xsArraySetInt(list, 52, 1061); // Tuntian
    xsArraySetInt(list, 53, 1062); // Ming Guang Armor
    xsArraySetInt(list, 54, 488); // Kamandaran
    xsArraySetInt(list, 55, 782); // Szlachta Privileges
    return (list);
}
int set_defend_unique_techs_descriptions() {
    int list = xsArrayCreateString(54, "", "defend_unique_techs_desc");
    xsArraySetString(list, 0, "Fereters: Infantry +30 HP"); // Feteters
    xsArraySetString(list, 1, "Atlatl: Skirmishers +1 attack and range"); // Atlatl
    xsArraySetString(list, 2, "Garland Wars: Infantry units: +4 attack"); // Garland Wars
    xsArraySetString(list, 3, "Mahayana: Villagers and Monks take -10% Population space"); // Mahayana
    xsArraySetString(list, 4, "Kasbah: Castles: +25% team work speed"); // Kabash
    xsArraySetString(list, 5, "Yeomen	Foot archers: +1 range and Towers: +2 attack"); // Yeomen
    xsArraySetString(list, 6, "Stirrups	Cavalry units: +33% attack speed"); // Stirrups
    xsArraySetString(list, 7, "Bagains	Two-Handed Swordsman: +5 melee armor"); // Bagains
    xsArraySetString(list, 8, "Burgundian Vineyards	Villagers generate 0.017 gold per second while working on Farms"); // Burgundian Vineyards
    xsArraySetString(list, 9, "Manipur Cavalry	Cavalry units: +4 attack against archers"); // Manipur Cavalry
    xsArraySetString(list, 10, "Stronghold	Castles and Towers: +33% attack speed and Castles heal 30 hit points per minute for allied infantry in a 7 tile radius"); // Stronghold
    xsArraySetString(list, 11, "Furor Celtica	Siege Workshop units: +40% hit points"); // Furor Celtica
    xsArraySetString(list, 12, "Great Wall	Walls and towers: +30% hit points"); // Great Wall
    xsArraySetString(list, 13, "Cuman Mercenaries	Allied players can train up to 5 free Elite Kipchaks per Castle"); // Cuman Mercenaries
    xsArraySetString(list, 14, "Wootz Steel	Infantry and cavalry units ignore armor"); // Wootz Steel
    xsArraySetString(list, 15, "Svan Towers	Defensive buildings +2 attack; Towers fire arrows that pierce multiple units"); // Svan Towers
    xsArraySetString(list, 16, "Aznauri Cavalry	Cavalry units take 15% less population space"); // Aznauri Cavalry
    xsArraySetString(list, 17, "Kshatriyas	Military units cost -25% food"); // Kshatriyas
    xsArraySetString(list, 18, "Grand Trunk Road	+10% gold gather speed from all sources (Gold Mines, trade, and Relics) and Trading fee reduced to 10%"); // Grant Trunk Road
    xsArraySetString(list, 19, "Shatagni	Hand Cannoneers: +2 range"); // Shatangi
    xsArraySetString(list, 20, "Andean Sling	Minimum range of Skirmishers and Slingers removed and Slingers: +1 attack"); // Andean Sling
    xsArraySetString(list, 21, "Silk Road	Trade Cart and Trade Cog cost -50%"); // Silk Road
    xsArraySetString(list, 22, "Pirotechnia	Hand Cannoneer: +15% pass-through damage, 90% accurate"); // Pirotechnia
    xsArraySetString(list, 23, "Yasama	Towers fire 2 additional arrows"); // Yasama
    xsArraySetString(list, 24, "Fortified Bastions	Castles, Town Centers, walls, gates, and towers to regenerate 500 hit points per minute."); // Fortified Bastions
    xsArraySetString(list, 25, "Lamellar Armor	Infantry and Skirmishers reflect 25% melee damage back to the attacker"); // Lamellar Armor
    xsArraySetString(list, 26, "Ordo Cavalry	Cavalry regenerates HP in combat"); // Ordo Cavalry
    xsArraySetString(list, 27, "Eupseong	Watch Tower-line: +2 range"); // Eupseong
    xsArraySetString(list, 28, "Tower Shields	Spearman-line and Skirmishers: +2 pierce armor"); // Tower Shields
    xsArraySetString(list, 29, "Recurve Bow	Mounted archers: +1 attack and range"); // Recurve Bow
    xsArraySetString(list, 30, "Forced Levy	Militia-line costs +20 food, -20 gold"); // Forced Levy
    xsArraySetString(list, 31, "Farimba	Cavalry units: +5 attack"); // Farimba
    xsArraySetString(list, 32, "Hul'che Javelineers	Skirmishers throw extra spear that deals 1 damage"); // Hulche Javelineers
    xsArraySetString(list, 33, "Citadels	Castles +4 pierce attack, +3 attack vs rams, +3 attack vs infantry, receive -25% bonus damage"); // Citadels
    xsArraySetString(list, 34, "Lechitic Legacy	Scout-line have +0.5 blast radius [33% effect]"); // Lechitic Legacy
    xsArraySetString(list, 35, "Arquebus	Improved gunpowder unit accuracy against moving targets and +0.5 gunpowder projectile speed, +0.2 for Bombard Cannon and Bombard Tower"); // Arquebus
    xsArraySetString(list, 36, "Ballistas	Scorpions: +33% attack speed and Galley-line: +2 attack"); // Ballistas
    xsArraySetString(list, 37, "Comitatenses	Militia-line, Knight-line, and Centurions train 50% faster and receive +5 charge attack."); // Comitatenses
    xsArraySetString(list, 38, "Bimaristan	Monks automatically heal multiple nearby units."); // Birmaristan
    xsArraySetString(list, 39, "Coiled Serpent Array	Spearman-line and White Feather Guards gain additional HP when near each other."); // Coiled Serpent Array
    xsArraySetString(list, 40, "Bolt Magazine	Archer-line, War Chariots and Lou Chuans fire additional projectiles"); // Bolt Magazine
    xsArraySetString(list, 41, "Hauberk	Knight-line: +1/+2 armor"); // Hauberk
    xsArraySetString(list, 42, "Detinets	Replaces 40% of Castles' and towers' stone cost with wood"); // Detinets
    xsArraySetString(list, 43, "Druzhina	Infantry units have +0.5 blast radius [+5 effect]"); // Druzhina
    xsArraySetString(list, 44, "Supremacy	Villagers: +6 attack, +2/+2 armor, and +40 hit points"); // Supremacy
    xsArraySetString(list, 45, "Silk Armor	Scout-line, Steppe Lancer, and mounted archers: +1/+1 armor"); // Silk Armor
    xsArraySetString(list, 46, "Crenellations	Castles: +3 range and Garrisoned infantry fire arrows"); // Crenellations
    xsArraySetString(list, 47, "Sipahi	Mounted archers: +20 hit points"); // Sipahi
    xsArraySetString(list, 48, "Artillery	Bombard Tower, Bombard Cannon, and Cannon Galleon: +2 range"); // Artillery
    xsArraySetString(list, 49, "Paper Money	Villagers generate 0.014 gold per second while gathering wood"); // Paper Money
    xsArraySetString(list, 50, "Chieftains	Infantry: +5 attack against cavalry units, +4 against camel units, and generate 5 gold when killing Villagers, 20 gold when killing trade units and Monks"); // Chieftains
    xsArraySetString(list, 51, "Bogsveigar	Archer-line and Longboats: +1 attack"); // Bigsveigar
    xsArraySetString(list, 52, "Tuntian	Soldiers passively produce food"); // Tuntian
    xsArraySetString(list, 53, "Ming Guang Armor	Cavalry +2 attack vs. Siege Weapons"); // Ming Guang Armor
    xsArraySetString(list, 54, "Kamandaran	Archer-line costs 60 wood instead of 25 wood, 45 gold"); // Kamandaran
    xsArraySetString(list, 55, "Szlachta Privileges	Knight-line costs -60% gold"); // Szlachta Privileges
    return (list);
}

void re_defend_unique_tech(int tech_index = 0, int player = 0) {
    int status = xsArrayGetInt(defend_unique_techs_status, tech_index);
    int tech_id = xsArrayGetInt(defend_unique_techs, tech_index);
    string tech_desc = xsArrayGetString(defend_unique_techs_desc, tech_index);
    xsChatData("Player "+player+" researched "+tech_desc);
    switch (player) {
        case 1 : {
            if (status % 2 < 1) {
                xsResearchTechnology(tech_id, true, false, player);
                xsArraySetInt(defend_unique_techs_status, tech_index, status + 1);
            }
        }
        case 2 : {
            if (status / 2 % 2 < 1) {
                xsResearchTechnology(tech_id, true, false, player);
                xsArraySetInt(defend_unique_techs_status, tech_index, status + 2);
            }
        }
        case 3 : {
            if (status / 2 / 2 % 2 < 1) {
                xsResearchTechnology(tech_id, true, false, player);
                xsArraySetInt(defend_unique_techs_status, tech_index, status + 4);
            }
        }
        case 4 : {
            if (status / 2 / 2 / 2 % 2 < 1) {
                xsResearchTechnology(tech_id, true, false, player);
                xsArraySetInt(defend_unique_techs_status, tech_index, status + 8);
            }
        }
    }
}
// ===== (END) Common Defend Events =====

// ===== Common Attack Events =====
void re_cavalry_armor(int player = 0) {
    xsResearchTechnology(80, false, true, player);
    xsResearchTechnology(82, false, true, player);
    xsResearchTechnology(81, false, true, player);
}

void re_infantry_armor(int player = 0) {
    xsResearchTechnology(77, false, true, player);
    xsResearchTechnology(76, false, true, player);
    xsResearchTechnology(74, false, true, player);
}

void re_archer_armor(int player = 0) {
    xsResearchTechnology(219, false, true, player);
    xsResearchTechnology(212, false, true, player);
    xsResearchTechnology(211, false, true, player);
}

void re_archer_attack(int player = 0) {
    xsResearchTechnology(201, false, true, player); // Bracer
    xsResearchTechnology(200, false, true, player); // Bodkin Arrow
    xsResearchTechnology(199, false, true, player); // Fletching
}

void re_melee_attack (int player = 0) {
    xsResearchTechnology(75, false, true, player); // Blast Furnace
    xsResearchTechnology(68, false, true, player); // Iron Casting
    xsResearchTechnology(67, false, true, player); // Forging Furnace
}
// ===== (END) Common Attack Events =====

// ===== Common Neutral Events =====
void spawn_deer() {
    int quantity = roll_dice(var_quantity_dice, 50);
    xsEffectAmount(cGaiaModResource, cAttributeSpawnCap, cAttributeSet, 15);
    xsEffectAmount(cGaiaSpawnUnit, 65, 109, quantity);
    xsChatData("Spring has come and the deer flourish");
}
// ===== (END) Common Neutral Events =====

void do_common_attack_event() {
    int player = roll_dice(var_player_dice, 4) + 3;
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
    int event = roll_dice(var_event_dice, 57);
    if (event <= xsArrayGetSize(defend_unique_techs)) {
        re_defend_unique_tech(event, player);
    } else {
        switch(event - xsArrayGetSize(defend_unique_techs)) {
            case 1 : {
                xsChatData("Event 55");
            }
        }
    }
}

void do_common_neutral_event() {
    int event = roll_dice(var_event_dice, 2);
    switch(event) {
        case 1 : {
            spawn_deer();
        }
        case 2 : {
            xsSetTriggerVariable(var_trigger_event, 1);
            xsChatData("Winter has come and hungry wolves decend the mountains");
        }
    }
}

void do_common_event() {
    int side = roll_dice(var_side_dice, 11);
    if (side <= 5) {
        do_common_attack_event();
    } else if (side <= 10) {
        do_common_defend_event();
    }
    else {
        do_common_neutral_event();
    }
}

void do_uncommon_event() {
    int side = roll_dice(var_side_dice, 1);
}

void event_roll() {
    int event_type = roll_dice(var_event_type_dice, 1000);
    if (event_type <= 20) {
        // 20 in 1000 or 1 in 50 or 2%
        do_common_event();
    } else if (event_type <= 5) {
        // 5 in 1000 or 1 in 200 or 0.5%
        do_uncommon_event();
    }
    roll_dice_unused(4);
    roll_dice_unused(5);
    roll_dice_unused(6);
    roll_dice_unused(7);
    roll_dice_unused(8);
    roll_dice_unused(9);
}

bool check_research_status(int status_list = 0, int index = 0, int player = 0) {
    int status = xsArrayGetInt(status_list, index);
    bool available = false;
    switch (player) {
        case 1 : {
            available = status % 2 < 1;
        }
        case 2 : {
            available = status / 2 % 2 < 1;
        }
        case 3 : {
            available = status / 2 / 2 % 2 < 1;
        }
        case 4 : {
            available = status / 2 / 2 / 2 % 2 < 1;
        }
    }
    return (available);
}

void research_defend_tech(int list = 0, int status_list = 0, int description_list = 0, int player = 0) {
    int i = xsGetRandomNumberMax(xsArrayGetSize(list));
    if check_research_status(status_list, i, player) {
        xsResearchTechnology(xsArrayGetInt(list, i), true, false, player);
        string colour = "";
        int status_binary = 0
        switch(player) {
            case 1 : {
                colour = "<blue>";
                status_binary = 1;
            }
            case 2 : {
                colour = "<red>";
                status_binary = 2;
            }
            default : {
                colour = "<green>";
                status_binary = 4;
            }
        }
        xsChatData(colour + "Player " + player + " Researched " + xsArrayGetString(description_list, i));
        xsArraySetInt(status_list, i, xsArrayGetInt(status_list, i) + status_binary);
    } else {
        xsChatData("Player " + player + " Already Researched " + xsArrayGetString(description_list, i) + " Retrying");
        research_defend_tech(list, status_list, description_list, player);
    }
}

void research_defend_defense_tech(int player = 0) {
    research_defend_tech(defend_defense_techs, defend_defense_techs_status, defend_defense_techs_desc, player);
}
void research_defend_eco_tech(int player = 0) {
    research_defend_tech(defend_eco_techs, defend_eco_techs_status, defend_eco_techs_desc, player);
}
void research_defend_unit_tech(int player = 0) {
    research_defend_tech(defend_unit_techs, defend_unit_techs_status, defend_unit_techs_desc, player);
}

// Player research techs entrypoints
void p1_research_defend_defense_tech() {
    research_defend_defense_tech(1);
}
void p1_research_defend_eco_tech() {
    research_defend_eco_tech(1);
}
void p1_research_defend_unit_tech() {
    research_defend_unit_tech(1);
}

void p2_research_defend_defense_tech() {
    research_defend_defense_tech(2);
}
void p2_research_defend_eco_tech() {
    research_defend_eco_tech(2);
}
void p2_research_defend_unit_tech() {
    research_defend_unit_tech(2);
}

void p3_research_defend_defense_tech() {
    research_defend_defense_tech(3);
}
void p3_research_defend_eco_tech() {
    research_defend_eco_tech(3);
}
void p3_research_defend_unit_tech() {
    research_defend_unit_tech(3);
}

// Set Research Lists
int set_defend_defense_techs() {
    int list = xsArrayCreateInt(19, 0, "defend_defense_techs");
    xsArraySetInt(list, 0, 756);  // Hussite Reforms
    xsArraySetInt(list, 1, 3);    // Yeomen
    xsArraySetInt(list, 2, 755);  // Flemish Revolution
    xsArraySetInt(list, 3, 408);  // Greek Fire
    xsArraySetInt(list, 4, 482);  // Stronghold
    xsArraySetInt(list, 5, 462);  // Great Wall
    xsArraySetInt(list, 6, 923);  // Svan Towers
    xsArraySetInt(list, 7, 484);  // Yasama
    xsArraySetInt(list, 8, 996);  // Fortified Bastions
    xsArraySetInt(list, 9, 486);  // Eupseong
    xsArraySetInt(list, 10, 626); // Hill Forts
    xsArraySetInt(list, 11, 576); // Tigui
    xsArraySetInt(list, 12, 7);   // Citadels
    xsArraySetInt(list, 13, 28);  // Bimaristan
    xsArraySetInt(list, 14, 758); // First Crusade
    xsArraySetInt(list, 15, 455); // Detinets
    xsArraySetInt(list, 16, 23);  // Inquisition
    xsArraySetInt(list, 17, 11);  // Crenellations
    xsArraySetInt(list, 18, 10);  // Artillery
    return (list);
}

int set_defend_defense_techs_descriptions() {
    int list = xsArrayCreateString(19, "", "defend_defense_techs_desc");
    xsArraySetString(list, 0, "Hussite Reforms: Monks and Monastery technologies have their gold cost replaced by food.");
    xsArraySetString(list, 1, "Yeomen: Foot archers +1 range, Towers +2 attack.");
    xsArraySetString(list, 2, "Flemish Revolution: Upgrades all Villagers to Flemish Militia and allows their training at Town Centers.");
    xsArraySetString(list, 3, "Greek Fire: Fire Ships +1 range.");
    xsArraySetString(list, 4, "Stronghold: Castles and Towers +33% attack speed and heal nearby allied infantry.");
    xsArraySetString(list, 5, "Great Wall: Walls and towers +30% hit points.");
    xsArraySetString(list, 6, "Svan Towers: Defensive buildings +2 attack; Towers fire arrows that pierce multiple units.");
    xsArraySetString(list, 7, "Yasama: Towers fire 2 additional arrows.");
    xsArraySetString(list, 8, "Fortified Bastions: Castles, Town Centers, walls, gates, and towers regenerate HP.");
    xsArraySetString(list, 9, "Eupseong: Watch Tower-line +2 range.");
    xsArraySetString(list, 10, "Hill Forts: Town Centers +10 garrison space and fire arrows without garrison.");
    xsArraySetString(list, 11, "Tigui: Town Centers fire arrows without garrison.");
    xsArraySetString(list, 12, "Citadels: Castles +4 pierce attack, +3 attack vs rams, +3 attack vs infantry, receive -25% bonus damage.");
    xsArraySetString(list, 13, "Bimaristan: Monks automatically heal multiple nearby units.");
    xsArraySetString(list, 14, "First Crusade: Spawns Sergeants from Town Centers and allows allies to train them.");
    xsArraySetString(list, 15, "Detinets: Replaces 40% of Castles' and towers' stone cost with wood.");
    xsArraySetString(list, 16, "Inquisition: Monks +1 conversion range and improved conversion speed.");
    xsArraySetString(list, 17, "Crenellations: Castles +3 range; Garrisoned infantry fire arrows.");
    xsArraySetString(list, 18, "Artillery: Bombard Tower, Bombard Cannon, and Cannon Galleon +2 range.");
    return (list);
}

int set_defend_eco_techs() {
    int list = xsArrayCreateInt(13, 0, "defend_eco_techs");
    xsArraySetInt(list, 0, 834);  // Mahayana
    xsArraySetInt(list, 1, 754);  // Burgundian Vineyards
    xsArraySetInt(list, 2, 924);  // Aznauri Cavalry
    xsArraySetInt(list, 3, 835);  // Kshatriyas
    xsArraySetInt(list, 4, 506);  // Grand Trunk Road
    xsArraySetInt(list, 5, 499);  // Silk Road
    xsArraySetInt(list, 6, 625);  // Forced Levy
    xsArraySetInt(list, 7, 514);  // Nomads
    xsArraySetInt(list, 8, 488);  // Kamandaran
    xsArraySetInt(list, 9, 782);  // Szlachta Privileges
    xsArraySetInt(list, 10, 440); // Supremacy
    xsArraySetInt(list, 11, 629); // Paper Money
    xsArraySetInt(list, 12, 1061);// Tuntian
    return (list);
}

int set_defend_eco_techs_descriptions() {
    int list = xsArrayCreateString(13, "", "defend_eco_techs_desc");
    xsArraySetString(list, 0, "Mahayana: Villagers and Monks take -10% Population space.");
    xsArraySetString(list, 1, "Burgundian Vineyards: Villagers generate gold from Farms.");
    xsArraySetString(list, 2, "Aznauri Cavalry: Cavalry units take 15% less population space.");
    xsArraySetString(list, 3, "Kshatriyas: Military units cost -25% food.");
    xsArraySetString(list, 4, "Grand Trunk Road: +10% gold gather speed and reduced trading fee.");
    xsArraySetString(list, 5, "Silk Road: Trade units cost -50%.");
    xsArraySetString(list, 6, "Forced Levy: Militia-line costs no gold.");
    xsArraySetString(list, 7, "Nomads: Houses do not cost population space.");
    xsArraySetString(list, 8, "Kamandaran: Archer-line costs no gold.");
    xsArraySetString(list, 9, "Szlachta Privileges: Knight-line costs -60% gold.");
    xsArraySetString(list, 10, "Supremacy: Villagers become much stronger fighters.");
    xsArraySetString(list, 11, "Paper Money: Villagers generate gold from gathering wood.");
    xsArraySetString(list, 12, "Tuntian: Soldiers passively produce food.");
    return (list);
}

int set_defend_unit_techs() {
    int list = xsArrayCreateInt(55, 0, "defend_unit_techs");
    xsArraySetInt(list, 0, 912);  // Fereters
    xsArraySetInt(list, 1, 460);  // Atlatl
    xsArraySetInt(list, 2, 24);   // Garland Wars
    xsArraySetInt(list, 3, 885);  // Paiks
    xsArraySetInt(list, 4, 574);  // Maghrebi Camels
    xsArraySetInt(list, 5, 757);  // Wagenburg Tactics
    xsArraySetInt(list, 6, 4);    // Warwolf
    xsArraySetInt(list, 7, 685);  // Stirrups
    xsArraySetInt(list, 8, 686);  // Bagains
    xsArraySetInt(list, 9, 627);  // Manipur Cavalry
    xsArraySetInt(list, 10, 628); // Howdah
    xsArraySetInt(list, 11, 5);   // Furor Celtica
    xsArraySetInt(list, 12, 441); // Rocketry
    xsArraySetInt(list, 13, 688); // Steppe Husbandry
    xsArraySetInt(list, 14, 690); // Cuman Mercenaries
    xsArraySetInt(list, 15, 886); // Medical Corps
    xsArraySetInt(list, 16, 832); // Wootz Steel
    xsArraySetInt(list, 17, 483); // Torsion Engines
    xsArraySetInt(list, 18, 438); // Chivalry
    xsArraySetInt(list, 19, 6);   // Anarchy
    xsArraySetInt(list, 20, 461); // Perfusion
    xsArraySetInt(list, 21, 1062);// Frontier Guards
    xsArraySetInt(list, 22, 507); // Shatagni
    xsArraySetInt(list, 23, 575); // Marauders
    xsArraySetInt(list, 24, 516); // Andean Sling
    xsArraySetInt(list, 25, 691); // Fabric Shields
    xsArraySetInt(list, 26, 494); // Pavise
    xsArraySetInt(list, 27, 489); // Kataparuto
    xsArraySetInt(list, 28, 1006);// Lamellar Armor
    xsArraySetInt(list, 29, 1007);// Ordo Cavalry
    xsArraySetInt(list, 30, 493); // Tusk Swords
    xsArraySetInt(list, 31, 692); // Tower Shields
    xsArraySetInt(list, 32, 515); // Recurve Bow
    xsArraySetInt(list, 33, 577); // Farimba
    xsArraySetInt(list, 34, 485); // Hul'che Javelineers
    xsArraySetInt(list, 35, 487); // El Dorado
    xsArraySetInt(list, 36, 512); // Drill
    xsArraySetInt(list, 37, 783); // Lechitic Legacy
    xsArraySetInt(list, 38, 573); // Arquebus
    xsArraySetInt(list, 39, 883); // Ballistas
    xsArraySetInt(list, 40, 884); // Comitatenses
    xsArraySetInt(list, 41, 28);  // Bimaristan
    xsArraySetInt(list, 42, 572); // Counterweights
    xsArraySetInt(list, 43, 1070);// Coiled Serpent Array
    xsArraySetInt(list, 44, 1069);// Bolt Magazine
    xsArraySetInt(list, 45, 758); // First Crusade
    xsArraySetInt(list, 46, 513); // Druzhina
    xsArraySetInt(list, 47, 687); // Silk Armor
    xsArraySetInt(list, 48, 500); // Timurid Siegecraft
    xsArraySetInt(list, 49, 492); // Ironclad
    xsArraySetInt(list, 50, 491); // Sipahi
    xsArraySetInt(list, 51, 490); // Chatras
    xsArraySetInt(list, 52, 463); // Chieftains
    xsArraySetInt(list, 53, 49);  // Bogsveigar
    xsArraySetInt(list, 54, 1062);// Ming Guang Armor
    return (list);
}

int set_defend_unit_techs_descriptions() {
    int list = xsArrayCreateString(55, "", "defend_unit_techs_desc");
    xsArraySetString(list, 0, "Fereters: Infantry +30 HP.");
    xsArraySetString(list, 1, "Atlatl: Skirmishers +1 attack and range.");
    xsArraySetString(list, 2, "Garland Wars: Infantry +4 attack.");
    xsArraySetString(list, 3, "Paiks: Battle Elephants and Rathas attack 20% faster.");
    xsArraySetString(list, 4, "Maghrebi Camels: Camel units and Camel Archers regenerate HP.");
    xsArraySetString(list, 5, "Wagenburg Tactics: Gunpowder units move 15% faster.");
    xsArraySetString(list, 6, "Warwolf: Trebuchets do blast damage and are 100% accurate against stationary targets.");
    xsArraySetString(list, 7, "Stirrups: Cavalry +33% attack speed.");
    xsArraySetString(list, 8, "Bagains: Two-Handed Swordsman +5 melee armor.");
    xsArraySetString(list, 9, "Manipur Cavalry: Cavalry +4 attack against archers.");
    xsArraySetString(list, 10, "Howdah: Battle Elephants +1/+2 armor.");
    xsArraySetString(list, 11, "Furor Celtica: Siege Workshop units +40% HP.");
    xsArraySetString(list, 12, "Rocketry: Chu Ko Nu +2 attack, Scorpions +4 attack.");
    xsArraySetString(list, 13, "Steppe Husbandry: Scout-line and Steppe Lancers train 100% faster.");
    xsArraySetString(list, 14, "Cuman Mercenaries: Team can create 10 free Elite Kipchaks at the Castle.");
    xsArraySetString(list, 15, "Medical Corps: Elephants regenerate HP.");
    xsArraySetString(list, 16, "Wootz Steel: Infantry and cavalry attacks ignore melee armor.");
    xsArraySetString(list, 17, "Torsion Engines: Siege Workshop units' blast radius increased.");
    xsArraySetString(list, 18, "Chivalry: Stables work 40% faster.");
    xsArraySetString(list, 19, "Anarchy: Huskarls can be created at the Barracks.");
    xsArraySetString(list, 20, "Perfusion: Barracks units are created 100% faster.");
    xsArraySetString(list, 21, "Ming Guang Armor: Cavalry +2 attack vs. Siege Weapons.");
    xsArraySetString(list, 22, "Shatagni: Hand Cannoneers +2 range.");
    xsArraySetString(list, 23, "Marauders: Create Keshiks at the Stable.");
    xsArraySetString(list, 24, "Andean Sling: Skirmishers and Slingers have no minimum range.");
    xsArraySetString(list, 25, "Fabric Shields: Kamayuks, Slingers, and Eagle Warriors +1/+2 armor.");
    xsArraySetString(list, 26, "Pavise: Archer-line and Condottieri +1/+1 armor.");
    xsArraySetString(list, 27, "Kataparuto: Trebuchets fire 33% faster.");
    xsArraySetString(list, 28, "Lamellar Armor: Infantry and Skirmishers reflect 25% melee damage back to the attacker.");
    xsArraySetString(list, 29, "Ordo Cavalry: Cavalry regenerates HP in combat.");
    xsArraySetString(list, 30, "Tusk Swords: Battle Elephants +3 attack.");
    xsArraySetString(list, 31, "Tower Shields: Spearman-line and Skirmishers +2 pierce armor.");
    xsArraySetString(list, 32, "Recurve Bow: Cavalry Archers +1 range, +1 attack.");
    xsArraySetString(list, 33, "Farimba: Cavalry +5 attack.");
    xsArraySetString(list, 34, "Hul'che Javelineers: Skirmishers fire a second projectile.");
    xsArraySetString(list, 35, "El Dorado: Eagle Warriors +40 HP.");
    xsArraySetString(list, 36, "Drill: Siege units move 50% faster.");
    xsArraySetString(list, 37, "Lechitic Legacy: Light Cavalry deals trample damage.");
    xsArraySetString(list, 38, "Arquebus: Gunpowder units benefit from Ballistics and are more accurate.");
    xsArraySetString(list, 39, "Ballistas: Scorpions and Galley-line +2 attack.");
    xsArraySetString(list, 40, "Comitatenses: Militia-line, Knight-line, and Centurions train 50% faster and receive +5 charge attack.");
    xsArraySetString(list, 41, "Bimaristan: Monks automatically heal multiple nearby units.");
    xsArraySetString(list, 42, "Counterweights: Trebuchets and Mangonel-line +15% attack.");
    xsArraySetString(list, 43, "Coiled Serpent Array: Spearman-line and White Feather Guards gain additional HP when near each other.");
    xsArraySetString(list, 44, "Bolt Magazine: Archer-line, War Chariots and Lou Chuans fire additional projectiles.");
    xsArraySetString(list, 45, "First Crusade: Spawns Sergeants from Town Centers and allows allies to train them.");
    xsArraySetString(list, 46, "Druzhina: Infantry units deal trample damage.");
    xsArraySetString(list, 47, "Silk Armor: Scout-line, Steppe Lancer, and Cavalry Archers +1/+1 armor.");
    xsArraySetString(list, 48, "Timurid Siegecraft: Trebuchets +2 range; enables Flaming Camels.");
    xsArraySetString(list, 49, "Ironclad: Siege units +4 melee armor.");
    xsArraySetString(list, 50, "Sipahi: Cavalry Archers +20 HP.");
    xsArraySetString(list, 51, "Chatras: Battle Elephants +30 HP.");
    xsArraySetString(list, 52, "Chieftains: Infantry get attack bonus vs cavalry and generate gold.");
    xsArraySetString(list, 53, "Bogsveigar: Archer-line and Longboats +1 attack.");
    xsArraySetString(list, 54, "Ming Guang Armor: Cavalry +2 attack vs. Siege Weapons.");
    return (list);
}

void main() {
    test = xsArrayCreateInt(5, 0, "test");
    defend_unique_techs = set_defend_unique_techs();
    defend_unique_techs_desc = set_defend_unique_techs_descriptions();
    defend_unique_techs_status = xsArrayCreateInt(xsArrayGetSize(defend_unique_techs), 0, "defend_unique_tech_status");

    defend_defense_techs = set_defend_defense_techs();
    defend_defense_techs_desc = set_defend_defense_techs_descriptions();
    defend_defense_techs_status = xsArrayCreateInt(xsArrayGetSize(defend_defense_techs), 0, "defend_defense_techs_status");

    defend_eco_techs = set_defend_eco_techs();
    defend_eco_techs_desc = set_defend_eco_techs_descriptions();
    defend_eco_techs_status = xsArrayCreateInt(xsArrayGetSize(defend_eco_techs), 0, "defend_eco_techs_status");

    defend_unit_techs = set_defend_unit_techs();
    defend_unit_techs_desc = set_defend_unit_techs_descriptions();
    defend_unit_techs_status = xsArrayCreateInt(xsArrayGetSize(defend_unit_techs), 0, "defend_unit_techs_status");
}