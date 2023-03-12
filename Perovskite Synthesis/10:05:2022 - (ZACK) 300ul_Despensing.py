from opentrons import protocol_api

# metadata
metadata = {
    'protocolName': 'Third Protocol',
    'author': 'Toscanini',
    'description': 'Pick up a tip and drop it',
    'apiLevel': '2.12'
}

# protocol run function
def run(protocol: protocol_api.ProtocolContext):

    # labware
    tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', location='8')
    plate = protocol.load_labware('opentrons_24_aluminumblock_nest_1.5ml_snapcap', location='2')

    # pipettes
    right_pipette = protocol.load_instrument(
         'p300_single_gen2', mount='right', tip_racks=[tiprack])
         

    # commands
    x = range(1,5)
    right_pipette.pick_up_tip()
    
    for i in x:
        right_pipette.aspirate(100,plate['A1'])
        right_pipette.dispense(100,plate['B' + str(i)])
    
    right_pipette.drop_tip()