from opentrons import protocol_api

# metadata
metadata = {
    'protocolName': 'Add Chloroform using multichannel pipette',
    'author': 'Martinez',
    'description': 'Make sure to exchange the tip of the right plate, then proceed ',
    'apiLevel': '2.12'
}

# protocol run function
def run(protocol: protocol_api.ProtocolContext):

	# the reservoir
	res = protocol.load_labware('nest_96_wellplate_200ul_flat', location = '1') 

	# tip rack for multichannel pipette
	tiprack_300 = protocol.load_labware('opentrons_96_tiprack_300ul', location = '3')

	# loading the multichannel pipette 
	right = protocol.load_instrument('p300_multi_gen2', 'right',  tip_racks=[tiprack_300])

	# the plate of interest
	plate = protocol.load_labware('nest_96_wellplate_200ul_flat', location='5')


	for i in range(1, 12+1):
		right.pick_up_tip(tiprack_300['A' + str(i)])
		right.aspirate(250, res['A' + str(i)])
		right.touch_tip() 
		right.dispense(250, plate['A' + str(i)])
		right.touch_tip()
		right.drop_tip()


	