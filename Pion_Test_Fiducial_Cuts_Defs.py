# # print("Defining Pion Fiducial Cuts for Individual Sectors:")



# polygon_sec_1  = {}
# # Outer_Sector_1 = [(0, 0), (340, 200), (340, -200), (0, 0)]
# Outer_Sector_1 = [(0, 0), (357, 210), (357, -210), (0, 0)]
# polygon_sec_1["Layer_6"]  = Outer_Sector_1.copy()
# polygon_sec_1["Layer_18"] = Outer_Sector_1.copy()
# polygon_sec_1["Layer_36"] = Outer_Sector_1.copy()
# del Outer_Sector_1

# polygon_sec_1["Layer_6"].append((24,    0))
# polygon_sec_1["Layer_6"].append((24,   -6))
# polygon_sec_1["Layer_6"].append((111, -54))
# polygon_sec_1["Layer_6"].append((111,  54))
# polygon_sec_1["Layer_6"].append((24,    6))
# polygon_sec_1["Layer_6"].append((24,    0))

# polygon_sec_1["Layer_18"].append((45,     0))
# polygon_sec_1["Layer_18"].append((50,    -6))
# polygon_sec_1["Layer_18"].append((72,   -25))
# polygon_sec_1["Layer_18"].append((100,  -42))
# polygon_sec_1["Layer_18"].append((166,  -78))
# polygon_sec_1["Layer_18"].append((166,   78))
# polygon_sec_1["Layer_18"].append((150,   70))
# polygon_sec_1["Layer_18"].append((100,   44))
# polygon_sec_1["Layer_18"].append((50,    11))
# polygon_sec_1["Layer_18"].append((45,     0))

# polygon_sec_1["Layer_36"].append((85,     0))
# polygon_sec_1["Layer_36"].append((90,    -7))
# # polygon_sec_1["Layer_36"].append((100,  -10))
# polygon_sec_1["Layer_36"].append((115,  -35))
# polygon_sec_1["Layer_36"].append((135,  -49))
# polygon_sec_1["Layer_36"].append((218,  -99))
# polygon_sec_1["Layer_36"].append((265, -127)) # OG
# polygon_sec_1["Layer_36"].append((290, -140))#
# polygon_sec_1["Layer_36"].append((290,  -70))
# polygon_sec_1["Layer_36"].append((310,    0))
# polygon_sec_1["Layer_36"].append((290,   90))
# polygon_sec_1["Layer_36"].append((290,  140))#
# polygon_sec_1["Layer_36"].append((265,  130)) # OG
# polygon_sec_1["Layer_36"].append((213,  100))
# polygon_sec_1["Layer_36"].append((200,   91))
# polygon_sec_1["Layer_36"].append((160,   68))
# polygon_sec_1["Layer_36"].append((100,   25))
# polygon_sec_1["Layer_36"].append((86,     7))
# polygon_sec_1["Layer_36"].append((85,     0))


# polygon_sec_2  = {}
# # Outer_Sector_2 = [(0, 0), (340, 200), (0, 350), (0, 0)]
# Outer_Sector_2 = [(0, 0), (357, 210), (0, 455), (0, 0)]
# polygon_sec_2["Layer_6"]  = Outer_Sector_2.copy()
# polygon_sec_2["Layer_18"] = Outer_Sector_2.copy()
# polygon_sec_2["Layer_36"] = Outer_Sector_2.copy()
# del Outer_Sector_2

# polygon_sec_2["Layer_6"].append((12,   21))
# polygon_sec_2["Layer_6"].append((8,    24))
# polygon_sec_2["Layer_6"].append((10,  120))
# polygon_sec_2["Layer_6"].append((100,  69))
# polygon_sec_2["Layer_6"].append((17,   19))
# polygon_sec_2["Layer_6"].append((12,   21))

# polygon_sec_2["Layer_18"].append((22,   38))
# polygon_sec_2["Layer_18"].append((16,   50))
# polygon_sec_2["Layer_18"].append((12,   84))
# polygon_sec_2["Layer_18"].append((12,  175))
# polygon_sec_2["Layer_18"].append((22,  178))
# polygon_sec_2["Layer_18"].append((50,  168))
# polygon_sec_2["Layer_18"].append((100, 141))
# polygon_sec_2["Layer_18"].append((151, 108))
# polygon_sec_2["Layer_18"].append((151, 103))
# polygon_sec_2["Layer_18"].append((100,  73))
# polygon_sec_2["Layer_18"].append((60,   51))
# polygon_sec_2["Layer_18"].append((50,   49))
# polygon_sec_2["Layer_18"].append((28,   38))
# polygon_sec_2["Layer_18"].append((22,   38))



# polygon_sec_2["Layer_36"].append((40,   75))
# polygon_sec_2["Layer_36"].append((32,   90))
# polygon_sec_2["Layer_36"].append((28,  100))
# polygon_sec_2["Layer_36"].append((22,  130))
# polygon_sec_2["Layer_36"].append((24,  150))
# polygon_sec_2["Layer_36"].append((23,  200))
# polygon_sec_2["Layer_36"].append((22,  250))
# # polygon_sec_2["Layer_36"].append((150, 113))
# polygon_sec_2["Layer_36"].append((20,  290)) # OG
# # polygon_sec_2["Layer_36"].append((25,  290))
# # polygon_sec_2["Layer_36"].append((25,  325))#
# polygon_sec_2["Layer_36"].append((25,  323))#
# # polygon_sec_2["Layer_36"].append((100, 250))
# # polygon_sec_2["Layer_36"].append((185, 200))
# # polygon_sec_2["Layer_36"].append((200, 190))
# polygon_sec_2["Layer_36"].append((150, 270))
# polygon_sec_2["Layer_36"].append((260, 180))#
# polygon_sec_2["Layer_36"].append((240, 165)) # OG
# # polygon_sec_2["Layer_36"].append((200, 142))
# polygon_sec_2["Layer_36"].append((120,  98))
# polygon_sec_2["Layer_36"].append((110,  95))
# # polygon_sec_2["Layer_36"].append((105,  97))
# # polygon_sec_2["Layer_36"].append((100,  95))
# # polygon_sec_2["Layer_36"].append((60,   78))
# polygon_sec_2["Layer_36"].append((50,   70))

