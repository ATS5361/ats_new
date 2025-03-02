import cv2

class Coordinates:
    def __init__(self, *args):
        super().__init__(*args)
        self.COORD_1_ToolNames = ["Tweezers", "Tweezers", "Tweezers", "Tweezers", "Tweezers", 
                                  "Hexacon Aid Black Stick", "Hexacon Aid Black Stick", "Soldier Pusher", "Soldier Pusher", "Telescopic Cicular Mirror 1-1/4", "Telescopic Cicular Mirror 2.1/4",
  "Magnifier Pocket", "Flexible Spring Pick Up Tool", "Parts Cleaning Brush", "Tape Rule", "Putty Knife", "Snap off Knife", "Telescoping Magnetic Pick Up Tool", "Scribe", "Chrome Telescoping Magnetic Pick Up Tool"
        ]#,"Rule"]

        self.dif = 17

        self.COORD_1_Groups = [0, 0, 0, 0, 0, 1, 1, 2, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        self.COORD_1_NumOfTools = [5, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        self.COORD_1_NumOfTools_Live = [0]*14
        self.COORD_1_NumOfTools_LiveAll = [0]*20
        
        self.COORD_1 =[[35, 35, 27, 330], [75, 35, 27, 330], [128, 49, 27, 311], [165, 135, 33, 230], [206, 135, 33, 230], [270, 38, 21, 287], [306, 38, 21, 287],
                       [343, 38, 21, 287], [379, 38, 21, 287], [190, 355, 250, 65], [15, 395, 370, 105], [43, 568, 105, 80], [195, 565, 325, 100], [440, 34, 450, 76], [927, 45, 145, 140], [492, 143, 415, 76],  [645, 258, 285, 77], [645, 362, 304, 40],
                       [550, 425, 404, 50], [776, 490, 206, 70]]

        ## 2. Çekmece Data ##

        self.COORD_2_ToolNames = ["Torque Ampilifier", "Nut Driver 3/32", "Nut Driver 1/8", "Nut Driver 5/32", "Nut Driver 3/16", "Nut Driver 7/32", "Nut Driver 1/4", "Nut Driver 9/32", "Nut Driver 5/16", "Nut Driver 11/32", "Nut Driver 1/2",
 "Socket Dip Dr 9/16", "Socket Dip Dr 1/2", "Socket Dip Dr 7/16", "Socket Dip Dr 3/8", "Socket Dip Dr 11/32", "Socket Dip Dr 5/16", "Socket Dip Dr 9/32", "Socket Dip Dr 1/4", "Socket Dip Dr 7/32", "Socket Dip Dr 3/16",
 "Socket Dr 9/16","Socket Dr 1/2","Socket Dr 7/16","Socket Dr 3/8","Socket Dr 11/32","Socket Dr 5/16","Socket Dr 9/32","Socket Dr 1/4","Socket Dr 7/32","Socket Dr 3/16",
 "Drive Hex Bit Socket 5/1", "Drive Hex Bit Socket 1/4", "Drive Hex Bit Socket 7/32", "Drive Hex Bit Socket 3/16", "Drive Hex Bit Socket 5/32", "Drive Hex Bit Socket 9/64", "Drive Hex Bit Socket 1/8", "Drive Hex Bit Socket 7/64", "Drive Hex Bit Socket 3/32", "Drive Hex Bit Socket 5/64", "Drive Hex Bit Socket 1/16",
 "Socket Dr M14", "Socket Dr M13", "Socket Dr M12", "Socket Dr M11", "Socket Dr M10", "Socket Dr M9", "Socket Dr M8", "Socket Dr M7", "Socket Dr M6", "Socket Dr M5.5", "Socket Dr M5", "Socket Dr M4",
 "Drive Deep Socket 9/32", "Drive Deep Socket 1/4", "Drive Deep Socket 7/32", "Drive Deep Socket 3/16", "Drive Deep Socket 5/32", "Drive Socket 9/32", "Drive Socket1/4", "Drive Socket 7/32", "Drive Socket 3/16", "Drive Socket 5/32",
 "Drive Magnetic Bit Holder 1/4", "Drive Magnetic Bit Holder 1/4", "Drive Magnetic Bit Holder 1/4", "Drive Adapter 1/4", "Drive Universal Joınt", "Drive Adapter 3/8", "Drive Flexible Extension",
 "Drive Extension 3", "Drive Extension 2", "Drive Extension 6", "Drive Extension 3/32", "Drive Dual Standart Hamdle Ratchet","Drive Dual Standart Hamdle Ratchet", "Drive Socket Drive",
 "Screwdrivers Philips PH0", "Screwdrivers Philips PH00", "Screwdrivers Slotted 1.8*50", "Screwdrivers Slotted 1.5*50","Screwdrivers Slotted 1.2*50", "Screwdrivers Slotted 1.0*50", "Wire Cutters", "Diagonal Midget", "Electrinics Diagonal Cutter Pliers", "Electrinics Diagonal Cutter Pliers",
 "Short Non-Serrated Jaws", "Angled Serrated Jaws", "Long Serrated Jaws"]

        self.COORD_2_Predefined_1 = [[110, 25, 174, 209], [209, 18, 244, 225], [275, 21, 309, 225], [343, 21, 375, 225], [408, 21, 440, 225], [473, 21, 507, 228], [536, 21, 572, 228], [598, 20, 636, 227], [664, 22, 700, 229], [727, 21, 766, 229], [789, 21, 830, 231]]
       
        self.COORD_2_Predefined_2_1 =  [[62, 48, 142, 109],[155, 52, 218, 107],[234, 58, 285, 107],[309, 61, 353, 103],[384, 64, 420, 102],[446, 67, 489, 105],[510, 68, 558, 104],[572, 69, 622, 103],[632, 69, 683, 103], [697, 72, 749, 100]]

        self.COORD_2_Predefined_2_2 =  [[85, 122, 149, 173],[168, 127, 219, 171],[243, 130, 287, 171],[313, 134, 350, 170],[382, 135, 416, 170],[448, 137, 479, 169],[510, 139, 540, 167],[567, 140, 603, 168],[623, 140, 659, 169],[684, 140, 721, 168]]

        self.COORD_2_Predefined_3_1 = [[108, 33, 164, 68], [172, 34, 222, 70], [236, 38, 275, 72], [295, 40, 327, 72], [349, 42, 380, 74], [402, 43, 432, 75], [453, 44, 487, 76], [506, 45, 543, 77], [554, 44, 598, 79],
                                     [609, 45, 661, 79], [666, 45, 719, 79]]
      
        self.COORD_2_Predefined_3_2 = [[91, 87, 149, 132],  [156, 88, 208, 132],  [217, 92, 263, 133],  [275, 93, 317, 134],  [331, 94, 369, 132],  [384, 98, 419, 132],  [435, 99, 466, 131],  [479, 102, 509, 131],  [521, 103, 553, 131], [565, 102, 597, 131], [606, 103, 642, 131], [650, 103, 687, 131]]

        self.COORD_2_Predefined_3_3 = [[30, 164, 82, 192],[84, 165, 136, 194], [139, 167, 190, 195],[200, 167, 244, 196],[252, 167, 284, 195],[317, 169, 346, 197],[363, 167, 393, 198],[409, 170, 438, 199],[461, 169, 490, 197],[502, 170, 531, 198],[565, 170, 604, 205],[611, 170, 650, 205],[661, 170, 700, 204],[713, 168, 758, 199],[768, 167, 825, 198],[825, 160, 876, 199]]

        self.COORD_2_Predefined_4 = [[54, 37, 94, 280], [123, 38, 161, 280], [192, 38, 230, 280], [259, 38, 294, 280], [326, 38, 361, 280], [396, 39, 431, 281]]


        # self.COORD_2_Predefined_1 = [[112, 83, 176, 260], [210, 69, 243, 270], [274, 70, 306, 270], [340, 75, 372, 269], [407, 73, 440, 270], [472, 73, 505, 270], [538, 73, 571, 269], [603, 73, 640, 269], [672, 73, 705, 269], [732, 73, 772, 269], [800, 73, 840, 269]]
       
        # self.COORD_2_Predefined_2_1 =  [[63,  69, 138, 126],[151,  73, 217, 127],[231,  76, 285, 124],[308,  81, 350, 123],[382,  81, 420, 121],[450,  84, 489, 123],[512,  87, 560, 123],[580,  88, 631, 123],[643,  89, 696, 121], [712,  89, 770, 119]]

        # self.COORD_2_Predefined_2_2 =  [[ 89, 142, 148, 16],[171, 147, 218, 191],[244, 150, 287, 192],[314, 153, 350, 190],[380, 154, 415, 189],[445, 155, 479, 188],[510, 157, 544, 189],[570, 157, 608, 190],[627, 159, 665, 189],[689, 158, 731, 191]]

        # self.COORD_2_Predefined_3_1 = [[112,  47, 168,  84], [173,  49, 220,  85], [234,  50, 274,  85], [295,  54, 326,  86], [349,  56, 378,  87], [401,  56, 432,  87], [454,  57, 488,  88], [506,  58, 545,  89], [559,  57, 602,  90],
        #                              [612,  58, 666,  91], [668,  57, 725,  91]]
      
        # self.COORD_2_Predefined_3_2 = [[96, 102, 152, 149],  [159, 104, 209, 148],  [219, 106, 264, 146],  [276, 108, 318, 147],  [332, 109, 369, 145],  [385, 111, 416, 143],  [434, 114, 465, 143],  [477, 115, 511, 142],  [521, 115, 554, 143], [567, 115, 601, 144], [611, 116, 647, 143], [655, 116, 694, 145]]

        # self.COORD_2_Predefined_3_3 = [[27, 180,  79, 212],[80, 181, 132, 212], [135, 182, 190, 211],[197, 181, 242, 214],[245, 182, 282, 212],[316, 182, 344, 210],[362, 181, 392, 210],[409, 182, 437, 210],[461, 183, 490, 211],[501, 183, 531, 212],[568, 184, 604, 217],[613, 184, 652, 217],[666, 184, 707, 218],[721, 182, 769, 215],[781, 182, 836, 216],[838, 174, 893, 217]]

        # self.COORD_2_Predefined_4 = [[ 46,  29,  86, 281], [114,  29, 153, 282], [184,  30, 222, 282], [248,  32, 285, 282], [317,  29, 353, 282], [386,  28, 421, 283]]
        
        
        self.COORD_2_Groups = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 
                               4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
                               6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 8, 8, 8, 9, 9, 9, 10, 11, 12, 13, 14, 15, 15, 16,
                               17, 17, 17, 17, 17, 17, 18, 19, 20, 20, 21, 22, 22]
        
        
        self.COORD_2_NumOfTools = [1, 10, 10, 10, 11, 12, 5, 5, 3, 3, 1, 1, 1, 1, 1, 2, 1, 6, 1, 1, 2, 1, 2]
        self.COORD_2_NumOfTools_Live = [0]*23
        self.COORD_2_NumOfTools_LiveAll = [0]*91
        
        self.COORD_2_DICT = {}

        self.COORD_2 =[[73, 34, 56, 155], [148, 29, 35, 173], [200, 29, 35, 173], [248, 29, 35, 173], [300, 29, 35, 173], [350, 29, 35, 173], [402, 29, 35, 173], [451, 29, 35, 173],
                        [501, 29, 35, 173], [551, 29, 35, 173], [600, 29, 35, 173], [41, 205, 43, 44], [100, 205, 43, 44], [156, 210, 36, 42], [214, 210, 33, 42], [266, 210, 33, 42], [318, 210, 33, 42], [368, 210, 32, 42], [418, 210, 31, 42],
                        [465, 210, 31, 42], [516, 210, 31, 42], [57, 263, 43, 42], [119, 263, 43, 42], [172, 263, 43, 42], [223, 263, 43, 42], [274, 270, 40, 40], [323, 270, 40, 40],
                        [373, 270, 39, 40], [423, 272, 37, 37], [466, 272, 36, 37], [513, 272, 36, 37], [65, 319, 43, 33], [116, 319, 43, 33], [161, 319, 40, 33], [202, 319, 40, 33],
                        [249, 319, 38, 33], [290, 319, 38, 33], [330, 319, 37, 33], [374, 319, 34, 33], [412, 319, 34, 33], [451, 319, 34, 33], [490, 319, 34, 33], [57, 360, 45, 40],
                        [105, 360, 43, 40], [152, 360, 43, 40], [197, 360, 37, 40], [237, 360, 38, 40], [280, 360, 33, 40], [317, 360, 33, 40], [351, 360, 33, 40], [385, 360, 33, 40],
                        [415, 360, 33, 40], [452, 360, 33, 40], [487, 360, 33, 40], [11, 428, 28, 28], [45, 428, 28, 28], [84, 428, 28, 28], [129, 428, 28, 28], [168, 428, 28, 28],
                        [227, 428, 28, 28], [261, 428, 28, 28], [296, 428, 28, 28], [338, 428, 28, 28], [371, 428, 28, 28], [421, 428, 30, 28], [462, 428, 28, 28], [499, 428, 28, 28],
                        [535, 428, 28, 28], [577, 425, 30, 30], [619, 416, 36, 36], [29, 476, 300, 32], [29, 523, 150, 32], [200, 523, 100, 32], [29, 568, 300, 32], [29, 610, 630, 32],
                        [329, 485, 211, 46], [329, 546, 211, 46], [426, 508, 273, 62], [663, 27, 35, 265], [713, 27, 35, 265], [764, 27, 35, 265], [815, 27, 35, 265], [866, 27, 35, 265],
                        [918, 27, 35, 265], [973, 42, 89, 240], [675, 298, 110, 200], [800, 308, 100, 200], [922, 308, 100, 200], [750, 373, 83, 280], [872, 373, 86, 280], [990, 373, 80, 280]]
        

        

        
        ## 5. Çekmece Data ##
        self.COORD_5_ToolNames = ["Short Combination Wrench 3/4", "Short Combination Wrench 11/16", "Short Combination Wrench 5/8", "Short Combination Wrench 9/16", "Short Combination Wrench 1/2","Short Combination Wrench 7/16","Short Combination Wrench 3/8","Short Combination Wrench 11/32","Short Combination Wrench 5/15",
"Short Combination Wrench 9/32","Short Combination Wrench 1/4","Ignition Wrench 1/8-1/8","Ignition Wrench 5/32-5/32","Ignition Wrench 3/16-3/16","Ignition Wrench 15/64-1/4","Ignition Wrench 1/4-15/64","Ignition Wrench 9/32-5/16","Ignition Wrench 5/16-9/32","Ignition Wrench 11/32-3/8"
,"Ignition Wrench 3/8-11/32","Combination Wrench M19","Combination Wrench M18","Combination Wrench M17","Combination Wrench M16","Combination Wrench M15","Combination Wrench M14","Combination Wrench M13","Combination Wrench M12","Combination Wrench M11","Combination Wrench M10"
,"Combination Wrench M9","Combination Wrench M8","Combination Wrench M7","Combination Wrench M6"]
        
        self.COORD_5_Groups = [0]*34
        
        self.COORD_5_NumOfTools = [1]*34
        self.COORD_5_NumOfTools_Live = [0]*34
        
        self.COORD_5_DICT = {}

        self.COORD_5_Predefined_1 =  [[58, 1, 92, 81], [128, 2, 161, 84], [191, 3, 224, 84],[252, 4, 284, 85],[313, 3, 342, 87],[370, 5, 396, 86],[424, 5, 448, 86],[475, 5, 498, 87],[526, 5, 547, 86],
                                    [573, 5, 590, 87], [612, 5, 628, 86], [651, 5, 666, 85], [690, 7, 706, 88], [726, 6, 740, 87]]
        
        self.COORD_5_Predefined_2 =   [[46, 12, 88, 83],[100, 12, 140, 82],[156, 12, 191, 82],[205, 13, 235, 83],[246, 15, 273, 86],[286, 14, 309, 84],[323, 14, 344, 84],[359, 15, 378, 86],[396, 15, 412, 86],
                                    [430, 15, 446, 85],[460, 16, 476, 87],[494, 15, 508, 88],[517, 15, 531, 88],[544, 15, 558, 88],[574, 16, 589, 87],[602, 16, 619, 87],[634, 16, 651, 87],[660, 16, 680, 86],[689, 16, 710, 87],[723, 16, 746, 87]]

        # self.COORD_5_Predefined_1 =  [[46, 11, 81, 99], [117, 9, 151, 100], [184, 8, 213, 101],[244, 10, 274, 99],[305, 9, 334, 101],[363, 6, 389, 98],[416, 5, 442, 97],[470, 7, 491, 99],[519, 7, 540, 98],
        #                             [566, 4, 582, 99], [605, 4, 621, 99], [646, 3, 659, 99], [685, 6, 698, 97], [718, 4, 730, 96]]
        
        # self.COORD_5_Predefined_2 =   [[38, 17, 79, 90],[91, 18, 132, 88],[147, 17, 182, 87],[197, 19, 224, 90],[239, 17, 264, 91],[278, 17, 300, 87],[315, 17, 335, 88],[352, 17, 373, 87],[389, 14, 405, 88],
        #                             [422, 16, 438, 89],[454, 17, 469, 88],[488, 16, 500, 89],[511, 14, 523, 88],[538, 16, 553, 87],[564, 16, 580, 86],[595, 15, 611, 88],[626, 16, 643, 87],[653, 14, 674, 88],[682, 15, 703, 85],[714, 16, 739, 89]]
        
        
        self.COORD_5 =[[20, 22, 75, 270], [109, 44, 75, 248], [187, 58, 73, 282-48], [263, 80, 64, 282-70], [330, 87, 55, 282-77], [388, 97, 50, 282-87], [441, 111, 47, 282-101],
                       [496, 116, 44, 293-106], [552, 126, 41, 293-116], [604, 129, 39, 293-119], [650, 139, 38, 293-129], [703, 153, 22, 293-143], [734, 153, 22, 293-143], [775, 152, 22, 293-142],
                       [816, 147, 22, 301-137], [856, 144, 28, 301-134], [903, 144, 28, 301-134], [943, 128, 30, 301-118], [985, 128, 30, 301-118], [1033, 125, 32, 301-115], [28, 305, 86, 646 - 290],
                       [139, 323, 82, 646 - 308], [236, 328, 78, 646 - 313], [331, 333, 73, 646 - 318], [422, 345, 70, 646 - 330], [506, 350, 70, 646 - 335], [589, 365, 62, 646 - 350],
                       [665, 380, 53, 646 - 365], [738, 384, 52, 646 - 369], [805, 390, 48, 646 - 375], [867, 400, 44, 646 - 385], [923, 410, 42, 646 - 395], [980, 420, 41, 646 - 405],
                       [1030, 428, 39, 646 - 413]]
        

        #Çekmece 3

        self.COORD_3_ToolNames = ["Slotted Keystone Round Bar Screwdrivers 5/16", "Slotted Keystone Round Bar Screwdrivers 1/4", "Slotted Round Bar Cabined Screwdrivers 3/16x5", "Slotted Round Bar Cabined Screwdrivers 3/16x4", "Slotted Round Bar Cabined Screwdrivers 3/16x3","Magnetic Screwdriver","Standart Screwdriver","Round Bar Screwdriver 3x6","Round Bar Screwdriver 2x4","Round Bar Screwdriver 1x3","Round Bar Screwdriver 0x3","bits","bits","bits","bits","bits","bits","bits","bits","bits","bits","bits","bits","bits","bits","bits","bits","bits","bits","Screwdriver Offset","T-Handle Hex Key","T-Handle Hex Key","T-Handle Hex Key 4x350"]
        self.COORD_3 =[[43, 23, 75, 512], [136, 36, 75, 400], [224, 36, 55, 430], [303, 36, 55, 390], [380, 37, 55, 340], [107, 490, 221, 71], [110, 603, 420, 71], [472, 36, 65, 490], 
                       [558, 36, 66, 400], [642, 47, 52, 325], [723, 47, 45, 290], [814, 50, 25, 25], [857, 50, 25, 25], [903, 50, 25, 25], [950, 50, 25, 25], [993, 50, 25, 25],
                       [1037, 50, 25, 25], [814, 93, 25, 25], [857, 93, 25, 25], [903, 93, 25, 25], [950, 93, 25, 25], [993, 93, 25, 25],  [1037, 93, 25, 25],
                       [814, 140, 25, 25], [857, 140, 25, 25], [903, 140, 25, 25], [950, 140, 25, 25], [993, 140, 25, 25],  [1037, 140, 25, 25], [801, 202, 192, 93], [775, 305, 270, 146], [622, 403, 288, 145], [381, 493, 696, 164],
                       ]
        
        self.COORD_3_Groups = [0, 0, 0, 0, 0, 1, 2, 3, 3, 3, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 7, 8, 9]
        self.COORD_3_NumOfTools_Live = [0]*10
        self.COORD_3_NumOfTools = [5, 1, 1, 3, 1, 18, 1, 1, 1, 1]
        self.COORD_3_NumOfTools_LiveAll = [0]*33

        self.COORD_3_Predefined_1 = [[62, 29, 128, 203], [154, 38, 210, 202], [234, 38, 283, 204], [310, 39, 359, 204], [387, 41, 435, 203]]
        
        self.COORD_3_Predefined_2 = [[38, 36, 110, 198], [131, 38, 192, 198], [214, 44, 267, 198], [296, 46, 336, 198]]
        


        # self.COORD_3_Predefined_1 = [[ 60,  33, 122, 199], [148,  40, 205, 199], [227,  39, 276, 200], [303,  40, 353, 201], [381,  40, 430, 202]]
        # self.COORD_3_Predefined_2 = [[ 40,  47,  109, 199], [ 129,  48, 191, 198], [212,  52, 265, 198], [297,  53, 336, 198]]
        

        #Çekmece 4

        self.COORD_4_ToolNames = ["Mini Pliers", "Scissors 7 inch", "Scissors 4 inch", "Scissors 4 inch", "Strap Wrench","Strap Wrench","Panduit Cable","Diagonal Cutting Pliers","Needle Nose Pliers","Lineman's Pliers","Soft Jaw Cannon Plug","Lock Joint Pliers"]
        self.COORD_4_Groups = [0, 1, 2, 2, 3, 3, 4, 5, 6, 7, 8, 9]
        
        self.COORD_4_NumOfTools = [1, 1, 2, 2, 1, 1, 1, 1, 1, 1]
        self.COORD_4_NumOfTools_Live = [0]*10
        self.COORD_4_NumOfTools_LiveAll = [0]*12
        
        self.COORD_4 =[[45, 37, 320, 140], [368, 95, 352, 130], [730, 125, 175, 82], [865, 58, 172, 86], [177, 142, 363, 161], [25, 230, 375, 154], [18, 390, 382, 260],
                       [403, 328, 102, 332], [522, 312, 104, 348], [640, 270, 110, 390], [775, 220, 138, 440], [940, 210, 120, 450]]
        
        
        #Çekmece 6
        
        self.COORD_6_ToolNames = ["Hex Key", "Hex Key", "Hex Key", "Hex Key", "Hex Key", "Hex Key", "Hex Key", "Hex Key", "Hex Key",
                                  "Hex Key", "Hex Key", "Hex Key", "Hex Key", "Hex Key", "Hex Key", "Hex Key", "Hex Key", "Hex Key", 
                                  "Reversible Ratcheting Wrench", "Reversible Ratcheting Wrench", "Reversible Ratcheting Wrench", "Reversible Ratcheting Wrench",
                                  "Reversible Ratcheting Wrench", "Reversible Ratcheting Wrench", "Reversible Ratcheting Wrench", "Reversible Ratcheting Wrench", "Reversible Ratcheting Wrench",
                                  "Adjustable Wrench", "Ruler" ]
        self.COORD_6_Groups = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 2, 2, 3, 3, 3, 4, 5, 6]
        self.COORD_6_NumOfTools = [18, 2, 3, 3, 1, 1, 1]
        self.COORD_6_NumOfTools_Live = [0]*7
        self.COORD_6_NumOfTools_LiveAll = [0]*29
        #self.COORD_6_Predefined_1 = [[23, 36, 37, 58], [74, 36, 86, 58], [124, 36, 134, 58], [168, 37, 177, 60], [208, 37, 214, 60], [243, 37, 249, 60],
                                     #[277, 37, 283, 59], [311, 37, 317, 59], [344, 38, 350, 61], [379, 37, 384, 59]]
        self.COORD_6_Predefined_1 = [[10, 50, 24, 74], [74, 36, 86, 58], [124, 36, 134, 58], [168, 37, 177, 60], [208, 37, 214, 60], [243, 37, 249, 60],
                                     [277, 37, 283, 59], [311, 37, 317, 59], [344, 38, 350, 61], [379, 37, 384, 59]] 

        self.COORD_6_Predefined_2 = [[39, 27, 49, 50], [85, 27, 94, 50], [128, 27, 135, 50], [167, 27, 173, 50], [205, 27, 211, 50], 
                                     [243, 27, 249, 50], [276, 27, 282, 50], [308, 28, 314, 51]]
        
        self.COORD_6 =[[44, 63, 84, 337], [142, 63, 77, 295], [237, 63, 62, 269], [314, 63, 62, 237], [386, 63, 57, 224], [455, 63, 50, 213], [519, 63, 45, 197],
                       [580, 63, 44, 190], [642, 63, 42, 180], [708, 63, 40, 171], [72, 495, 64, 160], [161, 495, 57, 154], [240, 495, 50, 145], [315, 495, 50, 125],
                       [385, 495, 47, 120], [460, 495, 43, 115], [520, 495, 42, 105], [580, 495, 40, 100], [825, 89, 222, 30], [825, 127, 222, 33],  [800, 175, 247, 38], [800, 225, 247, 38],
                       [785, 278, 262, 41], [768, 332, 282, 42], [760, 388, 290, 43], [740, 455, 308, 52], [715, 518, 333, 55], [778, 585, 270, 76], [105, 405, 565, 60]]

    def splitLine(self, line, tool, width):
        tool_in_place = 0
        class_id, x, _, w, _ = map(float, line.split())

        read_x_center = int(x * width)
        read_w = int(w * width)


        read_x1 = read_x_center - read_w//2
        read_x2 = read_x1 + read_w

        predefined_x1, _, predefined_x2, _ = tool


        if abs(read_x1 - predefined_x1) <= 20 and abs(read_x2 - predefined_x2) <= 20:
            tool_in_place = 1
           
        return tool_in_place