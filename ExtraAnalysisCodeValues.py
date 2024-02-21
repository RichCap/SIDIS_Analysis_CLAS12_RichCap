New_z_pT_and_MultiDim_Binning_Code = """
float z_pT_Bin_Borders[18][65][4];
   // z_pT_Bin_Borders[Q2_y_Bin][z_pT_Bin][Border_Num]
    // Border_Num = 0 -> z_max
    // Border_Num = 1 -> z_min
    // Border_Num = 2 -> pT_max
    // Border_Num = 4 -> pT_min
    // (Total of 17 Q2-y bins with defined z-pT borders)
int Phi_h_Bin_Values[40][65][3];
 // Phi_h_Bin_Values[Q2_y_Bin][z_pT_Bin][Dimension]
    // Dimension = 0 -> Number of phi_h bins (either 24 or 1)
    // Dimension = 1 -> Number of combined z_pT + phi_h bins        (used for 3D unfolding - add the appropiate phi_h bin number to these values to get the 3D bin number - resets with every new Q2-y bin)
    // Dimension = 2 -> Number of combined Q2_y + z_pT + phi_h bins (used for 5D unfolding - add the appropiate phi_h bin number to these values to get the 5D bin number - does not resets with new bins)
    // (Total of 39 Q2-y bins including overflow bins)
z_pT_Bin_Borders[1][1][0] = 0.71; z_pT_Bin_Borders[1][1][1] = 0.4; z_pT_Bin_Borders[1][1][2] = 0.22; z_pT_Bin_Borders[1][1][3] = 0.05;
Phi_h_Bin_Values[1][1][0] =  24; Phi_h_Bin_Values[1][1][1] = 0; Phi_h_Bin_Values[1][1][2] = 0;
z_pT_Bin_Borders[1][2][0] = 0.71; z_pT_Bin_Borders[1][2][1] = 0.4; z_pT_Bin_Borders[1][2][2] = 0.32; z_pT_Bin_Borders[1][2][3] = 0.22;
Phi_h_Bin_Values[1][2][0] =  24; Phi_h_Bin_Values[1][2][1] = 24; Phi_h_Bin_Values[1][2][2] = 24;
z_pT_Bin_Borders[1][3][0] = 0.71; z_pT_Bin_Borders[1][3][1] = 0.4; z_pT_Bin_Borders[1][3][2] = 0.42; z_pT_Bin_Borders[1][3][3] = 0.32;
Phi_h_Bin_Values[1][3][0] =  24; Phi_h_Bin_Values[1][3][1] = 48; Phi_h_Bin_Values[1][3][2] = 48;
z_pT_Bin_Borders[1][4][0] = 0.71; z_pT_Bin_Borders[1][4][1] = 0.4; z_pT_Bin_Borders[1][4][2] = 0.52; z_pT_Bin_Borders[1][4][3] = 0.42;
Phi_h_Bin_Values[1][4][0] =  24; Phi_h_Bin_Values[1][4][1] = 72; Phi_h_Bin_Values[1][4][2] = 72;
z_pT_Bin_Borders[1][5][0] = 0.71; z_pT_Bin_Borders[1][5][1] = 0.4; z_pT_Bin_Borders[1][5][2] = 0.63; z_pT_Bin_Borders[1][5][3] = 0.52;
Phi_h_Bin_Values[1][5][0] =  24; Phi_h_Bin_Values[1][5][1] = 96; Phi_h_Bin_Values[1][5][2] = 96;
z_pT_Bin_Borders[1][6][0] = 0.71; z_pT_Bin_Borders[1][6][1] = 0.4; z_pT_Bin_Borders[1][6][2] = 0.75; z_pT_Bin_Borders[1][6][3] = 0.63;
Phi_h_Bin_Values[1][6][0] =  24; Phi_h_Bin_Values[1][6][1] = 120; Phi_h_Bin_Values[1][6][2] = 120;
z_pT_Bin_Borders[1][7][0] = 0.71; z_pT_Bin_Borders[1][7][1] = 0.4; z_pT_Bin_Borders[1][7][2] = 0.99; z_pT_Bin_Borders[1][7][3] = 0.75;
Phi_h_Bin_Values[1][7][0] =  24; Phi_h_Bin_Values[1][7][1] = 144; Phi_h_Bin_Values[1][7][2] = 144;
z_pT_Bin_Borders[1][8][0] = 0.4; z_pT_Bin_Borders[1][8][1] = 0.29; z_pT_Bin_Borders[1][8][2] = 0.22; z_pT_Bin_Borders[1][8][3] = 0.05;
Phi_h_Bin_Values[1][8][0] =  24; Phi_h_Bin_Values[1][8][1] = 168; Phi_h_Bin_Values[1][8][2] = 168;
z_pT_Bin_Borders[1][9][0] = 0.4; z_pT_Bin_Borders[1][9][1] = 0.29; z_pT_Bin_Borders[1][9][2] = 0.32; z_pT_Bin_Borders[1][9][3] = 0.22;
Phi_h_Bin_Values[1][9][0] =  24; Phi_h_Bin_Values[1][9][1] = 192; Phi_h_Bin_Values[1][9][2] = 192;
z_pT_Bin_Borders[1][10][0] = 0.4; z_pT_Bin_Borders[1][10][1] = 0.29; z_pT_Bin_Borders[1][10][2] = 0.42; z_pT_Bin_Borders[1][10][3] = 0.32;
Phi_h_Bin_Values[1][10][0] =  24; Phi_h_Bin_Values[1][10][1] = 216; Phi_h_Bin_Values[1][10][2] = 216;
z_pT_Bin_Borders[1][11][0] = 0.4; z_pT_Bin_Borders[1][11][1] = 0.29; z_pT_Bin_Borders[1][11][2] = 0.52; z_pT_Bin_Borders[1][11][3] = 0.42;
Phi_h_Bin_Values[1][11][0] =  24; Phi_h_Bin_Values[1][11][1] = 240; Phi_h_Bin_Values[1][11][2] = 240;
z_pT_Bin_Borders[1][12][0] = 0.4; z_pT_Bin_Borders[1][12][1] = 0.29; z_pT_Bin_Borders[1][12][2] = 0.63; z_pT_Bin_Borders[1][12][3] = 0.52;
Phi_h_Bin_Values[1][12][0] =  24; Phi_h_Bin_Values[1][12][1] = 264; Phi_h_Bin_Values[1][12][2] = 264;
z_pT_Bin_Borders[1][13][0] = 0.4; z_pT_Bin_Borders[1][13][1] = 0.29; z_pT_Bin_Borders[1][13][2] = 0.75; z_pT_Bin_Borders[1][13][3] = 0.63;
Phi_h_Bin_Values[1][13][0] =  24; Phi_h_Bin_Values[1][13][1] = 288; Phi_h_Bin_Values[1][13][2] = 288;
z_pT_Bin_Borders[1][14][0] = 0.4; z_pT_Bin_Borders[1][14][1] = 0.29; z_pT_Bin_Borders[1][14][2] = 0.99; z_pT_Bin_Borders[1][14][3] = 0.75;
Phi_h_Bin_Values[1][14][0] =  24; Phi_h_Bin_Values[1][14][1] = 312; Phi_h_Bin_Values[1][14][2] = 312;
z_pT_Bin_Borders[1][15][0] = 0.29; z_pT_Bin_Borders[1][15][1] = 0.23; z_pT_Bin_Borders[1][15][2] = 0.22; z_pT_Bin_Borders[1][15][3] = 0.05;
Phi_h_Bin_Values[1][15][0] =  24; Phi_h_Bin_Values[1][15][1] = 336; Phi_h_Bin_Values[1][15][2] = 336;
z_pT_Bin_Borders[1][16][0] = 0.29; z_pT_Bin_Borders[1][16][1] = 0.23; z_pT_Bin_Borders[1][16][2] = 0.32; z_pT_Bin_Borders[1][16][3] = 0.22;
Phi_h_Bin_Values[1][16][0] =  24; Phi_h_Bin_Values[1][16][1] = 360; Phi_h_Bin_Values[1][16][2] = 360;
z_pT_Bin_Borders[1][17][0] = 0.29; z_pT_Bin_Borders[1][17][1] = 0.23; z_pT_Bin_Borders[1][17][2] = 0.42; z_pT_Bin_Borders[1][17][3] = 0.32;
Phi_h_Bin_Values[1][17][0] =  24; Phi_h_Bin_Values[1][17][1] = 384; Phi_h_Bin_Values[1][17][2] = 384;
z_pT_Bin_Borders[1][18][0] = 0.29; z_pT_Bin_Borders[1][18][1] = 0.23; z_pT_Bin_Borders[1][18][2] = 0.52; z_pT_Bin_Borders[1][18][3] = 0.42;
Phi_h_Bin_Values[1][18][0] =  24; Phi_h_Bin_Values[1][18][1] = 408; Phi_h_Bin_Values[1][18][2] = 408;
z_pT_Bin_Borders[1][19][0] = 0.29; z_pT_Bin_Borders[1][19][1] = 0.23; z_pT_Bin_Borders[1][19][2] = 0.63; z_pT_Bin_Borders[1][19][3] = 0.52;
Phi_h_Bin_Values[1][19][0] =  24; Phi_h_Bin_Values[1][19][1] = 432; Phi_h_Bin_Values[1][19][2] = 432;
z_pT_Bin_Borders[1][20][0] = 0.29; z_pT_Bin_Borders[1][20][1] = 0.23; z_pT_Bin_Borders[1][20][2] = 0.75; z_pT_Bin_Borders[1][20][3] = 0.63;
Phi_h_Bin_Values[1][20][0] =  24; Phi_h_Bin_Values[1][20][1] = 456; Phi_h_Bin_Values[1][20][2] = 456;
z_pT_Bin_Borders[1][21][0] = 0.29; z_pT_Bin_Borders[1][21][1] = 0.23; z_pT_Bin_Borders[1][21][2] = 0.99; z_pT_Bin_Borders[1][21][3] = 0.75;
Phi_h_Bin_Values[1][21][0] =  1; Phi_h_Bin_Values[1][21][1] = 480; Phi_h_Bin_Values[1][21][2] = 480;
z_pT_Bin_Borders[1][22][0] = 0.23; z_pT_Bin_Borders[1][22][1] = 0.19; z_pT_Bin_Borders[1][22][2] = 0.22; z_pT_Bin_Borders[1][22][3] = 0.05;
Phi_h_Bin_Values[1][22][0] =  24; Phi_h_Bin_Values[1][22][1] = 481; Phi_h_Bin_Values[1][22][2] = 481;
z_pT_Bin_Borders[1][23][0] = 0.23; z_pT_Bin_Borders[1][23][1] = 0.19; z_pT_Bin_Borders[1][23][2] = 0.32; z_pT_Bin_Borders[1][23][3] = 0.22;
Phi_h_Bin_Values[1][23][0] =  24; Phi_h_Bin_Values[1][23][1] = 505; Phi_h_Bin_Values[1][23][2] = 505;
z_pT_Bin_Borders[1][24][0] = 0.23; z_pT_Bin_Borders[1][24][1] = 0.19; z_pT_Bin_Borders[1][24][2] = 0.42; z_pT_Bin_Borders[1][24][3] = 0.32;
Phi_h_Bin_Values[1][24][0] =  24; Phi_h_Bin_Values[1][24][1] = 529; Phi_h_Bin_Values[1][24][2] = 529;
z_pT_Bin_Borders[1][25][0] = 0.23; z_pT_Bin_Borders[1][25][1] = 0.19; z_pT_Bin_Borders[1][25][2] = 0.52; z_pT_Bin_Borders[1][25][3] = 0.42;
Phi_h_Bin_Values[1][25][0] =  24; Phi_h_Bin_Values[1][25][1] = 553; Phi_h_Bin_Values[1][25][2] = 553;
z_pT_Bin_Borders[1][26][0] = 0.23; z_pT_Bin_Borders[1][26][1] = 0.19; z_pT_Bin_Borders[1][26][2] = 0.63; z_pT_Bin_Borders[1][26][3] = 0.52;
Phi_h_Bin_Values[1][26][0] =  24; Phi_h_Bin_Values[1][26][1] = 577; Phi_h_Bin_Values[1][26][2] = 577;
z_pT_Bin_Borders[1][27][0] = 0.23; z_pT_Bin_Borders[1][27][1] = 0.19; z_pT_Bin_Borders[1][27][2] = 0.75; z_pT_Bin_Borders[1][27][3] = 0.63;
Phi_h_Bin_Values[1][27][0] =  1; Phi_h_Bin_Values[1][27][1] = 601; Phi_h_Bin_Values[1][27][2] = 601;
z_pT_Bin_Borders[1][28][0] = 0.23; z_pT_Bin_Borders[1][28][1] = 0.19; z_pT_Bin_Borders[1][28][2] = 0.99; z_pT_Bin_Borders[1][28][3] = 0.75;
Phi_h_Bin_Values[1][28][0] =  1; Phi_h_Bin_Values[1][28][1] = 602; Phi_h_Bin_Values[1][28][2] = 602;
z_pT_Bin_Borders[1][29][0] = 0.19; z_pT_Bin_Borders[1][29][1] = 0.16; z_pT_Bin_Borders[1][29][2] = 0.22; z_pT_Bin_Borders[1][29][3] = 0.05;
Phi_h_Bin_Values[1][29][0] =  24; Phi_h_Bin_Values[1][29][1] = 603; Phi_h_Bin_Values[1][29][2] = 603;
z_pT_Bin_Borders[1][30][0] = 0.19; z_pT_Bin_Borders[1][30][1] = 0.16; z_pT_Bin_Borders[1][30][2] = 0.32; z_pT_Bin_Borders[1][30][3] = 0.22;
Phi_h_Bin_Values[1][30][0] =  24; Phi_h_Bin_Values[1][30][1] = 627; Phi_h_Bin_Values[1][30][2] = 627;
z_pT_Bin_Borders[1][31][0] = 0.19; z_pT_Bin_Borders[1][31][1] = 0.16; z_pT_Bin_Borders[1][31][2] = 0.42; z_pT_Bin_Borders[1][31][3] = 0.32;
Phi_h_Bin_Values[1][31][0] =  24; Phi_h_Bin_Values[1][31][1] = 651; Phi_h_Bin_Values[1][31][2] = 651;
z_pT_Bin_Borders[1][32][0] = 0.19; z_pT_Bin_Borders[1][32][1] = 0.16; z_pT_Bin_Borders[1][32][2] = 0.52; z_pT_Bin_Borders[1][32][3] = 0.42;
Phi_h_Bin_Values[1][32][0] =  24; Phi_h_Bin_Values[1][32][1] = 675; Phi_h_Bin_Values[1][32][2] = 675;
z_pT_Bin_Borders[1][33][0] = 0.19; z_pT_Bin_Borders[1][33][1] = 0.16; z_pT_Bin_Borders[1][33][2] = 0.63; z_pT_Bin_Borders[1][33][3] = 0.52;
Phi_h_Bin_Values[1][33][0] =  1; Phi_h_Bin_Values[1][33][1] = 699; Phi_h_Bin_Values[1][33][2] = 699;
z_pT_Bin_Borders[1][34][0] = 0.19; z_pT_Bin_Borders[1][34][1] = 0.16; z_pT_Bin_Borders[1][34][2] = 0.75; z_pT_Bin_Borders[1][34][3] = 0.63;
Phi_h_Bin_Values[1][34][0] =  1; Phi_h_Bin_Values[1][34][1] = 700; Phi_h_Bin_Values[1][34][2] = 700;
z_pT_Bin_Borders[1][35][0] = 0.19; z_pT_Bin_Borders[1][35][1] = 0.16; z_pT_Bin_Borders[1][35][2] = 0.99; z_pT_Bin_Borders[1][35][3] = 0.75;
Phi_h_Bin_Values[1][35][0] =  1; Phi_h_Bin_Values[1][35][1] = 701; Phi_h_Bin_Values[1][35][2] = 701;
z_pT_Bin_Borders[1][36][0] = 10; z_pT_Bin_Borders[1][36][1] = 0.71; z_pT_Bin_Borders[1][36][2] = 0.05; z_pT_Bin_Borders[1][36][3] = 0;
Phi_h_Bin_Values[1][36][0] =  1; Phi_h_Bin_Values[1][36][1] = 702; Phi_h_Bin_Values[1][36][2] = 702;
z_pT_Bin_Borders[1][37][0] = 10; z_pT_Bin_Borders[1][37][1] = 0.71; z_pT_Bin_Borders[1][37][2] = 0.22; z_pT_Bin_Borders[1][37][3] = 0.05;
Phi_h_Bin_Values[1][37][0] =  1; Phi_h_Bin_Values[1][37][1] = 703; Phi_h_Bin_Values[1][37][2] = 703;
z_pT_Bin_Borders[1][38][0] = 10; z_pT_Bin_Borders[1][38][1] = 0.71; z_pT_Bin_Borders[1][38][2] = 0.32; z_pT_Bin_Borders[1][38][3] = 0.22;
Phi_h_Bin_Values[1][38][0] =  1; Phi_h_Bin_Values[1][38][1] = 704; Phi_h_Bin_Values[1][38][2] = 704;
z_pT_Bin_Borders[1][39][0] = 10; z_pT_Bin_Borders[1][39][1] = 0.71; z_pT_Bin_Borders[1][39][2] = 0.42; z_pT_Bin_Borders[1][39][3] = 0.32;
Phi_h_Bin_Values[1][39][0] =  1; Phi_h_Bin_Values[1][39][1] = 705; Phi_h_Bin_Values[1][39][2] = 705;
z_pT_Bin_Borders[1][40][0] = 10; z_pT_Bin_Borders[1][40][1] = 0.71; z_pT_Bin_Borders[1][40][2] = 0.52; z_pT_Bin_Borders[1][40][3] = 0.42;
Phi_h_Bin_Values[1][40][0] =  1; Phi_h_Bin_Values[1][40][1] = 706; Phi_h_Bin_Values[1][40][2] = 706;
z_pT_Bin_Borders[1][41][0] = 10; z_pT_Bin_Borders[1][41][1] = 0.71; z_pT_Bin_Borders[1][41][2] = 0.63; z_pT_Bin_Borders[1][41][3] = 0.52;
Phi_h_Bin_Values[1][41][0] =  1; Phi_h_Bin_Values[1][41][1] = 707; Phi_h_Bin_Values[1][41][2] = 707;
z_pT_Bin_Borders[1][42][0] = 10; z_pT_Bin_Borders[1][42][1] = 0.71; z_pT_Bin_Borders[1][42][2] = 0.75; z_pT_Bin_Borders[1][42][3] = 0.63;
Phi_h_Bin_Values[1][42][0] =  1; Phi_h_Bin_Values[1][42][1] = 708; Phi_h_Bin_Values[1][42][2] = 708;
z_pT_Bin_Borders[1][43][0] = 10; z_pT_Bin_Borders[1][43][1] = 0.71; z_pT_Bin_Borders[1][43][2] = 0.99; z_pT_Bin_Borders[1][43][3] = 0.75;
Phi_h_Bin_Values[1][43][0] =  1; Phi_h_Bin_Values[1][43][1] = 709; Phi_h_Bin_Values[1][43][2] = 709;
z_pT_Bin_Borders[1][44][0] = 10; z_pT_Bin_Borders[1][44][1] = 0.71; z_pT_Bin_Borders[1][44][2] = 10; z_pT_Bin_Borders[1][44][3] = 0.99;
Phi_h_Bin_Values[1][44][0] =  1; Phi_h_Bin_Values[1][44][1] = 710; Phi_h_Bin_Values[1][44][2] = 710;
z_pT_Bin_Borders[1][45][0] = 0.71; z_pT_Bin_Borders[1][45][1] = 0.4; z_pT_Bin_Borders[1][45][2] = 0.05; z_pT_Bin_Borders[1][45][3] = 0;
Phi_h_Bin_Values[1][45][0] =  1; Phi_h_Bin_Values[1][45][1] = 711; Phi_h_Bin_Values[1][45][2] = 711;
z_pT_Bin_Borders[1][46][0] = 0.71; z_pT_Bin_Borders[1][46][1] = 0.4; z_pT_Bin_Borders[1][46][2] = 10; z_pT_Bin_Borders[1][46][3] = 0.99;
Phi_h_Bin_Values[1][46][0] =  1; Phi_h_Bin_Values[1][46][1] = 712; Phi_h_Bin_Values[1][46][2] = 712;
z_pT_Bin_Borders[1][47][0] = 0.4; z_pT_Bin_Borders[1][47][1] = 0.29; z_pT_Bin_Borders[1][47][2] = 0.05; z_pT_Bin_Borders[1][47][3] = 0;
Phi_h_Bin_Values[1][47][0] =  1; Phi_h_Bin_Values[1][47][1] = 713; Phi_h_Bin_Values[1][47][2] = 713;
z_pT_Bin_Borders[1][48][0] = 0.4; z_pT_Bin_Borders[1][48][1] = 0.29; z_pT_Bin_Borders[1][48][2] = 10; z_pT_Bin_Borders[1][48][3] = 0.99;
Phi_h_Bin_Values[1][48][0] =  1; Phi_h_Bin_Values[1][48][1] = 714; Phi_h_Bin_Values[1][48][2] = 714;
z_pT_Bin_Borders[1][49][0] = 0.29; z_pT_Bin_Borders[1][49][1] = 0.23; z_pT_Bin_Borders[1][49][2] = 0.05; z_pT_Bin_Borders[1][49][3] = 0;
Phi_h_Bin_Values[1][49][0] =  1; Phi_h_Bin_Values[1][49][1] = 715; Phi_h_Bin_Values[1][49][2] = 715;
z_pT_Bin_Borders[1][50][0] = 0.29; z_pT_Bin_Borders[1][50][1] = 0.23; z_pT_Bin_Borders[1][50][2] = 10; z_pT_Bin_Borders[1][50][3] = 0.99;
Phi_h_Bin_Values[1][50][0] =  1; Phi_h_Bin_Values[1][50][1] = 716; Phi_h_Bin_Values[1][50][2] = 716;
z_pT_Bin_Borders[1][51][0] = 0.23; z_pT_Bin_Borders[1][51][1] = 0.19; z_pT_Bin_Borders[1][51][2] = 0.05; z_pT_Bin_Borders[1][51][3] = 0;
Phi_h_Bin_Values[1][51][0] =  1; Phi_h_Bin_Values[1][51][1] = 717; Phi_h_Bin_Values[1][51][2] = 717;
z_pT_Bin_Borders[1][52][0] = 0.23; z_pT_Bin_Borders[1][52][1] = 0.19; z_pT_Bin_Borders[1][52][2] = 10; z_pT_Bin_Borders[1][52][3] = 0.99;
Phi_h_Bin_Values[1][52][0] =  1; Phi_h_Bin_Values[1][52][1] = 718; Phi_h_Bin_Values[1][52][2] = 718;
z_pT_Bin_Borders[1][53][0] = 0.19; z_pT_Bin_Borders[1][53][1] = 0.16; z_pT_Bin_Borders[1][53][2] = 0.05; z_pT_Bin_Borders[1][53][3] = 0;
Phi_h_Bin_Values[1][53][0] =  1; Phi_h_Bin_Values[1][53][1] = 719; Phi_h_Bin_Values[1][53][2] = 719;
z_pT_Bin_Borders[1][54][0] = 0.19; z_pT_Bin_Borders[1][54][1] = 0.16; z_pT_Bin_Borders[1][54][2] = 10; z_pT_Bin_Borders[1][54][3] = 0.99;
Phi_h_Bin_Values[1][54][0] =  1; Phi_h_Bin_Values[1][54][1] = 720; Phi_h_Bin_Values[1][54][2] = 720;
z_pT_Bin_Borders[1][55][0] = 0.16; z_pT_Bin_Borders[1][55][1] = 0; z_pT_Bin_Borders[1][55][2] = 0.05; z_pT_Bin_Borders[1][55][3] = 0;
Phi_h_Bin_Values[1][55][0] =  1; Phi_h_Bin_Values[1][55][1] = 721; Phi_h_Bin_Values[1][55][2] = 721;
z_pT_Bin_Borders[1][56][0] = 0.16; z_pT_Bin_Borders[1][56][1] = 0; z_pT_Bin_Borders[1][56][2] = 0.22; z_pT_Bin_Borders[1][56][3] = 0.05;
Phi_h_Bin_Values[1][56][0] =  1; Phi_h_Bin_Values[1][56][1] = 722; Phi_h_Bin_Values[1][56][2] = 722;
z_pT_Bin_Borders[1][57][0] = 0.16; z_pT_Bin_Borders[1][57][1] = 0; z_pT_Bin_Borders[1][57][2] = 0.32; z_pT_Bin_Borders[1][57][3] = 0.22;
Phi_h_Bin_Values[1][57][0] =  1; Phi_h_Bin_Values[1][57][1] = 723; Phi_h_Bin_Values[1][57][2] = 723;
z_pT_Bin_Borders[1][58][0] = 0.16; z_pT_Bin_Borders[1][58][1] = 0; z_pT_Bin_Borders[1][58][2] = 0.42; z_pT_Bin_Borders[1][58][3] = 0.32;
Phi_h_Bin_Values[1][58][0] =  1; Phi_h_Bin_Values[1][58][1] = 724; Phi_h_Bin_Values[1][58][2] = 724;
z_pT_Bin_Borders[1][59][0] = 0.16; z_pT_Bin_Borders[1][59][1] = 0; z_pT_Bin_Borders[1][59][2] = 0.52; z_pT_Bin_Borders[1][59][3] = 0.42;
Phi_h_Bin_Values[1][59][0] =  1; Phi_h_Bin_Values[1][59][1] = 725; Phi_h_Bin_Values[1][59][2] = 725;
z_pT_Bin_Borders[1][60][0] = 0.16; z_pT_Bin_Borders[1][60][1] = 0; z_pT_Bin_Borders[1][60][2] = 0.63; z_pT_Bin_Borders[1][60][3] = 0.52;
Phi_h_Bin_Values[1][60][0] =  1; Phi_h_Bin_Values[1][60][1] = 726; Phi_h_Bin_Values[1][60][2] = 726;
z_pT_Bin_Borders[1][61][0] = 0.16; z_pT_Bin_Borders[1][61][1] = 0; z_pT_Bin_Borders[1][61][2] = 0.75; z_pT_Bin_Borders[1][61][3] = 0.63;
Phi_h_Bin_Values[1][61][0] =  1; Phi_h_Bin_Values[1][61][1] = 727; Phi_h_Bin_Values[1][61][2] = 727;
z_pT_Bin_Borders[1][62][0] = 0.16; z_pT_Bin_Borders[1][62][1] = 0; z_pT_Bin_Borders[1][62][2] = 0.99; z_pT_Bin_Borders[1][62][3] = 0.75;
Phi_h_Bin_Values[1][62][0] =  1; Phi_h_Bin_Values[1][62][1] = 728; Phi_h_Bin_Values[1][62][2] = 728;
z_pT_Bin_Borders[1][63][0] = 0.16; z_pT_Bin_Borders[1][63][1] = 0; z_pT_Bin_Borders[1][63][2] = 10; z_pT_Bin_Borders[1][63][3] = 0.99;
Phi_h_Bin_Values[1][63][0] =  1; Phi_h_Bin_Values[1][63][1] = 729; Phi_h_Bin_Values[1][63][2] = 729;
z_pT_Bin_Borders[2][1][0] = 0.75; z_pT_Bin_Borders[2][1][1] = 0.5; z_pT_Bin_Borders[2][1][2] = 0.25; z_pT_Bin_Borders[2][1][3] = 0.05;
Phi_h_Bin_Values[2][1][0] =  24; Phi_h_Bin_Values[2][1][1] = 0; Phi_h_Bin_Values[2][1][2] = 730;
z_pT_Bin_Borders[2][2][0] = 0.75; z_pT_Bin_Borders[2][2][1] = 0.5; z_pT_Bin_Borders[2][2][2] = 0.35; z_pT_Bin_Borders[2][2][3] = 0.25;
Phi_h_Bin_Values[2][2][0] =  24; Phi_h_Bin_Values[2][2][1] = 24; Phi_h_Bin_Values[2][2][2] = 754;
z_pT_Bin_Borders[2][3][0] = 0.75; z_pT_Bin_Borders[2][3][1] = 0.5; z_pT_Bin_Borders[2][3][2] = 0.45; z_pT_Bin_Borders[2][3][3] = 0.35;
Phi_h_Bin_Values[2][3][0] =  24; Phi_h_Bin_Values[2][3][1] = 48; Phi_h_Bin_Values[2][3][2] = 778;
z_pT_Bin_Borders[2][4][0] = 0.75; z_pT_Bin_Borders[2][4][1] = 0.5; z_pT_Bin_Borders[2][4][2] = 0.54; z_pT_Bin_Borders[2][4][3] = 0.45;
Phi_h_Bin_Values[2][4][0] =  24; Phi_h_Bin_Values[2][4][1] = 72; Phi_h_Bin_Values[2][4][2] = 802;
z_pT_Bin_Borders[2][5][0] = 0.75; z_pT_Bin_Borders[2][5][1] = 0.5; z_pT_Bin_Borders[2][5][2] = 0.67; z_pT_Bin_Borders[2][5][3] = 0.54;
Phi_h_Bin_Values[2][5][0] =  24; Phi_h_Bin_Values[2][5][1] = 96; Phi_h_Bin_Values[2][5][2] = 826;
z_pT_Bin_Borders[2][6][0] = 0.75; z_pT_Bin_Borders[2][6][1] = 0.5; z_pT_Bin_Borders[2][6][2] = 0.93; z_pT_Bin_Borders[2][6][3] = 0.67;
Phi_h_Bin_Values[2][6][0] =  24; Phi_h_Bin_Values[2][6][1] = 120; Phi_h_Bin_Values[2][6][2] = 850;
z_pT_Bin_Borders[2][7][0] = 0.5; z_pT_Bin_Borders[2][7][1] = 0.38; z_pT_Bin_Borders[2][7][2] = 0.25; z_pT_Bin_Borders[2][7][3] = 0.05;
Phi_h_Bin_Values[2][7][0] =  24; Phi_h_Bin_Values[2][7][1] = 144; Phi_h_Bin_Values[2][7][2] = 874;
z_pT_Bin_Borders[2][8][0] = 0.5; z_pT_Bin_Borders[2][8][1] = 0.38; z_pT_Bin_Borders[2][8][2] = 0.35; z_pT_Bin_Borders[2][8][3] = 0.25;
Phi_h_Bin_Values[2][8][0] =  24; Phi_h_Bin_Values[2][8][1] = 168; Phi_h_Bin_Values[2][8][2] = 898;
z_pT_Bin_Borders[2][9][0] = 0.5; z_pT_Bin_Borders[2][9][1] = 0.38; z_pT_Bin_Borders[2][9][2] = 0.45; z_pT_Bin_Borders[2][9][3] = 0.35;
Phi_h_Bin_Values[2][9][0] =  24; Phi_h_Bin_Values[2][9][1] = 192; Phi_h_Bin_Values[2][9][2] = 922;
z_pT_Bin_Borders[2][10][0] = 0.5; z_pT_Bin_Borders[2][10][1] = 0.38; z_pT_Bin_Borders[2][10][2] = 0.54; z_pT_Bin_Borders[2][10][3] = 0.45;
Phi_h_Bin_Values[2][10][0] =  24; Phi_h_Bin_Values[2][10][1] = 216; Phi_h_Bin_Values[2][10][2] = 946;
z_pT_Bin_Borders[2][11][0] = 0.5; z_pT_Bin_Borders[2][11][1] = 0.38; z_pT_Bin_Borders[2][11][2] = 0.67; z_pT_Bin_Borders[2][11][3] = 0.54;
Phi_h_Bin_Values[2][11][0] =  24; Phi_h_Bin_Values[2][11][1] = 240; Phi_h_Bin_Values[2][11][2] = 970;
z_pT_Bin_Borders[2][12][0] = 0.5; z_pT_Bin_Borders[2][12][1] = 0.38; z_pT_Bin_Borders[2][12][2] = 0.93; z_pT_Bin_Borders[2][12][3] = 0.67;
Phi_h_Bin_Values[2][12][0] =  24; Phi_h_Bin_Values[2][12][1] = 264; Phi_h_Bin_Values[2][12][2] = 994;
z_pT_Bin_Borders[2][13][0] = 0.38; z_pT_Bin_Borders[2][13][1] = 0.31; z_pT_Bin_Borders[2][13][2] = 0.25; z_pT_Bin_Borders[2][13][3] = 0.05;
Phi_h_Bin_Values[2][13][0] =  24; Phi_h_Bin_Values[2][13][1] = 288; Phi_h_Bin_Values[2][13][2] = 1018;
z_pT_Bin_Borders[2][14][0] = 0.38; z_pT_Bin_Borders[2][14][1] = 0.31; z_pT_Bin_Borders[2][14][2] = 0.35; z_pT_Bin_Borders[2][14][3] = 0.25;
Phi_h_Bin_Values[2][14][0] =  24; Phi_h_Bin_Values[2][14][1] = 312; Phi_h_Bin_Values[2][14][2] = 1042;
z_pT_Bin_Borders[2][15][0] = 0.38; z_pT_Bin_Borders[2][15][1] = 0.31; z_pT_Bin_Borders[2][15][2] = 0.45; z_pT_Bin_Borders[2][15][3] = 0.35;
Phi_h_Bin_Values[2][15][0] =  24; Phi_h_Bin_Values[2][15][1] = 336; Phi_h_Bin_Values[2][15][2] = 1066;
z_pT_Bin_Borders[2][16][0] = 0.38; z_pT_Bin_Borders[2][16][1] = 0.31; z_pT_Bin_Borders[2][16][2] = 0.54; z_pT_Bin_Borders[2][16][3] = 0.45;
Phi_h_Bin_Values[2][16][0] =  24; Phi_h_Bin_Values[2][16][1] = 360; Phi_h_Bin_Values[2][16][2] = 1090;
z_pT_Bin_Borders[2][17][0] = 0.38; z_pT_Bin_Borders[2][17][1] = 0.31; z_pT_Bin_Borders[2][17][2] = 0.67; z_pT_Bin_Borders[2][17][3] = 0.54;
Phi_h_Bin_Values[2][17][0] =  24; Phi_h_Bin_Values[2][17][1] = 384; Phi_h_Bin_Values[2][17][2] = 1114;
z_pT_Bin_Borders[2][18][0] = 0.38; z_pT_Bin_Borders[2][18][1] = 0.31; z_pT_Bin_Borders[2][18][2] = 0.93; z_pT_Bin_Borders[2][18][3] = 0.67;
Phi_h_Bin_Values[2][18][0] =  24; Phi_h_Bin_Values[2][18][1] = 408; Phi_h_Bin_Values[2][18][2] = 1138;
z_pT_Bin_Borders[2][19][0] = 0.31; z_pT_Bin_Borders[2][19][1] = 0.26; z_pT_Bin_Borders[2][19][2] = 0.25; z_pT_Bin_Borders[2][19][3] = 0.05;
Phi_h_Bin_Values[2][19][0] =  24; Phi_h_Bin_Values[2][19][1] = 432; Phi_h_Bin_Values[2][19][2] = 1162;
z_pT_Bin_Borders[2][20][0] = 0.31; z_pT_Bin_Borders[2][20][1] = 0.26; z_pT_Bin_Borders[2][20][2] = 0.35; z_pT_Bin_Borders[2][20][3] = 0.25;
Phi_h_Bin_Values[2][20][0] =  24; Phi_h_Bin_Values[2][20][1] = 456; Phi_h_Bin_Values[2][20][2] = 1186;
z_pT_Bin_Borders[2][21][0] = 0.31; z_pT_Bin_Borders[2][21][1] = 0.26; z_pT_Bin_Borders[2][21][2] = 0.45; z_pT_Bin_Borders[2][21][3] = 0.35;
Phi_h_Bin_Values[2][21][0] =  24; Phi_h_Bin_Values[2][21][1] = 480; Phi_h_Bin_Values[2][21][2] = 1210;
z_pT_Bin_Borders[2][22][0] = 0.31; z_pT_Bin_Borders[2][22][1] = 0.26; z_pT_Bin_Borders[2][22][2] = 0.54; z_pT_Bin_Borders[2][22][3] = 0.45;
Phi_h_Bin_Values[2][22][0] =  24; Phi_h_Bin_Values[2][22][1] = 504; Phi_h_Bin_Values[2][22][2] = 1234;
z_pT_Bin_Borders[2][23][0] = 0.31; z_pT_Bin_Borders[2][23][1] = 0.26; z_pT_Bin_Borders[2][23][2] = 0.67; z_pT_Bin_Borders[2][23][3] = 0.54;
Phi_h_Bin_Values[2][23][0] =  24; Phi_h_Bin_Values[2][23][1] = 528; Phi_h_Bin_Values[2][23][2] = 1258;
z_pT_Bin_Borders[2][24][0] = 0.31; z_pT_Bin_Borders[2][24][1] = 0.26; z_pT_Bin_Borders[2][24][2] = 0.93; z_pT_Bin_Borders[2][24][3] = 0.67;
Phi_h_Bin_Values[2][24][0] =  1; Phi_h_Bin_Values[2][24][1] = 552; Phi_h_Bin_Values[2][24][2] = 1282;
z_pT_Bin_Borders[2][25][0] = 0.26; z_pT_Bin_Borders[2][25][1] = 0.23; z_pT_Bin_Borders[2][25][2] = 0.25; z_pT_Bin_Borders[2][25][3] = 0.05;
Phi_h_Bin_Values[2][25][0] =  24; Phi_h_Bin_Values[2][25][1] = 553; Phi_h_Bin_Values[2][25][2] = 1283;
z_pT_Bin_Borders[2][26][0] = 0.26; z_pT_Bin_Borders[2][26][1] = 0.23; z_pT_Bin_Borders[2][26][2] = 0.35; z_pT_Bin_Borders[2][26][3] = 0.25;
Phi_h_Bin_Values[2][26][0] =  24; Phi_h_Bin_Values[2][26][1] = 577; Phi_h_Bin_Values[2][26][2] = 1307;
z_pT_Bin_Borders[2][27][0] = 0.26; z_pT_Bin_Borders[2][27][1] = 0.23; z_pT_Bin_Borders[2][27][2] = 0.45; z_pT_Bin_Borders[2][27][3] = 0.35;
Phi_h_Bin_Values[2][27][0] =  24; Phi_h_Bin_Values[2][27][1] = 601; Phi_h_Bin_Values[2][27][2] = 1331;
z_pT_Bin_Borders[2][28][0] = 0.26; z_pT_Bin_Borders[2][28][1] = 0.23; z_pT_Bin_Borders[2][28][2] = 0.54; z_pT_Bin_Borders[2][28][3] = 0.45;
Phi_h_Bin_Values[2][28][0] =  24; Phi_h_Bin_Values[2][28][1] = 625; Phi_h_Bin_Values[2][28][2] = 1355;
z_pT_Bin_Borders[2][29][0] = 0.26; z_pT_Bin_Borders[2][29][1] = 0.23; z_pT_Bin_Borders[2][29][2] = 0.67; z_pT_Bin_Borders[2][29][3] = 0.54;
Phi_h_Bin_Values[2][29][0] =  24; Phi_h_Bin_Values[2][29][1] = 649; Phi_h_Bin_Values[2][29][2] = 1379;
z_pT_Bin_Borders[2][30][0] = 0.26; z_pT_Bin_Borders[2][30][1] = 0.23; z_pT_Bin_Borders[2][30][2] = 0.93; z_pT_Bin_Borders[2][30][3] = 0.67;
Phi_h_Bin_Values[2][30][0] =  1; Phi_h_Bin_Values[2][30][1] = 673; Phi_h_Bin_Values[2][30][2] = 1403;
z_pT_Bin_Borders[2][31][0] = 0.23; z_pT_Bin_Borders[2][31][1] = 0.19; z_pT_Bin_Borders[2][31][2] = 0.25; z_pT_Bin_Borders[2][31][3] = 0.05;
Phi_h_Bin_Values[2][31][0] =  24; Phi_h_Bin_Values[2][31][1] = 674; Phi_h_Bin_Values[2][31][2] = 1404;
z_pT_Bin_Borders[2][32][0] = 0.23; z_pT_Bin_Borders[2][32][1] = 0.19; z_pT_Bin_Borders[2][32][2] = 0.35; z_pT_Bin_Borders[2][32][3] = 0.25;
Phi_h_Bin_Values[2][32][0] =  24; Phi_h_Bin_Values[2][32][1] = 698; Phi_h_Bin_Values[2][32][2] = 1428;
z_pT_Bin_Borders[2][33][0] = 0.23; z_pT_Bin_Borders[2][33][1] = 0.19; z_pT_Bin_Borders[2][33][2] = 0.45; z_pT_Bin_Borders[2][33][3] = 0.35;
Phi_h_Bin_Values[2][33][0] =  24; Phi_h_Bin_Values[2][33][1] = 722; Phi_h_Bin_Values[2][33][2] = 1452;
z_pT_Bin_Borders[2][34][0] = 0.23; z_pT_Bin_Borders[2][34][1] = 0.19; z_pT_Bin_Borders[2][34][2] = 0.54; z_pT_Bin_Borders[2][34][3] = 0.45;
Phi_h_Bin_Values[2][34][0] =  24; Phi_h_Bin_Values[2][34][1] = 746; Phi_h_Bin_Values[2][34][2] = 1476;
z_pT_Bin_Borders[2][35][0] = 0.23; z_pT_Bin_Borders[2][35][1] = 0.19; z_pT_Bin_Borders[2][35][2] = 0.67; z_pT_Bin_Borders[2][35][3] = 0.54;
Phi_h_Bin_Values[2][35][0] =  1; Phi_h_Bin_Values[2][35][1] = 770; Phi_h_Bin_Values[2][35][2] = 1500;
z_pT_Bin_Borders[2][36][0] = 0.23; z_pT_Bin_Borders[2][36][1] = 0.19; z_pT_Bin_Borders[2][36][2] = 0.93; z_pT_Bin_Borders[2][36][3] = 0.67;
Phi_h_Bin_Values[2][36][0] =  1; Phi_h_Bin_Values[2][36][1] = 771; Phi_h_Bin_Values[2][36][2] = 1501;
z_pT_Bin_Borders[2][37][0] = 10; z_pT_Bin_Borders[2][37][1] = 0.75; z_pT_Bin_Borders[2][37][2] = 0.05; z_pT_Bin_Borders[2][37][3] = 0;
Phi_h_Bin_Values[2][37][0] =  1; Phi_h_Bin_Values[2][37][1] = 772; Phi_h_Bin_Values[2][37][2] = 1502;
z_pT_Bin_Borders[2][38][0] = 10; z_pT_Bin_Borders[2][38][1] = 0.75; z_pT_Bin_Borders[2][38][2] = 0.25; z_pT_Bin_Borders[2][38][3] = 0.05;
Phi_h_Bin_Values[2][38][0] =  1; Phi_h_Bin_Values[2][38][1] = 773; Phi_h_Bin_Values[2][38][2] = 1503;
z_pT_Bin_Borders[2][39][0] = 10; z_pT_Bin_Borders[2][39][1] = 0.75; z_pT_Bin_Borders[2][39][2] = 0.35; z_pT_Bin_Borders[2][39][3] = 0.25;
Phi_h_Bin_Values[2][39][0] =  1; Phi_h_Bin_Values[2][39][1] = 774; Phi_h_Bin_Values[2][39][2] = 1504;
z_pT_Bin_Borders[2][40][0] = 10; z_pT_Bin_Borders[2][40][1] = 0.75; z_pT_Bin_Borders[2][40][2] = 0.45; z_pT_Bin_Borders[2][40][3] = 0.35;
Phi_h_Bin_Values[2][40][0] =  1; Phi_h_Bin_Values[2][40][1] = 775; Phi_h_Bin_Values[2][40][2] = 1505;
z_pT_Bin_Borders[2][41][0] = 10; z_pT_Bin_Borders[2][41][1] = 0.75; z_pT_Bin_Borders[2][41][2] = 0.54; z_pT_Bin_Borders[2][41][3] = 0.45;
Phi_h_Bin_Values[2][41][0] =  1; Phi_h_Bin_Values[2][41][1] = 776; Phi_h_Bin_Values[2][41][2] = 1506;
z_pT_Bin_Borders[2][42][0] = 10; z_pT_Bin_Borders[2][42][1] = 0.75; z_pT_Bin_Borders[2][42][2] = 0.67; z_pT_Bin_Borders[2][42][3] = 0.54;
Phi_h_Bin_Values[2][42][0] =  1; Phi_h_Bin_Values[2][42][1] = 777; Phi_h_Bin_Values[2][42][2] = 1507;
z_pT_Bin_Borders[2][43][0] = 10; z_pT_Bin_Borders[2][43][1] = 0.75; z_pT_Bin_Borders[2][43][2] = 0.93; z_pT_Bin_Borders[2][43][3] = 0.67;
Phi_h_Bin_Values[2][43][0] =  1; Phi_h_Bin_Values[2][43][1] = 778; Phi_h_Bin_Values[2][43][2] = 1508;
z_pT_Bin_Borders[2][44][0] = 10; z_pT_Bin_Borders[2][44][1] = 0.75; z_pT_Bin_Borders[2][44][2] = 10; z_pT_Bin_Borders[2][44][3] = 0.93;
Phi_h_Bin_Values[2][44][0] =  1; Phi_h_Bin_Values[2][44][1] = 779; Phi_h_Bin_Values[2][44][2] = 1509;
z_pT_Bin_Borders[2][45][0] = 0.75; z_pT_Bin_Borders[2][45][1] = 0.5; z_pT_Bin_Borders[2][45][2] = 0.05; z_pT_Bin_Borders[2][45][3] = 0;
Phi_h_Bin_Values[2][45][0] =  1; Phi_h_Bin_Values[2][45][1] = 780; Phi_h_Bin_Values[2][45][2] = 1510;
z_pT_Bin_Borders[2][46][0] = 0.75; z_pT_Bin_Borders[2][46][1] = 0.5; z_pT_Bin_Borders[2][46][2] = 10; z_pT_Bin_Borders[2][46][3] = 0.93;
Phi_h_Bin_Values[2][46][0] =  1; Phi_h_Bin_Values[2][46][1] = 781; Phi_h_Bin_Values[2][46][2] = 1511;
z_pT_Bin_Borders[2][47][0] = 0.5; z_pT_Bin_Borders[2][47][1] = 0.38; z_pT_Bin_Borders[2][47][2] = 0.05; z_pT_Bin_Borders[2][47][3] = 0;
Phi_h_Bin_Values[2][47][0] =  1; Phi_h_Bin_Values[2][47][1] = 782; Phi_h_Bin_Values[2][47][2] = 1512;
z_pT_Bin_Borders[2][48][0] = 0.5; z_pT_Bin_Borders[2][48][1] = 0.38; z_pT_Bin_Borders[2][48][2] = 10; z_pT_Bin_Borders[2][48][3] = 0.93;
Phi_h_Bin_Values[2][48][0] =  1; Phi_h_Bin_Values[2][48][1] = 783; Phi_h_Bin_Values[2][48][2] = 1513;
z_pT_Bin_Borders[2][49][0] = 0.38; z_pT_Bin_Borders[2][49][1] = 0.31; z_pT_Bin_Borders[2][49][2] = 0.05; z_pT_Bin_Borders[2][49][3] = 0;
Phi_h_Bin_Values[2][49][0] =  1; Phi_h_Bin_Values[2][49][1] = 784; Phi_h_Bin_Values[2][49][2] = 1514;
z_pT_Bin_Borders[2][50][0] = 0.38; z_pT_Bin_Borders[2][50][1] = 0.31; z_pT_Bin_Borders[2][50][2] = 10; z_pT_Bin_Borders[2][50][3] = 0.93;
Phi_h_Bin_Values[2][50][0] =  1; Phi_h_Bin_Values[2][50][1] = 785; Phi_h_Bin_Values[2][50][2] = 1515;
z_pT_Bin_Borders[2][51][0] = 0.31; z_pT_Bin_Borders[2][51][1] = 0.26; z_pT_Bin_Borders[2][51][2] = 0.05; z_pT_Bin_Borders[2][51][3] = 0;
Phi_h_Bin_Values[2][51][0] =  1; Phi_h_Bin_Values[2][51][1] = 786; Phi_h_Bin_Values[2][51][2] = 1516;
z_pT_Bin_Borders[2][52][0] = 0.31; z_pT_Bin_Borders[2][52][1] = 0.26; z_pT_Bin_Borders[2][52][2] = 10; z_pT_Bin_Borders[2][52][3] = 0.93;
Phi_h_Bin_Values[2][52][0] =  1; Phi_h_Bin_Values[2][52][1] = 787; Phi_h_Bin_Values[2][52][2] = 1517;
z_pT_Bin_Borders[2][53][0] = 0.26; z_pT_Bin_Borders[2][53][1] = 0.23; z_pT_Bin_Borders[2][53][2] = 0.05; z_pT_Bin_Borders[2][53][3] = 0;
Phi_h_Bin_Values[2][53][0] =  1; Phi_h_Bin_Values[2][53][1] = 788; Phi_h_Bin_Values[2][53][2] = 1518;
z_pT_Bin_Borders[2][54][0] = 0.26; z_pT_Bin_Borders[2][54][1] = 0.23; z_pT_Bin_Borders[2][54][2] = 10; z_pT_Bin_Borders[2][54][3] = 0.93;
Phi_h_Bin_Values[2][54][0] =  1; Phi_h_Bin_Values[2][54][1] = 789; Phi_h_Bin_Values[2][54][2] = 1519;
z_pT_Bin_Borders[2][55][0] = 0.23; z_pT_Bin_Borders[2][55][1] = 0.19; z_pT_Bin_Borders[2][55][2] = 0.05; z_pT_Bin_Borders[2][55][3] = 0;
Phi_h_Bin_Values[2][55][0] =  1; Phi_h_Bin_Values[2][55][1] = 790; Phi_h_Bin_Values[2][55][2] = 1520;
z_pT_Bin_Borders[2][56][0] = 0.23; z_pT_Bin_Borders[2][56][1] = 0.19; z_pT_Bin_Borders[2][56][2] = 10; z_pT_Bin_Borders[2][56][3] = 0.93;
Phi_h_Bin_Values[2][56][0] =  1; Phi_h_Bin_Values[2][56][1] = 791; Phi_h_Bin_Values[2][56][2] = 1521;
z_pT_Bin_Borders[2][57][0] = 0.19; z_pT_Bin_Borders[2][57][1] = 0; z_pT_Bin_Borders[2][57][2] = 0.05; z_pT_Bin_Borders[2][57][3] = 0;
Phi_h_Bin_Values[2][57][0] =  1; Phi_h_Bin_Values[2][57][1] = 792; Phi_h_Bin_Values[2][57][2] = 1522;
z_pT_Bin_Borders[2][58][0] = 0.19; z_pT_Bin_Borders[2][58][1] = 0; z_pT_Bin_Borders[2][58][2] = 0.25; z_pT_Bin_Borders[2][58][3] = 0.05;
Phi_h_Bin_Values[2][58][0] =  1; Phi_h_Bin_Values[2][58][1] = 793; Phi_h_Bin_Values[2][58][2] = 1523;
z_pT_Bin_Borders[2][59][0] = 0.19; z_pT_Bin_Borders[2][59][1] = 0; z_pT_Bin_Borders[2][59][2] = 0.35; z_pT_Bin_Borders[2][59][3] = 0.25;
Phi_h_Bin_Values[2][59][0] =  1; Phi_h_Bin_Values[2][59][1] = 794; Phi_h_Bin_Values[2][59][2] = 1524;
z_pT_Bin_Borders[2][60][0] = 0.19; z_pT_Bin_Borders[2][60][1] = 0; z_pT_Bin_Borders[2][60][2] = 0.45; z_pT_Bin_Borders[2][60][3] = 0.35;
Phi_h_Bin_Values[2][60][0] =  1; Phi_h_Bin_Values[2][60][1] = 795; Phi_h_Bin_Values[2][60][2] = 1525;
z_pT_Bin_Borders[2][61][0] = 0.19; z_pT_Bin_Borders[2][61][1] = 0; z_pT_Bin_Borders[2][61][2] = 0.54; z_pT_Bin_Borders[2][61][3] = 0.45;
Phi_h_Bin_Values[2][61][0] =  1; Phi_h_Bin_Values[2][61][1] = 796; Phi_h_Bin_Values[2][61][2] = 1526;
z_pT_Bin_Borders[2][62][0] = 0.19; z_pT_Bin_Borders[2][62][1] = 0; z_pT_Bin_Borders[2][62][2] = 0.67; z_pT_Bin_Borders[2][62][3] = 0.54;
Phi_h_Bin_Values[2][62][0] =  1; Phi_h_Bin_Values[2][62][1] = 797; Phi_h_Bin_Values[2][62][2] = 1527;
z_pT_Bin_Borders[2][63][0] = 0.19; z_pT_Bin_Borders[2][63][1] = 0; z_pT_Bin_Borders[2][63][2] = 0.93; z_pT_Bin_Borders[2][63][3] = 0.67;
Phi_h_Bin_Values[2][63][0] =  1; Phi_h_Bin_Values[2][63][1] = 798; Phi_h_Bin_Values[2][63][2] = 1528;
z_pT_Bin_Borders[2][64][0] = 0.19; z_pT_Bin_Borders[2][64][1] = 0; z_pT_Bin_Borders[2][64][2] = 10; z_pT_Bin_Borders[2][64][3] = 0.93;
Phi_h_Bin_Values[2][64][0] =  1; Phi_h_Bin_Values[2][64][1] = 799; Phi_h_Bin_Values[2][64][2] = 1529;
z_pT_Bin_Borders[3][1][0] = 0.75; z_pT_Bin_Borders[3][1][1] = 0.56; z_pT_Bin_Borders[3][1][2] = 0.2; z_pT_Bin_Borders[3][1][3] = 0.05;
Phi_h_Bin_Values[3][1][0] =  24; Phi_h_Bin_Values[3][1][1] = 0; Phi_h_Bin_Values[3][1][2] = 1530;
z_pT_Bin_Borders[3][2][0] = 0.75; z_pT_Bin_Borders[3][2][1] = 0.56; z_pT_Bin_Borders[3][2][2] = 0.3; z_pT_Bin_Borders[3][2][3] = 0.2;
Phi_h_Bin_Values[3][2][0] =  24; Phi_h_Bin_Values[3][2][1] = 24; Phi_h_Bin_Values[3][2][2] = 1554;
z_pT_Bin_Borders[3][3][0] = 0.75; z_pT_Bin_Borders[3][3][1] = 0.56; z_pT_Bin_Borders[3][3][2] = 0.39; z_pT_Bin_Borders[3][3][3] = 0.3;
Phi_h_Bin_Values[3][3][0] =  24; Phi_h_Bin_Values[3][3][1] = 48; Phi_h_Bin_Values[3][3][2] = 1578;
z_pT_Bin_Borders[3][4][0] = 0.75; z_pT_Bin_Borders[3][4][1] = 0.56; z_pT_Bin_Borders[3][4][2] = 0.49; z_pT_Bin_Borders[3][4][3] = 0.39;
Phi_h_Bin_Values[3][4][0] =  24; Phi_h_Bin_Values[3][4][1] = 72; Phi_h_Bin_Values[3][4][2] = 1602;
z_pT_Bin_Borders[3][5][0] = 0.75; z_pT_Bin_Borders[3][5][1] = 0.56; z_pT_Bin_Borders[3][5][2] = 0.59; z_pT_Bin_Borders[3][5][3] = 0.49;
Phi_h_Bin_Values[3][5][0] =  24; Phi_h_Bin_Values[3][5][1] = 96; Phi_h_Bin_Values[3][5][2] = 1626;
z_pT_Bin_Borders[3][6][0] = 0.75; z_pT_Bin_Borders[3][6][1] = 0.56; z_pT_Bin_Borders[3][6][2] = 0.76; z_pT_Bin_Borders[3][6][3] = 0.59;
Phi_h_Bin_Values[3][6][0] =  24; Phi_h_Bin_Values[3][6][1] = 120; Phi_h_Bin_Values[3][6][2] = 1650;
z_pT_Bin_Borders[3][7][0] = 0.56; z_pT_Bin_Borders[3][7][1] = 0.41; z_pT_Bin_Borders[3][7][2] = 0.2; z_pT_Bin_Borders[3][7][3] = 0.05;
Phi_h_Bin_Values[3][7][0] =  24; Phi_h_Bin_Values[3][7][1] = 144; Phi_h_Bin_Values[3][7][2] = 1674;
z_pT_Bin_Borders[3][8][0] = 0.56; z_pT_Bin_Borders[3][8][1] = 0.41; z_pT_Bin_Borders[3][8][2] = 0.3; z_pT_Bin_Borders[3][8][3] = 0.2;
Phi_h_Bin_Values[3][8][0] =  24; Phi_h_Bin_Values[3][8][1] = 168; Phi_h_Bin_Values[3][8][2] = 1698;
z_pT_Bin_Borders[3][9][0] = 0.56; z_pT_Bin_Borders[3][9][1] = 0.41; z_pT_Bin_Borders[3][9][2] = 0.39; z_pT_Bin_Borders[3][9][3] = 0.3;
Phi_h_Bin_Values[3][9][0] =  24; Phi_h_Bin_Values[3][9][1] = 192; Phi_h_Bin_Values[3][9][2] = 1722;
z_pT_Bin_Borders[3][10][0] = 0.56; z_pT_Bin_Borders[3][10][1] = 0.41; z_pT_Bin_Borders[3][10][2] = 0.49; z_pT_Bin_Borders[3][10][3] = 0.39;
Phi_h_Bin_Values[3][10][0] =  24; Phi_h_Bin_Values[3][10][1] = 216; Phi_h_Bin_Values[3][10][2] = 1746;
z_pT_Bin_Borders[3][11][0] = 0.56; z_pT_Bin_Borders[3][11][1] = 0.41; z_pT_Bin_Borders[3][11][2] = 0.59; z_pT_Bin_Borders[3][11][3] = 0.49;
Phi_h_Bin_Values[3][11][0] =  24; Phi_h_Bin_Values[3][11][1] = 240; Phi_h_Bin_Values[3][11][2] = 1770;
z_pT_Bin_Borders[3][12][0] = 0.56; z_pT_Bin_Borders[3][12][1] = 0.41; z_pT_Bin_Borders[3][12][2] = 0.76; z_pT_Bin_Borders[3][12][3] = 0.59;
Phi_h_Bin_Values[3][12][0] =  24; Phi_h_Bin_Values[3][12][1] = 264; Phi_h_Bin_Values[3][12][2] = 1794;
z_pT_Bin_Borders[3][13][0] = 0.41; z_pT_Bin_Borders[3][13][1] = 0.33; z_pT_Bin_Borders[3][13][2] = 0.2; z_pT_Bin_Borders[3][13][3] = 0.05;
Phi_h_Bin_Values[3][13][0] =  24; Phi_h_Bin_Values[3][13][1] = 288; Phi_h_Bin_Values[3][13][2] = 1818;
z_pT_Bin_Borders[3][14][0] = 0.41; z_pT_Bin_Borders[3][14][1] = 0.33; z_pT_Bin_Borders[3][14][2] = 0.3; z_pT_Bin_Borders[3][14][3] = 0.2;
Phi_h_Bin_Values[3][14][0] =  24; Phi_h_Bin_Values[3][14][1] = 312; Phi_h_Bin_Values[3][14][2] = 1842;
z_pT_Bin_Borders[3][15][0] = 0.41; z_pT_Bin_Borders[3][15][1] = 0.33; z_pT_Bin_Borders[3][15][2] = 0.39; z_pT_Bin_Borders[3][15][3] = 0.3;
Phi_h_Bin_Values[3][15][0] =  24; Phi_h_Bin_Values[3][15][1] = 336; Phi_h_Bin_Values[3][15][2] = 1866;
z_pT_Bin_Borders[3][16][0] = 0.41; z_pT_Bin_Borders[3][16][1] = 0.33; z_pT_Bin_Borders[3][16][2] = 0.49; z_pT_Bin_Borders[3][16][3] = 0.39;
Phi_h_Bin_Values[3][16][0] =  24; Phi_h_Bin_Values[3][16][1] = 360; Phi_h_Bin_Values[3][16][2] = 1890;
z_pT_Bin_Borders[3][17][0] = 0.41; z_pT_Bin_Borders[3][17][1] = 0.33; z_pT_Bin_Borders[3][17][2] = 0.59; z_pT_Bin_Borders[3][17][3] = 0.49;
Phi_h_Bin_Values[3][17][0] =  24; Phi_h_Bin_Values[3][17][1] = 384; Phi_h_Bin_Values[3][17][2] = 1914;
z_pT_Bin_Borders[3][18][0] = 0.41; z_pT_Bin_Borders[3][18][1] = 0.33; z_pT_Bin_Borders[3][18][2] = 0.76; z_pT_Bin_Borders[3][18][3] = 0.59;
Phi_h_Bin_Values[3][18][0] =  24; Phi_h_Bin_Values[3][18][1] = 408; Phi_h_Bin_Values[3][18][2] = 1938;
z_pT_Bin_Borders[3][19][0] = 0.33; z_pT_Bin_Borders[3][19][1] = 0.28; z_pT_Bin_Borders[3][19][2] = 0.2; z_pT_Bin_Borders[3][19][3] = 0.05;
Phi_h_Bin_Values[3][19][0] =  24; Phi_h_Bin_Values[3][19][1] = 432; Phi_h_Bin_Values[3][19][2] = 1962;
z_pT_Bin_Borders[3][20][0] = 0.33; z_pT_Bin_Borders[3][20][1] = 0.28; z_pT_Bin_Borders[3][20][2] = 0.3; z_pT_Bin_Borders[3][20][3] = 0.2;
Phi_h_Bin_Values[3][20][0] =  24; Phi_h_Bin_Values[3][20][1] = 456; Phi_h_Bin_Values[3][20][2] = 1986;
z_pT_Bin_Borders[3][21][0] = 0.33; z_pT_Bin_Borders[3][21][1] = 0.28; z_pT_Bin_Borders[3][21][2] = 0.39; z_pT_Bin_Borders[3][21][3] = 0.3;
Phi_h_Bin_Values[3][21][0] =  24; Phi_h_Bin_Values[3][21][1] = 480; Phi_h_Bin_Values[3][21][2] = 2010;
z_pT_Bin_Borders[3][22][0] = 0.33; z_pT_Bin_Borders[3][22][1] = 0.28; z_pT_Bin_Borders[3][22][2] = 0.49; z_pT_Bin_Borders[3][22][3] = 0.39;
Phi_h_Bin_Values[3][22][0] =  24; Phi_h_Bin_Values[3][22][1] = 504; Phi_h_Bin_Values[3][22][2] = 2034;
z_pT_Bin_Borders[3][23][0] = 0.33; z_pT_Bin_Borders[3][23][1] = 0.28; z_pT_Bin_Borders[3][23][2] = 0.59; z_pT_Bin_Borders[3][23][3] = 0.49;
Phi_h_Bin_Values[3][23][0] =  24; Phi_h_Bin_Values[3][23][1] = 528; Phi_h_Bin_Values[3][23][2] = 2058;
z_pT_Bin_Borders[3][24][0] = 0.33; z_pT_Bin_Borders[3][24][1] = 0.28; z_pT_Bin_Borders[3][24][2] = 0.76; z_pT_Bin_Borders[3][24][3] = 0.59;
Phi_h_Bin_Values[3][24][0] =  24; Phi_h_Bin_Values[3][24][1] = 552; Phi_h_Bin_Values[3][24][2] = 2082;
z_pT_Bin_Borders[3][25][0] = 0.28; z_pT_Bin_Borders[3][25][1] = 0.22; z_pT_Bin_Borders[3][25][2] = 0.2; z_pT_Bin_Borders[3][25][3] = 0.05;
Phi_h_Bin_Values[3][25][0] =  24; Phi_h_Bin_Values[3][25][1] = 576; Phi_h_Bin_Values[3][25][2] = 2106;
z_pT_Bin_Borders[3][26][0] = 0.28; z_pT_Bin_Borders[3][26][1] = 0.22; z_pT_Bin_Borders[3][26][2] = 0.3; z_pT_Bin_Borders[3][26][3] = 0.2;
Phi_h_Bin_Values[3][26][0] =  24; Phi_h_Bin_Values[3][26][1] = 600; Phi_h_Bin_Values[3][26][2] = 2130;
z_pT_Bin_Borders[3][27][0] = 0.28; z_pT_Bin_Borders[3][27][1] = 0.22; z_pT_Bin_Borders[3][27][2] = 0.39; z_pT_Bin_Borders[3][27][3] = 0.3;
Phi_h_Bin_Values[3][27][0] =  24; Phi_h_Bin_Values[3][27][1] = 624; Phi_h_Bin_Values[3][27][2] = 2154;
z_pT_Bin_Borders[3][28][0] = 0.28; z_pT_Bin_Borders[3][28][1] = 0.22; z_pT_Bin_Borders[3][28][2] = 0.49; z_pT_Bin_Borders[3][28][3] = 0.39;
Phi_h_Bin_Values[3][28][0] =  24; Phi_h_Bin_Values[3][28][1] = 648; Phi_h_Bin_Values[3][28][2] = 2178;
z_pT_Bin_Borders[3][29][0] = 0.28; z_pT_Bin_Borders[3][29][1] = 0.22; z_pT_Bin_Borders[3][29][2] = 0.59; z_pT_Bin_Borders[3][29][3] = 0.49;
Phi_h_Bin_Values[3][29][0] =  24; Phi_h_Bin_Values[3][29][1] = 672; Phi_h_Bin_Values[3][29][2] = 2202;
z_pT_Bin_Borders[3][30][0] = 0.28; z_pT_Bin_Borders[3][30][1] = 0.22; z_pT_Bin_Borders[3][30][2] = 0.76; z_pT_Bin_Borders[3][30][3] = 0.59;
Phi_h_Bin_Values[3][30][0] =  1; Phi_h_Bin_Values[3][30][1] = 696; Phi_h_Bin_Values[3][30][2] = 2226;
z_pT_Bin_Borders[3][31][0] = 10; z_pT_Bin_Borders[3][31][1] = 0.75; z_pT_Bin_Borders[3][31][2] = 0.05; z_pT_Bin_Borders[3][31][3] = 0;
Phi_h_Bin_Values[3][31][0] =  1; Phi_h_Bin_Values[3][31][1] = 697; Phi_h_Bin_Values[3][31][2] = 2227;
z_pT_Bin_Borders[3][32][0] = 10; z_pT_Bin_Borders[3][32][1] = 0.75; z_pT_Bin_Borders[3][32][2] = 0.2; z_pT_Bin_Borders[3][32][3] = 0.05;
Phi_h_Bin_Values[3][32][0] =  1; Phi_h_Bin_Values[3][32][1] = 698; Phi_h_Bin_Values[3][32][2] = 2228;
z_pT_Bin_Borders[3][33][0] = 10; z_pT_Bin_Borders[3][33][1] = 0.75; z_pT_Bin_Borders[3][33][2] = 0.3; z_pT_Bin_Borders[3][33][3] = 0.2;
Phi_h_Bin_Values[3][33][0] =  1; Phi_h_Bin_Values[3][33][1] = 699; Phi_h_Bin_Values[3][33][2] = 2229;
z_pT_Bin_Borders[3][34][0] = 10; z_pT_Bin_Borders[3][34][1] = 0.75; z_pT_Bin_Borders[3][34][2] = 0.39; z_pT_Bin_Borders[3][34][3] = 0.3;
Phi_h_Bin_Values[3][34][0] =  1; Phi_h_Bin_Values[3][34][1] = 700; Phi_h_Bin_Values[3][34][2] = 2230;
z_pT_Bin_Borders[3][35][0] = 10; z_pT_Bin_Borders[3][35][1] = 0.75; z_pT_Bin_Borders[3][35][2] = 0.49; z_pT_Bin_Borders[3][35][3] = 0.39;
Phi_h_Bin_Values[3][35][0] =  1; Phi_h_Bin_Values[3][35][1] = 701; Phi_h_Bin_Values[3][35][2] = 2231;
z_pT_Bin_Borders[3][36][0] = 10; z_pT_Bin_Borders[3][36][1] = 0.75; z_pT_Bin_Borders[3][36][2] = 0.59; z_pT_Bin_Borders[3][36][3] = 0.49;
Phi_h_Bin_Values[3][36][0] =  1; Phi_h_Bin_Values[3][36][1] = 702; Phi_h_Bin_Values[3][36][2] = 2232;
z_pT_Bin_Borders[3][37][0] = 10; z_pT_Bin_Borders[3][37][1] = 0.75; z_pT_Bin_Borders[3][37][2] = 0.76; z_pT_Bin_Borders[3][37][3] = 0.59;
Phi_h_Bin_Values[3][37][0] =  1; Phi_h_Bin_Values[3][37][1] = 703; Phi_h_Bin_Values[3][37][2] = 2233;
z_pT_Bin_Borders[3][38][0] = 10; z_pT_Bin_Borders[3][38][1] = 0.75; z_pT_Bin_Borders[3][38][2] = 10; z_pT_Bin_Borders[3][38][3] = 0.76;
Phi_h_Bin_Values[3][38][0] =  1; Phi_h_Bin_Values[3][38][1] = 704; Phi_h_Bin_Values[3][38][2] = 2234;
z_pT_Bin_Borders[3][39][0] = 0.75; z_pT_Bin_Borders[3][39][1] = 0.56; z_pT_Bin_Borders[3][39][2] = 0.05; z_pT_Bin_Borders[3][39][3] = 0;
Phi_h_Bin_Values[3][39][0] =  1; Phi_h_Bin_Values[3][39][1] = 705; Phi_h_Bin_Values[3][39][2] = 2235;
z_pT_Bin_Borders[3][40][0] = 0.75; z_pT_Bin_Borders[3][40][1] = 0.56; z_pT_Bin_Borders[3][40][2] = 10; z_pT_Bin_Borders[3][40][3] = 0.76;
Phi_h_Bin_Values[3][40][0] =  1; Phi_h_Bin_Values[3][40][1] = 706; Phi_h_Bin_Values[3][40][2] = 2236;
z_pT_Bin_Borders[3][41][0] = 0.56; z_pT_Bin_Borders[3][41][1] = 0.41; z_pT_Bin_Borders[3][41][2] = 0.05; z_pT_Bin_Borders[3][41][3] = 0;
Phi_h_Bin_Values[3][41][0] =  1; Phi_h_Bin_Values[3][41][1] = 707; Phi_h_Bin_Values[3][41][2] = 2237;
z_pT_Bin_Borders[3][42][0] = 0.56; z_pT_Bin_Borders[3][42][1] = 0.41; z_pT_Bin_Borders[3][42][2] = 10; z_pT_Bin_Borders[3][42][3] = 0.76;
Phi_h_Bin_Values[3][42][0] =  1; Phi_h_Bin_Values[3][42][1] = 708; Phi_h_Bin_Values[3][42][2] = 2238;
z_pT_Bin_Borders[3][43][0] = 0.41; z_pT_Bin_Borders[3][43][1] = 0.33; z_pT_Bin_Borders[3][43][2] = 0.05; z_pT_Bin_Borders[3][43][3] = 0;
Phi_h_Bin_Values[3][43][0] =  1; Phi_h_Bin_Values[3][43][1] = 709; Phi_h_Bin_Values[3][43][2] = 2239;
z_pT_Bin_Borders[3][44][0] = 0.41; z_pT_Bin_Borders[3][44][1] = 0.33; z_pT_Bin_Borders[3][44][2] = 10; z_pT_Bin_Borders[3][44][3] = 0.76;
Phi_h_Bin_Values[3][44][0] =  1; Phi_h_Bin_Values[3][44][1] = 710; Phi_h_Bin_Values[3][44][2] = 2240;
z_pT_Bin_Borders[3][45][0] = 0.33; z_pT_Bin_Borders[3][45][1] = 0.28; z_pT_Bin_Borders[3][45][2] = 0.05; z_pT_Bin_Borders[3][45][3] = 0;
Phi_h_Bin_Values[3][45][0] =  1; Phi_h_Bin_Values[3][45][1] = 711; Phi_h_Bin_Values[3][45][2] = 2241;
z_pT_Bin_Borders[3][46][0] = 0.33; z_pT_Bin_Borders[3][46][1] = 0.28; z_pT_Bin_Borders[3][46][2] = 10; z_pT_Bin_Borders[3][46][3] = 0.76;
Phi_h_Bin_Values[3][46][0] =  1; Phi_h_Bin_Values[3][46][1] = 712; Phi_h_Bin_Values[3][46][2] = 2242;
z_pT_Bin_Borders[3][47][0] = 0.28; z_pT_Bin_Borders[3][47][1] = 0.22; z_pT_Bin_Borders[3][47][2] = 0.05; z_pT_Bin_Borders[3][47][3] = 0;
Phi_h_Bin_Values[3][47][0] =  1; Phi_h_Bin_Values[3][47][1] = 713; Phi_h_Bin_Values[3][47][2] = 2243;
z_pT_Bin_Borders[3][48][0] = 0.28; z_pT_Bin_Borders[3][48][1] = 0.22; z_pT_Bin_Borders[3][48][2] = 10; z_pT_Bin_Borders[3][48][3] = 0.76;
Phi_h_Bin_Values[3][48][0] =  1; Phi_h_Bin_Values[3][48][1] = 714; Phi_h_Bin_Values[3][48][2] = 2244;
z_pT_Bin_Borders[3][49][0] = 0.22; z_pT_Bin_Borders[3][49][1] = 0; z_pT_Bin_Borders[3][49][2] = 0.05; z_pT_Bin_Borders[3][49][3] = 0;
Phi_h_Bin_Values[3][49][0] =  1; Phi_h_Bin_Values[3][49][1] = 715; Phi_h_Bin_Values[3][49][2] = 2245;
z_pT_Bin_Borders[3][50][0] = 0.22; z_pT_Bin_Borders[3][50][1] = 0; z_pT_Bin_Borders[3][50][2] = 0.2; z_pT_Bin_Borders[3][50][3] = 0.05;
Phi_h_Bin_Values[3][50][0] =  1; Phi_h_Bin_Values[3][50][1] = 716; Phi_h_Bin_Values[3][50][2] = 2246;
z_pT_Bin_Borders[3][51][0] = 0.22; z_pT_Bin_Borders[3][51][1] = 0; z_pT_Bin_Borders[3][51][2] = 0.3; z_pT_Bin_Borders[3][51][3] = 0.2;
Phi_h_Bin_Values[3][51][0] =  1; Phi_h_Bin_Values[3][51][1] = 717; Phi_h_Bin_Values[3][51][2] = 2247;
z_pT_Bin_Borders[3][52][0] = 0.22; z_pT_Bin_Borders[3][52][1] = 0; z_pT_Bin_Borders[3][52][2] = 0.39; z_pT_Bin_Borders[3][52][3] = 0.3;
Phi_h_Bin_Values[3][52][0] =  1; Phi_h_Bin_Values[3][52][1] = 718; Phi_h_Bin_Values[3][52][2] = 2248;
z_pT_Bin_Borders[3][53][0] = 0.22; z_pT_Bin_Borders[3][53][1] = 0; z_pT_Bin_Borders[3][53][2] = 0.49; z_pT_Bin_Borders[3][53][3] = 0.39;
Phi_h_Bin_Values[3][53][0] =  1; Phi_h_Bin_Values[3][53][1] = 719; Phi_h_Bin_Values[3][53][2] = 2249;
z_pT_Bin_Borders[3][54][0] = 0.22; z_pT_Bin_Borders[3][54][1] = 0; z_pT_Bin_Borders[3][54][2] = 0.59; z_pT_Bin_Borders[3][54][3] = 0.49;
Phi_h_Bin_Values[3][54][0] =  1; Phi_h_Bin_Values[3][54][1] = 720; Phi_h_Bin_Values[3][54][2] = 2250;
z_pT_Bin_Borders[3][55][0] = 0.22; z_pT_Bin_Borders[3][55][1] = 0; z_pT_Bin_Borders[3][55][2] = 0.76; z_pT_Bin_Borders[3][55][3] = 0.59;
Phi_h_Bin_Values[3][55][0] =  1; Phi_h_Bin_Values[3][55][1] = 721; Phi_h_Bin_Values[3][55][2] = 2251;
z_pT_Bin_Borders[3][56][0] = 0.22; z_pT_Bin_Borders[3][56][1] = 0; z_pT_Bin_Borders[3][56][2] = 10; z_pT_Bin_Borders[3][56][3] = 0.76;
Phi_h_Bin_Values[3][56][0] =  1; Phi_h_Bin_Values[3][56][1] = 722; Phi_h_Bin_Values[3][56][2] = 2252;
z_pT_Bin_Borders[4][1][0] = 0.71; z_pT_Bin_Borders[4][1][1] = 0.59; z_pT_Bin_Borders[4][1][2] = 0.2; z_pT_Bin_Borders[4][1][3] = 0.05;
Phi_h_Bin_Values[4][1][0] =  24; Phi_h_Bin_Values[4][1][1] = 0; Phi_h_Bin_Values[4][1][2] = 2253;
z_pT_Bin_Borders[4][2][0] = 0.71; z_pT_Bin_Borders[4][2][1] = 0.59; z_pT_Bin_Borders[4][2][2] = 0.29; z_pT_Bin_Borders[4][2][3] = 0.2;
Phi_h_Bin_Values[4][2][0] =  24; Phi_h_Bin_Values[4][2][1] = 24; Phi_h_Bin_Values[4][2][2] = 2277;
z_pT_Bin_Borders[4][3][0] = 0.71; z_pT_Bin_Borders[4][3][1] = 0.59; z_pT_Bin_Borders[4][3][2] = 0.38; z_pT_Bin_Borders[4][3][3] = 0.29;
Phi_h_Bin_Values[4][3][0] =  24; Phi_h_Bin_Values[4][3][1] = 48; Phi_h_Bin_Values[4][3][2] = 2301;
z_pT_Bin_Borders[4][4][0] = 0.71; z_pT_Bin_Borders[4][4][1] = 0.59; z_pT_Bin_Borders[4][4][2] = 0.48; z_pT_Bin_Borders[4][4][3] = 0.38;
Phi_h_Bin_Values[4][4][0] =  24; Phi_h_Bin_Values[4][4][1] = 72; Phi_h_Bin_Values[4][4][2] = 2325;
z_pT_Bin_Borders[4][5][0] = 0.71; z_pT_Bin_Borders[4][5][1] = 0.59; z_pT_Bin_Borders[4][5][2] = 0.61; z_pT_Bin_Borders[4][5][3] = 0.48;
Phi_h_Bin_Values[4][5][0] =  24; Phi_h_Bin_Values[4][5][1] = 96; Phi_h_Bin_Values[4][5][2] = 2349;
z_pT_Bin_Borders[4][6][0] = 0.71; z_pT_Bin_Borders[4][6][1] = 0.59; z_pT_Bin_Borders[4][6][2] = 0.85; z_pT_Bin_Borders[4][6][3] = 0.61;
Phi_h_Bin_Values[4][6][0] =  1; Phi_h_Bin_Values[4][6][1] = 120; Phi_h_Bin_Values[4][6][2] = 2373;
z_pT_Bin_Borders[4][7][0] = 0.59; z_pT_Bin_Borders[4][7][1] = 0.5; z_pT_Bin_Borders[4][7][2] = 0.2; z_pT_Bin_Borders[4][7][3] = 0.05;
Phi_h_Bin_Values[4][7][0] =  24; Phi_h_Bin_Values[4][7][1] = 121; Phi_h_Bin_Values[4][7][2] = 2374;
z_pT_Bin_Borders[4][8][0] = 0.59; z_pT_Bin_Borders[4][8][1] = 0.5; z_pT_Bin_Borders[4][8][2] = 0.29; z_pT_Bin_Borders[4][8][3] = 0.2;
Phi_h_Bin_Values[4][8][0] =  24; Phi_h_Bin_Values[4][8][1] = 145; Phi_h_Bin_Values[4][8][2] = 2398;
z_pT_Bin_Borders[4][9][0] = 0.59; z_pT_Bin_Borders[4][9][1] = 0.5; z_pT_Bin_Borders[4][9][2] = 0.38; z_pT_Bin_Borders[4][9][3] = 0.29;
Phi_h_Bin_Values[4][9][0] =  24; Phi_h_Bin_Values[4][9][1] = 169; Phi_h_Bin_Values[4][9][2] = 2422;
z_pT_Bin_Borders[4][10][0] = 0.59; z_pT_Bin_Borders[4][10][1] = 0.5; z_pT_Bin_Borders[4][10][2] = 0.48; z_pT_Bin_Borders[4][10][3] = 0.38;
Phi_h_Bin_Values[4][10][0] =  24; Phi_h_Bin_Values[4][10][1] = 193; Phi_h_Bin_Values[4][10][2] = 2446;
z_pT_Bin_Borders[4][11][0] = 0.59; z_pT_Bin_Borders[4][11][1] = 0.5; z_pT_Bin_Borders[4][11][2] = 0.61; z_pT_Bin_Borders[4][11][3] = 0.48;
Phi_h_Bin_Values[4][11][0] =  24; Phi_h_Bin_Values[4][11][1] = 217; Phi_h_Bin_Values[4][11][2] = 2470;
z_pT_Bin_Borders[4][12][0] = 0.59; z_pT_Bin_Borders[4][12][1] = 0.5; z_pT_Bin_Borders[4][12][2] = 0.85; z_pT_Bin_Borders[4][12][3] = 0.61;
Phi_h_Bin_Values[4][12][0] =  24; Phi_h_Bin_Values[4][12][1] = 241; Phi_h_Bin_Values[4][12][2] = 2494;
z_pT_Bin_Borders[4][13][0] = 0.5; z_pT_Bin_Borders[4][13][1] = 0.43; z_pT_Bin_Borders[4][13][2] = 0.2; z_pT_Bin_Borders[4][13][3] = 0.05;
Phi_h_Bin_Values[4][13][0] =  24; Phi_h_Bin_Values[4][13][1] = 265; Phi_h_Bin_Values[4][13][2] = 2518;
z_pT_Bin_Borders[4][14][0] = 0.5; z_pT_Bin_Borders[4][14][1] = 0.43; z_pT_Bin_Borders[4][14][2] = 0.29; z_pT_Bin_Borders[4][14][3] = 0.2;
Phi_h_Bin_Values[4][14][0] =  24; Phi_h_Bin_Values[4][14][1] = 289; Phi_h_Bin_Values[4][14][2] = 2542;
z_pT_Bin_Borders[4][15][0] = 0.5; z_pT_Bin_Borders[4][15][1] = 0.43; z_pT_Bin_Borders[4][15][2] = 0.38; z_pT_Bin_Borders[4][15][3] = 0.29;
Phi_h_Bin_Values[4][15][0] =  24; Phi_h_Bin_Values[4][15][1] = 313; Phi_h_Bin_Values[4][15][2] = 2566;
z_pT_Bin_Borders[4][16][0] = 0.5; z_pT_Bin_Borders[4][16][1] = 0.43; z_pT_Bin_Borders[4][16][2] = 0.48; z_pT_Bin_Borders[4][16][3] = 0.38;
Phi_h_Bin_Values[4][16][0] =  24; Phi_h_Bin_Values[4][16][1] = 337; Phi_h_Bin_Values[4][16][2] = 2590;
z_pT_Bin_Borders[4][17][0] = 0.5; z_pT_Bin_Borders[4][17][1] = 0.43; z_pT_Bin_Borders[4][17][2] = 0.61; z_pT_Bin_Borders[4][17][3] = 0.48;
Phi_h_Bin_Values[4][17][0] =  24; Phi_h_Bin_Values[4][17][1] = 361; Phi_h_Bin_Values[4][17][2] = 2614;
z_pT_Bin_Borders[4][18][0] = 0.5; z_pT_Bin_Borders[4][18][1] = 0.43; z_pT_Bin_Borders[4][18][2] = 0.85; z_pT_Bin_Borders[4][18][3] = 0.61;
Phi_h_Bin_Values[4][18][0] =  24; Phi_h_Bin_Values[4][18][1] = 385; Phi_h_Bin_Values[4][18][2] = 2638;
z_pT_Bin_Borders[4][19][0] = 0.43; z_pT_Bin_Borders[4][19][1] = 0.38; z_pT_Bin_Borders[4][19][2] = 0.2; z_pT_Bin_Borders[4][19][3] = 0.05;
Phi_h_Bin_Values[4][19][0] =  24; Phi_h_Bin_Values[4][19][1] = 409; Phi_h_Bin_Values[4][19][2] = 2662;
z_pT_Bin_Borders[4][20][0] = 0.43; z_pT_Bin_Borders[4][20][1] = 0.38; z_pT_Bin_Borders[4][20][2] = 0.29; z_pT_Bin_Borders[4][20][3] = 0.2;
Phi_h_Bin_Values[4][20][0] =  24; Phi_h_Bin_Values[4][20][1] = 433; Phi_h_Bin_Values[4][20][2] = 2686;
z_pT_Bin_Borders[4][21][0] = 0.43; z_pT_Bin_Borders[4][21][1] = 0.38; z_pT_Bin_Borders[4][21][2] = 0.38; z_pT_Bin_Borders[4][21][3] = 0.29;
Phi_h_Bin_Values[4][21][0] =  24; Phi_h_Bin_Values[4][21][1] = 457; Phi_h_Bin_Values[4][21][2] = 2710;
z_pT_Bin_Borders[4][22][0] = 0.43; z_pT_Bin_Borders[4][22][1] = 0.38; z_pT_Bin_Borders[4][22][2] = 0.48; z_pT_Bin_Borders[4][22][3] = 0.38;
Phi_h_Bin_Values[4][22][0] =  24; Phi_h_Bin_Values[4][22][1] = 481; Phi_h_Bin_Values[4][22][2] = 2734;
z_pT_Bin_Borders[4][23][0] = 0.43; z_pT_Bin_Borders[4][23][1] = 0.38; z_pT_Bin_Borders[4][23][2] = 0.61; z_pT_Bin_Borders[4][23][3] = 0.48;
Phi_h_Bin_Values[4][23][0] =  24; Phi_h_Bin_Values[4][23][1] = 505; Phi_h_Bin_Values[4][23][2] = 2758;
z_pT_Bin_Borders[4][24][0] = 0.43; z_pT_Bin_Borders[4][24][1] = 0.38; z_pT_Bin_Borders[4][24][2] = 0.85; z_pT_Bin_Borders[4][24][3] = 0.61;
Phi_h_Bin_Values[4][24][0] =  24; Phi_h_Bin_Values[4][24][1] = 529; Phi_h_Bin_Values[4][24][2] = 2782;
z_pT_Bin_Borders[4][25][0] = 0.38; z_pT_Bin_Borders[4][25][1] = 0.33; z_pT_Bin_Borders[4][25][2] = 0.2; z_pT_Bin_Borders[4][25][3] = 0.05;
Phi_h_Bin_Values[4][25][0] =  24; Phi_h_Bin_Values[4][25][1] = 553; Phi_h_Bin_Values[4][25][2] = 2806;
z_pT_Bin_Borders[4][26][0] = 0.38; z_pT_Bin_Borders[4][26][1] = 0.33; z_pT_Bin_Borders[4][26][2] = 0.29; z_pT_Bin_Borders[4][26][3] = 0.2;
Phi_h_Bin_Values[4][26][0] =  24; Phi_h_Bin_Values[4][26][1] = 577; Phi_h_Bin_Values[4][26][2] = 2830;
z_pT_Bin_Borders[4][27][0] = 0.38; z_pT_Bin_Borders[4][27][1] = 0.33; z_pT_Bin_Borders[4][27][2] = 0.38; z_pT_Bin_Borders[4][27][3] = 0.29;
Phi_h_Bin_Values[4][27][0] =  24; Phi_h_Bin_Values[4][27][1] = 601; Phi_h_Bin_Values[4][27][2] = 2854;
z_pT_Bin_Borders[4][28][0] = 0.38; z_pT_Bin_Borders[4][28][1] = 0.33; z_pT_Bin_Borders[4][28][2] = 0.48; z_pT_Bin_Borders[4][28][3] = 0.38;
Phi_h_Bin_Values[4][28][0] =  24; Phi_h_Bin_Values[4][28][1] = 625; Phi_h_Bin_Values[4][28][2] = 2878;
z_pT_Bin_Borders[4][29][0] = 0.38; z_pT_Bin_Borders[4][29][1] = 0.33; z_pT_Bin_Borders[4][29][2] = 0.61; z_pT_Bin_Borders[4][29][3] = 0.48;
Phi_h_Bin_Values[4][29][0] =  24; Phi_h_Bin_Values[4][29][1] = 649; Phi_h_Bin_Values[4][29][2] = 2902;
z_pT_Bin_Borders[4][30][0] = 0.38; z_pT_Bin_Borders[4][30][1] = 0.33; z_pT_Bin_Borders[4][30][2] = 0.85; z_pT_Bin_Borders[4][30][3] = 0.61;
Phi_h_Bin_Values[4][30][0] =  1; Phi_h_Bin_Values[4][30][1] = 673; Phi_h_Bin_Values[4][30][2] = 2926;
z_pT_Bin_Borders[4][31][0] = 0.33; z_pT_Bin_Borders[4][31][1] = 0.26; z_pT_Bin_Borders[4][31][2] = 0.2; z_pT_Bin_Borders[4][31][3] = 0.05;
Phi_h_Bin_Values[4][31][0] =  24; Phi_h_Bin_Values[4][31][1] = 674; Phi_h_Bin_Values[4][31][2] = 2927;
z_pT_Bin_Borders[4][32][0] = 0.33; z_pT_Bin_Borders[4][32][1] = 0.26; z_pT_Bin_Borders[4][32][2] = 0.29; z_pT_Bin_Borders[4][32][3] = 0.2;
Phi_h_Bin_Values[4][32][0] =  24; Phi_h_Bin_Values[4][32][1] = 698; Phi_h_Bin_Values[4][32][2] = 2951;
z_pT_Bin_Borders[4][33][0] = 0.33; z_pT_Bin_Borders[4][33][1] = 0.26; z_pT_Bin_Borders[4][33][2] = 0.38; z_pT_Bin_Borders[4][33][3] = 0.29;
Phi_h_Bin_Values[4][33][0] =  24; Phi_h_Bin_Values[4][33][1] = 722; Phi_h_Bin_Values[4][33][2] = 2975;
z_pT_Bin_Borders[4][34][0] = 0.33; z_pT_Bin_Borders[4][34][1] = 0.26; z_pT_Bin_Borders[4][34][2] = 0.48; z_pT_Bin_Borders[4][34][3] = 0.38;
Phi_h_Bin_Values[4][34][0] =  24; Phi_h_Bin_Values[4][34][1] = 746; Phi_h_Bin_Values[4][34][2] = 2999;
z_pT_Bin_Borders[4][35][0] = 0.33; z_pT_Bin_Borders[4][35][1] = 0.26; z_pT_Bin_Borders[4][35][2] = 0.61; z_pT_Bin_Borders[4][35][3] = 0.48;
Phi_h_Bin_Values[4][35][0] =  24; Phi_h_Bin_Values[4][35][1] = 770; Phi_h_Bin_Values[4][35][2] = 3023;
z_pT_Bin_Borders[4][36][0] = 0.33; z_pT_Bin_Borders[4][36][1] = 0.26; z_pT_Bin_Borders[4][36][2] = 0.85; z_pT_Bin_Borders[4][36][3] = 0.61;
Phi_h_Bin_Values[4][36][0] =  1; Phi_h_Bin_Values[4][36][1] = 794; Phi_h_Bin_Values[4][36][2] = 3047;
z_pT_Bin_Borders[4][37][0] = 10; z_pT_Bin_Borders[4][37][1] = 0.71; z_pT_Bin_Borders[4][37][2] = 0.05; z_pT_Bin_Borders[4][37][3] = 0;
Phi_h_Bin_Values[4][37][0] =  1; Phi_h_Bin_Values[4][37][1] = 795; Phi_h_Bin_Values[4][37][2] = 3048;
z_pT_Bin_Borders[4][38][0] = 10; z_pT_Bin_Borders[4][38][1] = 0.71; z_pT_Bin_Borders[4][38][2] = 0.2; z_pT_Bin_Borders[4][38][3] = 0.05;
Phi_h_Bin_Values[4][38][0] =  1; Phi_h_Bin_Values[4][38][1] = 796; Phi_h_Bin_Values[4][38][2] = 3049;
z_pT_Bin_Borders[4][39][0] = 10; z_pT_Bin_Borders[4][39][1] = 0.71; z_pT_Bin_Borders[4][39][2] = 0.29; z_pT_Bin_Borders[4][39][3] = 0.2;
Phi_h_Bin_Values[4][39][0] =  1; Phi_h_Bin_Values[4][39][1] = 797; Phi_h_Bin_Values[4][39][2] = 3050;
z_pT_Bin_Borders[4][40][0] = 10; z_pT_Bin_Borders[4][40][1] = 0.71; z_pT_Bin_Borders[4][40][2] = 0.38; z_pT_Bin_Borders[4][40][3] = 0.29;
Phi_h_Bin_Values[4][40][0] =  1; Phi_h_Bin_Values[4][40][1] = 798; Phi_h_Bin_Values[4][40][2] = 3051;
z_pT_Bin_Borders[4][41][0] = 10; z_pT_Bin_Borders[4][41][1] = 0.71; z_pT_Bin_Borders[4][41][2] = 0.48; z_pT_Bin_Borders[4][41][3] = 0.38;
Phi_h_Bin_Values[4][41][0] =  1; Phi_h_Bin_Values[4][41][1] = 799; Phi_h_Bin_Values[4][41][2] = 3052;
z_pT_Bin_Borders[4][42][0] = 10; z_pT_Bin_Borders[4][42][1] = 0.71; z_pT_Bin_Borders[4][42][2] = 0.61; z_pT_Bin_Borders[4][42][3] = 0.48;
Phi_h_Bin_Values[4][42][0] =  1; Phi_h_Bin_Values[4][42][1] = 800; Phi_h_Bin_Values[4][42][2] = 3053;
z_pT_Bin_Borders[4][43][0] = 10; z_pT_Bin_Borders[4][43][1] = 0.71; z_pT_Bin_Borders[4][43][2] = 0.85; z_pT_Bin_Borders[4][43][3] = 0.61;
Phi_h_Bin_Values[4][43][0] =  1; Phi_h_Bin_Values[4][43][1] = 801; Phi_h_Bin_Values[4][43][2] = 3054;
z_pT_Bin_Borders[4][44][0] = 10; z_pT_Bin_Borders[4][44][1] = 0.71; z_pT_Bin_Borders[4][44][2] = 10; z_pT_Bin_Borders[4][44][3] = 0.85;
Phi_h_Bin_Values[4][44][0] =  1; Phi_h_Bin_Values[4][44][1] = 802; Phi_h_Bin_Values[4][44][2] = 3055;
z_pT_Bin_Borders[4][45][0] = 0.71; z_pT_Bin_Borders[4][45][1] = 0.59; z_pT_Bin_Borders[4][45][2] = 0.05; z_pT_Bin_Borders[4][45][3] = 0;
Phi_h_Bin_Values[4][45][0] =  1; Phi_h_Bin_Values[4][45][1] = 803; Phi_h_Bin_Values[4][45][2] = 3056;
z_pT_Bin_Borders[4][46][0] = 0.71; z_pT_Bin_Borders[4][46][1] = 0.59; z_pT_Bin_Borders[4][46][2] = 10; z_pT_Bin_Borders[4][46][3] = 0.85;
Phi_h_Bin_Values[4][46][0] =  1; Phi_h_Bin_Values[4][46][1] = 804; Phi_h_Bin_Values[4][46][2] = 3057;
z_pT_Bin_Borders[4][47][0] = 0.59; z_pT_Bin_Borders[4][47][1] = 0.5; z_pT_Bin_Borders[4][47][2] = 0.05; z_pT_Bin_Borders[4][47][3] = 0;
Phi_h_Bin_Values[4][47][0] =  1; Phi_h_Bin_Values[4][47][1] = 805; Phi_h_Bin_Values[4][47][2] = 3058;
z_pT_Bin_Borders[4][48][0] = 0.59; z_pT_Bin_Borders[4][48][1] = 0.5; z_pT_Bin_Borders[4][48][2] = 10; z_pT_Bin_Borders[4][48][3] = 0.85;
Phi_h_Bin_Values[4][48][0] =  1; Phi_h_Bin_Values[4][48][1] = 806; Phi_h_Bin_Values[4][48][2] = 3059;
z_pT_Bin_Borders[4][49][0] = 0.5; z_pT_Bin_Borders[4][49][1] = 0.43; z_pT_Bin_Borders[4][49][2] = 0.05; z_pT_Bin_Borders[4][49][3] = 0;
Phi_h_Bin_Values[4][49][0] =  1; Phi_h_Bin_Values[4][49][1] = 807; Phi_h_Bin_Values[4][49][2] = 3060;
z_pT_Bin_Borders[4][50][0] = 0.5; z_pT_Bin_Borders[4][50][1] = 0.43; z_pT_Bin_Borders[4][50][2] = 10; z_pT_Bin_Borders[4][50][3] = 0.85;
Phi_h_Bin_Values[4][50][0] =  1; Phi_h_Bin_Values[4][50][1] = 808; Phi_h_Bin_Values[4][50][2] = 3061;
z_pT_Bin_Borders[4][51][0] = 0.43; z_pT_Bin_Borders[4][51][1] = 0.38; z_pT_Bin_Borders[4][51][2] = 0.05; z_pT_Bin_Borders[4][51][3] = 0;
Phi_h_Bin_Values[4][51][0] =  1; Phi_h_Bin_Values[4][51][1] = 809; Phi_h_Bin_Values[4][51][2] = 3062;
z_pT_Bin_Borders[4][52][0] = 0.43; z_pT_Bin_Borders[4][52][1] = 0.38; z_pT_Bin_Borders[4][52][2] = 10; z_pT_Bin_Borders[4][52][3] = 0.85;
Phi_h_Bin_Values[4][52][0] =  1; Phi_h_Bin_Values[4][52][1] = 810; Phi_h_Bin_Values[4][52][2] = 3063;
z_pT_Bin_Borders[4][53][0] = 0.38; z_pT_Bin_Borders[4][53][1] = 0.33; z_pT_Bin_Borders[4][53][2] = 0.05; z_pT_Bin_Borders[4][53][3] = 0;
Phi_h_Bin_Values[4][53][0] =  1; Phi_h_Bin_Values[4][53][1] = 811; Phi_h_Bin_Values[4][53][2] = 3064;
z_pT_Bin_Borders[4][54][0] = 0.38; z_pT_Bin_Borders[4][54][1] = 0.33; z_pT_Bin_Borders[4][54][2] = 10; z_pT_Bin_Borders[4][54][3] = 0.85;
Phi_h_Bin_Values[4][54][0] =  1; Phi_h_Bin_Values[4][54][1] = 812; Phi_h_Bin_Values[4][54][2] = 3065;
z_pT_Bin_Borders[4][55][0] = 0.33; z_pT_Bin_Borders[4][55][1] = 0.26; z_pT_Bin_Borders[4][55][2] = 0.05; z_pT_Bin_Borders[4][55][3] = 0;
Phi_h_Bin_Values[4][55][0] =  1; Phi_h_Bin_Values[4][55][1] = 813; Phi_h_Bin_Values[4][55][2] = 3066;
z_pT_Bin_Borders[4][56][0] = 0.33; z_pT_Bin_Borders[4][56][1] = 0.26; z_pT_Bin_Borders[4][56][2] = 10; z_pT_Bin_Borders[4][56][3] = 0.85;
Phi_h_Bin_Values[4][56][0] =  1; Phi_h_Bin_Values[4][56][1] = 814; Phi_h_Bin_Values[4][56][2] = 3067;
z_pT_Bin_Borders[4][57][0] = 0.26; z_pT_Bin_Borders[4][57][1] = 0; z_pT_Bin_Borders[4][57][2] = 0.05; z_pT_Bin_Borders[4][57][3] = 0;
Phi_h_Bin_Values[4][57][0] =  1; Phi_h_Bin_Values[4][57][1] = 815; Phi_h_Bin_Values[4][57][2] = 3068;
z_pT_Bin_Borders[4][58][0] = 0.26; z_pT_Bin_Borders[4][58][1] = 0; z_pT_Bin_Borders[4][58][2] = 0.2; z_pT_Bin_Borders[4][58][3] = 0.05;
Phi_h_Bin_Values[4][58][0] =  1; Phi_h_Bin_Values[4][58][1] = 816; Phi_h_Bin_Values[4][58][2] = 3069;
z_pT_Bin_Borders[4][59][0] = 0.26; z_pT_Bin_Borders[4][59][1] = 0; z_pT_Bin_Borders[4][59][2] = 0.29; z_pT_Bin_Borders[4][59][3] = 0.2;
Phi_h_Bin_Values[4][59][0] =  1; Phi_h_Bin_Values[4][59][1] = 817; Phi_h_Bin_Values[4][59][2] = 3070;
z_pT_Bin_Borders[4][60][0] = 0.26; z_pT_Bin_Borders[4][60][1] = 0; z_pT_Bin_Borders[4][60][2] = 0.38; z_pT_Bin_Borders[4][60][3] = 0.29;
Phi_h_Bin_Values[4][60][0] =  1; Phi_h_Bin_Values[4][60][1] = 818; Phi_h_Bin_Values[4][60][2] = 3071;
z_pT_Bin_Borders[4][61][0] = 0.26; z_pT_Bin_Borders[4][61][1] = 0; z_pT_Bin_Borders[4][61][2] = 0.48; z_pT_Bin_Borders[4][61][3] = 0.38;
Phi_h_Bin_Values[4][61][0] =  1; Phi_h_Bin_Values[4][61][1] = 819; Phi_h_Bin_Values[4][61][2] = 3072;
z_pT_Bin_Borders[4][62][0] = 0.26; z_pT_Bin_Borders[4][62][1] = 0; z_pT_Bin_Borders[4][62][2] = 0.61; z_pT_Bin_Borders[4][62][3] = 0.48;
Phi_h_Bin_Values[4][62][0] =  1; Phi_h_Bin_Values[4][62][1] = 820; Phi_h_Bin_Values[4][62][2] = 3073;
z_pT_Bin_Borders[4][63][0] = 0.26; z_pT_Bin_Borders[4][63][1] = 0; z_pT_Bin_Borders[4][63][2] = 0.85; z_pT_Bin_Borders[4][63][3] = 0.61;
Phi_h_Bin_Values[4][63][0] =  1; Phi_h_Bin_Values[4][63][1] = 821; Phi_h_Bin_Values[4][63][2] = 3074;
z_pT_Bin_Borders[4][64][0] = 0.26; z_pT_Bin_Borders[4][64][1] = 0; z_pT_Bin_Borders[4][64][2] = 10; z_pT_Bin_Borders[4][64][3] = 0.85;
Phi_h_Bin_Values[4][64][0] =  1; Phi_h_Bin_Values[4][64][1] = 822; Phi_h_Bin_Values[4][64][2] = 3075;
z_pT_Bin_Borders[5][1][0] = 0.72; z_pT_Bin_Borders[5][1][1] = 0.49; z_pT_Bin_Borders[5][1][2] = 0.22; z_pT_Bin_Borders[5][1][3] = 0.05;
Phi_h_Bin_Values[5][1][0] =  24; Phi_h_Bin_Values[5][1][1] = 0; Phi_h_Bin_Values[5][1][2] = 3076;
z_pT_Bin_Borders[5][2][0] = 0.72; z_pT_Bin_Borders[5][2][1] = 0.49; z_pT_Bin_Borders[5][2][2] = 0.32; z_pT_Bin_Borders[5][2][3] = 0.22;
Phi_h_Bin_Values[5][2][0] =  24; Phi_h_Bin_Values[5][2][1] = 24; Phi_h_Bin_Values[5][2][2] = 3100;
z_pT_Bin_Borders[5][3][0] = 0.72; z_pT_Bin_Borders[5][3][1] = 0.49; z_pT_Bin_Borders[5][3][2] = 0.41; z_pT_Bin_Borders[5][3][3] = 0.32;
Phi_h_Bin_Values[5][3][0] =  24; Phi_h_Bin_Values[5][3][1] = 48; Phi_h_Bin_Values[5][3][2] = 3124;
z_pT_Bin_Borders[5][4][0] = 0.72; z_pT_Bin_Borders[5][4][1] = 0.49; z_pT_Bin_Borders[5][4][2] = 0.51; z_pT_Bin_Borders[5][4][3] = 0.41;
Phi_h_Bin_Values[5][4][0] =  24; Phi_h_Bin_Values[5][4][1] = 72; Phi_h_Bin_Values[5][4][2] = 3148;
z_pT_Bin_Borders[5][5][0] = 0.72; z_pT_Bin_Borders[5][5][1] = 0.49; z_pT_Bin_Borders[5][5][2] = 0.65; z_pT_Bin_Borders[5][5][3] = 0.51;
Phi_h_Bin_Values[5][5][0] =  24; Phi_h_Bin_Values[5][5][1] = 96; Phi_h_Bin_Values[5][5][2] = 3172;
z_pT_Bin_Borders[5][6][0] = 0.72; z_pT_Bin_Borders[5][6][1] = 0.49; z_pT_Bin_Borders[5][6][2] = 0.98; z_pT_Bin_Borders[5][6][3] = 0.65;
Phi_h_Bin_Values[5][6][0] =  24; Phi_h_Bin_Values[5][6][1] = 120; Phi_h_Bin_Values[5][6][2] = 3196;
z_pT_Bin_Borders[5][7][0] = 0.49; z_pT_Bin_Borders[5][7][1] = 0.38; z_pT_Bin_Borders[5][7][2] = 0.22; z_pT_Bin_Borders[5][7][3] = 0.05;
Phi_h_Bin_Values[5][7][0] =  24; Phi_h_Bin_Values[5][7][1] = 144; Phi_h_Bin_Values[5][7][2] = 3220;
z_pT_Bin_Borders[5][8][0] = 0.49; z_pT_Bin_Borders[5][8][1] = 0.38; z_pT_Bin_Borders[5][8][2] = 0.32; z_pT_Bin_Borders[5][8][3] = 0.22;
Phi_h_Bin_Values[5][8][0] =  24; Phi_h_Bin_Values[5][8][1] = 168; Phi_h_Bin_Values[5][8][2] = 3244;
z_pT_Bin_Borders[5][9][0] = 0.49; z_pT_Bin_Borders[5][9][1] = 0.38; z_pT_Bin_Borders[5][9][2] = 0.41; z_pT_Bin_Borders[5][9][3] = 0.32;
Phi_h_Bin_Values[5][9][0] =  24; Phi_h_Bin_Values[5][9][1] = 192; Phi_h_Bin_Values[5][9][2] = 3268;
z_pT_Bin_Borders[5][10][0] = 0.49; z_pT_Bin_Borders[5][10][1] = 0.38; z_pT_Bin_Borders[5][10][2] = 0.51; z_pT_Bin_Borders[5][10][3] = 0.41;
Phi_h_Bin_Values[5][10][0] =  24; Phi_h_Bin_Values[5][10][1] = 216; Phi_h_Bin_Values[5][10][2] = 3292;
z_pT_Bin_Borders[5][11][0] = 0.49; z_pT_Bin_Borders[5][11][1] = 0.38; z_pT_Bin_Borders[5][11][2] = 0.65; z_pT_Bin_Borders[5][11][3] = 0.51;
Phi_h_Bin_Values[5][11][0] =  24; Phi_h_Bin_Values[5][11][1] = 240; Phi_h_Bin_Values[5][11][2] = 3316;
z_pT_Bin_Borders[5][12][0] = 0.49; z_pT_Bin_Borders[5][12][1] = 0.38; z_pT_Bin_Borders[5][12][2] = 0.98; z_pT_Bin_Borders[5][12][3] = 0.65;
Phi_h_Bin_Values[5][12][0] =  24; Phi_h_Bin_Values[5][12][1] = 264; Phi_h_Bin_Values[5][12][2] = 3340;
z_pT_Bin_Borders[5][13][0] = 0.38; z_pT_Bin_Borders[5][13][1] = 0.3; z_pT_Bin_Borders[5][13][2] = 0.22; z_pT_Bin_Borders[5][13][3] = 0.05;
Phi_h_Bin_Values[5][13][0] =  24; Phi_h_Bin_Values[5][13][1] = 288; Phi_h_Bin_Values[5][13][2] = 3364;
z_pT_Bin_Borders[5][14][0] = 0.38; z_pT_Bin_Borders[5][14][1] = 0.3; z_pT_Bin_Borders[5][14][2] = 0.32; z_pT_Bin_Borders[5][14][3] = 0.22;
Phi_h_Bin_Values[5][14][0] =  24; Phi_h_Bin_Values[5][14][1] = 312; Phi_h_Bin_Values[5][14][2] = 3388;
z_pT_Bin_Borders[5][15][0] = 0.38; z_pT_Bin_Borders[5][15][1] = 0.3; z_pT_Bin_Borders[5][15][2] = 0.41; z_pT_Bin_Borders[5][15][3] = 0.32;
Phi_h_Bin_Values[5][15][0] =  24; Phi_h_Bin_Values[5][15][1] = 336; Phi_h_Bin_Values[5][15][2] = 3412;
z_pT_Bin_Borders[5][16][0] = 0.38; z_pT_Bin_Borders[5][16][1] = 0.3; z_pT_Bin_Borders[5][16][2] = 0.51; z_pT_Bin_Borders[5][16][3] = 0.41;
Phi_h_Bin_Values[5][16][0] =  24; Phi_h_Bin_Values[5][16][1] = 360; Phi_h_Bin_Values[5][16][2] = 3436;
z_pT_Bin_Borders[5][17][0] = 0.38; z_pT_Bin_Borders[5][17][1] = 0.3; z_pT_Bin_Borders[5][17][2] = 0.65; z_pT_Bin_Borders[5][17][3] = 0.51;
Phi_h_Bin_Values[5][17][0] =  24; Phi_h_Bin_Values[5][17][1] = 384; Phi_h_Bin_Values[5][17][2] = 3460;
z_pT_Bin_Borders[5][18][0] = 0.38; z_pT_Bin_Borders[5][18][1] = 0.3; z_pT_Bin_Borders[5][18][2] = 0.98; z_pT_Bin_Borders[5][18][3] = 0.65;
Phi_h_Bin_Values[5][18][0] =  24; Phi_h_Bin_Values[5][18][1] = 408; Phi_h_Bin_Values[5][18][2] = 3484;
z_pT_Bin_Borders[5][19][0] = 0.3; z_pT_Bin_Borders[5][19][1] = 0.24; z_pT_Bin_Borders[5][19][2] = 0.22; z_pT_Bin_Borders[5][19][3] = 0.05;
Phi_h_Bin_Values[5][19][0] =  24; Phi_h_Bin_Values[5][19][1] = 432; Phi_h_Bin_Values[5][19][2] = 3508;
z_pT_Bin_Borders[5][20][0] = 0.3; z_pT_Bin_Borders[5][20][1] = 0.24; z_pT_Bin_Borders[5][20][2] = 0.32; z_pT_Bin_Borders[5][20][3] = 0.22;
Phi_h_Bin_Values[5][20][0] =  24; Phi_h_Bin_Values[5][20][1] = 456; Phi_h_Bin_Values[5][20][2] = 3532;
z_pT_Bin_Borders[5][21][0] = 0.3; z_pT_Bin_Borders[5][21][1] = 0.24; z_pT_Bin_Borders[5][21][2] = 0.41; z_pT_Bin_Borders[5][21][3] = 0.32;
Phi_h_Bin_Values[5][21][0] =  24; Phi_h_Bin_Values[5][21][1] = 480; Phi_h_Bin_Values[5][21][2] = 3556;
z_pT_Bin_Borders[5][22][0] = 0.3; z_pT_Bin_Borders[5][22][1] = 0.24; z_pT_Bin_Borders[5][22][2] = 0.51; z_pT_Bin_Borders[5][22][3] = 0.41;
Phi_h_Bin_Values[5][22][0] =  24; Phi_h_Bin_Values[5][22][1] = 504; Phi_h_Bin_Values[5][22][2] = 3580;
z_pT_Bin_Borders[5][23][0] = 0.3; z_pT_Bin_Borders[5][23][1] = 0.24; z_pT_Bin_Borders[5][23][2] = 0.65; z_pT_Bin_Borders[5][23][3] = 0.51;
Phi_h_Bin_Values[5][23][0] =  24; Phi_h_Bin_Values[5][23][1] = 528; Phi_h_Bin_Values[5][23][2] = 3604;
z_pT_Bin_Borders[5][24][0] = 0.3; z_pT_Bin_Borders[5][24][1] = 0.24; z_pT_Bin_Borders[5][24][2] = 0.98; z_pT_Bin_Borders[5][24][3] = 0.65;
Phi_h_Bin_Values[5][24][0] =  1; Phi_h_Bin_Values[5][24][1] = 552; Phi_h_Bin_Values[5][24][2] = 3628;
z_pT_Bin_Borders[5][25][0] = 0.24; z_pT_Bin_Borders[5][25][1] = 0.2; z_pT_Bin_Borders[5][25][2] = 0.22; z_pT_Bin_Borders[5][25][3] = 0.05;
Phi_h_Bin_Values[5][25][0] =  24; Phi_h_Bin_Values[5][25][1] = 553; Phi_h_Bin_Values[5][25][2] = 3629;
z_pT_Bin_Borders[5][26][0] = 0.24; z_pT_Bin_Borders[5][26][1] = 0.2; z_pT_Bin_Borders[5][26][2] = 0.32; z_pT_Bin_Borders[5][26][3] = 0.22;
Phi_h_Bin_Values[5][26][0] =  24; Phi_h_Bin_Values[5][26][1] = 577; Phi_h_Bin_Values[5][26][2] = 3653;
z_pT_Bin_Borders[5][27][0] = 0.24; z_pT_Bin_Borders[5][27][1] = 0.2; z_pT_Bin_Borders[5][27][2] = 0.41; z_pT_Bin_Borders[5][27][3] = 0.32;
Phi_h_Bin_Values[5][27][0] =  24; Phi_h_Bin_Values[5][27][1] = 601; Phi_h_Bin_Values[5][27][2] = 3677;
z_pT_Bin_Borders[5][28][0] = 0.24; z_pT_Bin_Borders[5][28][1] = 0.2; z_pT_Bin_Borders[5][28][2] = 0.51; z_pT_Bin_Borders[5][28][3] = 0.41;
Phi_h_Bin_Values[5][28][0] =  24; Phi_h_Bin_Values[5][28][1] = 625; Phi_h_Bin_Values[5][28][2] = 3701;
z_pT_Bin_Borders[5][29][0] = 0.24; z_pT_Bin_Borders[5][29][1] = 0.2; z_pT_Bin_Borders[5][29][2] = 0.65; z_pT_Bin_Borders[5][29][3] = 0.51;
Phi_h_Bin_Values[5][29][0] =  24; Phi_h_Bin_Values[5][29][1] = 649; Phi_h_Bin_Values[5][29][2] = 3725;
z_pT_Bin_Borders[5][30][0] = 0.24; z_pT_Bin_Borders[5][30][1] = 0.2; z_pT_Bin_Borders[5][30][2] = 0.98; z_pT_Bin_Borders[5][30][3] = 0.65;
Phi_h_Bin_Values[5][30][0] =  1; Phi_h_Bin_Values[5][30][1] = 673; Phi_h_Bin_Values[5][30][2] = 3749;
z_pT_Bin_Borders[5][31][0] = 0.2; z_pT_Bin_Borders[5][31][1] = 0.16; z_pT_Bin_Borders[5][31][2] = 0.22; z_pT_Bin_Borders[5][31][3] = 0.05;
Phi_h_Bin_Values[5][31][0] =  24; Phi_h_Bin_Values[5][31][1] = 674; Phi_h_Bin_Values[5][31][2] = 3750;
z_pT_Bin_Borders[5][32][0] = 0.2; z_pT_Bin_Borders[5][32][1] = 0.16; z_pT_Bin_Borders[5][32][2] = 0.32; z_pT_Bin_Borders[5][32][3] = 0.22;
Phi_h_Bin_Values[5][32][0] =  24; Phi_h_Bin_Values[5][32][1] = 698; Phi_h_Bin_Values[5][32][2] = 3774;
z_pT_Bin_Borders[5][33][0] = 0.2; z_pT_Bin_Borders[5][33][1] = 0.16; z_pT_Bin_Borders[5][33][2] = 0.41; z_pT_Bin_Borders[5][33][3] = 0.32;
Phi_h_Bin_Values[5][33][0] =  24; Phi_h_Bin_Values[5][33][1] = 722; Phi_h_Bin_Values[5][33][2] = 3798;
z_pT_Bin_Borders[5][34][0] = 0.2; z_pT_Bin_Borders[5][34][1] = 0.16; z_pT_Bin_Borders[5][34][2] = 0.51; z_pT_Bin_Borders[5][34][3] = 0.41;
Phi_h_Bin_Values[5][34][0] =  24; Phi_h_Bin_Values[5][34][1] = 746; Phi_h_Bin_Values[5][34][2] = 3822;
z_pT_Bin_Borders[5][35][0] = 0.2; z_pT_Bin_Borders[5][35][1] = 0.16; z_pT_Bin_Borders[5][35][2] = 0.65; z_pT_Bin_Borders[5][35][3] = 0.51;
Phi_h_Bin_Values[5][35][0] =  1; Phi_h_Bin_Values[5][35][1] = 770; Phi_h_Bin_Values[5][35][2] = 3846;
z_pT_Bin_Borders[5][36][0] = 0.2; z_pT_Bin_Borders[5][36][1] = 0.16; z_pT_Bin_Borders[5][36][2] = 0.98; z_pT_Bin_Borders[5][36][3] = 0.65;
Phi_h_Bin_Values[5][36][0] =  1; Phi_h_Bin_Values[5][36][1] = 771; Phi_h_Bin_Values[5][36][2] = 3847;
z_pT_Bin_Borders[5][37][0] = 10; z_pT_Bin_Borders[5][37][1] = 0.72; z_pT_Bin_Borders[5][37][2] = 0.05; z_pT_Bin_Borders[5][37][3] = 0;
Phi_h_Bin_Values[5][37][0] =  1; Phi_h_Bin_Values[5][37][1] = 772; Phi_h_Bin_Values[5][37][2] = 3848;
z_pT_Bin_Borders[5][38][0] = 10; z_pT_Bin_Borders[5][38][1] = 0.72; z_pT_Bin_Borders[5][38][2] = 0.22; z_pT_Bin_Borders[5][38][3] = 0.05;
Phi_h_Bin_Values[5][38][0] =  1; Phi_h_Bin_Values[5][38][1] = 773; Phi_h_Bin_Values[5][38][2] = 3849;
z_pT_Bin_Borders[5][39][0] = 10; z_pT_Bin_Borders[5][39][1] = 0.72; z_pT_Bin_Borders[5][39][2] = 0.32; z_pT_Bin_Borders[5][39][3] = 0.22;
Phi_h_Bin_Values[5][39][0] =  1; Phi_h_Bin_Values[5][39][1] = 774; Phi_h_Bin_Values[5][39][2] = 3850;
z_pT_Bin_Borders[5][40][0] = 10; z_pT_Bin_Borders[5][40][1] = 0.72; z_pT_Bin_Borders[5][40][2] = 0.41; z_pT_Bin_Borders[5][40][3] = 0.32;
Phi_h_Bin_Values[5][40][0] =  1; Phi_h_Bin_Values[5][40][1] = 775; Phi_h_Bin_Values[5][40][2] = 3851;
z_pT_Bin_Borders[5][41][0] = 10; z_pT_Bin_Borders[5][41][1] = 0.72; z_pT_Bin_Borders[5][41][2] = 0.51; z_pT_Bin_Borders[5][41][3] = 0.41;
Phi_h_Bin_Values[5][41][0] =  1; Phi_h_Bin_Values[5][41][1] = 776; Phi_h_Bin_Values[5][41][2] = 3852;
z_pT_Bin_Borders[5][42][0] = 10; z_pT_Bin_Borders[5][42][1] = 0.72; z_pT_Bin_Borders[5][42][2] = 0.65; z_pT_Bin_Borders[5][42][3] = 0.51;
Phi_h_Bin_Values[5][42][0] =  1; Phi_h_Bin_Values[5][42][1] = 777; Phi_h_Bin_Values[5][42][2] = 3853;
z_pT_Bin_Borders[5][43][0] = 10; z_pT_Bin_Borders[5][43][1] = 0.72; z_pT_Bin_Borders[5][43][2] = 0.98; z_pT_Bin_Borders[5][43][3] = 0.65;
Phi_h_Bin_Values[5][43][0] =  1; Phi_h_Bin_Values[5][43][1] = 778; Phi_h_Bin_Values[5][43][2] = 3854;
z_pT_Bin_Borders[5][44][0] = 10; z_pT_Bin_Borders[5][44][1] = 0.72; z_pT_Bin_Borders[5][44][2] = 10; z_pT_Bin_Borders[5][44][3] = 0.98;
Phi_h_Bin_Values[5][44][0] =  1; Phi_h_Bin_Values[5][44][1] = 779; Phi_h_Bin_Values[5][44][2] = 3855;
z_pT_Bin_Borders[5][45][0] = 0.72; z_pT_Bin_Borders[5][45][1] = 0.49; z_pT_Bin_Borders[5][45][2] = 0.05; z_pT_Bin_Borders[5][45][3] = 0;
Phi_h_Bin_Values[5][45][0] =  1; Phi_h_Bin_Values[5][45][1] = 780; Phi_h_Bin_Values[5][45][2] = 3856;
z_pT_Bin_Borders[5][46][0] = 0.72; z_pT_Bin_Borders[5][46][1] = 0.49; z_pT_Bin_Borders[5][46][2] = 10; z_pT_Bin_Borders[5][46][3] = 0.98;
Phi_h_Bin_Values[5][46][0] =  1; Phi_h_Bin_Values[5][46][1] = 781; Phi_h_Bin_Values[5][46][2] = 3857;
z_pT_Bin_Borders[5][47][0] = 0.49; z_pT_Bin_Borders[5][47][1] = 0.38; z_pT_Bin_Borders[5][47][2] = 0.05; z_pT_Bin_Borders[5][47][3] = 0;
Phi_h_Bin_Values[5][47][0] =  1; Phi_h_Bin_Values[5][47][1] = 782; Phi_h_Bin_Values[5][47][2] = 3858;
z_pT_Bin_Borders[5][48][0] = 0.49; z_pT_Bin_Borders[5][48][1] = 0.38; z_pT_Bin_Borders[5][48][2] = 10; z_pT_Bin_Borders[5][48][3] = 0.98;
Phi_h_Bin_Values[5][48][0] =  1; Phi_h_Bin_Values[5][48][1] = 783; Phi_h_Bin_Values[5][48][2] = 3859;
z_pT_Bin_Borders[5][49][0] = 0.38; z_pT_Bin_Borders[5][49][1] = 0.3; z_pT_Bin_Borders[5][49][2] = 0.05; z_pT_Bin_Borders[5][49][3] = 0;
Phi_h_Bin_Values[5][49][0] =  1; Phi_h_Bin_Values[5][49][1] = 784; Phi_h_Bin_Values[5][49][2] = 3860;
z_pT_Bin_Borders[5][50][0] = 0.38; z_pT_Bin_Borders[5][50][1] = 0.3; z_pT_Bin_Borders[5][50][2] = 10; z_pT_Bin_Borders[5][50][3] = 0.98;
Phi_h_Bin_Values[5][50][0] =  1; Phi_h_Bin_Values[5][50][1] = 785; Phi_h_Bin_Values[5][50][2] = 3861;
z_pT_Bin_Borders[5][51][0] = 0.3; z_pT_Bin_Borders[5][51][1] = 0.24; z_pT_Bin_Borders[5][51][2] = 0.05; z_pT_Bin_Borders[5][51][3] = 0;
Phi_h_Bin_Values[5][51][0] =  1; Phi_h_Bin_Values[5][51][1] = 786; Phi_h_Bin_Values[5][51][2] = 3862;
z_pT_Bin_Borders[5][52][0] = 0.3; z_pT_Bin_Borders[5][52][1] = 0.24; z_pT_Bin_Borders[5][52][2] = 10; z_pT_Bin_Borders[5][52][3] = 0.98;
Phi_h_Bin_Values[5][52][0] =  1; Phi_h_Bin_Values[5][52][1] = 787; Phi_h_Bin_Values[5][52][2] = 3863;
z_pT_Bin_Borders[5][53][0] = 0.24; z_pT_Bin_Borders[5][53][1] = 0.2; z_pT_Bin_Borders[5][53][2] = 0.05; z_pT_Bin_Borders[5][53][3] = 0;
Phi_h_Bin_Values[5][53][0] =  1; Phi_h_Bin_Values[5][53][1] = 788; Phi_h_Bin_Values[5][53][2] = 3864;
z_pT_Bin_Borders[5][54][0] = 0.24; z_pT_Bin_Borders[5][54][1] = 0.2; z_pT_Bin_Borders[5][54][2] = 10; z_pT_Bin_Borders[5][54][3] = 0.98;
Phi_h_Bin_Values[5][54][0] =  1; Phi_h_Bin_Values[5][54][1] = 789; Phi_h_Bin_Values[5][54][2] = 3865;
z_pT_Bin_Borders[5][55][0] = 0.2; z_pT_Bin_Borders[5][55][1] = 0.16; z_pT_Bin_Borders[5][55][2] = 0.05; z_pT_Bin_Borders[5][55][3] = 0;
Phi_h_Bin_Values[5][55][0] =  1; Phi_h_Bin_Values[5][55][1] = 790; Phi_h_Bin_Values[5][55][2] = 3866;
z_pT_Bin_Borders[5][56][0] = 0.2; z_pT_Bin_Borders[5][56][1] = 0.16; z_pT_Bin_Borders[5][56][2] = 10; z_pT_Bin_Borders[5][56][3] = 0.98;
Phi_h_Bin_Values[5][56][0] =  1; Phi_h_Bin_Values[5][56][1] = 791; Phi_h_Bin_Values[5][56][2] = 3867;
z_pT_Bin_Borders[5][57][0] = 0.16; z_pT_Bin_Borders[5][57][1] = 0; z_pT_Bin_Borders[5][57][2] = 0.05; z_pT_Bin_Borders[5][57][3] = 0;
Phi_h_Bin_Values[5][57][0] =  1; Phi_h_Bin_Values[5][57][1] = 792; Phi_h_Bin_Values[5][57][2] = 3868;
z_pT_Bin_Borders[5][58][0] = 0.16; z_pT_Bin_Borders[5][58][1] = 0; z_pT_Bin_Borders[5][58][2] = 0.22; z_pT_Bin_Borders[5][58][3] = 0.05;
Phi_h_Bin_Values[5][58][0] =  1; Phi_h_Bin_Values[5][58][1] = 793; Phi_h_Bin_Values[5][58][2] = 3869;
z_pT_Bin_Borders[5][59][0] = 0.16; z_pT_Bin_Borders[5][59][1] = 0; z_pT_Bin_Borders[5][59][2] = 0.32; z_pT_Bin_Borders[5][59][3] = 0.22;
Phi_h_Bin_Values[5][59][0] =  1; Phi_h_Bin_Values[5][59][1] = 794; Phi_h_Bin_Values[5][59][2] = 3870;
z_pT_Bin_Borders[5][60][0] = 0.16; z_pT_Bin_Borders[5][60][1] = 0; z_pT_Bin_Borders[5][60][2] = 0.41; z_pT_Bin_Borders[5][60][3] = 0.32;
Phi_h_Bin_Values[5][60][0] =  1; Phi_h_Bin_Values[5][60][1] = 795; Phi_h_Bin_Values[5][60][2] = 3871;
z_pT_Bin_Borders[5][61][0] = 0.16; z_pT_Bin_Borders[5][61][1] = 0; z_pT_Bin_Borders[5][61][2] = 0.51; z_pT_Bin_Borders[5][61][3] = 0.41;
Phi_h_Bin_Values[5][61][0] =  1; Phi_h_Bin_Values[5][61][1] = 796; Phi_h_Bin_Values[5][61][2] = 3872;
z_pT_Bin_Borders[5][62][0] = 0.16; z_pT_Bin_Borders[5][62][1] = 0; z_pT_Bin_Borders[5][62][2] = 0.65; z_pT_Bin_Borders[5][62][3] = 0.51;
Phi_h_Bin_Values[5][62][0] =  1; Phi_h_Bin_Values[5][62][1] = 797; Phi_h_Bin_Values[5][62][2] = 3873;
z_pT_Bin_Borders[5][63][0] = 0.16; z_pT_Bin_Borders[5][63][1] = 0; z_pT_Bin_Borders[5][63][2] = 0.98; z_pT_Bin_Borders[5][63][3] = 0.65;
Phi_h_Bin_Values[5][63][0] =  1; Phi_h_Bin_Values[5][63][1] = 798; Phi_h_Bin_Values[5][63][2] = 3874;
z_pT_Bin_Borders[5][64][0] = 0.16; z_pT_Bin_Borders[5][64][1] = 0; z_pT_Bin_Borders[5][64][2] = 10; z_pT_Bin_Borders[5][64][3] = 0.98;
Phi_h_Bin_Values[5][64][0] =  1; Phi_h_Bin_Values[5][64][1] = 799; Phi_h_Bin_Values[5][64][2] = 3875;
z_pT_Bin_Borders[6][1][0] = 0.72; z_pT_Bin_Borders[6][1][1] = 0.45; z_pT_Bin_Borders[6][1][2] = 0.22; z_pT_Bin_Borders[6][1][3] = 0.05;
Phi_h_Bin_Values[6][1][0] =  24; Phi_h_Bin_Values[6][1][1] = 0; Phi_h_Bin_Values[6][1][2] = 3876;
z_pT_Bin_Borders[6][2][0] = 0.72; z_pT_Bin_Borders[6][2][1] = 0.45; z_pT_Bin_Borders[6][2][2] = 0.32; z_pT_Bin_Borders[6][2][3] = 0.22;
Phi_h_Bin_Values[6][2][0] =  24; Phi_h_Bin_Values[6][2][1] = 24; Phi_h_Bin_Values[6][2][2] = 3900;
z_pT_Bin_Borders[6][3][0] = 0.72; z_pT_Bin_Borders[6][3][1] = 0.45; z_pT_Bin_Borders[6][3][2] = 0.41; z_pT_Bin_Borders[6][3][3] = 0.32;
Phi_h_Bin_Values[6][3][0] =  24; Phi_h_Bin_Values[6][3][1] = 48; Phi_h_Bin_Values[6][3][2] = 3924;
z_pT_Bin_Borders[6][4][0] = 0.72; z_pT_Bin_Borders[6][4][1] = 0.45; z_pT_Bin_Borders[6][4][2] = 0.51; z_pT_Bin_Borders[6][4][3] = 0.41;
Phi_h_Bin_Values[6][4][0] =  24; Phi_h_Bin_Values[6][4][1] = 72; Phi_h_Bin_Values[6][4][2] = 3948;
z_pT_Bin_Borders[6][5][0] = 0.72; z_pT_Bin_Borders[6][5][1] = 0.45; z_pT_Bin_Borders[6][5][2] = 0.65; z_pT_Bin_Borders[6][5][3] = 0.51;
Phi_h_Bin_Values[6][5][0] =  24; Phi_h_Bin_Values[6][5][1] = 96; Phi_h_Bin_Values[6][5][2] = 3972;
z_pT_Bin_Borders[6][6][0] = 0.72; z_pT_Bin_Borders[6][6][1] = 0.45; z_pT_Bin_Borders[6][6][2] = 1.0; z_pT_Bin_Borders[6][6][3] = 0.65;
Phi_h_Bin_Values[6][6][0] =  24; Phi_h_Bin_Values[6][6][1] = 120; Phi_h_Bin_Values[6][6][2] = 3996;
z_pT_Bin_Borders[6][7][0] = 0.45; z_pT_Bin_Borders[6][7][1] = 0.35; z_pT_Bin_Borders[6][7][2] = 0.22; z_pT_Bin_Borders[6][7][3] = 0.05;
Phi_h_Bin_Values[6][7][0] =  24; Phi_h_Bin_Values[6][7][1] = 144; Phi_h_Bin_Values[6][7][2] = 4020;
z_pT_Bin_Borders[6][8][0] = 0.45; z_pT_Bin_Borders[6][8][1] = 0.35; z_pT_Bin_Borders[6][8][2] = 0.32; z_pT_Bin_Borders[6][8][3] = 0.22;
Phi_h_Bin_Values[6][8][0] =  24; Phi_h_Bin_Values[6][8][1] = 168; Phi_h_Bin_Values[6][8][2] = 4044;
z_pT_Bin_Borders[6][9][0] = 0.45; z_pT_Bin_Borders[6][9][1] = 0.35; z_pT_Bin_Borders[6][9][2] = 0.41; z_pT_Bin_Borders[6][9][3] = 0.32;
Phi_h_Bin_Values[6][9][0] =  24; Phi_h_Bin_Values[6][9][1] = 192; Phi_h_Bin_Values[6][9][2] = 4068;
z_pT_Bin_Borders[6][10][0] = 0.45; z_pT_Bin_Borders[6][10][1] = 0.35; z_pT_Bin_Borders[6][10][2] = 0.51; z_pT_Bin_Borders[6][10][3] = 0.41;
Phi_h_Bin_Values[6][10][0] =  24; Phi_h_Bin_Values[6][10][1] = 216; Phi_h_Bin_Values[6][10][2] = 4092;
z_pT_Bin_Borders[6][11][0] = 0.45; z_pT_Bin_Borders[6][11][1] = 0.35; z_pT_Bin_Borders[6][11][2] = 0.65; z_pT_Bin_Borders[6][11][3] = 0.51;
Phi_h_Bin_Values[6][11][0] =  24; Phi_h_Bin_Values[6][11][1] = 240; Phi_h_Bin_Values[6][11][2] = 4116;
z_pT_Bin_Borders[6][12][0] = 0.45; z_pT_Bin_Borders[6][12][1] = 0.35; z_pT_Bin_Borders[6][12][2] = 1.0; z_pT_Bin_Borders[6][12][3] = 0.65;
Phi_h_Bin_Values[6][12][0] =  24; Phi_h_Bin_Values[6][12][1] = 264; Phi_h_Bin_Values[6][12][2] = 4140;
z_pT_Bin_Borders[6][13][0] = 0.35; z_pT_Bin_Borders[6][13][1] = 0.28; z_pT_Bin_Borders[6][13][2] = 0.22; z_pT_Bin_Borders[6][13][3] = 0.05;
Phi_h_Bin_Values[6][13][0] =  24; Phi_h_Bin_Values[6][13][1] = 288; Phi_h_Bin_Values[6][13][2] = 4164;
z_pT_Bin_Borders[6][14][0] = 0.35; z_pT_Bin_Borders[6][14][1] = 0.28; z_pT_Bin_Borders[6][14][2] = 0.32; z_pT_Bin_Borders[6][14][3] = 0.22;
Phi_h_Bin_Values[6][14][0] =  24; Phi_h_Bin_Values[6][14][1] = 312; Phi_h_Bin_Values[6][14][2] = 4188;
z_pT_Bin_Borders[6][15][0] = 0.35; z_pT_Bin_Borders[6][15][1] = 0.28; z_pT_Bin_Borders[6][15][2] = 0.41; z_pT_Bin_Borders[6][15][3] = 0.32;
Phi_h_Bin_Values[6][15][0] =  24; Phi_h_Bin_Values[6][15][1] = 336; Phi_h_Bin_Values[6][15][2] = 4212;
z_pT_Bin_Borders[6][16][0] = 0.35; z_pT_Bin_Borders[6][16][1] = 0.28; z_pT_Bin_Borders[6][16][2] = 0.51; z_pT_Bin_Borders[6][16][3] = 0.41;
Phi_h_Bin_Values[6][16][0] =  24; Phi_h_Bin_Values[6][16][1] = 360; Phi_h_Bin_Values[6][16][2] = 4236;
z_pT_Bin_Borders[6][17][0] = 0.35; z_pT_Bin_Borders[6][17][1] = 0.28; z_pT_Bin_Borders[6][17][2] = 0.65; z_pT_Bin_Borders[6][17][3] = 0.51;
Phi_h_Bin_Values[6][17][0] =  24; Phi_h_Bin_Values[6][17][1] = 384; Phi_h_Bin_Values[6][17][2] = 4260;
z_pT_Bin_Borders[6][18][0] = 0.35; z_pT_Bin_Borders[6][18][1] = 0.28; z_pT_Bin_Borders[6][18][2] = 1.0; z_pT_Bin_Borders[6][18][3] = 0.65;
Phi_h_Bin_Values[6][18][0] =  1; Phi_h_Bin_Values[6][18][1] = 408; Phi_h_Bin_Values[6][18][2] = 4284;
z_pT_Bin_Borders[6][19][0] = 0.28; z_pT_Bin_Borders[6][19][1] = 0.23; z_pT_Bin_Borders[6][19][2] = 0.22; z_pT_Bin_Borders[6][19][3] = 0.05;
Phi_h_Bin_Values[6][19][0] =  24; Phi_h_Bin_Values[6][19][1] = 409; Phi_h_Bin_Values[6][19][2] = 4285;
z_pT_Bin_Borders[6][20][0] = 0.28; z_pT_Bin_Borders[6][20][1] = 0.23; z_pT_Bin_Borders[6][20][2] = 0.32; z_pT_Bin_Borders[6][20][3] = 0.22;
Phi_h_Bin_Values[6][20][0] =  24; Phi_h_Bin_Values[6][20][1] = 433; Phi_h_Bin_Values[6][20][2] = 4309;
z_pT_Bin_Borders[6][21][0] = 0.28; z_pT_Bin_Borders[6][21][1] = 0.23; z_pT_Bin_Borders[6][21][2] = 0.41; z_pT_Bin_Borders[6][21][3] = 0.32;
Phi_h_Bin_Values[6][21][0] =  24; Phi_h_Bin_Values[6][21][1] = 457; Phi_h_Bin_Values[6][21][2] = 4333;
z_pT_Bin_Borders[6][22][0] = 0.28; z_pT_Bin_Borders[6][22][1] = 0.23; z_pT_Bin_Borders[6][22][2] = 0.51; z_pT_Bin_Borders[6][22][3] = 0.41;
Phi_h_Bin_Values[6][22][0] =  24; Phi_h_Bin_Values[6][22][1] = 481; Phi_h_Bin_Values[6][22][2] = 4357;
z_pT_Bin_Borders[6][23][0] = 0.28; z_pT_Bin_Borders[6][23][1] = 0.23; z_pT_Bin_Borders[6][23][2] = 0.65; z_pT_Bin_Borders[6][23][3] = 0.51;
Phi_h_Bin_Values[6][23][0] =  24; Phi_h_Bin_Values[6][23][1] = 505; Phi_h_Bin_Values[6][23][2] = 4381;
z_pT_Bin_Borders[6][24][0] = 0.28; z_pT_Bin_Borders[6][24][1] = 0.23; z_pT_Bin_Borders[6][24][2] = 1.0; z_pT_Bin_Borders[6][24][3] = 0.65;
Phi_h_Bin_Values[6][24][0] =  1; Phi_h_Bin_Values[6][24][1] = 529; Phi_h_Bin_Values[6][24][2] = 4405;
z_pT_Bin_Borders[6][25][0] = 0.23; z_pT_Bin_Borders[6][25][1] = 0.18; z_pT_Bin_Borders[6][25][2] = 0.22; z_pT_Bin_Borders[6][25][3] = 0.05;
Phi_h_Bin_Values[6][25][0] =  24; Phi_h_Bin_Values[6][25][1] = 530; Phi_h_Bin_Values[6][25][2] = 4406;
z_pT_Bin_Borders[6][26][0] = 0.23; z_pT_Bin_Borders[6][26][1] = 0.18; z_pT_Bin_Borders[6][26][2] = 0.32; z_pT_Bin_Borders[6][26][3] = 0.22;
Phi_h_Bin_Values[6][26][0] =  24; Phi_h_Bin_Values[6][26][1] = 554; Phi_h_Bin_Values[6][26][2] = 4430;
z_pT_Bin_Borders[6][27][0] = 0.23; z_pT_Bin_Borders[6][27][1] = 0.18; z_pT_Bin_Borders[6][27][2] = 0.41; z_pT_Bin_Borders[6][27][3] = 0.32;
Phi_h_Bin_Values[6][27][0] =  24; Phi_h_Bin_Values[6][27][1] = 578; Phi_h_Bin_Values[6][27][2] = 4454;
z_pT_Bin_Borders[6][28][0] = 0.23; z_pT_Bin_Borders[6][28][1] = 0.18; z_pT_Bin_Borders[6][28][2] = 0.51; z_pT_Bin_Borders[6][28][3] = 0.41;
Phi_h_Bin_Values[6][28][0] =  24; Phi_h_Bin_Values[6][28][1] = 602; Phi_h_Bin_Values[6][28][2] = 4478;
z_pT_Bin_Borders[6][29][0] = 0.23; z_pT_Bin_Borders[6][29][1] = 0.18; z_pT_Bin_Borders[6][29][2] = 0.65; z_pT_Bin_Borders[6][29][3] = 0.51;
Phi_h_Bin_Values[6][29][0] =  1; Phi_h_Bin_Values[6][29][1] = 626; Phi_h_Bin_Values[6][29][2] = 4502;
z_pT_Bin_Borders[6][30][0] = 0.23; z_pT_Bin_Borders[6][30][1] = 0.18; z_pT_Bin_Borders[6][30][2] = 1.0; z_pT_Bin_Borders[6][30][3] = 0.65;
Phi_h_Bin_Values[6][30][0] =  1; Phi_h_Bin_Values[6][30][1] = 627; Phi_h_Bin_Values[6][30][2] = 4503;
z_pT_Bin_Borders[6][31][0] = 10; z_pT_Bin_Borders[6][31][1] = 0.72; z_pT_Bin_Borders[6][31][2] = 0.05; z_pT_Bin_Borders[6][31][3] = 0;
Phi_h_Bin_Values[6][31][0] =  1; Phi_h_Bin_Values[6][31][1] = 628; Phi_h_Bin_Values[6][31][2] = 4504;
z_pT_Bin_Borders[6][32][0] = 10; z_pT_Bin_Borders[6][32][1] = 0.72; z_pT_Bin_Borders[6][32][2] = 0.22; z_pT_Bin_Borders[6][32][3] = 0.05;
Phi_h_Bin_Values[6][32][0] =  1; Phi_h_Bin_Values[6][32][1] = 629; Phi_h_Bin_Values[6][32][2] = 4505;
z_pT_Bin_Borders[6][33][0] = 10; z_pT_Bin_Borders[6][33][1] = 0.72; z_pT_Bin_Borders[6][33][2] = 0.32; z_pT_Bin_Borders[6][33][3] = 0.22;
Phi_h_Bin_Values[6][33][0] =  1; Phi_h_Bin_Values[6][33][1] = 630; Phi_h_Bin_Values[6][33][2] = 4506;
z_pT_Bin_Borders[6][34][0] = 10; z_pT_Bin_Borders[6][34][1] = 0.72; z_pT_Bin_Borders[6][34][2] = 0.41; z_pT_Bin_Borders[6][34][3] = 0.32;
Phi_h_Bin_Values[6][34][0] =  1; Phi_h_Bin_Values[6][34][1] = 631; Phi_h_Bin_Values[6][34][2] = 4507;
z_pT_Bin_Borders[6][35][0] = 10; z_pT_Bin_Borders[6][35][1] = 0.72; z_pT_Bin_Borders[6][35][2] = 0.51; z_pT_Bin_Borders[6][35][3] = 0.41;
Phi_h_Bin_Values[6][35][0] =  1; Phi_h_Bin_Values[6][35][1] = 632; Phi_h_Bin_Values[6][35][2] = 4508;
z_pT_Bin_Borders[6][36][0] = 10; z_pT_Bin_Borders[6][36][1] = 0.72; z_pT_Bin_Borders[6][36][2] = 0.65; z_pT_Bin_Borders[6][36][3] = 0.51;
Phi_h_Bin_Values[6][36][0] =  1; Phi_h_Bin_Values[6][36][1] = 633; Phi_h_Bin_Values[6][36][2] = 4509;
z_pT_Bin_Borders[6][37][0] = 10; z_pT_Bin_Borders[6][37][1] = 0.72; z_pT_Bin_Borders[6][37][2] = 1.0; z_pT_Bin_Borders[6][37][3] = 0.65;
Phi_h_Bin_Values[6][37][0] =  1; Phi_h_Bin_Values[6][37][1] = 634; Phi_h_Bin_Values[6][37][2] = 4510;
z_pT_Bin_Borders[6][38][0] = 10; z_pT_Bin_Borders[6][38][1] = 0.72; z_pT_Bin_Borders[6][38][2] = 10; z_pT_Bin_Borders[6][38][3] = 1.0;
Phi_h_Bin_Values[6][38][0] =  1; Phi_h_Bin_Values[6][38][1] = 635; Phi_h_Bin_Values[6][38][2] = 4511;
z_pT_Bin_Borders[6][39][0] = 0.72; z_pT_Bin_Borders[6][39][1] = 0.45; z_pT_Bin_Borders[6][39][2] = 0.05; z_pT_Bin_Borders[6][39][3] = 0;
Phi_h_Bin_Values[6][39][0] =  1; Phi_h_Bin_Values[6][39][1] = 636; Phi_h_Bin_Values[6][39][2] = 4512;
z_pT_Bin_Borders[6][40][0] = 0.72; z_pT_Bin_Borders[6][40][1] = 0.45; z_pT_Bin_Borders[6][40][2] = 10; z_pT_Bin_Borders[6][40][3] = 1.0;
Phi_h_Bin_Values[6][40][0] =  1; Phi_h_Bin_Values[6][40][1] = 637; Phi_h_Bin_Values[6][40][2] = 4513;
z_pT_Bin_Borders[6][41][0] = 0.45; z_pT_Bin_Borders[6][41][1] = 0.35; z_pT_Bin_Borders[6][41][2] = 0.05; z_pT_Bin_Borders[6][41][3] = 0;
Phi_h_Bin_Values[6][41][0] =  1; Phi_h_Bin_Values[6][41][1] = 638; Phi_h_Bin_Values[6][41][2] = 4514;
z_pT_Bin_Borders[6][42][0] = 0.45; z_pT_Bin_Borders[6][42][1] = 0.35; z_pT_Bin_Borders[6][42][2] = 10; z_pT_Bin_Borders[6][42][3] = 1.0;
Phi_h_Bin_Values[6][42][0] =  1; Phi_h_Bin_Values[6][42][1] = 639; Phi_h_Bin_Values[6][42][2] = 4515;
z_pT_Bin_Borders[6][43][0] = 0.35; z_pT_Bin_Borders[6][43][1] = 0.28; z_pT_Bin_Borders[6][43][2] = 0.05; z_pT_Bin_Borders[6][43][3] = 0;
Phi_h_Bin_Values[6][43][0] =  1; Phi_h_Bin_Values[6][43][1] = 640; Phi_h_Bin_Values[6][43][2] = 4516;
z_pT_Bin_Borders[6][44][0] = 0.35; z_pT_Bin_Borders[6][44][1] = 0.28; z_pT_Bin_Borders[6][44][2] = 10; z_pT_Bin_Borders[6][44][3] = 1.0;
Phi_h_Bin_Values[6][44][0] =  1; Phi_h_Bin_Values[6][44][1] = 641; Phi_h_Bin_Values[6][44][2] = 4517;
z_pT_Bin_Borders[6][45][0] = 0.28; z_pT_Bin_Borders[6][45][1] = 0.23; z_pT_Bin_Borders[6][45][2] = 0.05; z_pT_Bin_Borders[6][45][3] = 0;
Phi_h_Bin_Values[6][45][0] =  1; Phi_h_Bin_Values[6][45][1] = 642; Phi_h_Bin_Values[6][45][2] = 4518;
z_pT_Bin_Borders[6][46][0] = 0.28; z_pT_Bin_Borders[6][46][1] = 0.23; z_pT_Bin_Borders[6][46][2] = 10; z_pT_Bin_Borders[6][46][3] = 1.0;
Phi_h_Bin_Values[6][46][0] =  1; Phi_h_Bin_Values[6][46][1] = 643; Phi_h_Bin_Values[6][46][2] = 4519;
z_pT_Bin_Borders[6][47][0] = 0.23; z_pT_Bin_Borders[6][47][1] = 0.18; z_pT_Bin_Borders[6][47][2] = 0.05; z_pT_Bin_Borders[6][47][3] = 0;
Phi_h_Bin_Values[6][47][0] =  1; Phi_h_Bin_Values[6][47][1] = 644; Phi_h_Bin_Values[6][47][2] = 4520;
z_pT_Bin_Borders[6][48][0] = 0.23; z_pT_Bin_Borders[6][48][1] = 0.18; z_pT_Bin_Borders[6][48][2] = 10; z_pT_Bin_Borders[6][48][3] = 1.0;
Phi_h_Bin_Values[6][48][0] =  1; Phi_h_Bin_Values[6][48][1] = 645; Phi_h_Bin_Values[6][48][2] = 4521;
z_pT_Bin_Borders[6][49][0] = 0.18; z_pT_Bin_Borders[6][49][1] = 0; z_pT_Bin_Borders[6][49][2] = 0.05; z_pT_Bin_Borders[6][49][3] = 0;
Phi_h_Bin_Values[6][49][0] =  1; Phi_h_Bin_Values[6][49][1] = 646; Phi_h_Bin_Values[6][49][2] = 4522;
z_pT_Bin_Borders[6][50][0] = 0.18; z_pT_Bin_Borders[6][50][1] = 0; z_pT_Bin_Borders[6][50][2] = 0.22; z_pT_Bin_Borders[6][50][3] = 0.05;
Phi_h_Bin_Values[6][50][0] =  1; Phi_h_Bin_Values[6][50][1] = 647; Phi_h_Bin_Values[6][50][2] = 4523;
z_pT_Bin_Borders[6][51][0] = 0.18; z_pT_Bin_Borders[6][51][1] = 0; z_pT_Bin_Borders[6][51][2] = 0.32; z_pT_Bin_Borders[6][51][3] = 0.22;
Phi_h_Bin_Values[6][51][0] =  1; Phi_h_Bin_Values[6][51][1] = 648; Phi_h_Bin_Values[6][51][2] = 4524;
z_pT_Bin_Borders[6][52][0] = 0.18; z_pT_Bin_Borders[6][52][1] = 0; z_pT_Bin_Borders[6][52][2] = 0.41; z_pT_Bin_Borders[6][52][3] = 0.32;
Phi_h_Bin_Values[6][52][0] =  1; Phi_h_Bin_Values[6][52][1] = 649; Phi_h_Bin_Values[6][52][2] = 4525;
z_pT_Bin_Borders[6][53][0] = 0.18; z_pT_Bin_Borders[6][53][1] = 0; z_pT_Bin_Borders[6][53][2] = 0.51; z_pT_Bin_Borders[6][53][3] = 0.41;
Phi_h_Bin_Values[6][53][0] =  1; Phi_h_Bin_Values[6][53][1] = 650; Phi_h_Bin_Values[6][53][2] = 4526;
z_pT_Bin_Borders[6][54][0] = 0.18; z_pT_Bin_Borders[6][54][1] = 0; z_pT_Bin_Borders[6][54][2] = 0.65; z_pT_Bin_Borders[6][54][3] = 0.51;
Phi_h_Bin_Values[6][54][0] =  1; Phi_h_Bin_Values[6][54][1] = 651; Phi_h_Bin_Values[6][54][2] = 4527;
z_pT_Bin_Borders[6][55][0] = 0.18; z_pT_Bin_Borders[6][55][1] = 0; z_pT_Bin_Borders[6][55][2] = 1.0; z_pT_Bin_Borders[6][55][3] = 0.65;
Phi_h_Bin_Values[6][55][0] =  1; Phi_h_Bin_Values[6][55][1] = 652; Phi_h_Bin_Values[6][55][2] = 4528;
z_pT_Bin_Borders[6][56][0] = 0.18; z_pT_Bin_Borders[6][56][1] = 0; z_pT_Bin_Borders[6][56][2] = 10; z_pT_Bin_Borders[6][56][3] = 1.0;
Phi_h_Bin_Values[6][56][0] =  1; Phi_h_Bin_Values[6][56][1] = 653; Phi_h_Bin_Values[6][56][2] = 4529;
z_pT_Bin_Borders[7][1][0] = 0.77; z_pT_Bin_Borders[7][1][1] = 0.58; z_pT_Bin_Borders[7][1][2] = 0.2; z_pT_Bin_Borders[7][1][3] = 0.05;
Phi_h_Bin_Values[7][1][0] =  24; Phi_h_Bin_Values[7][1][1] = 0; Phi_h_Bin_Values[7][1][2] = 4530;
z_pT_Bin_Borders[7][2][0] = 0.77; z_pT_Bin_Borders[7][2][1] = 0.58; z_pT_Bin_Borders[7][2][2] = 0.29; z_pT_Bin_Borders[7][2][3] = 0.2;
Phi_h_Bin_Values[7][2][0] =  24; Phi_h_Bin_Values[7][2][1] = 24; Phi_h_Bin_Values[7][2][2] = 4554;
z_pT_Bin_Borders[7][3][0] = 0.77; z_pT_Bin_Borders[7][3][1] = 0.58; z_pT_Bin_Borders[7][3][2] = 0.38; z_pT_Bin_Borders[7][3][3] = 0.29;
Phi_h_Bin_Values[7][3][0] =  24; Phi_h_Bin_Values[7][3][1] = 48; Phi_h_Bin_Values[7][3][2] = 4578;
z_pT_Bin_Borders[7][4][0] = 0.77; z_pT_Bin_Borders[7][4][1] = 0.58; z_pT_Bin_Borders[7][4][2] = 0.48; z_pT_Bin_Borders[7][4][3] = 0.38;
Phi_h_Bin_Values[7][4][0] =  24; Phi_h_Bin_Values[7][4][1] = 72; Phi_h_Bin_Values[7][4][2] = 4602;
z_pT_Bin_Borders[7][5][0] = 0.77; z_pT_Bin_Borders[7][5][1] = 0.58; z_pT_Bin_Borders[7][5][2] = 0.6; z_pT_Bin_Borders[7][5][3] = 0.48;
Phi_h_Bin_Values[7][5][0] =  24; Phi_h_Bin_Values[7][5][1] = 96; Phi_h_Bin_Values[7][5][2] = 4626;
z_pT_Bin_Borders[7][6][0] = 0.77; z_pT_Bin_Borders[7][6][1] = 0.58; z_pT_Bin_Borders[7][6][2] = 0.83; z_pT_Bin_Borders[7][6][3] = 0.6;
Phi_h_Bin_Values[7][6][0] =  1; Phi_h_Bin_Values[7][6][1] = 120; Phi_h_Bin_Values[7][6][2] = 4650;
z_pT_Bin_Borders[7][7][0] = 0.58; z_pT_Bin_Borders[7][7][1] = 0.45; z_pT_Bin_Borders[7][7][2] = 0.2; z_pT_Bin_Borders[7][7][3] = 0.05;
Phi_h_Bin_Values[7][7][0] =  24; Phi_h_Bin_Values[7][7][1] = 121; Phi_h_Bin_Values[7][7][2] = 4651;
z_pT_Bin_Borders[7][8][0] = 0.58; z_pT_Bin_Borders[7][8][1] = 0.45; z_pT_Bin_Borders[7][8][2] = 0.29; z_pT_Bin_Borders[7][8][3] = 0.2;
Phi_h_Bin_Values[7][8][0] =  24; Phi_h_Bin_Values[7][8][1] = 145; Phi_h_Bin_Values[7][8][2] = 4675;
z_pT_Bin_Borders[7][9][0] = 0.58; z_pT_Bin_Borders[7][9][1] = 0.45; z_pT_Bin_Borders[7][9][2] = 0.38; z_pT_Bin_Borders[7][9][3] = 0.29;
Phi_h_Bin_Values[7][9][0] =  24; Phi_h_Bin_Values[7][9][1] = 169; Phi_h_Bin_Values[7][9][2] = 4699;
z_pT_Bin_Borders[7][10][0] = 0.58; z_pT_Bin_Borders[7][10][1] = 0.45; z_pT_Bin_Borders[7][10][2] = 0.48; z_pT_Bin_Borders[7][10][3] = 0.38;
Phi_h_Bin_Values[7][10][0] =  24; Phi_h_Bin_Values[7][10][1] = 193; Phi_h_Bin_Values[7][10][2] = 4723;
z_pT_Bin_Borders[7][11][0] = 0.58; z_pT_Bin_Borders[7][11][1] = 0.45; z_pT_Bin_Borders[7][11][2] = 0.6; z_pT_Bin_Borders[7][11][3] = 0.48;
Phi_h_Bin_Values[7][11][0] =  24; Phi_h_Bin_Values[7][11][1] = 217; Phi_h_Bin_Values[7][11][2] = 4747;
z_pT_Bin_Borders[7][12][0] = 0.58; z_pT_Bin_Borders[7][12][1] = 0.45; z_pT_Bin_Borders[7][12][2] = 0.83; z_pT_Bin_Borders[7][12][3] = 0.6;
Phi_h_Bin_Values[7][12][0] =  24; Phi_h_Bin_Values[7][12][1] = 241; Phi_h_Bin_Values[7][12][2] = 4771;
z_pT_Bin_Borders[7][13][0] = 0.45; z_pT_Bin_Borders[7][13][1] = 0.37; z_pT_Bin_Borders[7][13][2] = 0.2; z_pT_Bin_Borders[7][13][3] = 0.05;
Phi_h_Bin_Values[7][13][0] =  24; Phi_h_Bin_Values[7][13][1] = 265; Phi_h_Bin_Values[7][13][2] = 4795;
z_pT_Bin_Borders[7][14][0] = 0.45; z_pT_Bin_Borders[7][14][1] = 0.37; z_pT_Bin_Borders[7][14][2] = 0.29; z_pT_Bin_Borders[7][14][3] = 0.2;
Phi_h_Bin_Values[7][14][0] =  24; Phi_h_Bin_Values[7][14][1] = 289; Phi_h_Bin_Values[7][14][2] = 4819;
z_pT_Bin_Borders[7][15][0] = 0.45; z_pT_Bin_Borders[7][15][1] = 0.37; z_pT_Bin_Borders[7][15][2] = 0.38; z_pT_Bin_Borders[7][15][3] = 0.29;
Phi_h_Bin_Values[7][15][0] =  24; Phi_h_Bin_Values[7][15][1] = 313; Phi_h_Bin_Values[7][15][2] = 4843;
z_pT_Bin_Borders[7][16][0] = 0.45; z_pT_Bin_Borders[7][16][1] = 0.37; z_pT_Bin_Borders[7][16][2] = 0.48; z_pT_Bin_Borders[7][16][3] = 0.38;
Phi_h_Bin_Values[7][16][0] =  24; Phi_h_Bin_Values[7][16][1] = 337; Phi_h_Bin_Values[7][16][2] = 4867;
z_pT_Bin_Borders[7][17][0] = 0.45; z_pT_Bin_Borders[7][17][1] = 0.37; z_pT_Bin_Borders[7][17][2] = 0.6; z_pT_Bin_Borders[7][17][3] = 0.48;
Phi_h_Bin_Values[7][17][0] =  24; Phi_h_Bin_Values[7][17][1] = 361; Phi_h_Bin_Values[7][17][2] = 4891;
z_pT_Bin_Borders[7][18][0] = 0.45; z_pT_Bin_Borders[7][18][1] = 0.37; z_pT_Bin_Borders[7][18][2] = 0.83; z_pT_Bin_Borders[7][18][3] = 0.6;
Phi_h_Bin_Values[7][18][0] =  24; Phi_h_Bin_Values[7][18][1] = 385; Phi_h_Bin_Values[7][18][2] = 4915;
z_pT_Bin_Borders[7][19][0] = 0.37; z_pT_Bin_Borders[7][19][1] = 0.31; z_pT_Bin_Borders[7][19][2] = 0.2; z_pT_Bin_Borders[7][19][3] = 0.05;
Phi_h_Bin_Values[7][19][0] =  24; Phi_h_Bin_Values[7][19][1] = 409; Phi_h_Bin_Values[7][19][2] = 4939;
z_pT_Bin_Borders[7][20][0] = 0.37; z_pT_Bin_Borders[7][20][1] = 0.31; z_pT_Bin_Borders[7][20][2] = 0.29; z_pT_Bin_Borders[7][20][3] = 0.2;
Phi_h_Bin_Values[7][20][0] =  24; Phi_h_Bin_Values[7][20][1] = 433; Phi_h_Bin_Values[7][20][2] = 4963;
z_pT_Bin_Borders[7][21][0] = 0.37; z_pT_Bin_Borders[7][21][1] = 0.31; z_pT_Bin_Borders[7][21][2] = 0.38; z_pT_Bin_Borders[7][21][3] = 0.29;
Phi_h_Bin_Values[7][21][0] =  24; Phi_h_Bin_Values[7][21][1] = 457; Phi_h_Bin_Values[7][21][2] = 4987;
z_pT_Bin_Borders[7][22][0] = 0.37; z_pT_Bin_Borders[7][22][1] = 0.31; z_pT_Bin_Borders[7][22][2] = 0.48; z_pT_Bin_Borders[7][22][3] = 0.38;
Phi_h_Bin_Values[7][22][0] =  24; Phi_h_Bin_Values[7][22][1] = 481; Phi_h_Bin_Values[7][22][2] = 5011;
z_pT_Bin_Borders[7][23][0] = 0.37; z_pT_Bin_Borders[7][23][1] = 0.31; z_pT_Bin_Borders[7][23][2] = 0.6; z_pT_Bin_Borders[7][23][3] = 0.48;
Phi_h_Bin_Values[7][23][0] =  24; Phi_h_Bin_Values[7][23][1] = 505; Phi_h_Bin_Values[7][23][2] = 5035;
z_pT_Bin_Borders[7][24][0] = 0.37; z_pT_Bin_Borders[7][24][1] = 0.31; z_pT_Bin_Borders[7][24][2] = 0.83; z_pT_Bin_Borders[7][24][3] = 0.6;
Phi_h_Bin_Values[7][24][0] =  24; Phi_h_Bin_Values[7][24][1] = 529; Phi_h_Bin_Values[7][24][2] = 5059;
z_pT_Bin_Borders[7][25][0] = 0.31; z_pT_Bin_Borders[7][25][1] = 0.27; z_pT_Bin_Borders[7][25][2] = 0.2; z_pT_Bin_Borders[7][25][3] = 0.05;
Phi_h_Bin_Values[7][25][0] =  24; Phi_h_Bin_Values[7][25][1] = 553; Phi_h_Bin_Values[7][25][2] = 5083;
z_pT_Bin_Borders[7][26][0] = 0.31; z_pT_Bin_Borders[7][26][1] = 0.27; z_pT_Bin_Borders[7][26][2] = 0.29; z_pT_Bin_Borders[7][26][3] = 0.2;
Phi_h_Bin_Values[7][26][0] =  24; Phi_h_Bin_Values[7][26][1] = 577; Phi_h_Bin_Values[7][26][2] = 5107;
z_pT_Bin_Borders[7][27][0] = 0.31; z_pT_Bin_Borders[7][27][1] = 0.27; z_pT_Bin_Borders[7][27][2] = 0.38; z_pT_Bin_Borders[7][27][3] = 0.29;
Phi_h_Bin_Values[7][27][0] =  24; Phi_h_Bin_Values[7][27][1] = 601; Phi_h_Bin_Values[7][27][2] = 5131;
z_pT_Bin_Borders[7][28][0] = 0.31; z_pT_Bin_Borders[7][28][1] = 0.27; z_pT_Bin_Borders[7][28][2] = 0.48; z_pT_Bin_Borders[7][28][3] = 0.38;
Phi_h_Bin_Values[7][28][0] =  24; Phi_h_Bin_Values[7][28][1] = 625; Phi_h_Bin_Values[7][28][2] = 5155;
z_pT_Bin_Borders[7][29][0] = 0.31; z_pT_Bin_Borders[7][29][1] = 0.27; z_pT_Bin_Borders[7][29][2] = 0.6; z_pT_Bin_Borders[7][29][3] = 0.48;
Phi_h_Bin_Values[7][29][0] =  24; Phi_h_Bin_Values[7][29][1] = 649; Phi_h_Bin_Values[7][29][2] = 5179;
z_pT_Bin_Borders[7][30][0] = 0.31; z_pT_Bin_Borders[7][30][1] = 0.27; z_pT_Bin_Borders[7][30][2] = 0.83; z_pT_Bin_Borders[7][30][3] = 0.6;
Phi_h_Bin_Values[7][30][0] =  1; Phi_h_Bin_Values[7][30][1] = 673; Phi_h_Bin_Values[7][30][2] = 5203;
z_pT_Bin_Borders[7][31][0] = 0.27; z_pT_Bin_Borders[7][31][1] = 0.22; z_pT_Bin_Borders[7][31][2] = 0.2; z_pT_Bin_Borders[7][31][3] = 0.05;
Phi_h_Bin_Values[7][31][0] =  24; Phi_h_Bin_Values[7][31][1] = 674; Phi_h_Bin_Values[7][31][2] = 5204;
z_pT_Bin_Borders[7][32][0] = 0.27; z_pT_Bin_Borders[7][32][1] = 0.22; z_pT_Bin_Borders[7][32][2] = 0.29; z_pT_Bin_Borders[7][32][3] = 0.2;
Phi_h_Bin_Values[7][32][0] =  24; Phi_h_Bin_Values[7][32][1] = 698; Phi_h_Bin_Values[7][32][2] = 5228;
z_pT_Bin_Borders[7][33][0] = 0.27; z_pT_Bin_Borders[7][33][1] = 0.22; z_pT_Bin_Borders[7][33][2] = 0.38; z_pT_Bin_Borders[7][33][3] = 0.29;
Phi_h_Bin_Values[7][33][0] =  24; Phi_h_Bin_Values[7][33][1] = 722; Phi_h_Bin_Values[7][33][2] = 5252;
z_pT_Bin_Borders[7][34][0] = 0.27; z_pT_Bin_Borders[7][34][1] = 0.22; z_pT_Bin_Borders[7][34][2] = 0.48; z_pT_Bin_Borders[7][34][3] = 0.38;
Phi_h_Bin_Values[7][34][0] =  24; Phi_h_Bin_Values[7][34][1] = 746; Phi_h_Bin_Values[7][34][2] = 5276;
z_pT_Bin_Borders[7][35][0] = 0.27; z_pT_Bin_Borders[7][35][1] = 0.22; z_pT_Bin_Borders[7][35][2] = 0.6; z_pT_Bin_Borders[7][35][3] = 0.48;
Phi_h_Bin_Values[7][35][0] =  24; Phi_h_Bin_Values[7][35][1] = 770; Phi_h_Bin_Values[7][35][2] = 5300;
z_pT_Bin_Borders[7][36][0] = 0.27; z_pT_Bin_Borders[7][36][1] = 0.22; z_pT_Bin_Borders[7][36][2] = 0.83; z_pT_Bin_Borders[7][36][3] = 0.6;
Phi_h_Bin_Values[7][36][0] =  1; Phi_h_Bin_Values[7][36][1] = 794; Phi_h_Bin_Values[7][36][2] = 5324;
z_pT_Bin_Borders[7][37][0] = 10; z_pT_Bin_Borders[7][37][1] = 0.77; z_pT_Bin_Borders[7][37][2] = 0.05; z_pT_Bin_Borders[7][37][3] = 0;
Phi_h_Bin_Values[7][37][0] =  1; Phi_h_Bin_Values[7][37][1] = 795; Phi_h_Bin_Values[7][37][2] = 5325;
z_pT_Bin_Borders[7][38][0] = 10; z_pT_Bin_Borders[7][38][1] = 0.77; z_pT_Bin_Borders[7][38][2] = 0.2; z_pT_Bin_Borders[7][38][3] = 0.05;
Phi_h_Bin_Values[7][38][0] =  1; Phi_h_Bin_Values[7][38][1] = 796; Phi_h_Bin_Values[7][38][2] = 5326;
z_pT_Bin_Borders[7][39][0] = 10; z_pT_Bin_Borders[7][39][1] = 0.77; z_pT_Bin_Borders[7][39][2] = 0.29; z_pT_Bin_Borders[7][39][3] = 0.2;
Phi_h_Bin_Values[7][39][0] =  1; Phi_h_Bin_Values[7][39][1] = 797; Phi_h_Bin_Values[7][39][2] = 5327;
z_pT_Bin_Borders[7][40][0] = 10; z_pT_Bin_Borders[7][40][1] = 0.77; z_pT_Bin_Borders[7][40][2] = 0.38; z_pT_Bin_Borders[7][40][3] = 0.29;
Phi_h_Bin_Values[7][40][0] =  1; Phi_h_Bin_Values[7][40][1] = 798; Phi_h_Bin_Values[7][40][2] = 5328;
z_pT_Bin_Borders[7][41][0] = 10; z_pT_Bin_Borders[7][41][1] = 0.77; z_pT_Bin_Borders[7][41][2] = 0.48; z_pT_Bin_Borders[7][41][3] = 0.38;
Phi_h_Bin_Values[7][41][0] =  1; Phi_h_Bin_Values[7][41][1] = 799; Phi_h_Bin_Values[7][41][2] = 5329;
z_pT_Bin_Borders[7][42][0] = 10; z_pT_Bin_Borders[7][42][1] = 0.77; z_pT_Bin_Borders[7][42][2] = 0.6; z_pT_Bin_Borders[7][42][3] = 0.48;
Phi_h_Bin_Values[7][42][0] =  1; Phi_h_Bin_Values[7][42][1] = 800; Phi_h_Bin_Values[7][42][2] = 5330;
z_pT_Bin_Borders[7][43][0] = 10; z_pT_Bin_Borders[7][43][1] = 0.77; z_pT_Bin_Borders[7][43][2] = 0.83; z_pT_Bin_Borders[7][43][3] = 0.6;
Phi_h_Bin_Values[7][43][0] =  1; Phi_h_Bin_Values[7][43][1] = 801; Phi_h_Bin_Values[7][43][2] = 5331;
z_pT_Bin_Borders[7][44][0] = 10; z_pT_Bin_Borders[7][44][1] = 0.77; z_pT_Bin_Borders[7][44][2] = 10; z_pT_Bin_Borders[7][44][3] = 0.83;
Phi_h_Bin_Values[7][44][0] =  1; Phi_h_Bin_Values[7][44][1] = 802; Phi_h_Bin_Values[7][44][2] = 5332;
z_pT_Bin_Borders[7][45][0] = 0.77; z_pT_Bin_Borders[7][45][1] = 0.58; z_pT_Bin_Borders[7][45][2] = 0.05; z_pT_Bin_Borders[7][45][3] = 0;
Phi_h_Bin_Values[7][45][0] =  1; Phi_h_Bin_Values[7][45][1] = 803; Phi_h_Bin_Values[7][45][2] = 5333;
z_pT_Bin_Borders[7][46][0] = 0.77; z_pT_Bin_Borders[7][46][1] = 0.58; z_pT_Bin_Borders[7][46][2] = 10; z_pT_Bin_Borders[7][46][3] = 0.83;
Phi_h_Bin_Values[7][46][0] =  1; Phi_h_Bin_Values[7][46][1] = 804; Phi_h_Bin_Values[7][46][2] = 5334;
z_pT_Bin_Borders[7][47][0] = 0.58; z_pT_Bin_Borders[7][47][1] = 0.45; z_pT_Bin_Borders[7][47][2] = 0.05; z_pT_Bin_Borders[7][47][3] = 0;
Phi_h_Bin_Values[7][47][0] =  1; Phi_h_Bin_Values[7][47][1] = 805; Phi_h_Bin_Values[7][47][2] = 5335;
z_pT_Bin_Borders[7][48][0] = 0.58; z_pT_Bin_Borders[7][48][1] = 0.45; z_pT_Bin_Borders[7][48][2] = 10; z_pT_Bin_Borders[7][48][3] = 0.83;
Phi_h_Bin_Values[7][48][0] =  1; Phi_h_Bin_Values[7][48][1] = 806; Phi_h_Bin_Values[7][48][2] = 5336;
z_pT_Bin_Borders[7][49][0] = 0.45; z_pT_Bin_Borders[7][49][1] = 0.37; z_pT_Bin_Borders[7][49][2] = 0.05; z_pT_Bin_Borders[7][49][3] = 0;
Phi_h_Bin_Values[7][49][0] =  1; Phi_h_Bin_Values[7][49][1] = 807; Phi_h_Bin_Values[7][49][2] = 5337;
z_pT_Bin_Borders[7][50][0] = 0.45; z_pT_Bin_Borders[7][50][1] = 0.37; z_pT_Bin_Borders[7][50][2] = 10; z_pT_Bin_Borders[7][50][3] = 0.83;
Phi_h_Bin_Values[7][50][0] =  1; Phi_h_Bin_Values[7][50][1] = 808; Phi_h_Bin_Values[7][50][2] = 5338;
z_pT_Bin_Borders[7][51][0] = 0.37; z_pT_Bin_Borders[7][51][1] = 0.31; z_pT_Bin_Borders[7][51][2] = 0.05; z_pT_Bin_Borders[7][51][3] = 0;
Phi_h_Bin_Values[7][51][0] =  1; Phi_h_Bin_Values[7][51][1] = 809; Phi_h_Bin_Values[7][51][2] = 5339;
z_pT_Bin_Borders[7][52][0] = 0.37; z_pT_Bin_Borders[7][52][1] = 0.31; z_pT_Bin_Borders[7][52][2] = 10; z_pT_Bin_Borders[7][52][3] = 0.83;
Phi_h_Bin_Values[7][52][0] =  1; Phi_h_Bin_Values[7][52][1] = 810; Phi_h_Bin_Values[7][52][2] = 5340;
z_pT_Bin_Borders[7][53][0] = 0.31; z_pT_Bin_Borders[7][53][1] = 0.27; z_pT_Bin_Borders[7][53][2] = 0.05; z_pT_Bin_Borders[7][53][3] = 0;
Phi_h_Bin_Values[7][53][0] =  1; Phi_h_Bin_Values[7][53][1] = 811; Phi_h_Bin_Values[7][53][2] = 5341;
z_pT_Bin_Borders[7][54][0] = 0.31; z_pT_Bin_Borders[7][54][1] = 0.27; z_pT_Bin_Borders[7][54][2] = 10; z_pT_Bin_Borders[7][54][3] = 0.83;
Phi_h_Bin_Values[7][54][0] =  1; Phi_h_Bin_Values[7][54][1] = 812; Phi_h_Bin_Values[7][54][2] = 5342;
z_pT_Bin_Borders[7][55][0] = 0.27; z_pT_Bin_Borders[7][55][1] = 0.22; z_pT_Bin_Borders[7][55][2] = 0.05; z_pT_Bin_Borders[7][55][3] = 0;
Phi_h_Bin_Values[7][55][0] =  1; Phi_h_Bin_Values[7][55][1] = 813; Phi_h_Bin_Values[7][55][2] = 5343;
z_pT_Bin_Borders[7][56][0] = 0.27; z_pT_Bin_Borders[7][56][1] = 0.22; z_pT_Bin_Borders[7][56][2] = 10; z_pT_Bin_Borders[7][56][3] = 0.83;
Phi_h_Bin_Values[7][56][0] =  1; Phi_h_Bin_Values[7][56][1] = 814; Phi_h_Bin_Values[7][56][2] = 5344;
z_pT_Bin_Borders[7][57][0] = 0.22; z_pT_Bin_Borders[7][57][1] = 0; z_pT_Bin_Borders[7][57][2] = 0.05; z_pT_Bin_Borders[7][57][3] = 0;
Phi_h_Bin_Values[7][57][0] =  1; Phi_h_Bin_Values[7][57][1] = 815; Phi_h_Bin_Values[7][57][2] = 5345;
z_pT_Bin_Borders[7][58][0] = 0.22; z_pT_Bin_Borders[7][58][1] = 0; z_pT_Bin_Borders[7][58][2] = 0.2; z_pT_Bin_Borders[7][58][3] = 0.05;
Phi_h_Bin_Values[7][58][0] =  1; Phi_h_Bin_Values[7][58][1] = 816; Phi_h_Bin_Values[7][58][2] = 5346;
z_pT_Bin_Borders[7][59][0] = 0.22; z_pT_Bin_Borders[7][59][1] = 0; z_pT_Bin_Borders[7][59][2] = 0.29; z_pT_Bin_Borders[7][59][3] = 0.2;
Phi_h_Bin_Values[7][59][0] =  1; Phi_h_Bin_Values[7][59][1] = 817; Phi_h_Bin_Values[7][59][2] = 5347;
z_pT_Bin_Borders[7][60][0] = 0.22; z_pT_Bin_Borders[7][60][1] = 0; z_pT_Bin_Borders[7][60][2] = 0.38; z_pT_Bin_Borders[7][60][3] = 0.29;
Phi_h_Bin_Values[7][60][0] =  1; Phi_h_Bin_Values[7][60][1] = 818; Phi_h_Bin_Values[7][60][2] = 5348;
z_pT_Bin_Borders[7][61][0] = 0.22; z_pT_Bin_Borders[7][61][1] = 0; z_pT_Bin_Borders[7][61][2] = 0.48; z_pT_Bin_Borders[7][61][3] = 0.38;
Phi_h_Bin_Values[7][61][0] =  1; Phi_h_Bin_Values[7][61][1] = 819; Phi_h_Bin_Values[7][61][2] = 5349;
z_pT_Bin_Borders[7][62][0] = 0.22; z_pT_Bin_Borders[7][62][1] = 0; z_pT_Bin_Borders[7][62][2] = 0.6; z_pT_Bin_Borders[7][62][3] = 0.48;
Phi_h_Bin_Values[7][62][0] =  1; Phi_h_Bin_Values[7][62][1] = 820; Phi_h_Bin_Values[7][62][2] = 5350;
z_pT_Bin_Borders[7][63][0] = 0.22; z_pT_Bin_Borders[7][63][1] = 0; z_pT_Bin_Borders[7][63][2] = 0.83; z_pT_Bin_Borders[7][63][3] = 0.6;
Phi_h_Bin_Values[7][63][0] =  1; Phi_h_Bin_Values[7][63][1] = 821; Phi_h_Bin_Values[7][63][2] = 5351;
z_pT_Bin_Borders[7][64][0] = 0.22; z_pT_Bin_Borders[7][64][1] = 0; z_pT_Bin_Borders[7][64][2] = 10; z_pT_Bin_Borders[7][64][3] = 0.83;
Phi_h_Bin_Values[7][64][0] =  1; Phi_h_Bin_Values[7][64][1] = 822; Phi_h_Bin_Values[7][64][2] = 5352;
z_pT_Bin_Borders[8][1][0] = 0.7; z_pT_Bin_Borders[8][1][1] = 0.56; z_pT_Bin_Borders[8][1][2] = 0.2; z_pT_Bin_Borders[8][1][3] = 0.05;
Phi_h_Bin_Values[8][1][0] =  24; Phi_h_Bin_Values[8][1][1] = 0; Phi_h_Bin_Values[8][1][2] = 5353;
z_pT_Bin_Borders[8][2][0] = 0.7; z_pT_Bin_Borders[8][2][1] = 0.56; z_pT_Bin_Borders[8][2][2] = 0.29; z_pT_Bin_Borders[8][2][3] = 0.2;
Phi_h_Bin_Values[8][2][0] =  24; Phi_h_Bin_Values[8][2][1] = 24; Phi_h_Bin_Values[8][2][2] = 5377;
z_pT_Bin_Borders[8][3][0] = 0.7; z_pT_Bin_Borders[8][3][1] = 0.56; z_pT_Bin_Borders[8][3][2] = 0.37; z_pT_Bin_Borders[8][3][3] = 0.29;
Phi_h_Bin_Values[8][3][0] =  24; Phi_h_Bin_Values[8][3][1] = 48; Phi_h_Bin_Values[8][3][2] = 5401;
z_pT_Bin_Borders[8][4][0] = 0.7; z_pT_Bin_Borders[8][4][1] = 0.56; z_pT_Bin_Borders[8][4][2] = 0.46; z_pT_Bin_Borders[8][4][3] = 0.37;
Phi_h_Bin_Values[8][4][0] =  24; Phi_h_Bin_Values[8][4][1] = 72; Phi_h_Bin_Values[8][4][2] = 5425;
z_pT_Bin_Borders[8][5][0] = 0.7; z_pT_Bin_Borders[8][5][1] = 0.56; z_pT_Bin_Borders[8][5][2] = 0.6; z_pT_Bin_Borders[8][5][3] = 0.46;
Phi_h_Bin_Values[8][5][0] =  24; Phi_h_Bin_Values[8][5][1] = 96; Phi_h_Bin_Values[8][5][2] = 5449;
z_pT_Bin_Borders[8][6][0] = 0.56; z_pT_Bin_Borders[8][6][1] = 0.49; z_pT_Bin_Borders[8][6][2] = 0.2; z_pT_Bin_Borders[8][6][3] = 0.05;
Phi_h_Bin_Values[8][6][0] =  24; Phi_h_Bin_Values[8][6][1] = 120; Phi_h_Bin_Values[8][6][2] = 5473;
z_pT_Bin_Borders[8][7][0] = 0.56; z_pT_Bin_Borders[8][7][1] = 0.49; z_pT_Bin_Borders[8][7][2] = 0.29; z_pT_Bin_Borders[8][7][3] = 0.2;
Phi_h_Bin_Values[8][7][0] =  24; Phi_h_Bin_Values[8][7][1] = 144; Phi_h_Bin_Values[8][7][2] = 5497;
z_pT_Bin_Borders[8][8][0] = 0.56; z_pT_Bin_Borders[8][8][1] = 0.49; z_pT_Bin_Borders[8][8][2] = 0.37; z_pT_Bin_Borders[8][8][3] = 0.29;
Phi_h_Bin_Values[8][8][0] =  24; Phi_h_Bin_Values[8][8][1] = 168; Phi_h_Bin_Values[8][8][2] = 5521;
z_pT_Bin_Borders[8][9][0] = 0.56; z_pT_Bin_Borders[8][9][1] = 0.49; z_pT_Bin_Borders[8][9][2] = 0.46; z_pT_Bin_Borders[8][9][3] = 0.37;
Phi_h_Bin_Values[8][9][0] =  24; Phi_h_Bin_Values[8][9][1] = 192; Phi_h_Bin_Values[8][9][2] = 5545;
z_pT_Bin_Borders[8][10][0] = 0.56; z_pT_Bin_Borders[8][10][1] = 0.49; z_pT_Bin_Borders[8][10][2] = 0.6; z_pT_Bin_Borders[8][10][3] = 0.46;
Phi_h_Bin_Values[8][10][0] =  24; Phi_h_Bin_Values[8][10][1] = 216; Phi_h_Bin_Values[8][10][2] = 5569;
z_pT_Bin_Borders[8][11][0] = 0.49; z_pT_Bin_Borders[8][11][1] = 0.44; z_pT_Bin_Borders[8][11][2] = 0.2; z_pT_Bin_Borders[8][11][3] = 0.05;
Phi_h_Bin_Values[8][11][0] =  24; Phi_h_Bin_Values[8][11][1] = 240; Phi_h_Bin_Values[8][11][2] = 5593;
z_pT_Bin_Borders[8][12][0] = 0.49; z_pT_Bin_Borders[8][12][1] = 0.44; z_pT_Bin_Borders[8][12][2] = 0.29; z_pT_Bin_Borders[8][12][3] = 0.2;
Phi_h_Bin_Values[8][12][0] =  24; Phi_h_Bin_Values[8][12][1] = 264; Phi_h_Bin_Values[8][12][2] = 5617;
z_pT_Bin_Borders[8][13][0] = 0.49; z_pT_Bin_Borders[8][13][1] = 0.44; z_pT_Bin_Borders[8][13][2] = 0.37; z_pT_Bin_Borders[8][13][3] = 0.29;
Phi_h_Bin_Values[8][13][0] =  24; Phi_h_Bin_Values[8][13][1] = 288; Phi_h_Bin_Values[8][13][2] = 5641;
z_pT_Bin_Borders[8][14][0] = 0.49; z_pT_Bin_Borders[8][14][1] = 0.44; z_pT_Bin_Borders[8][14][2] = 0.46; z_pT_Bin_Borders[8][14][3] = 0.37;
Phi_h_Bin_Values[8][14][0] =  24; Phi_h_Bin_Values[8][14][1] = 312; Phi_h_Bin_Values[8][14][2] = 5665;
z_pT_Bin_Borders[8][15][0] = 0.49; z_pT_Bin_Borders[8][15][1] = 0.44; z_pT_Bin_Borders[8][15][2] = 0.6; z_pT_Bin_Borders[8][15][3] = 0.46;
Phi_h_Bin_Values[8][15][0] =  24; Phi_h_Bin_Values[8][15][1] = 336; Phi_h_Bin_Values[8][15][2] = 5689;
z_pT_Bin_Borders[8][16][0] = 0.44; z_pT_Bin_Borders[8][16][1] = 0.39; z_pT_Bin_Borders[8][16][2] = 0.2; z_pT_Bin_Borders[8][16][3] = 0.05;
Phi_h_Bin_Values[8][16][0] =  24; Phi_h_Bin_Values[8][16][1] = 360; Phi_h_Bin_Values[8][16][2] = 5713;
z_pT_Bin_Borders[8][17][0] = 0.44; z_pT_Bin_Borders[8][17][1] = 0.39; z_pT_Bin_Borders[8][17][2] = 0.29; z_pT_Bin_Borders[8][17][3] = 0.2;
Phi_h_Bin_Values[8][17][0] =  24; Phi_h_Bin_Values[8][17][1] = 384; Phi_h_Bin_Values[8][17][2] = 5737;
z_pT_Bin_Borders[8][18][0] = 0.44; z_pT_Bin_Borders[8][18][1] = 0.39; z_pT_Bin_Borders[8][18][2] = 0.37; z_pT_Bin_Borders[8][18][3] = 0.29;
Phi_h_Bin_Values[8][18][0] =  24; Phi_h_Bin_Values[8][18][1] = 408; Phi_h_Bin_Values[8][18][2] = 5761;
z_pT_Bin_Borders[8][19][0] = 0.44; z_pT_Bin_Borders[8][19][1] = 0.39; z_pT_Bin_Borders[8][19][2] = 0.46; z_pT_Bin_Borders[8][19][3] = 0.37;
Phi_h_Bin_Values[8][19][0] =  24; Phi_h_Bin_Values[8][19][1] = 432; Phi_h_Bin_Values[8][19][2] = 5785;
z_pT_Bin_Borders[8][20][0] = 0.44; z_pT_Bin_Borders[8][20][1] = 0.39; z_pT_Bin_Borders[8][20][2] = 0.6; z_pT_Bin_Borders[8][20][3] = 0.46;
Phi_h_Bin_Values[8][20][0] =  24; Phi_h_Bin_Values[8][20][1] = 456; Phi_h_Bin_Values[8][20][2] = 5809;
z_pT_Bin_Borders[8][21][0] = 0.39; z_pT_Bin_Borders[8][21][1] = 0.36; z_pT_Bin_Borders[8][21][2] = 0.2; z_pT_Bin_Borders[8][21][3] = 0.05;
Phi_h_Bin_Values[8][21][0] =  24; Phi_h_Bin_Values[8][21][1] = 480; Phi_h_Bin_Values[8][21][2] = 5833;
z_pT_Bin_Borders[8][22][0] = 0.39; z_pT_Bin_Borders[8][22][1] = 0.36; z_pT_Bin_Borders[8][22][2] = 0.29; z_pT_Bin_Borders[8][22][3] = 0.2;
Phi_h_Bin_Values[8][22][0] =  24; Phi_h_Bin_Values[8][22][1] = 504; Phi_h_Bin_Values[8][22][2] = 5857;
z_pT_Bin_Borders[8][23][0] = 0.39; z_pT_Bin_Borders[8][23][1] = 0.36; z_pT_Bin_Borders[8][23][2] = 0.37; z_pT_Bin_Borders[8][23][3] = 0.29;
Phi_h_Bin_Values[8][23][0] =  24; Phi_h_Bin_Values[8][23][1] = 528; Phi_h_Bin_Values[8][23][2] = 5881;
z_pT_Bin_Borders[8][24][0] = 0.39; z_pT_Bin_Borders[8][24][1] = 0.36; z_pT_Bin_Borders[8][24][2] = 0.46; z_pT_Bin_Borders[8][24][3] = 0.37;
Phi_h_Bin_Values[8][24][0] =  24; Phi_h_Bin_Values[8][24][1] = 552; Phi_h_Bin_Values[8][24][2] = 5905;
z_pT_Bin_Borders[8][25][0] = 0.39; z_pT_Bin_Borders[8][25][1] = 0.36; z_pT_Bin_Borders[8][25][2] = 0.6; z_pT_Bin_Borders[8][25][3] = 0.46;
Phi_h_Bin_Values[8][25][0] =  24; Phi_h_Bin_Values[8][25][1] = 576; Phi_h_Bin_Values[8][25][2] = 5929;
z_pT_Bin_Borders[8][26][0] = 0.36; z_pT_Bin_Borders[8][26][1] = 0.33; z_pT_Bin_Borders[8][26][2] = 0.2; z_pT_Bin_Borders[8][26][3] = 0.05;
Phi_h_Bin_Values[8][26][0] =  24; Phi_h_Bin_Values[8][26][1] = 600; Phi_h_Bin_Values[8][26][2] = 5953;
z_pT_Bin_Borders[8][27][0] = 0.36; z_pT_Bin_Borders[8][27][1] = 0.33; z_pT_Bin_Borders[8][27][2] = 0.29; z_pT_Bin_Borders[8][27][3] = 0.2;
Phi_h_Bin_Values[8][27][0] =  24; Phi_h_Bin_Values[8][27][1] = 624; Phi_h_Bin_Values[8][27][2] = 5977;
z_pT_Bin_Borders[8][28][0] = 0.36; z_pT_Bin_Borders[8][28][1] = 0.33; z_pT_Bin_Borders[8][28][2] = 0.37; z_pT_Bin_Borders[8][28][3] = 0.29;
Phi_h_Bin_Values[8][28][0] =  24; Phi_h_Bin_Values[8][28][1] = 648; Phi_h_Bin_Values[8][28][2] = 6001;
z_pT_Bin_Borders[8][29][0] = 0.36; z_pT_Bin_Borders[8][29][1] = 0.33; z_pT_Bin_Borders[8][29][2] = 0.46; z_pT_Bin_Borders[8][29][3] = 0.37;
Phi_h_Bin_Values[8][29][0] =  24; Phi_h_Bin_Values[8][29][1] = 672; Phi_h_Bin_Values[8][29][2] = 6025;
z_pT_Bin_Borders[8][30][0] = 0.36; z_pT_Bin_Borders[8][30][1] = 0.33; z_pT_Bin_Borders[8][30][2] = 0.6; z_pT_Bin_Borders[8][30][3] = 0.46;
Phi_h_Bin_Values[8][30][0] =  24; Phi_h_Bin_Values[8][30][1] = 696; Phi_h_Bin_Values[8][30][2] = 6049;
z_pT_Bin_Borders[8][31][0] = 0.33; z_pT_Bin_Borders[8][31][1] = 0.27; z_pT_Bin_Borders[8][31][2] = 0.2; z_pT_Bin_Borders[8][31][3] = 0.05;
Phi_h_Bin_Values[8][31][0] =  24; Phi_h_Bin_Values[8][31][1] = 720; Phi_h_Bin_Values[8][31][2] = 6073;
z_pT_Bin_Borders[8][32][0] = 0.33; z_pT_Bin_Borders[8][32][1] = 0.27; z_pT_Bin_Borders[8][32][2] = 0.29; z_pT_Bin_Borders[8][32][3] = 0.2;
Phi_h_Bin_Values[8][32][0] =  24; Phi_h_Bin_Values[8][32][1] = 744; Phi_h_Bin_Values[8][32][2] = 6097;
z_pT_Bin_Borders[8][33][0] = 0.33; z_pT_Bin_Borders[8][33][1] = 0.27; z_pT_Bin_Borders[8][33][2] = 0.37; z_pT_Bin_Borders[8][33][3] = 0.29;
Phi_h_Bin_Values[8][33][0] =  24; Phi_h_Bin_Values[8][33][1] = 768; Phi_h_Bin_Values[8][33][2] = 6121;
z_pT_Bin_Borders[8][34][0] = 0.33; z_pT_Bin_Borders[8][34][1] = 0.27; z_pT_Bin_Borders[8][34][2] = 0.46; z_pT_Bin_Borders[8][34][3] = 0.37;
Phi_h_Bin_Values[8][34][0] =  24; Phi_h_Bin_Values[8][34][1] = 792; Phi_h_Bin_Values[8][34][2] = 6145;
z_pT_Bin_Borders[8][35][0] = 0.33; z_pT_Bin_Borders[8][35][1] = 0.27; z_pT_Bin_Borders[8][35][2] = 0.6; z_pT_Bin_Borders[8][35][3] = 0.46;
Phi_h_Bin_Values[8][35][0] =  24; Phi_h_Bin_Values[8][35][1] = 816; Phi_h_Bin_Values[8][35][2] = 6169;
z_pT_Bin_Borders[8][36][0] = 10; z_pT_Bin_Borders[8][36][1] = 0.7; z_pT_Bin_Borders[8][36][2] = 0.05; z_pT_Bin_Borders[8][36][3] = 0;
Phi_h_Bin_Values[8][36][0] =  1; Phi_h_Bin_Values[8][36][1] = 840; Phi_h_Bin_Values[8][36][2] = 6193;
z_pT_Bin_Borders[8][37][0] = 10; z_pT_Bin_Borders[8][37][1] = 0.7; z_pT_Bin_Borders[8][37][2] = 0.2; z_pT_Bin_Borders[8][37][3] = 0.05;
Phi_h_Bin_Values[8][37][0] =  1; Phi_h_Bin_Values[8][37][1] = 841; Phi_h_Bin_Values[8][37][2] = 6194;
z_pT_Bin_Borders[8][38][0] = 10; z_pT_Bin_Borders[8][38][1] = 0.7; z_pT_Bin_Borders[8][38][2] = 0.29; z_pT_Bin_Borders[8][38][3] = 0.2;
Phi_h_Bin_Values[8][38][0] =  1; Phi_h_Bin_Values[8][38][1] = 842; Phi_h_Bin_Values[8][38][2] = 6195;
z_pT_Bin_Borders[8][39][0] = 10; z_pT_Bin_Borders[8][39][1] = 0.7; z_pT_Bin_Borders[8][39][2] = 0.37; z_pT_Bin_Borders[8][39][3] = 0.29;
Phi_h_Bin_Values[8][39][0] =  1; Phi_h_Bin_Values[8][39][1] = 843; Phi_h_Bin_Values[8][39][2] = 6196;
z_pT_Bin_Borders[8][40][0] = 10; z_pT_Bin_Borders[8][40][1] = 0.7; z_pT_Bin_Borders[8][40][2] = 0.46; z_pT_Bin_Borders[8][40][3] = 0.37;
Phi_h_Bin_Values[8][40][0] =  1; Phi_h_Bin_Values[8][40][1] = 844; Phi_h_Bin_Values[8][40][2] = 6197;
z_pT_Bin_Borders[8][41][0] = 10; z_pT_Bin_Borders[8][41][1] = 0.7; z_pT_Bin_Borders[8][41][2] = 0.6; z_pT_Bin_Borders[8][41][3] = 0.46;
Phi_h_Bin_Values[8][41][0] =  1; Phi_h_Bin_Values[8][41][1] = 845; Phi_h_Bin_Values[8][41][2] = 6198;
z_pT_Bin_Borders[8][42][0] = 10; z_pT_Bin_Borders[8][42][1] = 0.7; z_pT_Bin_Borders[8][42][2] = 10; z_pT_Bin_Borders[8][42][3] = 0.6;
Phi_h_Bin_Values[8][42][0] =  1; Phi_h_Bin_Values[8][42][1] = 846; Phi_h_Bin_Values[8][42][2] = 6199;
z_pT_Bin_Borders[8][43][0] = 0.7; z_pT_Bin_Borders[8][43][1] = 0.56; z_pT_Bin_Borders[8][43][2] = 0.05; z_pT_Bin_Borders[8][43][3] = 0;
Phi_h_Bin_Values[8][43][0] =  1; Phi_h_Bin_Values[8][43][1] = 847; Phi_h_Bin_Values[8][43][2] = 6200;
z_pT_Bin_Borders[8][44][0] = 0.7; z_pT_Bin_Borders[8][44][1] = 0.56; z_pT_Bin_Borders[8][44][2] = 10; z_pT_Bin_Borders[8][44][3] = 0.6;
Phi_h_Bin_Values[8][44][0] =  1; Phi_h_Bin_Values[8][44][1] = 848; Phi_h_Bin_Values[8][44][2] = 6201;
z_pT_Bin_Borders[8][45][0] = 0.56; z_pT_Bin_Borders[8][45][1] = 0.49; z_pT_Bin_Borders[8][45][2] = 0.05; z_pT_Bin_Borders[8][45][3] = 0;
Phi_h_Bin_Values[8][45][0] =  1; Phi_h_Bin_Values[8][45][1] = 849; Phi_h_Bin_Values[8][45][2] = 6202;
z_pT_Bin_Borders[8][46][0] = 0.56; z_pT_Bin_Borders[8][46][1] = 0.49; z_pT_Bin_Borders[8][46][2] = 10; z_pT_Bin_Borders[8][46][3] = 0.6;
Phi_h_Bin_Values[8][46][0] =  1; Phi_h_Bin_Values[8][46][1] = 850; Phi_h_Bin_Values[8][46][2] = 6203;
z_pT_Bin_Borders[8][47][0] = 0.49; z_pT_Bin_Borders[8][47][1] = 0.44; z_pT_Bin_Borders[8][47][2] = 0.05; z_pT_Bin_Borders[8][47][3] = 0;
Phi_h_Bin_Values[8][47][0] =  1; Phi_h_Bin_Values[8][47][1] = 851; Phi_h_Bin_Values[8][47][2] = 6204;
z_pT_Bin_Borders[8][48][0] = 0.49; z_pT_Bin_Borders[8][48][1] = 0.44; z_pT_Bin_Borders[8][48][2] = 10; z_pT_Bin_Borders[8][48][3] = 0.6;
Phi_h_Bin_Values[8][48][0] =  1; Phi_h_Bin_Values[8][48][1] = 852; Phi_h_Bin_Values[8][48][2] = 6205;
z_pT_Bin_Borders[8][49][0] = 0.44; z_pT_Bin_Borders[8][49][1] = 0.39; z_pT_Bin_Borders[8][49][2] = 0.05; z_pT_Bin_Borders[8][49][3] = 0;
Phi_h_Bin_Values[8][49][0] =  1; Phi_h_Bin_Values[8][49][1] = 853; Phi_h_Bin_Values[8][49][2] = 6206;
z_pT_Bin_Borders[8][50][0] = 0.44; z_pT_Bin_Borders[8][50][1] = 0.39; z_pT_Bin_Borders[8][50][2] = 10; z_pT_Bin_Borders[8][50][3] = 0.6;
Phi_h_Bin_Values[8][50][0] =  1; Phi_h_Bin_Values[8][50][1] = 854; Phi_h_Bin_Values[8][50][2] = 6207;
z_pT_Bin_Borders[8][51][0] = 0.39; z_pT_Bin_Borders[8][51][1] = 0.36; z_pT_Bin_Borders[8][51][2] = 0.05; z_pT_Bin_Borders[8][51][3] = 0;
Phi_h_Bin_Values[8][51][0] =  1; Phi_h_Bin_Values[8][51][1] = 855; Phi_h_Bin_Values[8][51][2] = 6208;
z_pT_Bin_Borders[8][52][0] = 0.39; z_pT_Bin_Borders[8][52][1] = 0.36; z_pT_Bin_Borders[8][52][2] = 10; z_pT_Bin_Borders[8][52][3] = 0.6;
Phi_h_Bin_Values[8][52][0] =  1; Phi_h_Bin_Values[8][52][1] = 856; Phi_h_Bin_Values[8][52][2] = 6209;
z_pT_Bin_Borders[8][53][0] = 0.36; z_pT_Bin_Borders[8][53][1] = 0.33; z_pT_Bin_Borders[8][53][2] = 0.05; z_pT_Bin_Borders[8][53][3] = 0;
Phi_h_Bin_Values[8][53][0] =  1; Phi_h_Bin_Values[8][53][1] = 857; Phi_h_Bin_Values[8][53][2] = 6210;
z_pT_Bin_Borders[8][54][0] = 0.36; z_pT_Bin_Borders[8][54][1] = 0.33; z_pT_Bin_Borders[8][54][2] = 10; z_pT_Bin_Borders[8][54][3] = 0.6;
Phi_h_Bin_Values[8][54][0] =  1; Phi_h_Bin_Values[8][54][1] = 858; Phi_h_Bin_Values[8][54][2] = 6211;
z_pT_Bin_Borders[8][55][0] = 0.33; z_pT_Bin_Borders[8][55][1] = 0.27; z_pT_Bin_Borders[8][55][2] = 0.05; z_pT_Bin_Borders[8][55][3] = 0;
Phi_h_Bin_Values[8][55][0] =  1; Phi_h_Bin_Values[8][55][1] = 859; Phi_h_Bin_Values[8][55][2] = 6212;
z_pT_Bin_Borders[8][56][0] = 0.33; z_pT_Bin_Borders[8][56][1] = 0.27; z_pT_Bin_Borders[8][56][2] = 10; z_pT_Bin_Borders[8][56][3] = 0.6;
Phi_h_Bin_Values[8][56][0] =  1; Phi_h_Bin_Values[8][56][1] = 860; Phi_h_Bin_Values[8][56][2] = 6213;
z_pT_Bin_Borders[8][57][0] = 0.27; z_pT_Bin_Borders[8][57][1] = 0; z_pT_Bin_Borders[8][57][2] = 0.05; z_pT_Bin_Borders[8][57][3] = 0;
Phi_h_Bin_Values[8][57][0] =  1; Phi_h_Bin_Values[8][57][1] = 861; Phi_h_Bin_Values[8][57][2] = 6214;
z_pT_Bin_Borders[8][58][0] = 0.27; z_pT_Bin_Borders[8][58][1] = 0; z_pT_Bin_Borders[8][58][2] = 0.2; z_pT_Bin_Borders[8][58][3] = 0.05;
Phi_h_Bin_Values[8][58][0] =  1; Phi_h_Bin_Values[8][58][1] = 862; Phi_h_Bin_Values[8][58][2] = 6215;
z_pT_Bin_Borders[8][59][0] = 0.27; z_pT_Bin_Borders[8][59][1] = 0; z_pT_Bin_Borders[8][59][2] = 0.29; z_pT_Bin_Borders[8][59][3] = 0.2;
Phi_h_Bin_Values[8][59][0] =  1; Phi_h_Bin_Values[8][59][1] = 863; Phi_h_Bin_Values[8][59][2] = 6216;
z_pT_Bin_Borders[8][60][0] = 0.27; z_pT_Bin_Borders[8][60][1] = 0; z_pT_Bin_Borders[8][60][2] = 0.37; z_pT_Bin_Borders[8][60][3] = 0.29;
Phi_h_Bin_Values[8][60][0] =  1; Phi_h_Bin_Values[8][60][1] = 864; Phi_h_Bin_Values[8][60][2] = 6217;
z_pT_Bin_Borders[8][61][0] = 0.27; z_pT_Bin_Borders[8][61][1] = 0; z_pT_Bin_Borders[8][61][2] = 0.46; z_pT_Bin_Borders[8][61][3] = 0.37;
Phi_h_Bin_Values[8][61][0] =  1; Phi_h_Bin_Values[8][61][1] = 865; Phi_h_Bin_Values[8][61][2] = 6218;
z_pT_Bin_Borders[8][62][0] = 0.27; z_pT_Bin_Borders[8][62][1] = 0; z_pT_Bin_Borders[8][62][2] = 0.6; z_pT_Bin_Borders[8][62][3] = 0.46;
Phi_h_Bin_Values[8][62][0] =  1; Phi_h_Bin_Values[8][62][1] = 866; Phi_h_Bin_Values[8][62][2] = 6219;
z_pT_Bin_Borders[8][63][0] = 0.27; z_pT_Bin_Borders[8][63][1] = 0; z_pT_Bin_Borders[8][63][2] = 10; z_pT_Bin_Borders[8][63][3] = 0.6;
Phi_h_Bin_Values[8][63][0] =  1; Phi_h_Bin_Values[8][63][1] = 867; Phi_h_Bin_Values[8][63][2] = 6220;
z_pT_Bin_Borders[9][1][0] = 0.7; z_pT_Bin_Borders[9][1][1] = 0.42; z_pT_Bin_Borders[9][1][2] = 0.22; z_pT_Bin_Borders[9][1][3] = 0.05;
Phi_h_Bin_Values[9][1][0] =  24; Phi_h_Bin_Values[9][1][1] = 0; Phi_h_Bin_Values[9][1][2] = 6221;
z_pT_Bin_Borders[9][2][0] = 0.7; z_pT_Bin_Borders[9][2][1] = 0.42; z_pT_Bin_Borders[9][2][2] = 0.3; z_pT_Bin_Borders[9][2][3] = 0.22;
Phi_h_Bin_Values[9][2][0] =  24; Phi_h_Bin_Values[9][2][1] = 24; Phi_h_Bin_Values[9][2][2] = 6245;
z_pT_Bin_Borders[9][3][0] = 0.7; z_pT_Bin_Borders[9][3][1] = 0.42; z_pT_Bin_Borders[9][3][2] = 0.38; z_pT_Bin_Borders[9][3][3] = 0.3;
Phi_h_Bin_Values[9][3][0] =  24; Phi_h_Bin_Values[9][3][1] = 48; Phi_h_Bin_Values[9][3][2] = 6269;
z_pT_Bin_Borders[9][4][0] = 0.7; z_pT_Bin_Borders[9][4][1] = 0.42; z_pT_Bin_Borders[9][4][2] = 0.46; z_pT_Bin_Borders[9][4][3] = 0.38;
Phi_h_Bin_Values[9][4][0] =  24; Phi_h_Bin_Values[9][4][1] = 72; Phi_h_Bin_Values[9][4][2] = 6293;
z_pT_Bin_Borders[9][5][0] = 0.7; z_pT_Bin_Borders[9][5][1] = 0.42; z_pT_Bin_Borders[9][5][2] = 0.58; z_pT_Bin_Borders[9][5][3] = 0.46;
Phi_h_Bin_Values[9][5][0] =  24; Phi_h_Bin_Values[9][5][1] = 96; Phi_h_Bin_Values[9][5][2] = 6317;
z_pT_Bin_Borders[9][6][0] = 0.7; z_pT_Bin_Borders[9][6][1] = 0.42; z_pT_Bin_Borders[9][6][2] = 0.74; z_pT_Bin_Borders[9][6][3] = 0.58;
Phi_h_Bin_Values[9][6][0] =  24; Phi_h_Bin_Values[9][6][1] = 120; Phi_h_Bin_Values[9][6][2] = 6341;
z_pT_Bin_Borders[9][7][0] = 0.7; z_pT_Bin_Borders[9][7][1] = 0.42; z_pT_Bin_Borders[9][7][2] = 0.95; z_pT_Bin_Borders[9][7][3] = 0.74;
Phi_h_Bin_Values[9][7][0] =  24; Phi_h_Bin_Values[9][7][1] = 144; Phi_h_Bin_Values[9][7][2] = 6365;
z_pT_Bin_Borders[9][8][0] = 0.42; z_pT_Bin_Borders[9][8][1] = 0.3; z_pT_Bin_Borders[9][8][2] = 0.22; z_pT_Bin_Borders[9][8][3] = 0.05;
Phi_h_Bin_Values[9][8][0] =  24; Phi_h_Bin_Values[9][8][1] = 168; Phi_h_Bin_Values[9][8][2] = 6389;
z_pT_Bin_Borders[9][9][0] = 0.42; z_pT_Bin_Borders[9][9][1] = 0.3; z_pT_Bin_Borders[9][9][2] = 0.3; z_pT_Bin_Borders[9][9][3] = 0.22;
Phi_h_Bin_Values[9][9][0] =  24; Phi_h_Bin_Values[9][9][1] = 192; Phi_h_Bin_Values[9][9][2] = 6413;
z_pT_Bin_Borders[9][10][0] = 0.42; z_pT_Bin_Borders[9][10][1] = 0.3; z_pT_Bin_Borders[9][10][2] = 0.38; z_pT_Bin_Borders[9][10][3] = 0.3;
Phi_h_Bin_Values[9][10][0] =  24; Phi_h_Bin_Values[9][10][1] = 216; Phi_h_Bin_Values[9][10][2] = 6437;
z_pT_Bin_Borders[9][11][0] = 0.42; z_pT_Bin_Borders[9][11][1] = 0.3; z_pT_Bin_Borders[9][11][2] = 0.46; z_pT_Bin_Borders[9][11][3] = 0.38;
Phi_h_Bin_Values[9][11][0] =  24; Phi_h_Bin_Values[9][11][1] = 240; Phi_h_Bin_Values[9][11][2] = 6461;
z_pT_Bin_Borders[9][12][0] = 0.42; z_pT_Bin_Borders[9][12][1] = 0.3; z_pT_Bin_Borders[9][12][2] = 0.58; z_pT_Bin_Borders[9][12][3] = 0.46;
Phi_h_Bin_Values[9][12][0] =  24; Phi_h_Bin_Values[9][12][1] = 264; Phi_h_Bin_Values[9][12][2] = 6485;
z_pT_Bin_Borders[9][13][0] = 0.42; z_pT_Bin_Borders[9][13][1] = 0.3; z_pT_Bin_Borders[9][13][2] = 0.74; z_pT_Bin_Borders[9][13][3] = 0.58;
Phi_h_Bin_Values[9][13][0] =  24; Phi_h_Bin_Values[9][13][1] = 288; Phi_h_Bin_Values[9][13][2] = 6509;
z_pT_Bin_Borders[9][14][0] = 0.42; z_pT_Bin_Borders[9][14][1] = 0.3; z_pT_Bin_Borders[9][14][2] = 0.95; z_pT_Bin_Borders[9][14][3] = 0.74;
Phi_h_Bin_Values[9][14][0] =  24; Phi_h_Bin_Values[9][14][1] = 312; Phi_h_Bin_Values[9][14][2] = 6533;
z_pT_Bin_Borders[9][15][0] = 0.3; z_pT_Bin_Borders[9][15][1] = 0.24; z_pT_Bin_Borders[9][15][2] = 0.22; z_pT_Bin_Borders[9][15][3] = 0.05;
Phi_h_Bin_Values[9][15][0] =  24; Phi_h_Bin_Values[9][15][1] = 336; Phi_h_Bin_Values[9][15][2] = 6557;
z_pT_Bin_Borders[9][16][0] = 0.3; z_pT_Bin_Borders[9][16][1] = 0.24; z_pT_Bin_Borders[9][16][2] = 0.3; z_pT_Bin_Borders[9][16][3] = 0.22;
Phi_h_Bin_Values[9][16][0] =  24; Phi_h_Bin_Values[9][16][1] = 360; Phi_h_Bin_Values[9][16][2] = 6581;
z_pT_Bin_Borders[9][17][0] = 0.3; z_pT_Bin_Borders[9][17][1] = 0.24; z_pT_Bin_Borders[9][17][2] = 0.38; z_pT_Bin_Borders[9][17][3] = 0.3;
Phi_h_Bin_Values[9][17][0] =  24; Phi_h_Bin_Values[9][17][1] = 384; Phi_h_Bin_Values[9][17][2] = 6605;
z_pT_Bin_Borders[9][18][0] = 0.3; z_pT_Bin_Borders[9][18][1] = 0.24; z_pT_Bin_Borders[9][18][2] = 0.46; z_pT_Bin_Borders[9][18][3] = 0.38;
Phi_h_Bin_Values[9][18][0] =  24; Phi_h_Bin_Values[9][18][1] = 408; Phi_h_Bin_Values[9][18][2] = 6629;
z_pT_Bin_Borders[9][19][0] = 0.3; z_pT_Bin_Borders[9][19][1] = 0.24; z_pT_Bin_Borders[9][19][2] = 0.58; z_pT_Bin_Borders[9][19][3] = 0.46;
Phi_h_Bin_Values[9][19][0] =  24; Phi_h_Bin_Values[9][19][1] = 432; Phi_h_Bin_Values[9][19][2] = 6653;
z_pT_Bin_Borders[9][20][0] = 0.3; z_pT_Bin_Borders[9][20][1] = 0.24; z_pT_Bin_Borders[9][20][2] = 0.74; z_pT_Bin_Borders[9][20][3] = 0.58;
Phi_h_Bin_Values[9][20][0] =  24; Phi_h_Bin_Values[9][20][1] = 456; Phi_h_Bin_Values[9][20][2] = 6677;
z_pT_Bin_Borders[9][21][0] = 0.3; z_pT_Bin_Borders[9][21][1] = 0.24; z_pT_Bin_Borders[9][21][2] = 0.95; z_pT_Bin_Borders[9][21][3] = 0.74;
Phi_h_Bin_Values[9][21][0] =  1; Phi_h_Bin_Values[9][21][1] = 480; Phi_h_Bin_Values[9][21][2] = 6701;
z_pT_Bin_Borders[9][22][0] = 0.24; z_pT_Bin_Borders[9][22][1] = 0.2; z_pT_Bin_Borders[9][22][2] = 0.22; z_pT_Bin_Borders[9][22][3] = 0.05;
Phi_h_Bin_Values[9][22][0] =  24; Phi_h_Bin_Values[9][22][1] = 481; Phi_h_Bin_Values[9][22][2] = 6702;
z_pT_Bin_Borders[9][23][0] = 0.24; z_pT_Bin_Borders[9][23][1] = 0.2; z_pT_Bin_Borders[9][23][2] = 0.3; z_pT_Bin_Borders[9][23][3] = 0.22;
Phi_h_Bin_Values[9][23][0] =  24; Phi_h_Bin_Values[9][23][1] = 505; Phi_h_Bin_Values[9][23][2] = 6726;
z_pT_Bin_Borders[9][24][0] = 0.24; z_pT_Bin_Borders[9][24][1] = 0.2; z_pT_Bin_Borders[9][24][2] = 0.38; z_pT_Bin_Borders[9][24][3] = 0.3;
Phi_h_Bin_Values[9][24][0] =  24; Phi_h_Bin_Values[9][24][1] = 529; Phi_h_Bin_Values[9][24][2] = 6750;
z_pT_Bin_Borders[9][25][0] = 0.24; z_pT_Bin_Borders[9][25][1] = 0.2; z_pT_Bin_Borders[9][25][2] = 0.46; z_pT_Bin_Borders[9][25][3] = 0.38;
Phi_h_Bin_Values[9][25][0] =  24; Phi_h_Bin_Values[9][25][1] = 553; Phi_h_Bin_Values[9][25][2] = 6774;
z_pT_Bin_Borders[9][26][0] = 0.24; z_pT_Bin_Borders[9][26][1] = 0.2; z_pT_Bin_Borders[9][26][2] = 0.58; z_pT_Bin_Borders[9][26][3] = 0.46;
Phi_h_Bin_Values[9][26][0] =  24; Phi_h_Bin_Values[9][26][1] = 577; Phi_h_Bin_Values[9][26][2] = 6798;
z_pT_Bin_Borders[9][27][0] = 0.24; z_pT_Bin_Borders[9][27][1] = 0.2; z_pT_Bin_Borders[9][27][2] = 0.74; z_pT_Bin_Borders[9][27][3] = 0.58;
Phi_h_Bin_Values[9][27][0] =  1; Phi_h_Bin_Values[9][27][1] = 601; Phi_h_Bin_Values[9][27][2] = 6822;
z_pT_Bin_Borders[9][28][0] = 0.24; z_pT_Bin_Borders[9][28][1] = 0.2; z_pT_Bin_Borders[9][28][2] = 0.95; z_pT_Bin_Borders[9][28][3] = 0.74;
Phi_h_Bin_Values[9][28][0] =  1; Phi_h_Bin_Values[9][28][1] = 602; Phi_h_Bin_Values[9][28][2] = 6823;
z_pT_Bin_Borders[9][29][0] = 0.2; z_pT_Bin_Borders[9][29][1] = 0.16; z_pT_Bin_Borders[9][29][2] = 0.22; z_pT_Bin_Borders[9][29][3] = 0.05;
Phi_h_Bin_Values[9][29][0] =  24; Phi_h_Bin_Values[9][29][1] = 603; Phi_h_Bin_Values[9][29][2] = 6824;
z_pT_Bin_Borders[9][30][0] = 0.2; z_pT_Bin_Borders[9][30][1] = 0.16; z_pT_Bin_Borders[9][30][2] = 0.3; z_pT_Bin_Borders[9][30][3] = 0.22;
Phi_h_Bin_Values[9][30][0] =  24; Phi_h_Bin_Values[9][30][1] = 627; Phi_h_Bin_Values[9][30][2] = 6848;
z_pT_Bin_Borders[9][31][0] = 0.2; z_pT_Bin_Borders[9][31][1] = 0.16; z_pT_Bin_Borders[9][31][2] = 0.38; z_pT_Bin_Borders[9][31][3] = 0.3;
Phi_h_Bin_Values[9][31][0] =  24; Phi_h_Bin_Values[9][31][1] = 651; Phi_h_Bin_Values[9][31][2] = 6872;
z_pT_Bin_Borders[9][32][0] = 0.2; z_pT_Bin_Borders[9][32][1] = 0.16; z_pT_Bin_Borders[9][32][2] = 0.46; z_pT_Bin_Borders[9][32][3] = 0.38;
Phi_h_Bin_Values[9][32][0] =  24; Phi_h_Bin_Values[9][32][1] = 675; Phi_h_Bin_Values[9][32][2] = 6896;
z_pT_Bin_Borders[9][33][0] = 0.2; z_pT_Bin_Borders[9][33][1] = 0.16; z_pT_Bin_Borders[9][33][2] = 0.58; z_pT_Bin_Borders[9][33][3] = 0.46;
Phi_h_Bin_Values[9][33][0] =  1; Phi_h_Bin_Values[9][33][1] = 699; Phi_h_Bin_Values[9][33][2] = 6920;
z_pT_Bin_Borders[9][34][0] = 0.2; z_pT_Bin_Borders[9][34][1] = 0.16; z_pT_Bin_Borders[9][34][2] = 0.74; z_pT_Bin_Borders[9][34][3] = 0.58;
Phi_h_Bin_Values[9][34][0] =  1; Phi_h_Bin_Values[9][34][1] = 700; Phi_h_Bin_Values[9][34][2] = 6921;
z_pT_Bin_Borders[9][35][0] = 0.2; z_pT_Bin_Borders[9][35][1] = 0.16; z_pT_Bin_Borders[9][35][2] = 0.95; z_pT_Bin_Borders[9][35][3] = 0.74;
Phi_h_Bin_Values[9][35][0] =  1; Phi_h_Bin_Values[9][35][1] = 701; Phi_h_Bin_Values[9][35][2] = 6922;
z_pT_Bin_Borders[9][36][0] = 10; z_pT_Bin_Borders[9][36][1] = 0.7; z_pT_Bin_Borders[9][36][2] = 0.05; z_pT_Bin_Borders[9][36][3] = 0;
Phi_h_Bin_Values[9][36][0] =  1; Phi_h_Bin_Values[9][36][1] = 702; Phi_h_Bin_Values[9][36][2] = 6923;
z_pT_Bin_Borders[9][37][0] = 10; z_pT_Bin_Borders[9][37][1] = 0.7; z_pT_Bin_Borders[9][37][2] = 0.22; z_pT_Bin_Borders[9][37][3] = 0.05;
Phi_h_Bin_Values[9][37][0] =  1; Phi_h_Bin_Values[9][37][1] = 703; Phi_h_Bin_Values[9][37][2] = 6924;
z_pT_Bin_Borders[9][38][0] = 10; z_pT_Bin_Borders[9][38][1] = 0.7; z_pT_Bin_Borders[9][38][2] = 0.3; z_pT_Bin_Borders[9][38][3] = 0.22;
Phi_h_Bin_Values[9][38][0] =  1; Phi_h_Bin_Values[9][38][1] = 704; Phi_h_Bin_Values[9][38][2] = 6925;
z_pT_Bin_Borders[9][39][0] = 10; z_pT_Bin_Borders[9][39][1] = 0.7; z_pT_Bin_Borders[9][39][2] = 0.38; z_pT_Bin_Borders[9][39][3] = 0.3;
Phi_h_Bin_Values[9][39][0] =  1; Phi_h_Bin_Values[9][39][1] = 705; Phi_h_Bin_Values[9][39][2] = 6926;
z_pT_Bin_Borders[9][40][0] = 10; z_pT_Bin_Borders[9][40][1] = 0.7; z_pT_Bin_Borders[9][40][2] = 0.46; z_pT_Bin_Borders[9][40][3] = 0.38;
Phi_h_Bin_Values[9][40][0] =  1; Phi_h_Bin_Values[9][40][1] = 706; Phi_h_Bin_Values[9][40][2] = 6927;
z_pT_Bin_Borders[9][41][0] = 10; z_pT_Bin_Borders[9][41][1] = 0.7; z_pT_Bin_Borders[9][41][2] = 0.58; z_pT_Bin_Borders[9][41][3] = 0.46;
Phi_h_Bin_Values[9][41][0] =  1; Phi_h_Bin_Values[9][41][1] = 707; Phi_h_Bin_Values[9][41][2] = 6928;
z_pT_Bin_Borders[9][42][0] = 10; z_pT_Bin_Borders[9][42][1] = 0.7; z_pT_Bin_Borders[9][42][2] = 0.74; z_pT_Bin_Borders[9][42][3] = 0.58;
Phi_h_Bin_Values[9][42][0] =  1; Phi_h_Bin_Values[9][42][1] = 708; Phi_h_Bin_Values[9][42][2] = 6929;
z_pT_Bin_Borders[9][43][0] = 10; z_pT_Bin_Borders[9][43][1] = 0.7; z_pT_Bin_Borders[9][43][2] = 0.95; z_pT_Bin_Borders[9][43][3] = 0.74;
Phi_h_Bin_Values[9][43][0] =  1; Phi_h_Bin_Values[9][43][1] = 709; Phi_h_Bin_Values[9][43][2] = 6930;
z_pT_Bin_Borders[9][44][0] = 10; z_pT_Bin_Borders[9][44][1] = 0.7; z_pT_Bin_Borders[9][44][2] = 10; z_pT_Bin_Borders[9][44][3] = 0.95;
Phi_h_Bin_Values[9][44][0] =  1; Phi_h_Bin_Values[9][44][1] = 710; Phi_h_Bin_Values[9][44][2] = 6931;
z_pT_Bin_Borders[9][45][0] = 0.7; z_pT_Bin_Borders[9][45][1] = 0.42; z_pT_Bin_Borders[9][45][2] = 0.05; z_pT_Bin_Borders[9][45][3] = 0;
Phi_h_Bin_Values[9][45][0] =  1; Phi_h_Bin_Values[9][45][1] = 711; Phi_h_Bin_Values[9][45][2] = 6932;
z_pT_Bin_Borders[9][46][0] = 0.7; z_pT_Bin_Borders[9][46][1] = 0.42; z_pT_Bin_Borders[9][46][2] = 10; z_pT_Bin_Borders[9][46][3] = 0.95;
Phi_h_Bin_Values[9][46][0] =  1; Phi_h_Bin_Values[9][46][1] = 712; Phi_h_Bin_Values[9][46][2] = 6933;
z_pT_Bin_Borders[9][47][0] = 0.42; z_pT_Bin_Borders[9][47][1] = 0.3; z_pT_Bin_Borders[9][47][2] = 0.05; z_pT_Bin_Borders[9][47][3] = 0;
Phi_h_Bin_Values[9][47][0] =  1; Phi_h_Bin_Values[9][47][1] = 713; Phi_h_Bin_Values[9][47][2] = 6934;
z_pT_Bin_Borders[9][48][0] = 0.42; z_pT_Bin_Borders[9][48][1] = 0.3; z_pT_Bin_Borders[9][48][2] = 10; z_pT_Bin_Borders[9][48][3] = 0.95;
Phi_h_Bin_Values[9][48][0] =  1; Phi_h_Bin_Values[9][48][1] = 714; Phi_h_Bin_Values[9][48][2] = 6935;
z_pT_Bin_Borders[9][49][0] = 0.3; z_pT_Bin_Borders[9][49][1] = 0.24; z_pT_Bin_Borders[9][49][2] = 0.05; z_pT_Bin_Borders[9][49][3] = 0;
Phi_h_Bin_Values[9][49][0] =  1; Phi_h_Bin_Values[9][49][1] = 715; Phi_h_Bin_Values[9][49][2] = 6936;
z_pT_Bin_Borders[9][50][0] = 0.3; z_pT_Bin_Borders[9][50][1] = 0.24; z_pT_Bin_Borders[9][50][2] = 10; z_pT_Bin_Borders[9][50][3] = 0.95;
Phi_h_Bin_Values[9][50][0] =  1; Phi_h_Bin_Values[9][50][1] = 716; Phi_h_Bin_Values[9][50][2] = 6937;
z_pT_Bin_Borders[9][51][0] = 0.24; z_pT_Bin_Borders[9][51][1] = 0.2; z_pT_Bin_Borders[9][51][2] = 0.05; z_pT_Bin_Borders[9][51][3] = 0;
Phi_h_Bin_Values[9][51][0] =  1; Phi_h_Bin_Values[9][51][1] = 717; Phi_h_Bin_Values[9][51][2] = 6938;
z_pT_Bin_Borders[9][52][0] = 0.24; z_pT_Bin_Borders[9][52][1] = 0.2; z_pT_Bin_Borders[9][52][2] = 10; z_pT_Bin_Borders[9][52][3] = 0.95;
Phi_h_Bin_Values[9][52][0] =  1; Phi_h_Bin_Values[9][52][1] = 718; Phi_h_Bin_Values[9][52][2] = 6939;
z_pT_Bin_Borders[9][53][0] = 0.2; z_pT_Bin_Borders[9][53][1] = 0.16; z_pT_Bin_Borders[9][53][2] = 0.05; z_pT_Bin_Borders[9][53][3] = 0;
Phi_h_Bin_Values[9][53][0] =  1; Phi_h_Bin_Values[9][53][1] = 719; Phi_h_Bin_Values[9][53][2] = 6940;
z_pT_Bin_Borders[9][54][0] = 0.2; z_pT_Bin_Borders[9][54][1] = 0.16; z_pT_Bin_Borders[9][54][2] = 10; z_pT_Bin_Borders[9][54][3] = 0.95;
Phi_h_Bin_Values[9][54][0] =  1; Phi_h_Bin_Values[9][54][1] = 720; Phi_h_Bin_Values[9][54][2] = 6941;
z_pT_Bin_Borders[9][55][0] = 0.16; z_pT_Bin_Borders[9][55][1] = 0; z_pT_Bin_Borders[9][55][2] = 0.05; z_pT_Bin_Borders[9][55][3] = 0;
Phi_h_Bin_Values[9][55][0] =  1; Phi_h_Bin_Values[9][55][1] = 721; Phi_h_Bin_Values[9][55][2] = 6942;
z_pT_Bin_Borders[9][56][0] = 0.16; z_pT_Bin_Borders[9][56][1] = 0; z_pT_Bin_Borders[9][56][2] = 0.22; z_pT_Bin_Borders[9][56][3] = 0.05;
Phi_h_Bin_Values[9][56][0] =  1; Phi_h_Bin_Values[9][56][1] = 722; Phi_h_Bin_Values[9][56][2] = 6943;
z_pT_Bin_Borders[9][57][0] = 0.16; z_pT_Bin_Borders[9][57][1] = 0; z_pT_Bin_Borders[9][57][2] = 0.3; z_pT_Bin_Borders[9][57][3] = 0.22;
Phi_h_Bin_Values[9][57][0] =  1; Phi_h_Bin_Values[9][57][1] = 723; Phi_h_Bin_Values[9][57][2] = 6944;
z_pT_Bin_Borders[9][58][0] = 0.16; z_pT_Bin_Borders[9][58][1] = 0; z_pT_Bin_Borders[9][58][2] = 0.38; z_pT_Bin_Borders[9][58][3] = 0.3;
Phi_h_Bin_Values[9][58][0] =  1; Phi_h_Bin_Values[9][58][1] = 724; Phi_h_Bin_Values[9][58][2] = 6945;
z_pT_Bin_Borders[9][59][0] = 0.16; z_pT_Bin_Borders[9][59][1] = 0; z_pT_Bin_Borders[9][59][2] = 0.46; z_pT_Bin_Borders[9][59][3] = 0.38;
Phi_h_Bin_Values[9][59][0] =  1; Phi_h_Bin_Values[9][59][1] = 725; Phi_h_Bin_Values[9][59][2] = 6946;
z_pT_Bin_Borders[9][60][0] = 0.16; z_pT_Bin_Borders[9][60][1] = 0; z_pT_Bin_Borders[9][60][2] = 0.58; z_pT_Bin_Borders[9][60][3] = 0.46;
Phi_h_Bin_Values[9][60][0] =  1; Phi_h_Bin_Values[9][60][1] = 726; Phi_h_Bin_Values[9][60][2] = 6947;
z_pT_Bin_Borders[9][61][0] = 0.16; z_pT_Bin_Borders[9][61][1] = 0; z_pT_Bin_Borders[9][61][2] = 0.74; z_pT_Bin_Borders[9][61][3] = 0.58;
Phi_h_Bin_Values[9][61][0] =  1; Phi_h_Bin_Values[9][61][1] = 727; Phi_h_Bin_Values[9][61][2] = 6948;
z_pT_Bin_Borders[9][62][0] = 0.16; z_pT_Bin_Borders[9][62][1] = 0; z_pT_Bin_Borders[9][62][2] = 0.95; z_pT_Bin_Borders[9][62][3] = 0.74;
Phi_h_Bin_Values[9][62][0] =  1; Phi_h_Bin_Values[9][62][1] = 728; Phi_h_Bin_Values[9][62][2] = 6949;
z_pT_Bin_Borders[9][63][0] = 0.16; z_pT_Bin_Borders[9][63][1] = 0; z_pT_Bin_Borders[9][63][2] = 10; z_pT_Bin_Borders[9][63][3] = 0.95;
Phi_h_Bin_Values[9][63][0] =  1; Phi_h_Bin_Values[9][63][1] = 729; Phi_h_Bin_Values[9][63][2] = 6950;
z_pT_Bin_Borders[10][1][0] = 0.72; z_pT_Bin_Borders[10][1][1] = 0.5; z_pT_Bin_Borders[10][1][2] = 0.21; z_pT_Bin_Borders[10][1][3] = 0.05;
Phi_h_Bin_Values[10][1][0] =  24; Phi_h_Bin_Values[10][1][1] = 0; Phi_h_Bin_Values[10][1][2] = 6951;
z_pT_Bin_Borders[10][2][0] = 0.72; z_pT_Bin_Borders[10][2][1] = 0.5; z_pT_Bin_Borders[10][2][2] = 0.31; z_pT_Bin_Borders[10][2][3] = 0.21;
Phi_h_Bin_Values[10][2][0] =  24; Phi_h_Bin_Values[10][2][1] = 24; Phi_h_Bin_Values[10][2][2] = 6975;
z_pT_Bin_Borders[10][3][0] = 0.72; z_pT_Bin_Borders[10][3][1] = 0.5; z_pT_Bin_Borders[10][3][2] = 0.4; z_pT_Bin_Borders[10][3][3] = 0.31;
Phi_h_Bin_Values[10][3][0] =  24; Phi_h_Bin_Values[10][3][1] = 48; Phi_h_Bin_Values[10][3][2] = 6999;
z_pT_Bin_Borders[10][4][0] = 0.72; z_pT_Bin_Borders[10][4][1] = 0.5; z_pT_Bin_Borders[10][4][2] = 0.5; z_pT_Bin_Borders[10][4][3] = 0.4;
Phi_h_Bin_Values[10][4][0] =  24; Phi_h_Bin_Values[10][4][1] = 72; Phi_h_Bin_Values[10][4][2] = 7023;
z_pT_Bin_Borders[10][5][0] = 0.72; z_pT_Bin_Borders[10][5][1] = 0.5; z_pT_Bin_Borders[10][5][2] = 0.64; z_pT_Bin_Borders[10][5][3] = 0.5;
Phi_h_Bin_Values[10][5][0] =  24; Phi_h_Bin_Values[10][5][1] = 96; Phi_h_Bin_Values[10][5][2] = 7047;
z_pT_Bin_Borders[10][6][0] = 0.72; z_pT_Bin_Borders[10][6][1] = 0.5; z_pT_Bin_Borders[10][6][2] = 0.9; z_pT_Bin_Borders[10][6][3] = 0.64;
Phi_h_Bin_Values[10][6][0] =  24; Phi_h_Bin_Values[10][6][1] = 120; Phi_h_Bin_Values[10][6][2] = 7071;
z_pT_Bin_Borders[10][7][0] = 0.5; z_pT_Bin_Borders[10][7][1] = 0.4; z_pT_Bin_Borders[10][7][2] = 0.21; z_pT_Bin_Borders[10][7][3] = 0.05;
Phi_h_Bin_Values[10][7][0] =  24; Phi_h_Bin_Values[10][7][1] = 144; Phi_h_Bin_Values[10][7][2] = 7095;
z_pT_Bin_Borders[10][8][0] = 0.5; z_pT_Bin_Borders[10][8][1] = 0.4; z_pT_Bin_Borders[10][8][2] = 0.31; z_pT_Bin_Borders[10][8][3] = 0.21;
Phi_h_Bin_Values[10][8][0] =  24; Phi_h_Bin_Values[10][8][1] = 168; Phi_h_Bin_Values[10][8][2] = 7119;
z_pT_Bin_Borders[10][9][0] = 0.5; z_pT_Bin_Borders[10][9][1] = 0.4; z_pT_Bin_Borders[10][9][2] = 0.4; z_pT_Bin_Borders[10][9][3] = 0.31;
Phi_h_Bin_Values[10][9][0] =  24; Phi_h_Bin_Values[10][9][1] = 192; Phi_h_Bin_Values[10][9][2] = 7143;
z_pT_Bin_Borders[10][10][0] = 0.5; z_pT_Bin_Borders[10][10][1] = 0.4; z_pT_Bin_Borders[10][10][2] = 0.5; z_pT_Bin_Borders[10][10][3] = 0.4;
Phi_h_Bin_Values[10][10][0] =  24; Phi_h_Bin_Values[10][10][1] = 216; Phi_h_Bin_Values[10][10][2] = 7167;
z_pT_Bin_Borders[10][11][0] = 0.5; z_pT_Bin_Borders[10][11][1] = 0.4; z_pT_Bin_Borders[10][11][2] = 0.64; z_pT_Bin_Borders[10][11][3] = 0.5;
Phi_h_Bin_Values[10][11][0] =  24; Phi_h_Bin_Values[10][11][1] = 240; Phi_h_Bin_Values[10][11][2] = 7191;
z_pT_Bin_Borders[10][12][0] = 0.5; z_pT_Bin_Borders[10][12][1] = 0.4; z_pT_Bin_Borders[10][12][2] = 0.9; z_pT_Bin_Borders[10][12][3] = 0.64;
Phi_h_Bin_Values[10][12][0] =  24; Phi_h_Bin_Values[10][12][1] = 264; Phi_h_Bin_Values[10][12][2] = 7215;
z_pT_Bin_Borders[10][13][0] = 0.4; z_pT_Bin_Borders[10][13][1] = 0.32; z_pT_Bin_Borders[10][13][2] = 0.21; z_pT_Bin_Borders[10][13][3] = 0.05;
Phi_h_Bin_Values[10][13][0] =  24; Phi_h_Bin_Values[10][13][1] = 288; Phi_h_Bin_Values[10][13][2] = 7239;
z_pT_Bin_Borders[10][14][0] = 0.4; z_pT_Bin_Borders[10][14][1] = 0.32; z_pT_Bin_Borders[10][14][2] = 0.31; z_pT_Bin_Borders[10][14][3] = 0.21;
Phi_h_Bin_Values[10][14][0] =  24; Phi_h_Bin_Values[10][14][1] = 312; Phi_h_Bin_Values[10][14][2] = 7263;
z_pT_Bin_Borders[10][15][0] = 0.4; z_pT_Bin_Borders[10][15][1] = 0.32; z_pT_Bin_Borders[10][15][2] = 0.4; z_pT_Bin_Borders[10][15][3] = 0.31;
Phi_h_Bin_Values[10][15][0] =  24; Phi_h_Bin_Values[10][15][1] = 336; Phi_h_Bin_Values[10][15][2] = 7287;
z_pT_Bin_Borders[10][16][0] = 0.4; z_pT_Bin_Borders[10][16][1] = 0.32; z_pT_Bin_Borders[10][16][2] = 0.5; z_pT_Bin_Borders[10][16][3] = 0.4;
Phi_h_Bin_Values[10][16][0] =  24; Phi_h_Bin_Values[10][16][1] = 360; Phi_h_Bin_Values[10][16][2] = 7311;
z_pT_Bin_Borders[10][17][0] = 0.4; z_pT_Bin_Borders[10][17][1] = 0.32; z_pT_Bin_Borders[10][17][2] = 0.64; z_pT_Bin_Borders[10][17][3] = 0.5;
Phi_h_Bin_Values[10][17][0] =  24; Phi_h_Bin_Values[10][17][1] = 384; Phi_h_Bin_Values[10][17][2] = 7335;
z_pT_Bin_Borders[10][18][0] = 0.4; z_pT_Bin_Borders[10][18][1] = 0.32; z_pT_Bin_Borders[10][18][2] = 0.9; z_pT_Bin_Borders[10][18][3] = 0.64;
Phi_h_Bin_Values[10][18][0] =  24; Phi_h_Bin_Values[10][18][1] = 408; Phi_h_Bin_Values[10][18][2] = 7359;
z_pT_Bin_Borders[10][19][0] = 0.32; z_pT_Bin_Borders[10][19][1] = 0.26; z_pT_Bin_Borders[10][19][2] = 0.21; z_pT_Bin_Borders[10][19][3] = 0.05;
Phi_h_Bin_Values[10][19][0] =  24; Phi_h_Bin_Values[10][19][1] = 432; Phi_h_Bin_Values[10][19][2] = 7383;
z_pT_Bin_Borders[10][20][0] = 0.32; z_pT_Bin_Borders[10][20][1] = 0.26; z_pT_Bin_Borders[10][20][2] = 0.31; z_pT_Bin_Borders[10][20][3] = 0.21;
Phi_h_Bin_Values[10][20][0] =  24; Phi_h_Bin_Values[10][20][1] = 456; Phi_h_Bin_Values[10][20][2] = 7407;
z_pT_Bin_Borders[10][21][0] = 0.32; z_pT_Bin_Borders[10][21][1] = 0.26; z_pT_Bin_Borders[10][21][2] = 0.4; z_pT_Bin_Borders[10][21][3] = 0.31;
Phi_h_Bin_Values[10][21][0] =  24; Phi_h_Bin_Values[10][21][1] = 480; Phi_h_Bin_Values[10][21][2] = 7431;
z_pT_Bin_Borders[10][22][0] = 0.32; z_pT_Bin_Borders[10][22][1] = 0.26; z_pT_Bin_Borders[10][22][2] = 0.5; z_pT_Bin_Borders[10][22][3] = 0.4;
Phi_h_Bin_Values[10][22][0] =  24; Phi_h_Bin_Values[10][22][1] = 504; Phi_h_Bin_Values[10][22][2] = 7455;
z_pT_Bin_Borders[10][23][0] = 0.32; z_pT_Bin_Borders[10][23][1] = 0.26; z_pT_Bin_Borders[10][23][2] = 0.64; z_pT_Bin_Borders[10][23][3] = 0.5;
Phi_h_Bin_Values[10][23][0] =  24; Phi_h_Bin_Values[10][23][1] = 528; Phi_h_Bin_Values[10][23][2] = 7479;
z_pT_Bin_Borders[10][24][0] = 0.32; z_pT_Bin_Borders[10][24][1] = 0.26; z_pT_Bin_Borders[10][24][2] = 0.9; z_pT_Bin_Borders[10][24][3] = 0.64;
Phi_h_Bin_Values[10][24][0] =  1; Phi_h_Bin_Values[10][24][1] = 552; Phi_h_Bin_Values[10][24][2] = 7503;
z_pT_Bin_Borders[10][25][0] = 0.26; z_pT_Bin_Borders[10][25][1] = 0.23; z_pT_Bin_Borders[10][25][2] = 0.21; z_pT_Bin_Borders[10][25][3] = 0.05;
Phi_h_Bin_Values[10][25][0] =  24; Phi_h_Bin_Values[10][25][1] = 553; Phi_h_Bin_Values[10][25][2] = 7504;
z_pT_Bin_Borders[10][26][0] = 0.26; z_pT_Bin_Borders[10][26][1] = 0.23; z_pT_Bin_Borders[10][26][2] = 0.31; z_pT_Bin_Borders[10][26][3] = 0.21;
Phi_h_Bin_Values[10][26][0] =  24; Phi_h_Bin_Values[10][26][1] = 577; Phi_h_Bin_Values[10][26][2] = 7528;
z_pT_Bin_Borders[10][27][0] = 0.26; z_pT_Bin_Borders[10][27][1] = 0.23; z_pT_Bin_Borders[10][27][2] = 0.4; z_pT_Bin_Borders[10][27][3] = 0.31;
Phi_h_Bin_Values[10][27][0] =  24; Phi_h_Bin_Values[10][27][1] = 601; Phi_h_Bin_Values[10][27][2] = 7552;
z_pT_Bin_Borders[10][28][0] = 0.26; z_pT_Bin_Borders[10][28][1] = 0.23; z_pT_Bin_Borders[10][28][2] = 0.5; z_pT_Bin_Borders[10][28][3] = 0.4;
Phi_h_Bin_Values[10][28][0] =  24; Phi_h_Bin_Values[10][28][1] = 625; Phi_h_Bin_Values[10][28][2] = 7576;
z_pT_Bin_Borders[10][29][0] = 0.26; z_pT_Bin_Borders[10][29][1] = 0.23; z_pT_Bin_Borders[10][29][2] = 0.64; z_pT_Bin_Borders[10][29][3] = 0.5;
Phi_h_Bin_Values[10][29][0] =  24; Phi_h_Bin_Values[10][29][1] = 649; Phi_h_Bin_Values[10][29][2] = 7600;
z_pT_Bin_Borders[10][30][0] = 0.26; z_pT_Bin_Borders[10][30][1] = 0.23; z_pT_Bin_Borders[10][30][2] = 0.9; z_pT_Bin_Borders[10][30][3] = 0.64;
Phi_h_Bin_Values[10][30][0] =  1; Phi_h_Bin_Values[10][30][1] = 673; Phi_h_Bin_Values[10][30][2] = 7624;
z_pT_Bin_Borders[10][31][0] = 0.23; z_pT_Bin_Borders[10][31][1] = 0.19; z_pT_Bin_Borders[10][31][2] = 0.21; z_pT_Bin_Borders[10][31][3] = 0.05;
Phi_h_Bin_Values[10][31][0] =  24; Phi_h_Bin_Values[10][31][1] = 674; Phi_h_Bin_Values[10][31][2] = 7625;
z_pT_Bin_Borders[10][32][0] = 0.23; z_pT_Bin_Borders[10][32][1] = 0.19; z_pT_Bin_Borders[10][32][2] = 0.31; z_pT_Bin_Borders[10][32][3] = 0.21;
Phi_h_Bin_Values[10][32][0] =  24; Phi_h_Bin_Values[10][32][1] = 698; Phi_h_Bin_Values[10][32][2] = 7649;
z_pT_Bin_Borders[10][33][0] = 0.23; z_pT_Bin_Borders[10][33][1] = 0.19; z_pT_Bin_Borders[10][33][2] = 0.4; z_pT_Bin_Borders[10][33][3] = 0.31;
Phi_h_Bin_Values[10][33][0] =  24; Phi_h_Bin_Values[10][33][1] = 722; Phi_h_Bin_Values[10][33][2] = 7673;
z_pT_Bin_Borders[10][34][0] = 0.23; z_pT_Bin_Borders[10][34][1] = 0.19; z_pT_Bin_Borders[10][34][2] = 0.5; z_pT_Bin_Borders[10][34][3] = 0.4;
Phi_h_Bin_Values[10][34][0] =  24; Phi_h_Bin_Values[10][34][1] = 746; Phi_h_Bin_Values[10][34][2] = 7697;
z_pT_Bin_Borders[10][35][0] = 0.23; z_pT_Bin_Borders[10][35][1] = 0.19; z_pT_Bin_Borders[10][35][2] = 0.64; z_pT_Bin_Borders[10][35][3] = 0.5;
Phi_h_Bin_Values[10][35][0] =  1; Phi_h_Bin_Values[10][35][1] = 770; Phi_h_Bin_Values[10][35][2] = 7721;
z_pT_Bin_Borders[10][36][0] = 0.23; z_pT_Bin_Borders[10][36][1] = 0.19; z_pT_Bin_Borders[10][36][2] = 0.9; z_pT_Bin_Borders[10][36][3] = 0.64;
Phi_h_Bin_Values[10][36][0] =  1; Phi_h_Bin_Values[10][36][1] = 771; Phi_h_Bin_Values[10][36][2] = 7722;
z_pT_Bin_Borders[10][37][0] = 10; z_pT_Bin_Borders[10][37][1] = 0.72; z_pT_Bin_Borders[10][37][2] = 0.05; z_pT_Bin_Borders[10][37][3] = 0;
Phi_h_Bin_Values[10][37][0] =  1; Phi_h_Bin_Values[10][37][1] = 772; Phi_h_Bin_Values[10][37][2] = 7723;
z_pT_Bin_Borders[10][38][0] = 10; z_pT_Bin_Borders[10][38][1] = 0.72; z_pT_Bin_Borders[10][38][2] = 0.21; z_pT_Bin_Borders[10][38][3] = 0.05;
Phi_h_Bin_Values[10][38][0] =  1; Phi_h_Bin_Values[10][38][1] = 773; Phi_h_Bin_Values[10][38][2] = 7724;
z_pT_Bin_Borders[10][39][0] = 10; z_pT_Bin_Borders[10][39][1] = 0.72; z_pT_Bin_Borders[10][39][2] = 0.31; z_pT_Bin_Borders[10][39][3] = 0.21;
Phi_h_Bin_Values[10][39][0] =  1; Phi_h_Bin_Values[10][39][1] = 774; Phi_h_Bin_Values[10][39][2] = 7725;
z_pT_Bin_Borders[10][40][0] = 10; z_pT_Bin_Borders[10][40][1] = 0.72; z_pT_Bin_Borders[10][40][2] = 0.4; z_pT_Bin_Borders[10][40][3] = 0.31;
Phi_h_Bin_Values[10][40][0] =  1; Phi_h_Bin_Values[10][40][1] = 775; Phi_h_Bin_Values[10][40][2] = 7726;
z_pT_Bin_Borders[10][41][0] = 10; z_pT_Bin_Borders[10][41][1] = 0.72; z_pT_Bin_Borders[10][41][2] = 0.5; z_pT_Bin_Borders[10][41][3] = 0.4;
Phi_h_Bin_Values[10][41][0] =  1; Phi_h_Bin_Values[10][41][1] = 776; Phi_h_Bin_Values[10][41][2] = 7727;
z_pT_Bin_Borders[10][42][0] = 10; z_pT_Bin_Borders[10][42][1] = 0.72; z_pT_Bin_Borders[10][42][2] = 0.64; z_pT_Bin_Borders[10][42][3] = 0.5;
Phi_h_Bin_Values[10][42][0] =  1; Phi_h_Bin_Values[10][42][1] = 777; Phi_h_Bin_Values[10][42][2] = 7728;
z_pT_Bin_Borders[10][43][0] = 10; z_pT_Bin_Borders[10][43][1] = 0.72; z_pT_Bin_Borders[10][43][2] = 0.9; z_pT_Bin_Borders[10][43][3] = 0.64;
Phi_h_Bin_Values[10][43][0] =  1; Phi_h_Bin_Values[10][43][1] = 778; Phi_h_Bin_Values[10][43][2] = 7729;
z_pT_Bin_Borders[10][44][0] = 10; z_pT_Bin_Borders[10][44][1] = 0.72; z_pT_Bin_Borders[10][44][2] = 10; z_pT_Bin_Borders[10][44][3] = 0.9;
Phi_h_Bin_Values[10][44][0] =  1; Phi_h_Bin_Values[10][44][1] = 779; Phi_h_Bin_Values[10][44][2] = 7730;
z_pT_Bin_Borders[10][45][0] = 0.72; z_pT_Bin_Borders[10][45][1] = 0.5; z_pT_Bin_Borders[10][45][2] = 0.05; z_pT_Bin_Borders[10][45][3] = 0;
Phi_h_Bin_Values[10][45][0] =  1; Phi_h_Bin_Values[10][45][1] = 780; Phi_h_Bin_Values[10][45][2] = 7731;
z_pT_Bin_Borders[10][46][0] = 0.72; z_pT_Bin_Borders[10][46][1] = 0.5; z_pT_Bin_Borders[10][46][2] = 10; z_pT_Bin_Borders[10][46][3] = 0.9;
Phi_h_Bin_Values[10][46][0] =  1; Phi_h_Bin_Values[10][46][1] = 781; Phi_h_Bin_Values[10][46][2] = 7732;
z_pT_Bin_Borders[10][47][0] = 0.5; z_pT_Bin_Borders[10][47][1] = 0.4; z_pT_Bin_Borders[10][47][2] = 0.05; z_pT_Bin_Borders[10][47][3] = 0;
Phi_h_Bin_Values[10][47][0] =  1; Phi_h_Bin_Values[10][47][1] = 782; Phi_h_Bin_Values[10][47][2] = 7733;
z_pT_Bin_Borders[10][48][0] = 0.5; z_pT_Bin_Borders[10][48][1] = 0.4; z_pT_Bin_Borders[10][48][2] = 10; z_pT_Bin_Borders[10][48][3] = 0.9;
Phi_h_Bin_Values[10][48][0] =  1; Phi_h_Bin_Values[10][48][1] = 783; Phi_h_Bin_Values[10][48][2] = 7734;
z_pT_Bin_Borders[10][49][0] = 0.4; z_pT_Bin_Borders[10][49][1] = 0.32; z_pT_Bin_Borders[10][49][2] = 0.05; z_pT_Bin_Borders[10][49][3] = 0;
Phi_h_Bin_Values[10][49][0] =  1; Phi_h_Bin_Values[10][49][1] = 784; Phi_h_Bin_Values[10][49][2] = 7735;
z_pT_Bin_Borders[10][50][0] = 0.4; z_pT_Bin_Borders[10][50][1] = 0.32; z_pT_Bin_Borders[10][50][2] = 10; z_pT_Bin_Borders[10][50][3] = 0.9;
Phi_h_Bin_Values[10][50][0] =  1; Phi_h_Bin_Values[10][50][1] = 785; Phi_h_Bin_Values[10][50][2] = 7736;
z_pT_Bin_Borders[10][51][0] = 0.32; z_pT_Bin_Borders[10][51][1] = 0.26; z_pT_Bin_Borders[10][51][2] = 0.05; z_pT_Bin_Borders[10][51][3] = 0;
Phi_h_Bin_Values[10][51][0] =  1; Phi_h_Bin_Values[10][51][1] = 786; Phi_h_Bin_Values[10][51][2] = 7737;
z_pT_Bin_Borders[10][52][0] = 0.32; z_pT_Bin_Borders[10][52][1] = 0.26; z_pT_Bin_Borders[10][52][2] = 10; z_pT_Bin_Borders[10][52][3] = 0.9;
Phi_h_Bin_Values[10][52][0] =  1; Phi_h_Bin_Values[10][52][1] = 787; Phi_h_Bin_Values[10][52][2] = 7738;
z_pT_Bin_Borders[10][53][0] = 0.26; z_pT_Bin_Borders[10][53][1] = 0.23; z_pT_Bin_Borders[10][53][2] = 0.05; z_pT_Bin_Borders[10][53][3] = 0;
Phi_h_Bin_Values[10][53][0] =  1; Phi_h_Bin_Values[10][53][1] = 788; Phi_h_Bin_Values[10][53][2] = 7739;
z_pT_Bin_Borders[10][54][0] = 0.26; z_pT_Bin_Borders[10][54][1] = 0.23; z_pT_Bin_Borders[10][54][2] = 10; z_pT_Bin_Borders[10][54][3] = 0.9;
Phi_h_Bin_Values[10][54][0] =  1; Phi_h_Bin_Values[10][54][1] = 789; Phi_h_Bin_Values[10][54][2] = 7740;
z_pT_Bin_Borders[10][55][0] = 0.23; z_pT_Bin_Borders[10][55][1] = 0.19; z_pT_Bin_Borders[10][55][2] = 0.05; z_pT_Bin_Borders[10][55][3] = 0;
Phi_h_Bin_Values[10][55][0] =  1; Phi_h_Bin_Values[10][55][1] = 790; Phi_h_Bin_Values[10][55][2] = 7741;
z_pT_Bin_Borders[10][56][0] = 0.23; z_pT_Bin_Borders[10][56][1] = 0.19; z_pT_Bin_Borders[10][56][2] = 10; z_pT_Bin_Borders[10][56][3] = 0.9;
Phi_h_Bin_Values[10][56][0] =  1; Phi_h_Bin_Values[10][56][1] = 791; Phi_h_Bin_Values[10][56][2] = 7742;
z_pT_Bin_Borders[10][57][0] = 0.19; z_pT_Bin_Borders[10][57][1] = 0; z_pT_Bin_Borders[10][57][2] = 0.05; z_pT_Bin_Borders[10][57][3] = 0;
Phi_h_Bin_Values[10][57][0] =  1; Phi_h_Bin_Values[10][57][1] = 792; Phi_h_Bin_Values[10][57][2] = 7743;
z_pT_Bin_Borders[10][58][0] = 0.19; z_pT_Bin_Borders[10][58][1] = 0; z_pT_Bin_Borders[10][58][2] = 0.21; z_pT_Bin_Borders[10][58][3] = 0.05;
Phi_h_Bin_Values[10][58][0] =  1; Phi_h_Bin_Values[10][58][1] = 793; Phi_h_Bin_Values[10][58][2] = 7744;
z_pT_Bin_Borders[10][59][0] = 0.19; z_pT_Bin_Borders[10][59][1] = 0; z_pT_Bin_Borders[10][59][2] = 0.31; z_pT_Bin_Borders[10][59][3] = 0.21;
Phi_h_Bin_Values[10][59][0] =  1; Phi_h_Bin_Values[10][59][1] = 794; Phi_h_Bin_Values[10][59][2] = 7745;
z_pT_Bin_Borders[10][60][0] = 0.19; z_pT_Bin_Borders[10][60][1] = 0; z_pT_Bin_Borders[10][60][2] = 0.4; z_pT_Bin_Borders[10][60][3] = 0.31;
Phi_h_Bin_Values[10][60][0] =  1; Phi_h_Bin_Values[10][60][1] = 795; Phi_h_Bin_Values[10][60][2] = 7746;
z_pT_Bin_Borders[10][61][0] = 0.19; z_pT_Bin_Borders[10][61][1] = 0; z_pT_Bin_Borders[10][61][2] = 0.5; z_pT_Bin_Borders[10][61][3] = 0.4;
Phi_h_Bin_Values[10][61][0] =  1; Phi_h_Bin_Values[10][61][1] = 796; Phi_h_Bin_Values[10][61][2] = 7747;
z_pT_Bin_Borders[10][62][0] = 0.19; z_pT_Bin_Borders[10][62][1] = 0; z_pT_Bin_Borders[10][62][2] = 0.64; z_pT_Bin_Borders[10][62][3] = 0.5;
Phi_h_Bin_Values[10][62][0] =  1; Phi_h_Bin_Values[10][62][1] = 797; Phi_h_Bin_Values[10][62][2] = 7748;
z_pT_Bin_Borders[10][63][0] = 0.19; z_pT_Bin_Borders[10][63][1] = 0; z_pT_Bin_Borders[10][63][2] = 0.9; z_pT_Bin_Borders[10][63][3] = 0.64;
Phi_h_Bin_Values[10][63][0] =  1; Phi_h_Bin_Values[10][63][1] = 798; Phi_h_Bin_Values[10][63][2] = 7749;
z_pT_Bin_Borders[10][64][0] = 0.19; z_pT_Bin_Borders[10][64][1] = 0; z_pT_Bin_Borders[10][64][2] = 10; z_pT_Bin_Borders[10][64][3] = 0.9;
Phi_h_Bin_Values[10][64][0] =  1; Phi_h_Bin_Values[10][64][1] = 799; Phi_h_Bin_Values[10][64][2] = 7750;
z_pT_Bin_Borders[11][1][0] = 0.73; z_pT_Bin_Borders[11][1][1] = 0.52; z_pT_Bin_Borders[11][1][2] = 0.2; z_pT_Bin_Borders[11][1][3] = 0.05;
Phi_h_Bin_Values[11][1][0] =  24; Phi_h_Bin_Values[11][1][1] = 0; Phi_h_Bin_Values[11][1][2] = 7751;
z_pT_Bin_Borders[11][2][0] = 0.73; z_pT_Bin_Borders[11][2][1] = 0.52; z_pT_Bin_Borders[11][2][2] = 0.3; z_pT_Bin_Borders[11][2][3] = 0.2;
Phi_h_Bin_Values[11][2][0] =  24; Phi_h_Bin_Values[11][2][1] = 24; Phi_h_Bin_Values[11][2][2] = 7775;
z_pT_Bin_Borders[11][3][0] = 0.73; z_pT_Bin_Borders[11][3][1] = 0.52; z_pT_Bin_Borders[11][3][2] = 0.4; z_pT_Bin_Borders[11][3][3] = 0.3;
Phi_h_Bin_Values[11][3][0] =  24; Phi_h_Bin_Values[11][3][1] = 48; Phi_h_Bin_Values[11][3][2] = 7799;
z_pT_Bin_Borders[11][4][0] = 0.73; z_pT_Bin_Borders[11][4][1] = 0.52; z_pT_Bin_Borders[11][4][2] = 0.53; z_pT_Bin_Borders[11][4][3] = 0.4;
Phi_h_Bin_Values[11][4][0] =  24; Phi_h_Bin_Values[11][4][1] = 72; Phi_h_Bin_Values[11][4][2] = 7823;
z_pT_Bin_Borders[11][5][0] = 0.73; z_pT_Bin_Borders[11][5][1] = 0.52; z_pT_Bin_Borders[11][5][2] = 0.69; z_pT_Bin_Borders[11][5][3] = 0.53;
Phi_h_Bin_Values[11][5][0] =  24; Phi_h_Bin_Values[11][5][1] = 96; Phi_h_Bin_Values[11][5][2] = 7847;
z_pT_Bin_Borders[11][6][0] = 0.52; z_pT_Bin_Borders[11][6][1] = 0.39; z_pT_Bin_Borders[11][6][2] = 0.2; z_pT_Bin_Borders[11][6][3] = 0.05;
Phi_h_Bin_Values[11][6][0] =  24; Phi_h_Bin_Values[11][6][1] = 120; Phi_h_Bin_Values[11][6][2] = 7871;
z_pT_Bin_Borders[11][7][0] = 0.52; z_pT_Bin_Borders[11][7][1] = 0.39; z_pT_Bin_Borders[11][7][2] = 0.3; z_pT_Bin_Borders[11][7][3] = 0.2;
Phi_h_Bin_Values[11][7][0] =  24; Phi_h_Bin_Values[11][7][1] = 144; Phi_h_Bin_Values[11][7][2] = 7895;
z_pT_Bin_Borders[11][8][0] = 0.52; z_pT_Bin_Borders[11][8][1] = 0.39; z_pT_Bin_Borders[11][8][2] = 0.4; z_pT_Bin_Borders[11][8][3] = 0.3;
Phi_h_Bin_Values[11][8][0] =  24; Phi_h_Bin_Values[11][8][1] = 168; Phi_h_Bin_Values[11][8][2] = 7919;
z_pT_Bin_Borders[11][9][0] = 0.52; z_pT_Bin_Borders[11][9][1] = 0.39; z_pT_Bin_Borders[11][9][2] = 0.53; z_pT_Bin_Borders[11][9][3] = 0.4;
Phi_h_Bin_Values[11][9][0] =  24; Phi_h_Bin_Values[11][9][1] = 192; Phi_h_Bin_Values[11][9][2] = 7943;
z_pT_Bin_Borders[11][10][0] = 0.52; z_pT_Bin_Borders[11][10][1] = 0.39; z_pT_Bin_Borders[11][10][2] = 0.69; z_pT_Bin_Borders[11][10][3] = 0.53;
Phi_h_Bin_Values[11][10][0] =  24; Phi_h_Bin_Values[11][10][1] = 216; Phi_h_Bin_Values[11][10][2] = 7967;
z_pT_Bin_Borders[11][11][0] = 0.39; z_pT_Bin_Borders[11][11][1] = 0.32; z_pT_Bin_Borders[11][11][2] = 0.2; z_pT_Bin_Borders[11][11][3] = 0.05;
Phi_h_Bin_Values[11][11][0] =  24; Phi_h_Bin_Values[11][11][1] = 240; Phi_h_Bin_Values[11][11][2] = 7991;
z_pT_Bin_Borders[11][12][0] = 0.39; z_pT_Bin_Borders[11][12][1] = 0.32; z_pT_Bin_Borders[11][12][2] = 0.3; z_pT_Bin_Borders[11][12][3] = 0.2;
Phi_h_Bin_Values[11][12][0] =  24; Phi_h_Bin_Values[11][12][1] = 264; Phi_h_Bin_Values[11][12][2] = 8015;
z_pT_Bin_Borders[11][13][0] = 0.39; z_pT_Bin_Borders[11][13][1] = 0.32; z_pT_Bin_Borders[11][13][2] = 0.4; z_pT_Bin_Borders[11][13][3] = 0.3;
Phi_h_Bin_Values[11][13][0] =  24; Phi_h_Bin_Values[11][13][1] = 288; Phi_h_Bin_Values[11][13][2] = 8039;
z_pT_Bin_Borders[11][14][0] = 0.39; z_pT_Bin_Borders[11][14][1] = 0.32; z_pT_Bin_Borders[11][14][2] = 0.53; z_pT_Bin_Borders[11][14][3] = 0.4;
Phi_h_Bin_Values[11][14][0] =  24; Phi_h_Bin_Values[11][14][1] = 312; Phi_h_Bin_Values[11][14][2] = 8063;
z_pT_Bin_Borders[11][15][0] = 0.39; z_pT_Bin_Borders[11][15][1] = 0.32; z_pT_Bin_Borders[11][15][2] = 0.69; z_pT_Bin_Borders[11][15][3] = 0.53;
Phi_h_Bin_Values[11][15][0] =  24; Phi_h_Bin_Values[11][15][1] = 336; Phi_h_Bin_Values[11][15][2] = 8087;
z_pT_Bin_Borders[11][16][0] = 0.32; z_pT_Bin_Borders[11][16][1] = 0.27; z_pT_Bin_Borders[11][16][2] = 0.2; z_pT_Bin_Borders[11][16][3] = 0.05;
Phi_h_Bin_Values[11][16][0] =  24; Phi_h_Bin_Values[11][16][1] = 360; Phi_h_Bin_Values[11][16][2] = 8111;
z_pT_Bin_Borders[11][17][0] = 0.32; z_pT_Bin_Borders[11][17][1] = 0.27; z_pT_Bin_Borders[11][17][2] = 0.3; z_pT_Bin_Borders[11][17][3] = 0.2;
Phi_h_Bin_Values[11][17][0] =  24; Phi_h_Bin_Values[11][17][1] = 384; Phi_h_Bin_Values[11][17][2] = 8135;
z_pT_Bin_Borders[11][18][0] = 0.32; z_pT_Bin_Borders[11][18][1] = 0.27; z_pT_Bin_Borders[11][18][2] = 0.4; z_pT_Bin_Borders[11][18][3] = 0.3;
Phi_h_Bin_Values[11][18][0] =  24; Phi_h_Bin_Values[11][18][1] = 408; Phi_h_Bin_Values[11][18][2] = 8159;
z_pT_Bin_Borders[11][19][0] = 0.32; z_pT_Bin_Borders[11][19][1] = 0.27; z_pT_Bin_Borders[11][19][2] = 0.53; z_pT_Bin_Borders[11][19][3] = 0.4;
Phi_h_Bin_Values[11][19][0] =  24; Phi_h_Bin_Values[11][19][1] = 432; Phi_h_Bin_Values[11][19][2] = 8183;
z_pT_Bin_Borders[11][20][0] = 0.32; z_pT_Bin_Borders[11][20][1] = 0.27; z_pT_Bin_Borders[11][20][2] = 0.69; z_pT_Bin_Borders[11][20][3] = 0.53;
Phi_h_Bin_Values[11][20][0] =  24; Phi_h_Bin_Values[11][20][1] = 456; Phi_h_Bin_Values[11][20][2] = 8207;
z_pT_Bin_Borders[11][21][0] = 0.27; z_pT_Bin_Borders[11][21][1] = 0.22; z_pT_Bin_Borders[11][21][2] = 0.2; z_pT_Bin_Borders[11][21][3] = 0.05;
Phi_h_Bin_Values[11][21][0] =  24; Phi_h_Bin_Values[11][21][1] = 480; Phi_h_Bin_Values[11][21][2] = 8231;
z_pT_Bin_Borders[11][22][0] = 0.27; z_pT_Bin_Borders[11][22][1] = 0.22; z_pT_Bin_Borders[11][22][2] = 0.3; z_pT_Bin_Borders[11][22][3] = 0.2;
Phi_h_Bin_Values[11][22][0] =  24; Phi_h_Bin_Values[11][22][1] = 504; Phi_h_Bin_Values[11][22][2] = 8255;
z_pT_Bin_Borders[11][23][0] = 0.27; z_pT_Bin_Borders[11][23][1] = 0.22; z_pT_Bin_Borders[11][23][2] = 0.4; z_pT_Bin_Borders[11][23][3] = 0.3;
Phi_h_Bin_Values[11][23][0] =  24; Phi_h_Bin_Values[11][23][1] = 528; Phi_h_Bin_Values[11][23][2] = 8279;
z_pT_Bin_Borders[11][24][0] = 0.27; z_pT_Bin_Borders[11][24][1] = 0.22; z_pT_Bin_Borders[11][24][2] = 0.53; z_pT_Bin_Borders[11][24][3] = 0.4;
Phi_h_Bin_Values[11][24][0] =  24; Phi_h_Bin_Values[11][24][1] = 552; Phi_h_Bin_Values[11][24][2] = 8303;
z_pT_Bin_Borders[11][25][0] = 0.27; z_pT_Bin_Borders[11][25][1] = 0.22; z_pT_Bin_Borders[11][25][2] = 0.69; z_pT_Bin_Borders[11][25][3] = 0.53;
Phi_h_Bin_Values[11][25][0] =  1; Phi_h_Bin_Values[11][25][1] = 576; Phi_h_Bin_Values[11][25][2] = 8327;
z_pT_Bin_Borders[11][26][0] = 10; z_pT_Bin_Borders[11][26][1] = 0.73; z_pT_Bin_Borders[11][26][2] = 0.05; z_pT_Bin_Borders[11][26][3] = 0;
Phi_h_Bin_Values[11][26][0] =  1; Phi_h_Bin_Values[11][26][1] = 577; Phi_h_Bin_Values[11][26][2] = 8328;
z_pT_Bin_Borders[11][27][0] = 10; z_pT_Bin_Borders[11][27][1] = 0.73; z_pT_Bin_Borders[11][27][2] = 0.2; z_pT_Bin_Borders[11][27][3] = 0.05;
Phi_h_Bin_Values[11][27][0] =  1; Phi_h_Bin_Values[11][27][1] = 578; Phi_h_Bin_Values[11][27][2] = 8329;
z_pT_Bin_Borders[11][28][0] = 10; z_pT_Bin_Borders[11][28][1] = 0.73; z_pT_Bin_Borders[11][28][2] = 0.3; z_pT_Bin_Borders[11][28][3] = 0.2;
Phi_h_Bin_Values[11][28][0] =  1; Phi_h_Bin_Values[11][28][1] = 579; Phi_h_Bin_Values[11][28][2] = 8330;
z_pT_Bin_Borders[11][29][0] = 10; z_pT_Bin_Borders[11][29][1] = 0.73; z_pT_Bin_Borders[11][29][2] = 0.4; z_pT_Bin_Borders[11][29][3] = 0.3;
Phi_h_Bin_Values[11][29][0] =  1; Phi_h_Bin_Values[11][29][1] = 580; Phi_h_Bin_Values[11][29][2] = 8331;
z_pT_Bin_Borders[11][30][0] = 10; z_pT_Bin_Borders[11][30][1] = 0.73; z_pT_Bin_Borders[11][30][2] = 0.53; z_pT_Bin_Borders[11][30][3] = 0.4;
Phi_h_Bin_Values[11][30][0] =  1; Phi_h_Bin_Values[11][30][1] = 581; Phi_h_Bin_Values[11][30][2] = 8332;
z_pT_Bin_Borders[11][31][0] = 10; z_pT_Bin_Borders[11][31][1] = 0.73; z_pT_Bin_Borders[11][31][2] = 0.69; z_pT_Bin_Borders[11][31][3] = 0.53;
Phi_h_Bin_Values[11][31][0] =  1; Phi_h_Bin_Values[11][31][1] = 582; Phi_h_Bin_Values[11][31][2] = 8333;
z_pT_Bin_Borders[11][32][0] = 10; z_pT_Bin_Borders[11][32][1] = 0.73; z_pT_Bin_Borders[11][32][2] = 10; z_pT_Bin_Borders[11][32][3] = 0.69;
Phi_h_Bin_Values[11][32][0] =  1; Phi_h_Bin_Values[11][32][1] = 583; Phi_h_Bin_Values[11][32][2] = 8334;
z_pT_Bin_Borders[11][33][0] = 0.73; z_pT_Bin_Borders[11][33][1] = 0.52; z_pT_Bin_Borders[11][33][2] = 0.05; z_pT_Bin_Borders[11][33][3] = 0;
Phi_h_Bin_Values[11][33][0] =  1; Phi_h_Bin_Values[11][33][1] = 584; Phi_h_Bin_Values[11][33][2] = 8335;
z_pT_Bin_Borders[11][34][0] = 0.73; z_pT_Bin_Borders[11][34][1] = 0.52; z_pT_Bin_Borders[11][34][2] = 10; z_pT_Bin_Borders[11][34][3] = 0.69;
Phi_h_Bin_Values[11][34][0] =  1; Phi_h_Bin_Values[11][34][1] = 585; Phi_h_Bin_Values[11][34][2] = 8336;
z_pT_Bin_Borders[11][35][0] = 0.52; z_pT_Bin_Borders[11][35][1] = 0.39; z_pT_Bin_Borders[11][35][2] = 0.05; z_pT_Bin_Borders[11][35][3] = 0;
Phi_h_Bin_Values[11][35][0] =  1; Phi_h_Bin_Values[11][35][1] = 586; Phi_h_Bin_Values[11][35][2] = 8337;
z_pT_Bin_Borders[11][36][0] = 0.52; z_pT_Bin_Borders[11][36][1] = 0.39; z_pT_Bin_Borders[11][36][2] = 10; z_pT_Bin_Borders[11][36][3] = 0.69;
Phi_h_Bin_Values[11][36][0] =  1; Phi_h_Bin_Values[11][36][1] = 587; Phi_h_Bin_Values[11][36][2] = 8338;
z_pT_Bin_Borders[11][37][0] = 0.39; z_pT_Bin_Borders[11][37][1] = 0.32; z_pT_Bin_Borders[11][37][2] = 0.05; z_pT_Bin_Borders[11][37][3] = 0;
Phi_h_Bin_Values[11][37][0] =  1; Phi_h_Bin_Values[11][37][1] = 588; Phi_h_Bin_Values[11][37][2] = 8339;
z_pT_Bin_Borders[11][38][0] = 0.39; z_pT_Bin_Borders[11][38][1] = 0.32; z_pT_Bin_Borders[11][38][2] = 10; z_pT_Bin_Borders[11][38][3] = 0.69;
Phi_h_Bin_Values[11][38][0] =  1; Phi_h_Bin_Values[11][38][1] = 589; Phi_h_Bin_Values[11][38][2] = 8340;
z_pT_Bin_Borders[11][39][0] = 0.32; z_pT_Bin_Borders[11][39][1] = 0.27; z_pT_Bin_Borders[11][39][2] = 0.05; z_pT_Bin_Borders[11][39][3] = 0;
Phi_h_Bin_Values[11][39][0] =  1; Phi_h_Bin_Values[11][39][1] = 590; Phi_h_Bin_Values[11][39][2] = 8341;
z_pT_Bin_Borders[11][40][0] = 0.32; z_pT_Bin_Borders[11][40][1] = 0.27; z_pT_Bin_Borders[11][40][2] = 10; z_pT_Bin_Borders[11][40][3] = 0.69;
Phi_h_Bin_Values[11][40][0] =  1; Phi_h_Bin_Values[11][40][1] = 591; Phi_h_Bin_Values[11][40][2] = 8342;
z_pT_Bin_Borders[11][41][0] = 0.27; z_pT_Bin_Borders[11][41][1] = 0.22; z_pT_Bin_Borders[11][41][2] = 0.05; z_pT_Bin_Borders[11][41][3] = 0;
Phi_h_Bin_Values[11][41][0] =  1; Phi_h_Bin_Values[11][41][1] = 592; Phi_h_Bin_Values[11][41][2] = 8343;
z_pT_Bin_Borders[11][42][0] = 0.27; z_pT_Bin_Borders[11][42][1] = 0.22; z_pT_Bin_Borders[11][42][2] = 10; z_pT_Bin_Borders[11][42][3] = 0.69;
Phi_h_Bin_Values[11][42][0] =  1; Phi_h_Bin_Values[11][42][1] = 593; Phi_h_Bin_Values[11][42][2] = 8344;
z_pT_Bin_Borders[11][43][0] = 0.22; z_pT_Bin_Borders[11][43][1] = 0; z_pT_Bin_Borders[11][43][2] = 0.05; z_pT_Bin_Borders[11][43][3] = 0;
Phi_h_Bin_Values[11][43][0] =  1; Phi_h_Bin_Values[11][43][1] = 594; Phi_h_Bin_Values[11][43][2] = 8345;
z_pT_Bin_Borders[11][44][0] = 0.22; z_pT_Bin_Borders[11][44][1] = 0; z_pT_Bin_Borders[11][44][2] = 0.2; z_pT_Bin_Borders[11][44][3] = 0.05;
Phi_h_Bin_Values[11][44][0] =  1; Phi_h_Bin_Values[11][44][1] = 595; Phi_h_Bin_Values[11][44][2] = 8346;
z_pT_Bin_Borders[11][45][0] = 0.22; z_pT_Bin_Borders[11][45][1] = 0; z_pT_Bin_Borders[11][45][2] = 0.3; z_pT_Bin_Borders[11][45][3] = 0.2;
Phi_h_Bin_Values[11][45][0] =  1; Phi_h_Bin_Values[11][45][1] = 596; Phi_h_Bin_Values[11][45][2] = 8347;
z_pT_Bin_Borders[11][46][0] = 0.22; z_pT_Bin_Borders[11][46][1] = 0; z_pT_Bin_Borders[11][46][2] = 0.4; z_pT_Bin_Borders[11][46][3] = 0.3;
Phi_h_Bin_Values[11][46][0] =  1; Phi_h_Bin_Values[11][46][1] = 597; Phi_h_Bin_Values[11][46][2] = 8348;
z_pT_Bin_Borders[11][47][0] = 0.22; z_pT_Bin_Borders[11][47][1] = 0; z_pT_Bin_Borders[11][47][2] = 0.53; z_pT_Bin_Borders[11][47][3] = 0.4;
Phi_h_Bin_Values[11][47][0] =  1; Phi_h_Bin_Values[11][47][1] = 598; Phi_h_Bin_Values[11][47][2] = 8349;
z_pT_Bin_Borders[11][48][0] = 0.22; z_pT_Bin_Borders[11][48][1] = 0; z_pT_Bin_Borders[11][48][2] = 0.69; z_pT_Bin_Borders[11][48][3] = 0.53;
Phi_h_Bin_Values[11][48][0] =  1; Phi_h_Bin_Values[11][48][1] = 599; Phi_h_Bin_Values[11][48][2] = 8350;
z_pT_Bin_Borders[11][49][0] = 0.22; z_pT_Bin_Borders[11][49][1] = 0; z_pT_Bin_Borders[11][49][2] = 10; z_pT_Bin_Borders[11][49][3] = 0.69;
Phi_h_Bin_Values[11][49][0] =  1; Phi_h_Bin_Values[11][49][1] = 600; Phi_h_Bin_Values[11][49][2] = 8351;
z_pT_Bin_Borders[12][1][0] = 0.7; z_pT_Bin_Borders[12][1][1] = 0.51; z_pT_Bin_Borders[12][1][2] = 0.2; z_pT_Bin_Borders[12][1][3] = 0.05;
Phi_h_Bin_Values[12][1][0] =  24; Phi_h_Bin_Values[12][1][1] = 0; Phi_h_Bin_Values[12][1][2] = 8352;
z_pT_Bin_Borders[12][2][0] = 0.7; z_pT_Bin_Borders[12][2][1] = 0.51; z_pT_Bin_Borders[12][2][2] = 0.28; z_pT_Bin_Borders[12][2][3] = 0.2;
Phi_h_Bin_Values[12][2][0] =  24; Phi_h_Bin_Values[12][2][1] = 24; Phi_h_Bin_Values[12][2][2] = 8376;
z_pT_Bin_Borders[12][3][0] = 0.7; z_pT_Bin_Borders[12][3][1] = 0.51; z_pT_Bin_Borders[12][3][2] = 0.36; z_pT_Bin_Borders[12][3][3] = 0.28;
Phi_h_Bin_Values[12][3][0] =  24; Phi_h_Bin_Values[12][3][1] = 48; Phi_h_Bin_Values[12][3][2] = 8400;
z_pT_Bin_Borders[12][4][0] = 0.7; z_pT_Bin_Borders[12][4][1] = 0.51; z_pT_Bin_Borders[12][4][2] = 0.45; z_pT_Bin_Borders[12][4][3] = 0.36;
Phi_h_Bin_Values[12][4][0] =  24; Phi_h_Bin_Values[12][4][1] = 72; Phi_h_Bin_Values[12][4][2] = 8424;
z_pT_Bin_Borders[12][5][0] = 0.7; z_pT_Bin_Borders[12][5][1] = 0.51; z_pT_Bin_Borders[12][5][2] = 0.6; z_pT_Bin_Borders[12][5][3] = 0.45;
Phi_h_Bin_Values[12][5][0] =  1; Phi_h_Bin_Values[12][5][1] = 96; Phi_h_Bin_Values[12][5][2] = 8448;
z_pT_Bin_Borders[12][6][0] = 0.51; z_pT_Bin_Borders[12][6][1] = 0.43; z_pT_Bin_Borders[12][6][2] = 0.2; z_pT_Bin_Borders[12][6][3] = 0.05;
Phi_h_Bin_Values[12][6][0] =  24; Phi_h_Bin_Values[12][6][1] = 97; Phi_h_Bin_Values[12][6][2] = 8449;
z_pT_Bin_Borders[12][7][0] = 0.51; z_pT_Bin_Borders[12][7][1] = 0.43; z_pT_Bin_Borders[12][7][2] = 0.28; z_pT_Bin_Borders[12][7][3] = 0.2;
Phi_h_Bin_Values[12][7][0] =  24; Phi_h_Bin_Values[12][7][1] = 121; Phi_h_Bin_Values[12][7][2] = 8473;
z_pT_Bin_Borders[12][8][0] = 0.51; z_pT_Bin_Borders[12][8][1] = 0.43; z_pT_Bin_Borders[12][8][2] = 0.36; z_pT_Bin_Borders[12][8][3] = 0.28;
Phi_h_Bin_Values[12][8][0] =  24; Phi_h_Bin_Values[12][8][1] = 145; Phi_h_Bin_Values[12][8][2] = 8497;
z_pT_Bin_Borders[12][9][0] = 0.51; z_pT_Bin_Borders[12][9][1] = 0.43; z_pT_Bin_Borders[12][9][2] = 0.45; z_pT_Bin_Borders[12][9][3] = 0.36;
Phi_h_Bin_Values[12][9][0] =  24; Phi_h_Bin_Values[12][9][1] = 169; Phi_h_Bin_Values[12][9][2] = 8521;
z_pT_Bin_Borders[12][10][0] = 0.51; z_pT_Bin_Borders[12][10][1] = 0.43; z_pT_Bin_Borders[12][10][2] = 0.6; z_pT_Bin_Borders[12][10][3] = 0.45;
Phi_h_Bin_Values[12][10][0] =  24; Phi_h_Bin_Values[12][10][1] = 193; Phi_h_Bin_Values[12][10][2] = 8545;
z_pT_Bin_Borders[12][11][0] = 0.43; z_pT_Bin_Borders[12][11][1] = 0.37; z_pT_Bin_Borders[12][11][2] = 0.2; z_pT_Bin_Borders[12][11][3] = 0.05;
Phi_h_Bin_Values[12][11][0] =  24; Phi_h_Bin_Values[12][11][1] = 217; Phi_h_Bin_Values[12][11][2] = 8569;
z_pT_Bin_Borders[12][12][0] = 0.43; z_pT_Bin_Borders[12][12][1] = 0.37; z_pT_Bin_Borders[12][12][2] = 0.28; z_pT_Bin_Borders[12][12][3] = 0.2;
Phi_h_Bin_Values[12][12][0] =  24; Phi_h_Bin_Values[12][12][1] = 241; Phi_h_Bin_Values[12][12][2] = 8593;
z_pT_Bin_Borders[12][13][0] = 0.43; z_pT_Bin_Borders[12][13][1] = 0.37; z_pT_Bin_Borders[12][13][2] = 0.36; z_pT_Bin_Borders[12][13][3] = 0.28;
Phi_h_Bin_Values[12][13][0] =  24; Phi_h_Bin_Values[12][13][1] = 265; Phi_h_Bin_Values[12][13][2] = 8617;
z_pT_Bin_Borders[12][14][0] = 0.43; z_pT_Bin_Borders[12][14][1] = 0.37; z_pT_Bin_Borders[12][14][2] = 0.45; z_pT_Bin_Borders[12][14][3] = 0.36;
Phi_h_Bin_Values[12][14][0] =  24; Phi_h_Bin_Values[12][14][1] = 289; Phi_h_Bin_Values[12][14][2] = 8641;
z_pT_Bin_Borders[12][15][0] = 0.43; z_pT_Bin_Borders[12][15][1] = 0.37; z_pT_Bin_Borders[12][15][2] = 0.6; z_pT_Bin_Borders[12][15][3] = 0.45;
Phi_h_Bin_Values[12][15][0] =  24; Phi_h_Bin_Values[12][15][1] = 313; Phi_h_Bin_Values[12][15][2] = 8665;
z_pT_Bin_Borders[12][16][0] = 0.37; z_pT_Bin_Borders[12][16][1] = 0.33; z_pT_Bin_Borders[12][16][2] = 0.2; z_pT_Bin_Borders[12][16][3] = 0.05;
Phi_h_Bin_Values[12][16][0] =  24; Phi_h_Bin_Values[12][16][1] = 337; Phi_h_Bin_Values[12][16][2] = 8689;
z_pT_Bin_Borders[12][17][0] = 0.37; z_pT_Bin_Borders[12][17][1] = 0.33; z_pT_Bin_Borders[12][17][2] = 0.28; z_pT_Bin_Borders[12][17][3] = 0.2;
Phi_h_Bin_Values[12][17][0] =  24; Phi_h_Bin_Values[12][17][1] = 361; Phi_h_Bin_Values[12][17][2] = 8713;
z_pT_Bin_Borders[12][18][0] = 0.37; z_pT_Bin_Borders[12][18][1] = 0.33; z_pT_Bin_Borders[12][18][2] = 0.36; z_pT_Bin_Borders[12][18][3] = 0.28;
Phi_h_Bin_Values[12][18][0] =  24; Phi_h_Bin_Values[12][18][1] = 385; Phi_h_Bin_Values[12][18][2] = 8737;
z_pT_Bin_Borders[12][19][0] = 0.37; z_pT_Bin_Borders[12][19][1] = 0.33; z_pT_Bin_Borders[12][19][2] = 0.45; z_pT_Bin_Borders[12][19][3] = 0.36;
Phi_h_Bin_Values[12][19][0] =  24; Phi_h_Bin_Values[12][19][1] = 409; Phi_h_Bin_Values[12][19][2] = 8761;
z_pT_Bin_Borders[12][20][0] = 0.37; z_pT_Bin_Borders[12][20][1] = 0.33; z_pT_Bin_Borders[12][20][2] = 0.6; z_pT_Bin_Borders[12][20][3] = 0.45;
Phi_h_Bin_Values[12][20][0] =  24; Phi_h_Bin_Values[12][20][1] = 433; Phi_h_Bin_Values[12][20][2] = 8785;
z_pT_Bin_Borders[12][21][0] = 0.33; z_pT_Bin_Borders[12][21][1] = 0.27; z_pT_Bin_Borders[12][21][2] = 0.2; z_pT_Bin_Borders[12][21][3] = 0.05;
Phi_h_Bin_Values[12][21][0] =  24; Phi_h_Bin_Values[12][21][1] = 457; Phi_h_Bin_Values[12][21][2] = 8809;
z_pT_Bin_Borders[12][22][0] = 0.33; z_pT_Bin_Borders[12][22][1] = 0.27; z_pT_Bin_Borders[12][22][2] = 0.28; z_pT_Bin_Borders[12][22][3] = 0.2;
Phi_h_Bin_Values[12][22][0] =  24; Phi_h_Bin_Values[12][22][1] = 481; Phi_h_Bin_Values[12][22][2] = 8833;
z_pT_Bin_Borders[12][23][0] = 0.33; z_pT_Bin_Borders[12][23][1] = 0.27; z_pT_Bin_Borders[12][23][2] = 0.36; z_pT_Bin_Borders[12][23][3] = 0.28;
Phi_h_Bin_Values[12][23][0] =  24; Phi_h_Bin_Values[12][23][1] = 505; Phi_h_Bin_Values[12][23][2] = 8857;
z_pT_Bin_Borders[12][24][0] = 0.33; z_pT_Bin_Borders[12][24][1] = 0.27; z_pT_Bin_Borders[12][24][2] = 0.45; z_pT_Bin_Borders[12][24][3] = 0.36;
Phi_h_Bin_Values[12][24][0] =  24; Phi_h_Bin_Values[12][24][1] = 529; Phi_h_Bin_Values[12][24][2] = 8881;
z_pT_Bin_Borders[12][25][0] = 0.33; z_pT_Bin_Borders[12][25][1] = 0.27; z_pT_Bin_Borders[12][25][2] = 0.6; z_pT_Bin_Borders[12][25][3] = 0.45;
Phi_h_Bin_Values[12][25][0] =  24; Phi_h_Bin_Values[12][25][1] = 553; Phi_h_Bin_Values[12][25][2] = 8905;
z_pT_Bin_Borders[12][26][0] = 10; z_pT_Bin_Borders[12][26][1] = 0.7; z_pT_Bin_Borders[12][26][2] = 0.05; z_pT_Bin_Borders[12][26][3] = 0;
Phi_h_Bin_Values[12][26][0] =  1; Phi_h_Bin_Values[12][26][1] = 577; Phi_h_Bin_Values[12][26][2] = 8929;
z_pT_Bin_Borders[12][27][0] = 10; z_pT_Bin_Borders[12][27][1] = 0.7; z_pT_Bin_Borders[12][27][2] = 0.2; z_pT_Bin_Borders[12][27][3] = 0.05;
Phi_h_Bin_Values[12][27][0] =  1; Phi_h_Bin_Values[12][27][1] = 578; Phi_h_Bin_Values[12][27][2] = 8930;
z_pT_Bin_Borders[12][28][0] = 10; z_pT_Bin_Borders[12][28][1] = 0.7; z_pT_Bin_Borders[12][28][2] = 0.28; z_pT_Bin_Borders[12][28][3] = 0.2;
Phi_h_Bin_Values[12][28][0] =  1; Phi_h_Bin_Values[12][28][1] = 579; Phi_h_Bin_Values[12][28][2] = 8931;
z_pT_Bin_Borders[12][29][0] = 10; z_pT_Bin_Borders[12][29][1] = 0.7; z_pT_Bin_Borders[12][29][2] = 0.36; z_pT_Bin_Borders[12][29][3] = 0.28;
Phi_h_Bin_Values[12][29][0] =  1; Phi_h_Bin_Values[12][29][1] = 580; Phi_h_Bin_Values[12][29][2] = 8932;
z_pT_Bin_Borders[12][30][0] = 10; z_pT_Bin_Borders[12][30][1] = 0.7; z_pT_Bin_Borders[12][30][2] = 0.45; z_pT_Bin_Borders[12][30][3] = 0.36;
Phi_h_Bin_Values[12][30][0] =  1; Phi_h_Bin_Values[12][30][1] = 581; Phi_h_Bin_Values[12][30][2] = 8933;
z_pT_Bin_Borders[12][31][0] = 10; z_pT_Bin_Borders[12][31][1] = 0.7; z_pT_Bin_Borders[12][31][2] = 0.6; z_pT_Bin_Borders[12][31][3] = 0.45;
Phi_h_Bin_Values[12][31][0] =  1; Phi_h_Bin_Values[12][31][1] = 582; Phi_h_Bin_Values[12][31][2] = 8934;
z_pT_Bin_Borders[12][32][0] = 10; z_pT_Bin_Borders[12][32][1] = 0.7; z_pT_Bin_Borders[12][32][2] = 10; z_pT_Bin_Borders[12][32][3] = 0.6;
Phi_h_Bin_Values[12][32][0] =  1; Phi_h_Bin_Values[12][32][1] = 583; Phi_h_Bin_Values[12][32][2] = 8935;
z_pT_Bin_Borders[12][33][0] = 0.7; z_pT_Bin_Borders[12][33][1] = 0.51; z_pT_Bin_Borders[12][33][2] = 0.05; z_pT_Bin_Borders[12][33][3] = 0;
Phi_h_Bin_Values[12][33][0] =  1; Phi_h_Bin_Values[12][33][1] = 584; Phi_h_Bin_Values[12][33][2] = 8936;
z_pT_Bin_Borders[12][34][0] = 0.7; z_pT_Bin_Borders[12][34][1] = 0.51; z_pT_Bin_Borders[12][34][2] = 10; z_pT_Bin_Borders[12][34][3] = 0.6;
Phi_h_Bin_Values[12][34][0] =  1; Phi_h_Bin_Values[12][34][1] = 585; Phi_h_Bin_Values[12][34][2] = 8937;
z_pT_Bin_Borders[12][35][0] = 0.51; z_pT_Bin_Borders[12][35][1] = 0.43; z_pT_Bin_Borders[12][35][2] = 0.05; z_pT_Bin_Borders[12][35][3] = 0;
Phi_h_Bin_Values[12][35][0] =  1; Phi_h_Bin_Values[12][35][1] = 586; Phi_h_Bin_Values[12][35][2] = 8938;
z_pT_Bin_Borders[12][36][0] = 0.51; z_pT_Bin_Borders[12][36][1] = 0.43; z_pT_Bin_Borders[12][36][2] = 10; z_pT_Bin_Borders[12][36][3] = 0.6;
Phi_h_Bin_Values[12][36][0] =  1; Phi_h_Bin_Values[12][36][1] = 587; Phi_h_Bin_Values[12][36][2] = 8939;
z_pT_Bin_Borders[12][37][0] = 0.43; z_pT_Bin_Borders[12][37][1] = 0.37; z_pT_Bin_Borders[12][37][2] = 0.05; z_pT_Bin_Borders[12][37][3] = 0;
Phi_h_Bin_Values[12][37][0] =  1; Phi_h_Bin_Values[12][37][1] = 588; Phi_h_Bin_Values[12][37][2] = 8940;
z_pT_Bin_Borders[12][38][0] = 0.43; z_pT_Bin_Borders[12][38][1] = 0.37; z_pT_Bin_Borders[12][38][2] = 10; z_pT_Bin_Borders[12][38][3] = 0.6;
Phi_h_Bin_Values[12][38][0] =  1; Phi_h_Bin_Values[12][38][1] = 589; Phi_h_Bin_Values[12][38][2] = 8941;
z_pT_Bin_Borders[12][39][0] = 0.37; z_pT_Bin_Borders[12][39][1] = 0.33; z_pT_Bin_Borders[12][39][2] = 0.05; z_pT_Bin_Borders[12][39][3] = 0;
Phi_h_Bin_Values[12][39][0] =  1; Phi_h_Bin_Values[12][39][1] = 590; Phi_h_Bin_Values[12][39][2] = 8942;
z_pT_Bin_Borders[12][40][0] = 0.37; z_pT_Bin_Borders[12][40][1] = 0.33; z_pT_Bin_Borders[12][40][2] = 10; z_pT_Bin_Borders[12][40][3] = 0.6;
Phi_h_Bin_Values[12][40][0] =  1; Phi_h_Bin_Values[12][40][1] = 591; Phi_h_Bin_Values[12][40][2] = 8943;
z_pT_Bin_Borders[12][41][0] = 0.33; z_pT_Bin_Borders[12][41][1] = 0.27; z_pT_Bin_Borders[12][41][2] = 0.05; z_pT_Bin_Borders[12][41][3] = 0;
Phi_h_Bin_Values[12][41][0] =  1; Phi_h_Bin_Values[12][41][1] = 592; Phi_h_Bin_Values[12][41][2] = 8944;
z_pT_Bin_Borders[12][42][0] = 0.33; z_pT_Bin_Borders[12][42][1] = 0.27; z_pT_Bin_Borders[12][42][2] = 10; z_pT_Bin_Borders[12][42][3] = 0.6;
Phi_h_Bin_Values[12][42][0] =  1; Phi_h_Bin_Values[12][42][1] = 593; Phi_h_Bin_Values[12][42][2] = 8945;
z_pT_Bin_Borders[12][43][0] = 0.27; z_pT_Bin_Borders[12][43][1] = 0; z_pT_Bin_Borders[12][43][2] = 0.05; z_pT_Bin_Borders[12][43][3] = 0;
Phi_h_Bin_Values[12][43][0] =  1; Phi_h_Bin_Values[12][43][1] = 594; Phi_h_Bin_Values[12][43][2] = 8946;
z_pT_Bin_Borders[12][44][0] = 0.27; z_pT_Bin_Borders[12][44][1] = 0; z_pT_Bin_Borders[12][44][2] = 0.2; z_pT_Bin_Borders[12][44][3] = 0.05;
Phi_h_Bin_Values[12][44][0] =  1; Phi_h_Bin_Values[12][44][1] = 595; Phi_h_Bin_Values[12][44][2] = 8947;
z_pT_Bin_Borders[12][45][0] = 0.27; z_pT_Bin_Borders[12][45][1] = 0; z_pT_Bin_Borders[12][45][2] = 0.28; z_pT_Bin_Borders[12][45][3] = 0.2;
Phi_h_Bin_Values[12][45][0] =  1; Phi_h_Bin_Values[12][45][1] = 596; Phi_h_Bin_Values[12][45][2] = 8948;
z_pT_Bin_Borders[12][46][0] = 0.27; z_pT_Bin_Borders[12][46][1] = 0; z_pT_Bin_Borders[12][46][2] = 0.36; z_pT_Bin_Borders[12][46][3] = 0.28;
Phi_h_Bin_Values[12][46][0] =  1; Phi_h_Bin_Values[12][46][1] = 597; Phi_h_Bin_Values[12][46][2] = 8949;
z_pT_Bin_Borders[12][47][0] = 0.27; z_pT_Bin_Borders[12][47][1] = 0; z_pT_Bin_Borders[12][47][2] = 0.45; z_pT_Bin_Borders[12][47][3] = 0.36;
Phi_h_Bin_Values[12][47][0] =  1; Phi_h_Bin_Values[12][47][1] = 598; Phi_h_Bin_Values[12][47][2] = 8950;
z_pT_Bin_Borders[12][48][0] = 0.27; z_pT_Bin_Borders[12][48][1] = 0; z_pT_Bin_Borders[12][48][2] = 0.6; z_pT_Bin_Borders[12][48][3] = 0.45;
Phi_h_Bin_Values[12][48][0] =  1; Phi_h_Bin_Values[12][48][1] = 599; Phi_h_Bin_Values[12][48][2] = 8951;
z_pT_Bin_Borders[12][49][0] = 0.27; z_pT_Bin_Borders[12][49][1] = 0; z_pT_Bin_Borders[12][49][2] = 10; z_pT_Bin_Borders[12][49][3] = 0.6;
Phi_h_Bin_Values[12][49][0] =  1; Phi_h_Bin_Values[12][49][1] = 600; Phi_h_Bin_Values[12][49][2] = 8952;
z_pT_Bin_Borders[13][1][0] = 0.72; z_pT_Bin_Borders[13][1][1] = 0.46; z_pT_Bin_Borders[13][1][2] = 0.22; z_pT_Bin_Borders[13][1][3] = 0.05;
Phi_h_Bin_Values[13][1][0] =  24; Phi_h_Bin_Values[13][1][1] = 0; Phi_h_Bin_Values[13][1][2] = 8953;
z_pT_Bin_Borders[13][2][0] = 0.72; z_pT_Bin_Borders[13][2][1] = 0.46; z_pT_Bin_Borders[13][2][2] = 0.34; z_pT_Bin_Borders[13][2][3] = 0.22;
Phi_h_Bin_Values[13][2][0] =  24; Phi_h_Bin_Values[13][2][1] = 24; Phi_h_Bin_Values[13][2][2] = 8977;
z_pT_Bin_Borders[13][3][0] = 0.72; z_pT_Bin_Borders[13][3][1] = 0.46; z_pT_Bin_Borders[13][3][2] = 0.44; z_pT_Bin_Borders[13][3][3] = 0.34;
Phi_h_Bin_Values[13][3][0] =  24; Phi_h_Bin_Values[13][3][1] = 48; Phi_h_Bin_Values[13][3][2] = 9001;
z_pT_Bin_Borders[13][4][0] = 0.72; z_pT_Bin_Borders[13][4][1] = 0.46; z_pT_Bin_Borders[13][4][2] = 0.58; z_pT_Bin_Borders[13][4][3] = 0.44;
Phi_h_Bin_Values[13][4][0] =  24; Phi_h_Bin_Values[13][4][1] = 72; Phi_h_Bin_Values[13][4][2] = 9025;
z_pT_Bin_Borders[13][5][0] = 0.72; z_pT_Bin_Borders[13][5][1] = 0.46; z_pT_Bin_Borders[13][5][2] = 0.9; z_pT_Bin_Borders[13][5][3] = 0.58;
Phi_h_Bin_Values[13][5][0] =  24; Phi_h_Bin_Values[13][5][1] = 96; Phi_h_Bin_Values[13][5][2] = 9049;
z_pT_Bin_Borders[13][6][0] = 0.46; z_pT_Bin_Borders[13][6][1] = 0.35; z_pT_Bin_Borders[13][6][2] = 0.22; z_pT_Bin_Borders[13][6][3] = 0.05;
Phi_h_Bin_Values[13][6][0] =  24; Phi_h_Bin_Values[13][6][1] = 120; Phi_h_Bin_Values[13][6][2] = 9073;
z_pT_Bin_Borders[13][7][0] = 0.46; z_pT_Bin_Borders[13][7][1] = 0.35; z_pT_Bin_Borders[13][7][2] = 0.34; z_pT_Bin_Borders[13][7][3] = 0.22;
Phi_h_Bin_Values[13][7][0] =  24; Phi_h_Bin_Values[13][7][1] = 144; Phi_h_Bin_Values[13][7][2] = 9097;
z_pT_Bin_Borders[13][8][0] = 0.46; z_pT_Bin_Borders[13][8][1] = 0.35; z_pT_Bin_Borders[13][8][2] = 0.44; z_pT_Bin_Borders[13][8][3] = 0.34;
Phi_h_Bin_Values[13][8][0] =  24; Phi_h_Bin_Values[13][8][1] = 168; Phi_h_Bin_Values[13][8][2] = 9121;
z_pT_Bin_Borders[13][9][0] = 0.46; z_pT_Bin_Borders[13][9][1] = 0.35; z_pT_Bin_Borders[13][9][2] = 0.58; z_pT_Bin_Borders[13][9][3] = 0.44;
Phi_h_Bin_Values[13][9][0] =  24; Phi_h_Bin_Values[13][9][1] = 192; Phi_h_Bin_Values[13][9][2] = 9145;
z_pT_Bin_Borders[13][10][0] = 0.46; z_pT_Bin_Borders[13][10][1] = 0.35; z_pT_Bin_Borders[13][10][2] = 0.9; z_pT_Bin_Borders[13][10][3] = 0.58;
Phi_h_Bin_Values[13][10][0] =  24; Phi_h_Bin_Values[13][10][1] = 216; Phi_h_Bin_Values[13][10][2] = 9169;
z_pT_Bin_Borders[13][11][0] = 0.35; z_pT_Bin_Borders[13][11][1] = 0.29; z_pT_Bin_Borders[13][11][2] = 0.22; z_pT_Bin_Borders[13][11][3] = 0.05;
Phi_h_Bin_Values[13][11][0] =  24; Phi_h_Bin_Values[13][11][1] = 240; Phi_h_Bin_Values[13][11][2] = 9193;
z_pT_Bin_Borders[13][12][0] = 0.35; z_pT_Bin_Borders[13][12][1] = 0.29; z_pT_Bin_Borders[13][12][2] = 0.34; z_pT_Bin_Borders[13][12][3] = 0.22;
Phi_h_Bin_Values[13][12][0] =  24; Phi_h_Bin_Values[13][12][1] = 264; Phi_h_Bin_Values[13][12][2] = 9217;
z_pT_Bin_Borders[13][13][0] = 0.35; z_pT_Bin_Borders[13][13][1] = 0.29; z_pT_Bin_Borders[13][13][2] = 0.44; z_pT_Bin_Borders[13][13][3] = 0.34;
Phi_h_Bin_Values[13][13][0] =  24; Phi_h_Bin_Values[13][13][1] = 288; Phi_h_Bin_Values[13][13][2] = 9241;
z_pT_Bin_Borders[13][14][0] = 0.35; z_pT_Bin_Borders[13][14][1] = 0.29; z_pT_Bin_Borders[13][14][2] = 0.58; z_pT_Bin_Borders[13][14][3] = 0.44;
Phi_h_Bin_Values[13][14][0] =  24; Phi_h_Bin_Values[13][14][1] = 312; Phi_h_Bin_Values[13][14][2] = 9265;
z_pT_Bin_Borders[13][15][0] = 0.35; z_pT_Bin_Borders[13][15][1] = 0.29; z_pT_Bin_Borders[13][15][2] = 0.9; z_pT_Bin_Borders[13][15][3] = 0.58;
Phi_h_Bin_Values[13][15][0] =  24; Phi_h_Bin_Values[13][15][1] = 336; Phi_h_Bin_Values[13][15][2] = 9289;
z_pT_Bin_Borders[13][16][0] = 0.29; z_pT_Bin_Borders[13][16][1] = 0.24; z_pT_Bin_Borders[13][16][2] = 0.22; z_pT_Bin_Borders[13][16][3] = 0.05;
Phi_h_Bin_Values[13][16][0] =  24; Phi_h_Bin_Values[13][16][1] = 360; Phi_h_Bin_Values[13][16][2] = 9313;
z_pT_Bin_Borders[13][17][0] = 0.29; z_pT_Bin_Borders[13][17][1] = 0.24; z_pT_Bin_Borders[13][17][2] = 0.34; z_pT_Bin_Borders[13][17][3] = 0.22;
Phi_h_Bin_Values[13][17][0] =  24; Phi_h_Bin_Values[13][17][1] = 384; Phi_h_Bin_Values[13][17][2] = 9337;
z_pT_Bin_Borders[13][18][0] = 0.29; z_pT_Bin_Borders[13][18][1] = 0.24; z_pT_Bin_Borders[13][18][2] = 0.44; z_pT_Bin_Borders[13][18][3] = 0.34;
Phi_h_Bin_Values[13][18][0] =  24; Phi_h_Bin_Values[13][18][1] = 408; Phi_h_Bin_Values[13][18][2] = 9361;
z_pT_Bin_Borders[13][19][0] = 0.29; z_pT_Bin_Borders[13][19][1] = 0.24; z_pT_Bin_Borders[13][19][2] = 0.58; z_pT_Bin_Borders[13][19][3] = 0.44;
Phi_h_Bin_Values[13][19][0] =  24; Phi_h_Bin_Values[13][19][1] = 432; Phi_h_Bin_Values[13][19][2] = 9385;
z_pT_Bin_Borders[13][20][0] = 0.29; z_pT_Bin_Borders[13][20][1] = 0.24; z_pT_Bin_Borders[13][20][2] = 0.9; z_pT_Bin_Borders[13][20][3] = 0.58;
Phi_h_Bin_Values[13][20][0] =  1; Phi_h_Bin_Values[13][20][1] = 456; Phi_h_Bin_Values[13][20][2] = 9409;
z_pT_Bin_Borders[13][21][0] = 0.24; z_pT_Bin_Borders[13][21][1] = 0.2; z_pT_Bin_Borders[13][21][2] = 0.22; z_pT_Bin_Borders[13][21][3] = 0.05;
Phi_h_Bin_Values[13][21][0] =  24; Phi_h_Bin_Values[13][21][1] = 457; Phi_h_Bin_Values[13][21][2] = 9410;
z_pT_Bin_Borders[13][22][0] = 0.24; z_pT_Bin_Borders[13][22][1] = 0.2; z_pT_Bin_Borders[13][22][2] = 0.34; z_pT_Bin_Borders[13][22][3] = 0.22;
Phi_h_Bin_Values[13][22][0] =  24; Phi_h_Bin_Values[13][22][1] = 481; Phi_h_Bin_Values[13][22][2] = 9434;
z_pT_Bin_Borders[13][23][0] = 0.24; z_pT_Bin_Borders[13][23][1] = 0.2; z_pT_Bin_Borders[13][23][2] = 0.44; z_pT_Bin_Borders[13][23][3] = 0.34;
Phi_h_Bin_Values[13][23][0] =  24; Phi_h_Bin_Values[13][23][1] = 505; Phi_h_Bin_Values[13][23][2] = 9458;
z_pT_Bin_Borders[13][24][0] = 0.24; z_pT_Bin_Borders[13][24][1] = 0.2; z_pT_Bin_Borders[13][24][2] = 0.58; z_pT_Bin_Borders[13][24][3] = 0.44;
Phi_h_Bin_Values[13][24][0] =  24; Phi_h_Bin_Values[13][24][1] = 529; Phi_h_Bin_Values[13][24][2] = 9482;
z_pT_Bin_Borders[13][25][0] = 0.24; z_pT_Bin_Borders[13][25][1] = 0.2; z_pT_Bin_Borders[13][25][2] = 0.9; z_pT_Bin_Borders[13][25][3] = 0.58;
Phi_h_Bin_Values[13][25][0] =  1; Phi_h_Bin_Values[13][25][1] = 553; Phi_h_Bin_Values[13][25][2] = 9506;
z_pT_Bin_Borders[13][26][0] = 0.2; z_pT_Bin_Borders[13][26][1] = 0.16; z_pT_Bin_Borders[13][26][2] = 0.22; z_pT_Bin_Borders[13][26][3] = 0.05;
Phi_h_Bin_Values[13][26][0] =  24; Phi_h_Bin_Values[13][26][1] = 554; Phi_h_Bin_Values[13][26][2] = 9507;
z_pT_Bin_Borders[13][27][0] = 0.2; z_pT_Bin_Borders[13][27][1] = 0.16; z_pT_Bin_Borders[13][27][2] = 0.34; z_pT_Bin_Borders[13][27][3] = 0.22;
Phi_h_Bin_Values[13][27][0] =  24; Phi_h_Bin_Values[13][27][1] = 578; Phi_h_Bin_Values[13][27][2] = 9531;
z_pT_Bin_Borders[13][28][0] = 0.2; z_pT_Bin_Borders[13][28][1] = 0.16; z_pT_Bin_Borders[13][28][2] = 0.44; z_pT_Bin_Borders[13][28][3] = 0.34;
Phi_h_Bin_Values[13][28][0] =  24; Phi_h_Bin_Values[13][28][1] = 602; Phi_h_Bin_Values[13][28][2] = 9555;
z_pT_Bin_Borders[13][29][0] = 0.2; z_pT_Bin_Borders[13][29][1] = 0.16; z_pT_Bin_Borders[13][29][2] = 0.58; z_pT_Bin_Borders[13][29][3] = 0.44;
Phi_h_Bin_Values[13][29][0] =  1; Phi_h_Bin_Values[13][29][1] = 626; Phi_h_Bin_Values[13][29][2] = 9579;
z_pT_Bin_Borders[13][30][0] = 0.2; z_pT_Bin_Borders[13][30][1] = 0.16; z_pT_Bin_Borders[13][30][2] = 0.9; z_pT_Bin_Borders[13][30][3] = 0.58;
Phi_h_Bin_Values[13][30][0] =  1; Phi_h_Bin_Values[13][30][1] = 627; Phi_h_Bin_Values[13][30][2] = 9580;
z_pT_Bin_Borders[13][31][0] = 10; z_pT_Bin_Borders[13][31][1] = 0.72; z_pT_Bin_Borders[13][31][2] = 0.05; z_pT_Bin_Borders[13][31][3] = 0;
Phi_h_Bin_Values[13][31][0] =  1; Phi_h_Bin_Values[13][31][1] = 628; Phi_h_Bin_Values[13][31][2] = 9581;
z_pT_Bin_Borders[13][32][0] = 10; z_pT_Bin_Borders[13][32][1] = 0.72; z_pT_Bin_Borders[13][32][2] = 0.22; z_pT_Bin_Borders[13][32][3] = 0.05;
Phi_h_Bin_Values[13][32][0] =  1; Phi_h_Bin_Values[13][32][1] = 629; Phi_h_Bin_Values[13][32][2] = 9582;
z_pT_Bin_Borders[13][33][0] = 10; z_pT_Bin_Borders[13][33][1] = 0.72; z_pT_Bin_Borders[13][33][2] = 0.34; z_pT_Bin_Borders[13][33][3] = 0.22;
Phi_h_Bin_Values[13][33][0] =  1; Phi_h_Bin_Values[13][33][1] = 630; Phi_h_Bin_Values[13][33][2] = 9583;
z_pT_Bin_Borders[13][34][0] = 10; z_pT_Bin_Borders[13][34][1] = 0.72; z_pT_Bin_Borders[13][34][2] = 0.44; z_pT_Bin_Borders[13][34][3] = 0.34;
Phi_h_Bin_Values[13][34][0] =  1; Phi_h_Bin_Values[13][34][1] = 631; Phi_h_Bin_Values[13][34][2] = 9584;
z_pT_Bin_Borders[13][35][0] = 10; z_pT_Bin_Borders[13][35][1] = 0.72; z_pT_Bin_Borders[13][35][2] = 0.58; z_pT_Bin_Borders[13][35][3] = 0.44;
Phi_h_Bin_Values[13][35][0] =  1; Phi_h_Bin_Values[13][35][1] = 632; Phi_h_Bin_Values[13][35][2] = 9585;
z_pT_Bin_Borders[13][36][0] = 10; z_pT_Bin_Borders[13][36][1] = 0.72; z_pT_Bin_Borders[13][36][2] = 0.9; z_pT_Bin_Borders[13][36][3] = 0.58;
Phi_h_Bin_Values[13][36][0] =  1; Phi_h_Bin_Values[13][36][1] = 633; Phi_h_Bin_Values[13][36][2] = 9586;
z_pT_Bin_Borders[13][37][0] = 10; z_pT_Bin_Borders[13][37][1] = 0.72; z_pT_Bin_Borders[13][37][2] = 10; z_pT_Bin_Borders[13][37][3] = 0.9;
Phi_h_Bin_Values[13][37][0] =  1; Phi_h_Bin_Values[13][37][1] = 634; Phi_h_Bin_Values[13][37][2] = 9587;
z_pT_Bin_Borders[13][38][0] = 0.72; z_pT_Bin_Borders[13][38][1] = 0.46; z_pT_Bin_Borders[13][38][2] = 0.05; z_pT_Bin_Borders[13][38][3] = 0;
Phi_h_Bin_Values[13][38][0] =  1; Phi_h_Bin_Values[13][38][1] = 635; Phi_h_Bin_Values[13][38][2] = 9588;
z_pT_Bin_Borders[13][39][0] = 0.72; z_pT_Bin_Borders[13][39][1] = 0.46; z_pT_Bin_Borders[13][39][2] = 10; z_pT_Bin_Borders[13][39][3] = 0.9;
Phi_h_Bin_Values[13][39][0] =  1; Phi_h_Bin_Values[13][39][1] = 636; Phi_h_Bin_Values[13][39][2] = 9589;
z_pT_Bin_Borders[13][40][0] = 0.46; z_pT_Bin_Borders[13][40][1] = 0.35; z_pT_Bin_Borders[13][40][2] = 0.05; z_pT_Bin_Borders[13][40][3] = 0;
Phi_h_Bin_Values[13][40][0] =  1; Phi_h_Bin_Values[13][40][1] = 637; Phi_h_Bin_Values[13][40][2] = 9590;
z_pT_Bin_Borders[13][41][0] = 0.46; z_pT_Bin_Borders[13][41][1] = 0.35; z_pT_Bin_Borders[13][41][2] = 10; z_pT_Bin_Borders[13][41][3] = 0.9;
Phi_h_Bin_Values[13][41][0] =  1; Phi_h_Bin_Values[13][41][1] = 638; Phi_h_Bin_Values[13][41][2] = 9591;
z_pT_Bin_Borders[13][42][0] = 0.35; z_pT_Bin_Borders[13][42][1] = 0.29; z_pT_Bin_Borders[13][42][2] = 0.05; z_pT_Bin_Borders[13][42][3] = 0;
Phi_h_Bin_Values[13][42][0] =  1; Phi_h_Bin_Values[13][42][1] = 639; Phi_h_Bin_Values[13][42][2] = 9592;
z_pT_Bin_Borders[13][43][0] = 0.35; z_pT_Bin_Borders[13][43][1] = 0.29; z_pT_Bin_Borders[13][43][2] = 10; z_pT_Bin_Borders[13][43][3] = 0.9;
Phi_h_Bin_Values[13][43][0] =  1; Phi_h_Bin_Values[13][43][1] = 640; Phi_h_Bin_Values[13][43][2] = 9593;
z_pT_Bin_Borders[13][44][0] = 0.29; z_pT_Bin_Borders[13][44][1] = 0.24; z_pT_Bin_Borders[13][44][2] = 0.05; z_pT_Bin_Borders[13][44][3] = 0;
Phi_h_Bin_Values[13][44][0] =  1; Phi_h_Bin_Values[13][44][1] = 641; Phi_h_Bin_Values[13][44][2] = 9594;
z_pT_Bin_Borders[13][45][0] = 0.29; z_pT_Bin_Borders[13][45][1] = 0.24; z_pT_Bin_Borders[13][45][2] = 10; z_pT_Bin_Borders[13][45][3] = 0.9;
Phi_h_Bin_Values[13][45][0] =  1; Phi_h_Bin_Values[13][45][1] = 642; Phi_h_Bin_Values[13][45][2] = 9595;
z_pT_Bin_Borders[13][46][0] = 0.24; z_pT_Bin_Borders[13][46][1] = 0.2; z_pT_Bin_Borders[13][46][2] = 0.05; z_pT_Bin_Borders[13][46][3] = 0;
Phi_h_Bin_Values[13][46][0] =  1; Phi_h_Bin_Values[13][46][1] = 643; Phi_h_Bin_Values[13][46][2] = 9596;
z_pT_Bin_Borders[13][47][0] = 0.24; z_pT_Bin_Borders[13][47][1] = 0.2; z_pT_Bin_Borders[13][47][2] = 10; z_pT_Bin_Borders[13][47][3] = 0.9;
Phi_h_Bin_Values[13][47][0] =  1; Phi_h_Bin_Values[13][47][1] = 644; Phi_h_Bin_Values[13][47][2] = 9597;
z_pT_Bin_Borders[13][48][0] = 0.2; z_pT_Bin_Borders[13][48][1] = 0.16; z_pT_Bin_Borders[13][48][2] = 0.05; z_pT_Bin_Borders[13][48][3] = 0;
Phi_h_Bin_Values[13][48][0] =  1; Phi_h_Bin_Values[13][48][1] = 645; Phi_h_Bin_Values[13][48][2] = 9598;
z_pT_Bin_Borders[13][49][0] = 0.2; z_pT_Bin_Borders[13][49][1] = 0.16; z_pT_Bin_Borders[13][49][2] = 10; z_pT_Bin_Borders[13][49][3] = 0.9;
Phi_h_Bin_Values[13][49][0] =  1; Phi_h_Bin_Values[13][49][1] = 646; Phi_h_Bin_Values[13][49][2] = 9599;
z_pT_Bin_Borders[13][50][0] = 0.16; z_pT_Bin_Borders[13][50][1] = 0; z_pT_Bin_Borders[13][50][2] = 0.05; z_pT_Bin_Borders[13][50][3] = 0;
Phi_h_Bin_Values[13][50][0] =  1; Phi_h_Bin_Values[13][50][1] = 647; Phi_h_Bin_Values[13][50][2] = 9600;
z_pT_Bin_Borders[13][51][0] = 0.16; z_pT_Bin_Borders[13][51][1] = 0; z_pT_Bin_Borders[13][51][2] = 0.22; z_pT_Bin_Borders[13][51][3] = 0.05;
Phi_h_Bin_Values[13][51][0] =  1; Phi_h_Bin_Values[13][51][1] = 648; Phi_h_Bin_Values[13][51][2] = 9601;
z_pT_Bin_Borders[13][52][0] = 0.16; z_pT_Bin_Borders[13][52][1] = 0; z_pT_Bin_Borders[13][52][2] = 0.34; z_pT_Bin_Borders[13][52][3] = 0.22;
Phi_h_Bin_Values[13][52][0] =  1; Phi_h_Bin_Values[13][52][1] = 649; Phi_h_Bin_Values[13][52][2] = 9602;
z_pT_Bin_Borders[13][53][0] = 0.16; z_pT_Bin_Borders[13][53][1] = 0; z_pT_Bin_Borders[13][53][2] = 0.44; z_pT_Bin_Borders[13][53][3] = 0.34;
Phi_h_Bin_Values[13][53][0] =  1; Phi_h_Bin_Values[13][53][1] = 650; Phi_h_Bin_Values[13][53][2] = 9603;
z_pT_Bin_Borders[13][54][0] = 0.16; z_pT_Bin_Borders[13][54][1] = 0; z_pT_Bin_Borders[13][54][2] = 0.58; z_pT_Bin_Borders[13][54][3] = 0.44;
Phi_h_Bin_Values[13][54][0] =  1; Phi_h_Bin_Values[13][54][1] = 651; Phi_h_Bin_Values[13][54][2] = 9604;
z_pT_Bin_Borders[13][55][0] = 0.16; z_pT_Bin_Borders[13][55][1] = 0; z_pT_Bin_Borders[13][55][2] = 0.9; z_pT_Bin_Borders[13][55][3] = 0.58;
Phi_h_Bin_Values[13][55][0] =  1; Phi_h_Bin_Values[13][55][1] = 652; Phi_h_Bin_Values[13][55][2] = 9605;
z_pT_Bin_Borders[13][56][0] = 0.16; z_pT_Bin_Borders[13][56][1] = 0; z_pT_Bin_Borders[13][56][2] = 10; z_pT_Bin_Borders[13][56][3] = 0.9;
Phi_h_Bin_Values[13][56][0] =  1; Phi_h_Bin_Values[13][56][1] = 653; Phi_h_Bin_Values[13][56][2] = 9606;
z_pT_Bin_Borders[14][1][0] = 0.71; z_pT_Bin_Borders[14][1][1] = 0.5; z_pT_Bin_Borders[14][1][2] = 0.21; z_pT_Bin_Borders[14][1][3] = 0.05;
Phi_h_Bin_Values[14][1][0] =  24; Phi_h_Bin_Values[14][1][1] = 0; Phi_h_Bin_Values[14][1][2] = 9607;
z_pT_Bin_Borders[14][2][0] = 0.71; z_pT_Bin_Borders[14][2][1] = 0.5; z_pT_Bin_Borders[14][2][2] = 0.31; z_pT_Bin_Borders[14][2][3] = 0.21;
Phi_h_Bin_Values[14][2][0] =  24; Phi_h_Bin_Values[14][2][1] = 24; Phi_h_Bin_Values[14][2][2] = 9631;
z_pT_Bin_Borders[14][3][0] = 0.71; z_pT_Bin_Borders[14][3][1] = 0.5; z_pT_Bin_Borders[14][3][2] = 0.4; z_pT_Bin_Borders[14][3][3] = 0.31;
Phi_h_Bin_Values[14][3][0] =  24; Phi_h_Bin_Values[14][3][1] = 48; Phi_h_Bin_Values[14][3][2] = 9655;
z_pT_Bin_Borders[14][4][0] = 0.71; z_pT_Bin_Borders[14][4][1] = 0.5; z_pT_Bin_Borders[14][4][2] = 0.5; z_pT_Bin_Borders[14][4][3] = 0.4;
Phi_h_Bin_Values[14][4][0] =  24; Phi_h_Bin_Values[14][4][1] = 72; Phi_h_Bin_Values[14][4][2] = 9679;
z_pT_Bin_Borders[14][5][0] = 0.71; z_pT_Bin_Borders[14][5][1] = 0.5; z_pT_Bin_Borders[14][5][2] = 0.64; z_pT_Bin_Borders[14][5][3] = 0.5;
Phi_h_Bin_Values[14][5][0] =  24; Phi_h_Bin_Values[14][5][1] = 96; Phi_h_Bin_Values[14][5][2] = 9703;
z_pT_Bin_Borders[14][6][0] = 0.71; z_pT_Bin_Borders[14][6][1] = 0.5; z_pT_Bin_Borders[14][6][2] = 0.9; z_pT_Bin_Borders[14][6][3] = 0.64;
Phi_h_Bin_Values[14][6][0] =  24; Phi_h_Bin_Values[14][6][1] = 120; Phi_h_Bin_Values[14][6][2] = 9727;
z_pT_Bin_Borders[14][7][0] = 0.5; z_pT_Bin_Borders[14][7][1] = 0.39; z_pT_Bin_Borders[14][7][2] = 0.21; z_pT_Bin_Borders[14][7][3] = 0.05;
Phi_h_Bin_Values[14][7][0] =  24; Phi_h_Bin_Values[14][7][1] = 144; Phi_h_Bin_Values[14][7][2] = 9751;
z_pT_Bin_Borders[14][8][0] = 0.5; z_pT_Bin_Borders[14][8][1] = 0.39; z_pT_Bin_Borders[14][8][2] = 0.31; z_pT_Bin_Borders[14][8][3] = 0.21;
Phi_h_Bin_Values[14][8][0] =  24; Phi_h_Bin_Values[14][8][1] = 168; Phi_h_Bin_Values[14][8][2] = 9775;
z_pT_Bin_Borders[14][9][0] = 0.5; z_pT_Bin_Borders[14][9][1] = 0.39; z_pT_Bin_Borders[14][9][2] = 0.4; z_pT_Bin_Borders[14][9][3] = 0.31;
Phi_h_Bin_Values[14][9][0] =  24; Phi_h_Bin_Values[14][9][1] = 192; Phi_h_Bin_Values[14][9][2] = 9799;
z_pT_Bin_Borders[14][10][0] = 0.5; z_pT_Bin_Borders[14][10][1] = 0.39; z_pT_Bin_Borders[14][10][2] = 0.5; z_pT_Bin_Borders[14][10][3] = 0.4;
Phi_h_Bin_Values[14][10][0] =  24; Phi_h_Bin_Values[14][10][1] = 216; Phi_h_Bin_Values[14][10][2] = 9823;
z_pT_Bin_Borders[14][11][0] = 0.5; z_pT_Bin_Borders[14][11][1] = 0.39; z_pT_Bin_Borders[14][11][2] = 0.64; z_pT_Bin_Borders[14][11][3] = 0.5;
Phi_h_Bin_Values[14][11][0] =  24; Phi_h_Bin_Values[14][11][1] = 240; Phi_h_Bin_Values[14][11][2] = 9847;
z_pT_Bin_Borders[14][12][0] = 0.5; z_pT_Bin_Borders[14][12][1] = 0.39; z_pT_Bin_Borders[14][12][2] = 0.9; z_pT_Bin_Borders[14][12][3] = 0.64;
Phi_h_Bin_Values[14][12][0] =  24; Phi_h_Bin_Values[14][12][1] = 264; Phi_h_Bin_Values[14][12][2] = 9871;
z_pT_Bin_Borders[14][13][0] = 0.39; z_pT_Bin_Borders[14][13][1] = 0.32; z_pT_Bin_Borders[14][13][2] = 0.21; z_pT_Bin_Borders[14][13][3] = 0.05;
Phi_h_Bin_Values[14][13][0] =  24; Phi_h_Bin_Values[14][13][1] = 288; Phi_h_Bin_Values[14][13][2] = 9895;
z_pT_Bin_Borders[14][14][0] = 0.39; z_pT_Bin_Borders[14][14][1] = 0.32; z_pT_Bin_Borders[14][14][2] = 0.31; z_pT_Bin_Borders[14][14][3] = 0.21;
Phi_h_Bin_Values[14][14][0] =  24; Phi_h_Bin_Values[14][14][1] = 312; Phi_h_Bin_Values[14][14][2] = 9919;
z_pT_Bin_Borders[14][15][0] = 0.39; z_pT_Bin_Borders[14][15][1] = 0.32; z_pT_Bin_Borders[14][15][2] = 0.4; z_pT_Bin_Borders[14][15][3] = 0.31;
Phi_h_Bin_Values[14][15][0] =  24; Phi_h_Bin_Values[14][15][1] = 336; Phi_h_Bin_Values[14][15][2] = 9943;
z_pT_Bin_Borders[14][16][0] = 0.39; z_pT_Bin_Borders[14][16][1] = 0.32; z_pT_Bin_Borders[14][16][2] = 0.5; z_pT_Bin_Borders[14][16][3] = 0.4;
Phi_h_Bin_Values[14][16][0] =  24; Phi_h_Bin_Values[14][16][1] = 360; Phi_h_Bin_Values[14][16][2] = 9967;
z_pT_Bin_Borders[14][17][0] = 0.39; z_pT_Bin_Borders[14][17][1] = 0.32; z_pT_Bin_Borders[14][17][2] = 0.64; z_pT_Bin_Borders[14][17][3] = 0.5;
Phi_h_Bin_Values[14][17][0] =  24; Phi_h_Bin_Values[14][17][1] = 384; Phi_h_Bin_Values[14][17][2] = 9991;
z_pT_Bin_Borders[14][18][0] = 0.39; z_pT_Bin_Borders[14][18][1] = 0.32; z_pT_Bin_Borders[14][18][2] = 0.9; z_pT_Bin_Borders[14][18][3] = 0.64;
Phi_h_Bin_Values[14][18][0] =  24; Phi_h_Bin_Values[14][18][1] = 408; Phi_h_Bin_Values[14][18][2] = 10015;
z_pT_Bin_Borders[14][19][0] = 0.32; z_pT_Bin_Borders[14][19][1] = 0.27; z_pT_Bin_Borders[14][19][2] = 0.21; z_pT_Bin_Borders[14][19][3] = 0.05;
Phi_h_Bin_Values[14][19][0] =  24; Phi_h_Bin_Values[14][19][1] = 432; Phi_h_Bin_Values[14][19][2] = 10039;
z_pT_Bin_Borders[14][20][0] = 0.32; z_pT_Bin_Borders[14][20][1] = 0.27; z_pT_Bin_Borders[14][20][2] = 0.31; z_pT_Bin_Borders[14][20][3] = 0.21;
Phi_h_Bin_Values[14][20][0] =  24; Phi_h_Bin_Values[14][20][1] = 456; Phi_h_Bin_Values[14][20][2] = 10063;
z_pT_Bin_Borders[14][21][0] = 0.32; z_pT_Bin_Borders[14][21][1] = 0.27; z_pT_Bin_Borders[14][21][2] = 0.4; z_pT_Bin_Borders[14][21][3] = 0.31;
Phi_h_Bin_Values[14][21][0] =  24; Phi_h_Bin_Values[14][21][1] = 480; Phi_h_Bin_Values[14][21][2] = 10087;
z_pT_Bin_Borders[14][22][0] = 0.32; z_pT_Bin_Borders[14][22][1] = 0.27; z_pT_Bin_Borders[14][22][2] = 0.5; z_pT_Bin_Borders[14][22][3] = 0.4;
Phi_h_Bin_Values[14][22][0] =  24; Phi_h_Bin_Values[14][22][1] = 504; Phi_h_Bin_Values[14][22][2] = 10111;
z_pT_Bin_Borders[14][23][0] = 0.32; z_pT_Bin_Borders[14][23][1] = 0.27; z_pT_Bin_Borders[14][23][2] = 0.64; z_pT_Bin_Borders[14][23][3] = 0.5;
Phi_h_Bin_Values[14][23][0] =  24; Phi_h_Bin_Values[14][23][1] = 528; Phi_h_Bin_Values[14][23][2] = 10135;
z_pT_Bin_Borders[14][24][0] = 0.32; z_pT_Bin_Borders[14][24][1] = 0.27; z_pT_Bin_Borders[14][24][2] = 0.9; z_pT_Bin_Borders[14][24][3] = 0.64;
Phi_h_Bin_Values[14][24][0] =  1; Phi_h_Bin_Values[14][24][1] = 552; Phi_h_Bin_Values[14][24][2] = 10159;
z_pT_Bin_Borders[14][25][0] = 0.27; z_pT_Bin_Borders[14][25][1] = 0.23; z_pT_Bin_Borders[14][25][2] = 0.21; z_pT_Bin_Borders[14][25][3] = 0.05;
Phi_h_Bin_Values[14][25][0] =  24; Phi_h_Bin_Values[14][25][1] = 553; Phi_h_Bin_Values[14][25][2] = 10160;
z_pT_Bin_Borders[14][26][0] = 0.27; z_pT_Bin_Borders[14][26][1] = 0.23; z_pT_Bin_Borders[14][26][2] = 0.31; z_pT_Bin_Borders[14][26][3] = 0.21;
Phi_h_Bin_Values[14][26][0] =  24; Phi_h_Bin_Values[14][26][1] = 577; Phi_h_Bin_Values[14][26][2] = 10184;
z_pT_Bin_Borders[14][27][0] = 0.27; z_pT_Bin_Borders[14][27][1] = 0.23; z_pT_Bin_Borders[14][27][2] = 0.4; z_pT_Bin_Borders[14][27][3] = 0.31;
Phi_h_Bin_Values[14][27][0] =  24; Phi_h_Bin_Values[14][27][1] = 601; Phi_h_Bin_Values[14][27][2] = 10208;
z_pT_Bin_Borders[14][28][0] = 0.27; z_pT_Bin_Borders[14][28][1] = 0.23; z_pT_Bin_Borders[14][28][2] = 0.5; z_pT_Bin_Borders[14][28][3] = 0.4;
Phi_h_Bin_Values[14][28][0] =  24; Phi_h_Bin_Values[14][28][1] = 625; Phi_h_Bin_Values[14][28][2] = 10232;
z_pT_Bin_Borders[14][29][0] = 0.27; z_pT_Bin_Borders[14][29][1] = 0.23; z_pT_Bin_Borders[14][29][2] = 0.64; z_pT_Bin_Borders[14][29][3] = 0.5;
Phi_h_Bin_Values[14][29][0] =  24; Phi_h_Bin_Values[14][29][1] = 649; Phi_h_Bin_Values[14][29][2] = 10256;
z_pT_Bin_Borders[14][30][0] = 0.27; z_pT_Bin_Borders[14][30][1] = 0.23; z_pT_Bin_Borders[14][30][2] = 0.9; z_pT_Bin_Borders[14][30][3] = 0.64;
Phi_h_Bin_Values[14][30][0] =  1; Phi_h_Bin_Values[14][30][1] = 673; Phi_h_Bin_Values[14][30][2] = 10280;
z_pT_Bin_Borders[14][31][0] = 0.23; z_pT_Bin_Borders[14][31][1] = 0.19; z_pT_Bin_Borders[14][31][2] = 0.21; z_pT_Bin_Borders[14][31][3] = 0.05;
Phi_h_Bin_Values[14][31][0] =  24; Phi_h_Bin_Values[14][31][1] = 674; Phi_h_Bin_Values[14][31][2] = 10281;
z_pT_Bin_Borders[14][32][0] = 0.23; z_pT_Bin_Borders[14][32][1] = 0.19; z_pT_Bin_Borders[14][32][2] = 0.31; z_pT_Bin_Borders[14][32][3] = 0.21;
Phi_h_Bin_Values[14][32][0] =  24; Phi_h_Bin_Values[14][32][1] = 698; Phi_h_Bin_Values[14][32][2] = 10305;
z_pT_Bin_Borders[14][33][0] = 0.23; z_pT_Bin_Borders[14][33][1] = 0.19; z_pT_Bin_Borders[14][33][2] = 0.4; z_pT_Bin_Borders[14][33][3] = 0.31;
Phi_h_Bin_Values[14][33][0] =  24; Phi_h_Bin_Values[14][33][1] = 722; Phi_h_Bin_Values[14][33][2] = 10329;
z_pT_Bin_Borders[14][34][0] = 0.23; z_pT_Bin_Borders[14][34][1] = 0.19; z_pT_Bin_Borders[14][34][2] = 0.5; z_pT_Bin_Borders[14][34][3] = 0.4;
Phi_h_Bin_Values[14][34][0] =  24; Phi_h_Bin_Values[14][34][1] = 746; Phi_h_Bin_Values[14][34][2] = 10353;
z_pT_Bin_Borders[14][35][0] = 0.23; z_pT_Bin_Borders[14][35][1] = 0.19; z_pT_Bin_Borders[14][35][2] = 0.64; z_pT_Bin_Borders[14][35][3] = 0.5;
Phi_h_Bin_Values[14][35][0] =  1; Phi_h_Bin_Values[14][35][1] = 770; Phi_h_Bin_Values[14][35][2] = 10377;
z_pT_Bin_Borders[14][36][0] = 0.23; z_pT_Bin_Borders[14][36][1] = 0.19; z_pT_Bin_Borders[14][36][2] = 0.9; z_pT_Bin_Borders[14][36][3] = 0.64;
Phi_h_Bin_Values[14][36][0] =  1; Phi_h_Bin_Values[14][36][1] = 771; Phi_h_Bin_Values[14][36][2] = 10378;
z_pT_Bin_Borders[14][37][0] = 10; z_pT_Bin_Borders[14][37][1] = 0.71; z_pT_Bin_Borders[14][37][2] = 0.05; z_pT_Bin_Borders[14][37][3] = 0;
Phi_h_Bin_Values[14][37][0] =  1; Phi_h_Bin_Values[14][37][1] = 772; Phi_h_Bin_Values[14][37][2] = 10379;
z_pT_Bin_Borders[14][38][0] = 10; z_pT_Bin_Borders[14][38][1] = 0.71; z_pT_Bin_Borders[14][38][2] = 0.21; z_pT_Bin_Borders[14][38][3] = 0.05;
Phi_h_Bin_Values[14][38][0] =  1; Phi_h_Bin_Values[14][38][1] = 773; Phi_h_Bin_Values[14][38][2] = 10380;
z_pT_Bin_Borders[14][39][0] = 10; z_pT_Bin_Borders[14][39][1] = 0.71; z_pT_Bin_Borders[14][39][2] = 0.31; z_pT_Bin_Borders[14][39][3] = 0.21;
Phi_h_Bin_Values[14][39][0] =  1; Phi_h_Bin_Values[14][39][1] = 774; Phi_h_Bin_Values[14][39][2] = 10381;
z_pT_Bin_Borders[14][40][0] = 10; z_pT_Bin_Borders[14][40][1] = 0.71; z_pT_Bin_Borders[14][40][2] = 0.4; z_pT_Bin_Borders[14][40][3] = 0.31;
Phi_h_Bin_Values[14][40][0] =  1; Phi_h_Bin_Values[14][40][1] = 775; Phi_h_Bin_Values[14][40][2] = 10382;
z_pT_Bin_Borders[14][41][0] = 10; z_pT_Bin_Borders[14][41][1] = 0.71; z_pT_Bin_Borders[14][41][2] = 0.5; z_pT_Bin_Borders[14][41][3] = 0.4;
Phi_h_Bin_Values[14][41][0] =  1; Phi_h_Bin_Values[14][41][1] = 776; Phi_h_Bin_Values[14][41][2] = 10383;
z_pT_Bin_Borders[14][42][0] = 10; z_pT_Bin_Borders[14][42][1] = 0.71; z_pT_Bin_Borders[14][42][2] = 0.64; z_pT_Bin_Borders[14][42][3] = 0.5;
Phi_h_Bin_Values[14][42][0] =  1; Phi_h_Bin_Values[14][42][1] = 777; Phi_h_Bin_Values[14][42][2] = 10384;
z_pT_Bin_Borders[14][43][0] = 10; z_pT_Bin_Borders[14][43][1] = 0.71; z_pT_Bin_Borders[14][43][2] = 0.9; z_pT_Bin_Borders[14][43][3] = 0.64;
Phi_h_Bin_Values[14][43][0] =  1; Phi_h_Bin_Values[14][43][1] = 778; Phi_h_Bin_Values[14][43][2] = 10385;
z_pT_Bin_Borders[14][44][0] = 10; z_pT_Bin_Borders[14][44][1] = 0.71; z_pT_Bin_Borders[14][44][2] = 10; z_pT_Bin_Borders[14][44][3] = 0.9;
Phi_h_Bin_Values[14][44][0] =  1; Phi_h_Bin_Values[14][44][1] = 779; Phi_h_Bin_Values[14][44][2] = 10386;
z_pT_Bin_Borders[14][45][0] = 0.71; z_pT_Bin_Borders[14][45][1] = 0.5; z_pT_Bin_Borders[14][45][2] = 0.05; z_pT_Bin_Borders[14][45][3] = 0;
Phi_h_Bin_Values[14][45][0] =  1; Phi_h_Bin_Values[14][45][1] = 780; Phi_h_Bin_Values[14][45][2] = 10387;
z_pT_Bin_Borders[14][46][0] = 0.71; z_pT_Bin_Borders[14][46][1] = 0.5; z_pT_Bin_Borders[14][46][2] = 10; z_pT_Bin_Borders[14][46][3] = 0.9;
Phi_h_Bin_Values[14][46][0] =  1; Phi_h_Bin_Values[14][46][1] = 781; Phi_h_Bin_Values[14][46][2] = 10388;
z_pT_Bin_Borders[14][47][0] = 0.5; z_pT_Bin_Borders[14][47][1] = 0.39; z_pT_Bin_Borders[14][47][2] = 0.05; z_pT_Bin_Borders[14][47][3] = 0;
Phi_h_Bin_Values[14][47][0] =  1; Phi_h_Bin_Values[14][47][1] = 782; Phi_h_Bin_Values[14][47][2] = 10389;
z_pT_Bin_Borders[14][48][0] = 0.5; z_pT_Bin_Borders[14][48][1] = 0.39; z_pT_Bin_Borders[14][48][2] = 10; z_pT_Bin_Borders[14][48][3] = 0.9;
Phi_h_Bin_Values[14][48][0] =  1; Phi_h_Bin_Values[14][48][1] = 783; Phi_h_Bin_Values[14][48][2] = 10390;
z_pT_Bin_Borders[14][49][0] = 0.39; z_pT_Bin_Borders[14][49][1] = 0.32; z_pT_Bin_Borders[14][49][2] = 0.05; z_pT_Bin_Borders[14][49][3] = 0;
Phi_h_Bin_Values[14][49][0] =  1; Phi_h_Bin_Values[14][49][1] = 784; Phi_h_Bin_Values[14][49][2] = 10391;
z_pT_Bin_Borders[14][50][0] = 0.39; z_pT_Bin_Borders[14][50][1] = 0.32; z_pT_Bin_Borders[14][50][2] = 10; z_pT_Bin_Borders[14][50][3] = 0.9;
Phi_h_Bin_Values[14][50][0] =  1; Phi_h_Bin_Values[14][50][1] = 785; Phi_h_Bin_Values[14][50][2] = 10392;
z_pT_Bin_Borders[14][51][0] = 0.32; z_pT_Bin_Borders[14][51][1] = 0.27; z_pT_Bin_Borders[14][51][2] = 0.05; z_pT_Bin_Borders[14][51][3] = 0;
Phi_h_Bin_Values[14][51][0] =  1; Phi_h_Bin_Values[14][51][1] = 786; Phi_h_Bin_Values[14][51][2] = 10393;
z_pT_Bin_Borders[14][52][0] = 0.32; z_pT_Bin_Borders[14][52][1] = 0.27; z_pT_Bin_Borders[14][52][2] = 10; z_pT_Bin_Borders[14][52][3] = 0.9;
Phi_h_Bin_Values[14][52][0] =  1; Phi_h_Bin_Values[14][52][1] = 787; Phi_h_Bin_Values[14][52][2] = 10394;
z_pT_Bin_Borders[14][53][0] = 0.27; z_pT_Bin_Borders[14][53][1] = 0.23; z_pT_Bin_Borders[14][53][2] = 0.05; z_pT_Bin_Borders[14][53][3] = 0;
Phi_h_Bin_Values[14][53][0] =  1; Phi_h_Bin_Values[14][53][1] = 788; Phi_h_Bin_Values[14][53][2] = 10395;
z_pT_Bin_Borders[14][54][0] = 0.27; z_pT_Bin_Borders[14][54][1] = 0.23; z_pT_Bin_Borders[14][54][2] = 10; z_pT_Bin_Borders[14][54][3] = 0.9;
Phi_h_Bin_Values[14][54][0] =  1; Phi_h_Bin_Values[14][54][1] = 789; Phi_h_Bin_Values[14][54][2] = 10396;
z_pT_Bin_Borders[14][55][0] = 0.23; z_pT_Bin_Borders[14][55][1] = 0.19; z_pT_Bin_Borders[14][55][2] = 0.05; z_pT_Bin_Borders[14][55][3] = 0;
Phi_h_Bin_Values[14][55][0] =  1; Phi_h_Bin_Values[14][55][1] = 790; Phi_h_Bin_Values[14][55][2] = 10397;
z_pT_Bin_Borders[14][56][0] = 0.23; z_pT_Bin_Borders[14][56][1] = 0.19; z_pT_Bin_Borders[14][56][2] = 10; z_pT_Bin_Borders[14][56][3] = 0.9;
Phi_h_Bin_Values[14][56][0] =  1; Phi_h_Bin_Values[14][56][1] = 791; Phi_h_Bin_Values[14][56][2] = 10398;
z_pT_Bin_Borders[14][57][0] = 0.19; z_pT_Bin_Borders[14][57][1] = 0; z_pT_Bin_Borders[14][57][2] = 0.05; z_pT_Bin_Borders[14][57][3] = 0;
Phi_h_Bin_Values[14][57][0] =  1; Phi_h_Bin_Values[14][57][1] = 792; Phi_h_Bin_Values[14][57][2] = 10399;
z_pT_Bin_Borders[14][58][0] = 0.19; z_pT_Bin_Borders[14][58][1] = 0; z_pT_Bin_Borders[14][58][2] = 0.21; z_pT_Bin_Borders[14][58][3] = 0.05;
Phi_h_Bin_Values[14][58][0] =  1; Phi_h_Bin_Values[14][58][1] = 793; Phi_h_Bin_Values[14][58][2] = 10400;
z_pT_Bin_Borders[14][59][0] = 0.19; z_pT_Bin_Borders[14][59][1] = 0; z_pT_Bin_Borders[14][59][2] = 0.31; z_pT_Bin_Borders[14][59][3] = 0.21;
Phi_h_Bin_Values[14][59][0] =  1; Phi_h_Bin_Values[14][59][1] = 794; Phi_h_Bin_Values[14][59][2] = 10401;
z_pT_Bin_Borders[14][60][0] = 0.19; z_pT_Bin_Borders[14][60][1] = 0; z_pT_Bin_Borders[14][60][2] = 0.4; z_pT_Bin_Borders[14][60][3] = 0.31;
Phi_h_Bin_Values[14][60][0] =  1; Phi_h_Bin_Values[14][60][1] = 795; Phi_h_Bin_Values[14][60][2] = 10402;
z_pT_Bin_Borders[14][61][0] = 0.19; z_pT_Bin_Borders[14][61][1] = 0; z_pT_Bin_Borders[14][61][2] = 0.5; z_pT_Bin_Borders[14][61][3] = 0.4;
Phi_h_Bin_Values[14][61][0] =  1; Phi_h_Bin_Values[14][61][1] = 796; Phi_h_Bin_Values[14][61][2] = 10403;
z_pT_Bin_Borders[14][62][0] = 0.19; z_pT_Bin_Borders[14][62][1] = 0; z_pT_Bin_Borders[14][62][2] = 0.64; z_pT_Bin_Borders[14][62][3] = 0.5;
Phi_h_Bin_Values[14][62][0] =  1; Phi_h_Bin_Values[14][62][1] = 797; Phi_h_Bin_Values[14][62][2] = 10404;
z_pT_Bin_Borders[14][63][0] = 0.19; z_pT_Bin_Borders[14][63][1] = 0; z_pT_Bin_Borders[14][63][2] = 0.9; z_pT_Bin_Borders[14][63][3] = 0.64;
Phi_h_Bin_Values[14][63][0] =  1; Phi_h_Bin_Values[14][63][1] = 798; Phi_h_Bin_Values[14][63][2] = 10405;
z_pT_Bin_Borders[14][64][0] = 0.19; z_pT_Bin_Borders[14][64][1] = 0; z_pT_Bin_Borders[14][64][2] = 10; z_pT_Bin_Borders[14][64][3] = 0.9;
Phi_h_Bin_Values[14][64][0] =  1; Phi_h_Bin_Values[14][64][1] = 799; Phi_h_Bin_Values[14][64][2] = 10406;
z_pT_Bin_Borders[15][1][0] = 0.73; z_pT_Bin_Borders[15][1][1] = 0.49; z_pT_Bin_Borders[15][1][2] = 0.22; z_pT_Bin_Borders[15][1][3] = 0.05;
Phi_h_Bin_Values[15][1][0] =  24; Phi_h_Bin_Values[15][1][1] = 0; Phi_h_Bin_Values[15][1][2] = 10407;
z_pT_Bin_Borders[15][2][0] = 0.73; z_pT_Bin_Borders[15][2][1] = 0.49; z_pT_Bin_Borders[15][2][2] = 0.32; z_pT_Bin_Borders[15][2][3] = 0.22;
Phi_h_Bin_Values[15][2][0] =  24; Phi_h_Bin_Values[15][2][1] = 24; Phi_h_Bin_Values[15][2][2] = 10431;
z_pT_Bin_Borders[15][3][0] = 0.73; z_pT_Bin_Borders[15][3][1] = 0.49; z_pT_Bin_Borders[15][3][2] = 0.42; z_pT_Bin_Borders[15][3][3] = 0.32;
Phi_h_Bin_Values[15][3][0] =  24; Phi_h_Bin_Values[15][3][1] = 48; Phi_h_Bin_Values[15][3][2] = 10455;
z_pT_Bin_Borders[15][4][0] = 0.73; z_pT_Bin_Borders[15][4][1] = 0.49; z_pT_Bin_Borders[15][4][2] = 0.55; z_pT_Bin_Borders[15][4][3] = 0.42;
Phi_h_Bin_Values[15][4][0] =  24; Phi_h_Bin_Values[15][4][1] = 72; Phi_h_Bin_Values[15][4][2] = 10479;
z_pT_Bin_Borders[15][5][0] = 0.73; z_pT_Bin_Borders[15][5][1] = 0.49; z_pT_Bin_Borders[15][5][2] = 0.8; z_pT_Bin_Borders[15][5][3] = 0.55;
Phi_h_Bin_Values[15][5][0] =  1; Phi_h_Bin_Values[15][5][1] = 96; Phi_h_Bin_Values[15][5][2] = 10503;
z_pT_Bin_Borders[15][6][0] = 0.49; z_pT_Bin_Borders[15][6][1] = 0.4; z_pT_Bin_Borders[15][6][2] = 0.22; z_pT_Bin_Borders[15][6][3] = 0.05;
Phi_h_Bin_Values[15][6][0] =  24; Phi_h_Bin_Values[15][6][1] = 97; Phi_h_Bin_Values[15][6][2] = 10504;
z_pT_Bin_Borders[15][7][0] = 0.49; z_pT_Bin_Borders[15][7][1] = 0.4; z_pT_Bin_Borders[15][7][2] = 0.32; z_pT_Bin_Borders[15][7][3] = 0.22;
Phi_h_Bin_Values[15][7][0] =  24; Phi_h_Bin_Values[15][7][1] = 121; Phi_h_Bin_Values[15][7][2] = 10528;
z_pT_Bin_Borders[15][8][0] = 0.49; z_pT_Bin_Borders[15][8][1] = 0.4; z_pT_Bin_Borders[15][8][2] = 0.42; z_pT_Bin_Borders[15][8][3] = 0.32;
Phi_h_Bin_Values[15][8][0] =  24; Phi_h_Bin_Values[15][8][1] = 145; Phi_h_Bin_Values[15][8][2] = 10552;
z_pT_Bin_Borders[15][9][0] = 0.49; z_pT_Bin_Borders[15][9][1] = 0.4; z_pT_Bin_Borders[15][9][2] = 0.55; z_pT_Bin_Borders[15][9][3] = 0.42;
Phi_h_Bin_Values[15][9][0] =  24; Phi_h_Bin_Values[15][9][1] = 169; Phi_h_Bin_Values[15][9][2] = 10576;
z_pT_Bin_Borders[15][10][0] = 0.49; z_pT_Bin_Borders[15][10][1] = 0.4; z_pT_Bin_Borders[15][10][2] = 0.8; z_pT_Bin_Borders[15][10][3] = 0.55;
Phi_h_Bin_Values[15][10][0] =  24; Phi_h_Bin_Values[15][10][1] = 193; Phi_h_Bin_Values[15][10][2] = 10600;
z_pT_Bin_Borders[15][11][0] = 0.4; z_pT_Bin_Borders[15][11][1] = 0.32; z_pT_Bin_Borders[15][11][2] = 0.22; z_pT_Bin_Borders[15][11][3] = 0.05;
Phi_h_Bin_Values[15][11][0] =  24; Phi_h_Bin_Values[15][11][1] = 217; Phi_h_Bin_Values[15][11][2] = 10624;
z_pT_Bin_Borders[15][12][0] = 0.4; z_pT_Bin_Borders[15][12][1] = 0.32; z_pT_Bin_Borders[15][12][2] = 0.32; z_pT_Bin_Borders[15][12][3] = 0.22;
Phi_h_Bin_Values[15][12][0] =  24; Phi_h_Bin_Values[15][12][1] = 241; Phi_h_Bin_Values[15][12][2] = 10648;
z_pT_Bin_Borders[15][13][0] = 0.4; z_pT_Bin_Borders[15][13][1] = 0.32; z_pT_Bin_Borders[15][13][2] = 0.42; z_pT_Bin_Borders[15][13][3] = 0.32;
Phi_h_Bin_Values[15][13][0] =  24; Phi_h_Bin_Values[15][13][1] = 265; Phi_h_Bin_Values[15][13][2] = 10672;
z_pT_Bin_Borders[15][14][0] = 0.4; z_pT_Bin_Borders[15][14][1] = 0.32; z_pT_Bin_Borders[15][14][2] = 0.55; z_pT_Bin_Borders[15][14][3] = 0.42;
Phi_h_Bin_Values[15][14][0] =  24; Phi_h_Bin_Values[15][14][1] = 289; Phi_h_Bin_Values[15][14][2] = 10696;
z_pT_Bin_Borders[15][15][0] = 0.4; z_pT_Bin_Borders[15][15][1] = 0.32; z_pT_Bin_Borders[15][15][2] = 0.8; z_pT_Bin_Borders[15][15][3] = 0.55;
Phi_h_Bin_Values[15][15][0] =  24; Phi_h_Bin_Values[15][15][1] = 313; Phi_h_Bin_Values[15][15][2] = 10720;
z_pT_Bin_Borders[15][16][0] = 0.32; z_pT_Bin_Borders[15][16][1] = 0.27; z_pT_Bin_Borders[15][16][2] = 0.22; z_pT_Bin_Borders[15][16][3] = 0.05;
Phi_h_Bin_Values[15][16][0] =  24; Phi_h_Bin_Values[15][16][1] = 337; Phi_h_Bin_Values[15][16][2] = 10744;
z_pT_Bin_Borders[15][17][0] = 0.32; z_pT_Bin_Borders[15][17][1] = 0.27; z_pT_Bin_Borders[15][17][2] = 0.32; z_pT_Bin_Borders[15][17][3] = 0.22;
Phi_h_Bin_Values[15][17][0] =  24; Phi_h_Bin_Values[15][17][1] = 361; Phi_h_Bin_Values[15][17][2] = 10768;
z_pT_Bin_Borders[15][18][0] = 0.32; z_pT_Bin_Borders[15][18][1] = 0.27; z_pT_Bin_Borders[15][18][2] = 0.42; z_pT_Bin_Borders[15][18][3] = 0.32;
Phi_h_Bin_Values[15][18][0] =  24; Phi_h_Bin_Values[15][18][1] = 385; Phi_h_Bin_Values[15][18][2] = 10792;
z_pT_Bin_Borders[15][19][0] = 0.32; z_pT_Bin_Borders[15][19][1] = 0.27; z_pT_Bin_Borders[15][19][2] = 0.55; z_pT_Bin_Borders[15][19][3] = 0.42;
Phi_h_Bin_Values[15][19][0] =  24; Phi_h_Bin_Values[15][19][1] = 409; Phi_h_Bin_Values[15][19][2] = 10816;
z_pT_Bin_Borders[15][20][0] = 0.32; z_pT_Bin_Borders[15][20][1] = 0.27; z_pT_Bin_Borders[15][20][2] = 0.8; z_pT_Bin_Borders[15][20][3] = 0.55;
Phi_h_Bin_Values[15][20][0] =  1; Phi_h_Bin_Values[15][20][1] = 433; Phi_h_Bin_Values[15][20][2] = 10840;
z_pT_Bin_Borders[15][21][0] = 0.27; z_pT_Bin_Borders[15][21][1] = 0.22; z_pT_Bin_Borders[15][21][2] = 0.22; z_pT_Bin_Borders[15][21][3] = 0.05;
Phi_h_Bin_Values[15][21][0] =  24; Phi_h_Bin_Values[15][21][1] = 434; Phi_h_Bin_Values[15][21][2] = 10841;
z_pT_Bin_Borders[15][22][0] = 0.27; z_pT_Bin_Borders[15][22][1] = 0.22; z_pT_Bin_Borders[15][22][2] = 0.32; z_pT_Bin_Borders[15][22][3] = 0.22;
Phi_h_Bin_Values[15][22][0] =  24; Phi_h_Bin_Values[15][22][1] = 458; Phi_h_Bin_Values[15][22][2] = 10865;
z_pT_Bin_Borders[15][23][0] = 0.27; z_pT_Bin_Borders[15][23][1] = 0.22; z_pT_Bin_Borders[15][23][2] = 0.42; z_pT_Bin_Borders[15][23][3] = 0.32;
Phi_h_Bin_Values[15][23][0] =  24; Phi_h_Bin_Values[15][23][1] = 482; Phi_h_Bin_Values[15][23][2] = 10889;
z_pT_Bin_Borders[15][24][0] = 0.27; z_pT_Bin_Borders[15][24][1] = 0.22; z_pT_Bin_Borders[15][24][2] = 0.55; z_pT_Bin_Borders[15][24][3] = 0.42;
Phi_h_Bin_Values[15][24][0] =  24; Phi_h_Bin_Values[15][24][1] = 506; Phi_h_Bin_Values[15][24][2] = 10913;
z_pT_Bin_Borders[15][25][0] = 0.27; z_pT_Bin_Borders[15][25][1] = 0.22; z_pT_Bin_Borders[15][25][2] = 0.8; z_pT_Bin_Borders[15][25][3] = 0.55;
Phi_h_Bin_Values[15][25][0] =  1; Phi_h_Bin_Values[15][25][1] = 530; Phi_h_Bin_Values[15][25][2] = 10937;
z_pT_Bin_Borders[15][26][0] = 10; z_pT_Bin_Borders[15][26][1] = 0.73; z_pT_Bin_Borders[15][26][2] = 0.05; z_pT_Bin_Borders[15][26][3] = 0;
Phi_h_Bin_Values[15][26][0] =  1; Phi_h_Bin_Values[15][26][1] = 531; Phi_h_Bin_Values[15][26][2] = 10938;
z_pT_Bin_Borders[15][27][0] = 10; z_pT_Bin_Borders[15][27][1] = 0.73; z_pT_Bin_Borders[15][27][2] = 0.22; z_pT_Bin_Borders[15][27][3] = 0.05;
Phi_h_Bin_Values[15][27][0] =  1; Phi_h_Bin_Values[15][27][1] = 532; Phi_h_Bin_Values[15][27][2] = 10939;
z_pT_Bin_Borders[15][28][0] = 10; z_pT_Bin_Borders[15][28][1] = 0.73; z_pT_Bin_Borders[15][28][2] = 0.32; z_pT_Bin_Borders[15][28][3] = 0.22;
Phi_h_Bin_Values[15][28][0] =  1; Phi_h_Bin_Values[15][28][1] = 533; Phi_h_Bin_Values[15][28][2] = 10940;
z_pT_Bin_Borders[15][29][0] = 10; z_pT_Bin_Borders[15][29][1] = 0.73; z_pT_Bin_Borders[15][29][2] = 0.42; z_pT_Bin_Borders[15][29][3] = 0.32;
Phi_h_Bin_Values[15][29][0] =  1; Phi_h_Bin_Values[15][29][1] = 534; Phi_h_Bin_Values[15][29][2] = 10941;
z_pT_Bin_Borders[15][30][0] = 10; z_pT_Bin_Borders[15][30][1] = 0.73; z_pT_Bin_Borders[15][30][2] = 0.55; z_pT_Bin_Borders[15][30][3] = 0.42;
Phi_h_Bin_Values[15][30][0] =  1; Phi_h_Bin_Values[15][30][1] = 535; Phi_h_Bin_Values[15][30][2] = 10942;
z_pT_Bin_Borders[15][31][0] = 10; z_pT_Bin_Borders[15][31][1] = 0.73; z_pT_Bin_Borders[15][31][2] = 0.8; z_pT_Bin_Borders[15][31][3] = 0.55;
Phi_h_Bin_Values[15][31][0] =  1; Phi_h_Bin_Values[15][31][1] = 536; Phi_h_Bin_Values[15][31][2] = 10943;
z_pT_Bin_Borders[15][32][0] = 10; z_pT_Bin_Borders[15][32][1] = 0.73; z_pT_Bin_Borders[15][32][2] = 10; z_pT_Bin_Borders[15][32][3] = 0.8;
Phi_h_Bin_Values[15][32][0] =  1; Phi_h_Bin_Values[15][32][1] = 537; Phi_h_Bin_Values[15][32][2] = 10944;
z_pT_Bin_Borders[15][33][0] = 0.73; z_pT_Bin_Borders[15][33][1] = 0.49; z_pT_Bin_Borders[15][33][2] = 0.05; z_pT_Bin_Borders[15][33][3] = 0;
Phi_h_Bin_Values[15][33][0] =  1; Phi_h_Bin_Values[15][33][1] = 538; Phi_h_Bin_Values[15][33][2] = 10945;
z_pT_Bin_Borders[15][34][0] = 0.73; z_pT_Bin_Borders[15][34][1] = 0.49; z_pT_Bin_Borders[15][34][2] = 10; z_pT_Bin_Borders[15][34][3] = 0.8;
Phi_h_Bin_Values[15][34][0] =  1; Phi_h_Bin_Values[15][34][1] = 539; Phi_h_Bin_Values[15][34][2] = 10946;
z_pT_Bin_Borders[15][35][0] = 0.49; z_pT_Bin_Borders[15][35][1] = 0.4; z_pT_Bin_Borders[15][35][2] = 0.05; z_pT_Bin_Borders[15][35][3] = 0;
Phi_h_Bin_Values[15][35][0] =  1; Phi_h_Bin_Values[15][35][1] = 540; Phi_h_Bin_Values[15][35][2] = 10947;
z_pT_Bin_Borders[15][36][0] = 0.49; z_pT_Bin_Borders[15][36][1] = 0.4; z_pT_Bin_Borders[15][36][2] = 10; z_pT_Bin_Borders[15][36][3] = 0.8;
Phi_h_Bin_Values[15][36][0] =  1; Phi_h_Bin_Values[15][36][1] = 541; Phi_h_Bin_Values[15][36][2] = 10948;
z_pT_Bin_Borders[15][37][0] = 0.4; z_pT_Bin_Borders[15][37][1] = 0.32; z_pT_Bin_Borders[15][37][2] = 0.05; z_pT_Bin_Borders[15][37][3] = 0;
Phi_h_Bin_Values[15][37][0] =  1; Phi_h_Bin_Values[15][37][1] = 542; Phi_h_Bin_Values[15][37][2] = 10949;
z_pT_Bin_Borders[15][38][0] = 0.4; z_pT_Bin_Borders[15][38][1] = 0.32; z_pT_Bin_Borders[15][38][2] = 10; z_pT_Bin_Borders[15][38][3] = 0.8;
Phi_h_Bin_Values[15][38][0] =  1; Phi_h_Bin_Values[15][38][1] = 543; Phi_h_Bin_Values[15][38][2] = 10950;
z_pT_Bin_Borders[15][39][0] = 0.32; z_pT_Bin_Borders[15][39][1] = 0.27; z_pT_Bin_Borders[15][39][2] = 0.05; z_pT_Bin_Borders[15][39][3] = 0;
Phi_h_Bin_Values[15][39][0] =  1; Phi_h_Bin_Values[15][39][1] = 544; Phi_h_Bin_Values[15][39][2] = 10951;
z_pT_Bin_Borders[15][40][0] = 0.32; z_pT_Bin_Borders[15][40][1] = 0.27; z_pT_Bin_Borders[15][40][2] = 10; z_pT_Bin_Borders[15][40][3] = 0.8;
Phi_h_Bin_Values[15][40][0] =  1; Phi_h_Bin_Values[15][40][1] = 545; Phi_h_Bin_Values[15][40][2] = 10952;
z_pT_Bin_Borders[15][41][0] = 0.27; z_pT_Bin_Borders[15][41][1] = 0.22; z_pT_Bin_Borders[15][41][2] = 0.05; z_pT_Bin_Borders[15][41][3] = 0;
Phi_h_Bin_Values[15][41][0] =  1; Phi_h_Bin_Values[15][41][1] = 546; Phi_h_Bin_Values[15][41][2] = 10953;
z_pT_Bin_Borders[15][42][0] = 0.27; z_pT_Bin_Borders[15][42][1] = 0.22; z_pT_Bin_Borders[15][42][2] = 10; z_pT_Bin_Borders[15][42][3] = 0.8;
Phi_h_Bin_Values[15][42][0] =  1; Phi_h_Bin_Values[15][42][1] = 547; Phi_h_Bin_Values[15][42][2] = 10954;
z_pT_Bin_Borders[15][43][0] = 0.22; z_pT_Bin_Borders[15][43][1] = 0; z_pT_Bin_Borders[15][43][2] = 0.05; z_pT_Bin_Borders[15][43][3] = 0;
Phi_h_Bin_Values[15][43][0] =  1; Phi_h_Bin_Values[15][43][1] = 548; Phi_h_Bin_Values[15][43][2] = 10955;
z_pT_Bin_Borders[15][44][0] = 0.22; z_pT_Bin_Borders[15][44][1] = 0; z_pT_Bin_Borders[15][44][2] = 0.22; z_pT_Bin_Borders[15][44][3] = 0.05;
Phi_h_Bin_Values[15][44][0] =  1; Phi_h_Bin_Values[15][44][1] = 549; Phi_h_Bin_Values[15][44][2] = 10956;
z_pT_Bin_Borders[15][45][0] = 0.22; z_pT_Bin_Borders[15][45][1] = 0; z_pT_Bin_Borders[15][45][2] = 0.32; z_pT_Bin_Borders[15][45][3] = 0.22;
Phi_h_Bin_Values[15][45][0] =  1; Phi_h_Bin_Values[15][45][1] = 550; Phi_h_Bin_Values[15][45][2] = 10957;
z_pT_Bin_Borders[15][46][0] = 0.22; z_pT_Bin_Borders[15][46][1] = 0; z_pT_Bin_Borders[15][46][2] = 0.42; z_pT_Bin_Borders[15][46][3] = 0.32;
Phi_h_Bin_Values[15][46][0] =  1; Phi_h_Bin_Values[15][46][1] = 551; Phi_h_Bin_Values[15][46][2] = 10958;
z_pT_Bin_Borders[15][47][0] = 0.22; z_pT_Bin_Borders[15][47][1] = 0; z_pT_Bin_Borders[15][47][2] = 0.55; z_pT_Bin_Borders[15][47][3] = 0.42;
Phi_h_Bin_Values[15][47][0] =  1; Phi_h_Bin_Values[15][47][1] = 552; Phi_h_Bin_Values[15][47][2] = 10959;
z_pT_Bin_Borders[15][48][0] = 0.22; z_pT_Bin_Borders[15][48][1] = 0; z_pT_Bin_Borders[15][48][2] = 0.8; z_pT_Bin_Borders[15][48][3] = 0.55;
Phi_h_Bin_Values[15][48][0] =  1; Phi_h_Bin_Values[15][48][1] = 553; Phi_h_Bin_Values[15][48][2] = 10960;
z_pT_Bin_Borders[15][49][0] = 0.22; z_pT_Bin_Borders[15][49][1] = 0; z_pT_Bin_Borders[15][49][2] = 10; z_pT_Bin_Borders[15][49][3] = 0.8;
Phi_h_Bin_Values[15][49][0] =  1; Phi_h_Bin_Values[15][49][1] = 554; Phi_h_Bin_Values[15][49][2] = 10961;
z_pT_Bin_Borders[16][1][0] = 0.67; z_pT_Bin_Borders[16][1][1] = 0.42; z_pT_Bin_Borders[16][1][2] = 0.22; z_pT_Bin_Borders[16][1][3] = 0.05;
Phi_h_Bin_Values[16][1][0] =  24; Phi_h_Bin_Values[16][1][1] = 0; Phi_h_Bin_Values[16][1][2] = 10962;
z_pT_Bin_Borders[16][2][0] = 0.67; z_pT_Bin_Borders[16][2][1] = 0.42; z_pT_Bin_Borders[16][2][2] = 0.32; z_pT_Bin_Borders[16][2][3] = 0.22;
Phi_h_Bin_Values[16][2][0] =  24; Phi_h_Bin_Values[16][2][1] = 24; Phi_h_Bin_Values[16][2][2] = 10986;
z_pT_Bin_Borders[16][3][0] = 0.67; z_pT_Bin_Borders[16][3][1] = 0.42; z_pT_Bin_Borders[16][3][2] = 0.42; z_pT_Bin_Borders[16][3][3] = 0.32;
Phi_h_Bin_Values[16][3][0] =  24; Phi_h_Bin_Values[16][3][1] = 48; Phi_h_Bin_Values[16][3][2] = 11010;
z_pT_Bin_Borders[16][4][0] = 0.67; z_pT_Bin_Borders[16][4][1] = 0.42; z_pT_Bin_Borders[16][4][2] = 0.52; z_pT_Bin_Borders[16][4][3] = 0.42;
Phi_h_Bin_Values[16][4][0] =  24; Phi_h_Bin_Values[16][4][1] = 72; Phi_h_Bin_Values[16][4][2] = 11034;
z_pT_Bin_Borders[16][5][0] = 0.67; z_pT_Bin_Borders[16][5][1] = 0.42; z_pT_Bin_Borders[16][5][2] = 0.66; z_pT_Bin_Borders[16][5][3] = 0.52;
Phi_h_Bin_Values[16][5][0] =  24; Phi_h_Bin_Values[16][5][1] = 96; Phi_h_Bin_Values[16][5][2] = 11058;
z_pT_Bin_Borders[16][6][0] = 0.67; z_pT_Bin_Borders[16][6][1] = 0.42; z_pT_Bin_Borders[16][6][2] = 0.9; z_pT_Bin_Borders[16][6][3] = 0.66;
Phi_h_Bin_Values[16][6][0] =  24; Phi_h_Bin_Values[16][6][1] = 120; Phi_h_Bin_Values[16][6][2] = 11082;
z_pT_Bin_Borders[16][7][0] = 0.42; z_pT_Bin_Borders[16][7][1] = 0.31; z_pT_Bin_Borders[16][7][2] = 0.22; z_pT_Bin_Borders[16][7][3] = 0.05;
Phi_h_Bin_Values[16][7][0] =  24; Phi_h_Bin_Values[16][7][1] = 144; Phi_h_Bin_Values[16][7][2] = 11106;
z_pT_Bin_Borders[16][8][0] = 0.42; z_pT_Bin_Borders[16][8][1] = 0.31; z_pT_Bin_Borders[16][8][2] = 0.32; z_pT_Bin_Borders[16][8][3] = 0.22;
Phi_h_Bin_Values[16][8][0] =  24; Phi_h_Bin_Values[16][8][1] = 168; Phi_h_Bin_Values[16][8][2] = 11130;
z_pT_Bin_Borders[16][9][0] = 0.42; z_pT_Bin_Borders[16][9][1] = 0.31; z_pT_Bin_Borders[16][9][2] = 0.42; z_pT_Bin_Borders[16][9][3] = 0.32;
Phi_h_Bin_Values[16][9][0] =  24; Phi_h_Bin_Values[16][9][1] = 192; Phi_h_Bin_Values[16][9][2] = 11154;
z_pT_Bin_Borders[16][10][0] = 0.42; z_pT_Bin_Borders[16][10][1] = 0.31; z_pT_Bin_Borders[16][10][2] = 0.52; z_pT_Bin_Borders[16][10][3] = 0.42;
Phi_h_Bin_Values[16][10][0] =  24; Phi_h_Bin_Values[16][10][1] = 216; Phi_h_Bin_Values[16][10][2] = 11178;
z_pT_Bin_Borders[16][11][0] = 0.42; z_pT_Bin_Borders[16][11][1] = 0.31; z_pT_Bin_Borders[16][11][2] = 0.66; z_pT_Bin_Borders[16][11][3] = 0.52;
Phi_h_Bin_Values[16][11][0] =  24; Phi_h_Bin_Values[16][11][1] = 240; Phi_h_Bin_Values[16][11][2] = 11202;
z_pT_Bin_Borders[16][12][0] = 0.42; z_pT_Bin_Borders[16][12][1] = 0.31; z_pT_Bin_Borders[16][12][2] = 0.9; z_pT_Bin_Borders[16][12][3] = 0.66;
Phi_h_Bin_Values[16][12][0] =  24; Phi_h_Bin_Values[16][12][1] = 264; Phi_h_Bin_Values[16][12][2] = 11226;
z_pT_Bin_Borders[16][13][0] = 0.31; z_pT_Bin_Borders[16][13][1] = 0.24; z_pT_Bin_Borders[16][13][2] = 0.22; z_pT_Bin_Borders[16][13][3] = 0.05;
Phi_h_Bin_Values[16][13][0] =  24; Phi_h_Bin_Values[16][13][1] = 288; Phi_h_Bin_Values[16][13][2] = 11250;
z_pT_Bin_Borders[16][14][0] = 0.31; z_pT_Bin_Borders[16][14][1] = 0.24; z_pT_Bin_Borders[16][14][2] = 0.32; z_pT_Bin_Borders[16][14][3] = 0.22;
Phi_h_Bin_Values[16][14][0] =  24; Phi_h_Bin_Values[16][14][1] = 312; Phi_h_Bin_Values[16][14][2] = 11274;
z_pT_Bin_Borders[16][15][0] = 0.31; z_pT_Bin_Borders[16][15][1] = 0.24; z_pT_Bin_Borders[16][15][2] = 0.42; z_pT_Bin_Borders[16][15][3] = 0.32;
Phi_h_Bin_Values[16][15][0] =  24; Phi_h_Bin_Values[16][15][1] = 336; Phi_h_Bin_Values[16][15][2] = 11298;
z_pT_Bin_Borders[16][16][0] = 0.31; z_pT_Bin_Borders[16][16][1] = 0.24; z_pT_Bin_Borders[16][16][2] = 0.52; z_pT_Bin_Borders[16][16][3] = 0.42;
Phi_h_Bin_Values[16][16][0] =  24; Phi_h_Bin_Values[16][16][1] = 360; Phi_h_Bin_Values[16][16][2] = 11322;
z_pT_Bin_Borders[16][17][0] = 0.31; z_pT_Bin_Borders[16][17][1] = 0.24; z_pT_Bin_Borders[16][17][2] = 0.66; z_pT_Bin_Borders[16][17][3] = 0.52;
Phi_h_Bin_Values[16][17][0] =  24; Phi_h_Bin_Values[16][17][1] = 384; Phi_h_Bin_Values[16][17][2] = 11346;
z_pT_Bin_Borders[16][18][0] = 0.31; z_pT_Bin_Borders[16][18][1] = 0.24; z_pT_Bin_Borders[16][18][2] = 0.9; z_pT_Bin_Borders[16][18][3] = 0.66;
Phi_h_Bin_Values[16][18][0] =  1; Phi_h_Bin_Values[16][18][1] = 408; Phi_h_Bin_Values[16][18][2] = 11370;
z_pT_Bin_Borders[16][19][0] = 0.24; z_pT_Bin_Borders[16][19][1] = 0.2; z_pT_Bin_Borders[16][19][2] = 0.22; z_pT_Bin_Borders[16][19][3] = 0.05;
Phi_h_Bin_Values[16][19][0] =  24; Phi_h_Bin_Values[16][19][1] = 409; Phi_h_Bin_Values[16][19][2] = 11371;
z_pT_Bin_Borders[16][20][0] = 0.24; z_pT_Bin_Borders[16][20][1] = 0.2; z_pT_Bin_Borders[16][20][2] = 0.32; z_pT_Bin_Borders[16][20][3] = 0.22;
Phi_h_Bin_Values[16][20][0] =  24; Phi_h_Bin_Values[16][20][1] = 433; Phi_h_Bin_Values[16][20][2] = 11395;
z_pT_Bin_Borders[16][21][0] = 0.24; z_pT_Bin_Borders[16][21][1] = 0.2; z_pT_Bin_Borders[16][21][2] = 0.42; z_pT_Bin_Borders[16][21][3] = 0.32;
Phi_h_Bin_Values[16][21][0] =  24; Phi_h_Bin_Values[16][21][1] = 457; Phi_h_Bin_Values[16][21][2] = 11419;
z_pT_Bin_Borders[16][22][0] = 0.24; z_pT_Bin_Borders[16][22][1] = 0.2; z_pT_Bin_Borders[16][22][2] = 0.52; z_pT_Bin_Borders[16][22][3] = 0.42;
Phi_h_Bin_Values[16][22][0] =  24; Phi_h_Bin_Values[16][22][1] = 481; Phi_h_Bin_Values[16][22][2] = 11443;
z_pT_Bin_Borders[16][23][0] = 0.24; z_pT_Bin_Borders[16][23][1] = 0.2; z_pT_Bin_Borders[16][23][2] = 0.66; z_pT_Bin_Borders[16][23][3] = 0.52;
Phi_h_Bin_Values[16][23][0] =  1; Phi_h_Bin_Values[16][23][1] = 505; Phi_h_Bin_Values[16][23][2] = 11467;
z_pT_Bin_Borders[16][24][0] = 0.24; z_pT_Bin_Borders[16][24][1] = 0.2; z_pT_Bin_Borders[16][24][2] = 0.9; z_pT_Bin_Borders[16][24][3] = 0.66;
Phi_h_Bin_Values[16][24][0] =  1; Phi_h_Bin_Values[16][24][1] = 506; Phi_h_Bin_Values[16][24][2] = 11468;
z_pT_Bin_Borders[16][25][0] = 0.2; z_pT_Bin_Borders[16][25][1] = 0.16; z_pT_Bin_Borders[16][25][2] = 0.22; z_pT_Bin_Borders[16][25][3] = 0.05;
Phi_h_Bin_Values[16][25][0] =  24; Phi_h_Bin_Values[16][25][1] = 507; Phi_h_Bin_Values[16][25][2] = 11469;
z_pT_Bin_Borders[16][26][0] = 0.2; z_pT_Bin_Borders[16][26][1] = 0.16; z_pT_Bin_Borders[16][26][2] = 0.32; z_pT_Bin_Borders[16][26][3] = 0.22;
Phi_h_Bin_Values[16][26][0] =  24; Phi_h_Bin_Values[16][26][1] = 531; Phi_h_Bin_Values[16][26][2] = 11493;
z_pT_Bin_Borders[16][27][0] = 0.2; z_pT_Bin_Borders[16][27][1] = 0.16; z_pT_Bin_Borders[16][27][2] = 0.42; z_pT_Bin_Borders[16][27][3] = 0.32;
Phi_h_Bin_Values[16][27][0] =  24; Phi_h_Bin_Values[16][27][1] = 555; Phi_h_Bin_Values[16][27][2] = 11517;
z_pT_Bin_Borders[16][28][0] = 0.2; z_pT_Bin_Borders[16][28][1] = 0.16; z_pT_Bin_Borders[16][28][2] = 0.52; z_pT_Bin_Borders[16][28][3] = 0.42;
Phi_h_Bin_Values[16][28][0] =  1; Phi_h_Bin_Values[16][28][1] = 579; Phi_h_Bin_Values[16][28][2] = 11541;
z_pT_Bin_Borders[16][29][0] = 0.2; z_pT_Bin_Borders[16][29][1] = 0.16; z_pT_Bin_Borders[16][29][2] = 0.66; z_pT_Bin_Borders[16][29][3] = 0.52;
Phi_h_Bin_Values[16][29][0] =  1; Phi_h_Bin_Values[16][29][1] = 580; Phi_h_Bin_Values[16][29][2] = 11542;
z_pT_Bin_Borders[16][30][0] = 0.2; z_pT_Bin_Borders[16][30][1] = 0.16; z_pT_Bin_Borders[16][30][2] = 0.9; z_pT_Bin_Borders[16][30][3] = 0.66;
Phi_h_Bin_Values[16][30][0] =  1; Phi_h_Bin_Values[16][30][1] = 581; Phi_h_Bin_Values[16][30][2] = 11543;
z_pT_Bin_Borders[16][31][0] = 10; z_pT_Bin_Borders[16][31][1] = 0.67; z_pT_Bin_Borders[16][31][2] = 0.05; z_pT_Bin_Borders[16][31][3] = 0;
Phi_h_Bin_Values[16][31][0] =  1; Phi_h_Bin_Values[16][31][1] = 582; Phi_h_Bin_Values[16][31][2] = 11544;
z_pT_Bin_Borders[16][32][0] = 10; z_pT_Bin_Borders[16][32][1] = 0.67; z_pT_Bin_Borders[16][32][2] = 0.22; z_pT_Bin_Borders[16][32][3] = 0.05;
Phi_h_Bin_Values[16][32][0] =  1; Phi_h_Bin_Values[16][32][1] = 583; Phi_h_Bin_Values[16][32][2] = 11545;
z_pT_Bin_Borders[16][33][0] = 10; z_pT_Bin_Borders[16][33][1] = 0.67; z_pT_Bin_Borders[16][33][2] = 0.32; z_pT_Bin_Borders[16][33][3] = 0.22;
Phi_h_Bin_Values[16][33][0] =  1; Phi_h_Bin_Values[16][33][1] = 584; Phi_h_Bin_Values[16][33][2] = 11546;
z_pT_Bin_Borders[16][34][0] = 10; z_pT_Bin_Borders[16][34][1] = 0.67; z_pT_Bin_Borders[16][34][2] = 0.42; z_pT_Bin_Borders[16][34][3] = 0.32;
Phi_h_Bin_Values[16][34][0] =  1; Phi_h_Bin_Values[16][34][1] = 585; Phi_h_Bin_Values[16][34][2] = 11547;
z_pT_Bin_Borders[16][35][0] = 10; z_pT_Bin_Borders[16][35][1] = 0.67; z_pT_Bin_Borders[16][35][2] = 0.52; z_pT_Bin_Borders[16][35][3] = 0.42;
Phi_h_Bin_Values[16][35][0] =  1; Phi_h_Bin_Values[16][35][1] = 586; Phi_h_Bin_Values[16][35][2] = 11548;
z_pT_Bin_Borders[16][36][0] = 10; z_pT_Bin_Borders[16][36][1] = 0.67; z_pT_Bin_Borders[16][36][2] = 0.66; z_pT_Bin_Borders[16][36][3] = 0.52;
Phi_h_Bin_Values[16][36][0] =  1; Phi_h_Bin_Values[16][36][1] = 587; Phi_h_Bin_Values[16][36][2] = 11549;
z_pT_Bin_Borders[16][37][0] = 10; z_pT_Bin_Borders[16][37][1] = 0.67; z_pT_Bin_Borders[16][37][2] = 0.9; z_pT_Bin_Borders[16][37][3] = 0.66;
Phi_h_Bin_Values[16][37][0] =  1; Phi_h_Bin_Values[16][37][1] = 588; Phi_h_Bin_Values[16][37][2] = 11550;
z_pT_Bin_Borders[16][38][0] = 10; z_pT_Bin_Borders[16][38][1] = 0.67; z_pT_Bin_Borders[16][38][2] = 10; z_pT_Bin_Borders[16][38][3] = 0.9;
Phi_h_Bin_Values[16][38][0] =  1; Phi_h_Bin_Values[16][38][1] = 589; Phi_h_Bin_Values[16][38][2] = 11551;
z_pT_Bin_Borders[16][39][0] = 0.67; z_pT_Bin_Borders[16][39][1] = 0.42; z_pT_Bin_Borders[16][39][2] = 0.05; z_pT_Bin_Borders[16][39][3] = 0;
Phi_h_Bin_Values[16][39][0] =  1; Phi_h_Bin_Values[16][39][1] = 590; Phi_h_Bin_Values[16][39][2] = 11552;
z_pT_Bin_Borders[16][40][0] = 0.67; z_pT_Bin_Borders[16][40][1] = 0.42; z_pT_Bin_Borders[16][40][2] = 10; z_pT_Bin_Borders[16][40][3] = 0.9;
Phi_h_Bin_Values[16][40][0] =  1; Phi_h_Bin_Values[16][40][1] = 591; Phi_h_Bin_Values[16][40][2] = 11553;
z_pT_Bin_Borders[16][41][0] = 0.42; z_pT_Bin_Borders[16][41][1] = 0.31; z_pT_Bin_Borders[16][41][2] = 0.05; z_pT_Bin_Borders[16][41][3] = 0;
Phi_h_Bin_Values[16][41][0] =  1; Phi_h_Bin_Values[16][41][1] = 592; Phi_h_Bin_Values[16][41][2] = 11554;
z_pT_Bin_Borders[16][42][0] = 0.42; z_pT_Bin_Borders[16][42][1] = 0.31; z_pT_Bin_Borders[16][42][2] = 10; z_pT_Bin_Borders[16][42][3] = 0.9;
Phi_h_Bin_Values[16][42][0] =  1; Phi_h_Bin_Values[16][42][1] = 593; Phi_h_Bin_Values[16][42][2] = 11555;
z_pT_Bin_Borders[16][43][0] = 0.31; z_pT_Bin_Borders[16][43][1] = 0.24; z_pT_Bin_Borders[16][43][2] = 0.05; z_pT_Bin_Borders[16][43][3] = 0;
Phi_h_Bin_Values[16][43][0] =  1; Phi_h_Bin_Values[16][43][1] = 594; Phi_h_Bin_Values[16][43][2] = 11556;
z_pT_Bin_Borders[16][44][0] = 0.31; z_pT_Bin_Borders[16][44][1] = 0.24; z_pT_Bin_Borders[16][44][2] = 10; z_pT_Bin_Borders[16][44][3] = 0.9;
Phi_h_Bin_Values[16][44][0] =  1; Phi_h_Bin_Values[16][44][1] = 595; Phi_h_Bin_Values[16][44][2] = 11557;
z_pT_Bin_Borders[16][45][0] = 0.24; z_pT_Bin_Borders[16][45][1] = 0.2; z_pT_Bin_Borders[16][45][2] = 0.05; z_pT_Bin_Borders[16][45][3] = 0;
Phi_h_Bin_Values[16][45][0] =  1; Phi_h_Bin_Values[16][45][1] = 596; Phi_h_Bin_Values[16][45][2] = 11558;
z_pT_Bin_Borders[16][46][0] = 0.24; z_pT_Bin_Borders[16][46][1] = 0.2; z_pT_Bin_Borders[16][46][2] = 10; z_pT_Bin_Borders[16][46][3] = 0.9;
Phi_h_Bin_Values[16][46][0] =  1; Phi_h_Bin_Values[16][46][1] = 597; Phi_h_Bin_Values[16][46][2] = 11559;
z_pT_Bin_Borders[16][47][0] = 0.2; z_pT_Bin_Borders[16][47][1] = 0.16; z_pT_Bin_Borders[16][47][2] = 0.05; z_pT_Bin_Borders[16][47][3] = 0;
Phi_h_Bin_Values[16][47][0] =  1; Phi_h_Bin_Values[16][47][1] = 598; Phi_h_Bin_Values[16][47][2] = 11560;
z_pT_Bin_Borders[16][48][0] = 0.2; z_pT_Bin_Borders[16][48][1] = 0.16; z_pT_Bin_Borders[16][48][2] = 10; z_pT_Bin_Borders[16][48][3] = 0.9;
Phi_h_Bin_Values[16][48][0] =  1; Phi_h_Bin_Values[16][48][1] = 599; Phi_h_Bin_Values[16][48][2] = 11561;
z_pT_Bin_Borders[16][49][0] = 0.16; z_pT_Bin_Borders[16][49][1] = 0; z_pT_Bin_Borders[16][49][2] = 0.05; z_pT_Bin_Borders[16][49][3] = 0;
Phi_h_Bin_Values[16][49][0] =  1; Phi_h_Bin_Values[16][49][1] = 600; Phi_h_Bin_Values[16][49][2] = 11562;
z_pT_Bin_Borders[16][50][0] = 0.16; z_pT_Bin_Borders[16][50][1] = 0; z_pT_Bin_Borders[16][50][2] = 0.22; z_pT_Bin_Borders[16][50][3] = 0.05;
Phi_h_Bin_Values[16][50][0] =  1; Phi_h_Bin_Values[16][50][1] = 601; Phi_h_Bin_Values[16][50][2] = 11563;
z_pT_Bin_Borders[16][51][0] = 0.16; z_pT_Bin_Borders[16][51][1] = 0; z_pT_Bin_Borders[16][51][2] = 0.32; z_pT_Bin_Borders[16][51][3] = 0.22;
Phi_h_Bin_Values[16][51][0] =  1; Phi_h_Bin_Values[16][51][1] = 602; Phi_h_Bin_Values[16][51][2] = 11564;
z_pT_Bin_Borders[16][52][0] = 0.16; z_pT_Bin_Borders[16][52][1] = 0; z_pT_Bin_Borders[16][52][2] = 0.42; z_pT_Bin_Borders[16][52][3] = 0.32;
Phi_h_Bin_Values[16][52][0] =  1; Phi_h_Bin_Values[16][52][1] = 603; Phi_h_Bin_Values[16][52][2] = 11565;
z_pT_Bin_Borders[16][53][0] = 0.16; z_pT_Bin_Borders[16][53][1] = 0; z_pT_Bin_Borders[16][53][2] = 0.52; z_pT_Bin_Borders[16][53][3] = 0.42;
Phi_h_Bin_Values[16][53][0] =  1; Phi_h_Bin_Values[16][53][1] = 604; Phi_h_Bin_Values[16][53][2] = 11566;
z_pT_Bin_Borders[16][54][0] = 0.16; z_pT_Bin_Borders[16][54][1] = 0; z_pT_Bin_Borders[16][54][2] = 0.66; z_pT_Bin_Borders[16][54][3] = 0.52;
Phi_h_Bin_Values[16][54][0] =  1; Phi_h_Bin_Values[16][54][1] = 605; Phi_h_Bin_Values[16][54][2] = 11567;
z_pT_Bin_Borders[16][55][0] = 0.16; z_pT_Bin_Borders[16][55][1] = 0; z_pT_Bin_Borders[16][55][2] = 0.9; z_pT_Bin_Borders[16][55][3] = 0.66;
Phi_h_Bin_Values[16][55][0] =  1; Phi_h_Bin_Values[16][55][1] = 606; Phi_h_Bin_Values[16][55][2] = 11568;
z_pT_Bin_Borders[16][56][0] = 0.16; z_pT_Bin_Borders[16][56][1] = 0; z_pT_Bin_Borders[16][56][2] = 10; z_pT_Bin_Borders[16][56][3] = 0.9;
Phi_h_Bin_Values[16][56][0] =  1; Phi_h_Bin_Values[16][56][1] = 607; Phi_h_Bin_Values[16][56][2] = 11569;
z_pT_Bin_Borders[17][1][0] = 0.68; z_pT_Bin_Borders[17][1][1] = 0.44; z_pT_Bin_Borders[17][1][2] = 0.19; z_pT_Bin_Borders[17][1][3] = 0.05;
Phi_h_Bin_Values[17][1][0] =  24; Phi_h_Bin_Values[17][1][1] = 0; Phi_h_Bin_Values[17][1][2] = 11570;
z_pT_Bin_Borders[17][2][0] = 0.68; z_pT_Bin_Borders[17][2][1] = 0.44; z_pT_Bin_Borders[17][2][2] = 0.28; z_pT_Bin_Borders[17][2][3] = 0.19;
Phi_h_Bin_Values[17][2][0] =  24; Phi_h_Bin_Values[17][2][1] = 24; Phi_h_Bin_Values[17][2][2] = 11594;
z_pT_Bin_Borders[17][3][0] = 0.68; z_pT_Bin_Borders[17][3][1] = 0.44; z_pT_Bin_Borders[17][3][2] = 0.37; z_pT_Bin_Borders[17][3][3] = 0.28;
Phi_h_Bin_Values[17][3][0] =  24; Phi_h_Bin_Values[17][3][1] = 48; Phi_h_Bin_Values[17][3][2] = 11618;
z_pT_Bin_Borders[17][4][0] = 0.68; z_pT_Bin_Borders[17][4][1] = 0.44; z_pT_Bin_Borders[17][4][2] = 0.45; z_pT_Bin_Borders[17][4][3] = 0.37;
Phi_h_Bin_Values[17][4][0] =  24; Phi_h_Bin_Values[17][4][1] = 72; Phi_h_Bin_Values[17][4][2] = 11642;
z_pT_Bin_Borders[17][5][0] = 0.68; z_pT_Bin_Borders[17][5][1] = 0.44; z_pT_Bin_Borders[17][5][2] = 0.55; z_pT_Bin_Borders[17][5][3] = 0.45;
Phi_h_Bin_Values[17][5][0] =  24; Phi_h_Bin_Values[17][5][1] = 96; Phi_h_Bin_Values[17][5][2] = 11666;
z_pT_Bin_Borders[17][6][0] = 0.68; z_pT_Bin_Borders[17][6][1] = 0.44; z_pT_Bin_Borders[17][6][2] = 0.73; z_pT_Bin_Borders[17][6][3] = 0.55;
Phi_h_Bin_Values[17][6][0] =  24; Phi_h_Bin_Values[17][6][1] = 120; Phi_h_Bin_Values[17][6][2] = 11690;
z_pT_Bin_Borders[17][7][0] = 0.44; z_pT_Bin_Borders[17][7][1] = 0.34; z_pT_Bin_Borders[17][7][2] = 0.19; z_pT_Bin_Borders[17][7][3] = 0.05;
Phi_h_Bin_Values[17][7][0] =  24; Phi_h_Bin_Values[17][7][1] = 144; Phi_h_Bin_Values[17][7][2] = 11714;
z_pT_Bin_Borders[17][8][0] = 0.44; z_pT_Bin_Borders[17][8][1] = 0.34; z_pT_Bin_Borders[17][8][2] = 0.28; z_pT_Bin_Borders[17][8][3] = 0.19;
Phi_h_Bin_Values[17][8][0] =  24; Phi_h_Bin_Values[17][8][1] = 168; Phi_h_Bin_Values[17][8][2] = 11738;
z_pT_Bin_Borders[17][9][0] = 0.44; z_pT_Bin_Borders[17][9][1] = 0.34; z_pT_Bin_Borders[17][9][2] = 0.37; z_pT_Bin_Borders[17][9][3] = 0.28;
Phi_h_Bin_Values[17][9][0] =  24; Phi_h_Bin_Values[17][9][1] = 192; Phi_h_Bin_Values[17][9][2] = 11762;
z_pT_Bin_Borders[17][10][0] = 0.44; z_pT_Bin_Borders[17][10][1] = 0.34; z_pT_Bin_Borders[17][10][2] = 0.45; z_pT_Bin_Borders[17][10][3] = 0.37;
Phi_h_Bin_Values[17][10][0] =  24; Phi_h_Bin_Values[17][10][1] = 216; Phi_h_Bin_Values[17][10][2] = 11786;
z_pT_Bin_Borders[17][11][0] = 0.44; z_pT_Bin_Borders[17][11][1] = 0.34; z_pT_Bin_Borders[17][11][2] = 0.55; z_pT_Bin_Borders[17][11][3] = 0.45;
Phi_h_Bin_Values[17][11][0] =  24; Phi_h_Bin_Values[17][11][1] = 240; Phi_h_Bin_Values[17][11][2] = 11810;
z_pT_Bin_Borders[17][12][0] = 0.44; z_pT_Bin_Borders[17][12][1] = 0.34; z_pT_Bin_Borders[17][12][2] = 0.73; z_pT_Bin_Borders[17][12][3] = 0.55;
Phi_h_Bin_Values[17][12][0] =  24; Phi_h_Bin_Values[17][12][1] = 264; Phi_h_Bin_Values[17][12][2] = 11834;
z_pT_Bin_Borders[17][13][0] = 0.34; z_pT_Bin_Borders[17][13][1] = 0.28; z_pT_Bin_Borders[17][13][2] = 0.19; z_pT_Bin_Borders[17][13][3] = 0.05;
Phi_h_Bin_Values[17][13][0] =  24; Phi_h_Bin_Values[17][13][1] = 288; Phi_h_Bin_Values[17][13][2] = 11858;
z_pT_Bin_Borders[17][14][0] = 0.34; z_pT_Bin_Borders[17][14][1] = 0.28; z_pT_Bin_Borders[17][14][2] = 0.28; z_pT_Bin_Borders[17][14][3] = 0.19;
Phi_h_Bin_Values[17][14][0] =  24; Phi_h_Bin_Values[17][14][1] = 312; Phi_h_Bin_Values[17][14][2] = 11882;
z_pT_Bin_Borders[17][15][0] = 0.34; z_pT_Bin_Borders[17][15][1] = 0.28; z_pT_Bin_Borders[17][15][2] = 0.37; z_pT_Bin_Borders[17][15][3] = 0.28;
Phi_h_Bin_Values[17][15][0] =  24; Phi_h_Bin_Values[17][15][1] = 336; Phi_h_Bin_Values[17][15][2] = 11906;
z_pT_Bin_Borders[17][16][0] = 0.34; z_pT_Bin_Borders[17][16][1] = 0.28; z_pT_Bin_Borders[17][16][2] = 0.45; z_pT_Bin_Borders[17][16][3] = 0.37;
Phi_h_Bin_Values[17][16][0] =  24; Phi_h_Bin_Values[17][16][1] = 360; Phi_h_Bin_Values[17][16][2] = 11930;
z_pT_Bin_Borders[17][17][0] = 0.34; z_pT_Bin_Borders[17][17][1] = 0.28; z_pT_Bin_Borders[17][17][2] = 0.55; z_pT_Bin_Borders[17][17][3] = 0.45;
Phi_h_Bin_Values[17][17][0] =  24; Phi_h_Bin_Values[17][17][1] = 384; Phi_h_Bin_Values[17][17][2] = 11954;
z_pT_Bin_Borders[17][18][0] = 0.34; z_pT_Bin_Borders[17][18][1] = 0.28; z_pT_Bin_Borders[17][18][2] = 0.73; z_pT_Bin_Borders[17][18][3] = 0.55;
Phi_h_Bin_Values[17][18][0] =  24; Phi_h_Bin_Values[17][18][1] = 408; Phi_h_Bin_Values[17][18][2] = 11978;
z_pT_Bin_Borders[17][19][0] = 0.28; z_pT_Bin_Borders[17][19][1] = 0.23; z_pT_Bin_Borders[17][19][2] = 0.19; z_pT_Bin_Borders[17][19][3] = 0.05;
Phi_h_Bin_Values[17][19][0] =  24; Phi_h_Bin_Values[17][19][1] = 432; Phi_h_Bin_Values[17][19][2] = 12002;
z_pT_Bin_Borders[17][20][0] = 0.28; z_pT_Bin_Borders[17][20][1] = 0.23; z_pT_Bin_Borders[17][20][2] = 0.28; z_pT_Bin_Borders[17][20][3] = 0.19;
Phi_h_Bin_Values[17][20][0] =  24; Phi_h_Bin_Values[17][20][1] = 456; Phi_h_Bin_Values[17][20][2] = 12026;
z_pT_Bin_Borders[17][21][0] = 0.28; z_pT_Bin_Borders[17][21][1] = 0.23; z_pT_Bin_Borders[17][21][2] = 0.37; z_pT_Bin_Borders[17][21][3] = 0.28;
Phi_h_Bin_Values[17][21][0] =  24; Phi_h_Bin_Values[17][21][1] = 480; Phi_h_Bin_Values[17][21][2] = 12050;
z_pT_Bin_Borders[17][22][0] = 0.28; z_pT_Bin_Borders[17][22][1] = 0.23; z_pT_Bin_Borders[17][22][2] = 0.45; z_pT_Bin_Borders[17][22][3] = 0.37;
Phi_h_Bin_Values[17][22][0] =  24; Phi_h_Bin_Values[17][22][1] = 504; Phi_h_Bin_Values[17][22][2] = 12074;
z_pT_Bin_Borders[17][23][0] = 0.28; z_pT_Bin_Borders[17][23][1] = 0.23; z_pT_Bin_Borders[17][23][2] = 0.55; z_pT_Bin_Borders[17][23][3] = 0.45;
Phi_h_Bin_Values[17][23][0] =  24; Phi_h_Bin_Values[17][23][1] = 528; Phi_h_Bin_Values[17][23][2] = 12098;
z_pT_Bin_Borders[17][24][0] = 0.28; z_pT_Bin_Borders[17][24][1] = 0.23; z_pT_Bin_Borders[17][24][2] = 0.73; z_pT_Bin_Borders[17][24][3] = 0.55;
Phi_h_Bin_Values[17][24][0] =  1; Phi_h_Bin_Values[17][24][1] = 552; Phi_h_Bin_Values[17][24][2] = 12122;
z_pT_Bin_Borders[17][25][0] = 0.23; z_pT_Bin_Borders[17][25][1] = 0.19; z_pT_Bin_Borders[17][25][2] = 0.19; z_pT_Bin_Borders[17][25][3] = 0.05;
Phi_h_Bin_Values[17][25][0] =  24; Phi_h_Bin_Values[17][25][1] = 553; Phi_h_Bin_Values[17][25][2] = 12123;
z_pT_Bin_Borders[17][26][0] = 0.23; z_pT_Bin_Borders[17][26][1] = 0.19; z_pT_Bin_Borders[17][26][2] = 0.28; z_pT_Bin_Borders[17][26][3] = 0.19;
Phi_h_Bin_Values[17][26][0] =  24; Phi_h_Bin_Values[17][26][1] = 577; Phi_h_Bin_Values[17][26][2] = 12147;
z_pT_Bin_Borders[17][27][0] = 0.23; z_pT_Bin_Borders[17][27][1] = 0.19; z_pT_Bin_Borders[17][27][2] = 0.37; z_pT_Bin_Borders[17][27][3] = 0.28;
Phi_h_Bin_Values[17][27][0] =  24; Phi_h_Bin_Values[17][27][1] = 601; Phi_h_Bin_Values[17][27][2] = 12171;
z_pT_Bin_Borders[17][28][0] = 0.23; z_pT_Bin_Borders[17][28][1] = 0.19; z_pT_Bin_Borders[17][28][2] = 0.45; z_pT_Bin_Borders[17][28][3] = 0.37;
Phi_h_Bin_Values[17][28][0] =  24; Phi_h_Bin_Values[17][28][1] = 625; Phi_h_Bin_Values[17][28][2] = 12195;
z_pT_Bin_Borders[17][29][0] = 0.23; z_pT_Bin_Borders[17][29][1] = 0.19; z_pT_Bin_Borders[17][29][2] = 0.55; z_pT_Bin_Borders[17][29][3] = 0.45;
Phi_h_Bin_Values[17][29][0] =  1; Phi_h_Bin_Values[17][29][1] = 649; Phi_h_Bin_Values[17][29][2] = 12219;
z_pT_Bin_Borders[17][30][0] = 0.23; z_pT_Bin_Borders[17][30][1] = 0.19; z_pT_Bin_Borders[17][30][2] = 0.73; z_pT_Bin_Borders[17][30][3] = 0.55;
Phi_h_Bin_Values[17][30][0] =  1; Phi_h_Bin_Values[17][30][1] = 650; Phi_h_Bin_Values[17][30][2] = 12220;
z_pT_Bin_Borders[17][31][0] = 10; z_pT_Bin_Borders[17][31][1] = 0.68; z_pT_Bin_Borders[17][31][2] = 0.05; z_pT_Bin_Borders[17][31][3] = 0;
Phi_h_Bin_Values[17][31][0] =  1; Phi_h_Bin_Values[17][31][1] = 651; Phi_h_Bin_Values[17][31][2] = 12221;
z_pT_Bin_Borders[17][32][0] = 10; z_pT_Bin_Borders[17][32][1] = 0.68; z_pT_Bin_Borders[17][32][2] = 0.19; z_pT_Bin_Borders[17][32][3] = 0.05;
Phi_h_Bin_Values[17][32][0] =  1; Phi_h_Bin_Values[17][32][1] = 652; Phi_h_Bin_Values[17][32][2] = 12222;
z_pT_Bin_Borders[17][33][0] = 10; z_pT_Bin_Borders[17][33][1] = 0.68; z_pT_Bin_Borders[17][33][2] = 0.28; z_pT_Bin_Borders[17][33][3] = 0.19;
Phi_h_Bin_Values[17][33][0] =  1; Phi_h_Bin_Values[17][33][1] = 653; Phi_h_Bin_Values[17][33][2] = 12223;
z_pT_Bin_Borders[17][34][0] = 10; z_pT_Bin_Borders[17][34][1] = 0.68; z_pT_Bin_Borders[17][34][2] = 0.37; z_pT_Bin_Borders[17][34][3] = 0.28;
Phi_h_Bin_Values[17][34][0] =  1; Phi_h_Bin_Values[17][34][1] = 654; Phi_h_Bin_Values[17][34][2] = 12224;
z_pT_Bin_Borders[17][35][0] = 10; z_pT_Bin_Borders[17][35][1] = 0.68; z_pT_Bin_Borders[17][35][2] = 0.45; z_pT_Bin_Borders[17][35][3] = 0.37;
Phi_h_Bin_Values[17][35][0] =  1; Phi_h_Bin_Values[17][35][1] = 655; Phi_h_Bin_Values[17][35][2] = 12225;
z_pT_Bin_Borders[17][36][0] = 10; z_pT_Bin_Borders[17][36][1] = 0.68; z_pT_Bin_Borders[17][36][2] = 0.55; z_pT_Bin_Borders[17][36][3] = 0.45;
Phi_h_Bin_Values[17][36][0] =  1; Phi_h_Bin_Values[17][36][1] = 656; Phi_h_Bin_Values[17][36][2] = 12226;
z_pT_Bin_Borders[17][37][0] = 10; z_pT_Bin_Borders[17][37][1] = 0.68; z_pT_Bin_Borders[17][37][2] = 0.73; z_pT_Bin_Borders[17][37][3] = 0.55;
Phi_h_Bin_Values[17][37][0] =  1; Phi_h_Bin_Values[17][37][1] = 657; Phi_h_Bin_Values[17][37][2] = 12227;
z_pT_Bin_Borders[17][38][0] = 10; z_pT_Bin_Borders[17][38][1] = 0.68; z_pT_Bin_Borders[17][38][2] = 10; z_pT_Bin_Borders[17][38][3] = 0.73;
Phi_h_Bin_Values[17][38][0] =  1; Phi_h_Bin_Values[17][38][1] = 658; Phi_h_Bin_Values[17][38][2] = 12228;
z_pT_Bin_Borders[17][39][0] = 0.68; z_pT_Bin_Borders[17][39][1] = 0.44; z_pT_Bin_Borders[17][39][2] = 0.05; z_pT_Bin_Borders[17][39][3] = 0;
Phi_h_Bin_Values[17][39][0] =  1; Phi_h_Bin_Values[17][39][1] = 659; Phi_h_Bin_Values[17][39][2] = 12229;
z_pT_Bin_Borders[17][40][0] = 0.68; z_pT_Bin_Borders[17][40][1] = 0.44; z_pT_Bin_Borders[17][40][2] = 10; z_pT_Bin_Borders[17][40][3] = 0.73;
Phi_h_Bin_Values[17][40][0] =  1; Phi_h_Bin_Values[17][40][1] = 660; Phi_h_Bin_Values[17][40][2] = 12230;
z_pT_Bin_Borders[17][41][0] = 0.44; z_pT_Bin_Borders[17][41][1] = 0.34; z_pT_Bin_Borders[17][41][2] = 0.05; z_pT_Bin_Borders[17][41][3] = 0;
Phi_h_Bin_Values[17][41][0] =  1; Phi_h_Bin_Values[17][41][1] = 661; Phi_h_Bin_Values[17][41][2] = 12231;
z_pT_Bin_Borders[17][42][0] = 0.44; z_pT_Bin_Borders[17][42][1] = 0.34; z_pT_Bin_Borders[17][42][2] = 10; z_pT_Bin_Borders[17][42][3] = 0.73;
Phi_h_Bin_Values[17][42][0] =  1; Phi_h_Bin_Values[17][42][1] = 662; Phi_h_Bin_Values[17][42][2] = 12232;
z_pT_Bin_Borders[17][43][0] = 0.34; z_pT_Bin_Borders[17][43][1] = 0.28; z_pT_Bin_Borders[17][43][2] = 0.05; z_pT_Bin_Borders[17][43][3] = 0;
Phi_h_Bin_Values[17][43][0] =  1; Phi_h_Bin_Values[17][43][1] = 663; Phi_h_Bin_Values[17][43][2] = 12233;
z_pT_Bin_Borders[17][44][0] = 0.34; z_pT_Bin_Borders[17][44][1] = 0.28; z_pT_Bin_Borders[17][44][2] = 10; z_pT_Bin_Borders[17][44][3] = 0.73;
Phi_h_Bin_Values[17][44][0] =  1; Phi_h_Bin_Values[17][44][1] = 664; Phi_h_Bin_Values[17][44][2] = 12234;
z_pT_Bin_Borders[17][45][0] = 0.28; z_pT_Bin_Borders[17][45][1] = 0.23; z_pT_Bin_Borders[17][45][2] = 0.05; z_pT_Bin_Borders[17][45][3] = 0;
Phi_h_Bin_Values[17][45][0] =  1; Phi_h_Bin_Values[17][45][1] = 665; Phi_h_Bin_Values[17][45][2] = 12235;
z_pT_Bin_Borders[17][46][0] = 0.28; z_pT_Bin_Borders[17][46][1] = 0.23; z_pT_Bin_Borders[17][46][2] = 10; z_pT_Bin_Borders[17][46][3] = 0.73;
Phi_h_Bin_Values[17][46][0] =  1; Phi_h_Bin_Values[17][46][1] = 666; Phi_h_Bin_Values[17][46][2] = 12236;
z_pT_Bin_Borders[17][47][0] = 0.23; z_pT_Bin_Borders[17][47][1] = 0.19; z_pT_Bin_Borders[17][47][2] = 0.05; z_pT_Bin_Borders[17][47][3] = 0;
Phi_h_Bin_Values[17][47][0] =  1; Phi_h_Bin_Values[17][47][1] = 667; Phi_h_Bin_Values[17][47][2] = 12237;
z_pT_Bin_Borders[17][48][0] = 0.23; z_pT_Bin_Borders[17][48][1] = 0.19; z_pT_Bin_Borders[17][48][2] = 10; z_pT_Bin_Borders[17][48][3] = 0.73;
Phi_h_Bin_Values[17][48][0] =  1; Phi_h_Bin_Values[17][48][1] = 668; Phi_h_Bin_Values[17][48][2] = 12238;
z_pT_Bin_Borders[17][49][0] = 0.19; z_pT_Bin_Borders[17][49][1] = 0; z_pT_Bin_Borders[17][49][2] = 0.05; z_pT_Bin_Borders[17][49][3] = 0;
Phi_h_Bin_Values[17][49][0] =  1; Phi_h_Bin_Values[17][49][1] = 669; Phi_h_Bin_Values[17][49][2] = 12239;
z_pT_Bin_Borders[17][50][0] = 0.19; z_pT_Bin_Borders[17][50][1] = 0; z_pT_Bin_Borders[17][50][2] = 0.19; z_pT_Bin_Borders[17][50][3] = 0.05;
Phi_h_Bin_Values[17][50][0] =  1; Phi_h_Bin_Values[17][50][1] = 670; Phi_h_Bin_Values[17][50][2] = 12240;
z_pT_Bin_Borders[17][51][0] = 0.19; z_pT_Bin_Borders[17][51][1] = 0; z_pT_Bin_Borders[17][51][2] = 0.28; z_pT_Bin_Borders[17][51][3] = 0.19;
Phi_h_Bin_Values[17][51][0] =  1; Phi_h_Bin_Values[17][51][1] = 671; Phi_h_Bin_Values[17][51][2] = 12241;
z_pT_Bin_Borders[17][52][0] = 0.19; z_pT_Bin_Borders[17][52][1] = 0; z_pT_Bin_Borders[17][52][2] = 0.37; z_pT_Bin_Borders[17][52][3] = 0.28;
Phi_h_Bin_Values[17][52][0] =  1; Phi_h_Bin_Values[17][52][1] = 672; Phi_h_Bin_Values[17][52][2] = 12242;
z_pT_Bin_Borders[17][53][0] = 0.19; z_pT_Bin_Borders[17][53][1] = 0; z_pT_Bin_Borders[17][53][2] = 0.45; z_pT_Bin_Borders[17][53][3] = 0.37;
Phi_h_Bin_Values[17][53][0] =  1; Phi_h_Bin_Values[17][53][1] = 673; Phi_h_Bin_Values[17][53][2] = 12243;
z_pT_Bin_Borders[17][54][0] = 0.19; z_pT_Bin_Borders[17][54][1] = 0; z_pT_Bin_Borders[17][54][2] = 0.55; z_pT_Bin_Borders[17][54][3] = 0.45;
Phi_h_Bin_Values[17][54][0] =  1; Phi_h_Bin_Values[17][54][1] = 674; Phi_h_Bin_Values[17][54][2] = 12244;
z_pT_Bin_Borders[17][55][0] = 0.19; z_pT_Bin_Borders[17][55][1] = 0; z_pT_Bin_Borders[17][55][2] = 0.73; z_pT_Bin_Borders[17][55][3] = 0.55;
Phi_h_Bin_Values[17][55][0] =  1; Phi_h_Bin_Values[17][55][1] = 675; Phi_h_Bin_Values[17][55][2] = 12245;
z_pT_Bin_Borders[17][56][0] = 0.19; z_pT_Bin_Borders[17][56][1] = 0; z_pT_Bin_Borders[17][56][2] = 10; z_pT_Bin_Borders[17][56][3] = 0.73;
Phi_h_Bin_Values[17][56][0] =  1; Phi_h_Bin_Values[17][56][1] = 676; Phi_h_Bin_Values[17][56][2] = 12246;
Phi_h_Bin_Values[18][1][0] = 1; Phi_h_Bin_Values[18][1][1] = 1; Phi_h_Bin_Values[18][1][2] = 12247;
Phi_h_Bin_Values[19][1][0] = 1; Phi_h_Bin_Values[19][1][1] = 1; Phi_h_Bin_Values[19][1][2] = 12248;
Phi_h_Bin_Values[20][1][0] = 1; Phi_h_Bin_Values[20][1][1] = 1; Phi_h_Bin_Values[20][1][2] = 12249;
Phi_h_Bin_Values[21][1][0] = 1; Phi_h_Bin_Values[21][1][1] = 1; Phi_h_Bin_Values[21][1][2] = 12250;
Phi_h_Bin_Values[22][1][0] = 1; Phi_h_Bin_Values[22][1][1] = 1; Phi_h_Bin_Values[22][1][2] = 12251;
Phi_h_Bin_Values[23][1][0] = 1; Phi_h_Bin_Values[23][1][1] = 1; Phi_h_Bin_Values[23][1][2] = 12252;
Phi_h_Bin_Values[24][1][0] = 1; Phi_h_Bin_Values[24][1][1] = 1; Phi_h_Bin_Values[24][1][2] = 12253;
Phi_h_Bin_Values[25][1][0] = 1; Phi_h_Bin_Values[25][1][1] = 1; Phi_h_Bin_Values[25][1][2] = 12254;
Phi_h_Bin_Values[26][1][0] = 1; Phi_h_Bin_Values[26][1][1] = 1; Phi_h_Bin_Values[26][1][2] = 12255;
Phi_h_Bin_Values[27][1][0] = 1; Phi_h_Bin_Values[27][1][1] = 1; Phi_h_Bin_Values[27][1][2] = 12256;
Phi_h_Bin_Values[28][1][0] = 1; Phi_h_Bin_Values[28][1][1] = 1; Phi_h_Bin_Values[28][1][2] = 12257;
Phi_h_Bin_Values[29][1][0] = 1; Phi_h_Bin_Values[29][1][1] = 1; Phi_h_Bin_Values[29][1][2] = 12258;
Phi_h_Bin_Values[30][1][0] = 1; Phi_h_Bin_Values[30][1][1] = 1; Phi_h_Bin_Values[30][1][2] = 12259;
Phi_h_Bin_Values[31][1][0] = 1; Phi_h_Bin_Values[31][1][1] = 1; Phi_h_Bin_Values[31][1][2] = 12260;
Phi_h_Bin_Values[32][1][0] = 1; Phi_h_Bin_Values[32][1][1] = 1; Phi_h_Bin_Values[32][1][2] = 12261;
Phi_h_Bin_Values[33][1][0] = 1; Phi_h_Bin_Values[33][1][1] = 1; Phi_h_Bin_Values[33][1][2] = 12262;
Phi_h_Bin_Values[34][1][0] = 1; Phi_h_Bin_Values[34][1][1] = 1; Phi_h_Bin_Values[34][1][2] = 12263;
Phi_h_Bin_Values[35][1][0] = 1; Phi_h_Bin_Values[35][1][1] = 1; Phi_h_Bin_Values[35][1][2] = 12264;
Phi_h_Bin_Values[36][1][0] = 1; Phi_h_Bin_Values[36][1][1] = 1; Phi_h_Bin_Values[36][1][2] = 12265;
Phi_h_Bin_Values[37][1][0] = 1; Phi_h_Bin_Values[37][1][1] = 1; Phi_h_Bin_Values[37][1][2] = 12266;
Phi_h_Bin_Values[38][1][0] = 1; Phi_h_Bin_Values[38][1][1] = 1; Phi_h_Bin_Values[38][1][2] = 12267;
Phi_h_Bin_Values[39][1][0] = 1; Phi_h_Bin_Values[39][1][1] = 1; Phi_h_Bin_Values[39][1][2] = 12268;
auto Find_z_pT_Bin = [&](int Q2_y_Bin_Num_Value, double Z_Value, double PT_Value){
    int z_pT_Bin_Max = 1;
    // 'z_pT_Bin_Max' Includes both the main kinematic bins AND the overflow/migration bins
    if(Q2_y_Bin_Num_Value ==  1){z_pT_Bin_Max = 63;}
    if(Q2_y_Bin_Num_Value ==  2){z_pT_Bin_Max = 64;}
    if(Q2_y_Bin_Num_Value ==  3){z_pT_Bin_Max = 56;}
    if(Q2_y_Bin_Num_Value ==  4){z_pT_Bin_Max = 64;}
    if(Q2_y_Bin_Num_Value ==  5){z_pT_Bin_Max = 64;}
    if(Q2_y_Bin_Num_Value ==  6){z_pT_Bin_Max = 56;}
    if(Q2_y_Bin_Num_Value ==  7){z_pT_Bin_Max = 64;}
    if(Q2_y_Bin_Num_Value ==  8){z_pT_Bin_Max = 63;}
    if(Q2_y_Bin_Num_Value ==  9){z_pT_Bin_Max = 63;}
    if(Q2_y_Bin_Num_Value == 10){z_pT_Bin_Max = 64;}
    if(Q2_y_Bin_Num_Value == 11){z_pT_Bin_Max = 49;}
    if(Q2_y_Bin_Num_Value == 12){z_pT_Bin_Max = 49;}
    if(Q2_y_Bin_Num_Value == 13){z_pT_Bin_Max = 56;}
    if(Q2_y_Bin_Num_Value == 14){z_pT_Bin_Max = 64;}
    if(Q2_y_Bin_Num_Value == 15){z_pT_Bin_Max = 49;}
    if(Q2_y_Bin_Num_Value == 16){z_pT_Bin_Max = 56;}
    if(Q2_y_Bin_Num_Value == 17){z_pT_Bin_Max = 56;}
    
    if(Q2_y_Bin_Num_Value < 1 || Q2_y_Bin_Num_Value > 17){return 1;} // The overflow Q2-y bins do not have defined z-pT bins
    double z_max  = 0;
    double z_min  = 0;
    double pT_max = 0;
    double pT_min = 0;
    for(int Z_PT_BIN = 1; Z_PT_BIN < (z_pT_Bin_Max + 1); Z_PT_BIN++){
        z_max  = z_pT_Bin_Borders[Q2_y_Bin_Num_Value][Z_PT_BIN][0];
        z_min  = z_pT_Bin_Borders[Q2_y_Bin_Num_Value][Z_PT_BIN][1];
        pT_max = z_pT_Bin_Borders[Q2_y_Bin_Num_Value][Z_PT_BIN][2];
        pT_min = z_pT_Bin_Borders[Q2_y_Bin_Num_Value][Z_PT_BIN][3];
        if(((Z_Value <= z_max) && (Z_Value > z_min)) && ((PT_Value <= pT_max) && (PT_Value > pT_min))){
            return Z_PT_BIN;
            break;
        }
    }
    return 0; // ERROR: Events should not return 0 (missed all bin definitions)
};
auto Find_phi_h_Bin = [&](int Q2_y_Bin_Num_Value, int Z_PT_Bin_Num_Value, double PHI_H_Value){
    int Num_PHI_BINS = Phi_h_Bin_Values[Q2_y_Bin_Num_Value][Z_PT_Bin_Num_Value][0];
    if(Num_PHI_BINS == 1){return Num_PHI_BINS;}
    else{
        double bin_size = 360/Num_PHI_BINS;
        int PHI_BIN     = (PHI_H_Value/bin_size) + 1;
        if(PHI_H_Value == 360){PHI_BIN = Num_PHI_BINS;} // Include 360 in the last phi_h bin
        return PHI_BIN;
    }
    return -1; // ERROR: Events should not return -1
};
"""










###########################################################################################################################################################################
###########################################################################################################################################################################
###########################################################################################################################################################################
###########################################################################################################################################################################
###########################################################################################################################################################################










Correction_Code_Full_In = """
auto dppC = [&](float Px, float Py, float Pz, int sec, int ivec, int corON){

    // corON == 0 --> DOES NOT apply the momentum corrections (i.e., turns the corrections 'off')
    // corON == 1 --> Applies the momentum corrections for the experimental (real) data
    // corON == 2 --> Applies the momentum corrections for the Monte Carlo (simulated) data

    if(corON == 0){ // Momentum Corrections are OFF
        double dp = 0;
        return dp;
    }

    else{ // corON != 0 --> Applies the momentum corrections (i.e., turns the corrections 'on')
        // ivec = 0 --> Electron Corrections
        // ivec = 1 --> π+ Corrections
        // ivec = 2 --> π- Corrections
        // ivec = 3 --> Proton Corrections

        // Momentum Magnitude
        double pp = sqrt(Px*Px + Py*Py + Pz*Pz);

        // Initializing the correction factor
        double dp = 0;

        // Defining Phi Angle
        double Phi = (180/3.1415926)*atan2(Py, Px);

        // (Initial) Shift of the Phi Angle (done to realign sectors whose data is separated when plotted from ±180˚)
        if(((sec == 4 || sec == 3) && Phi < 0) || (sec > 4 && Phi < 90)){
            Phi += 360;
        }

        // Getting Local Phi Angle
        double PhiLocal = Phi - (sec - 1)*60;

        // Applying Shift Functions to Phi Angles (local shifted phi = phi)
        double phi = PhiLocal;

        // For Electron Shift
        if(ivec == 0){
            phi = PhiLocal - 30/pp;
        }

        // For π+ Pion/Proton Shift
        if(ivec == 1 || ivec == 3){
            phi = PhiLocal + (32/(pp-0.05));
        }

        // For π- Pion Shift
        if(ivec == 2){
            phi = PhiLocal - (32/(pp-0.05));
        }

        if(corON == 2){ // Monte Carlo Simulated Corrections
            // Not Sector or Angle dependent (as of 3-21-2023)

            // Both particles were corrected at the same time using Extra_Name = "Multi_Dimension_Unfold_V1_"
            // Used ∆P = GEN - REC so the other particle does not affect how much the correction is needed
            if(ivec == 0){ // Electron Corrections
                // // For MC REC (Unsmeared) ∆P(Electron) Vs Momentum Correction Equation:
                // dp = (-8.2310e-04)*pp*pp + (9.0877e-03)*pp + (-1.5853e-02);

                // From Normal ∆P corrections:
                // For MC REC (Unsmeared) ∆P(Electron) Vs Momentum Correction Equation:
                dp = (-6.9141e-04)*pp*pp + (5.5852e-03)*pp + (-5.2144e-03);
                // Corrected after the pion

            }
            if(ivec == 1){ // Pi+ Pion Corrections
                // For MC REC (Unsmeared) ∆P(Pi+ Pion) Vs Momentum Correction Equation:
                dp = (-7.3067e-05)*pp*pp + (-8.1215e-06)*pp + (4.2144e-03);

                // From Normal ∆P corrections:
                // For MC REC (Unsmeared) ∆P(Pi+ Pion) Vs Momentum Correction Equation:
                dp = (-1.8752e-03)*pp*pp + (1.0679e-02)*pp +  (2.5653e-03);
                // Corrected before the electron

                // Cannot use iterative corrections as of 7-8-2023 due to the corrections being applied automatically so that dp is no longer a function of the same pp
                // dp = dp + (-1.8949e-03)*pp*pp + (9.3060e-03)*pp + (-9.7925e-03);
            }

            return dp/pp;
        }
        else{

            //////////////////////////////////////////////////////////////////////////////////
            //==============================================================================//
            //==========//==========//     Electron Corrections     //==========//==========//
            //==============================================================================//
            //////////////////////////////////////////////////////////////////////////////////

            if(ivec == 0){
                if(sec == 1){
                    dp = ((-4.3303e-06)*phi*phi +  (1.1006e-04)*phi + (-5.7235e-04))*pp*pp +  ((3.2555e-05)*phi*phi +  (-0.0014559)*phi +   (0.0014878))*pp + ((-1.9577e-05)*phi*phi +   (0.0017996)*phi + (0.025963));
                }
                if(sec == 2){
                    dp = ((-9.8045e-07)*phi*phi +  (6.7395e-05)*phi + (-4.6757e-05))*pp*pp + ((-1.4958e-05)*phi*phi +  (-0.0011191)*phi +  (-0.0025143))*pp +  ((1.2699e-04)*phi*phi +   (0.0033121)*phi + (0.020819));
                }
                if(sec == 3){
                    dp = ((-5.9459e-07)*phi*phi + (-2.8289e-05)*phi + (-4.3541e-04))*pp*pp + ((-1.5025e-05)*phi*phi +  (5.7730e-04)*phi +  (-0.0077582))*pp +  ((7.3348e-05)*phi*phi +   (-0.001102)*phi + (0.057052));
                }
                if(sec == 4){
                    dp = ((-2.2714e-06)*phi*phi + (-3.0360e-05)*phi + (-8.9322e-04))*pp*pp +  ((2.9737e-05)*phi*phi +  (5.1142e-04)*phi +   (0.0045641))*pp + ((-1.0582e-04)*phi*phi + (-5.6852e-04)*phi + (0.027506));
                }
                if(sec == 5){
                    dp = ((-1.1490e-06)*phi*phi + (-6.2147e-06)*phi + (-4.7235e-04))*pp*pp +  ((3.7039e-06)*phi*phi + (-1.5943e-04)*phi + (-8.5238e-04))*pp +  ((4.4069e-05)*phi*phi +   (0.0014152)*phi + (0.031933));
                }
                if(sec == 6){
                    dp =  ((1.1076e-06)*phi*phi +  (4.0156e-05)*phi + (-1.6341e-04))*pp*pp + ((-2.8613e-05)*phi*phi + (-5.1861e-04)*phi +  (-0.0056437))*pp +  ((1.2419e-04)*phi*phi +  (4.9084e-04)*phi + (0.049976));
                }
            }

            //////////////////////////////////////////////////////////////////////////////////
            //==============================================================================//
            //==========//==========//  Electron Corrections (End)  //==========//==========//
            //==============================================================================//
            //////////////////////////////////////////////////////////////////////////////////


            /////////////////////////////////////////////////////////////////////////////////
            //=============================================================================//
            //==========//==========//     π+ Pion Corrections     //==========//==========//
            //=============================================================================//
            /////////////////////////////////////////////////////////////////////////////////

            if(ivec == 1){
                if(sec == 1){
                    dp =      ((-5.4904e-07)*phi*phi + (-1.4436e-05)*phi +  (3.1534e-04))*pp*pp +  ((3.8231e-06)*phi*phi +  (3.6582e-04)*phi +  (-0.0046759))*pp + ((-5.4913e-06)*phi*phi + (-4.0157e-04)*phi + (0.010767));
                    dp = dp +  ((6.1103e-07)*phi*phi +  (5.5291e-06)*phi + (-1.9120e-04))*pp*pp + ((-3.2300e-06)*phi*phi +  (1.5377e-05)*phi +  (7.5279e-04))*pp +  ((2.1434e-06)*phi*phi + (-6.9572e-06)*phi + (-7.9333e-05));
                    dp = dp + ((-1.3049e-06)*phi*phi +  (1.1295e-05)*phi +  (4.5797e-04))*pp*pp +  ((9.3122e-06)*phi*phi + (-5.1074e-05)*phi +  (-0.0030757))*pp + ((-1.3102e-05)*phi*phi +  (2.2153e-05)*phi + (0.0040938));
                }
                if(sec == 2){
                    dp =      ((-1.0087e-06)*phi*phi +  (2.1319e-05)*phi +  (7.8641e-04))*pp*pp +  ((6.7485e-06)*phi*phi +  (7.3716e-05)*phi +  (-0.0094591))*pp + ((-1.1820e-05)*phi*phi + (-3.8103e-04)*phi + (0.018936));
                    dp = dp +  ((8.8155e-07)*phi*phi + (-2.8257e-06)*phi + (-2.6729e-04))*pp*pp + ((-5.4499e-06)*phi*phi +  (3.8397e-05)*phi +   (0.0015914))*pp +  ((6.8926e-06)*phi*phi + (-5.9386e-05)*phi + (-0.0021749));
                    dp = dp + ((-2.0147e-07)*phi*phi +  (1.1061e-05)*phi +  (3.8827e-04))*pp*pp +  ((4.9294e-07)*phi*phi + (-6.0257e-05)*phi +  (-0.0022087))*pp +  ((9.8548e-07)*phi*phi +  (5.9047e-05)*phi + (0.0022905));
                }
                if(sec == 3){
                    dp =       ((8.6722e-08)*phi*phi + (-1.7975e-05)*phi +  (4.8118e-05))*pp*pp +  ((2.6273e-06)*phi*phi +  (3.1453e-05)*phi +  (-0.0015943))*pp + ((-6.4463e-06)*phi*phi + (-5.8990e-05)*phi + (0.0041703));
                    dp = dp +  ((9.6317e-07)*phi*phi + (-1.7659e-06)*phi + (-8.8318e-05))*pp*pp + ((-5.1346e-06)*phi*phi +  (8.3318e-06)*phi +  (3.7723e-04))*pp +  ((3.9548e-06)*phi*phi + (-6.9614e-05)*phi + (2.1393e-04));
                    dp = dp +  ((5.6438e-07)*phi*phi +  (8.1678e-06)*phi + (-9.4406e-05))*pp*pp + ((-3.9074e-06)*phi*phi + (-6.5174e-05)*phi +  (5.4218e-04))*pp +  ((6.3198e-06)*phi*phi +  (1.0611e-04)*phi + (-4.5749e-04));
                }
                if(sec == 4){
                    dp =       ((4.3406e-07)*phi*phi + (-4.9036e-06)*phi +  (2.3064e-04))*pp*pp +  ((1.3624e-06)*phi*phi +  (3.2907e-05)*phi +  (-0.0034872))*pp + ((-5.1017e-06)*phi*phi +  (2.4593e-05)*phi + (0.0092479));
                    dp = dp +  ((6.0218e-07)*phi*phi + (-1.4383e-05)*phi + (-3.1999e-05))*pp*pp + ((-1.1243e-06)*phi*phi +  (9.3884e-05)*phi + (-4.1985e-04))*pp + ((-1.8808e-06)*phi*phi + (-1.2222e-04)*phi + (0.0014037));
                    dp = dp + ((-2.5490e-07)*phi*phi + (-8.5120e-07)*phi +  (7.9109e-05))*pp*pp +  ((2.5879e-06)*phi*phi +  (8.6108e-06)*phi + (-5.1533e-04))*pp + ((-4.4521e-06)*phi*phi + (-1.7012e-05)*phi + (7.4848e-04));
                }
                if(sec == 5){
                    dp =       ((2.4292e-07)*phi*phi +  (8.8741e-06)*phi +  (2.9482e-04))*pp*pp +  ((3.7229e-06)*phi*phi +  (7.3215e-06)*phi +  (-0.0050685))*pp + ((-1.1974e-05)*phi*phi + (-1.3043e-04)*phi + (0.0078836));
                    dp = dp +  ((1.0867e-06)*phi*phi + (-7.7630e-07)*phi + (-4.4930e-05))*pp*pp + ((-5.6564e-06)*phi*phi + (-1.3417e-05)*phi +  (2.5224e-04))*pp +  ((6.8460e-06)*phi*phi +  (9.0495e-05)*phi + (-4.6587e-04));
                    dp = dp +  ((8.5720e-07)*phi*phi + (-6.7464e-06)*phi + (-4.0944e-05))*pp*pp + ((-4.7370e-06)*phi*phi +  (5.8808e-05)*phi +  (1.9047e-04))*pp +  ((5.7404e-06)*phi*phi + (-1.1105e-04)*phi + (-1.9392e-04));
                }
                if(sec == 6){
                    dp =       ((2.1191e-06)*phi*phi + (-3.3710e-05)*phi +  (2.5741e-04))*pp*pp + ((-1.2915e-05)*phi*phi +  (2.3753e-04)*phi + (-2.6882e-04))*pp +  ((2.2676e-05)*phi*phi + (-2.3115e-04)*phi + (-0.001283));
                    dp = dp +  ((6.0270e-07)*phi*phi + (-6.8200e-06)*phi +  (1.3103e-04))*pp*pp + ((-1.8745e-06)*phi*phi +  (3.8646e-05)*phi + (-8.8056e-04))*pp +  ((2.0885e-06)*phi*phi + (-3.4932e-05)*phi + (4.5895e-04));
                    dp = dp +  ((4.7349e-08)*phi*phi + (-5.7528e-06)*phi + (-3.4097e-06))*pp*pp +  ((1.7731e-06)*phi*phi +  (3.5865e-05)*phi + (-5.7881e-04))*pp + ((-9.7008e-06)*phi*phi + (-4.1836e-05)*phi + (0.0035403));
                }
            }

            /////////////////////////////////////////////////////////////////////////////////
            //=============================================================================//
            //==========//==========//  π+ Pion Corrections (End)  //==========//==========//
            //=============================================================================//
            /////////////////////////////////////////////////////////////////////////////////


            /////////////////////////////////////////////////////////////////////////////////
            //=============================================================================//
            //==========//==========//     π- Pion Corrections     //==========//==========//
            //=============================================================================//
            /////////////////////////////////////////////////////////////////////////////////

            if(ivec == 2){
                if(sec == 1){
                    dp = ((-4.0192658422317425e-06)*phi*phi - (2.660222128967742e-05)*phi + 0.004774434682983547)*pp*pp;
                    dp = dp + ((1.9549520962477972e-05)*phi*phi - 0.0002456062756770577*phi - 0.03787692408323466)*pp; 
                    dp = dp + (-2.128953094937459e-05)*phi*phi + 0.0002461708852239913*phi + 0.08060704449822174 - 0.01;
                }
                if(sec == 2){
                    dp = ((1.193010521758372e-05)*phi*phi - (5.996221756031922e-05)*phi + 0.0009093437955814359)*pp*pp;
                    dp = dp + ((-4.89113824430594e-05)*phi*phi + 0.00021676479488147118*phi - 0.01861892053916726)*pp;  
                    dp = dp + (4.446394152208071e-05)*phi*phi - (3.6592784167335244e-05)*phi + 0.05498710249944096 - 0.01;
                }
                if(sec == 3){
                    dp = ((-1.6596664895992133e-07)*phi*phi + (6.317189710683516e-05)*phi + 0.0016364212312654086)*pp*pp;
                    dp = dp + ((-2.898409777520318e-07)*phi*phi - 0.00014531513577533802*phi - 0.025456145839203827)*pp;  
                    dp = dp + (2.6432552410603506e-06)*phi*phi + 0.00018447151306275443*phi + 0.06442602664627255 - 0.01;
                }
                if(sec == 4){
                    dp = ((2.4035259647558634e-07)*phi*phi - (8.649647351491232e-06)*phi + 0.004558993439848128)*pp*pp;
                    dp = dp + ((-5.981498144060984e-06)*phi*phi + 0.00010582131454222416*phi - 0.033572004651981686)*pp;  
                    dp = dp + (8.70140266889548e-06)*phi*phi - 0.00020137414379966883*phi + 0.07258774523336173 - 0.01;   
                }
                if(sec == 5){
                    dp = ((2.5817024702834863e-06)*phi*phi + 0.00010132810066914441*phi + 0.003397314538804711)*pp*pp;
                    dp = dp + ((-1.5116941263931812e-05)*phi*phi - 0.00040679799541839254*phi - 0.028144285760769876)*pp;  
                    dp = dp + (1.4701931057951464e-05)*phi*phi + 0.0002426350390593454*phi + 0.06781682510174941 - 0.01;
                }
                if(sec == 6){
                    dp = ((-8.196823669099362e-07)*phi*phi - (5.280412421933636e-05)*phi + 0.0018457238328451137)*pp*pp;
                    dp = dp + ((5.2675062282094536e-06)*phi*phi + 0.0001515803461044587*phi - 0.02294371578470564)*pp;  
                    dp = dp + (-9.459454671739747e-06)*phi*phi - 0.0002389523716779765*phi + 0.06428970810739926 - 0.01;
                }
            }

            /////////////////////////////////////////////////////////////////////////////////
            //=============================================================================//
            //==========//==========//  π- Pion Corrections (End)  //==========//==========//
            //=============================================================================//
            /////////////////////////////////////////////////////////////////////////////////


            //////////////////////////////////////////////////////////////////////////////////
            //==============================================================================//
            //==========//==========//      Proton Corrections      //==========//==========//
            //==============================================================================//
            //////////////////////////////////////////////////////////////////////////////////

            if(ivec == 3){
                if(sec == 1){
                    dp = (5.415e-04)*pp*pp + (-1.0262e-02)*pp + (7.78075e-03);
                    dp = dp + ((1.2129e-04)*pp*pp + (1.5373e-04)*pp + (-2.7084e-04));
                }
                if(sec == 2){
                    dp = (-9.5439e-04)*pp*pp + (-2.86273e-03)*pp + (3.38149e-03);
                    dp = dp + ((-1.6890e-03)*pp*pp + (4.3744e-03)*pp + (-2.1218e-03));
                }
                if(sec == 3){
                    dp = (-5.5541e-04)*pp*pp + (-7.69739e-03)*pp + (5.7692e-03);
                    dp = dp + ((7.6422e-04)*pp*pp + (-1.5425e-03)*pp + (5.4255e-04));
                }
                if(sec == 4){
                    dp = (-1.944e-04)*pp*pp + (-5.77104e-03)*pp + (3.42399e-03);
                    dp = dp + ((1.1174e-03)*pp*pp + (-3.2747e-03)*pp + (2.3687e-03));
                }
                if(sec == 5){
                    dp = (1.54009e-03)*pp*pp + (-1.69437e-02)*pp + (1.04656e-02);
                    dp = dp + ((-2.1067e-04)*pp*pp + (1.2266e-03)*pp + (-1.0553e-03));
                }
                if(sec == 6){
                    dp = (2.38182e-03)*pp*pp + (-2.07301e-02)*pp + (1.72325e-02);
                    dp = dp + ((-3.6002e-04)*pp*pp + (8.9582e-04)*pp + (-1.0093e-03));
                }
            }

            //////////////////////////////////////////////////////////////////////////////////
            //==============================================================================//
            //==========//==========//   Proton Corrections (End)   //==========//==========//
            //==============================================================================//
            //////////////////////////////////////////////////////////////////////////////////

            return dp/pp;
        }
    }
};"""










###########################################################################################################################################################################
###########################################################################################################################################################################
###########################################################################################################################################################################
###########################################################################################################################################################################
###########################################################################################################################################################################










Rotation_Matrix = """
/////////////////////////////////////////////          Rotation Matrix          /////////////////////////////////////////////

auto Rot_Matrix = [&](TLorentzVector vector, int Lab2CM_or_CM2Lab, double Theta_Rot, double Phi_Rot){
    double Rot_X1 = vector.X();
    double Rot_Y1 = vector.Y();
    double Rot_Z1 = vector.Z();

    double Rot_X = Rot_X1;
    double Rot_Y = Rot_Y1;
    double Rot_Z = Rot_Z1;

    // Lab2CM_or_CM2Lab is a parameter which determines if you rotating from the lab frame to the CM frame, or if you are rotating back in the opposite direction
    // Lab2CM_or_CM2Lab = -1 gives a rotation to the CM frame (from the lab frame)
    // Lab2CM_or_CM2Lab = +1 gives a rotation to the lab frame (from the CM frame)

    Theta_Rot = -1*Theta_Rot;   // Always give the angle of rotation Theta as the value given by .Theta()
                                // This subroutine will handle the fact that the matrix rotation wants the negative of the angle of rotation

    // Rotation to Lab Frame
    if(Lab2CM_or_CM2Lab == -1){
        Rot_X = Rot_X1*TMath::Cos(Theta_Rot)*TMath::Cos(Phi_Rot) - Rot_Z1*TMath::Sin(Theta_Rot) + Rot_Y1*TMath::Cos(Theta_Rot)*TMath::Sin(Phi_Rot);
        Rot_Y = Rot_Y1*TMath::Cos(Phi_Rot) - Rot_X1*TMath::Sin(Phi_Rot);
        Rot_Z = Rot_Z1*TMath::Cos(Theta_Rot) + Rot_X1*TMath::Cos(Phi_Rot)*TMath::Sin(Theta_Rot) + Rot_Y1*TMath::Sin(Theta_Rot)*TMath::Sin(Phi_Rot);
    }

    // Rotation to CM Frame
    if(Lab2CM_or_CM2Lab == 1){
        Rot_X = Rot_X1*TMath::Cos(Theta_Rot)*TMath::Cos(Phi_Rot) + Rot_Z1*TMath::Cos(Phi_Rot)*TMath::Sin(Theta_Rot) - Rot_Y1*TMath::Sin(Phi_Rot);
        Rot_Y = Rot_Y1*TMath::Cos(Phi_Rot) + Rot_X1*TMath::Sin(Phi_Rot)*TMath::Cos(Theta_Rot) + Rot_Z1*TMath::Sin(Theta_Rot)*TMath::Sin(Phi_Rot);
        Rot_Z = Rot_Z1*TMath::Cos(Theta_Rot) - Rot_X1*TMath::Sin(Theta_Rot);
    }

    TLorentzVector vector_Rotated(Rot_X, Rot_Y, Rot_Z, vector.E());

    return vector_Rotated;

};

/////////////////////////////////////////////          (End of) Rotation Matrix          /////////////////////////////////////////////"""









###########################################################################################################################################################################
###########################################################################################################################################################################
###########################################################################################################################################################################
###########################################################################################################################################################################
###########################################################################################################################################################################









# Up-to-date as of: 2/12/2024
def smearing_function_SF(smear_factor=0.75, Use_Pass_2_Function=False):
    if(Use_Pass_2_Function):
        smearing_function = "".join(["""
        //=======================================================================//
        //=================// Sigma Smearing Factor (Pass 2) //=================//
        //=======================================================================//
        auto smear_func = [&](TLorentzVector V4, int ivec){
            // // True generated values (i.e., values of the unsmeared TLorentzVector)
            // double M_rec   = V4.M();
            // double P_rec   = V4.P();
            // double Th_rec  = V4.Theta();
            // double Phi_rec = V4.Phi();
            // 
            // double Smear_SF_Theta = 0;
            // if(ivec == 0){ // Electron
            //     Smear_SF_Theta       = (-3.1431e-05)*(TMath::RadToDeg()*Th_rec)*(TMath::RadToDeg()*Th_rec) + (1.0284e-03)*(TMath::RadToDeg()*Th_rec) + (-4.0027e-03);
            // }
            // if(ivec == 1){ // Pi+ Pion
            //     Smear_SF_Theta       = (-1.6434e-06)*(TMath::RadToDeg()*Th_rec)*(TMath::RadToDeg()*Th_rec) + (5.1530e-04)*(TMath::RadToDeg()*Th_rec) + (-4.4158e-03);
            // }
            // // Calculate resolutions
            // double smear_factor = """, str(smear_factor), """;
            // double P_new_rec    = P_rec   +   (P_rec)*Smear_SF_Theta*smear_factor*(gRandom->Gaus(0,1));
            // double Th_new_rec   = Th_rec  +  (Th_rec)*Smear_SF_Theta*smear_factor*(gRandom->Gaus(0,1));
            // double Phi_new_rec  = Phi_rec + (Phi_rec)*Smear_SF_Theta*smear_factor*(gRandom->Gaus(0,1));
            // Th_new_rec  = Th_rec;
            // Phi_new_rec = Phi_rec;
            
            // double Extra_Smear_SF_Theta = 0;
            // if(ivec == 1){ // Pi+ Pion
            //     Extra_Smear_SF_Theta = (2.2747e-06)*(TMath::RadToDeg()*Th_rec)*(TMath::RadToDeg()*Th_rec) + (3.0985e-04)*(TMath::RadToDeg()*Th_rec) + (-5.1206e-03);
            //     P_new_rec      = P_new_rec   +   (P_new_rec)*Extra_Smear_SF_Theta*smear_factor*(gRandom->Gaus(0,1));
            //     // Th_new_rec  = Th_new_rec  +  (Th_new_rec)*Extra_Smear_SF_Theta*smear_factor*(gRandom->Gaus(0,1));
            //     // Phi_new_rec = Phi_new_rec + (Phi_new_rec)*Extra_Smear_SF_Theta*smear_factor*(gRandom->Gaus(0,1));
            // }
            
            // Making the smeared TLorentzVector:
            TLorentzVector V4_smear(V4.X(), V4.Y(), V4.Z(), V4.E());
            // V4_smear.SetE(TMath::Sqrt(P_new_rec*P_new_rec + M_rec*M_rec));
            // V4_smear.SetRho(   P_new_rec);
            // V4_smear.SetTheta(Th_new_rec);
            // V4_smear.SetPhi( Phi_new_rec);
            return V4_smear;
        };"""])
    else:
        smearing_function = "".join(["""
        //=======================================================================//
        //=================//      Sigma Smearing Factor      //=================//
        //=======================================================================//
        auto smear_func = [&](TLorentzVector V4, int ivec){
            // True generated values (i.e., values of the unsmeared TLorentzVector)
            double M_rec   = V4.M();
            double P_rec   = V4.P();
            double Th_rec  = V4.Theta();
            double Phi_rec = V4.Phi();
            
            double Smear_SF_Theta = 0;
            if(ivec == 0){ // Electron
                // Smear_SF_Theta    = (-2.0472e-05)*(TMath::RadToDeg()*Th_rec)*(TMath::RadToDeg()*Th_rec) + (8.7962e-04)*(TMath::RadToDeg()*Th_rec) + (-5.8595e-03);
                Smear_SF_Theta       = (-3.1431e-05)*(TMath::RadToDeg()*Th_rec)*(TMath::RadToDeg()*Th_rec) + (1.0284e-03)*(TMath::RadToDeg()*Th_rec) + (-4.0027e-03);
            }
            if(ivec == 1){ // Pi+ Pion
                // Smear_SF_Theta    = (-2.4939e-06)*(TMath::RadToDeg()*Th_rec)*(TMath::RadToDeg()*Th_rec) + (5.8277e-04)*(TMath::RadToDeg()*Th_rec) + (-5.8521e-03);
                Smear_SF_Theta       = (-1.6434e-06)*(TMath::RadToDeg()*Th_rec)*(TMath::RadToDeg()*Th_rec) + (5.1530e-04)*(TMath::RadToDeg()*Th_rec) + (-4.4158e-03);
            }
            
            // Calculate resolutions
            double smear_factor = """, str(smear_factor), """;
            double P_new_rec    = P_rec   +   (P_rec)*Smear_SF_Theta*smear_factor*(gRandom->Gaus(0,1));
            double Th_new_rec   = Th_rec  +  (Th_rec)*Smear_SF_Theta*smear_factor*(gRandom->Gaus(0,1));
            double Phi_new_rec  = Phi_rec + (Phi_rec)*Smear_SF_Theta*smear_factor*(gRandom->Gaus(0,1));
            Th_new_rec  = Th_rec;
            Phi_new_rec = Phi_rec;
            
            
            
            double Extra_Smear_SF_Theta = 0;
            if(ivec == 1){ // Pi+ Pion
                Extra_Smear_SF_Theta = (2.2747e-06)*(TMath::RadToDeg()*Th_rec)*(TMath::RadToDeg()*Th_rec) + (3.0985e-04)*(TMath::RadToDeg()*Th_rec) + (-5.1206e-03);
                P_new_rec      = P_new_rec   +   (P_new_rec)*Extra_Smear_SF_Theta*smear_factor*(gRandom->Gaus(0,1));
                // Th_new_rec  = Th_new_rec  +  (Th_new_rec)*Extra_Smear_SF_Theta*smear_factor*(gRandom->Gaus(0,1));
                // Phi_new_rec = Phi_new_rec + (Phi_new_rec)*Extra_Smear_SF_Theta*smear_factor*(gRandom->Gaus(0,1));
            }
            if(ivec == 0){ // Electron
                Extra_Smear_SF_Theta = (-2.1655e-05)*(TMath::RadToDeg()*Th_rec)*(TMath::RadToDeg()*Th_rec) + (7.6626e-04)*(TMath::RadToDeg()*Th_rec) + (-3.8613e-03);
                P_new_rec      = P_new_rec   +   (P_new_rec)*Extra_Smear_SF_Theta*smear_factor*(gRandom->Gaus(0,1));
                // Th_new_rec  = Th_new_rec  +  (Th_new_rec)*Extra_Smear_SF_Theta*smear_factor*(gRandom->Gaus(0,1));
                // Phi_new_rec = Phi_new_rec + (Phi_new_rec)*Extra_Smear_SF_Theta*smear_factor*(gRandom->Gaus(0,1));
            }
            

            // Making the smeared TLorentzVector:
            TLorentzVector V4_smear(V4.X(), V4.Y(), V4.Z(), V4.E());
            V4_smear.SetE(TMath::Sqrt(P_new_rec*P_new_rec + M_rec*M_rec));
            V4_smear.SetRho(   P_new_rec);
            V4_smear.SetTheta(Th_new_rec);
            V4_smear.SetPhi( Phi_new_rec);
            return V4_smear;
        };"""])
    
    return smearing_function








###########################################################################################################################################################################
###########################################################################################################################################################################
###########################################################################################################################################################################
###########################################################################################################################################################################
###########################################################################################################################################################################









# Conditions for (Monte Carlo) Background Events
# # Convension Used in this list:
    # # (*) If ANY of the statements given in 'List_of_Cuts' are true, the event will be considered 'background'
        # # To remove everything but the background events from a rdf dataframe, use the following line:
          # # # WITH_background_rdf = rdf.Filter(Background_Cuts_MC)
          # # # (This will keep any event which passes at least one of the background conditions given)
    # # (*) To remove the background events from a rdf dataframe, use the following line:
        # # # NO_background_rdf = rdf.Filter(f"!({Background_Cuts_MC})")
        # # # (This will keep only those events which fail every condition given)
Background_Cuts_MC = ""
List_of_Cuts = ["MM_gen < 1.5"]
for cuts in List_of_Cuts:
    if(Background_Cuts_MC in [""]):
        Background_Cuts_MC = cuts
    else:
        Background_Cuts_MC = "".join([str(Background_Cuts_MC), " || ", str(cuts)])
    
del cuts
del List_of_Cuts



