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

# polygon_sec_1["Layer_6"].append((24,    0))
# polygon_sec_1["Layer_6"].append((24,   -6))
# polygon_sec_1["Layer_6"].append((111, -54))
# polygon_sec_1["Layer_6"].append((111,  54))
# polygon_sec_1["Layer_6"].append((24,    6))
# polygon_sec_1["Layer_6"].append((24,    0))

polygon_sec_1["Layer_6"].append((24,    0))
polygon_sec_1["Layer_6"].append((24,   -6))
polygon_sec_1["Layer_6"].append((111, -54)) # OG
polygon_sec_1["Layer_6"].append((118, -50))#
polygon_sec_1["Layer_6"].append((122,   0))
polygon_sec_1["Layer_6"].append((120,  20))
polygon_sec_1["Layer_6"].append((111,  54)) # OG
polygon_sec_1["Layer_6"].append((24,    6))
polygon_sec_1["Layer_6"].append((24,    0))

# polygon_sec_1["Layer_18"].append((45,     0))
# polygon_sec_1["Layer_18"].append((47,    -6))
# polygon_sec_1["Layer_18"].append((50,    -6))
# polygon_sec_1["Layer_18"].append((72,   -25))
# polygon_sec_1["Layer_18"].append((100,  -42))
# polygon_sec_1["Layer_18"].append((166,  -78)) # OG
# polygon_sec_1["Layer_18"].append((183,  -88))#
# polygon_sec_1["Layer_18"].append((185,  -50))
# polygon_sec_1["Layer_18"].append((200,    0))
# polygon_sec_1["Layer_18"].append((195,   50))
# polygon_sec_1["Layer_18"].append((185,   80))
# polygon_sec_1["Layer_18"].append((185,   80))
# polygon_sec_1["Layer_18"].append((183,   88))#
# polygon_sec_1["Layer_18"].append((166,   78)) # OG
# polygon_sec_1["Layer_18"].append((150,   70))
# polygon_sec_1["Layer_18"].append((100,   44))
# polygon_sec_1["Layer_18"].append((50,    11))
# polygon_sec_1["Layer_18"].append((45,     0))
polygon_sec_1["Layer_18"].append((45,     0))
polygon_sec_1["Layer_18"].append((47,    -6))
polygon_sec_1["Layer_18"].append((50,    -6))
polygon_sec_1["Layer_18"].append((72,   -25))
polygon_sec_1["Layer_18"].append((100,  -42))
polygon_sec_1["Layer_18"].append((166,  -78)) # OG
polygon_sec_1["Layer_18"].append((183,  -88))#
polygon_sec_1["Layer_18"].append((185,  -50))
polygon_sec_1["Layer_18"].append((185,    0))
polygon_sec_1["Layer_18"].append((180,   80))#
polygon_sec_1["Layer_18"].append((166,   78)) # OG
polygon_sec_1["Layer_18"].append((150,   70))
polygon_sec_1["Layer_18"].append((100,   44))
polygon_sec_1["Layer_18"].append((50,    11))
polygon_sec_1["Layer_18"].append((45,     0))

# # polygon_sec_1["Layer_36"].append((85,     0))
# polygon_sec_1["Layer_36"].append((80,     0))
# polygon_sec_1["Layer_36"].append((90,    -7))
# polygon_sec_1["Layer_36"].append((115,  -35))
# polygon_sec_1["Layer_36"].append((135,  -49))
# polygon_sec_1["Layer_36"].append((218,  -99))
# polygon_sec_1["Layer_36"].append((265, -127)) # OG
# polygon_sec_1["Layer_36"].append((290, -140))#
# polygon_sec_1["Layer_36"].append((290, -100))
# polygon_sec_1["Layer_36"].append((295,  -70))
# polygon_sec_1["Layer_36"].append((310,  -40))
# polygon_sec_1["Layer_36"].append((310,    0))
# polygon_sec_1["Layer_36"].append((295,   90))
# polygon_sec_1["Layer_36"].append((290,  115))
# polygon_sec_1["Layer_36"].append((290,  145))#
# # polygon_sec_1["Layer_36"].append((290,  140))#
# polygon_sec_1["Layer_36"].append((265,  130)) # OG
# polygon_sec_1["Layer_36"].append((213,  100))
# polygon_sec_1["Layer_36"].append((200,   91))
# polygon_sec_1["Layer_36"].append((160,   68))
# polygon_sec_1["Layer_36"].append((100,   25))
# # polygon_sec_1["Layer_36"].append((86,     7))
# polygon_sec_1["Layer_36"].append((81,     7))
# polygon_sec_1["Layer_36"].append((80,     0))
# # polygon_sec_1["Layer_36"].append((85,     0))

polygon_sec_1["Layer_36"].append((80,     0))
polygon_sec_1["Layer_36"].append((90,    -7))
polygon_sec_1["Layer_36"].append((115,  -35))
polygon_sec_1["Layer_36"].append((135,  -47))
polygon_sec_1["Layer_36"].append((218,  -97))
polygon_sec_1["Layer_36"].append((265, -125)) # OG
polygon_sec_1["Layer_36"].append((285, -138))#
polygon_sec_1["Layer_36"].append((285,  130))#
# polygon_sec_1["Layer_36"].append((288,  143))#
polygon_sec_1["Layer_36"].append((265,  130))
# polygon_sec_1["Layer_36"].append((265,  128)) # OG
polygon_sec_1["Layer_36"].append((213,   98))
polygon_sec_1["Layer_36"].append((200,   90))
polygon_sec_1["Layer_36"].append((160,   66))
polygon_sec_1["Layer_36"].append((100,   24))
polygon_sec_1["Layer_36"].append((81,     6))
polygon_sec_1["Layer_36"].append((80,     0))


polygon_sec_2  = {}
# Outer_Sector_2 = [(0, 0), (340, 200), (0, 350), (0, 0)]
# Outer_Sector_2 = [(0, 0), (357, 210), (0, 455), (0, 0)]
Outer_Sector_2 = [(0, 0), (357, 210), (357, 425), (0, 425), (0, 0)]
polygon_sec_2["Layer_6"]  = Outer_Sector_2.copy()
polygon_sec_2["Layer_18"] = Outer_Sector_2.copy()
polygon_sec_2["Layer_36"] = Outer_Sector_2.copy()
del Outer_Sector_2

# polygon_sec_2["Layer_6"].append((12,   21))
# polygon_sec_2["Layer_6"].append((8,    24))
# polygon_sec_2["Layer_6"].append((10,  120))
# polygon_sec_2["Layer_6"].append((100,  69))
# polygon_sec_2["Layer_6"].append((17,   19))
# polygon_sec_2["Layer_6"].append((12,   21))
polygon_sec_2["Layer_6"].append((12,   21))
polygon_sec_2["Layer_6"].append((8,    24))
polygon_sec_2["Layer_6"].append((10,  120)) # OG
polygon_sec_2["Layer_6"].append((10,  126))#
polygon_sec_2["Layer_6"].append((50,  110))
polygon_sec_2["Layer_6"].append((75,  100))
polygon_sec_2["Layer_6"].append((100,  75))#
polygon_sec_2["Layer_6"].append((100,  69)) # OG
polygon_sec_2["Layer_6"].append((17,   19))
polygon_sec_2["Layer_6"].append((12,   21))

