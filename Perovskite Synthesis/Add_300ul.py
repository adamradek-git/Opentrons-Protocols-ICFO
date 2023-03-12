from opentrons import protocol_api

# metadata
metadata = {
    'protocolName': 'Add 300ul to each well in 96 microtiter',
    'author': 'Martinez',
    'description': "Done after higgins experiment",
    'apiLevel': '2.12'
}

columns = range(1,12 + 1)
rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

def run(protocol: protocol_api.ProtocolContext):
    # labware for pipette tips
    tiprack_300 = protocol.load_labware('opentrons_96_tiprack_300ul', location = '5')
    
    # Chloroform reservoir(just a tube here ... not sure how to replicate) 
    well = protocol.load_labware('agilent_1_reservoir_290ml', location='4')

    # unlimited 96 well microtiter plate 
    plate = protocol.load_labware('nest_96_wellplate_200ul_flat', location = '6')
    
    # pipette configuration --> using both right and left tips
    right_pipette = protocol.load_instrument('p300_single_gen2', mount='right', tip_racks=[tiprack_300])

    right_pipette.pick_up_tip()

    for row in rows:
    	for col in columns: 
    		right_pipette.aspirate(250, well['A1'])
    		right_pipette.dispense(250, plate[row + str(col)])

    right_pipette.drop_tip()


