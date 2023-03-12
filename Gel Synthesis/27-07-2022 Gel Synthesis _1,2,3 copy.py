from opentrons import protocol_api
#from opentrons import instruments

# metadata
metadata = {
    'protocolName': 'Aparna Gel Synthesis Protocol',
    'author': 'Martinez',
    'description': 'Dripping two precurser solutions consistantly to form a Ru Gel',
    'apiLevel': '2.12'
}


def run(protocol: protocol_api.ProtocolContext):# labware for pipette tips

    ########## MODULE DEFINITION ############

    tiprack_300 = protocol.load_labware('opentrons_96_tiprack_300ul', location = '11')

    # temperature module containing the two pre-cursor solutions
    temperature_module = protocol.load_module('temperature module', location = '8')
    #temperature_module.set_temperature(4)
    source_plate = temperature_module.load_labware('corning_384_wellplate_112ul_flat')     # stock solution in 2ml tubes

    # location of the stirring items here 
    destination_plate = protocol.load_labware('corning_384_wellplate_112ul_flat', location = '6')

    # loading the 300ul pipette item
    right = protocol.load_instrument('p300_single_gen2', mount='right', tip_racks=[tiprack_300])

    ########## PROTOCOL ############
    
    # precurser solution 0 --> A1
    # precurser solution 1 --> A2
    # precurser solution 2 --> A3
    # precurser solution 3 --> A4

    # add precurser 0 to all wells with appropriate values | 1 PIPETTE TIP
    # [2180, 545, 1090, 3270, 4360, 8720]

    water_volumes = 2180 / 8

    def solvant_1(): 
        right.move_to(source_plate['D22'].bottom(z=65))
        right.aspirate(50, source_plate['D22'].bottom(5))
        right.move_to(source_plate['D22'].bottom(z=65))
        right.dispense(50, destination_plate['F11'].bottom(70))
        right.move_to(destination_plate['F11'].bottom(z=120))
        right.drop_tip()

    def solvant_2():
        right.pick_up_tip()
        right.move_to(source_plate['D6'].bottom(z=65))
        right.aspirate(109, source_plate['D6'].bottom(5))
        right.move_to(source_plate['D6'].bottom(z=65))
        right.dispense(109, destination_plate['F11'].bottom(70))
        right.move_to(destination_plate['F11'].bottom(z=120))

    
    for i in range(1, 8 + 1):
        solvant_2() # water, left hand side
        solvant_1() # other thing, right hand side
    