# polygon_sec_2["Layer_36"].append((40,   75))


# polygon_sec_3  = {}
# # Outer_Sector_3 = [(0, 0), (0, 350), (-340, 200), (0, 0)]
# Outer_Sector_3 = [(0, 0), (0, 455), (-357, 210), (0, 0)]
# polygon_sec_3["Layer_6"]  = Outer_Sector_3.copy()
# polygon_sec_3["Layer_18"] = Outer_Sector_3.copy()
# polygon_sec_3["Layer_36"] = Outer_Sector_3.copy()
# del Outer_Sector_3

# polygon_sec_3["Layer_6"].append((-12,   21))
# polygon_sec_3["Layer_6"].append((-17,   18))
# polygon_sec_3["Layer_6"].append((-98,   70))
# polygon_sec_3["Layer_6"].append((-11,  120))
# polygon_sec_3["Layer_6"].append((-8,    24))
# polygon_sec_3["Layer_6"].append((-12,   21))

# polygon_sec_3["Layer_18"].append((-22,    38))
# polygon_sec_3["Layer_18"].append((-30,    35))
# polygon_sec_3["Layer_18"].append((-35,    40))
# polygon_sec_3["Layer_18"].append((-50,    45))
# polygon_sec_3["Layer_18"].append((-80,    61))
# polygon_sec_3["Layer_18"].append((-150,  105))
# polygon_sec_3["Layer_18"].append((-80,   150))
# polygon_sec_3["Layer_18"].append((-14,   180))
# polygon_sec_3["Layer_18"].append((-14,    80))
# polygon_sec_3["Layer_18"].append((-17,    60))
# polygon_sec_3["Layer_18"].append((-18,    42))
# polygon_sec_3["Layer_18"].append((-22,    38))

# polygon_sec_3["Layer_36"].append((-50,    72))
# polygon_sec_3["Layer_36"].append((-54,    71))
# polygon_sec_3["Layer_36"].append((-100,   87))
# polygon_sec_3["Layer_36"].append((-120,  100))
# polygon_sec_3["Layer_36"].append((-150,  116))
# polygon_sec_3["Layer_36"].append((-200,  145))
# polygon_sec_3["Layer_36"].append((-234,  162))
# polygon_sec_3["Layer_36"].append((-240,  174))
# polygon_sec_3["Layer_36"].append((-258,  174))
# # polygon_sec_3["Layer_36"].append((-225,  168)) # OG
# polygon_sec_3["Layer_36"].append((-270,  180))#
# # polygon_sec_3["Layer_36"].append((-185,  200))
# polygon_sec_3["Layer_36"].append((-150,   255))
# # polygon_sec_3["Layer_36"].append((-100,  245))
# polygon_sec_3["Layer_36"].append((-27,   320))#
# polygon_sec_3["Layer_36"].append((-27,   285)) # OG
# polygon_sec_3["Layer_36"].append((-27,   250))
# polygon_sec_3["Layer_36"].append((-27,   200))
# polygon_sec_3["Layer_36"].append((-30,   150))
# polygon_sec_3["Layer_36"].append((-30,   110))
# polygon_sec_3["Layer_36"].append((-35,   100))
# polygon_sec_3["Layer_36"].append((-40,    80))
# polygon_sec_3["Layer_36"].append((-50,    72))


# polygon_sec_4  = {}
# # Outer_Sector_4 = [(0, 0), (-340, 200), (-340, -200), (0, 0)]
# Outer_Sector_4 = [(0, 0), (-357, 210), (-357, -210), (0, 0)]
# polygon_sec_4["Layer_6"]  = Outer_Sector_4.copy()
# polygon_sec_4["Layer_18"] = Outer_Sector_4.copy()
# polygon_sec_4["Layer_36"] = Outer_Sector_4.copy()
# del Outer_Sector_4

# polygon_sec_4["Layer_6"].append((-24,    0))
# polygon_sec_4["Layer_6"].append((-24,   -6))
# polygon_sec_4["Layer_6"].append((-110, -54))
# polygon_sec_4["Layer_6"].append((-110,  54))
# polygon_sec_4["Layer_6"].append((-24,    6))
# polygon_sec_4["Layer_6"].append((-24,    0))

# polygon_sec_4["Layer_18"].append((-40,     0))
# polygon_sec_4["Layer_18"].append((-40,    -5))
# polygon_sec_4["Layer_18"].append((-50,    -8))
# polygon_sec_4["Layer_18"].append((-61,   -18))
# polygon_sec_4["Layer_18"].append((-62,   -21))
# polygon_sec_4["Layer_18"].append((-166,  -80))
# polygon_sec_4["Layer_18"].append((-166,  -78))
# polygon_sec_4["Layer_18"].append((-172,    0))
# polygon_sec_4["Layer_18"].append((-166,   80))
# polygon_sec_4["Layer_18"].append((-150,   70))
# polygon_sec_4["Layer_18"].append((-100,   43))
# polygon_sec_4["Layer_18"].append((-70,    25))
# polygon_sec_4["Layer_18"].append((-65,    20))
# polygon_sec_4["Layer_18"].append((-50,    10))
# polygon_sec_4["Layer_18"].append((-42,     5))
# polygon_sec_4["Layer_18"].append((-40,     0))

