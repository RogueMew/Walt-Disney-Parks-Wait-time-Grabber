import requests
import os
import json
from function import *

os.system("cls")
parkWanted = input("What park is the one you will like to get details?\n\n\nWalt Disney World Resort Parks:\n   - Magic Kingdom\n   - EPCOT\n   - Hollywood Studios\n   - Animal Kingddom\n\nDisneyland Resort Parks:\n   - Disneyland\n   - California Adventure\n\nTokyo Disney Resort:\n   - Tokyo Disneyland\n   - Tokyo DisneySea\n\nShanghai Disney Resort:\n   - Shanghai Disneyland\n\nHong Kong Disneyland Parks:\n   - Hong Kong Disneyland\n\nDisneyland Paris:\n   - Disneyland Park\n   - Walt DIsney Studios Park\n\n")

RawRideID = RideID(parkWanted)
print("------------------------------------------------")
timecheck(parkWanted)
print("------------------------------------------------")
RideTypeWanted = input("\n\nWhat type of attraction would you like to look for?\nOptions:\n   - Rides\n   - Restaurant\n\n******************WIP******************\n\n   - Shows\n******************WIP******************\n\n")
RideDisplay(RawRideID,RideTypeWanted)