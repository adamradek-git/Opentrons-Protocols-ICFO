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
    'description': "Replicating the protocol from Higgins with 96-well. However, using Food coloring for precurser solutions.",
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

columns = range(1,12 + 1)
rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

#input_matrix[0][2][1] --> will output 16 for reference. [row][column][0,1,2]

def run(protocol: protocol_api.ProtocolContext):
    # labware for pipette tips
    tiprack_300_1 = protocol.load_labware('opentrons_96_tiprack_300ul', location = '7')
    tiprack_300_2 = protocol.load_labware('opentrons_96_tiprack_300ul', location = '8')
    tiprack_20 = protocol.load_labware('opentrons_96_tiprack_20ul', location = '9')

    # stock solution in 2ml tubes
    well1 = protocol.load_labware('opentrons_24_aluminumblock_nest_2ml_snapcap', location='1')

    # Chloroform reservoir(just a tube here ... not sure how to replicate) 
    well2 = protocol.load_labware('agilent_1_reservoir_290ml', location='4')

    # unlimited 96 well microtiter plate 
    plate = protocol.load_labware('nest_96_wellplate_200ul_flat', location = '5')
    
    # pipette configuration --> using both right and left tips
    right_pipette = protocol.load_instrument('p300_single_gen2', mount='right', tip_racks=[tiprack_300_1,tiprack_300_2])
    left_pipette = protocol.load_instrument('p20_single_gen2', mount='left', tip_racks=[tiprack_20])

    ########## START FUNCTION DEFINITION ############

    def mixing(loc, vol, num = 3): # number of times you want to mix, 3 should be good
        count = 0
        while count != 3:
            right_pipette.aspirate(vol, plate[loc])
            right_pipette.dispense(vol, plate[loc])
            count += 1

    def matrix_retreive(row, column, inp = input_matrix): # you input a row and column on microtiter plate, gives you back value in the matrix
        return inp[ord(row) - 65][column -1]

    ########## END FUNCTION DEFINITION ############

    # precurser solution 1 --> A1
    # precurser solution 2 --> A2
    # precurser solution 3 --> A3
    # chloforom solution --> A4 --> Will need to change to a reservoir once we get this input

    # add precurser 1 to all wells with appropriate values | 1 PIPETTE TIP

    right_pipette.pick_up_tip()

    for row in rows:
    	for col in columns:
    		mat = matrix_retreive(row, col)
    		if mat != []: # checking if data has been inputed into the matrix at that location 
	    		data = mat[0] # this will be the amount for the first reagent
                if (data <= 10):
                    left_pipette.aspirate(data,well1['A1'])
                    left_pipette.dispense(data, plate[row + str(col)])
                else:
                    right_pipette.aspirate(data,well1['A1'])
                    right_pipette.dispense(data, plate[row + str(col)])

    right_pipette.drop_tip()

    # add precurser 2 and 3, and right after

    for row in rows:
        for col in columns:
            mat = matrix_retreive(row, col)
            if mat != []: # checking if data has been inputed into the matrix at that location 
                data_pre_2 = mat[1]
                data_pre_3 = mat[2]
                # precurser solution A2
                if data_pre_2 > 10: # need to determine which tip to use based on size
                    right_pipette.pick_up_tip()
                    right_pipette.aspirate(data_pre_2, well1['A2'])
                    right_pipette.dispense(data_pre_2, plate[row + str(col)])
                    right_pipette.drop_tip()
                else: 
                    left_pipette.pick_up_tip()
                    left_pipette.aspirate(data_pre_2, well1['A2'])
                    left_pipette.dispense(data_pre_2, plate[row + str(col)])
                    left_pipette.drop_tip()

	    		# precurser solution A3
                if data_pre_2 > 10: # need to determine which tip to use based on size 
                    right_pipette.pick_up_tip()
                    right_pipette.aspirate(data_pre_3, well1['A3'])
                    right_pipette.dispense(data_pre_3, plate[row + str(col)])
                    mixing(row + str(col), 20)
                    right_pipette.drop_tip()
                else:
                    left_pipette.pick_up_tip()
                    left_pipette.aspirate(data_pre_3, well1['A3'])
                    left_pipette.dispense(data_pre_3, plate[row + str(col)])
                    mixing(row + str(col), 20)
                    left_pipette.drop_tip() 



	    		# add cholorform
                '''
                right_pipette.pick_up_tip()
                right_pipette.aspirate(10, well1['A3']) # would need to change to 300ul, would be well 2
                right_pipette.dispense(10, plate[row + str(col)]) # would need to change to 300ul, would be well 2

                right_pipette.drop_tip()
                '''   

############ working code, do not look here ##########

'''
def matrix_retreive(row, column, inp = input_matrix): # you input a row and column on microtiter plate, gives you back value in the matrix
    return inp[ord(row) - 65][column -1]

print(matrix_retreive('A',1))

for row in rows:
    for col in columns:
        mat = matrix_retreive(row, col, input_matrix)
        print(mat)
'''        













