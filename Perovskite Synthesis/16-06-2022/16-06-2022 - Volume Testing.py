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
    'protocolName': 'Volume Testing',
    'author': 'Martinez',
    'description': 'Protocol is divded into two parts, first part 1. Then Part 2 for Chloroform. ',
    'apiLevel': '2.12'
}

# Here Solution A is added accross the 96 well. Then, for each well from A1 - H12, both B,C are added
# Right after B,C are added in each well, choloform is placed to deactivate
# A --> Yellow B --> Blue C --> Red, Choloform --> Water

# each pair of 3 numbers represents the value of the pre-curser solutions you want in each well
# this matrix is a 96 well matrix

input_matrix = [[[50,0,0],[38,4,8],[30,16,4],[26,12,12],[22,12,16],[18,16,16],[14,24,12],[10,36,4],[10,4,36],[6,20,24],[2,40,8],[2,8,40]],
				[[46,4,0],[38,0,12],[30,12,8],[26,8,16],[22,8,20],[18,12,20],[14,20,16],[10,32,8],[10,0,4],[6,16,28],[2,36,12],[2,4,44]],
				[[46,0,4],[34,16,0],[30,8,12],[26,4,20],[22,4,24],[18,8,24],[14,16,20],[10,28,12],[6,44,0],[6,12,32],[2,32,16],[2,0,48]],
				[[42,8,0],[34,12,4],[30,4,16],[26,0,24],[22,0,28],[18,4,28],[14,12,14],[10,24,16],[6,40,4],[6,8,36],[2,28,20],[]],
				[[42,4,4],[34,8,8],[30,0,20],[22,28,0],[18,32,0],[18,0,32],[14,8,28],[10,20,20],[6,36,8],[6,4,40],[2,24,24],[]],
				[[42,0,8],[34,4,12],[26,24,0],[22,24,4],[18,28,4],[14,36,0],[14,4,32],[10,16,24],[6,32,12],[6,0,44],[2,20,28],[]],
				[[38,12,0],[34,0,16],[26,20,4],[22,20,8],[18,24,8],[14,32,4],[14,0,36],[10,12,28],[6,28,16],[2,48,0],[2,16,32],[]],
				[[38,8,4],[30,20,0],[26,16,8],[22,16,12],[18,20,12],[14,28,12],[10,40,0],[10,8,32],[6,24,20],[2,44,4],[2,12,36],[]]]

columns = range(1,11 + 1)
rows = ['A'] # just for testing 

#input_matrix[0][2][1] --> will output 16 for reference. [row][column][0,1,2]
# right pipette 300
# left pipette 20ul 

def run(protocol: protocol_api.ProtocolContext):# labware for pipette tips
    tiprack_300_1 = protocol.load_labware('opentrons_96_tiprack_300ul', location = '7')

    tiprack_20_1 = protocol.load_labware('opentrons_96_tiprack_20ul', location = '9')

    well1 = protocol.load_labware('opentrons_24_aluminumblock_nest_2ml_snapcap', location='1')     # stock solution in 2ml tubes

    plate = protocol.load_labware('nest_96_wellplate_200ul_flat', location = '5') # unlimited 96 well microtiter plate 

    right = protocol.load_instrument('p300_single_gen2', mount='right', tip_racks=[tiprack_300_1])
    left = protocol.load_instrument('p20_single_gen2', mount='left', tip_racks=[tiprack_20_1])
    ########## START FUNCTION DEFINITION ############

    def matrix_retreive(row, column, inp = input_matrix): # you input a row and column on microtiter plate, gives you back value in the matrix
        return inp[ord(row) - 65][column -1]

    ########## END FUNCTION DEFINITION ############

    # precurser solution 1 --> A1
    # precurser solution 2 --> A2
    # precurser solution 3 --> A3
    # chloforom solution --> A4 --> Will need to change to a reservoir once we get this input

    # add precurser 1 to all wells with appropriate values | 1 PIPETTE TIP

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
                
                # precurser solution A2
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

                # precurser solution A3
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