# polygon_sec_2["Layer_18"].append((22,   38))
# polygon_sec_2["Layer_18"].append((16,   50))
# polygon_sec_2["Layer_18"].append((15,   84))
# polygon_sec_2["Layer_18"].append((15,  175)) # OG
# polygon_sec_2["Layer_18"].append((18,  185))#
# # polygon_sec_2["Layer_18"].append((22,  200))#
# # polygon_sec_2["Layer_18"].append((35,  200))
# # polygon_sec_2["Layer_18"].append((100, 185))
# # polygon_sec_2["Layer_18"].append((120, 170))
# polygon_sec_2["Layer_18"].append((120, 150))
# polygon_sec_2["Layer_18"].append((165, 115))#
# polygon_sec_2["Layer_18"].append((151, 103)) # OG
# polygon_sec_2["Layer_18"].append((100,  73))
# polygon_sec_2["Layer_18"].append((60,   51))
# polygon_sec_2["Layer_18"].append((50,   49))
# polygon_sec_2["Layer_18"].append((28,   38))
# polygon_sec_2["Layer_18"].append((22,   38))
polygon_sec_2["Layer_18"].append((22,   38))
polygon_sec_2["Layer_18"].append((16,   50))
polygon_sec_2["Layer_18"].append((15,   84))
polygon_sec_2["Layer_18"].append((15,  175)) # OG
polygon_sec_2["Layer_18"].append((18,  190))#
polygon_sec_2["Layer_18"].append((120, 150))
polygon_sec_2["Layer_18"].append((155, 120))
polygon_sec_2["Layer_18"].append((155, 110))#
polygon_sec_2["Layer_18"].append((150, 103)) # OG
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


# polygon_sec_2["Layer_36"].append((40,   70))
# polygon_sec_2["Layer_36"].append((32,   90))
# polygon_sec_2["Layer_36"].append((28,  100))
# polygon_sec_2["Layer_36"].append((22,  130))
# # polygon_sec_2["Layer_36"].append((24,  150))
# polygon_sec_2["Layer_36"].append((23,  200))
# polygon_sec_2["Layer_36"].append((22,  250))
# polygon_sec_2["Layer_36"].append((20,  290)) # OG
# polygon_sec_2["Layer_36"].append((25,  323))#
# polygon_sec_2["Layer_36"].append((150, 275))
# polygon_sec_2["Layer_36"].append((175, 250))
# # polygon_sec_2["Layer_36"].append((260, 180))#
# polygon_sec_2["Layer_36"].append((250, 190))
# polygon_sec_2["Layer_36"].append((264, 190))
# polygon_sec_2["Layer_36"].append((264, 180))#
# polygon_sec_2["Layer_36"].append((240, 165)) # OG
# polygon_sec_2["Layer_36"].append((120,  98))
# polygon_sec_2["Layer_36"].append((110,  95))
# polygon_sec_2["Layer_36"].append((50,   70))
# polygon_sec_2["Layer_36"].append((40,   70))

polygon_sec_2["Layer_36"].append((40,   70))
polygon_sec_2["Layer_36"].append((32,   90))
polygon_sec_2["Layer_36"].append((28,  100))
polygon_sec_2["Layer_36"].append((23,  130))
polygon_sec_2["Layer_36"].append((23,  310))#
polygon_sec_2["Layer_36"].append((250, 190))
polygon_sec_2["Layer_36"].append((255, 180))#
polygon_sec_2["Layer_36"].append((238, 167)) # OG
polygon_sec_2["Layer_36"].append((118, 100))
polygon_sec_2["Layer_36"].append((108,  97))
polygon_sec_2["Layer_36"].append((48,   72))
polygon_sec_2["Layer_36"].append((40,   70))


polygon_sec_3  = {}
# Outer_Sector_3 = [(0, 0), (0, 350), (-340, 200), (0, 0)]
# Outer_Sector_3 = [(0, 0), (0, 455), (-357, 210), (0, 0)]
Outer_Sector_3 = [(0, 0), (0, 425), (-357, 425), (-357, 210), (0, 0)]
polygon_sec_3["Layer_6"]  = Outer_Sector_3.copy()
polygon_sec_3["Layer_18"] = Outer_Sector_3.copy()
polygon_sec_3["Layer_36"] = Outer_Sector_3.copy()
del Outer_Sector_3

# polygon_sec_3["Layer_6"].append((-12,   21))
# polygon_sec_3["Layer_6"].append((-17,   18))
# polygon_sec_3["Layer_6"].append((-98,   70))
# polygon_sec_3["Layer_6"].append((-11,  120))
# polygon_sec_3["Layer_6"].append((-8,    24))
# polygon_sec_3["Layer_6"].append((-12,   21))
polygon_sec_3["Layer_6"].append((-12,   21))
polygon_sec_3["Layer_6"].append((-17,   18))
polygon_sec_3["Layer_6"].append((-98,   70)) # OG
polygon_sec_3["Layer_6"].append((-100,  75))#
polygon_sec_3["Layer_6"].append((-78,  100))
polygon_sec_3["Layer_6"].append((-50,  112))
polygon_sec_3["Layer_6"].append((-15,  125))#
polygon_sec_3["Layer_6"].append((-11,  120)) # OG
polygon_sec_3["Layer_6"].append((-8,    24))
polygon_sec_3["Layer_6"].append((-12,   21))

# polygon_sec_3["Layer_18"].append((-22,    38))
# polygon_sec_3["Layer_18"].append((-30,    35))
# polygon_sec_3["Layer_18"].append((-35,    40))
# polygon_sec_3["Layer_18"].append((-50,    45))
# polygon_sec_3["Layer_18"].append((-80,    61))
# polygon_sec_3["Layer_18"].append((-150,  105)) # OG
# # polygon_sec_3["Layer_18"].append((-150,  110))#
# # polygon_sec_3["Layer_18"].append((-80,   150))
# polygon_sec_3["Layer_18"].append((-100,  150))
# polygon_sec_3["Layer_18"].append((-20,   182))#
# polygon_sec_3["Layer_18"].append((-14,   180)) # OG
# polygon_sec_3["Layer_18"].append((-14,    80))
# polygon_sec_3["Layer_18"].append((-17,    60))
# polygon_sec_3["Layer_18"].append((-18,    42))
# polygon_sec_3["Layer_18"].append((-22,    38))
polygon_sec_3["Layer_18"].append((-22,    38))
polygon_sec_3["Layer_18"].append((-30,    35))
polygon_sec_3["Layer_18"].append((-35,    40))
polygon_sec_3["Layer_18"].append((-50,    45))
polygon_sec_3["Layer_18"].append((-80,    61))
polygon_sec_3["Layer_18"].append((-150,  105)) # OG
polygon_sec_3["Layer_18"].append((-150,  120))#
polygon_sec_3["Layer_18"].append((-100,  160))
polygon_sec_3["Layer_18"].append((-20,   190))#
polygon_sec_3["Layer_18"].append((-15,   180)) # OG
polygon_sec_3["Layer_18"].append((-15,    80))
polygon_sec_3["Layer_18"].append((-17,    60))
polygon_sec_3["Layer_18"].append((-18,    42))
polygon_sec_3["Layer_18"].append((-22,    38))

