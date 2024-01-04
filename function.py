import requests, json
import datetime
import pytz

ParkTimeZones = {
    "epcot": "America/New_York",
    "magic kingdom": "America/New_York",
    "hollywood studios": "America/New_York",
    "animal kingdom": "America/New_York",
    "disneyland": "America/Los_Angeles",
    "california adventure": "America/Los_Angeles",
    "tokyo disneySea": "Asia/Tokyo",
    "tokyo disneyland": "Asia/Tokyo",
    "shanghai disneyland": "Asia/Shanghai",
    "walt disney studios park": "Europe/Paris",
    "disneyland park": "Europe/Paris",
    "hong kong disneyland park": "Asia/Hong_Kong",
}

Park_IDs = {
    "epcot": "47f90d2c-e191-4239-a466-5892ef59a88b",
    "magic kingdom": "75ea578a-adc8-4116-a54d-dccb60765ef9",
    "hollywood studios": "288747d1-8b4f-4a64-867e-ea7c9b27bad8",
    "animal kingdom": "1c84a229-8862-4648-9c71-378ddd2c7693",
    "disneyland": "7340550b-c14d-4def-80bb-acdb51d49a66",
    "california adventure": "832fcd51-ea19-4e77-85c7-75d5843b127c",
    "tokyo disneySea": "67b290d5-3478-4f23-b601-2f8fb71ba803",
    "tokyo disneyland": "3cc919f1-d16d-43e0-8c3f-1dd269bd1a42",
    "shanghai disneyland": "ddc4357c-c148-4b36-9888-07894fe75e83",
    "walt disney studios park": "ca888437-ebb4-4d50-aed2-d227f7096968",
    "disneyland park": "dae968d5-630d-4719-8b06-3d107e944401",
    "hong kong disneyland park": "bd0eb47b-2f02-4d4d-90fa-cb3a68988e3b",
}

def timecheck(parkWanted):
    parks = ParkTimeZones.keys()
    parkWantedTimeZone = None
    SpecialEvent = False
    completed = None

    for parkTime in parks:
        if parkWanted.lower() == parkTime:
            URL = "https://api.themeparks.wiki/v1/entity/{}/schedule".format(
                Park_IDs[parkTime]
            )
            Park_JSONRAW = requests.get(URL)
            Park_JSON = Park_JSONRAW.json()
            parkWanted = parkTime
            parkWantedTimeZone = ParkTimeZones[parkTime]
            parkCurrentDate = datetime.datetime.now(
                pytz.timezone(parkWantedTimeZone)
            ).strftime("%Y-%m-%d")
            parkCurrentTime = datetime.datetime.now(
                pytz.timezone(parkWantedTimeZone)
            ).strftime("%Y-%m-%dT%X")
            parkOffset = (
                str(
                    datetime.datetime.now(pytz.timezone(parkWantedTimeZone)).strftime("%z")
                ).split("00")[0]
                + ":00"
            )
            print("\nCurrent date at {}: {}\n".format(parkTime, parkCurrentDate))
            print(
                "\nCurrent time at {}: {}\n".format(
                    parkTime, parkCurrentTime.split("T")[-1]
                )
            )
            if "schedule" in Park_JSON:
                for schedule in Park_JSON["schedule"]:
                    if (
                        schedule["date"] == str(parkCurrentDate)
                        and schedule["type"] != "TICKETED_EVENT"
                        and completed != "Done"
                    ):
                        BaseOperationsOpen = (
                            str(schedule["openingTime"])
                            .split("T")[-1]
                            .split("-")[0]
                            .split("+")[0]
                        )
                        BaseOperationsClose = (
                            str(schedule["closingTime"])
                            .split("T")[-1]
                            .split("-")[0]
                            .split("+")[0]
                        )
                        completed = "Done"

                    if (
                        schedule["date"] == str(parkCurrentDate)
                        and schedule["type"] == "TICKETED_EVENT"
                    ):
                        SpecialOperationsDesc = schedule["description"]
                        SpecialOperationsOpen = (
                            str(schedule["openingTime"])
                            .split("T")[-1]
                            .split("-")[0]
                            .split("+")[0]
                        )
                        SpecialOperationsExit = (
                            str(schedule["closingTime"])
                            .split("T")[-1]
                            .split("-")[0]
                            .split("+")[0]
                        )
                        SpecialEvent = True
            print(
                "\nBasic Operation Open Time: {}\nBasic Operation Exit Time: {}".format(
                    BaseOperationsOpen, BaseOperationsClose
                )
            )
            if SpecialEvent:
                print(
                    "\n\nSpecial Events\n\n{} Open Time: {} \n{} Closing Time: {}".format(
                        SpecialOperationsDesc,
                        SpecialOperationsOpen,
                        SpecialOperationsDesc,
                        SpecialOperationsExit,
                    )
                )
            print("\n\n")
            break

