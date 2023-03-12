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
    'protocolName': 'Perovskite AgBi Protocol ',
    'author': 'Martinez',
    'description': ' Mixing A and X sites accordingly ',
    'apiLevel': '2.12'
}

# Here Solution A is added accross the 96 well. Then, for each well from A1 - H12, both B,C are added
# Right after B,C are added in each well, choloform is placed to deactivate
# A --> Yellow B --> Blue C --> Red, Choloform --> Water

# each pair of 3 numbers represents the value of the pre-curser solutions you want in each well
# this matrix is a 96 well matrix

'''

total : 64ul 
32ul P0

2

1

'''
               # P0 P1 P2 P3
input_matrix = [[[32,32,0,0],[32,30,2,0],[32,28,4,0],[32,26,6,0],[32,24,8,0],[32,22,10,0],[32,20,12,0],[32,18,14,0],[32,16,16,0],[],[],[]],
				[[32,31,0,1],[32,29,2,1],[32,27,4,1],[32,25,6,1],[32,23,8,1],[32,21,10,1],[32,19,12,1],[32,17,14,1],[32,15,16,1],[],[],[]],
				[[32,30,0,2],[32,28,2,2],[32,26,4,2],[32,24,6,2],[32,22,8,2],[32,20,10,2],[32,18,12,2],[32,16,14,2],[32,14,16,2],[],[],[]],
				[[32,29,0,3],[32,27,2,3],[32,25,4,3],[32,23,6,3],[32,21,8,3],[32,19,10,3],[32,17,12,3],[32,15,14,3],[32,13,16,3],[],[],[]],
				[[32,28,0,4],[32,26,2,4],[32,24,4,4],[32,22,6,4],[32,20,8,4],[32,18,10,4],[32,16,12,4],[32,14,14,4],[32,12,16,4],[],[],[]],
				[[32,27,0,5],[32,25,2,5],[32,23,4,5],[32,21,6,5],[32,19,8,5],[32,17,10,5],[32,15,12,5],[32,13,14,5],[32,11,16,5],[],[],[]],
				[[32,26,0,6],[32,24,2,6],[32,22,4,6],[32,20,6,6],[32,18,8,6],[32,16,10,6],[32,14,12,6],[32,12,14,6],[32,10,16,7],[],[],[]],
				[[32,25,0,7],[32,23,2,7],[32,21,4,7],[32,19,6,7],[32,17,8,7],[32,15,10,7],[32,13,12,7],[32,11,14,7],[32,9,16,7],[],[],[]]]

columns = range(1,12 + 1)
rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

#input_matrix[0][2][1] --> will output 16 for reference. [row][column][0,1,2]
# right pipette 300
# left pipette 20ul 

def run(protocol: protocol_api.ProtocolContext):# labware for pipette tips

    well2 = protocol.load_labware('agilent_1_reservoir_290ml', location='4') # antisolvent

    tiprack_300_1 = protocol.load_labware('opentrons_96_tiprack_300ul', location = '7')
    tiprack_300_2 = protocol.load_labware('opentrons_96_tiprack_300ul', location = '8')

    tiprack_20_1 = protocol.load_labware('opentrons_96_tiprack_20ul', location = '9')
    tiprack_20_2 = protocol.load_labware('opentrons_96_tiprack_20ul', location = '10')

    temperature_module = protocol.load_module('temperature module', location = '1')
    temperature_module.set_temperature(90)
    well1 = temperature_module.load_labware('opentrons_24_aluminumblock_nest_2ml_snapcap')     # stock solution in 2ml tubes

    plate = protocol.load_labware('nest_96_wellplate_200ul_flat', location = '5') # unlimited 96 well microtiter plate 

    right = protocol.load_instrument('p300_single_gen2', mount='right', tip_racks=[tiprack_300_1,tiprack_300_2])
    left = protocol.load_instrument('p20_single_gen2', mount='left', tip_racks=[tiprack_20_1,tiprack_20_2])
    ########## START FUNCTION DEFINITION ############

    def matrix_retreive(row, column, inp = input_matrix): # you input a row and column on microtiter plate, gives you back value in the matrix
        return inp[ord(row) - 65][column -1]

    ########## END FUNCTION DEFINITION ############
    
    # precurser solution 0 --> A1
    # precurser solution 1 --> A2
    # precurser solution 2 --> A3
    # precurser solution 3 --> A4

    # add precurser 0 to all wells with appropriate values | 1 PIPETTE TIP

    
    right.pick_up_tip()
    left.pick_up_tip()

    for row in rows:
        for col in columns:
            mat = matrix_retreive(row, col)
            if mat != []: # checking if data has been inputed into the matrix at that location 
                data = mat[0] # this will be the amount for the first reagent
                if data >= 15 and data != 0: 
                    right.aspirate(data,well1['A1'])
                    right.touch_tip()
                    right.touch_tip() 
                    right.dispense(data, plate[row + str(col)])
                    right.touch_tip()
                    right.touch_tip() 
                elif data != 0:
                    left.aspirate(data, well1['A1'])
                    left.touch_tip()
                    left.touch_tip() 
                    left.dispense(data, plate[row + str(col)])
                    left.touch_tip()
                    left.touch_tip()

    right.drop_tip()
    left.drop_tip()

    # add precurser 2 and 3, and right after