# polygon_sec_3["Layer_36"].append((-50,    65))
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
# polygon_sec_3["Layer_36"].append((-150,  255))
# polygon_sec_3["Layer_36"].append((-50,   315))
# polygon_sec_3["Layer_36"].append((-27,   320))#
# polygon_sec_3["Layer_36"].append((-27,   285)) # OG
# polygon_sec_3["Layer_36"].append((-27,   250))
# polygon_sec_3["Layer_36"].append((-27,   200))
# polygon_sec_3["Layer_36"].append((-30,   150))
# polygon_sec_3["Layer_36"].append((-30,   110))
# polygon_sec_3["Layer_36"].append((-35,   100))
# polygon_sec_3["Layer_36"].append((-38,    80))
# polygon_sec_3["Layer_36"].append((-50,    65))

polygon_sec_3["Layer_36"].append((-50,    65))
polygon_sec_3["Layer_36"].append((-54,    71))
polygon_sec_3["Layer_36"].append((-100,   87))
polygon_sec_3["Layer_36"].append((-120,  100))
polygon_sec_3["Layer_36"].append((-150,  116))
polygon_sec_3["Layer_36"].append((-200,  145))
polygon_sec_3["Layer_36"].append((-234,  162))
polygon_sec_3["Layer_36"].append((-250,  180))#
# polygon_sec_3["Layer_36"].append((-240,  174))
# polygon_sec_3["Layer_36"].append((-258,  174))
# polygon_sec_3["Layer_36"].append((-270,  180))#
polygon_sec_3["Layer_36"].append((-150,  250))
polygon_sec_3["Layer_36"].append((-50,   295))
polygon_sec_3["Layer_36"].append((-30,   300))#
polygon_sec_3["Layer_36"].append((-30,   285)) # OG
polygon_sec_3["Layer_36"].append((-30,   250))
polygon_sec_3["Layer_36"].append((-30,   200))
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

# polygon_sec_4["Layer_6"].append((-24,    0))
# polygon_sec_4["Layer_6"].append((-24,   -6))
# polygon_sec_4["Layer_6"].append((-110, -54))
# polygon_sec_4["Layer_6"].append((-110,  54))
# polygon_sec_4["Layer_6"].append((-24,    6))
# polygon_sec_4["Layer_6"].append((-24,    0))
polygon_sec_4["Layer_6"].append((-24,    0))
polygon_sec_4["Layer_6"].append((-24,   -6))
polygon_sec_4["Layer_6"].append((-110, -54)) # OG
polygon_sec_4["Layer_6"].append((-120, -54))#
polygon_sec_4["Layer_6"].append((-125,   0))
polygon_sec_4["Layer_6"].append((-120,  58))#
polygon_sec_4["Layer_6"].append((-110,  54)) # OG
polygon_sec_4["Layer_6"].append((-24,    6))
polygon_sec_4["Layer_6"].append((-24,    0))


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
polygon_sec_4["Layer_18"].append((-40,     0))
polygon_sec_4["Layer_18"].append((-40,    -5))
polygon_sec_4["Layer_18"].append((-50,    -8))
polygon_sec_4["Layer_18"].append((-61,   -18))
polygon_sec_4["Layer_18"].append((-62,   -21))
polygon_sec_4["Layer_18"].append((-166,  -80))#
polygon_sec_4["Layer_18"].append((-185,    0))
polygon_sec_4["Layer_18"].append((-166,   80))#
polygon_sec_4["Layer_18"].append((-150,   70))
polygon_sec_4["Layer_18"].append((-100,   43))
polygon_sec_4["Layer_18"].append((-70,    25))
polygon_sec_4["Layer_18"].append((-65,    20))
polygon_sec_4["Layer_18"].append((-50,    10))
polygon_sec_4["Layer_18"].append((-42,     5))
polygon_sec_4["Layer_18"].append((-40,     0))

# polygon_sec_4["Layer_36"].append((-85,     0))
# polygon_sec_4["Layer_36"].append((-86,    -7))
# # polygon_sec_4["Layer_36"].append((-96,   -15))
# polygon_sec_4["Layer_36"].append((-100,  -25))
# polygon_sec_4["Layer_36"].append((-131,  -49))
# polygon_sec_4["Layer_36"].append((-150,  -61))
# polygon_sec_4["Layer_36"].append((-160,  -67))
# polygon_sec_4["Layer_36"].append((-200,  -90))
# polygon_sec_4["Layer_36"].append((-213,  -99))
# polygon_sec_4["Layer_36"].append((-265, -129)) # OG
# polygon_sec_4["Layer_36"].append((-281, -140))#
# polygon_sec_4["Layer_36"].append((-295, -100))
# polygon_sec_4["Layer_36"].append((-298,    0))
# polygon_sec_4["Layer_36"].append((-295,  100))
# polygon_sec_4["Layer_36"].append((-285,  110))
# polygon_sec_4["Layer_36"].append((-281,  135))#
# polygon_sec_4["Layer_36"].append((-265,  127)) # OG
# polygon_sec_4["Layer_36"].append((-218,   99))
# polygon_sec_4["Layer_36"].append((-135,   49))
# polygon_sec_4["Layer_36"].append((-115,   37))
# polygon_sec_4["Layer_36"].append((-100,   18))
# polygon_sec_4["Layer_36"].append((-90,    11))
# polygon_sec_4["Layer_36"].append((-85,     0))

polygon_sec_4["Layer_36"].append((-85,     0))
polygon_sec_4["Layer_36"].append((-86,    -7))
polygon_sec_4["Layer_36"].append((-100,  -10))
polygon_sec_4["Layer_36"].append((-130,  -45))
polygon_sec_4["Layer_36"].append((-150,  -60))
polygon_sec_4["Layer_36"].append((-160,  -65))
polygon_sec_4["Layer_36"].append((-200,  -90))
polygon_sec_4["Layer_36"].append((-213,  -95))
polygon_sec_4["Layer_36"].append((-265, -125)) # OG
polygon_sec_4["Layer_36"].append((-275, -135))#
polygon_sec_4["Layer_36"].append((-285,    0))
polygon_sec_4["Layer_36"].append((-275,  135))#
polygon_sec_4["Layer_36"].append((-265,  125)) # OG
polygon_sec_4["Layer_36"].append((-220,   95))
polygon_sec_4["Layer_36"].append((-135,   45))
polygon_sec_4["Layer_36"].append((-115,   35))
polygon_sec_4["Layer_36"].append((-100,   15))
polygon_sec_4["Layer_36"].append((-90,    10))
polygon_sec_4["Layer_36"].append((-85,     0))


polygon_sec_5  = {}
# Outer_Sector_5 = [(0, 0), (-340, -200), (0, -450), (0, 0)]
# Outer_Sector_5 = [(0, 0), (-357, -210), (0, -455), (0, 0)]
Outer_Sector_5 = [(0, 0), (-357, -210), (-357, -425), (0, -425), (0, 0)]
polygon_sec_5["Layer_6"]  = Outer_Sector_5.copy()
polygon_sec_5["Layer_18"] = Outer_Sector_5.copy()
polygon_sec_5["Layer_36"] = Outer_Sector_5.copy()
del Outer_Sector_5

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
polygon_sec_5["Layer_6"].append((-14,    -20))
polygon_sec_5["Layer_6"].append((-8,     -25))
polygon_sec_5["Layer_6"].append((-9,     -80))
polygon_sec_5["Layer_6"].append((-12,   -120)) # OG
polygon_sec_5["Layer_6"].append((-15,   -128))#
polygon_sec_5["Layer_6"].append((-65,   -109))
polygon_sec_5["Layer_6"].append((-105,   -75)) # OG
polygon_sec_5["Layer_6"].append((-100,   -70))
polygon_sec_5["Layer_6"].append((-18,    -18))
# polygon_sec_5["Layer_6"].append((-17,    -18))
polygon_sec_5["Layer_6"].append((-14,    -20))

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

