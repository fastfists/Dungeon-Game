''' A moudle of dictionaries that have tuples (TopX,TopY,width,height) '''

# 17 is a floor tile, the rest are wall tiles.
Tile_ref = {1 : (0, 0, 32, 32),
        2 : (32, 0, 32, 32),
        3 : (64, 0, 32, 32),
        4 : (96, 0, 32, 32),
        5 : (0, 32, 32, 32),
        6 : (32, 32, 32, 32),
        7 : (64, 32, 32, 32),
        8 : (96, 32, 32, 32),
        9 : (0, 64, 32, 32),
        10 : (32, 64, 32, 32),
        11 : (64, 64, 32, 32),
        12 : (96, 64, 32, 32),
        13 : (0, 96, 32, 32),
        14 : (32, 96, 32, 32),
        15 : (64, 96, 32, 32),
        16 : (96, 96, 32, 32),
        17 : (0, 128, 32, 32),
        18 : (32, 128, 32, 32)}

Ranger_ref = {1 : (9, 1, 16, 32),
              2 : (41, 1, 16, 32),
              3 : (73, 1, 16, 32),
              4 : (105, 1, 16, 32),
              5 : (137, 1, 16, 32),
              6 : (169, 1, 16, 32),
              7 : (201, 1, 16, 32),
              8 : (233, 1, 16, 32),
              9 : (265, 1, 16, 32),
              10 : (297, 1, 16, 32),
              11 : (9, 33, 16, 32),
              12 : (41, 33, 16, 32),
              13 : (72, 33, 16, 32),
              14 : (103, 33, 16, 32),
              15 : (133, 33, 16, 32),
              16 : (165, 33, 16, 32),
              17 : (196, 33, 16, 32),
              18 : (228, 33, 16, 32),
              19 : (262, 33, 16, 32),
              20 : (296, 33, 16, 32),
              21 : (9, 65, 16, 32),
              22 : (40, 65, 16, 32),
              23 : (74, 64, 16, 32),
              24 : (107, 65, 16, 32),
              25 : (137, 66, 16, 32),
              26 : (167, 65, 16, 32),
              27 : (199, 65, 16, 32),
              28 : (231, 64, 16, 32),
              29 : (264, 65, 16, 32),
              30 : (297, 66, 16, 32),
              31 : (9, 97, 16, 32),
              32 : (42, 97, 16, 32),
              33 : (74, 97, 16, 32),
              34 : (106, 97, 16, 32),
              35 : (138, 96, 16, 32),
              36 : (170, 96, 16, 32),
              37 : (202, 96, 16, 32),
              38 : (234, 96, 16, 32),
              39 : (267, 96, 16, 32),
              40 : (298, 97, 16, 32),
              41 : (7, 129, 16, 32),
              42 : (38, 129, 16, 32),
              43 : (71, 129, 16, 32),
              44 : (103, 129, 16, 32),
              45 : (136, 129, 16, 32),
              46 : (169, 129, 16, 32),
              47 : (200, 132, 16, 32),
              48 : (231, 136, 16, 32),
              49 : (264, 143, 16, 32),
              50 : (295, 150, 16, 32)}
              
Skeleton_ref = {1 : (9, 1, 20, 31),
                2 : (41, 1, 20, 31),
                3 : (73, 1, 20, 31),
                4 : (105, 1, 20, 31),
                5 : (137, 1, 20, 31),
                6 : (169, 1, 20, 31),
                7 : (201, 1, 20, 31),
                8 : (233, 1, 20, 31),
                9 : (265, 1, 20, 31),
                10 : (297, 1, 20, 31),
                11 : (9 - 5, 33, 23, 30),
                12 : (41 - 5, 33, 23, 30),
                13 : (73 - 5, 33, 23, 30),
                14 : (105 - 5, 33, 23, 30),
                15 : (137 - 5, 33, 23, 30),
                16 : (169 - 5, 33, 23, 30),
                17 : (201 - 5, 33, 23, 30),
                18 : (233 - 5, 33, 23, 30),
                19 : (265 - 5, 33, 23, 30),
                20 : (297 - 5, 33, 23, 30),              
                21 : (9, 65, 20, 30),
                22 : (40, 65, 20, 30),
                23 : (74, 64, 20, 31),
                24 : (107, 65, 20, 30),
                25 : (137, 66, 20, 29),
                26 : (167, 65, 20, 30),
                27 : (199, 65, 20, 30),
                28 : (231, 64, 20, 31),
                29 : (264, 65, 20, 30),
                30 : (297, 66, 20, 29),
                31 : (9, 97, 20, 30),
                32 : (42, 97, 20, 30),
                33 : (74, 97, 20, 30),
                34 : (106, 97, 20, 30),
                35 : (138, 96, 20, 31),
                36 : (170, 96, 20, 31),
                37 : (202, 96, 20, 31),
                38 : (234, 96, 20, 31),
                39 : (267, 96, 20, 31),
                40 : (298, 97, 20, 30),
                41 : (7, 129, 20, 30),
                42 : (38, 129, 20, 30),
                43 : (71, 129, 20, 30),
                44 : (103, 129, 20, 30),
                45 : (136, 129, 20, 30),
                46 : (169, 129, 20, 30),
                47 : (200, 129, 20, 27),
                48 : (231, 129, 20, 23),
                49 : (264, 129, 20, 16),
                50 : (295, 129, 20, 9)}