# run addition of chloroform protocol

    for row in rows:
        for col in columns:
            mat = matrix_retreive(row, col)
            if mat != []: # checking if data has been inputed into the matrix at that location 
                data_pre_2 = mat[1]
                data_pre_3 = mat[2]
                data_pre_4 = mat[3]
                
                # precurser solution 1
                if data_pre_2 >= 15 and data_pre_2 != 0: # need to determine which tip to use based on size
                    right.pick_up_tip()
                    right.aspirate(data_pre_2, well1['A2'])
                    right.touch_tip()
                    right.touch_tip()
                    right.touch_tip()
                    right.dispense(data_pre_2, plate[row + str(col)])
                    right.touch_tip()
                    right.touch_tip()
                    right.touch_tip()
                    right.drop_tip()
                elif data_pre_2 != 0: 
                    left.pick_up_tip()
                    left.aspirate(data_pre_2, well1['A2'])
                    left.touch_tip()
                    left.touch_tip()
                    left.touch_tip() 
                    left.dispense(data_pre_2, plate[row + str(col)])
                    left.touch_tip()
                    left.touch_tip()
                    left.touch_tip()  
                    left.drop_tip()

                # precurser solution 2
                if data_pre_3 >= 15 and data_pre_3 != 0: # need to determine which tip to use based on size 
                    right.pick_up_tip()
                    right.aspirate(data_pre_3, well1['A3'])
                    right.touch_tip()
                    right.touch_tip()
                    right.touch_tip() 
                    right.dispense(data_pre_3, plate[row + str(col)])
                    right.touch_tip()
                    right.touch_tip()
                    right.touch_tip() 
                    right.drop_tip()
                elif data_pre_3 != 0:
                    left.pick_up_tip()
                    left.aspirate(data_pre_3, well1['A3'])
                    left.touch_tip()
                    left.touch_tip()
                    left.touch_tip() 
                    left.dispense(data_pre_3, plate[row + str(col)])
                    left.touch_tip()
                    left.touch_tip()
                    left.touch_tip() 
                    left.drop_tip()

                # precurser solution 2
                if data_pre_4 >= 15 and data_pre_4 != 0: # need to determine which tip to use based on size 
                    right.pick_up_tip()
                    right.aspirate(data_pre_4, well1['A4'])
                    right.touch_tip()
                    right.touch_tip()
                    right.touch_tip() 
                    right.dispense(data_pre_4, plate[row + str(col)])
                    right.touch_tip()
                    right.touch_tip()
                    right.touch_tip() 
                    right.drop_tip()

                elif data_pre_4 != 0:
                    left.pick_up_tip()
                    left.aspirate(data_pre_4, well1['A4'])
                    left.touch_tip()
                    left.touch_tip()
                    left.touch_tip() 
                    left.dispense(data_pre_4, plate[row + str(col)])
                    left.touch_tip()
                    left.touch_tip()
                    left.touch_tip() 
                    left.drop_tip()

    # add the chloroform 
    

    right.pick_up_tip()

    for row in rows:
        for col in columns:
            mat = matrix_retreive(row, col)
            if mat != []:
                right.aspirate(200, well2['A1'])
                right.touch_tip() 
                right.dispense(200, plate[row + str(col)])
                right.touch_tip() 

    right.drop_tip()