polygon_sec_5["Layer_18"].append((-21,   -35))
# polygon_sec_5["Layer_18"].append((-13,   -38))
polygon_sec_5["Layer_18"].append((-16,   -45))
polygon_sec_5["Layer_18"].append((-15,   -60))
polygon_sec_5["Layer_18"].append((-15,  -195))#
polygon_sec_5["Layer_18"].append((-50,  -190))
polygon_sec_5["Layer_18"].append((-100, -168))
polygon_sec_5["Layer_18"].append((-140, -141))
polygon_sec_5["Layer_18"].append((-160, -115))#
polygon_sec_5["Layer_18"].append((-151, -103))
polygon_sec_5["Layer_18"].append((-100,  -73))
polygon_sec_5["Layer_18"].append((-50,   -44))
polygon_sec_5["Layer_18"].append((-30,   -37))
# polygon_sec_5["Layer_18"].append((-26,   -31))
polygon_sec_5["Layer_18"].append((-21,   -35))


# polygon_sec_5["Layer_36"].append((-45,   -75))
# # polygon_sec_5["Layer_36"].append((-35,   -76))
# polygon_sec_5["Layer_36"].append((-40,   -76))
# polygon_sec_5["Layer_36"].append((-26,   -104))
# polygon_sec_5["Layer_36"].append((-24,   -150))
# polygon_sec_5["Layer_36"].append((-22,   -200))
# polygon_sec_5["Layer_36"].append((-22,   -250))
# polygon_sec_5["Layer_36"].append((-26,   -290))
# polygon_sec_5["Layer_36"].append((-35,   -300))#
# polygon_sec_5["Layer_36"].append((-50,   -310))
# polygon_sec_5["Layer_36"].append((-70,   -300))
# polygon_sec_5["Layer_36"].append((-100,  -299))
# polygon_sec_5["Layer_36"].append((-150,  -270))
# polygon_sec_5["Layer_36"].append((-200,  -230))
# polygon_sec_5["Layer_36"].append((-255,  -182-8))
# polygon_sec_5["Layer_36"].append((-260,  -180))#
# polygon_sec_5["Layer_36"].append((-236,  -178))
# polygon_sec_5["Layer_36"].append((-235,  -165))
# polygon_sec_5["Layer_36"].append((-200,  -150+8))
# polygon_sec_5["Layer_36"].append((-150,  -120+4))
# polygon_sec_5["Layer_36"].append((-100,  -90+4))
# polygon_sec_5["Layer_36"].append((-80,   -78))
# polygon_sec_5["Layer_36"].append((-45,   -75))

polygon_sec_5["Layer_36"].append((-45,    -75))
# polygon_sec_5["Layer_36"].append((-40,    -76))
polygon_sec_5["Layer_36"].append((-30,   -100))
polygon_sec_5["Layer_36"].append((-25,   -150))
# polygon_sec_5["Layer_36"].append((-24,   -200))
polygon_sec_5["Layer_36"].append((-25,   -250))
polygon_sec_5["Layer_36"].append((-26,   -290))
polygon_sec_5["Layer_36"].append((-35,   -300)) #
polygon_sec_5["Layer_36"].append((-45,   -310))#
# polygon_sec_5["Layer_36"].append((-70,   -300))
# polygon_sec_5["Layer_36"].append((-100,  -299))
# polygon_sec_5["Layer_36"].append((-150,  -270))
# polygon_sec_5["Layer_36"].append((-200,  -230))
# polygon_sec_5["Layer_36"].append((-255,  -190))
polygon_sec_5["Layer_36"].append((-260,  -180))#
polygon_sec_5["Layer_36"].append((-236,  -180))
polygon_sec_5["Layer_36"].append((-235,  -165))
polygon_sec_5["Layer_36"].append((-200,  -145))
polygon_sec_5["Layer_36"].append((-150,  -116))
polygon_sec_5["Layer_36"].append((-100,   -86))
polygon_sec_5["Layer_36"].append((-80,    -78))
polygon_sec_5["Layer_36"].append((-45,    -75))

polygon_sec_6  = {}
# Outer_Sector_6 = [(0, 0), (0, -455), (357, -210), (0, 0)]
Outer_Sector_6 = [(0, 0), (0, -425), (357, -425), (357, -210), (0, 0)]
polygon_sec_6["Layer_6"]  = Outer_Sector_6.copy()
polygon_sec_6["Layer_18"] = Outer_Sector_6.copy()
polygon_sec_6["Layer_36"] = Outer_Sector_6.copy()
del Outer_Sector_6

# polygon_sec_6["Layer_6"].append((12,   -21))
# polygon_sec_6["Layer_6"].append((17,   -18))
# polygon_sec_6["Layer_6"].append((100,  -69))
# polygon_sec_6["Layer_6"].append((10,  -118))
# polygon_sec_6["Layer_6"].append((8,    -24))
# polygon_sec_6["Layer_6"].append((12,   -21))
polygon_sec_6["Layer_6"].append((12,   -21))
polygon_sec_6["Layer_6"].append((17,   -18))
polygon_sec_6["Layer_6"].append((100,  -69)) # OG
polygon_sec_6["Layer_6"].append((100,  -75))#
polygon_sec_6["Layer_6"].append((70,  -100))
polygon_sec_6["Layer_6"].append((50,  -110))
polygon_sec_6["Layer_6"].append((14,  -125))#
polygon_sec_6["Layer_6"].append((10,  -118)) # OG
polygon_sec_6["Layer_6"].append((8,    -24))
polygon_sec_6["Layer_6"].append((12,   -21))

# polygon_sec_6["Layer_18"].append((20,   -35))
# polygon_sec_6["Layer_18"].append((27,   -34))
# polygon_sec_6["Layer_18"].append((30,   -35))
# polygon_sec_6["Layer_18"].append((35,   -38))
# polygon_sec_6["Layer_18"].append((50,   -43))
# polygon_sec_6["Layer_18"].append((80,   -61))
# polygon_sec_6["Layer_18"].append((172, -115))#
# polygon_sec_6["Layer_18"].append((150, -135+10))
# polygon_sec_6["Layer_18"].append((140, -150+10))
# polygon_sec_6["Layer_18"].append((100, -180+10))
# polygon_sec_6["Layer_18"].append((50,  -200+10))
# polygon_sec_6["Layer_18"].append((13,  -200))#
# polygon_sec_6["Layer_18"].append((13,   -80))
# polygon_sec_6["Layer_18"].append((17,   -60))
# polygon_sec_6["Layer_18"].append((18,   -42))
# polygon_sec_6["Layer_18"].append((15,   -39))
# polygon_sec_6["Layer_18"].append((20,   -35))
###############################################
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

polygon_sec_6["Layer_18"].append((20,   -35))
# polygon_sec_6["Layer_18"].append((27,   -34))
polygon_sec_6["Layer_18"].append((30,   -35))
polygon_sec_6["Layer_18"].append((35,   -38))
polygon_sec_6["Layer_18"].append((50,   -43))
polygon_sec_6["Layer_18"].append((80,   -61))
# polygon_sec_6["Layer_18"].append((172, -115))#
polygon_sec_6["Layer_18"].append((150, -100))#
polygon_sec_6["Layer_18"].append((150, -120))
polygon_sec_6["Layer_18"].append((140, -135))
polygon_sec_6["Layer_18"].append((100, -165))
polygon_sec_6["Layer_18"].append((50,  -185))
polygon_sec_6["Layer_18"].append((15,  -195))#
polygon_sec_6["Layer_18"].append((15,   -80))
polygon_sec_6["Layer_18"].append((17,   -60))
polygon_sec_6["Layer_18"].append((18,   -42))
# polygon_sec_6["Layer_18"].append((15,   -39))
polygon_sec_6["Layer_18"].append((20,   -35))