# polygon_sec_4["Layer_36"].append((-85,     0))
# polygon_sec_4["Layer_36"].append((-86,    -7))
# polygon_sec_4["Layer_36"].append((-96,   -15))
# polygon_sec_4["Layer_36"].append((-100,  -25))
# polygon_sec_4["Layer_36"].append((-131,  -49))
# polygon_sec_4["Layer_36"].append((-150,  -61))
# polygon_sec_4["Layer_36"].append((-160,  -67))
# polygon_sec_4["Layer_36"].append((-200,  -90))
# polygon_sec_4["Layer_36"].append((-213,  -99))
# polygon_sec_4["Layer_36"].append((-265, -129)) # OG
# polygon_sec_4["Layer_36"].append((-281, -135))#
# polygon_sec_4["Layer_36"].append((-300,    0))
# polygon_sec_4["Layer_36"].append((-281,  135))#
# polygon_sec_4["Layer_36"].append((-265,  127)) # OG
# polygon_sec_4["Layer_36"].append((-218,   99))
# polygon_sec_4["Layer_36"].append((-135,   49))
# polygon_sec_4["Layer_36"].append((-115,   37))
# polygon_sec_4["Layer_36"].append((-100,   18))
# polygon_sec_4["Layer_36"].append((-90,    11))
# polygon_sec_4["Layer_36"].append((-85,     0))


# polygon_sec_5  = {}
# # Outer_Sector_5 = [(0, 0), (-340, -200), (0, -450), (0, 0)]
# Outer_Sector_5 = [(0, 0), (-357, -210), (0, -455), (0, 0)]
# polygon_sec_5["Layer_6"]  = Outer_Sector_5.copy()
# polygon_sec_5["Layer_18"] = Outer_Sector_5.copy()
# polygon_sec_5["Layer_36"] = Outer_Sector_5.copy()
# del Outer_Sector_5

# polygon_sec_5["Layer_6"].append((-14,   -20))
# polygon_sec_5["Layer_6"].append((-8,    -25))
# polygon_sec_5["Layer_6"].append((-9,    -80))
# polygon_sec_5["Layer_6"].append((-12,   -120))
# polygon_sec_5["Layer_6"].append((-15,   -130))
# polygon_sec_5["Layer_6"].append((-65,   -110))
# polygon_sec_5["Layer_6"].append((-105,  -75))
# polygon_sec_5["Layer_6"].append((-100,  -70))
# polygon_sec_5["Layer_6"].append((-17,   -18))
# polygon_sec_5["Layer_6"].append((-14,   -20))

# polygon_sec_5["Layer_18"].append((-21,   -35))
# polygon_sec_5["Layer_18"].append((-13,   -38))
# polygon_sec_5["Layer_18"].append((-16,   -45))
# polygon_sec_5["Layer_18"].append((-12,   -60))
# polygon_sec_5["Layer_18"].append((-12,  -200))
# polygon_sec_5["Layer_18"].append((-50,  -190))
# polygon_sec_5["Layer_18"].append((-100, -168))
# polygon_sec_5["Layer_18"].append((-140, -141))
# polygon_sec_5["Layer_18"].append((-160, -115))
# polygon_sec_5["Layer_18"].append((-151, -103))
# polygon_sec_5["Layer_18"].append((-100,  -73))
# polygon_sec_5["Layer_18"].append((-50,   -44))
# polygon_sec_5["Layer_18"].append((-30,   -37))
# polygon_sec_5["Layer_18"].append((-26,   -31))
# polygon_sec_5["Layer_18"].append((-21,   -35))

# polygon_sec_5["Layer_36"].append((-45,   -75))
# polygon_sec_5["Layer_36"].append((-35,   -80+4))
# polygon_sec_5["Layer_36"].append((-26,   -104))
# polygon_sec_5["Layer_36"].append((-26+2, -150))
# polygon_sec_5["Layer_36"].append((-26+2, -200))
# polygon_sec_5["Layer_36"].append((-30+4, -290))
# polygon_sec_5["Layer_36"].append((-35,   -300))#
# polygon_sec_5["Layer_36"].append((-100,  -295-4))
# polygon_sec_5["Layer_36"].append((-150,  -270))
# polygon_sec_5["Layer_36"].append((-200,  -230))
# polygon_sec_5["Layer_36"].append((-255,  -182-8))
# polygon_sec_5["Layer_36"].append((-260,  -180))#
# polygon_sec_5["Layer_36"].append((-236,  -178))
# # polygon_sec_5["Layer_36"].append((-245, -180))
# polygon_sec_5["Layer_36"].append((-235,  -165))
# polygon_sec_5["Layer_36"].append((-200,  -150+8))
# polygon_sec_5["Layer_36"].append((-150,  -120+4))
# polygon_sec_5["Layer_36"].append((-100,  -90+4))
# polygon_sec_5["Layer_36"].append((-80,   -78))
# polygon_sec_5["Layer_36"].append((-45,   -75))

