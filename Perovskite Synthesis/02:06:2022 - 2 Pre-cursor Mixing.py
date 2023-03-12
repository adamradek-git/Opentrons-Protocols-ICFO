from opentrons import protocol_api

###### TIMING ANALYSIS ######
'''
-> Pre setup phase: 0:20 second
-> Despensing part A (1 pipette): 8:00 min
-> Despensing Part B, C ( X Pipettes): 100 min 
--> Ending: 

Total Time:  

- how about accuracy at 2ul should I switch to another pipette? 

'''
###### END OF TIMING ANALYSIS ######

# metadata
metadata = {
    'protocolName': 'Perovskite Protocol with Food Coloring 96-well',
    'author': 'Martinez',
    'description': "Replicating the protocol from Higgins with 96-well. We are mixing 2 pre-curser starting at 50 0 .... 5 45 and 0 50",
    'apiLevel': '2.12'
}

# Here Solution A is added accross the 96 well. Then, for each well from A1 - H12, both B,C are added
# Right after B,C are added in each well, choloform is placed to deactivate
# A --> Yellow B --> Blue C --> Red, Choloform --> Water

# each pair of 3 numbers represents the value of the pre-curser solutions you want in each well
# this matrix is a 96 well matrix


columns = range(1,12 + 1)
rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

#input_matrix[0][2][1] --> will output 16 for reference. [row][column][0,1,2]

def run(protocol: protocol_api.ProtocolContext):
    # labware for pipette tips
    tiprack_300_1 = protocol.load_labware('opentrons_96_tiprack_300ul', location = '9')
    tiprack_20 = protocol.load_labware('opentrons_96_tiprack_20ul', location = '8')

    module = protocol.load_module('Temperature Module', location = '10')

    # stock solution in 2ml tubes
    well1 = protocol.load_labware('opentrons_24_aluminumblock_nest_2ml_snapcap', location='7')

    # Chloroform reservoir(just a tube here ... not sure how to replicate) 
    #well2 = protocol.load_labware('agilent_1_reservoir_290ml', location='4')

    # unlimited 96 well microtiter plate 
    plate = module.load_labware('nest_96_wellplate_200ul_flat', label='Temperature-Controlled Tubes')
    
    # pipette configuration --> using both right and left tips
    right_pipette = protocol.load_instrument('p300_single_gen2', mount='right', tip_racks=[tiprack_300_1])
    left_pipette = protocol.load_instrument('p20_single_gen2', mount='left', tip_racks=[tiprack_20])

    # precurser solution 1 --> A1
    # precurser solution 2 --> A2
    # chloforom solution --> A4 --> Will need to change to a reservoir once we get this input

    # add precurser 1 to all wells with appropriate values | 1 PIPETTE TIP

    right_pipette.pick_up_tip()
    left_pipette.pick_up_tip()
    pre_1 = 50 
    for col in [1,2]:
        for row in rows:
            if pre_1 != 0:
                if pre_1 > 20: 
                    right_pipette.aspirate(pre_1, well1['A1'])
                    right_pipette.touch_tip()  
                    right_pipette.dispense(pre_1, plate[row + str(col)])
                    right_pipette.touch_tip()   
                else: 
                    left_pipette.aspirate(pre_1, well1['A1'])
                    left_pipette.touch_tip() 
                    left_pipette.dispense(pre_1, plate[row + str(col)])
                    left_pipette.touch_tip()   
                pre_1 -= 5

    right_pipette.drop_tip()
    left_pipette.drop_tip()

    # add precurser 2 , and right after. Adjusting from the top as to use one pipette
    
    right_pipette.pick_up_tip()
    left_pipette.pick_up_tip()
    pre_2 = 0
    for col in [1,2]:
        for row in rows:
            if pre_2 <= 50:
                if pre_2 != 0:
                    if pre_2 > 20:  
                        right_pipette.aspirate(pre_2, well1['A2'])
                        right_pipette.touch_tip()  
                        right_pipette.dispense(pre_2, plate[row + str(col)], rate = 5)
                        right_pipette.touch_tip()    
                    else: 
                        left_pipette.aspirate(pre_2, well1['A2'])
                        left_pipette.touch_tip()  
                        left_pipette.dispense(pre_2, plate[row + str(col)], rate = 5)
                        left_pipette.touch_tip()  
                    pre_2 += 5
                else: 
                    pre_2 += 5

    right_pipette.drop_tip()
    left_pipette.drop_tip()
    
    count = 0

    for col in [1,2]:
        for row in rows:
            if count <= 1750:
                right_pipette.pick_up_tip()
                right_pipette.aspirate(250, well1['A3'])
                right_pipette.dispense(250, plate[row + str(col)], rate = 3.0)
                right_pipette.drop_tip()
                count += 250
            else:
                right_pipette.pick_up_tip()
                right_pipette.aspirate(250, well1['A4'])
                right_pipette.dispense(250, plate[row + str(col)], rate = 3.0)
                count += 250
                right_pipette.drop_tip()


'''
    right_pipette.pick_up_tip()
    
    count = 0

    for col in [1,2]:
        for row in rows:
            if  row + str(col) != 'E2':
                if count <= 1750:
                    right_pipette.aspirate(250, plate[row + str(col)], rate = 0.5)
                    right_pipette.dispense(250, well1['A5'])
                    count += 250
                else:
                    right_pipette.aspirate(250, plate[row + str(col)], rate = 0.5)
                    right_pipette.dispense(250,  well1['A6'])
                    count += 250

    right_pipette.drop_tip()
'''



 