# # polygon_sec_6["Layer_36"].append((50,    -65))
# polygon_sec_6["Layer_36"].append((50,    -73))
# # polygon_sec_6["Layer_36"].append((100,   -200))
# polygon_sec_6["Layer_36"].append((54,    -73))
# polygon_sec_6["Layer_36"].append((75,    -76))
# polygon_sec_6["Layer_36"].append((100,   -85))
# polygon_sec_6["Layer_36"].append((120,   -95))
# polygon_sec_6["Layer_36"].append((150,  -115))
# polygon_sec_6["Layer_36"].append((200,  -141))
# polygon_sec_6["Layer_36"].append((230,  -157))
# # polygon_sec_6["Layer_36"].append((235,  -165)) # OG
# polygon_sec_6["Layer_36"].append((265,  -175))#
# polygon_sec_6["Layer_36"].append((265,  -180))
# polygon_sec_6["Layer_36"].append((175,  -250))
# # polygon_sec_6["Layer_36"].append((150,  -275))
# polygon_sec_6["Layer_36"].append((150,  -270))
# # polygon_sec_6["Layer_36"].append((50,   -315))
# polygon_sec_6["Layer_36"].append((40,   -315))
# polygon_sec_6["Layer_36"].append((35,   -315))
# # polygon_sec_6["Layer_36"].append((24,   -325))
# # polygon_sec_6["Layer_36"].append((22,   -325))#
# polygon_sec_6["Layer_36"].append((25,   -315))#
# polygon_sec_6["Layer_36"].append((25,   -285))
# polygon_sec_6["Layer_36"].append((25,   -250))
# polygon_sec_6["Layer_36"].append((26,   -235))
# polygon_sec_6["Layer_36"].append((25,   -200))
# polygon_sec_6["Layer_36"].append((27,   -150))
# polygon_sec_6["Layer_36"].append((30,   -120))
# polygon_sec_6["Layer_36"].append((30,   -110))
# polygon_sec_6["Layer_36"].append((35,   -100))
# polygon_sec_6["Layer_36"].append((38,    -80))
# # polygon_sec_6["Layer_36"].append((100,   -200))
# # polygon_sec_6["Layer_36"].append((50,    -65))
# polygon_sec_6["Layer_36"].append((50,    -73))

polygon_sec_6["Layer_36"].append((50,    -73))
polygon_sec_6["Layer_36"].append((54,    -73))
polygon_sec_6["Layer_36"].append((75,    -76))
polygon_sec_6["Layer_36"].append((100,   -85))
polygon_sec_6["Layer_36"].append((240,  -160))
polygon_sec_6["Layer_36"].append((240,  -190))#
polygon_sec_6["Layer_36"].append((145,  -260))
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
polygon_sec_6["Layer_36"].append((50,    -73))
    
polygon_pip_secs = {}
polygon_pip_secs["Sector_1"] = polygon_sec_1
polygon_pip_secs["Sector_2"] = polygon_sec_2
polygon_pip_secs["Sector_3"] = polygon_sec_3
polygon_pip_secs["Sector_4"] = polygon_sec_4
polygon_pip_secs["Sector_5"] = polygon_sec_5
polygon_pip_secs["Sector_6"] = polygon_sec_6