# polygon_sec_6  = {}
# Outer_Sector_6 = [(0, 0), (0, -455), (357, -210), (0, 0)]
# polygon_sec_6["Layer_6"]  = Outer_Sector_6.copy()
# polygon_sec_6["Layer_18"] = Outer_Sector_6.copy()
# polygon_sec_6["Layer_36"] = Outer_Sector_6.copy()
# del Outer_Sector_6

# polygon_sec_6["Layer_6"].append((12,   -21))
# polygon_sec_6["Layer_6"].append((17,   -18))
# polygon_sec_6["Layer_6"].append((100,  -69))
# polygon_sec_6["Layer_6"].append((10,  -118))
# polygon_sec_6["Layer_6"].append((8,    -24))
# polygon_sec_6["Layer_6"].append((12,   -21))

# polygon_sec_6["Layer_18"].append((20,   -35))
# polygon_sec_6["Layer_18"].append((27,   -34))
# polygon_sec_6["Layer_18"].append((30,   -35))
# polygon_sec_6["Layer_18"].append((35,   -38))
# polygon_sec_6["Layer_18"].append((50,   -43))
# polygon_sec_6["Layer_18"].append((80,   -61))
# polygon_sec_6["Layer_18"].append((150, -101))
# polygon_sec_6["Layer_18"].append((150, -105))
# polygon_sec_6["Layer_18"].append((80,  -150))
# polygon_sec_6["Layer_18"].append((13,  -180))
# polygon_sec_6["Layer_18"].append((13,   -80))
# polygon_sec_6["Layer_18"].append((17,   -60))
# polygon_sec_6["Layer_18"].append((18,   -42))
# polygon_sec_6["Layer_18"].append((15,   -39))
# polygon_sec_6["Layer_18"].append((20,   -35))

# polygon_sec_6["Layer_36"].append((50,    -72))
# polygon_sec_6["Layer_36"].append((54,    -71))
# polygon_sec_6["Layer_36"].append((75,    -76))
# polygon_sec_6["Layer_36"].append((100,   -85))
# polygon_sec_6["Layer_36"].append((120,   -95))
# polygon_sec_6["Layer_36"].append((150,  -115))
# polygon_sec_6["Layer_36"].append((200,  -141))
# polygon_sec_6["Layer_36"].append((230,  -157))
# polygon_sec_6["Layer_36"].append((235,  -165)) # OG
# polygon_sec_6["Layer_36"].append((265,  -180))#
# # polygon_sec_6["Layer_36"].append((185,  -195))
# # polygon_sec_6["Layer_36"].append((100,  -245))
# polygon_sec_6["Layer_36"].append((150,  -270))
# polygon_sec_6["Layer_36"].append((24,   -325))#
# polygon_sec_6["Layer_36"].append((24,   -285)) # OG
# polygon_sec_6["Layer_36"].append((25,   -250))
# polygon_sec_6["Layer_36"].append((26,   -235))
# polygon_sec_6["Layer_36"].append((27,   -200))
# polygon_sec_6["Layer_36"].append((30,   -150))
# polygon_sec_6["Layer_36"].append((30,   -110))
# polygon_sec_6["Layer_36"].append((35,   -100))
# polygon_sec_6["Layer_36"].append((38,    -80))
# polygon_sec_6["Layer_36"].append((50,    -72))
    
# polygon_pip_secs = {}
# polygon_pip_secs["Sector_1"] = polygon_sec_1
# polygon_pip_secs["Sector_2"] = polygon_sec_2
# polygon_pip_secs["Sector_3"] = polygon_sec_3
# polygon_pip_secs["Sector_4"] = polygon_sec_4
# polygon_pip_secs["Sector_5"] = polygon_sec_5
# polygon_pip_secs["Sector_6"] = polygon_sec_6



    
# # print("\nDone defining polygon_pip_secs...\n")



# print("Defining Pion Fiducial Cuts for Individual Sectors:")



polygon_sec_1  = {}
# Outer_Sector_1 = [(0, 0), (340, 200), (340, -200), (0, 0)]
Outer_Sector_1 = [(0, 0), (357, 210), (357, -210), (0, 0)]
polygon_sec_1["Layer_6"]  = Outer_Sector_1.copy()
polygon_sec_1["Layer_18"] = Outer_Sector_1.copy()
polygon_sec_1["Layer_36"] = Outer_Sector_1.copy()
del Outer_Sector_1

polygon_sec_1["Layer_6"].append((24,    0))
polygon_sec_1["Layer_6"].append((24,   -6))
polygon_sec_1["Layer_6"].append((111, -54))
polygon_sec_1["Layer_6"].append((111,  54))
polygon_sec_1["Layer_6"].append((24,    6))
polygon_sec_1["Layer_6"].append((24,    0))

polygon_sec_1["Layer_18"].append((45,     0))
polygon_sec_1["Layer_18"].append((47,    -6))
polygon_sec_1["Layer_18"].append((50,    -6))
polygon_sec_1["Layer_18"].append((72,   -25))
polygon_sec_1["Layer_18"].append((100,  -42))
polygon_sec_1["Layer_18"].append((166,  -78)) # OG
polygon_sec_1["Layer_18"].append((183,  -88))#
polygon_sec_1["Layer_18"].append((185,  -50))
polygon_sec_1["Layer_18"].append((200,    0))
polygon_sec_1["Layer_18"].append((195,   50))
polygon_sec_1["Layer_18"].append((185,   80))
polygon_sec_1["Layer_18"].append((185,   80))
polygon_sec_1["Layer_18"].append((183,   88))#
polygon_sec_1["Layer_18"].append((166,   78)) # OG
polygon_sec_1["Layer_18"].append((150,   70))
polygon_sec_1["Layer_18"].append((100,   44))
polygon_sec_1["Layer_18"].append((50,    11))
polygon_sec_1["Layer_18"].append((45,     0))