Rouge_ref = {1 : (9, 1, 16, 32),
             2 : (41, 1, 16, 32),
             3 : (73, 1, 16, 32),
             4 : (105, 1, 16, 32),
             5 : (137, 1, 16, 32),
             6 : (169, 1, 16, 32),
             7 : (201, 1, 16, 32),
             8 : (233, 1, 16, 32),
             9 : (265, 1, 16, 32),
             10 : (297, 1, 16, 32),
             11 : (9, 33, 16, 32),
             12 : (41, 33, 16, 32),
             13 : (73, 33, 16, 32),
             14 : (105, 33, 16, 32),
             15 : (137, 33, 16, 32),
             16 : (169, 33, 16, 32),
             17 : (201, 33, 16, 32),
             18 : (233, 33, 16, 32),
             19 : (265, 33, 16, 32),
             20 : (297, 33, 16, 32),
             21 : (9, 65, 16, 32),
             22 : (41, 65, 16, 32),
             23 : (73, 65, 16, 32),
             24 : (105, 65, 16, 32),
             25 : (137, 66, 16, 32),
             26 : (169, 65, 16, 32),
             27 : (201, 65, 16, 32),
             28 : (233, 65, 16, 32),
             29 : (265, 65, 16, 32),
             30 : (297, 66, 16, 32),
             31 : (9, 97, 16, 32),
             32 : (42, 97, 16, 32),
             33 : (74, 97, 16, 32),
             34 : (106, 97, 16, 32),
             35 : (139, 97, 16, 32),
             36 : (171, 97, 16, 32),
             37 : (202, 97, 16, 32),
             38 : (234, 97, 16, 32),
             39 : (267, 97, 16, 32),
             40 : (298, 97, 16, 32),
             41 : (9, 129, 16, 32),
             42 : (41, 129, 16, 32),
             43 : (73, 129, 16, 32),
             44 : (105, 130, 16, 32),
             45 : (137, 131, 16, 32),
             46 : (169, 134, 16, 32),
             47 : (201, 137, 16, 32),
             48 : (233, 141, 16, 32),
             49 : (265, 145, 16, 32),
             50 : (29, 153, 16, 32)}

# use 53 as open ... for now
Door_ref = {1 : (0,0,32,32),
             2 : (32,0,32,32),
             3 : (64,0,32,32),
             4 : (96,0,32,32),
             5 : (128,0,32,32),
             6 : (160,0,32,32),
             7 : (192,0,32,32),
             8 : (224,0,32,32),
             9 : (256,0,32,32),
             10 : (0,32,32,32),
             11 : (32,32,32,32),
             12 : (64,32,32,32),
             13 : (96,32,32,32),
             14 : (128,32,32,32),
             15 : (160,32,32,32),
             16 : (192,32,32,32),
             17 : (224,32,32,32),
             18 : (256,32,32,32),
             19 : (0,64,32,32),
             20 : (32,64,32,32),
             21 : (64,64,32,32),
             22 : (96,64,32,32),
             23 : (128,64,32,32),
             24 : (160,64,32,32),
             25 : (192,64,32,32),
             26 : (224,64,32,32),
             27 : (256,64,32,32),
             28 : (0,96,32,32),
             29 : (32,96,32,32),
             30 : (64,96,32,32),
             31 : (96,96,32,32),
             32 : (128,96,32,32),
             33 : (160,96,32,32),
             34 : (192,96,32,32),
             35 : (224,96,32,32),
             36 : (256,96,32,32),
             37 : (0,128,32,32),
             38 : (32,128,32,32),
             39 : (64,128,32,32),
             40 : (96,128,32,32),
             41 : (128,128,32,32),
             42 : (160,128,32,32),
             43 : (192,128,32,32),
             44 : (224,128,32,32),
             45 : (256,128,32,32),
             46 : (0,160,32,32),
             47 : (32,160,32,32),
             48 : (64,160,32,32),
             49 : (96,160,32,32),
             50 : (128,160,32,32),
             51 : (160,160,32,32),
             52 : (192,160,32,32),
             53 : (224,160,32,32),
             54 : (256,160,32,32),
             55 : (0,192,32,32),
             56 : (32,192,32,32),
             57 : (64,192,32,32),
             58 : (96,192,32,32),
             59 : (128,192,32,32),
             60 : (160,192,32,32),
             61 : (192,192,32,32),
             62 : (224,192,32,32),
             63 : (256,192,32,32),
             64 : (0,224,32,32),
             65 : (32,224,32,32),
             66 : (64,224,32,32),
             67 : (96,224,32,32),
             68 : (128,224,32,32),
             69 : (160,224,32,32),
             70 : (192,224,32,32),
             71 : (224,224,32,32),
             72 : (256,224,32,32),
             73 : (0,256,32,32),
             74 : (32,256,32,32),
             75 : (64,256,32,32),
             76 : (96,256,32,32),
             77 : (128,256,32,32),
             78 : (160,256,32,32),
             79 : (192,256,32,32),
             80 : (224,256,32,32),
             81 : (256,256,32,32),
             82 : (0,288,32,32),
             83 : (32,288,32,32),
             84 : (64,288,32,32),
             85 : (96,288,32,32),
             86 : (128,288,32,32),
             87 : (160,288,32,32),
             88 : (192,288,32,32),
             89 : (224,288,32,32),
             90 : (256,288,32,32)}

