void roll_dice() {
    for (var = 0; < 10)
        int sides = 1000;
        xsChatData("Set Dice "+var);
        if(xsTriggerVariable(var) < 0)
            sides = xsTriggerVariable(var) * -1;
            xsChatData("Dice "+var+" current value = "+sides);
        int num = xsGetRandomNumberMax(sides) + 1;
        xsChatData("Set Dice "+var+" to "+num);
        xsSetTriggerVariable(var, num);
}