# polygon_sec_1["Layer_36"].append((85,     0))
polygon_sec_1["Layer_36"].append((80,     0))
polygon_sec_1["Layer_36"].append((90,    -7))
polygon_sec_1["Layer_36"].append((115,  -35))
polygon_sec_1["Layer_36"].append((135,  -49))
polygon_sec_1["Layer_36"].append((218,  -99))
polygon_sec_1["Layer_36"].append((265, -127)) # OG
polygon_sec_1["Layer_36"].append((290, -140))#
polygon_sec_1["Layer_36"].append((290, -100))
polygon_sec_1["Layer_36"].append((295,  -70))
polygon_sec_1["Layer_36"].append((310,  -40))
polygon_sec_1["Layer_36"].append((310,    0))
polygon_sec_1["Layer_36"].append((295,   90))
polygon_sec_1["Layer_36"].append((290,  115))
polygon_sec_1["Layer_36"].append((290,  145))#
# polygon_sec_1["Layer_36"].append((290,  140))#
polygon_sec_1["Layer_36"].append((265,  130)) # OG
polygon_sec_1["Layer_36"].append((213,  100))
polygon_sec_1["Layer_36"].append((200,   91))
polygon_sec_1["Layer_36"].append((160,   68))
polygon_sec_1["Layer_36"].append((100,   25))
# polygon_sec_1["Layer_36"].append((86,     7))
polygon_sec_1["Layer_36"].append((81,     7))
polygon_sec_1["Layer_36"].append((80,     0))
# polygon_sec_1["Layer_36"].append((85,     0))


polygon_sec_2  = {}
# Outer_Sector_2 = [(0, 0), (340, 200), (0, 350), (0, 0)]
# Outer_Sector_2 = [(0, 0), (357, 210), (0, 455), (0, 0)]
Outer_Sector_2 = [(0, 0), (357, 210), (357, 425), (0, 425), (0, 0)]
polygon_sec_2["Layer_6"]  = Outer_Sector_2.copy()
polygon_sec_2["Layer_18"] = Outer_Sector_2.copy()
polygon_sec_2["Layer_36"] = Outer_Sector_2.copy()
del Outer_Sector_2

polygon_sec_2["Layer_6"].append((12,   21))
polygon_sec_2["Layer_6"].append((8,    24))
polygon_sec_2["Layer_6"].append((10,  120))
polygon_sec_2["Layer_6"].append((100,  69))
polygon_sec_2["Layer_6"].append((17,   19))
polygon_sec_2["Layer_6"].append((12,   21))

polygon_sec_2["Layer_18"].append((22,   38))
polygon_sec_2["Layer_18"].append((16,   50))
polygon_sec_2["Layer_18"].append((15,   84))
polygon_sec_2["Layer_18"].append((15,  175)) # OG
polygon_sec_2["Layer_18"].append((18,  185))#
# polygon_sec_2["Layer_18"].append((22,  200))#
# polygon_sec_2["Layer_18"].append((35,  200))
# polygon_sec_2["Layer_18"].append((100, 185))
# polygon_sec_2["Layer_18"].append((120, 170))
polygon_sec_2["Layer_18"].append((120, 150))
polygon_sec_2["Layer_18"].append((165, 115))#
polygon_sec_2["Layer_18"].append((151, 103)) # OG
polygon_sec_2["Layer_18"].append((100,  73))
polygon_sec_2["Layer_18"].append((60,   51))
polygon_sec_2["Layer_18"].append((50,   49))
polygon_sec_2["Layer_18"].append((28,   38))
polygon_sec_2["Layer_18"].append((22,   38))

# polygon_sec_2["Layer_18"].append((22,   38))
# polygon_sec_2["Layer_18"].append((16,   50))
# polygon_sec_2["Layer_18"].append((12,   84))
# polygon_sec_2["Layer_18"].append((12,  175)) # OG
# polygon_sec_2["Layer_18"].append((22,  178))
# polygon_sec_2["Layer_18"].append((50,  168))
# polygon_sec_2["Layer_18"].append((100, 141))
# polygon_sec_2["Layer_18"].append((151, 108))
# polygon_sec_2["Layer_18"].append((151, 103)) # OG
# polygon_sec_2["Layer_18"].append((100,  73))
# polygon_sec_2["Layer_18"].append((60,   51))
# polygon_sec_2["Layer_18"].append((50,   49))
# polygon_sec_2["Layer_18"].append((28,   38))
# polygon_sec_2["Layer_18"].append((22,   38))


polygon_sec_2["Layer_36"].append((40,   70))
polygon_sec_2["Layer_36"].append((32,   90))
polygon_sec_2["Layer_36"].append((28,  100))
polygon_sec_2["Layer_36"].append((22,  130))
# polygon_sec_2["Layer_36"].append((24,  150))
polygon_sec_2["Layer_36"].append((23,  200))
polygon_sec_2["Layer_36"].append((22,  250))
polygon_sec_2["Layer_36"].append((20,  290)) # OG
polygon_sec_2["Layer_36"].append((25,  323))#
polygon_sec_2["Layer_36"].append((150, 275))
polygon_sec_2["Layer_36"].append((175, 250))
# polygon_sec_2["Layer_36"].append((260, 180))#
polygon_sec_2["Layer_36"].append((250, 190))
polygon_sec_2["Layer_36"].append((264, 190))
polygon_sec_2["Layer_36"].append((264, 180))#
polygon_sec_2["Layer_36"].append((240, 165)) # OG
polygon_sec_2["Layer_36"].append((120,  98))
polygon_sec_2["Layer_36"].append((110,  95))
polygon_sec_2["Layer_36"].append((50,   70))
polygon_sec_2["Layer_36"].append((40,   70))