def RideID(parkWanted):
    if parkWanted.lower() == "epcot":
        Park_ID = Park_IDs["epcot"]
    elif parkWanted.lower() == "magic kingdom":
        Park_ID = Park_IDs["magic kingdom"]
    elif parkWanted.lower() == "hollywood studios":
        Park_ID = Park_IDs["hollywood studios"]
    elif parkWanted.lower() == "animal kingdom":
        Park_ID = Park_IDs["animal kingdom"]
    elif parkWanted.lower() == "disneyland":
        Park_ID = Park_IDs["disneyland"]
    elif parkWanted.lower() == "california adventure":
        Park_ID = Park_IDs["california adventure"]
    elif parkWanted.lower() == "tokyo disneySea":
        Park_ID = Park_IDs["tokyo disneySea"]
    elif parkWanted.lower() == "tokyo disneyland":
        Park_ID = Park_IDs["tokyo disneyland"]
    elif parkWanted.lower() == "shanghai disneyland":
        Park_ID = Park_IDs["shanghai disneyland"]
    elif parkWanted.lower() == "walt disney studios park":
        Park_ID = Park_IDs["walt disney studios park"]
    elif parkWanted.lower() == "disneyland park":
        Park_ID = Park_IDs["disneyland park"]
    elif parkWanted.lower() == "hong kong disneyland park":
        Park_ID = Park_IDs["hong kong disneyland park"]
    elif parkWanted.lower() == "exit":
        print("Thank you for using. Have a magical day!!!")
        exit()
    else:
        Park_ID = "None"
    
    if Park_ID != "None":
        Park_URL = "https://api.themeparks.wiki/v1/entity/{}/children".format(Park_ID)
        Park_JSONRAW = requests.get(Park_URL)
        Park_JSON = Park_JSONRAW.json()
        return Park_JSON
    else:
        print("That is not an option. Stopping program")
        exit()

