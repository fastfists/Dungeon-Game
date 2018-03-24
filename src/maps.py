''' A moudle of dictionaries that have tuples (TopX,TopY,width,height) '''

# sprites 2 - 70 are traditional tiles, 71 - 73 are special tiles, The rest are ceilings(74 - )
Tiles_and_ceil_ref =   {2 : (0,0,16,16),
                    3 : (16,0,16,16),
                    4 : (32,0,16,16),
                    5 : (48,0,16,16),
                    6 : (64,0,16,16),
                    7 : (80,0,16,16),
                    8 : (96,0,16,16),
                    9 : (112,0,16,16),
                    10 : (128,0,16,16),
                    11 : (144,0,16,16),
                    12 : (160,0,16,16),
                    13 : (176,0,16,16),
                    14 : (192,0,16,16),
                    15 : (208,0,16,16),
                    16 : (224,0,16,16),
                    17 : (240,0,16,16),
                    18 : (256,0,16,16),
                    19 : (272,0,16,16),
                    20 : (288,0,16,16),
                    21 : (304,0,16,16),
                    22 : (320,0,16,16),
                    23 : (336,0,16,16),
                    24 : (352,0,16,16),
                    25 : (368,0,16,16),
                    26 : (384,0,16,16),
                    27 : (400,0,16,16),
                    28 : (416,0,16,16),
                    29 : (432,0,16,16),
                    30 : (448,0,16,16),
                    31 : (464,0,16,16),
                    32 : (0,16,16,16),
                    33 : (16,16,16,16),
                    34 : (32,16,16,16),
                    35 : (48,16,16,16),
                    36 : (64,16,16,16),
                    37 : (80,16,16,16),
                    38 : (96,16,16,16),
                    39 : (112,16,16,16),
                    40 : (128,16,16,16),
                    41 : (144,16,16,16),
                    42 : (160,16,16,16),
                    43 : (176,16,16,16),
                    44 : (192,16,16,16),
                    45 : (208,16,16,16),
                    46 : (224,16,16,16),
                    47 : (240,16,16,16),
                    48 : (256,16,16,16),
                    49 : (272,16,16,16),
                    50 : (288,16,16,16),
                    51 : (304,16,16,16),
                    52 : (320,16,16,16),
                    53 : (336,16,16,16),
                    54 : (352,16,16,16),
                    55 : (368,16,16,16),
                    56 : (384,16,16,16),
                    57 : (400,16,16,16),
                    58 : (416,16,16,16),
                    59 : (432,16,16,16),
                    60 : (448,16,16,16),
                    61 : (464,16,16,16),
                    62 : (0,32,16,16),
                    63 : (16,32,16,16),
                    64 : (32,32,16,16),
                    65 : (48,32,16,16),
                    66 : (64,32,16,16),
                    67 : (80,32,16,16),
                    68 : (96,32,16,16),
                    69 : (112,32,16,16),
                    70 : (128,32,16,16),
                    71 : (144,32,16,16),
                    72 : (160,32,16,16),
                    73 : (176,32,16,16),
                    74 : (0,48,16,16),
                    75 : (16,48,16,16),
                    76 : (32,48,16,16),
                    77 : (48,48,16,16),
                    78 : (64,48,16,16),
                    79 : (80,48,16,16),
                    80 : (96,48,16,16),
                    81 : (112,48,16,16),
                    82 : (128,48,16,16),
                    83 : (144,48,16,16),
                    84 : (160,48,16,16),
                    85 : (176,48,16,16),
                    86 : (192,48,16,16),
                    87 : (208,48,16,16),
                    88 : (224,48,16,16),
                    89 : (240,48,16,16),
                    90 : (256,48,16,16),
                    91 : (272,48,16,16),
                    92 : (288,48,16,16),
                    93 : (304,48,16,16),
                    94 : (320,48,16,16),
                    95 : (336,48,16,16),
                    96 : (352,48,16,16),
                    97 : (368,48,16,16),
                    98 : (384,48,16,16),
                    99 : (400,48,16,16),
                    100 : (416,48,16,16),
                    101 : (432,48,16,16),
                    102 : (448,48,16,16),
                    103 : (464,48,16,16),
                    104 : (0,64,16,16),
                    105 : (16,64,16,16),
                    106 : (32,64,16,16),
                    107 : (48,64,16,16),
                    108 : (64,64,16,16),
                    109 : (80,64,16,16),
                    110 : (96,64,16,16),
                    111 : (112,64,16,16),
                    112 : (128,64,16,16),
                    113 : (144,64,16,16),
                    114 : (160,64,16,16),
                    115 : (176,64,16,16),
                    116 : (192,64,16,16),
                    117 : (208,64,16,16),
                    118 : (224,64,16,16),
                    119 : (240,64,16,16),
                    120 : (256,64,16,16),
                    121 : (272,64,16,16),
                    122 : (288,64,16,16),
                    123 : (304,64,16,16),
                    124 : (320,64,16,16),
                    125 : (336,64,16,16),
                    126 : (352,64,16,16),
                    127 : (368,64,16,16),
                    128 : (384,64,16,16),
                    129 : (400,64,16,16),
                    130 : (416,64,16,16),
                    131 : (432,64,16,16),
                    132 : (448,64,16,16),
                    133 : (464,64,16,16),
                    134 : (0,80,16,16),
                    135 : (16,80,16,16),
                    136 : (32,80,16,16),
                    137 : (48,80,16,16),
                    138 : (64,80,16,16),
                    139 : (80,80,16,16),
                    140 : (96,80,16,16),
                    141 : (112,80,16,16),
                    142 : (128,80,16,16),
                    143 : (144,80,16,16),
                    144 : (160,80,16,16),
                    145 : (176,80,16,16),
                    146 : (192,80,16,16),
                    147 : (208,80,16,16),
                    148 : (224,80,16,16),
                    149 : (240,80,16,16),
                    150 : (256,80,16,16),
                    151 : (272,80,16,16),
                    152 : (288,80,16,16),
                    153 : (304,80,16,16),
                    154 : (320,80,16,16),
                    155 : (336,80,16,16),
                    156 : (352,80,16,16),
                    157 : (368,80,16,16),
                    158 : (384,80,16,16),
                    159 : (400,80,16,16),
                    160 : (416,80,16,16),}

