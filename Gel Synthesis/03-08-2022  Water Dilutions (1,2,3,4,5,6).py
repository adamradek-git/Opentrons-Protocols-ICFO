from opentrons import protocol_api
#from opentrons import instruments

# metadata
metadata = {
    'protocolName': 'Aparna Gel Synthesis Protocol',
    'author': 'Martinez',
    'description': 'Dripping two precurser solutions consistantly to form a Ru Gel. Here the water + ethonal is first fully added. Then, the second agent is added. ',
    'apiLevel': '2.12'
}


def run(protocol: protocol_api.ProtocolContext):# labware for pipette tips

    ########## MODULE DEFINITION ############

    tiprack_1000 = protocol.load_labware('opentrons_96_tiprack_1000ul', location = '11')

    # temperature module containing the two pre-cursor solutions
    temperature_module = protocol.load_module('temperature module', location = '8')
    #temperature_module.set_temperature(4)
    source_plate = temperature_module.load_labware('corning_384_wellplate_112ul_flat')     # stock solution in 2ml tubes
    # location of the stirring items here 
    destination_plate = protocol.load_labware('corning_384_wellplate_112ul_flat', location = '6')

    # loading the 300ul pipette item
    left = protocol.load_instrument('p1000_single_gen2', mount='left', tip_racks=[tiprack_1000])

    ########## PROTOCOL ############
    
    # precurser solution 0 --> A1
    # precurser solution 1 --> A2
    # precurser solution 2 --> A3
    # precurser solution 3 --> A4

    # add precurser 0 to all wells with appropriate values | 1 PIPETTE TIP

    amount = 8720/9

    def solvant_1(): 
        left.move_to(source_plate['D22'].bottom(z=55))
        left.aspirate(1000, source_plate['D22'].bottom(5))
        left.move_to(source_plate['D22'].bottom(z=55))
        left.dispense(1000, destination_plate['F11'].bottom(70))
        left.move_to(destination_plate['F11'].bottom(z=120))

    def solvant_2():
        left.move_to(source_plate['D6'].bottom(z=55))
        left.aspirate(amount, source_plate['D6'].bottom(5))
        left.move_to(source_plate['D6'].bottom(z=55))
        left.dispense(amount, destination_plate['F11'].bottom(70))
        left.move_to(destination_plate['F11'].bottom(z=120))

    left.pick_up_tip()
    for i in range(1, 8 + 1):
        solvant_2() # water, left hand side
    solvant_1()
    left.drop_tip()
    