def RideDisplay(RideIDJason, RideTypeWanted):
    firstItem = RideIDJason["children"]
    
    
    for rides in firstItem:
        Ride_ID = rides["id"]
        Ride_Name = rides["name"]
        Ride_Type = rides["entityType"]

        WaitTime_URL = "https://api.themeparks.wiki/v1/entity/{}/live".format(Ride_ID)
        RideWaitJSONRAW = requests.get(WaitTime_URL)
        RideWaitJSON = RideWaitJSONRAW.json()
        
        if RideTypeWanted.lower() == "ride" or RideTypeWanted.lower() == "rides":
            if Ride_Type == "ATTRACTION" and len(RideWaitJSON["liveData"]) > 0:
                RideWaitJSON = RideWaitJSON["liveData"][0]
                Ride_Status = RideWaitJSON["status"]
                output = "\nName: {}\nType: {}\nStatus: {}\n".format(Ride_Name, Ride_Type, Ride_Status)
                print("===========================================================")
                print(output)
                if Ride_Status == "OPERATING":
                    if "queue" in RideWaitJSON:
                        if "STANDBY" in RideWaitJSON["queue"]:
                            Ride_Standby = RideWaitJSON["queue"]["STANDBY"]["waitTime"]
                            if Ride_Standby is None:
                                Ride_Standby_Output = "Standby Wait Time: {}\n".format(Ride_Standby)
                                print(Ride_Standby_Output)
                            else:    
                                Ride_Standby_Output = "Standby Wait Time: {} minutes\n".format(Ride_Standby)
                                print(Ride_Standby_Output)
                    
                        if "SINGLE_RIDER" in RideWaitJSON["queue"]:
                            Ride_Single = RideWaitJSON["queue"]["SINGLE_RIDER"]["waitTime"]
                            if Ride_Single is None:
                                Ride_Single_Output = "Single Rider Wait Time: {}\n".format(Ride_Single)
                                print(Ride_Single_Output)
                            else:
                                Ride_Single_Output = "Single Rider Wait Time: {} minutes\n".format(Ride_Single)
                                print(Ride_Single_Output)

                        if "PAID_RETURN_TIME" in RideWaitJSON["queue"]:
                            Ride_Lightning_State = RideWaitJSON["queue"]["PAID_RETURN_TIME"]["state"]
                            print("\nLightning Lane State: {}")
                            if Ride_Lightning_State == "AVAILABLE":
                                Ride_Lightning_Start = RideWaitJSON["queue"]["PAID_RETURN_TIME"]["returnStart"]
                                Ride_Lightning_End = RideWaitJSON["queue"]["PAID_RETURN_TIME"]["returnEnd"]
                                Ride_Lightning_Price = str(RideWaitJSON["queue"]["PAID_RETURN_TIME"]["price"]["amount"]).split("00")[0]
                                Ride_Lightning_Output = "\nLightning Lane Price: ${}\nLightning Lane Time Group Start: {}\nLightning Lane Time Group End: {}\n".format(Ride_Lightning_Price, Ride_Lightning_Start, Ride_Lightning_End)
                                print(Ride_Lightning_Output)

                        if "RETURN_TIME" in RideWaitJSON["queue"]:
                            Ride_ReturnTime_State = RideWaitJSON["queue"]["RETURN_TIME"]["state"]
                            Ride_ReturnTime_State_Output = "Return Time Status: {}".format(Ride_ReturnTime_State)
                            print(Ride_ReturnTime_State_Output)

                            if Ride_ReturnTime_State != "FINISHED":
                                Ride_ReturnTime_Start = str(RideWaitJSON["queue"]["RETURN_TIME"]["returnStart"]).split("T")[-1]
                                Ride_ReturnTime_End = str(RideWaitJSON["queue"]["RETURN_TIME"]["returnEnd"]).split("T")[-1]
                                Ride_ReturnTime_Time_Output = "Return Time Start: {}\nReturn Time End: {}\n".format(Ride_ReturnTime_Start, Ride_ReturnTime_End)
                                print(Ride_ReturnTime_Time_Output)
                        
                        if "BOARDING_GROUP" in RideWaitJSON["queue"]:
                            BOARDING_GROUP_Allocation = RideWaitJSON["queue"]["BOARDING_GROUP"]["allocationStatus"]
                            if BOARDING_GROUP_Allocation == "AVAILABLE":
                                BOARDING_GROUP_Current_Start = str(RideWaitJSON["queue"]["BOARDING_GROUP"]["currentGroupStart"]).split("T")[-1]
                                BOARDING_GROUP_Current_End = str(RideWaitJSON["queue"]["BOARDING_GROUP"]["currentGroupEnd"]).split("T")[-1]
                                BOARDING_GROUP_Wait = RideWaitJSON["queue"]["BOARDING_GROUP"]["estimatedWait"]
                                if BOARDING_GROUP_Wait is None:
                                    BOARDING_GROUP_Output = "Boarding Groups Allocation Status: {}\nCurrent Group Start Time: {}\nCurrent Group End Time: {}\nCurrent Wait Time: {}\n".format(BOARDING_GROUP_Allocation,BOARDING_GROUP_Current_Start,BOARDING_GROUP_Current_End,BOARDING_GROUP_Wait)
                                    print(BOARDING_GROUP_Output)
                                else:
                                    BOARDING_GROUP_Output = "Boarding Groups Allocation Status: {}\nCurrent Group Start Time: {}\nCurrent Group End Time: {}\nCurrent Wait Time: {} minutes\n".format(BOARDING_GROUP_Allocation,BOARDING_GROUP_Current_Start,BOARDING_GROUP_Current_End,BOARDING_GROUP_Wait)
                                    print(BOARDING_GROUP_Output)
        
        if RideTypeWanted.lower() == "restaurant" or RideTypeWanted.lower() == "restaurants":
            if Ride_Type == "RESTAURANT":
                output = "\nName: {}\nType: {}\n".format(Ride_Name, Ride_Type)
                print("===========================================================")
                print(output)
            
            if Ride_Type == "RESTAURANT" and len(RideWaitJSON["liveData"]) > 0:
                RideWaitJSON = RideWaitJSON["liveData"][0]
                Ride_Status = RideWaitJSON["status"]
                if Ride_Status == "OPERATING":
                    if "queue" in RideWaitJSON:
                        if "STANDBY" in RideWaitJSON["queue"]:
                            Ride_Standby = RideWaitJSON["queue"]["STANDBY"]["waitTime"]
                            if Ride_Standby is None:
                                Ride_Standby_Output = "Standby Wait Time: {}\n".format(Ride_Standby)
                            else:
                                Ride_Standby_Output = "Standby Wait Time: {} minutes\n".format(Ride_Standby)
                            print(Ride_Standby_Output)
                        if "diningAvailability" in RideWaitJSON:
                            for Partysize in RideWaitJSON["diningAvailability"]:
                                sizeOfParty = Partysize["partySize"]
                                PartyWait = Partysize["waitTime"]
                                PartyOutput = "-------------------\nParty Size: {}\nWait for Party size: {} minutes\n"
                        if "operatingHours" in RideWaitJSON:
                            OperatingTimeOpened = RideWaitJSON["operatingHours"][0]["startTime"]
                            OperatingTimeClosed = RideWaitJSON["operatingHours"][0]["endTime"]
                            OperatingOutput = "\nOpened: {}\nClosed: {}\n".format(OperatingTimeOpened,OperatingTimeClosed)
                            print(OperatingOutput)                