import time
import pandas as pd

# Define constant
BATT_MAX_CAPACITY = 67.5 # kWh
BATT_MIN_CAPACITY = 2.5 # kWh
BATT_POWER_RATE = 25 # kW
GENSET_MAX_POWER = 24 # kW

# Define global variable
socBatt = 67.5
gridAvailable = True
gensetIsOn = False

# check
def power_strategy_management(pPhotoVoltaic = 0, pBuilding = 0, pEV = 0, pGrid = 0):
    global socBatt
    global gridAvailable
    global gensetIsOn

    if pGrid == 0: 
        print("grid unavailable")
        gridAvailable = False

    load = pBuilding + pEV
    pvExcess = pPhotoVoltaic - load

    if(pvExcess>0):
        if(socBatt == BATT_MAX_CAPACITY):
            # use pv, send excess to grid
            print("battery is full...")
            print("using photvoltaic power " + str(pPhotoVoltaic) + " kW")
            print("sending excess to grid " + str(pvExcess)+ " kW")
        else:
            # use pv, charge battery
            battPowerNeeded = BATT_MAX_CAPACITY - socBatt
            print("charging battery....")
            print("current battery soc : " + str(socBatt))
            if(pvExcess > battPowerNeeded):
                if(battPowerNeeded > BATT_POWER_RATE):
                    socBatt = socBatt + BATT_POWER_RATE
                    print("adding "+str(BATT_POWER_RATE)+" to battery")
                    print("send excess "+str(battPowerNeeded-BATT_POWER_RATE)+" to Grid")
                else:
                    socBatt = socBatt + battPowerNeeded
                    print("adding "+str(battPowerNeeded)+" to battery") 
                    print("send excess "+str(pvExcess-battPowerNeeded)+" to Grid")
            else:
                if(pvExcess >= BATT_POWER_RATE):
                    socBatt = socBatt + BATT_POWER_RATE
                    print("adding "+str(BATT_POWER_RATE)+" to battery")
                    print("send excess "+str(battPowerNeeded-BATT_POWER_RATE)+" to Grid")
                else:
                    socBatt = socBatt + pvExcess
                    print("adding "+str(pvExcess)+" to battery")
                    print("no excess sent to Grid")

    elif(pvExcess==0):
        # use pv only
        print("using photvoltaic power " + str(pPhotoVoltaic) + " kW")

    else:
        # use pv and ...
        print("using photvoltaic power " + str(pPhotoVoltaic) + " kW")
        if(gridAvailable):
            # use grid
            print("using power from grid "+ str(load-pPhotoVoltaic) + " kW")
        else:
            powerNeeded = load - pPhotoVoltaic
            battPower = socBatt-BATT_MIN_CAPACITY
            battOutput = BATT_POWER_RATE

            if battPower < BATT_POWER_RATE:
                battOutput=battPower 
            if powerNeeded < BATT_POWER_RATE:
                battOutput=powerNeeded

            if(battPower > 0):
                # discharge battery
                print("current battery soc : " + str(socBatt))
                if(powerNeeded > battOutput+GENSET_MAX_POWER):
                    # system failure
                    print("BLACKOUT, shortage by "+str(powerNeeded-(battOutput+GENSET_MAX_POWER))+" kW")
                elif(powerNeeded <= battOutput):
                    # using battery only
                    print("discharging battery...")
                    print("releasing "+str(powerNeeded)+" kW from battery")
                    socBatt = socBatt - battOutput
                else:
                    # using battery and genset
                    print("discharging battery...")
                    print("releasing "+str(battOutput)+" kW from battery")
                    print("releasing "+str(powerNeeded - battOutput)+" kW from GenSet")
                    socBatt = socBatt - battOutput
                    gensetIsOn = True
            else:
                if(powerNeeded<=GENSET_MAX_POWER):
                    # use genset only
                    gensetIsOn = True
                    print("using Genset "+str(powerNeeded)+" kW")
                else:
                    # system failure
                    print("BLACKOUT, shortage by "+str(powerNeeded-GENSET_MAX_POWER)+" kW")
        

# read excel file
df = pd.read_excel (r'.\DATA PENELITIAN FEVC.xlsx', sheet_name='data')
df_array = df.to_numpy()
socBatt = df_array[0][7]
for row in df_array:
    print ("============================")
    print ("time : "+str(row[0]))
    power_strategy_management(pPhotoVoltaic=row[4], pBuilding=row[2], pEV=row[3], pGrid=row[6])
    print ("============================\n")
    time.sleep(1)