rouge_ref ={1 : (0,0,32,32),
            2 : (32,0,32,32),
            3 : (64,0,32,32),
            4 : (96,0,32,32),
            5 : (128,0,32,32),
            6 : (160,0,32,32),
            7 : (192,0,32,32),
            8 : (224,0,32,32),
            9 : (256,0,32,32),
            10 : (288,0,32,32),
            11 : (0,32,32,32),
            12 : (32,32,32,32),
            13 : (64,32,32,32),
            14 : (96,32,32,32),
            15 : (128,32,32,32),
            16 : (160,32,32,32),
            17 : (192,32,32,32),
            18 : (224,32,32,32),
            19 : (256,32,32,32),
            20 : (288,32,32,32),
            21 : (0,64,32,32),
            22 : (32,64,32,32),
            23 : (64,64,32,32),
            24 : (96,64,32,32),
            25 : (128,64,32,32),
            26 : (160,64,32,32),
            27 : (192,64,32,32),
            28 : (224,64,32,32),
            29 : (256,64,32,32),
            30 : (288,64,32,32),
            31 : (0,96,32,32),
            32 : (32,96,32,32),
            33 : (64,96,32,32),
            34 : (96,96,32,32),
            35 : (128,96,32,32),
            36 : (160,96,32,32),
            37 : (192,96,32,32),
            38 : (224,96,32,32),
            39 : (256,96,32,32),
            40 : (288,96,32,32),
            41 : (0,128,32,32),
            42 : (32,128,32,32),
            43 : (64,128,32,32),
            44 : (96,128,32,32),
            45 : (128,128,32,32),
            46 : (160,128,32,32),
            47 : (192,128,32,32),
            48 : (224,128,32,32),
            49 : (256,128,32,32),
            50 : (288,128,32,32),
            51 : (0,160,32,32),
            52 : (32,160,32,32),
            53 : (64,160,32,32),
            54 : (96,160,32,32),
            55 : (128,160,32,32),
            56 : (160,160,32,32),
            57 : (192,160,32,32),
            58 : (224,160,32,32),
            59 : (256,160,32,32),
            60 : (288,160,32,32),
            61 : (0,192,32,32),
            62 : (32,192,32,32),
            63 : (64,192,32,32),
            64 : (96,192,32,32),
            65 : (128,192,32,32),
            66 : (160,192,32,32),
            67 : (192,192,32,32),
            68 : (224,192,32,32),
            69 : (256,192,32,32),
            70 : (288,192,32,32),
            71 : (0,224,32,32),
            72 : (32,224,32,32),
            73 : (64,224,32,32),
            74 : (96,224,32,32),
            75 : (128,224,32,32),
            76 : (160,224,32,32),
            77 : (192,224,32,32),
            78 : (224,224,32,32),
            79 : (256,224,32,32),
            80 : (288,224,32,32),
            81 : (0,256,32,32),
            82 : (32,256,32,32),
            83 : (64,256,32,32),
            84 : (96,256,32,32),
            85 : (128,256,32,32),
            86 : (160,256,32,32),
            87 : (192,256,32,32),
            88 : (224,256,32,32),
            89 : (256,256,32,32),
            90 : (288,256,32,32),
            91 : (0,288,32,32),
            92 : (32,288,32,32),
            93 : (64,288,32,32),
            94 : (96,288,32,32),
            95 : (128,288,32,32),
            96 : (160,288,32,32),
            97 : (192,288,32,32),
            98 : (224,288,32,32),
            99 : (256,288,32,32),
            100 : (288,288,32,32)}
      