polygon_sec_3  = {}
# Outer_Sector_3 = [(0, 0), (0, 350), (-340, 200), (0, 0)]
# Outer_Sector_3 = [(0, 0), (0, 455), (-357, 210), (0, 0)]
Outer_Sector_3 = [(0, 0), (0, 425), (-357, 425), (-357, 210), (0, 0)]
polygon_sec_3["Layer_6"]  = Outer_Sector_3.copy()
polygon_sec_3["Layer_18"] = Outer_Sector_3.copy()
polygon_sec_3["Layer_36"] = Outer_Sector_3.copy()
del Outer_Sector_3

polygon_sec_3["Layer_6"].append((-12,   21))
polygon_sec_3["Layer_6"].append((-17,   18))
polygon_sec_3["Layer_6"].append((-98,   70))
polygon_sec_3["Layer_6"].append((-11,  120))
polygon_sec_3["Layer_6"].append((-8,    24))
polygon_sec_3["Layer_6"].append((-12,   21))

polygon_sec_3["Layer_18"].append((-22,    38))
polygon_sec_3["Layer_18"].append((-30,    35))
polygon_sec_3["Layer_18"].append((-35,    40))
polygon_sec_3["Layer_18"].append((-50,    45))
polygon_sec_3["Layer_18"].append((-80,    61))
polygon_sec_3["Layer_18"].append((-150,  105)) # OG
# polygon_sec_3["Layer_18"].append((-150,  110))#
# polygon_sec_3["Layer_18"].append((-80,   150))
polygon_sec_3["Layer_18"].append((-100,  150))
polygon_sec_3["Layer_18"].append((-20,   182))#
polygon_sec_3["Layer_18"].append((-14,   180)) # OG
polygon_sec_3["Layer_18"].append((-14,    80))
polygon_sec_3["Layer_18"].append((-17,    60))
polygon_sec_3["Layer_18"].append((-18,    42))
polygon_sec_3["Layer_18"].append((-22,    38))

polygon_sec_3["Layer_36"].append((-50,    65))
polygon_sec_3["Layer_36"].append((-54,    71))
polygon_sec_3["Layer_36"].append((-100,   87))
polygon_sec_3["Layer_36"].append((-120,  100))
polygon_sec_3["Layer_36"].append((-150,  116))
polygon_sec_3["Layer_36"].append((-200,  145))
polygon_sec_3["Layer_36"].append((-234,  162))
polygon_sec_3["Layer_36"].append((-240,  174))
polygon_sec_3["Layer_36"].append((-258,  174))
# polygon_sec_3["Layer_36"].append((-225,  168)) # OG
polygon_sec_3["Layer_36"].append((-270,  180))#
polygon_sec_3["Layer_36"].append((-150,  255))
polygon_sec_3["Layer_36"].append((-50,   315))
polygon_sec_3["Layer_36"].append((-27,   320))#
polygon_sec_3["Layer_36"].append((-27,   285)) # OG
polygon_sec_3["Layer_36"].append((-27,   250))
polygon_sec_3["Layer_36"].append((-27,   200))
polygon_sec_3["Layer_36"].append((-30,   150))
polygon_sec_3["Layer_36"].append((-30,   110))
polygon_sec_3["Layer_36"].append((-35,   100))
polygon_sec_3["Layer_36"].append((-38,    80))
polygon_sec_3["Layer_36"].append((-50,    65))


polygon_sec_4  = {}
# Outer_Sector_4 = [(0, 0), (-340, 200), (-340, -200), (0, 0)]
Outer_Sector_4 = [(0, 0), (-357, 210), (-357, -210), (0, 0)]
polygon_sec_4["Layer_6"]  = Outer_Sector_4.copy()
polygon_sec_4["Layer_18"] = Outer_Sector_4.copy()
polygon_sec_4["Layer_36"] = Outer_Sector_4.copy()
del Outer_Sector_4

polygon_sec_4["Layer_6"].append((-24,    0))
polygon_sec_4["Layer_6"].append((-24,   -6))
polygon_sec_4["Layer_6"].append((-110, -54))
polygon_sec_4["Layer_6"].append((-110,  54))
polygon_sec_4["Layer_6"].append((-24,    6))
polygon_sec_4["Layer_6"].append((-24,    0))

polygon_sec_4["Layer_18"].append((-40,     0))
polygon_sec_4["Layer_18"].append((-40,    -5))
polygon_sec_4["Layer_18"].append((-50,    -8))
polygon_sec_4["Layer_18"].append((-61,   -18))
polygon_sec_4["Layer_18"].append((-62,   -21))
polygon_sec_4["Layer_18"].append((-166,  -80))
polygon_sec_4["Layer_18"].append((-166,  -78))
polygon_sec_4["Layer_18"].append((-172,    0))
polygon_sec_4["Layer_18"].append((-166,   80))
polygon_sec_4["Layer_18"].append((-150,   70))
polygon_sec_4["Layer_18"].append((-100,   43))
polygon_sec_4["Layer_18"].append((-70,    25))
polygon_sec_4["Layer_18"].append((-65,    20))
polygon_sec_4["Layer_18"].append((-50,    10))
polygon_sec_4["Layer_18"].append((-42,     5))
polygon_sec_4["Layer_18"].append((-40,     0))