sword_slash_ref = None

sci_fi_ref = {  1 : (0, 0, 31, 31),
        2 : (32, 0, 31, 31),
        3 : (64, 0, 31, 31),
        4 : (96, 0, 31, 31),
        5 : (128, 0, 31, 31),
        6 : (160, 0, 31, 31),
        7 : (192, 0, 31, 31),
        8 : (224, 0, 31, 31),
        9 : (256, 0, 31, 31),
        10 : (288, 0, 31, 31),
        11 : (320, 0, 31, 31),
        12 : (352, 0, 31, 31),
        13 : (384, 0, 31, 31),
        14 : (416, 0, 31, 31),
        15 : (0, 32, 31, 31),
        16 : (32, 32, 31, 31),
        17 : (64, 32, 31, 31),
        18 : (96, 32, 31, 31),
        19 : (128, 32, 31, 31),
        20 : (160, 32, 31, 31),
        21 : (192, 32, 31, 31),
        22 : (224, 32, 31, 31),
        23 : (256, 32, 31, 31),
        24 : (288, 32, 31, 31),
        25 : (320, 32, 31, 31),
        26 : (352, 32, 31, 31),
        27 : (384, 32, 31, 31),
        28 : (416, 32, 31, 31),
        29 : (0, 64, 31, 31),
        30 : (32, 64, 31, 31),
        31 : (64, 64, 31, 31),
        32 : (96, 64, 31, 31),
        33 : (128, 64, 31, 31),
        34 : (160, 64, 31, 31),
        35 : (192, 64, 31, 31),
        36 : (224, 64, 31, 31),
        37 : (256, 64, 31, 31),
        38 : (288, 64, 31, 31),
        39 : (320, 64, 31, 31),
        40 : (352, 64, 31, 31),
        41 : (384, 64, 31, 31),
        42 : (416, 64, 31, 31),
        43 : (0, 96, 31, 31),
        44 : (32, 96, 31, 31),
        45 : (64, 96, 31, 31),
        46 : (96, 96, 31, 31),
        47 : (128, 96, 31, 31),
        48 : (160, 96, 31, 31),
        49 : (192, 96, 31, 31),
        50 : (224, 96, 31, 31),
        51 : (256, 96, 31, 31),
        52 : (288, 96, 31, 31),
        53 : (320, 96, 31, 31),
        54 : (352, 96, 31, 31),
        55 : (384, 96, 31, 31),
        56 : (416, 96, 31, 31),
        57 : (0, 128, 31, 31),
        58 : (32, 128, 31, 31),
        59 : (64, 128, 31, 31),
        60 : (96, 128, 31, 31),
        61 : (128, 128, 31, 31),
        62 : (160, 128, 31, 31),
        63 : (192, 128, 31, 31),
        64 : (224, 128, 31, 31),
        65 : (256, 128, 31, 31),
        66 : (288, 128, 31, 31),
        67 : (320, 128, 31, 31),
        68 : (352, 128, 31, 31),
        69 : (384, 128, 31, 31),
        70 : (416, 128, 31, 31),
        71 : (0, 160, 31, 31),
        72 : (32, 160, 31, 31),
        73 : (64, 160, 31, 31),
        74 : (96, 160, 31, 31),
        75 : (128, 160, 31, 31),
        76 : (160, 160, 31, 31),
        77 : (192, 160, 31, 31),
        78 : (224, 160, 31, 31),
        79 : (256, 160, 31, 31),
        80 : (288, 160, 31, 31),
        81 : (320, 160, 31, 31),
        82 : (352, 160, 31, 31),
        83 : (384, 160, 31, 31),
        84 : (416, 160, 31, 31)}