skeleton_ref = {1 : (0,0,32,32),
                2 : (32,0,32,32),
                3 : (64,0,32,32),
                4 : (96,0,32,32),
                5 : (128,0,32,32),
                6 : (160,0,32,32),
                7 : (192,0,32,32),
                8 : (224,0,32,32),
                9 : (256,0,32,32),
                10 : (288,0,32,32),
                11 : (0,32,32,32),
                12 : (32,32,32,32),
                13 : (64,32,32,32),
                14 : (96,32,32,32),
                15 : (128,32,32,32),
                16 : (160,32,32,32),
                17 : (192,32,32,32),
                18 : (224,32,32,32),
                19 : (256,32,32,32),
                20 : (288,32,32,32),
                21 : (0,64,32,32),
                22 : (32,64,32,32),
                23 : (64,64,32,32),
                24 : (96,64,32,32),
                25 : (128,64,32,32),
                26 : (160,64,32,32),
                27 : (192,64,32,32),
                28 : (224,64,32,32),
                29 : (256,64,32,32),
                30 : (288,64,32,32),
                31 : (0,96,32,32),
                32 : (32,96,32,32),
                33 : (64,96,32,32),
                34 : (96,96,32,32),
                35 : (128,96,32,32),
                36 : (160,96,32,32),
                37 : (192,96,32,32),
                38 : (224,96,32,32),
                39 : (256,96,32,32),
                40 : (288,96,32,32),
                41 : (0,128,32,32),
                42 : (32,128,32,32),
                43 : (64,128,32,32),
                44 : (96,128,32,32),
                45 : (128,128,32,32),
                46 : (160,128,32,32),
                47 : (192,128,32,32),
                48 : (224,128,32,32),
                49 : (256,128,32,32),
                50 : (288,128,32,32)}