polygon_sec_4["Layer_36"].append((-85,     0))
polygon_sec_4["Layer_36"].append((-86,    -7))
# polygon_sec_4["Layer_36"].append((-96,   -15))
polygon_sec_4["Layer_36"].append((-100,  -25))
polygon_sec_4["Layer_36"].append((-131,  -49))
polygon_sec_4["Layer_36"].append((-150,  -61))
polygon_sec_4["Layer_36"].append((-160,  -67))
polygon_sec_4["Layer_36"].append((-200,  -90))
polygon_sec_4["Layer_36"].append((-213,  -99))
polygon_sec_4["Layer_36"].append((-265, -129)) # OG
polygon_sec_4["Layer_36"].append((-281, -140))#
polygon_sec_4["Layer_36"].append((-295, -100))
polygon_sec_4["Layer_36"].append((-298,    0))
polygon_sec_4["Layer_36"].append((-295,  100))
polygon_sec_4["Layer_36"].append((-285,  110))
polygon_sec_4["Layer_36"].append((-281,  135))#
polygon_sec_4["Layer_36"].append((-265,  127)) # OG
polygon_sec_4["Layer_36"].append((-218,   99))
polygon_sec_4["Layer_36"].append((-135,   49))
polygon_sec_4["Layer_36"].append((-115,   37))
polygon_sec_4["Layer_36"].append((-100,   18))
polygon_sec_4["Layer_36"].append((-90,    11))
polygon_sec_4["Layer_36"].append((-85,     0))


polygon_sec_5  = {}
# Outer_Sector_5 = [(0, 0), (-340, -200), (0, -450), (0, 0)]
# Outer_Sector_5 = [(0, 0), (-357, -210), (0, -455), (0, 0)]
Outer_Sector_5 = [(0, 0), (-357, -210), (-357, -425), (0, -425), (0, 0)]
polygon_sec_5["Layer_6"]  = Outer_Sector_5.copy()
polygon_sec_5["Layer_18"] = Outer_Sector_5.copy()
polygon_sec_5["Layer_36"] = Outer_Sector_5.copy()
del Outer_Sector_5

polygon_sec_5["Layer_6"].append((-14,   -20))
polygon_sec_5["Layer_6"].append((-8,    -25))
polygon_sec_5["Layer_6"].append((-9,    -80))
polygon_sec_5["Layer_6"].append((-12,   -120))
polygon_sec_5["Layer_6"].append((-15,   -130))
polygon_sec_5["Layer_6"].append((-65,   -110))
polygon_sec_5["Layer_6"].append((-105,  -75))
polygon_sec_5["Layer_6"].append((-100,  -70))
polygon_sec_5["Layer_6"].append((-17,   -18))
polygon_sec_5["Layer_6"].append((-14,   -20))

polygon_sec_5["Layer_18"].append((-21,   -35))
polygon_sec_5["Layer_18"].append((-13,   -38))
polygon_sec_5["Layer_18"].append((-16,   -45))
polygon_sec_5["Layer_18"].append((-12,   -60))
polygon_sec_5["Layer_18"].append((-12,  -200))
polygon_sec_5["Layer_18"].append((-50,  -190))
polygon_sec_5["Layer_18"].append((-100, -168))
polygon_sec_5["Layer_18"].append((-140, -141))
polygon_sec_5["Layer_18"].append((-160, -115))
polygon_sec_5["Layer_18"].append((-151, -103))
polygon_sec_5["Layer_18"].append((-100,  -73))
polygon_sec_5["Layer_18"].append((-50,   -44))
polygon_sec_5["Layer_18"].append((-30,   -37))
polygon_sec_5["Layer_18"].append((-26,   -31))
polygon_sec_5["Layer_18"].append((-21,   -35))

polygon_sec_5["Layer_36"].append((-45,   -75))
# polygon_sec_5["Layer_36"].append((-35,   -76))
polygon_sec_5["Layer_36"].append((-40,   -76))
polygon_sec_5["Layer_36"].append((-26,   -104))
polygon_sec_5["Layer_36"].append((-24,   -150))
polygon_sec_5["Layer_36"].append((-22,   -200))
polygon_sec_5["Layer_36"].append((-22,   -250))
polygon_sec_5["Layer_36"].append((-26,   -290))
polygon_sec_5["Layer_36"].append((-35,   -300))#
polygon_sec_5["Layer_36"].append((-50,   -310))
polygon_sec_5["Layer_36"].append((-70,   -300))
polygon_sec_5["Layer_36"].append((-100,  -299))
polygon_sec_5["Layer_36"].append((-150,  -270))
polygon_sec_5["Layer_36"].append((-200,  -230))
polygon_sec_5["Layer_36"].append((-255,  -182-8))
polygon_sec_5["Layer_36"].append((-260,  -180))#
polygon_sec_5["Layer_36"].append((-236,  -178))
polygon_sec_5["Layer_36"].append((-235,  -165))
polygon_sec_5["Layer_36"].append((-200,  -150+8))
polygon_sec_5["Layer_36"].append((-150,  -120+4))
polygon_sec_5["Layer_36"].append((-100,  -90+4))
polygon_sec_5["Layer_36"].append((-80,   -78))
polygon_sec_5["Layer_36"].append((-45,   -75))

