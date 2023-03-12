from opentrons import protocol_api

# metadata
metadata = {
    'protocolName': '10/05/2022 Test Protocol 2',
    'author': 'Martinez',
    'description': 'Despensing from A1 Down a Column',
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
    right_pipette.pick_up_tip()
    
    # take liquid from A1 then move it accross the row starting from 1 to 4 (1,5) --> [1,5)
    letter = 'B'
    for i in range(1,5): # should cycle through B C D E
        right_pipette.aspirate(100, plate['A1'])
        right_pipette.dispense(100, plate[letter + '1'])
        letter = chr(ord(letter) + 1)

    right_pipette.drop_tip()