# Inner contours for the loose and tight additional pion DC polygons.
# Each pair is (x, y) in detector cm in the raw, unrotated pion DC frame.
PIP_TESTDC_OUTERS = {
    1: [(0, 0), (357, 210), (357, -210), (0, 0)],
    2: [(0, 0), (357, 210), (357, 425), (0, 425), (0, 0)],
    3: [(0, 0), (0, 425), (-357, 425), (-357, 210), (0, 0)],
    4: [(0, 0), (-357, 210), (-357, -210), (0, 0)],
    5: [(0, 0), (-357, -210), (-357, -425), (0, -425), (0, 0)],
    6: [(0, 0), (0, -425), (357, -425), (357, -210), (0, 0)],
}
PIP_TESTDC_INNER = {
    "loose": {
        6: {
            1: [(14.10006638, -6.25698026), (114.14966106, -61.45700747), (122.19700478, -56.85738068), (126.80332077, 0.6428354), (124.50016277, 23.64322222), (114.14966106, 62.74267828), (14.10006638, 7.54265107)],
            2: [(7.39802821, 13.10912149), (2.79797316, 16.55903643), (5.09834341, 133.8583973), (79.84666758, 103.96263896), (108.59855392, 75.20909234), (108.59855392, 68.30926246), (13.14758294, 10.80892787)],
            3: [(-13.06650837, 9.61658286), (-106.2167999, 69.41648916), (-108.51654476, 75.16661013), (-83.21660944, 103.9202188), (-51.01675408, 117.71540257), (-10.76676351, 132.66706881), (-6.16658833, 126.91469496), (-2.7166283, 16.51642764)],
            4: [(-14.03572945, -6.98558607), (-112.93558211, -62.18567262), (-124.43566063, -62.18567262), (-130.18604262, -0.08576299), (-124.43566063, 66.61452933), (-112.93558211, 62.01414663), (-14.03572945, 6.81406008)],
            5: [(-10.33328935, -12.2497887), (-3.43337826, -17.99987375), (-4.58290646, -81.25005828), (-8.03354748, -127.24998768), (-11.48350303, -136.44997356), (-68.98321913, -114.60010096), (-114.98354039, -75.49997323), (-109.2331575, -69.74988819), (-14.93345857, -9.95035545)],
            6: [(13.1998438, -9.70009533), (108.65068318, -68.35012507), (108.65068318, -75.24995187), (74.14860423, -103.99973085), (51.14904613, -115.49994282), (9.74997863, -132.75026079), (5.15061537, -124.69996221), (2.85024829, -16.59992213)],
        },
        18: {
            1: [(34.40188243, -4.0295352), (36.69818359, -10.92935039), (40.14606264, -10.92935039), (65.44650315, -32.77926579), (97.64955638, -52.32974343), (193.10028358, -105.22957812), (195.39658473, -61.52974733), (195.39658473, -4.0295352), (189.6455499, 87.97050381), (173.55087791, 85.6703151), (97.64955638, 46.57086173), (40.14606264, 8.62037629)],
            2: [(14.06808848, 27.97768499), (7.16531212, 41.7780872), (6.02056172, 80.87534682), (6.02056172, 185.52921042), (9.46852251, 202.77877448), (126.76773705, 156.77493059), (167.01908043, 122.27580248), (167.01908043, 110.77859631), (161.26790926, 102.72829911), (103.76990718, 68.22842004), (57.76739264, 42.92780782), (46.2650503, 40.62836658), (20.97086484, 27.97768499)],
            3: [(-19.32054519, 29.03877381), (-28.51954926, 25.5888958), (-34.27064048, 31.3389428), (-51.51705944, 37.08898979), (-86.01675206, 55.48883981), (-166.51831973, 106.08654996), (-166.51831973, 123.33594), (-109.02111693, 169.33931979), (-17.01736683, 203.83809987), (-11.26627561, 192.34100969), (-11.26627561, 77.33856783), (-13.56945397, 54.33913079), (-14.72104316, 33.63911179)],
            4: [(-27.93247657, -2.40317773), (-27.93247657, -8.15327309), (-39.42771325, -11.60318011), (-52.08138464, -23.10337083), (-53.2329647, -26.55327785), (-172.8327796, -94.40320156), (-194.67852754, -2.40317773), (-172.8327796, 89.5968461), (-154.42806255, 78.09665538), (-96.93131522, 47.04674121), (-62.4318959, 26.34654811), (-56.68085024, 20.59720371), (-30.22878205, 3.34691763)],
            5: [(-13.5513612, -25.17501133), (-7.80041715, -36.67519495), (-6.64885744, -53.92471942), (-6.64885744, -209.17494544), (-46.89861126, -203.42485363), (-104.40119722, -178.12505043), (-150.40189509, -147.07515542), (-173.39881677, -117.17497838), (-163.04848838, -103.3753588), (-46.89861126, -35.52472601), (-23.90168958, -27.47519825)],
            6: [(13.78171949, -25.14268039), (25.283928, -25.14268039), (31.03503226, -28.59258613), (48.28149031, -34.34267935), (82.78811584, -55.04286476), (163.28301127, -99.89239037), (163.28301127, -122.89276326), (151.78765748, -140.14304293), (105.78567815, -174.6428513), (48.28149031, -197.64247324), (8.03746995, -209.14265968), (8.03746995, -76.89276844), (10.33379882, -53.89239554), (11.48539062, -33.19296109)],
        },
        36: {
            1: [(64.97912279, -1.48191207), (76.4812428, -9.53142037), (105.22968819, -41.73170646), (277.72721514, -145.23160688), (300.73145517, -160.18165924), (300.73145517, 148.02011352), (277.72721514, 148.02011352), (156.97551894, 74.41806496), (87.97650816, 26.11801131), (66.13070572, 5.41788104)],
            2: [(29.18690138, 58.83146915), (15.388557, 93.33531624), (9.63753318, 127.83465753), (9.63753318, 334.83070532), (270.68877387, 196.83334013), (276.43979768, 185.33606291), (256.88357487, 170.38434578), (118.8864218, 93.33531624), (107.38437417, 89.88087632), (38.38579764, 61.13167556)],
            3: [(-46.88840218, 47.37999217), (-51.48789251, 54.27987952), (-104.38545869, 72.68158169), (-127.38976504, 87.63334019), (-219.3864264, 139.38249529), (-258.49237626, 158.93017353), (-276.8903376, 179.63434137), (-161.88936989, 260.13052387), (-46.88840218, 311.87967897), (-23.89095051, 317.63208832), (-23.89095051, 99.13064921), (-29.63517241, 87.63334019), (-33.08993117, 64.62971054)],
            4: [(-63.81836526, -2.53020335), (-64.96995222, -10.57974763), (-81.06475103, -14.03041056), (-115.57123194, -54.28038485), (-138.56869786, -71.52994471), (-196.06579002, -106.03056636), (-211.01585654, -111.78066997), (-270.81612262, -146.28054065), (-282.31828293, -157.78074787), (-293.82044323, -2.53020335), (-282.31828293, 152.71733733), (-270.81612262, 141.22013396), (-219.07011062, 106.72101424), (-121.31545741, 49.21997816), (-98.31799148, 37.71977095), (-81.06475103, 14.72010748), (-69.56944541, 8.97000387)],
            5: [(-38.27170178, -49.73687191), (-21.02533631, -78.48654421), (-15.27426293, -135.98663977), (-15.27426293, -250.98683089), (-16.42584854, -296.98675715), (-38.27170178, -319.9863448), (-285.52672909, -170.48714768), (-257.9229478, -170.48714768), (-256.77136219, -153.23689373), (-101.51979961, -62.38675776), (-78.52236077, -53.18677251)],
            6: [(43.97852249, -62.9602332), (72.72697905, -66.41013517), (101.4754356, -76.76059204), (262.47775979, -163.01039415), (262.47775979, -197.5101648), (153.22814114, -278.01063094), (15.23006593, -341.26008531), (15.23006593, -266.51045707), (16.37479465, -249.26019626), (15.23006593, -209.01033868), (17.52637803, -151.51022028), (20.97427351, -117.01044963), (20.97427351, -105.51027576), (26.72533576, -94.01010189), (30.1800859, -71.01050511)],
        },
    },
    "tight": {
        6: {
            1: [(30.60005019, -5.8284436), (108.89973299, -49.0284649), (115.19765416, -45.42875698), (118.80259711, -0.42858787), (117.00012563, 17.57171486), (108.89973299, 48.17128917), (30.60005019, 4.97126787)],
            2: [(15.06820178, 26.26037616), (11.4681587, 28.9603096), (13.26844846, 120.75980941), (71.76713694, 97.36312897), (94.26861321, 74.86035336), (94.26861321, 69.46048649), (19.56785331, 24.46022464)],
            3: [(-19.62209833, 23.58882332), (-92.52232648, 70.38874999), (-94.32212681, 74.88884465), (-74.52217743, 97.39166883), (-49.32229062, 108.18789961), (-17.82229801, 119.88920362), (-14.2221609, 115.38734583), (-11.52219219, 28.98870183)],
            4: [(-30.64286864, -5.34275552), (-108.04275333, -48.54282325), (-117.04281478, -48.54282325), (-121.54311373, 0.05710602), (-117.04281478, 52.2573348), (-108.04275333, 48.6570353), (-30.64286864, 5.45696756)],
            5: [(-16.44441, -25.16650129), (-11.04447957, -29.66656785), (-11.94411034, -79.16671226), (-14.64461201, -115.16665701), (-17.34457722, -122.36664596), (-62.34435504, -105.26674567), (-98.34460646, -74.66664571), (-93.84430681, -70.16657915), (-20.04454243, -23.36694483)],
            6: [(19.53321112, -23.53340797), (94.23386803, -69.43343124), (94.23386803, -74.8332957), (67.23224102, -97.33312272), (49.23258685, -106.33328862), (16.83331664, -119.83353746), (13.23381496, -113.53330379), (11.43352768, -28.93327243)],
        },
        18: {
            1: [(52.07075258, 2.68631856), (53.86785783, -2.7135368), (56.56619796, -2.7135368), (76.3665427, -19.81347059), (101.56893219, -35.1138444), (176.2695013, -76.51371503), (178.06660655, -42.31384745), (178.06660655, 2.68631856), (173.56579668, 74.6863491), (160.96996643, 72.88620141), (101.56893219, 42.28662921), (56.56619796, 12.5862493)],
            2: [(27.28739267, 44.6816429), (21.88521987, 55.48195767), (20.98932825, 86.07981303), (20.98932825, 167.98283671), (23.68773235, 181.48249554), (115.48711764, 145.47948728), (146.98816898, 118.48016963), (146.98816898, 109.4823561), (142.48725241, 103.18212351), (97.488816, 76.18221815), (61.4868481, 56.38173902), (52.48501497, 54.58217632), (32.68956548, 44.6816429)],
            3: [(-23.78901998, 43.97436121), (-30.98824056, 41.27445668), (-35.48909456, 45.77449346), (-48.986292, 50.27453024), (-75.98605144, 64.67441286), (-138.98727832, 104.2726208), (-138.98727832, 117.77214344), (-93.98946743, 153.7747885), (-21.98653257, 180.77383378), (-17.48567857, 171.77611103), (-17.48567857, 81.77420001), (-19.28816599, 63.77464058), (-20.18940969, 47.57462571)],
            4: [(-48.04759847, 1.60214389), (-48.04759847, -2.89793074), (-57.04387065, -5.59785798), (-66.94674391, -14.59800724), (-67.84798048, -17.29793447), (-161.44783562, -70.39787476), (-178.54450792, 1.60214389), (-161.44783562, 73.60216253), (-147.04414402, 64.60201328), (-102.04668959, 40.30208045), (-75.04714403, 24.10192932), (-70.54632568, 19.6024424), (-49.8447071, 6.10221851)],
            5: [(-25.96773195, -41.55000885), (-21.46699313, -50.55015255), (-20.56577249, -64.0497804), (-20.56577249, -185.54995728), (-52.06557982, -181.04988542), (-97.06760362, -161.25003944), (-133.06814978, -136.95012161), (-151.06574066, -113.54998306), (-142.96548366, -102.75028078), (-52.06557982, -49.64978555), (-34.06798895, -43.35015513)],
            6: [(24.14125628, -41.57151831), (33.14298468, -41.57151831), (37.64384888, -44.27144454), (51.14107692, -48.7715175), (78.14626211, -64.9716626), (141.14226724, -100.07129134), (141.14226724, -118.07158316), (132.14590339, -131.57180203), (96.14435436, -158.57165207), (51.14107692, -176.57135619), (19.64575664, -185.5715021), (19.64575664, -82.07158721), (22.34412933, -47.87173799)],
        },
        36: {
            1: [(90.014746, 0.9877881), (99.01640514, -5.31182709), (121.51518848, -30.51205099), (274.51657134, -123.21201403), (274.51657134, 117.98937334), (256.51325305, 117.98937334), (162.01192559, 60.38777013), (108.01269977, 22.58772814), (90.91598481, 6.38762619)],
            2: [(47.20855393, 77.44329807), (36.40984963, 104.44630884), (31.90904838, 131.44579333), (31.90904838, 293.44270029), (236.21001935, 185.44476232), (240.7108206, 176.44689319), (225.40595057, 164.74554935), (117.4081786, 104.44630884), (108.40657611, 101.74283412), (54.40769013, 79.24345961)],
            3: [(-52.07300019, 76.74512421), (-55.67260132, 82.14503604), (-97.0706966, 96.54636818), (-115.07406678, 108.24774439), (-187.07145393, 148.74708317), (-217.67611035, 164.04526614), (-232.07451487, 180.24852793), (-142.07375753, 243.24554031), (-52.07300019, 283.74487909), (-34.07499454, 288.24676467), (-34.07499454, 117.24563841), (-38.57047255, 108.24774439), (-41.2741968, 90.2449038)],
            4: [(-99.12173893, 1.68691992), (-100.0229809, -4.61272343), (-112.6189104, -7.31324225), (-139.62398242, -38.81322213), (-157.62199923, -52.31287768), (-202.61972352, -79.31336418), (-214.31977558, -83.81344526), (-261.11998382, -110.81334406), (-270.12167449, -119.81350623), (-279.12336517, 1.68691992), (-270.12167449, 123.18499523), (-261.11998382, 114.1871839), (-220.62310487, 87.18787281), (-144.11946322, 42.18706197), (-126.12144641, 33.1868998), (-112.6189104, 15.18716317), (-103.62258426, 10.68708209)],
            5: [(-49.48383177, -91.8422409), (-35.98667619, -114.34198444), (-31.48583616, -159.34205922), (-32.38707707, -285.34215108), (-49.48383177, -303.34182837), (-242.9877662, -186.34245672), (-221.38480692, -186.34245672), (-220.48356601, -172.84225797), (-98.98234312, -101.74215156), (-80.98434751, -94.54216311)],
            6: [(54.01575722, -79.69306161), (76.51454931, -82.39298489), (99.01334139, -90.49334244), (225.01516032, -157.99318757), (225.01516032, -184.99300808), (139.51545877, -247.99337288), (31.51696513, -297.49294586), (31.51696513, -238.99323681), (32.41283978, -225.4930327), (31.51696513, -193.99314415), (33.31407895, -148.99305149), (36.01243193, -121.99323098), (36.01243193, -112.99309491), (40.51326325, -103.99295884), (43.21698076, -85.9932744)],
        },
    },
}

