# Define constant
BATT_MAX_CAPACITY = 67.5 # kWh
BATT_MIN_CAPACITY = 2.5 # kWh
BATT_POWER_RATE = 25 # kW
GENSET_MAX_POWER = 24 # kW

# Define Variables
pPhotoVoltaic = 0
pGenSet = 0
pBuilding = 0
pEV = 0
pBattery = 0
gridAvailable = True
socBatt = 67.5

# read param

# check
load = pBuilding + pEV
pvExcess = pPhotoVoltaic - load

if(pvExcess>0):
    if(socBatt == BATT_MAX_CAPACITY):
        # send Power to grid
        print("no charging battery")
        print("send to grid " + str(pvExcess)+ " kW")
    else:
        # charge battery
        battPowerNeeded = BATT_MAX_CAPACITY - socBatt
        print("charging battery")
        print("current battery soc : " + str(socBatt))
        if(pvExcess > battPowerNeeded):
            if(battPowerNeeded > BATT_POWER_RATE):
                socBatt = socBatt + BATT_POWER_RATE
                print("adding "+str(BATT_POWER_RATE)+" to battery and send excess "+str(battPowerNeeded-BATT_POWER_RATE)+" to Grid")
            else:
                socBatt = socBatt + battPowerNeeded
                print("adding "+str(battPowerNeeded)+" to battery and send excess "+str(pvExcess-battPowerNeeded)+" to Grid")
        else:
            if(pvExcess >= BATT_POWER_RATE):
                socBatt = socBatt + BATT_POWER_RATE
                print("adding "+str(BATT_POWER_RATE)+" to battery and send excess "+str(battPowerNeeded-BATT_POWER_RATE)+" to Grid")
            else:
                socBatt = socBatt + pvExcess
                print("adding "+str(pvExcess)+" to battery and send excess "+str(0)+" to Grid")

elif(pvExcess==0):
    print("using photvoltaic poer " + str(pPhotoVoltaic) + " kW")

else:
    if(gridAvailable):
        print("using photvoltaic poer " + str(pPhotoVoltaic) + " kW and using Grid power also")
    else:
        if(socBatt > BATT_MIN_CAPACITY):
            # discharge battery
            print("discharging battery")
            print("current battery soc : " + str(socBatt))
            if(socBatt > BATT_POWER_RATE):
                print("releasing "+str(BATT_POWER_RATE)+" from battery")
        else:
            print()
        
            

