from opentrons import protocol_api

# metadata
metadata = {
    'protocolName': 'Multichannel Pipette Testing and Calibration',
    'author': 'Martinez',
    'description': 'We make the multichannel pipette dispense 150ul into an entire 96 well microtiter plate',
    'apiLevel': '2.12'
}

# protocol run function
def run(protocol: protocol_api.ProtocolContext):

	# the reservoir
	res = protocol.load_labware('nest_96_wellplate_200ul_flat', location = '5') 

	# tip rack for multichannel pipette
	tiprack_20 = protocol.load_labware('opentrons_96_tiprack_20ul', location = '9')

	# loading the multichannel pipette 
	right = protocol.load_instrument('p20_multi_gen2', 'right',  tip_racks=[tiprack_20])

	# the plate of interest
	plate = protocol.load_labware('nest_96_wellplate_200ul_flat', location='7')

	right.pick_up_tip(tiprack_20['A1'])

	for i in range(1, 12):
		right.aspirate(20, res['A1'])
		right.dispense(20, plate['A' + str(i)])
		right.touch_tip() 

	right.drop_tip()


	