polygon_sec_6  = {}
# Outer_Sector_6 = [(0, 0), (0, -455), (357, -210), (0, 0)]
Outer_Sector_6 = [(0, 0), (0, -425), (357, -425), (357, -210), (0, 0)]
polygon_sec_6["Layer_6"]  = Outer_Sector_6.copy()
polygon_sec_6["Layer_18"] = Outer_Sector_6.copy()
polygon_sec_6["Layer_36"] = Outer_Sector_6.copy()
del Outer_Sector_6

polygon_sec_6["Layer_6"].append((12,   -21))
polygon_sec_6["Layer_6"].append((17,   -18))
polygon_sec_6["Layer_6"].append((100,  -69))
polygon_sec_6["Layer_6"].append((10,  -118))
polygon_sec_6["Layer_6"].append((8,    -24))
polygon_sec_6["Layer_6"].append((12,   -21))

polygon_sec_6["Layer_18"].append((20,   -35))
polygon_sec_6["Layer_18"].append((27,   -34))
polygon_sec_6["Layer_18"].append((30,   -35))
polygon_sec_6["Layer_18"].append((35,   -38))
polygon_sec_6["Layer_18"].append((50,   -43))
polygon_sec_6["Layer_18"].append((80,   -61))
polygon_sec_6["Layer_18"].append((172, -115))#
polygon_sec_6["Layer_18"].append((150, -135+10))
polygon_sec_6["Layer_18"].append((140, -150+10))
polygon_sec_6["Layer_18"].append((100, -180+10))
polygon_sec_6["Layer_18"].append((50,  -200+10))
polygon_sec_6["Layer_18"].append((13,  -200))#
polygon_sec_6["Layer_18"].append((13,   -80))
polygon_sec_6["Layer_18"].append((17,   -60))
polygon_sec_6["Layer_18"].append((18,   -42))
polygon_sec_6["Layer_18"].append((15,   -39))
polygon_sec_6["Layer_18"].append((20,   -35))

# polygon_sec_6["Layer_18"].append((20,   -35))
# polygon_sec_6["Layer_18"].append((27,   -34))
# polygon_sec_6["Layer_18"].append((30,   -35))
# polygon_sec_6["Layer_18"].append((35,   -38))
# polygon_sec_6["Layer_18"].append((50,   -43))
# polygon_sec_6["Layer_18"].append((80,   -61))
# polygon_sec_6["Layer_18"].append((150, -101))
# polygon_sec_6["Layer_18"].append((150, -105))
# polygon_sec_6["Layer_18"].append((80,  -150))
# polygon_sec_6["Layer_18"].append((13,  -180))
# polygon_sec_6["Layer_18"].append((13,   -80))
# polygon_sec_6["Layer_18"].append((17,   -60))
# polygon_sec_6["Layer_18"].append((18,   -42))
# polygon_sec_6["Layer_18"].append((15,   -39))
# polygon_sec_6["Layer_18"].append((20,   -35))


# polygon_sec_6["Layer_36"].append((50,    -65))
polygon_sec_6["Layer_36"].append((50,    -73))
# polygon_sec_6["Layer_36"].append((100,   -200))
polygon_sec_6["Layer_36"].append((54,    -73))
polygon_sec_6["Layer_36"].append((75,    -76))
polygon_sec_6["Layer_36"].append((100,   -85))
polygon_sec_6["Layer_36"].append((120,   -95))
polygon_sec_6["Layer_36"].append((150,  -115))
polygon_sec_6["Layer_36"].append((200,  -141))
polygon_sec_6["Layer_36"].append((230,  -157))
# polygon_sec_6["Layer_36"].append((235,  -165)) # OG
polygon_sec_6["Layer_36"].append((265,  -175))#
polygon_sec_6["Layer_36"].append((265,  -180))
polygon_sec_6["Layer_36"].append((175,  -250))
# polygon_sec_6["Layer_36"].append((150,  -275))
polygon_sec_6["Layer_36"].append((150,  -270))
# polygon_sec_6["Layer_36"].append((50,   -315))
polygon_sec_6["Layer_36"].append((40,   -315))
polygon_sec_6["Layer_36"].append((35,   -315))
# polygon_sec_6["Layer_36"].append((24,   -325))
# polygon_sec_6["Layer_36"].append((22,   -325))#
polygon_sec_6["Layer_36"].append((25,   -315))#
polygon_sec_6["Layer_36"].append((25,   -285))
polygon_sec_6["Layer_36"].append((25,   -250))
polygon_sec_6["Layer_36"].append((26,   -235))
polygon_sec_6["Layer_36"].append((25,   -200))
polygon_sec_6["Layer_36"].append((27,   -150))
polygon_sec_6["Layer_36"].append((30,   -120))
polygon_sec_6["Layer_36"].append((30,   -110))
polygon_sec_6["Layer_36"].append((35,   -100))
polygon_sec_6["Layer_36"].append((38,    -80))
# polygon_sec_6["Layer_36"].append((100,   -200))
# polygon_sec_6["Layer_36"].append((50,    -65))
polygon_sec_6["Layer_36"].append((50,    -73))
    
polygon_pip_secs = {}
polygon_pip_secs["Sector_1"] = polygon_sec_1
polygon_pip_secs["Sector_2"] = polygon_sec_2
polygon_pip_secs["Sector_3"] = polygon_sec_3
polygon_pip_secs["Sector_4"] = polygon_sec_4
polygon_pip_secs["Sector_5"] = polygon_sec_5
polygon_pip_secs["Sector_6"] = polygon_sec_6



    
# print("\nDone defining polygon_pip_secs...\n")