def pip_testdc_outer(sector):
    expected = PIP_TESTDC_OUTERS[sector]
    count    = len(expected)
    for layer in [6, 18, 36]:
        path = polygon_pip_secs["Sector_%s" % sector]["Layer_%s" % layer]
        if(list(path[:count]) != expected):
            raise ValueError("pion test DC outer path does not match sector %s layer %s" % (sector, layer))
    return list(expected)

def assemble_pip_testdc_layer(layer, level):
    # Nominal outer path, then the supplied inner contour, closed by repeating its first vertex.
    path = []
    for sector in range(1, 7, 1):
        inner = list(PIP_TESTDC_INNER[level][layer][sector])
        sector_path = pip_testdc_outer(sector)
        sector_path.extend(inner)
        sector_path.append(inner[0])
        path.extend(sector_path)
    return path

def pip_testdc_polygon_key(layer, level):
    if(int(layer) == 6):
        return "Layer_6__pip_%s" % level
    return "Layer_%s_pip_%s" % (int(layer), level)

def pip_testdc_layer_column(layer, level):
    return "My_pip_DC_Fiducial_Cuts_Layer_%s_%s" % (int(layer), level)

def pip_testdc_layer_code(layer, level):
    # The negation stays on the assembled outer-plus-inner path.
    key = pip_testdc_polygon_key(layer, level)
    return "! is_point_in_polygon(pip_x_DC_%s, pip_y_DC_%s, Polygon_Layers[\"%s\"])" % (int(layer), int(layer), key)


if(__name__ in ["__main__"]):    
    print("\nDone defining polygon_pip_secs...\n")


polygon_ele = {}
polygon_ele["Layer_6__ele"] = [(-65, 0), (-65, -3), (13, -41), (14, -40)]
polygon_ele["Layer_6__ele"].append((19,    0))
polygon_ele["Layer_6__ele"].append((13,   42))#
polygon_ele["Layer_6__ele"].append((-65,   2))
polygon_ele["Layer_6__ele"].append((-65,   0))

polygon_ele["Layer_18_ele"] = [(-105, 0), (-94, -8), (15, -62)]
polygon_ele["Layer_18_ele"].append((25,   0))
polygon_ele["Layer_18_ele"].append((15,   63))#
polygon_ele["Layer_18_ele"].append((-92,  9))
polygon_ele["Layer_18_ele"].append((-105, 0))

polygon_ele["Layer_36_ele"] = [(-170, 0), (-169, -5), (-100, -36), (5, -81)]
polygon_ele["Layer_36_ele"].append((18,    0))
polygon_ele["Layer_36_ele"].append((5,    85))#
polygon_ele["Layer_36_ele"].append((-75,  49))
polygon_ele["Layer_36_ele"].append((-170,  3))    
polygon_ele["Layer_36_ele"].append((-170,  0))

if(__name__ in ["__main__"]):
    print("\nDone defining polygon_ele...\n")

