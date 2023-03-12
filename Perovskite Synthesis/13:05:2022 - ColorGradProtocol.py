from opentrons import protocol_api

# metadata
metadata = {
    'protocolName': 'Color Gradient Protocol',
    'author': 'Toscanini & Martinez',
    'description': 'Makes a multi-color rainbow with increasing color saturation',
    'apiLevel': '2.12'
}

# protocol run function
def run(protocol: protocol_api.ProtocolContext):

    # labware
    tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', location='8')
    well1 = protocol.load_labware('opentrons_24_aluminumblock_nest_1.5ml_snapcap', location='1')
     # 2000 ul per well
    well2 = protocol.load_labware('agilent_1_reservoir_290ml', location='4')
     # unlimited
    plate = protocol.load_labware('opentrons_96_aluminumblock_biorad_wellplate_200ul', location='2')
     # 200 ul per well, 12x8 wells
    
    # pipette
    right_pipette = protocol.load_instrument(
         'p300_single_gen2', mount='right', tip_racks=[tiprack])
         
    def mixing(loc, vol, num = 3): # number of times you want to mix, 3 should be good
        count = 0
        while count != 3:
            right_pipette.aspirate(vol, plate[loc])
            right_pipette.dispense(vol, plate[loc])
            count += 1
    
    # commands
    x = range(1,13) # Controls the number of columns
    y = range(1,4) # Controls the number of rows
    increment = 2 # Controls the amount to subtract/add for each sample
        # Make sure that the pipette won't try to aspirate more than the available amount
    
    right_pipette.pick_up_tip()
    
    
    # dispense decreasing amounts of water across rows
    letter = 'A'
    for i in y:
        z = 150
        
        for j in x:
            right_pipette.aspirate(z,well2['A1'])
            right_pipette.dispense(z,plate[letter + str(j)])
            z -= increment
            
        letter = chr(ord(letter) + 1)
      
    del i,j
    
    # dispense increasing amounts of color across rows    
    letter = 'A'
    for i in y:
        right_pipette.drop_tip()
        right_pipette.pick_up_tip()
        z = 1 
        w = 'A' + str(i)
        
        for j in x:
            p = letter + str(j)
            right_pipette.aspirate(z,well1[w])
            right_pipette.dispense(z,plate[p])
            mixing(p, 100)
            z += increment
        
        letter = chr(ord(letter) + 1)
        
    right_pipette.drop_tip()
    