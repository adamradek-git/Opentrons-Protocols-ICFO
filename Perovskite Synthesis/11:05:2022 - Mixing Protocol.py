from opentrons import protocol_api

# metadata
metadata = {
    'protocolName': '10/05/2022 Test Protocol 2',
    'author': 'Martinez',
    'description': 'Mixing at a location A1',
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

    def mixing(loc, vol, num = 3): # number of times you want to mix, 3 should be good
        count = 1
        while count != 4:
            right_pipette.aspirate(vol, plate[loc])
            right_pipette.dispense(vol, plate[loc])
            count += 1
    
    mixing('A1', 100)

    right_pipette.drop_tip()