polygon_all    = {}
for particle    in ["ele", "pip"]:
    for DC_Layer_ii in [6, 18, 36]:
        if(particle in ["ele"]):
            polygon_all["".join(["Layer_",     str(DC_Layer_ii), "_", "" if(DC_Layer_ii not in [6]) else "_", "ele"])] = polygon_ele["".join(["Layer_",       str(DC_Layer_ii), "_", "" if(DC_Layer_ii not in [6]) else "_", "ele"])].copy()
        else:
            polygon_all["".join(["Layer_",     str(DC_Layer_ii), "_", "" if(DC_Layer_ii not in [6]) else "_", "pip"])] = polygon_pip_secs[f"Sector_{1}"][f"Layer_{DC_Layer_ii}"].copy()
            for sec in range(2, 7, 1):
                polygon_all["".join(["Layer_", str(DC_Layer_ii), "_", "" if(DC_Layer_ii not in [6]) else "_", "pip"])].extend(polygon_pip_secs[f"Sector_{sec}"][f"Layer_{DC_Layer_ii}"])
for level in ["loose", "tight"]:
    for layer in [6, 18, 36]:
        polygon_all[pip_testdc_polygon_key(layer, level)] = assemble_pip_testdc_layer(layer, level)

if(__name__ in ["__main__"]):
    print("\nDone defining polygon_all...\n")
    for ii in polygon_all:
        print(f"polygon_all[{ii}] = {polygon_all[ii]}")

New_Test_Fiducial_DC_Cuts_Functions = str(str("".join(["""
    auto Polygon_Layers = std::map<std::string, std::vector<std::pair<double, double>>>{
    \t""", str(str(str(str(str(str(str(polygon_all).replace("[", "{")).replace("], 'Lay", "}},\n\t{'Lay")).replace("]", "}")).replace(":", ",")).replace("(", "{")).replace(")", "}")).replace(", ", ", "), """
    };
    
    bool is_point_in_polygon(double x, double y, const std::vector<std::pair<double, double>>& polygon) {
        double winding_number = 0.0;
        int num_vertices = polygon.size();
    
        for (int i = 0; i < num_vertices; ++i) {
            double x1 = polygon[i].first;
            double y1 = polygon[i].second;
            double x2 = polygon[(i + 1) % num_vertices].first;
            double y2 = polygon[(i + 1) % num_vertices].second;
    
            double a1 = atan2(y1 - y, x1 - x);
            double a2 = atan2(y2 - y, x2 - x);
            double angle_diff = a2 - a1;
    
            if(angle_diff > 3.1415926){
                angle_diff -= 2 * 3.1415926;
            } else if(angle_diff < -3.1415926){
                angle_diff += 2 * 3.1415926;
            }
            winding_number += angle_diff;
        }
        return (std::abs(winding_number) > 3.1415926);
    }
"""])).replace("'", '"'))

if(__name__ in ["__main__"]):
    print("Code to run these Fiducial Cuts:")
    from MyCommonAnalysisFunction_richcap import color
    print(f'''{color.BOLD}\nNew_Test_Fiducial_DC_Cuts_Functions = """{New_Test_Fiducial_DC_Cuts_Functions}"""
    
    ROOT.gInterpreter.Declare(New_Test_Fiducial_DC_Cuts_Functions)
    {color.END}''')


import ROOT
# Declare a global variable to track if the functions have been declared
# fiducial_cuts_declared = False
ROOT.gInterpreter.Declare(New_Test_Fiducial_DC_Cuts_Functions)
def Apply_Test_Fiducial_Cuts(Data_Frame_In, List_of_Layers=["6", "18", "36"], List_of_Particles=["ele", "pip"], Define_Column=False, show_cut_code=False):
    # global fiducial_cuts_declared
    Data_Frame_Out = Data_Frame_In
    # if(not fiducial_cuts_declared): # Only declare the functions once
    #     ROOT.gInterpreter.Declare(New_Test_Fiducial_DC_Cuts_Functions)
    #     fiducial_cuts_declared = True
    if(show_cut_code):
        print(f"Code to run Fiducial Cuts from 'Apply_Test_Fiducial_Cuts':\n\n{New_Test_Fiducial_DC_Cuts_Functions}\n\n")
    for layer        in List_of_Layers:
        Polygon_Layer = f"{layer}" if(str(layer) not in ["6"]) else "6_"
        for particle in List_of_Particles:
            if(particle in ["ele"]):
                # As of 9/23/2024, the electron fiducial cuts are only meant for the rotated DC hit variables
                    # Also uses the inverse condition of the is_point_in_polygon() fuction (i.e., cuts are applied if 'is_point_in_polygon' is 'True' for the electron, but for the pion, they are applied if 'is_point_in_polygon' is False)
                cut_code_txt = f"""is_point_in_polygon({particle}_x_DC_{layer}_rot,  {particle}_y_DC_{layer}_rot,  Polygon_Layers["Layer_{Polygon_Layer}_{particle}"])"""
            else:
                cut_code_txt = f"""! is_point_in_polygon({particle}_x_DC_{layer},    {particle}_y_DC_{layer},      Polygon_Layers["Layer_{Polygon_Layer}_{particle}"])"""
            if(not Define_Column):
                Data_Frame_Out = Data_Frame_Out.Filter(cut_code_txt)
            if(show_cut_code):
                print(f"Applied Cut:\n{cut_code_txt}\n")
            else:
                Data_Frame_Out = Data_Frame_Out.Define(f"My_{particle}_DC_Fiducial_Cuts_Layer_{layer}", cut_code_txt)
            # if(not Define_Column):
            #     if(particle in ["ele"]):
            #         # As of 9/23/2024, the electron fiducial cuts are only meant for the rotated DC hit variables
            #             # Also uses the inverse condition of the is_point_in_polygon() fuction (i.e., cuts are applied if 'is_point_in_polygon' is 'True' for the electron, but for the pion, they are applied if 'is_point_in_polygon' is False)
            #         Data_Frame_Out = Data_Frame_Out.Filter(                                                 f"""is_point_in_polygon({particle}_x_DC_{layer}_rot,  {particle}_y_DC_{layer}_rot,  Polygon_Layers["Layer_{Polygon_Layer}_{particle}"])""")
            #     else:
            #         Data_Frame_Out = Data_Frame_Out.Filter(                                                 f"""! is_point_in_polygon({particle}_x_DC_{layer},    {particle}_y_DC_{layer},      Polygon_Layers["Layer_{Polygon_Layer}_{particle}"])""")
            # else:
            #     if(particle in ["ele"]):
            #         Data_Frame_Out = Data_Frame_Out.Define(f"My_{particle}_DC_Fiducial_Cuts_Layer_{layer}", f"""is_point_in_polygon({particle}_x_DC_{layer}_rot,  {particle}_y_DC_{layer}_rot,  Polygon_Layers["Layer_{Polygon_Layer}_{particle}"])""")
            #     else:
            #         Data_Frame_Out = Data_Frame_Out.Define(f"My_{particle}_DC_Fiducial_Cuts_Layer_{layer}", f"""! is_point_in_polygon({particle}_x_DC_{layer},    {particle}_y_DC_{layer},      Polygon_Layers["Layer_{Polygon_Layer}_{particle}"])""")
    return Data_Frame_Out

if(__name__ in ["__main__"]):
    print("\nDone defining the 'Apply_Test_Fiducial_Cuts(...)' function\n")
