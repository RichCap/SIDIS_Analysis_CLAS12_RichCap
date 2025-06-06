New_z_pT_and_MultiDim_Binning_Code = '''
float z_pT_Bin_Borders[18][37][4];
   // z_pT_Bin_Borders[Q2_y_Bin][z_pT_Bin][Border_Num]
    // Border_Num = 0 -> z_max
    // Border_Num = 1 -> z_min
    // Border_Num = 2 -> pT_max
    // Border_Num = 4 -> pT_min
    // (Total of 17 Q2-y bins with defined z-pT borders)
int Phi_h_Bin_Values[40][37][3];
 // Phi_h_Bin_Values[Q2_y_Bin][z_pT_Bin][Dimension]
    // Dimension = 0 -> Number of phi_h bins (either 24 or 1)
    // Dimension = 1 -> Number of combined z_pT + phi_h bins        (used for 3D unfolding - add the appropiate phi_h bin number to these values to get the 3D bin number - resets with every new Q2-y bin)
    // Dimension = 2 -> Number of combined Q2_y + z_pT + phi_h bins (used for 5D unfolding - add the appropiate phi_h bin number to these values to get the 5D bin number - does not resets with new bins)
    // (Total of 39 Q2-y bins including overflow bins)
z_pT_Bin_Borders[1][1][0]   = 0.71;	z_pT_Bin_Borders[1][1][1]   = 0.4;	z_pT_Bin_Borders[1][1][2]   = 0.22;	z_pT_Bin_Borders[1][1][3]   = 0.05;	Phi_h_Bin_Values[1][1][0]   =  24;	Phi_h_Bin_Values[1][1][1]   = 0;	Phi_h_Bin_Values[1][1][2]   = 0;
z_pT_Bin_Borders[1][2][0]   = 0.71;	z_pT_Bin_Borders[1][2][1]   = 0.4;	z_pT_Bin_Borders[1][2][2]   = 0.32;	z_pT_Bin_Borders[1][2][3]   = 0.22;	Phi_h_Bin_Values[1][2][0]   =  24;	Phi_h_Bin_Values[1][2][1]   = 24;	Phi_h_Bin_Values[1][2][2]   = 24;
z_pT_Bin_Borders[1][3][0]   = 0.71;	z_pT_Bin_Borders[1][3][1]   = 0.4;	z_pT_Bin_Borders[1][3][2]   = 0.42;	z_pT_Bin_Borders[1][3][3]   = 0.32;	Phi_h_Bin_Values[1][3][0]   =  24;	Phi_h_Bin_Values[1][3][1]   = 48;	Phi_h_Bin_Values[1][3][2]   = 48;
z_pT_Bin_Borders[1][4][0]   = 0.71;	z_pT_Bin_Borders[1][4][1]   = 0.4;	z_pT_Bin_Borders[1][4][2]   = 0.52;	z_pT_Bin_Borders[1][4][3]   = 0.42;	Phi_h_Bin_Values[1][4][0]   =  24;	Phi_h_Bin_Values[1][4][1]   = 72;	Phi_h_Bin_Values[1][4][2]   = 72;
z_pT_Bin_Borders[1][5][0]   = 0.71;	z_pT_Bin_Borders[1][5][1]   = 0.4;	z_pT_Bin_Borders[1][5][2]   = 0.63;	z_pT_Bin_Borders[1][5][3]   = 0.52;	Phi_h_Bin_Values[1][5][0]   =  24;	Phi_h_Bin_Values[1][5][1]   = 96;	Phi_h_Bin_Values[1][5][2]   = 96;
z_pT_Bin_Borders[1][6][0]   = 0.71;	z_pT_Bin_Borders[1][6][1]   = 0.4;	z_pT_Bin_Borders[1][6][2]   = 0.75;	z_pT_Bin_Borders[1][6][3]   = 0.63;	Phi_h_Bin_Values[1][6][0]   =  24;	Phi_h_Bin_Values[1][6][1]   = 120;	Phi_h_Bin_Values[1][6][2]   = 120;
z_pT_Bin_Borders[1][7][0]   = 0.71;	z_pT_Bin_Borders[1][7][1]   = 0.4;	z_pT_Bin_Borders[1][7][2]   = 0.99;	z_pT_Bin_Borders[1][7][3]   = 0.75;	Phi_h_Bin_Values[1][7][0]   =  24;	Phi_h_Bin_Values[1][7][1]   = 144;	Phi_h_Bin_Values[1][7][2]   = 144;
z_pT_Bin_Borders[1][8][0]   = 0.4;	z_pT_Bin_Borders[1][8][1]   = 0.29;	z_pT_Bin_Borders[1][8][2]   = 0.22;	z_pT_Bin_Borders[1][8][3]   = 0.05;	Phi_h_Bin_Values[1][8][0]   =  24;	Phi_h_Bin_Values[1][8][1]   = 168;	Phi_h_Bin_Values[1][8][2]   = 168;
z_pT_Bin_Borders[1][9][0]   = 0.4;	z_pT_Bin_Borders[1][9][1]   = 0.29;	z_pT_Bin_Borders[1][9][2]   = 0.32;	z_pT_Bin_Borders[1][9][3]   = 0.22;	Phi_h_Bin_Values[1][9][0]   =  24;	Phi_h_Bin_Values[1][9][1]   = 192;	Phi_h_Bin_Values[1][9][2]   = 192;
z_pT_Bin_Borders[1][10][0]  = 0.4;	z_pT_Bin_Borders[1][10][1]  = 0.29;	z_pT_Bin_Borders[1][10][2]  = 0.42;	z_pT_Bin_Borders[1][10][3]  = 0.32;	Phi_h_Bin_Values[1][10][0]  =  24;	Phi_h_Bin_Values[1][10][1]  = 216;	Phi_h_Bin_Values[1][10][2]  = 216;
z_pT_Bin_Borders[1][11][0]  = 0.4;	z_pT_Bin_Borders[1][11][1]  = 0.29;	z_pT_Bin_Borders[1][11][2]  = 0.52;	z_pT_Bin_Borders[1][11][3]  = 0.42;	Phi_h_Bin_Values[1][11][0]  =  24;	Phi_h_Bin_Values[1][11][1]  = 240;	Phi_h_Bin_Values[1][11][2]  = 240;
z_pT_Bin_Borders[1][12][0]  = 0.4;	z_pT_Bin_Borders[1][12][1]  = 0.29;	z_pT_Bin_Borders[1][12][2]  = 0.63;	z_pT_Bin_Borders[1][12][3]  = 0.52;	Phi_h_Bin_Values[1][12][0]  =  24;	Phi_h_Bin_Values[1][12][1]  = 264;	Phi_h_Bin_Values[1][12][2]  = 264;
z_pT_Bin_Borders[1][13][0]  = 0.4;	z_pT_Bin_Borders[1][13][1]  = 0.29;	z_pT_Bin_Borders[1][13][2]  = 0.75;	z_pT_Bin_Borders[1][13][3]  = 0.63;	Phi_h_Bin_Values[1][13][0]  =  24;	Phi_h_Bin_Values[1][13][1]  = 288;	Phi_h_Bin_Values[1][13][2]  = 288;
z_pT_Bin_Borders[1][14][0]  = 0.4;	z_pT_Bin_Borders[1][14][1]  = 0.29;	z_pT_Bin_Borders[1][14][2]  = 0.99;	z_pT_Bin_Borders[1][14][3]  = 0.75;	Phi_h_Bin_Values[1][14][0]  =  24;	Phi_h_Bin_Values[1][14][1]  = 312;	Phi_h_Bin_Values[1][14][2]  = 312;
z_pT_Bin_Borders[1][15][0]  = 0.29;	z_pT_Bin_Borders[1][15][1]  = 0.23;	z_pT_Bin_Borders[1][15][2]  = 0.22;	z_pT_Bin_Borders[1][15][3]  = 0.05;	Phi_h_Bin_Values[1][15][0]  =  24;	Phi_h_Bin_Values[1][15][1]  = 336;	Phi_h_Bin_Values[1][15][2]  = 336;
z_pT_Bin_Borders[1][16][0]  = 0.29;	z_pT_Bin_Borders[1][16][1]  = 0.23;	z_pT_Bin_Borders[1][16][2]  = 0.32;	z_pT_Bin_Borders[1][16][3]  = 0.22;	Phi_h_Bin_Values[1][16][0]  =  24;	Phi_h_Bin_Values[1][16][1]  = 360;	Phi_h_Bin_Values[1][16][2]  = 360;
z_pT_Bin_Borders[1][17][0]  = 0.29;	z_pT_Bin_Borders[1][17][1]  = 0.23;	z_pT_Bin_Borders[1][17][2]  = 0.42;	z_pT_Bin_Borders[1][17][3]  = 0.32;	Phi_h_Bin_Values[1][17][0]  =  24;	Phi_h_Bin_Values[1][17][1]  = 384;	Phi_h_Bin_Values[1][17][2]  = 384;
z_pT_Bin_Borders[1][18][0]  = 0.29;	z_pT_Bin_Borders[1][18][1]  = 0.23;	z_pT_Bin_Borders[1][18][2]  = 0.52;	z_pT_Bin_Borders[1][18][3]  = 0.42;	Phi_h_Bin_Values[1][18][0]  =  24;	Phi_h_Bin_Values[1][18][1]  = 408;	Phi_h_Bin_Values[1][18][2]  = 408;
z_pT_Bin_Borders[1][19][0]  = 0.29;	z_pT_Bin_Borders[1][19][1]  = 0.23;	z_pT_Bin_Borders[1][19][2]  = 0.63;	z_pT_Bin_Borders[1][19][3]  = 0.52;	Phi_h_Bin_Values[1][19][0]  =  24;	Phi_h_Bin_Values[1][19][1]  = 432;	Phi_h_Bin_Values[1][19][2]  = 432;
z_pT_Bin_Borders[1][20][0]  = 0.29;	z_pT_Bin_Borders[1][20][1]  = 0.23;	z_pT_Bin_Borders[1][20][2]  = 0.75;	z_pT_Bin_Borders[1][20][3]  = 0.63;	Phi_h_Bin_Values[1][20][0]  =  24;	Phi_h_Bin_Values[1][20][1]  = 456;	Phi_h_Bin_Values[1][20][2]  = 456;
z_pT_Bin_Borders[1][21][0]  = 0.29;	z_pT_Bin_Borders[1][21][1]  = 0.23;	z_pT_Bin_Borders[1][21][2]  = 0.99;	z_pT_Bin_Borders[1][21][3]  = 0.75;	Phi_h_Bin_Values[1][21][0]  =  1;	Phi_h_Bin_Values[1][21][1]  = 480;	Phi_h_Bin_Values[1][21][2]  = 480;
z_pT_Bin_Borders[1][22][0]  = 0.23;	z_pT_Bin_Borders[1][22][1]  = 0.19;	z_pT_Bin_Borders[1][22][2]  = 0.22;	z_pT_Bin_Borders[1][22][3]  = 0.05;	Phi_h_Bin_Values[1][22][0]  =  24;	Phi_h_Bin_Values[1][22][1]  = 481;	Phi_h_Bin_Values[1][22][2]  = 481;
z_pT_Bin_Borders[1][23][0]  = 0.23;	z_pT_Bin_Borders[1][23][1]  = 0.19;	z_pT_Bin_Borders[1][23][2]  = 0.32;	z_pT_Bin_Borders[1][23][3]  = 0.22;	Phi_h_Bin_Values[1][23][0]  =  24;	Phi_h_Bin_Values[1][23][1]  = 505;	Phi_h_Bin_Values[1][23][2]  = 505;
z_pT_Bin_Borders[1][24][0]  = 0.23;	z_pT_Bin_Borders[1][24][1]  = 0.19;	z_pT_Bin_Borders[1][24][2]  = 0.42;	z_pT_Bin_Borders[1][24][3]  = 0.32;	Phi_h_Bin_Values[1][24][0]  =  24;	Phi_h_Bin_Values[1][24][1]  = 529;	Phi_h_Bin_Values[1][24][2]  = 529;
z_pT_Bin_Borders[1][25][0]  = 0.23;	z_pT_Bin_Borders[1][25][1]  = 0.19;	z_pT_Bin_Borders[1][25][2]  = 0.52;	z_pT_Bin_Borders[1][25][3]  = 0.42;	Phi_h_Bin_Values[1][25][0]  =  24;	Phi_h_Bin_Values[1][25][1]  = 553;	Phi_h_Bin_Values[1][25][2]  = 553;
z_pT_Bin_Borders[1][26][0]  = 0.23;	z_pT_Bin_Borders[1][26][1]  = 0.19;	z_pT_Bin_Borders[1][26][2]  = 0.63;	z_pT_Bin_Borders[1][26][3]  = 0.52;	Phi_h_Bin_Values[1][26][0]  =  24;	Phi_h_Bin_Values[1][26][1]  = 577;	Phi_h_Bin_Values[1][26][2]  = 577;
z_pT_Bin_Borders[1][27][0]  = 0.23;	z_pT_Bin_Borders[1][27][1]  = 0.19;	z_pT_Bin_Borders[1][27][2]  = 0.75;	z_pT_Bin_Borders[1][27][3]  = 0.63;	Phi_h_Bin_Values[1][27][0]  =  1;	Phi_h_Bin_Values[1][27][1]  = 601;	Phi_h_Bin_Values[1][27][2]  = 601;
z_pT_Bin_Borders[1][28][0]  = 0.23;	z_pT_Bin_Borders[1][28][1]  = 0.19;	z_pT_Bin_Borders[1][28][2]  = 0.99;	z_pT_Bin_Borders[1][28][3]  = 0.75;	Phi_h_Bin_Values[1][28][0]  =  1;	Phi_h_Bin_Values[1][28][1]  = 602;	Phi_h_Bin_Values[1][28][2]  = 602;
z_pT_Bin_Borders[1][29][0]  = 0.19;	z_pT_Bin_Borders[1][29][1]  = 0.16;	z_pT_Bin_Borders[1][29][2]  = 0.22;	z_pT_Bin_Borders[1][29][3]  = 0.05;	Phi_h_Bin_Values[1][29][0]  =  24;	Phi_h_Bin_Values[1][29][1]  = 603;	Phi_h_Bin_Values[1][29][2]  = 603;
z_pT_Bin_Borders[1][30][0]  = 0.19;	z_pT_Bin_Borders[1][30][1]  = 0.16;	z_pT_Bin_Borders[1][30][2]  = 0.32;	z_pT_Bin_Borders[1][30][3]  = 0.22;	Phi_h_Bin_Values[1][30][0]  =  24;	Phi_h_Bin_Values[1][30][1]  = 627;	Phi_h_Bin_Values[1][30][2]  = 627;
z_pT_Bin_Borders[1][31][0]  = 0.19;	z_pT_Bin_Borders[1][31][1]  = 0.16;	z_pT_Bin_Borders[1][31][2]  = 0.42;	z_pT_Bin_Borders[1][31][3]  = 0.32;	Phi_h_Bin_Values[1][31][0]  =  24;	Phi_h_Bin_Values[1][31][1]  = 651;	Phi_h_Bin_Values[1][31][2]  = 651;
z_pT_Bin_Borders[1][32][0]  = 0.19;	z_pT_Bin_Borders[1][32][1]  = 0.16;	z_pT_Bin_Borders[1][32][2]  = 0.52;	z_pT_Bin_Borders[1][32][3]  = 0.42;	Phi_h_Bin_Values[1][32][0]  =  24;	Phi_h_Bin_Values[1][32][1]  = 675;	Phi_h_Bin_Values[1][32][2]  = 675;
z_pT_Bin_Borders[1][33][0]  = 0.19;	z_pT_Bin_Borders[1][33][1]  = 0.16;	z_pT_Bin_Borders[1][33][2]  = 0.63;	z_pT_Bin_Borders[1][33][3]  = 0.52;	Phi_h_Bin_Values[1][33][0]  =  1;	Phi_h_Bin_Values[1][33][1]  = 699;	Phi_h_Bin_Values[1][33][2]  = 699;
z_pT_Bin_Borders[1][34][0]  = 0.19;	z_pT_Bin_Borders[1][34][1]  = 0.16;	z_pT_Bin_Borders[1][34][2]  = 0.75;	z_pT_Bin_Borders[1][34][3]  = 0.63;	Phi_h_Bin_Values[1][34][0]  =  1;	Phi_h_Bin_Values[1][34][1]  = 700;	Phi_h_Bin_Values[1][34][2]  = 700;
z_pT_Bin_Borders[1][35][0]  = 0.19;	z_pT_Bin_Borders[1][35][1]  = 0.16;	z_pT_Bin_Borders[1][35][2]  = 0.99;	z_pT_Bin_Borders[1][35][3]  = 0.75;	Phi_h_Bin_Values[1][35][0]  =  1;	Phi_h_Bin_Values[1][35][1]  = 701;	Phi_h_Bin_Values[1][35][2]  = 701;
z_pT_Bin_Borders[2][1][0]   = 0.75;	z_pT_Bin_Borders[2][1][1]   = 0.5;	z_pT_Bin_Borders[2][1][2]   = 0.25;	z_pT_Bin_Borders[2][1][3]   = 0.05;	Phi_h_Bin_Values[2][1][0]   =  24;	Phi_h_Bin_Values[2][1][1]   = 0;	Phi_h_Bin_Values[2][1][2]   = 702;
z_pT_Bin_Borders[2][2][0]   = 0.75;	z_pT_Bin_Borders[2][2][1]   = 0.5;	z_pT_Bin_Borders[2][2][2]   = 0.35;	z_pT_Bin_Borders[2][2][3]   = 0.25;	Phi_h_Bin_Values[2][2][0]   =  24;	Phi_h_Bin_Values[2][2][1]   = 24;	Phi_h_Bin_Values[2][2][2]   = 726;
z_pT_Bin_Borders[2][3][0]   = 0.75;	z_pT_Bin_Borders[2][3][1]   = 0.5;	z_pT_Bin_Borders[2][3][2]   = 0.45;	z_pT_Bin_Borders[2][3][3]   = 0.35;	Phi_h_Bin_Values[2][3][0]   =  24;	Phi_h_Bin_Values[2][3][1]   = 48;	Phi_h_Bin_Values[2][3][2]   = 750;
z_pT_Bin_Borders[2][4][0]   = 0.75;	z_pT_Bin_Borders[2][4][1]   = 0.5;	z_pT_Bin_Borders[2][4][2]   = 0.54;	z_pT_Bin_Borders[2][4][3]   = 0.45;	Phi_h_Bin_Values[2][4][0]   =  24;	Phi_h_Bin_Values[2][4][1]   = 72;	Phi_h_Bin_Values[2][4][2]   = 774;
z_pT_Bin_Borders[2][5][0]   = 0.75;	z_pT_Bin_Borders[2][5][1]   = 0.5;	z_pT_Bin_Borders[2][5][2]   = 0.67;	z_pT_Bin_Borders[2][5][3]   = 0.54;	Phi_h_Bin_Values[2][5][0]   =  24;	Phi_h_Bin_Values[2][5][1]   = 96;	Phi_h_Bin_Values[2][5][2]   = 798;
z_pT_Bin_Borders[2][6][0]   = 0.75;	z_pT_Bin_Borders[2][6][1]   = 0.5;	z_pT_Bin_Borders[2][6][2]   = 0.93;	z_pT_Bin_Borders[2][6][3]   = 0.67;	Phi_h_Bin_Values[2][6][0]   =  24;	Phi_h_Bin_Values[2][6][1]   = 120;	Phi_h_Bin_Values[2][6][2]   = 822;
z_pT_Bin_Borders[2][7][0]   = 0.5;	z_pT_Bin_Borders[2][7][1]   = 0.38;	z_pT_Bin_Borders[2][7][2]   = 0.25;	z_pT_Bin_Borders[2][7][3]   = 0.05;	Phi_h_Bin_Values[2][7][0]   =  24;	Phi_h_Bin_Values[2][7][1]   = 144;	Phi_h_Bin_Values[2][7][2]   = 846;
z_pT_Bin_Borders[2][8][0]   = 0.5;	z_pT_Bin_Borders[2][8][1]   = 0.38;	z_pT_Bin_Borders[2][8][2]   = 0.35;	z_pT_Bin_Borders[2][8][3]   = 0.25;	Phi_h_Bin_Values[2][8][0]   =  24;	Phi_h_Bin_Values[2][8][1]   = 168;	Phi_h_Bin_Values[2][8][2]   = 870;
z_pT_Bin_Borders[2][9][0]   = 0.5;	z_pT_Bin_Borders[2][9][1]   = 0.38;	z_pT_Bin_Borders[2][9][2]   = 0.45;	z_pT_Bin_Borders[2][9][3]   = 0.35;	Phi_h_Bin_Values[2][9][0]   =  24;	Phi_h_Bin_Values[2][9][1]   = 192;	Phi_h_Bin_Values[2][9][2]   = 894;
z_pT_Bin_Borders[2][10][0]  = 0.5;	z_pT_Bin_Borders[2][10][1]  = 0.38;	z_pT_Bin_Borders[2][10][2]  = 0.54;	z_pT_Bin_Borders[2][10][3]  = 0.45;	Phi_h_Bin_Values[2][10][0]  =  24;	Phi_h_Bin_Values[2][10][1]  = 216;	Phi_h_Bin_Values[2][10][2]  = 918;
z_pT_Bin_Borders[2][11][0]  = 0.5;	z_pT_Bin_Borders[2][11][1]  = 0.38;	z_pT_Bin_Borders[2][11][2]  = 0.67;	z_pT_Bin_Borders[2][11][3]  = 0.54;	Phi_h_Bin_Values[2][11][0]  =  24;	Phi_h_Bin_Values[2][11][1]  = 240;	Phi_h_Bin_Values[2][11][2]  = 942;
z_pT_Bin_Borders[2][12][0]  = 0.5;	z_pT_Bin_Borders[2][12][1]  = 0.38;	z_pT_Bin_Borders[2][12][2]  = 0.93;	z_pT_Bin_Borders[2][12][3]  = 0.67;	Phi_h_Bin_Values[2][12][0]  =  24;	Phi_h_Bin_Values[2][12][1]  = 264;	Phi_h_Bin_Values[2][12][2]  = 966;
z_pT_Bin_Borders[2][13][0]  = 0.38;	z_pT_Bin_Borders[2][13][1]  = 0.31;	z_pT_Bin_Borders[2][13][2]  = 0.25;	z_pT_Bin_Borders[2][13][3]  = 0.05;	Phi_h_Bin_Values[2][13][0]  =  24;	Phi_h_Bin_Values[2][13][1]  = 288;	Phi_h_Bin_Values[2][13][2]  = 990;
z_pT_Bin_Borders[2][14][0]  = 0.38;	z_pT_Bin_Borders[2][14][1]  = 0.31;	z_pT_Bin_Borders[2][14][2]  = 0.35;	z_pT_Bin_Borders[2][14][3]  = 0.25;	Phi_h_Bin_Values[2][14][0]  =  24;	Phi_h_Bin_Values[2][14][1]  = 312;	Phi_h_Bin_Values[2][14][2]  = 1014;
z_pT_Bin_Borders[2][15][0]  = 0.38;	z_pT_Bin_Borders[2][15][1]  = 0.31;	z_pT_Bin_Borders[2][15][2]  = 0.45;	z_pT_Bin_Borders[2][15][3]  = 0.35;	Phi_h_Bin_Values[2][15][0]  =  24;	Phi_h_Bin_Values[2][15][1]  = 336;	Phi_h_Bin_Values[2][15][2]  = 1038;
z_pT_Bin_Borders[2][16][0]  = 0.38;	z_pT_Bin_Borders[2][16][1]  = 0.31;	z_pT_Bin_Borders[2][16][2]  = 0.54;	z_pT_Bin_Borders[2][16][3]  = 0.45;	Phi_h_Bin_Values[2][16][0]  =  24;	Phi_h_Bin_Values[2][16][1]  = 360;	Phi_h_Bin_Values[2][16][2]  = 1062;
z_pT_Bin_Borders[2][17][0]  = 0.38;	z_pT_Bin_Borders[2][17][1]  = 0.31;	z_pT_Bin_Borders[2][17][2]  = 0.67;	z_pT_Bin_Borders[2][17][3]  = 0.54;	Phi_h_Bin_Values[2][17][0]  =  24;	Phi_h_Bin_Values[2][17][1]  = 384;	Phi_h_Bin_Values[2][17][2]  = 1086;
z_pT_Bin_Borders[2][18][0]  = 0.38;	z_pT_Bin_Borders[2][18][1]  = 0.31;	z_pT_Bin_Borders[2][18][2]  = 0.93;	z_pT_Bin_Borders[2][18][3]  = 0.67;	Phi_h_Bin_Values[2][18][0]  =  24;	Phi_h_Bin_Values[2][18][1]  = 408;	Phi_h_Bin_Values[2][18][2]  = 1110;
z_pT_Bin_Borders[2][19][0]  = 0.31;	z_pT_Bin_Borders[2][19][1]  = 0.26;	z_pT_Bin_Borders[2][19][2]  = 0.25;	z_pT_Bin_Borders[2][19][3]  = 0.05;	Phi_h_Bin_Values[2][19][0]  =  24;	Phi_h_Bin_Values[2][19][1]  = 432;	Phi_h_Bin_Values[2][19][2]  = 1134;
z_pT_Bin_Borders[2][20][0]  = 0.31;	z_pT_Bin_Borders[2][20][1]  = 0.26;	z_pT_Bin_Borders[2][20][2]  = 0.35;	z_pT_Bin_Borders[2][20][3]  = 0.25;	Phi_h_Bin_Values[2][20][0]  =  24;	Phi_h_Bin_Values[2][20][1]  = 456;	Phi_h_Bin_Values[2][20][2]  = 1158;
z_pT_Bin_Borders[2][21][0]  = 0.31;	z_pT_Bin_Borders[2][21][1]  = 0.26;	z_pT_Bin_Borders[2][21][2]  = 0.45;	z_pT_Bin_Borders[2][21][3]  = 0.35;	Phi_h_Bin_Values[2][21][0]  =  24;	Phi_h_Bin_Values[2][21][1]  = 480;	Phi_h_Bin_Values[2][21][2]  = 1182;
z_pT_Bin_Borders[2][22][0]  = 0.31;	z_pT_Bin_Borders[2][22][1]  = 0.26;	z_pT_Bin_Borders[2][22][2]  = 0.54;	z_pT_Bin_Borders[2][22][3]  = 0.45;	Phi_h_Bin_Values[2][22][0]  =  24;	Phi_h_Bin_Values[2][22][1]  = 504;	Phi_h_Bin_Values[2][22][2]  = 1206;
z_pT_Bin_Borders[2][23][0]  = 0.31;	z_pT_Bin_Borders[2][23][1]  = 0.26;	z_pT_Bin_Borders[2][23][2]  = 0.67;	z_pT_Bin_Borders[2][23][3]  = 0.54;	Phi_h_Bin_Values[2][23][0]  =  24;	Phi_h_Bin_Values[2][23][1]  = 528;	Phi_h_Bin_Values[2][23][2]  = 1230;
z_pT_Bin_Borders[2][24][0]  = 0.31;	z_pT_Bin_Borders[2][24][1]  = 0.26;	z_pT_Bin_Borders[2][24][2]  = 0.93;	z_pT_Bin_Borders[2][24][3]  = 0.67;	Phi_h_Bin_Values[2][24][0]  =  1;	Phi_h_Bin_Values[2][24][1]  = 552;	Phi_h_Bin_Values[2][24][2]  = 1254;
z_pT_Bin_Borders[2][25][0]  = 0.26;	z_pT_Bin_Borders[2][25][1]  = 0.23;	z_pT_Bin_Borders[2][25][2]  = 0.25;	z_pT_Bin_Borders[2][25][3]  = 0.05;	Phi_h_Bin_Values[2][25][0]  =  24;	Phi_h_Bin_Values[2][25][1]  = 553;	Phi_h_Bin_Values[2][25][2]  = 1255;
z_pT_Bin_Borders[2][26][0]  = 0.26;	z_pT_Bin_Borders[2][26][1]  = 0.23;	z_pT_Bin_Borders[2][26][2]  = 0.35;	z_pT_Bin_Borders[2][26][3]  = 0.25;	Phi_h_Bin_Values[2][26][0]  =  24;	Phi_h_Bin_Values[2][26][1]  = 577;	Phi_h_Bin_Values[2][26][2]  = 1279;
z_pT_Bin_Borders[2][27][0]  = 0.26;	z_pT_Bin_Borders[2][27][1]  = 0.23;	z_pT_Bin_Borders[2][27][2]  = 0.45;	z_pT_Bin_Borders[2][27][3]  = 0.35;	Phi_h_Bin_Values[2][27][0]  =  24;	Phi_h_Bin_Values[2][27][1]  = 601;	Phi_h_Bin_Values[2][27][2]  = 1303;
z_pT_Bin_Borders[2][28][0]  = 0.26;	z_pT_Bin_Borders[2][28][1]  = 0.23;	z_pT_Bin_Borders[2][28][2]  = 0.54;	z_pT_Bin_Borders[2][28][3]  = 0.45;	Phi_h_Bin_Values[2][28][0]  =  24;	Phi_h_Bin_Values[2][28][1]  = 625;	Phi_h_Bin_Values[2][28][2]  = 1327;
z_pT_Bin_Borders[2][29][0]  = 0.26;	z_pT_Bin_Borders[2][29][1]  = 0.23;	z_pT_Bin_Borders[2][29][2]  = 0.67;	z_pT_Bin_Borders[2][29][3]  = 0.54;	Phi_h_Bin_Values[2][29][0]  =  24;	Phi_h_Bin_Values[2][29][1]  = 649;	Phi_h_Bin_Values[2][29][2]  = 1351;
z_pT_Bin_Borders[2][30][0]  = 0.26;	z_pT_Bin_Borders[2][30][1]  = 0.23;	z_pT_Bin_Borders[2][30][2]  = 0.93;	z_pT_Bin_Borders[2][30][3]  = 0.67;	Phi_h_Bin_Values[2][30][0]  =  1;	Phi_h_Bin_Values[2][30][1]  = 673;	Phi_h_Bin_Values[2][30][2]  = 1375;
z_pT_Bin_Borders[2][31][0]  = 0.23;	z_pT_Bin_Borders[2][31][1]  = 0.19;	z_pT_Bin_Borders[2][31][2]  = 0.25;	z_pT_Bin_Borders[2][31][3]  = 0.05;	Phi_h_Bin_Values[2][31][0]  =  24;	Phi_h_Bin_Values[2][31][1]  = 674;	Phi_h_Bin_Values[2][31][2]  = 1376;
z_pT_Bin_Borders[2][32][0]  = 0.23;	z_pT_Bin_Borders[2][32][1]  = 0.19;	z_pT_Bin_Borders[2][32][2]  = 0.35;	z_pT_Bin_Borders[2][32][3]  = 0.25;	Phi_h_Bin_Values[2][32][0]  =  24;	Phi_h_Bin_Values[2][32][1]  = 698;	Phi_h_Bin_Values[2][32][2]  = 1400;
z_pT_Bin_Borders[2][33][0]  = 0.23;	z_pT_Bin_Borders[2][33][1]  = 0.19;	z_pT_Bin_Borders[2][33][2]  = 0.45;	z_pT_Bin_Borders[2][33][3]  = 0.35;	Phi_h_Bin_Values[2][33][0]  =  24;	Phi_h_Bin_Values[2][33][1]  = 722;	Phi_h_Bin_Values[2][33][2]  = 1424;
z_pT_Bin_Borders[2][34][0]  = 0.23;	z_pT_Bin_Borders[2][34][1]  = 0.19;	z_pT_Bin_Borders[2][34][2]  = 0.54;	z_pT_Bin_Borders[2][34][3]  = 0.45;	Phi_h_Bin_Values[2][34][0]  =  24;	Phi_h_Bin_Values[2][34][1]  = 746;	Phi_h_Bin_Values[2][34][2]  = 1448;
z_pT_Bin_Borders[2][35][0]  = 0.23;	z_pT_Bin_Borders[2][35][1]  = 0.19;	z_pT_Bin_Borders[2][35][2]  = 0.67;	z_pT_Bin_Borders[2][35][3]  = 0.54;	Phi_h_Bin_Values[2][35][0]  =  1;	Phi_h_Bin_Values[2][35][1]  = 770;	Phi_h_Bin_Values[2][35][2]  = 1472;
z_pT_Bin_Borders[2][36][0]  = 0.23;	z_pT_Bin_Borders[2][36][1]  = 0.19;	z_pT_Bin_Borders[2][36][2]  = 0.93;	z_pT_Bin_Borders[2][36][3]  = 0.67;	Phi_h_Bin_Values[2][36][0]  =  1;	Phi_h_Bin_Values[2][36][1]  = 771;	Phi_h_Bin_Values[2][36][2]  = 1473;
z_pT_Bin_Borders[3][1][0]   = 0.75;	z_pT_Bin_Borders[3][1][1]   = 0.56;	z_pT_Bin_Borders[3][1][2]   = 0.2;	z_pT_Bin_Borders[3][1][3]   = 0.05;	Phi_h_Bin_Values[3][1][0]   =  24;	Phi_h_Bin_Values[3][1][1]   = 0;	Phi_h_Bin_Values[3][1][2]   = 1474;
z_pT_Bin_Borders[3][2][0]   = 0.75;	z_pT_Bin_Borders[3][2][1]   = 0.56;	z_pT_Bin_Borders[3][2][2]   = 0.3;	z_pT_Bin_Borders[3][2][3]   = 0.2;	Phi_h_Bin_Values[3][2][0]   =  24;	Phi_h_Bin_Values[3][2][1]   = 24;	Phi_h_Bin_Values[3][2][2]   = 1498;
z_pT_Bin_Borders[3][3][0]   = 0.75;	z_pT_Bin_Borders[3][3][1]   = 0.56;	z_pT_Bin_Borders[3][3][2]   = 0.39;	z_pT_Bin_Borders[3][3][3]   = 0.3;	Phi_h_Bin_Values[3][3][0]   =  24;	Phi_h_Bin_Values[3][3][1]   = 48;	Phi_h_Bin_Values[3][3][2]   = 1522;
z_pT_Bin_Borders[3][4][0]   = 0.75;	z_pT_Bin_Borders[3][4][1]   = 0.56;	z_pT_Bin_Borders[3][4][2]   = 0.49;	z_pT_Bin_Borders[3][4][3]   = 0.39;	Phi_h_Bin_Values[3][4][0]   =  24;	Phi_h_Bin_Values[3][4][1]   = 72;	Phi_h_Bin_Values[3][4][2]   = 1546;
z_pT_Bin_Borders[3][5][0]   = 0.75;	z_pT_Bin_Borders[3][5][1]   = 0.56;	z_pT_Bin_Borders[3][5][2]   = 0.59;	z_pT_Bin_Borders[3][5][3]   = 0.49;	Phi_h_Bin_Values[3][5][0]   =  24;	Phi_h_Bin_Values[3][5][1]   = 96;	Phi_h_Bin_Values[3][5][2]   = 1570;
z_pT_Bin_Borders[3][6][0]   = 0.75;	z_pT_Bin_Borders[3][6][1]   = 0.56;	z_pT_Bin_Borders[3][6][2]   = 0.76;	z_pT_Bin_Borders[3][6][3]   = 0.59;	Phi_h_Bin_Values[3][6][0]   =  24;	Phi_h_Bin_Values[3][6][1]   = 120;	Phi_h_Bin_Values[3][6][2]   = 1594;
z_pT_Bin_Borders[3][7][0]   = 0.56;	z_pT_Bin_Borders[3][7][1]   = 0.41;	z_pT_Bin_Borders[3][7][2]   = 0.2;	z_pT_Bin_Borders[3][7][3]   = 0.05;	Phi_h_Bin_Values[3][7][0]   =  24;	Phi_h_Bin_Values[3][7][1]   = 144;	Phi_h_Bin_Values[3][7][2]   = 1618;
z_pT_Bin_Borders[3][8][0]   = 0.56;	z_pT_Bin_Borders[3][8][1]   = 0.41;	z_pT_Bin_Borders[3][8][2]   = 0.3;	z_pT_Bin_Borders[3][8][3]   = 0.2;	Phi_h_Bin_Values[3][8][0]   =  24;	Phi_h_Bin_Values[3][8][1]   = 168;	Phi_h_Bin_Values[3][8][2]   = 1642;
z_pT_Bin_Borders[3][9][0]   = 0.56;	z_pT_Bin_Borders[3][9][1]   = 0.41;	z_pT_Bin_Borders[3][9][2]   = 0.39;	z_pT_Bin_Borders[3][9][3]   = 0.3;	Phi_h_Bin_Values[3][9][0]   =  24;	Phi_h_Bin_Values[3][9][1]   = 192;	Phi_h_Bin_Values[3][9][2]   = 1666;
z_pT_Bin_Borders[3][10][0]  = 0.56;	z_pT_Bin_Borders[3][10][1]  = 0.41;	z_pT_Bin_Borders[3][10][2]  = 0.49;	z_pT_Bin_Borders[3][10][3]  = 0.39;	Phi_h_Bin_Values[3][10][0]  =  24;	Phi_h_Bin_Values[3][10][1]  = 216;	Phi_h_Bin_Values[3][10][2]  = 1690;
z_pT_Bin_Borders[3][11][0]  = 0.56;	z_pT_Bin_Borders[3][11][1]  = 0.41;	z_pT_Bin_Borders[3][11][2]  = 0.59;	z_pT_Bin_Borders[3][11][3]  = 0.49;	Phi_h_Bin_Values[3][11][0]  =  24;	Phi_h_Bin_Values[3][11][1]  = 240;	Phi_h_Bin_Values[3][11][2]  = 1714;
z_pT_Bin_Borders[3][12][0]  = 0.56;	z_pT_Bin_Borders[3][12][1]  = 0.41;	z_pT_Bin_Borders[3][12][2]  = 0.76;	z_pT_Bin_Borders[3][12][3]  = 0.59;	Phi_h_Bin_Values[3][12][0]  =  24;	Phi_h_Bin_Values[3][12][1]  = 264;	Phi_h_Bin_Values[3][12][2]  = 1738;
z_pT_Bin_Borders[3][13][0]  = 0.41;	z_pT_Bin_Borders[3][13][1]  = 0.33;	z_pT_Bin_Borders[3][13][2]  = 0.2;	z_pT_Bin_Borders[3][13][3]  = 0.05;	Phi_h_Bin_Values[3][13][0]  =  24;	Phi_h_Bin_Values[3][13][1]  = 288;	Phi_h_Bin_Values[3][13][2]  = 1762;
z_pT_Bin_Borders[3][14][0]  = 0.41;	z_pT_Bin_Borders[3][14][1]  = 0.33;	z_pT_Bin_Borders[3][14][2]  = 0.3;	z_pT_Bin_Borders[3][14][3]  = 0.2;	Phi_h_Bin_Values[3][14][0]  =  24;	Phi_h_Bin_Values[3][14][1]  = 312;	Phi_h_Bin_Values[3][14][2]  = 1786;
z_pT_Bin_Borders[3][15][0]  = 0.41;	z_pT_Bin_Borders[3][15][1]  = 0.33;	z_pT_Bin_Borders[3][15][2]  = 0.39;	z_pT_Bin_Borders[3][15][3]  = 0.3;	Phi_h_Bin_Values[3][15][0]  =  24;	Phi_h_Bin_Values[3][15][1]  = 336;	Phi_h_Bin_Values[3][15][2]  = 1810;
z_pT_Bin_Borders[3][16][0]  = 0.41;	z_pT_Bin_Borders[3][16][1]  = 0.33;	z_pT_Bin_Borders[3][16][2]  = 0.49;	z_pT_Bin_Borders[3][16][3]  = 0.39;	Phi_h_Bin_Values[3][16][0]  =  24;	Phi_h_Bin_Values[3][16][1]  = 360;	Phi_h_Bin_Values[3][16][2]  = 1834;
z_pT_Bin_Borders[3][17][0]  = 0.41;	z_pT_Bin_Borders[3][17][1]  = 0.33;	z_pT_Bin_Borders[3][17][2]  = 0.59;	z_pT_Bin_Borders[3][17][3]  = 0.49;	Phi_h_Bin_Values[3][17][0]  =  24;	Phi_h_Bin_Values[3][17][1]  = 384;	Phi_h_Bin_Values[3][17][2]  = 1858;
z_pT_Bin_Borders[3][18][0]  = 0.41;	z_pT_Bin_Borders[3][18][1]  = 0.33;	z_pT_Bin_Borders[3][18][2]  = 0.76;	z_pT_Bin_Borders[3][18][3]  = 0.59;	Phi_h_Bin_Values[3][18][0]  =  24;	Phi_h_Bin_Values[3][18][1]  = 408;	Phi_h_Bin_Values[3][18][2]  = 1882;
z_pT_Bin_Borders[3][19][0]  = 0.33;	z_pT_Bin_Borders[3][19][1]  = 0.28;	z_pT_Bin_Borders[3][19][2]  = 0.2;	z_pT_Bin_Borders[3][19][3]  = 0.05;	Phi_h_Bin_Values[3][19][0]  =  24;	Phi_h_Bin_Values[3][19][1]  = 432;	Phi_h_Bin_Values[3][19][2]  = 1906;
z_pT_Bin_Borders[3][20][0]  = 0.33;	z_pT_Bin_Borders[3][20][1]  = 0.28;	z_pT_Bin_Borders[3][20][2]  = 0.3;	z_pT_Bin_Borders[3][20][3]  = 0.2;	Phi_h_Bin_Values[3][20][0]  =  24;	Phi_h_Bin_Values[3][20][1]  = 456;	Phi_h_Bin_Values[3][20][2]  = 1930;
z_pT_Bin_Borders[3][21][0]  = 0.33;	z_pT_Bin_Borders[3][21][1]  = 0.28;	z_pT_Bin_Borders[3][21][2]  = 0.39;	z_pT_Bin_Borders[3][21][3]  = 0.3;	Phi_h_Bin_Values[3][21][0]  =  24;	Phi_h_Bin_Values[3][21][1]  = 480;	Phi_h_Bin_Values[3][21][2]  = 1954;
z_pT_Bin_Borders[3][22][0]  = 0.33;	z_pT_Bin_Borders[3][22][1]  = 0.28;	z_pT_Bin_Borders[3][22][2]  = 0.49;	z_pT_Bin_Borders[3][22][3]  = 0.39;	Phi_h_Bin_Values[3][22][0]  =  24;	Phi_h_Bin_Values[3][22][1]  = 504;	Phi_h_Bin_Values[3][22][2]  = 1978;
z_pT_Bin_Borders[3][23][0]  = 0.33;	z_pT_Bin_Borders[3][23][1]  = 0.28;	z_pT_Bin_Borders[3][23][2]  = 0.59;	z_pT_Bin_Borders[3][23][3]  = 0.49;	Phi_h_Bin_Values[3][23][0]  =  24;	Phi_h_Bin_Values[3][23][1]  = 528;	Phi_h_Bin_Values[3][23][2]  = 2002;
z_pT_Bin_Borders[3][24][0]  = 0.33;	z_pT_Bin_Borders[3][24][1]  = 0.28;	z_pT_Bin_Borders[3][24][2]  = 0.76;	z_pT_Bin_Borders[3][24][3]  = 0.59;	Phi_h_Bin_Values[3][24][0]  =  24;	Phi_h_Bin_Values[3][24][1]  = 552;	Phi_h_Bin_Values[3][24][2]  = 2026;
z_pT_Bin_Borders[3][25][0]  = 0.28;	z_pT_Bin_Borders[3][25][1]  = 0.22;	z_pT_Bin_Borders[3][25][2]  = 0.2;	z_pT_Bin_Borders[3][25][3]  = 0.05;	Phi_h_Bin_Values[3][25][0]  =  24;	Phi_h_Bin_Values[3][25][1]  = 576;	Phi_h_Bin_Values[3][25][2]  = 2050;
z_pT_Bin_Borders[3][26][0]  = 0.28;	z_pT_Bin_Borders[3][26][1]  = 0.22;	z_pT_Bin_Borders[3][26][2]  = 0.3;	z_pT_Bin_Borders[3][26][3]  = 0.2;	Phi_h_Bin_Values[3][26][0]  =  24;	Phi_h_Bin_Values[3][26][1]  = 600;	Phi_h_Bin_Values[3][26][2]  = 2074;
z_pT_Bin_Borders[3][27][0]  = 0.28;	z_pT_Bin_Borders[3][27][1]  = 0.22;	z_pT_Bin_Borders[3][27][2]  = 0.39;	z_pT_Bin_Borders[3][27][3]  = 0.3;	Phi_h_Bin_Values[3][27][0]  =  24;	Phi_h_Bin_Values[3][27][1]  = 624;	Phi_h_Bin_Values[3][27][2]  = 2098;
z_pT_Bin_Borders[3][28][0]  = 0.28;	z_pT_Bin_Borders[3][28][1]  = 0.22;	z_pT_Bin_Borders[3][28][2]  = 0.49;	z_pT_Bin_Borders[3][28][3]  = 0.39;	Phi_h_Bin_Values[3][28][0]  =  24;	Phi_h_Bin_Values[3][28][1]  = 648;	Phi_h_Bin_Values[3][28][2]  = 2122;
z_pT_Bin_Borders[3][29][0]  = 0.28;	z_pT_Bin_Borders[3][29][1]  = 0.22;	z_pT_Bin_Borders[3][29][2]  = 0.59;	z_pT_Bin_Borders[3][29][3]  = 0.49;	Phi_h_Bin_Values[3][29][0]  =  24;	Phi_h_Bin_Values[3][29][1]  = 672;	Phi_h_Bin_Values[3][29][2]  = 2146;
z_pT_Bin_Borders[3][30][0]  = 0.28;	z_pT_Bin_Borders[3][30][1]  = 0.22;	z_pT_Bin_Borders[3][30][2]  = 0.76;	z_pT_Bin_Borders[3][30][3]  = 0.59;	Phi_h_Bin_Values[3][30][0]  =  1;	Phi_h_Bin_Values[3][30][1]  = 696;	Phi_h_Bin_Values[3][30][2]  = 2170;
z_pT_Bin_Borders[4][1][0]   = 0.71;	z_pT_Bin_Borders[4][1][1]   = 0.59;	z_pT_Bin_Borders[4][1][2]   = 0.2;	z_pT_Bin_Borders[4][1][3]   = 0.05;	Phi_h_Bin_Values[4][1][0]   =  24;	Phi_h_Bin_Values[4][1][1]   = 0;	Phi_h_Bin_Values[4][1][2]   = 2171;
z_pT_Bin_Borders[4][2][0]   = 0.71;	z_pT_Bin_Borders[4][2][1]   = 0.59;	z_pT_Bin_Borders[4][2][2]   = 0.29;	z_pT_Bin_Borders[4][2][3]   = 0.2;	Phi_h_Bin_Values[4][2][0]   =  24;	Phi_h_Bin_Values[4][2][1]   = 24;	Phi_h_Bin_Values[4][2][2]   = 2195;
z_pT_Bin_Borders[4][3][0]   = 0.71;	z_pT_Bin_Borders[4][3][1]   = 0.59;	z_pT_Bin_Borders[4][3][2]   = 0.38;	z_pT_Bin_Borders[4][3][3]   = 0.29;	Phi_h_Bin_Values[4][3][0]   =  24;	Phi_h_Bin_Values[4][3][1]   = 48;	Phi_h_Bin_Values[4][3][2]   = 2219;
z_pT_Bin_Borders[4][4][0]   = 0.71;	z_pT_Bin_Borders[4][4][1]   = 0.59;	z_pT_Bin_Borders[4][4][2]   = 0.48;	z_pT_Bin_Borders[4][4][3]   = 0.38;	Phi_h_Bin_Values[4][4][0]   =  24;	Phi_h_Bin_Values[4][4][1]   = 72;	Phi_h_Bin_Values[4][4][2]   = 2243;
z_pT_Bin_Borders[4][5][0]   = 0.71;	z_pT_Bin_Borders[4][5][1]   = 0.59;	z_pT_Bin_Borders[4][5][2]   = 0.61;	z_pT_Bin_Borders[4][5][3]   = 0.48;	Phi_h_Bin_Values[4][5][0]   =  24;	Phi_h_Bin_Values[4][5][1]   = 96;	Phi_h_Bin_Values[4][5][2]   = 2267;
z_pT_Bin_Borders[4][6][0]   = 0.71;	z_pT_Bin_Borders[4][6][1]   = 0.59;	z_pT_Bin_Borders[4][6][2]   = 0.85;	z_pT_Bin_Borders[4][6][3]   = 0.61;	Phi_h_Bin_Values[4][6][0]   =  1;	Phi_h_Bin_Values[4][6][1]   = 120;	Phi_h_Bin_Values[4][6][2]   = 2291;
z_pT_Bin_Borders[4][7][0]   = 0.59;	z_pT_Bin_Borders[4][7][1]   = 0.5;	z_pT_Bin_Borders[4][7][2]   = 0.2;	z_pT_Bin_Borders[4][7][3]   = 0.05;	Phi_h_Bin_Values[4][7][0]   =  24;	Phi_h_Bin_Values[4][7][1]   = 121;	Phi_h_Bin_Values[4][7][2]   = 2292;
z_pT_Bin_Borders[4][8][0]   = 0.59;	z_pT_Bin_Borders[4][8][1]   = 0.5;	z_pT_Bin_Borders[4][8][2]   = 0.29;	z_pT_Bin_Borders[4][8][3]   = 0.2;	Phi_h_Bin_Values[4][8][0]   =  24;	Phi_h_Bin_Values[4][8][1]   = 145;	Phi_h_Bin_Values[4][8][2]   = 2316;
z_pT_Bin_Borders[4][9][0]   = 0.59;	z_pT_Bin_Borders[4][9][1]   = 0.5;	z_pT_Bin_Borders[4][9][2]   = 0.38;	z_pT_Bin_Borders[4][9][3]   = 0.29;	Phi_h_Bin_Values[4][9][0]   =  24;	Phi_h_Bin_Values[4][9][1]   = 169;	Phi_h_Bin_Values[4][9][2]   = 2340;
z_pT_Bin_Borders[4][10][0]  = 0.59;	z_pT_Bin_Borders[4][10][1]  = 0.5;	z_pT_Bin_Borders[4][10][2]  = 0.48;	z_pT_Bin_Borders[4][10][3]  = 0.38;	Phi_h_Bin_Values[4][10][0]  =  24;	Phi_h_Bin_Values[4][10][1]  = 193;	Phi_h_Bin_Values[4][10][2]  = 2364;
z_pT_Bin_Borders[4][11][0]  = 0.59;	z_pT_Bin_Borders[4][11][1]  = 0.5;	z_pT_Bin_Borders[4][11][2]  = 0.61;	z_pT_Bin_Borders[4][11][3]  = 0.48;	Phi_h_Bin_Values[4][11][0]  =  24;	Phi_h_Bin_Values[4][11][1]  = 217;	Phi_h_Bin_Values[4][11][2]  = 2388;
z_pT_Bin_Borders[4][12][0]  = 0.59;	z_pT_Bin_Borders[4][12][1]  = 0.5;	z_pT_Bin_Borders[4][12][2]  = 0.85;	z_pT_Bin_Borders[4][12][3]  = 0.61;	Phi_h_Bin_Values[4][12][0]  =  24;	Phi_h_Bin_Values[4][12][1]  = 241;	Phi_h_Bin_Values[4][12][2]  = 2412;
z_pT_Bin_Borders[4][13][0]  = 0.5;	z_pT_Bin_Borders[4][13][1]  = 0.43;	z_pT_Bin_Borders[4][13][2]  = 0.2;	z_pT_Bin_Borders[4][13][3]  = 0.05;	Phi_h_Bin_Values[4][13][0]  =  24;	Phi_h_Bin_Values[4][13][1]  = 265;	Phi_h_Bin_Values[4][13][2]  = 2436;
z_pT_Bin_Borders[4][14][0]  = 0.5;	z_pT_Bin_Borders[4][14][1]  = 0.43;	z_pT_Bin_Borders[4][14][2]  = 0.29;	z_pT_Bin_Borders[4][14][3]  = 0.2;	Phi_h_Bin_Values[4][14][0]  =  24;	Phi_h_Bin_Values[4][14][1]  = 289;	Phi_h_Bin_Values[4][14][2]  = 2460;
z_pT_Bin_Borders[4][15][0]  = 0.5;	z_pT_Bin_Borders[4][15][1]  = 0.43;	z_pT_Bin_Borders[4][15][2]  = 0.38;	z_pT_Bin_Borders[4][15][3]  = 0.29;	Phi_h_Bin_Values[4][15][0]  =  24;	Phi_h_Bin_Values[4][15][1]  = 313;	Phi_h_Bin_Values[4][15][2]  = 2484;
z_pT_Bin_Borders[4][16][0]  = 0.5;	z_pT_Bin_Borders[4][16][1]  = 0.43;	z_pT_Bin_Borders[4][16][2]  = 0.48;	z_pT_Bin_Borders[4][16][3]  = 0.38;	Phi_h_Bin_Values[4][16][0]  =  24;	Phi_h_Bin_Values[4][16][1]  = 337;	Phi_h_Bin_Values[4][16][2]  = 2508;
z_pT_Bin_Borders[4][17][0]  = 0.5;	z_pT_Bin_Borders[4][17][1]  = 0.43;	z_pT_Bin_Borders[4][17][2]  = 0.61;	z_pT_Bin_Borders[4][17][3]  = 0.48;	Phi_h_Bin_Values[4][17][0]  =  24;	Phi_h_Bin_Values[4][17][1]  = 361;	Phi_h_Bin_Values[4][17][2]  = 2532;
z_pT_Bin_Borders[4][18][0]  = 0.5;	z_pT_Bin_Borders[4][18][1]  = 0.43;	z_pT_Bin_Borders[4][18][2]  = 0.85;	z_pT_Bin_Borders[4][18][3]  = 0.61;	Phi_h_Bin_Values[4][18][0]  =  24;	Phi_h_Bin_Values[4][18][1]  = 385;	Phi_h_Bin_Values[4][18][2]  = 2556;
z_pT_Bin_Borders[4][19][0]  = 0.43;	z_pT_Bin_Borders[4][19][1]  = 0.38;	z_pT_Bin_Borders[4][19][2]  = 0.2;	z_pT_Bin_Borders[4][19][3]  = 0.05;	Phi_h_Bin_Values[4][19][0]  =  24;	Phi_h_Bin_Values[4][19][1]  = 409;	Phi_h_Bin_Values[4][19][2]  = 2580;
z_pT_Bin_Borders[4][20][0]  = 0.43;	z_pT_Bin_Borders[4][20][1]  = 0.38;	z_pT_Bin_Borders[4][20][2]  = 0.29;	z_pT_Bin_Borders[4][20][3]  = 0.2;	Phi_h_Bin_Values[4][20][0]  =  24;	Phi_h_Bin_Values[4][20][1]  = 433;	Phi_h_Bin_Values[4][20][2]  = 2604;
z_pT_Bin_Borders[4][21][0]  = 0.43;	z_pT_Bin_Borders[4][21][1]  = 0.38;	z_pT_Bin_Borders[4][21][2]  = 0.38;	z_pT_Bin_Borders[4][21][3]  = 0.29;	Phi_h_Bin_Values[4][21][0]  =  24;	Phi_h_Bin_Values[4][21][1]  = 457;	Phi_h_Bin_Values[4][21][2]  = 2628;
z_pT_Bin_Borders[4][22][0]  = 0.43;	z_pT_Bin_Borders[4][22][1]  = 0.38;	z_pT_Bin_Borders[4][22][2]  = 0.48;	z_pT_Bin_Borders[4][22][3]  = 0.38;	Phi_h_Bin_Values[4][22][0]  =  24;	Phi_h_Bin_Values[4][22][1]  = 481;	Phi_h_Bin_Values[4][22][2]  = 2652;
z_pT_Bin_Borders[4][23][0]  = 0.43;	z_pT_Bin_Borders[4][23][1]  = 0.38;	z_pT_Bin_Borders[4][23][2]  = 0.61;	z_pT_Bin_Borders[4][23][3]  = 0.48;	Phi_h_Bin_Values[4][23][0]  =  24;	Phi_h_Bin_Values[4][23][1]  = 505;	Phi_h_Bin_Values[4][23][2]  = 2676;
z_pT_Bin_Borders[4][24][0]  = 0.43;	z_pT_Bin_Borders[4][24][1]  = 0.38;	z_pT_Bin_Borders[4][24][2]  = 0.85;	z_pT_Bin_Borders[4][24][3]  = 0.61;	Phi_h_Bin_Values[4][24][0]  =  24;	Phi_h_Bin_Values[4][24][1]  = 529;	Phi_h_Bin_Values[4][24][2]  = 2700;
z_pT_Bin_Borders[4][25][0]  = 0.38;	z_pT_Bin_Borders[4][25][1]  = 0.33;	z_pT_Bin_Borders[4][25][2]  = 0.2;	z_pT_Bin_Borders[4][25][3]  = 0.05;	Phi_h_Bin_Values[4][25][0]  =  24;	Phi_h_Bin_Values[4][25][1]  = 553;	Phi_h_Bin_Values[4][25][2]  = 2724;
z_pT_Bin_Borders[4][26][0]  = 0.38;	z_pT_Bin_Borders[4][26][1]  = 0.33;	z_pT_Bin_Borders[4][26][2]  = 0.29;	z_pT_Bin_Borders[4][26][3]  = 0.2;	Phi_h_Bin_Values[4][26][0]  =  24;	Phi_h_Bin_Values[4][26][1]  = 577;	Phi_h_Bin_Values[4][26][2]  = 2748;
z_pT_Bin_Borders[4][27][0]  = 0.38;	z_pT_Bin_Borders[4][27][1]  = 0.33;	z_pT_Bin_Borders[4][27][2]  = 0.38;	z_pT_Bin_Borders[4][27][3]  = 0.29;	Phi_h_Bin_Values[4][27][0]  =  24;	Phi_h_Bin_Values[4][27][1]  = 601;	Phi_h_Bin_Values[4][27][2]  = 2772;
z_pT_Bin_Borders[4][28][0]  = 0.38;	z_pT_Bin_Borders[4][28][1]  = 0.33;	z_pT_Bin_Borders[4][28][2]  = 0.48;	z_pT_Bin_Borders[4][28][3]  = 0.38;	Phi_h_Bin_Values[4][28][0]  =  24;	Phi_h_Bin_Values[4][28][1]  = 625;	Phi_h_Bin_Values[4][28][2]  = 2796;
z_pT_Bin_Borders[4][29][0]  = 0.38;	z_pT_Bin_Borders[4][29][1]  = 0.33;	z_pT_Bin_Borders[4][29][2]  = 0.61;	z_pT_Bin_Borders[4][29][3]  = 0.48;	Phi_h_Bin_Values[4][29][0]  =  24;	Phi_h_Bin_Values[4][29][1]  = 649;	Phi_h_Bin_Values[4][29][2]  = 2820;
z_pT_Bin_Borders[4][30][0]  = 0.38;	z_pT_Bin_Borders[4][30][1]  = 0.33;	z_pT_Bin_Borders[4][30][2]  = 0.85;	z_pT_Bin_Borders[4][30][3]  = 0.61;	Phi_h_Bin_Values[4][30][0]  =  1;	Phi_h_Bin_Values[4][30][1]  = 673;	Phi_h_Bin_Values[4][30][2]  = 2844;
z_pT_Bin_Borders[4][31][0]  = 0.33;	z_pT_Bin_Borders[4][31][1]  = 0.26;	z_pT_Bin_Borders[4][31][2]  = 0.2;	z_pT_Bin_Borders[4][31][3]  = 0.05;	Phi_h_Bin_Values[4][31][0]  =  24;	Phi_h_Bin_Values[4][31][1]  = 674;	Phi_h_Bin_Values[4][31][2]  = 2845;
z_pT_Bin_Borders[4][32][0]  = 0.33;	z_pT_Bin_Borders[4][32][1]  = 0.26;	z_pT_Bin_Borders[4][32][2]  = 0.29;	z_pT_Bin_Borders[4][32][3]  = 0.2;	Phi_h_Bin_Values[4][32][0]  =  24;	Phi_h_Bin_Values[4][32][1]  = 698;	Phi_h_Bin_Values[4][32][2]  = 2869;
z_pT_Bin_Borders[4][33][0]  = 0.33;	z_pT_Bin_Borders[4][33][1]  = 0.26;	z_pT_Bin_Borders[4][33][2]  = 0.38;	z_pT_Bin_Borders[4][33][3]  = 0.29;	Phi_h_Bin_Values[4][33][0]  =  24;	Phi_h_Bin_Values[4][33][1]  = 722;	Phi_h_Bin_Values[4][33][2]  = 2893;
z_pT_Bin_Borders[4][34][0]  = 0.33;	z_pT_Bin_Borders[4][34][1]  = 0.26;	z_pT_Bin_Borders[4][34][2]  = 0.48;	z_pT_Bin_Borders[4][34][3]  = 0.38;	Phi_h_Bin_Values[4][34][0]  =  24;	Phi_h_Bin_Values[4][34][1]  = 746;	Phi_h_Bin_Values[4][34][2]  = 2917;
z_pT_Bin_Borders[4][35][0]  = 0.33;	z_pT_Bin_Borders[4][35][1]  = 0.26;	z_pT_Bin_Borders[4][35][2]  = 0.61;	z_pT_Bin_Borders[4][35][3]  = 0.48;	Phi_h_Bin_Values[4][35][0]  =  24;	Phi_h_Bin_Values[4][35][1]  = 770;	Phi_h_Bin_Values[4][35][2]  = 2941;
z_pT_Bin_Borders[4][36][0]  = 0.33;	z_pT_Bin_Borders[4][36][1]  = 0.26;	z_pT_Bin_Borders[4][36][2]  = 0.85;	z_pT_Bin_Borders[4][36][3]  = 0.61;	Phi_h_Bin_Values[4][36][0]  =  1;	Phi_h_Bin_Values[4][36][1]  = 794;	Phi_h_Bin_Values[4][36][2]  = 2965;
z_pT_Bin_Borders[5][1][0]   = 0.72;	z_pT_Bin_Borders[5][1][1]   = 0.49;	z_pT_Bin_Borders[5][1][2]   = 0.22;	z_pT_Bin_Borders[5][1][3]   = 0.05;	Phi_h_Bin_Values[5][1][0]   =  24;	Phi_h_Bin_Values[5][1][1]   = 0;	Phi_h_Bin_Values[5][1][2]   = 2966;
z_pT_Bin_Borders[5][2][0]   = 0.72;	z_pT_Bin_Borders[5][2][1]   = 0.49;	z_pT_Bin_Borders[5][2][2]   = 0.32;	z_pT_Bin_Borders[5][2][3]   = 0.22;	Phi_h_Bin_Values[5][2][0]   =  24;	Phi_h_Bin_Values[5][2][1]   = 24;	Phi_h_Bin_Values[5][2][2]   = 2990;
z_pT_Bin_Borders[5][3][0]   = 0.72;	z_pT_Bin_Borders[5][3][1]   = 0.49;	z_pT_Bin_Borders[5][3][2]   = 0.41;	z_pT_Bin_Borders[5][3][3]   = 0.32;	Phi_h_Bin_Values[5][3][0]   =  24;	Phi_h_Bin_Values[5][3][1]   = 48;	Phi_h_Bin_Values[5][3][2]   = 3014;
z_pT_Bin_Borders[5][4][0]   = 0.72;	z_pT_Bin_Borders[5][4][1]   = 0.49;	z_pT_Bin_Borders[5][4][2]   = 0.51;	z_pT_Bin_Borders[5][4][3]   = 0.41;	Phi_h_Bin_Values[5][4][0]   =  24;	Phi_h_Bin_Values[5][4][1]   = 72;	Phi_h_Bin_Values[5][4][2]   = 3038;
z_pT_Bin_Borders[5][5][0]   = 0.72;	z_pT_Bin_Borders[5][5][1]   = 0.49;	z_pT_Bin_Borders[5][5][2]   = 0.65;	z_pT_Bin_Borders[5][5][3]   = 0.51;	Phi_h_Bin_Values[5][5][0]   =  24;	Phi_h_Bin_Values[5][5][1]   = 96;	Phi_h_Bin_Values[5][5][2]   = 3062;
z_pT_Bin_Borders[5][6][0]   = 0.72;	z_pT_Bin_Borders[5][6][1]   = 0.49;	z_pT_Bin_Borders[5][6][2]   = 0.98;	z_pT_Bin_Borders[5][6][3]   = 0.65;	Phi_h_Bin_Values[5][6][0]   =  24;	Phi_h_Bin_Values[5][6][1]   = 120;	Phi_h_Bin_Values[5][6][2]   = 3086;
z_pT_Bin_Borders[5][7][0]   = 0.49;	z_pT_Bin_Borders[5][7][1]   = 0.38;	z_pT_Bin_Borders[5][7][2]   = 0.22;	z_pT_Bin_Borders[5][7][3]   = 0.05;	Phi_h_Bin_Values[5][7][0]   =  24;	Phi_h_Bin_Values[5][7][1]   = 144;	Phi_h_Bin_Values[5][7][2]   = 3110;
z_pT_Bin_Borders[5][8][0]   = 0.49;	z_pT_Bin_Borders[5][8][1]   = 0.38;	z_pT_Bin_Borders[5][8][2]   = 0.32;	z_pT_Bin_Borders[5][8][3]   = 0.22;	Phi_h_Bin_Values[5][8][0]   =  24;	Phi_h_Bin_Values[5][8][1]   = 168;	Phi_h_Bin_Values[5][8][2]   = 3134;
z_pT_Bin_Borders[5][9][0]   = 0.49;	z_pT_Bin_Borders[5][9][1]   = 0.38;	z_pT_Bin_Borders[5][9][2]   = 0.41;	z_pT_Bin_Borders[5][9][3]   = 0.32;	Phi_h_Bin_Values[5][9][0]   =  24;	Phi_h_Bin_Values[5][9][1]   = 192;	Phi_h_Bin_Values[5][9][2]   = 3158;
z_pT_Bin_Borders[5][10][0]  = 0.49;	z_pT_Bin_Borders[5][10][1]  = 0.38;	z_pT_Bin_Borders[5][10][2]  = 0.51;	z_pT_Bin_Borders[5][10][3]  = 0.41;	Phi_h_Bin_Values[5][10][0]  =  24;	Phi_h_Bin_Values[5][10][1]  = 216;	Phi_h_Bin_Values[5][10][2]  = 3182;
z_pT_Bin_Borders[5][11][0]  = 0.49;	z_pT_Bin_Borders[5][11][1]  = 0.38;	z_pT_Bin_Borders[5][11][2]  = 0.65;	z_pT_Bin_Borders[5][11][3]  = 0.51;	Phi_h_Bin_Values[5][11][0]  =  24;	Phi_h_Bin_Values[5][11][1]  = 240;	Phi_h_Bin_Values[5][11][2]  = 3206;
z_pT_Bin_Borders[5][12][0]  = 0.49;	z_pT_Bin_Borders[5][12][1]  = 0.38;	z_pT_Bin_Borders[5][12][2]  = 0.98;	z_pT_Bin_Borders[5][12][3]  = 0.65;	Phi_h_Bin_Values[5][12][0]  =  24;	Phi_h_Bin_Values[5][12][1]  = 264;	Phi_h_Bin_Values[5][12][2]  = 3230;
z_pT_Bin_Borders[5][13][0]  = 0.38;	z_pT_Bin_Borders[5][13][1]  = 0.3;	z_pT_Bin_Borders[5][13][2]  = 0.22;	z_pT_Bin_Borders[5][13][3]  = 0.05;	Phi_h_Bin_Values[5][13][0]  =  24;	Phi_h_Bin_Values[5][13][1]  = 288;	Phi_h_Bin_Values[5][13][2]  = 3254;
z_pT_Bin_Borders[5][14][0]  = 0.38;	z_pT_Bin_Borders[5][14][1]  = 0.3;	z_pT_Bin_Borders[5][14][2]  = 0.32;	z_pT_Bin_Borders[5][14][3]  = 0.22;	Phi_h_Bin_Values[5][14][0]  =  24;	Phi_h_Bin_Values[5][14][1]  = 312;	Phi_h_Bin_Values[5][14][2]  = 3278;
z_pT_Bin_Borders[5][15][0]  = 0.38;	z_pT_Bin_Borders[5][15][1]  = 0.3;	z_pT_Bin_Borders[5][15][2]  = 0.41;	z_pT_Bin_Borders[5][15][3]  = 0.32;	Phi_h_Bin_Values[5][15][0]  =  24;	Phi_h_Bin_Values[5][15][1]  = 336;	Phi_h_Bin_Values[5][15][2]  = 3302;
z_pT_Bin_Borders[5][16][0]  = 0.38;	z_pT_Bin_Borders[5][16][1]  = 0.3;	z_pT_Bin_Borders[5][16][2]  = 0.51;	z_pT_Bin_Borders[5][16][3]  = 0.41;	Phi_h_Bin_Values[5][16][0]  =  24;	Phi_h_Bin_Values[5][16][1]  = 360;	Phi_h_Bin_Values[5][16][2]  = 3326;
z_pT_Bin_Borders[5][17][0]  = 0.38;	z_pT_Bin_Borders[5][17][1]  = 0.3;	z_pT_Bin_Borders[5][17][2]  = 0.65;	z_pT_Bin_Borders[5][17][3]  = 0.51;	Phi_h_Bin_Values[5][17][0]  =  24;	Phi_h_Bin_Values[5][17][1]  = 384;	Phi_h_Bin_Values[5][17][2]  = 3350;
z_pT_Bin_Borders[5][18][0]  = 0.38;	z_pT_Bin_Borders[5][18][1]  = 0.3;	z_pT_Bin_Borders[5][18][2]  = 0.98;	z_pT_Bin_Borders[5][18][3]  = 0.65;	Phi_h_Bin_Values[5][18][0]  =  24;	Phi_h_Bin_Values[5][18][1]  = 408;	Phi_h_Bin_Values[5][18][2]  = 3374;
z_pT_Bin_Borders[5][19][0]  = 0.3;	z_pT_Bin_Borders[5][19][1]  = 0.24;	z_pT_Bin_Borders[5][19][2]  = 0.22;	z_pT_Bin_Borders[5][19][3]  = 0.05;	Phi_h_Bin_Values[5][19][0]  =  24;	Phi_h_Bin_Values[5][19][1]  = 432;	Phi_h_Bin_Values[5][19][2]  = 3398;
z_pT_Bin_Borders[5][20][0]  = 0.3;	z_pT_Bin_Borders[5][20][1]  = 0.24;	z_pT_Bin_Borders[5][20][2]  = 0.32;	z_pT_Bin_Borders[5][20][3]  = 0.22;	Phi_h_Bin_Values[5][20][0]  =  24;	Phi_h_Bin_Values[5][20][1]  = 456;	Phi_h_Bin_Values[5][20][2]  = 3422;
z_pT_Bin_Borders[5][21][0]  = 0.3;	z_pT_Bin_Borders[5][21][1]  = 0.24;	z_pT_Bin_Borders[5][21][2]  = 0.41;	z_pT_Bin_Borders[5][21][3]  = 0.32;	Phi_h_Bin_Values[5][21][0]  =  24;	Phi_h_Bin_Values[5][21][1]  = 480;	Phi_h_Bin_Values[5][21][2]  = 3446;
z_pT_Bin_Borders[5][22][0]  = 0.3;	z_pT_Bin_Borders[5][22][1]  = 0.24;	z_pT_Bin_Borders[5][22][2]  = 0.51;	z_pT_Bin_Borders[5][22][3]  = 0.41;	Phi_h_Bin_Values[5][22][0]  =  24;	Phi_h_Bin_Values[5][22][1]  = 504;	Phi_h_Bin_Values[5][22][2]  = 3470;
z_pT_Bin_Borders[5][23][0]  = 0.3;	z_pT_Bin_Borders[5][23][1]  = 0.24;	z_pT_Bin_Borders[5][23][2]  = 0.65;	z_pT_Bin_Borders[5][23][3]  = 0.51;	Phi_h_Bin_Values[5][23][0]  =  24;	Phi_h_Bin_Values[5][23][1]  = 528;	Phi_h_Bin_Values[5][23][2]  = 3494;
z_pT_Bin_Borders[5][24][0]  = 0.3;	z_pT_Bin_Borders[5][24][1]  = 0.24;	z_pT_Bin_Borders[5][24][2]  = 0.98;	z_pT_Bin_Borders[5][24][3]  = 0.65;	Phi_h_Bin_Values[5][24][0]  =  1;	Phi_h_Bin_Values[5][24][1]  = 552;	Phi_h_Bin_Values[5][24][2]  = 3518;
z_pT_Bin_Borders[5][25][0]  = 0.24;	z_pT_Bin_Borders[5][25][1]  = 0.2;	z_pT_Bin_Borders[5][25][2]  = 0.22;	z_pT_Bin_Borders[5][25][3]  = 0.05;	Phi_h_Bin_Values[5][25][0]  =  24;	Phi_h_Bin_Values[5][25][1]  = 553;	Phi_h_Bin_Values[5][25][2]  = 3519;
z_pT_Bin_Borders[5][26][0]  = 0.24;	z_pT_Bin_Borders[5][26][1]  = 0.2;	z_pT_Bin_Borders[5][26][2]  = 0.32;	z_pT_Bin_Borders[5][26][3]  = 0.22;	Phi_h_Bin_Values[5][26][0]  =  24;	Phi_h_Bin_Values[5][26][1]  = 577;	Phi_h_Bin_Values[5][26][2]  = 3543;
z_pT_Bin_Borders[5][27][0]  = 0.24;	z_pT_Bin_Borders[5][27][1]  = 0.2;	z_pT_Bin_Borders[5][27][2]  = 0.41;	z_pT_Bin_Borders[5][27][3]  = 0.32;	Phi_h_Bin_Values[5][27][0]  =  24;	Phi_h_Bin_Values[5][27][1]  = 601;	Phi_h_Bin_Values[5][27][2]  = 3567;
z_pT_Bin_Borders[5][28][0]  = 0.24;	z_pT_Bin_Borders[5][28][1]  = 0.2;	z_pT_Bin_Borders[5][28][2]  = 0.51;	z_pT_Bin_Borders[5][28][3]  = 0.41;	Phi_h_Bin_Values[5][28][0]  =  24;	Phi_h_Bin_Values[5][28][1]  = 625;	Phi_h_Bin_Values[5][28][2]  = 3591;
z_pT_Bin_Borders[5][29][0]  = 0.24;	z_pT_Bin_Borders[5][29][1]  = 0.2;	z_pT_Bin_Borders[5][29][2]  = 0.65;	z_pT_Bin_Borders[5][29][3]  = 0.51;	Phi_h_Bin_Values[5][29][0]  =  24;	Phi_h_Bin_Values[5][29][1]  = 649;	Phi_h_Bin_Values[5][29][2]  = 3615;
z_pT_Bin_Borders[5][30][0]  = 0.24;	z_pT_Bin_Borders[5][30][1]  = 0.2;	z_pT_Bin_Borders[5][30][2]  = 0.98;	z_pT_Bin_Borders[5][30][3]  = 0.65;	Phi_h_Bin_Values[5][30][0]  =  1;	Phi_h_Bin_Values[5][30][1]  = 673;	Phi_h_Bin_Values[5][30][2]  = 3639;
z_pT_Bin_Borders[5][31][0]  = 0.2;	z_pT_Bin_Borders[5][31][1]  = 0.16;	z_pT_Bin_Borders[5][31][2]  = 0.22;	z_pT_Bin_Borders[5][31][3]  = 0.05;	Phi_h_Bin_Values[5][31][0]  =  24;	Phi_h_Bin_Values[5][31][1]  = 674;	Phi_h_Bin_Values[5][31][2]  = 3640;
z_pT_Bin_Borders[5][32][0]  = 0.2;	z_pT_Bin_Borders[5][32][1]  = 0.16;	z_pT_Bin_Borders[5][32][2]  = 0.32;	z_pT_Bin_Borders[5][32][3]  = 0.22;	Phi_h_Bin_Values[5][32][0]  =  24;	Phi_h_Bin_Values[5][32][1]  = 698;	Phi_h_Bin_Values[5][32][2]  = 3664;
z_pT_Bin_Borders[5][33][0]  = 0.2;	z_pT_Bin_Borders[5][33][1]  = 0.16;	z_pT_Bin_Borders[5][33][2]  = 0.41;	z_pT_Bin_Borders[5][33][3]  = 0.32;	Phi_h_Bin_Values[5][33][0]  =  24;	Phi_h_Bin_Values[5][33][1]  = 722;	Phi_h_Bin_Values[5][33][2]  = 3688;
z_pT_Bin_Borders[5][34][0]  = 0.2;	z_pT_Bin_Borders[5][34][1]  = 0.16;	z_pT_Bin_Borders[5][34][2]  = 0.51;	z_pT_Bin_Borders[5][34][3]  = 0.41;	Phi_h_Bin_Values[5][34][0]  =  24;	Phi_h_Bin_Values[5][34][1]  = 746;	Phi_h_Bin_Values[5][34][2]  = 3712;
z_pT_Bin_Borders[5][35][0]  = 0.2;	z_pT_Bin_Borders[5][35][1]  = 0.16;	z_pT_Bin_Borders[5][35][2]  = 0.65;	z_pT_Bin_Borders[5][35][3]  = 0.51;	Phi_h_Bin_Values[5][35][0]  =  1;	Phi_h_Bin_Values[5][35][1]  = 770;	Phi_h_Bin_Values[5][35][2]  = 3736;
z_pT_Bin_Borders[5][36][0]  = 0.2;	z_pT_Bin_Borders[5][36][1]  = 0.16;	z_pT_Bin_Borders[5][36][2]  = 0.98;	z_pT_Bin_Borders[5][36][3]  = 0.65;	Phi_h_Bin_Values[5][36][0]  =  1;	Phi_h_Bin_Values[5][36][1]  = 771;	Phi_h_Bin_Values[5][36][2]  = 3737;
z_pT_Bin_Borders[6][1][0]   = 0.72;	z_pT_Bin_Borders[6][1][1]   = 0.45;	z_pT_Bin_Borders[6][1][2]   = 0.22;	z_pT_Bin_Borders[6][1][3]   = 0.05;	Phi_h_Bin_Values[6][1][0]   =  24;	Phi_h_Bin_Values[6][1][1]   = 0;	Phi_h_Bin_Values[6][1][2]   = 3738;
z_pT_Bin_Borders[6][2][0]   = 0.72;	z_pT_Bin_Borders[6][2][1]   = 0.45;	z_pT_Bin_Borders[6][2][2]   = 0.32;	z_pT_Bin_Borders[6][2][3]   = 0.22;	Phi_h_Bin_Values[6][2][0]   =  24;	Phi_h_Bin_Values[6][2][1]   = 24;	Phi_h_Bin_Values[6][2][2]   = 3762;
z_pT_Bin_Borders[6][3][0]   = 0.72;	z_pT_Bin_Borders[6][3][1]   = 0.45;	z_pT_Bin_Borders[6][3][2]   = 0.41;	z_pT_Bin_Borders[6][3][3]   = 0.32;	Phi_h_Bin_Values[6][3][0]   =  24;	Phi_h_Bin_Values[6][3][1]   = 48;	Phi_h_Bin_Values[6][3][2]   = 3786;
z_pT_Bin_Borders[6][4][0]   = 0.72;	z_pT_Bin_Borders[6][4][1]   = 0.45;	z_pT_Bin_Borders[6][4][2]   = 0.51;	z_pT_Bin_Borders[6][4][3]   = 0.41;	Phi_h_Bin_Values[6][4][0]   =  24;	Phi_h_Bin_Values[6][4][1]   = 72;	Phi_h_Bin_Values[6][4][2]   = 3810;
z_pT_Bin_Borders[6][5][0]   = 0.72;	z_pT_Bin_Borders[6][5][1]   = 0.45;	z_pT_Bin_Borders[6][5][2]   = 0.65;	z_pT_Bin_Borders[6][5][3]   = 0.51;	Phi_h_Bin_Values[6][5][0]   =  24;	Phi_h_Bin_Values[6][5][1]   = 96;	Phi_h_Bin_Values[6][5][2]   = 3834;
z_pT_Bin_Borders[6][6][0]   = 0.72;	z_pT_Bin_Borders[6][6][1]   = 0.45;	z_pT_Bin_Borders[6][6][2]   = 1.0;	z_pT_Bin_Borders[6][6][3]   = 0.65;	Phi_h_Bin_Values[6][6][0]   =  24;	Phi_h_Bin_Values[6][6][1]   = 120;	Phi_h_Bin_Values[6][6][2]   = 3858;
z_pT_Bin_Borders[6][7][0]   = 0.45;	z_pT_Bin_Borders[6][7][1]   = 0.35;	z_pT_Bin_Borders[6][7][2]   = 0.22;	z_pT_Bin_Borders[6][7][3]   = 0.05;	Phi_h_Bin_Values[6][7][0]   =  24;	Phi_h_Bin_Values[6][7][1]   = 144;	Phi_h_Bin_Values[6][7][2]   = 3882;
z_pT_Bin_Borders[6][8][0]   = 0.45;	z_pT_Bin_Borders[6][8][1]   = 0.35;	z_pT_Bin_Borders[6][8][2]   = 0.32;	z_pT_Bin_Borders[6][8][3]   = 0.22;	Phi_h_Bin_Values[6][8][0]   =  24;	Phi_h_Bin_Values[6][8][1]   = 168;	Phi_h_Bin_Values[6][8][2]   = 3906;
z_pT_Bin_Borders[6][9][0]   = 0.45;	z_pT_Bin_Borders[6][9][1]   = 0.35;	z_pT_Bin_Borders[6][9][2]   = 0.41;	z_pT_Bin_Borders[6][9][3]   = 0.32;	Phi_h_Bin_Values[6][9][0]   =  24;	Phi_h_Bin_Values[6][9][1]   = 192;	Phi_h_Bin_Values[6][9][2]   = 3930;
z_pT_Bin_Borders[6][10][0]  = 0.45;	z_pT_Bin_Borders[6][10][1]  = 0.35;	z_pT_Bin_Borders[6][10][2]  = 0.51;	z_pT_Bin_Borders[6][10][3]  = 0.41;	Phi_h_Bin_Values[6][10][0]  =  24;	Phi_h_Bin_Values[6][10][1]  = 216;	Phi_h_Bin_Values[6][10][2]  = 3954;
z_pT_Bin_Borders[6][11][0]  = 0.45;	z_pT_Bin_Borders[6][11][1]  = 0.35;	z_pT_Bin_Borders[6][11][2]  = 0.65;	z_pT_Bin_Borders[6][11][3]  = 0.51;	Phi_h_Bin_Values[6][11][0]  =  24;	Phi_h_Bin_Values[6][11][1]  = 240;	Phi_h_Bin_Values[6][11][2]  = 3978;
z_pT_Bin_Borders[6][12][0]  = 0.45;	z_pT_Bin_Borders[6][12][1]  = 0.35;	z_pT_Bin_Borders[6][12][2]  = 1.0;	z_pT_Bin_Borders[6][12][3]  = 0.65;	Phi_h_Bin_Values[6][12][0]  =  24;	Phi_h_Bin_Values[6][12][1]  = 264;	Phi_h_Bin_Values[6][12][2]  = 4002;
z_pT_Bin_Borders[6][13][0]  = 0.35;	z_pT_Bin_Borders[6][13][1]  = 0.28;	z_pT_Bin_Borders[6][13][2]  = 0.22;	z_pT_Bin_Borders[6][13][3]  = 0.05;	Phi_h_Bin_Values[6][13][0]  =  24;	Phi_h_Bin_Values[6][13][1]  = 288;	Phi_h_Bin_Values[6][13][2]  = 4026;
z_pT_Bin_Borders[6][14][0]  = 0.35;	z_pT_Bin_Borders[6][14][1]  = 0.28;	z_pT_Bin_Borders[6][14][2]  = 0.32;	z_pT_Bin_Borders[6][14][3]  = 0.22;	Phi_h_Bin_Values[6][14][0]  =  24;	Phi_h_Bin_Values[6][14][1]  = 312;	Phi_h_Bin_Values[6][14][2]  = 4050;
z_pT_Bin_Borders[6][15][0]  = 0.35;	z_pT_Bin_Borders[6][15][1]  = 0.28;	z_pT_Bin_Borders[6][15][2]  = 0.41;	z_pT_Bin_Borders[6][15][3]  = 0.32;	Phi_h_Bin_Values[6][15][0]  =  24;	Phi_h_Bin_Values[6][15][1]  = 336;	Phi_h_Bin_Values[6][15][2]  = 4074;
z_pT_Bin_Borders[6][16][0]  = 0.35;	z_pT_Bin_Borders[6][16][1]  = 0.28;	z_pT_Bin_Borders[6][16][2]  = 0.51;	z_pT_Bin_Borders[6][16][3]  = 0.41;	Phi_h_Bin_Values[6][16][0]  =  24;	Phi_h_Bin_Values[6][16][1]  = 360;	Phi_h_Bin_Values[6][16][2]  = 4098;
z_pT_Bin_Borders[6][17][0]  = 0.35;	z_pT_Bin_Borders[6][17][1]  = 0.28;	z_pT_Bin_Borders[6][17][2]  = 0.65;	z_pT_Bin_Borders[6][17][3]  = 0.51;	Phi_h_Bin_Values[6][17][0]  =  24;	Phi_h_Bin_Values[6][17][1]  = 384;	Phi_h_Bin_Values[6][17][2]  = 4122;
z_pT_Bin_Borders[6][18][0]  = 0.35;	z_pT_Bin_Borders[6][18][1]  = 0.28;	z_pT_Bin_Borders[6][18][2]  = 1.0;	z_pT_Bin_Borders[6][18][3]  = 0.65;	Phi_h_Bin_Values[6][18][0]  =  1;	Phi_h_Bin_Values[6][18][1]  = 408;	Phi_h_Bin_Values[6][18][2]  = 4146;
z_pT_Bin_Borders[6][19][0]  = 0.28;	z_pT_Bin_Borders[6][19][1]  = 0.23;	z_pT_Bin_Borders[6][19][2]  = 0.22;	z_pT_Bin_Borders[6][19][3]  = 0.05;	Phi_h_Bin_Values[6][19][0]  =  24;	Phi_h_Bin_Values[6][19][1]  = 409;	Phi_h_Bin_Values[6][19][2]  = 4147;
z_pT_Bin_Borders[6][20][0]  = 0.28;	z_pT_Bin_Borders[6][20][1]  = 0.23;	z_pT_Bin_Borders[6][20][2]  = 0.32;	z_pT_Bin_Borders[6][20][3]  = 0.22;	Phi_h_Bin_Values[6][20][0]  =  24;	Phi_h_Bin_Values[6][20][1]  = 433;	Phi_h_Bin_Values[6][20][2]  = 4171;
z_pT_Bin_Borders[6][21][0]  = 0.28;	z_pT_Bin_Borders[6][21][1]  = 0.23;	z_pT_Bin_Borders[6][21][2]  = 0.41;	z_pT_Bin_Borders[6][21][3]  = 0.32;	Phi_h_Bin_Values[6][21][0]  =  24;	Phi_h_Bin_Values[6][21][1]  = 457;	Phi_h_Bin_Values[6][21][2]  = 4195;
z_pT_Bin_Borders[6][22][0]  = 0.28;	z_pT_Bin_Borders[6][22][1]  = 0.23;	z_pT_Bin_Borders[6][22][2]  = 0.51;	z_pT_Bin_Borders[6][22][3]  = 0.41;	Phi_h_Bin_Values[6][22][0]  =  24;	Phi_h_Bin_Values[6][22][1]  = 481;	Phi_h_Bin_Values[6][22][2]  = 4219;
z_pT_Bin_Borders[6][23][0]  = 0.28;	z_pT_Bin_Borders[6][23][1]  = 0.23;	z_pT_Bin_Borders[6][23][2]  = 0.65;	z_pT_Bin_Borders[6][23][3]  = 0.51;	Phi_h_Bin_Values[6][23][0]  =  24;	Phi_h_Bin_Values[6][23][1]  = 505;	Phi_h_Bin_Values[6][23][2]  = 4243;
z_pT_Bin_Borders[6][24][0]  = 0.28;	z_pT_Bin_Borders[6][24][1]  = 0.23;	z_pT_Bin_Borders[6][24][2]  = 1.0;	z_pT_Bin_Borders[6][24][3]  = 0.65;	Phi_h_Bin_Values[6][24][0]  =  1;	Phi_h_Bin_Values[6][24][1]  = 529;	Phi_h_Bin_Values[6][24][2]  = 4267;
z_pT_Bin_Borders[6][25][0]  = 0.23;	z_pT_Bin_Borders[6][25][1]  = 0.18;	z_pT_Bin_Borders[6][25][2]  = 0.22;	z_pT_Bin_Borders[6][25][3]  = 0.05;	Phi_h_Bin_Values[6][25][0]  =  24;	Phi_h_Bin_Values[6][25][1]  = 530;	Phi_h_Bin_Values[6][25][2]  = 4268;
z_pT_Bin_Borders[6][26][0]  = 0.23;	z_pT_Bin_Borders[6][26][1]  = 0.18;	z_pT_Bin_Borders[6][26][2]  = 0.32;	z_pT_Bin_Borders[6][26][3]  = 0.22;	Phi_h_Bin_Values[6][26][0]  =  24;	Phi_h_Bin_Values[6][26][1]  = 554;	Phi_h_Bin_Values[6][26][2]  = 4292;
z_pT_Bin_Borders[6][27][0]  = 0.23;	z_pT_Bin_Borders[6][27][1]  = 0.18;	z_pT_Bin_Borders[6][27][2]  = 0.41;	z_pT_Bin_Borders[6][27][3]  = 0.32;	Phi_h_Bin_Values[6][27][0]  =  24;	Phi_h_Bin_Values[6][27][1]  = 578;	Phi_h_Bin_Values[6][27][2]  = 4316;
z_pT_Bin_Borders[6][28][0]  = 0.23;	z_pT_Bin_Borders[6][28][1]  = 0.18;	z_pT_Bin_Borders[6][28][2]  = 0.51;	z_pT_Bin_Borders[6][28][3]  = 0.41;	Phi_h_Bin_Values[6][28][0]  =  24;	Phi_h_Bin_Values[6][28][1]  = 602;	Phi_h_Bin_Values[6][28][2]  = 4340;
z_pT_Bin_Borders[6][29][0]  = 0.23;	z_pT_Bin_Borders[6][29][1]  = 0.18;	z_pT_Bin_Borders[6][29][2]  = 0.65;	z_pT_Bin_Borders[6][29][3]  = 0.51;	Phi_h_Bin_Values[6][29][0]  =  1;	Phi_h_Bin_Values[6][29][1]  = 626;	Phi_h_Bin_Values[6][29][2]  = 4364;
z_pT_Bin_Borders[6][30][0]  = 0.23;	z_pT_Bin_Borders[6][30][1]  = 0.18;	z_pT_Bin_Borders[6][30][2]  = 1.0;	z_pT_Bin_Borders[6][30][3]  = 0.65;	Phi_h_Bin_Values[6][30][0]  =  1;	Phi_h_Bin_Values[6][30][1]  = 627;	Phi_h_Bin_Values[6][30][2]  = 4365;
z_pT_Bin_Borders[7][1][0]   = 0.77;	z_pT_Bin_Borders[7][1][1]   = 0.58;	z_pT_Bin_Borders[7][1][2]   = 0.2;	z_pT_Bin_Borders[7][1][3]   = 0.05;	Phi_h_Bin_Values[7][1][0]   =  24;	Phi_h_Bin_Values[7][1][1]   = 0;	Phi_h_Bin_Values[7][1][2]   = 4366;
z_pT_Bin_Borders[7][2][0]   = 0.77;	z_pT_Bin_Borders[7][2][1]   = 0.58;	z_pT_Bin_Borders[7][2][2]   = 0.29;	z_pT_Bin_Borders[7][2][3]   = 0.2;	Phi_h_Bin_Values[7][2][0]   =  24;	Phi_h_Bin_Values[7][2][1]   = 24;	Phi_h_Bin_Values[7][2][2]   = 4390;
z_pT_Bin_Borders[7][3][0]   = 0.77;	z_pT_Bin_Borders[7][3][1]   = 0.58;	z_pT_Bin_Borders[7][3][2]   = 0.38;	z_pT_Bin_Borders[7][3][3]   = 0.29;	Phi_h_Bin_Values[7][3][0]   =  24;	Phi_h_Bin_Values[7][3][1]   = 48;	Phi_h_Bin_Values[7][3][2]   = 4414;
z_pT_Bin_Borders[7][4][0]   = 0.77;	z_pT_Bin_Borders[7][4][1]   = 0.58;	z_pT_Bin_Borders[7][4][2]   = 0.48;	z_pT_Bin_Borders[7][4][3]   = 0.38;	Phi_h_Bin_Values[7][4][0]   =  24;	Phi_h_Bin_Values[7][4][1]   = 72;	Phi_h_Bin_Values[7][4][2]   = 4438;
z_pT_Bin_Borders[7][5][0]   = 0.77;	z_pT_Bin_Borders[7][5][1]   = 0.58;	z_pT_Bin_Borders[7][5][2]   = 0.6;	z_pT_Bin_Borders[7][5][3]   = 0.48;	Phi_h_Bin_Values[7][5][0]   =  24;	Phi_h_Bin_Values[7][5][1]   = 96;	Phi_h_Bin_Values[7][5][2]   = 4462;
z_pT_Bin_Borders[7][6][0]   = 0.77;	z_pT_Bin_Borders[7][6][1]   = 0.58;	z_pT_Bin_Borders[7][6][2]   = 0.83;	z_pT_Bin_Borders[7][6][3]   = 0.6;	Phi_h_Bin_Values[7][6][0]   =  1;	Phi_h_Bin_Values[7][6][1]   = 120;	Phi_h_Bin_Values[7][6][2]   = 4486;
z_pT_Bin_Borders[7][7][0]   = 0.58;	z_pT_Bin_Borders[7][7][1]   = 0.45;	z_pT_Bin_Borders[7][7][2]   = 0.2;	z_pT_Bin_Borders[7][7][3]   = 0.05;	Phi_h_Bin_Values[7][7][0]   =  24;	Phi_h_Bin_Values[7][7][1]   = 121;	Phi_h_Bin_Values[7][7][2]   = 4487;
z_pT_Bin_Borders[7][8][0]   = 0.58;	z_pT_Bin_Borders[7][8][1]   = 0.45;	z_pT_Bin_Borders[7][8][2]   = 0.29;	z_pT_Bin_Borders[7][8][3]   = 0.2;	Phi_h_Bin_Values[7][8][0]   =  24;	Phi_h_Bin_Values[7][8][1]   = 145;	Phi_h_Bin_Values[7][8][2]   = 4511;
z_pT_Bin_Borders[7][9][0]   = 0.58;	z_pT_Bin_Borders[7][9][1]   = 0.45;	z_pT_Bin_Borders[7][9][2]   = 0.38;	z_pT_Bin_Borders[7][9][3]   = 0.29;	Phi_h_Bin_Values[7][9][0]   =  24;	Phi_h_Bin_Values[7][9][1]   = 169;	Phi_h_Bin_Values[7][9][2]   = 4535;
z_pT_Bin_Borders[7][10][0]  = 0.58;	z_pT_Bin_Borders[7][10][1]  = 0.45;	z_pT_Bin_Borders[7][10][2]  = 0.48;	z_pT_Bin_Borders[7][10][3]  = 0.38;	Phi_h_Bin_Values[7][10][0]  =  24;	Phi_h_Bin_Values[7][10][1]  = 193;	Phi_h_Bin_Values[7][10][2]  = 4559;
z_pT_Bin_Borders[7][11][0]  = 0.58;	z_pT_Bin_Borders[7][11][1]  = 0.45;	z_pT_Bin_Borders[7][11][2]  = 0.6;	z_pT_Bin_Borders[7][11][3]  = 0.48;	Phi_h_Bin_Values[7][11][0]  =  24;	Phi_h_Bin_Values[7][11][1]  = 217;	Phi_h_Bin_Values[7][11][2]  = 4583;
z_pT_Bin_Borders[7][12][0]  = 0.58;	z_pT_Bin_Borders[7][12][1]  = 0.45;	z_pT_Bin_Borders[7][12][2]  = 0.83;	z_pT_Bin_Borders[7][12][3]  = 0.6;	Phi_h_Bin_Values[7][12][0]  =  24;	Phi_h_Bin_Values[7][12][1]  = 241;	Phi_h_Bin_Values[7][12][2]  = 4607;
z_pT_Bin_Borders[7][13][0]  = 0.45;	z_pT_Bin_Borders[7][13][1]  = 0.37;	z_pT_Bin_Borders[7][13][2]  = 0.2;	z_pT_Bin_Borders[7][13][3]  = 0.05;	Phi_h_Bin_Values[7][13][0]  =  24;	Phi_h_Bin_Values[7][13][1]  = 265;	Phi_h_Bin_Values[7][13][2]  = 4631;
z_pT_Bin_Borders[7][14][0]  = 0.45;	z_pT_Bin_Borders[7][14][1]  = 0.37;	z_pT_Bin_Borders[7][14][2]  = 0.29;	z_pT_Bin_Borders[7][14][3]  = 0.2;	Phi_h_Bin_Values[7][14][0]  =  24;	Phi_h_Bin_Values[7][14][1]  = 289;	Phi_h_Bin_Values[7][14][2]  = 4655;
z_pT_Bin_Borders[7][15][0]  = 0.45;	z_pT_Bin_Borders[7][15][1]  = 0.37;	z_pT_Bin_Borders[7][15][2]  = 0.38;	z_pT_Bin_Borders[7][15][3]  = 0.29;	Phi_h_Bin_Values[7][15][0]  =  24;	Phi_h_Bin_Values[7][15][1]  = 313;	Phi_h_Bin_Values[7][15][2]  = 4679;
z_pT_Bin_Borders[7][16][0]  = 0.45;	z_pT_Bin_Borders[7][16][1]  = 0.37;	z_pT_Bin_Borders[7][16][2]  = 0.48;	z_pT_Bin_Borders[7][16][3]  = 0.38;	Phi_h_Bin_Values[7][16][0]  =  24;	Phi_h_Bin_Values[7][16][1]  = 337;	Phi_h_Bin_Values[7][16][2]  = 4703;
z_pT_Bin_Borders[7][17][0]  = 0.45;	z_pT_Bin_Borders[7][17][1]  = 0.37;	z_pT_Bin_Borders[7][17][2]  = 0.6;	z_pT_Bin_Borders[7][17][3]  = 0.48;	Phi_h_Bin_Values[7][17][0]  =  24;	Phi_h_Bin_Values[7][17][1]  = 361;	Phi_h_Bin_Values[7][17][2]  = 4727;
z_pT_Bin_Borders[7][18][0]  = 0.45;	z_pT_Bin_Borders[7][18][1]  = 0.37;	z_pT_Bin_Borders[7][18][2]  = 0.83;	z_pT_Bin_Borders[7][18][3]  = 0.6;	Phi_h_Bin_Values[7][18][0]  =  24;	Phi_h_Bin_Values[7][18][1]  = 385;	Phi_h_Bin_Values[7][18][2]  = 4751;
z_pT_Bin_Borders[7][19][0]  = 0.37;	z_pT_Bin_Borders[7][19][1]  = 0.31;	z_pT_Bin_Borders[7][19][2]  = 0.2;	z_pT_Bin_Borders[7][19][3]  = 0.05;	Phi_h_Bin_Values[7][19][0]  =  24;	Phi_h_Bin_Values[7][19][1]  = 409;	Phi_h_Bin_Values[7][19][2]  = 4775;
z_pT_Bin_Borders[7][20][0]  = 0.37;	z_pT_Bin_Borders[7][20][1]  = 0.31;	z_pT_Bin_Borders[7][20][2]  = 0.29;	z_pT_Bin_Borders[7][20][3]  = 0.2;	Phi_h_Bin_Values[7][20][0]  =  24;	Phi_h_Bin_Values[7][20][1]  = 433;	Phi_h_Bin_Values[7][20][2]  = 4799;
z_pT_Bin_Borders[7][21][0]  = 0.37;	z_pT_Bin_Borders[7][21][1]  = 0.31;	z_pT_Bin_Borders[7][21][2]  = 0.38;	z_pT_Bin_Borders[7][21][3]  = 0.29;	Phi_h_Bin_Values[7][21][0]  =  24;	Phi_h_Bin_Values[7][21][1]  = 457;	Phi_h_Bin_Values[7][21][2]  = 4823;
z_pT_Bin_Borders[7][22][0]  = 0.37;	z_pT_Bin_Borders[7][22][1]  = 0.31;	z_pT_Bin_Borders[7][22][2]  = 0.48;	z_pT_Bin_Borders[7][22][3]  = 0.38;	Phi_h_Bin_Values[7][22][0]  =  24;	Phi_h_Bin_Values[7][22][1]  = 481;	Phi_h_Bin_Values[7][22][2]  = 4847;
z_pT_Bin_Borders[7][23][0]  = 0.37;	z_pT_Bin_Borders[7][23][1]  = 0.31;	z_pT_Bin_Borders[7][23][2]  = 0.6;	z_pT_Bin_Borders[7][23][3]  = 0.48;	Phi_h_Bin_Values[7][23][0]  =  24;	Phi_h_Bin_Values[7][23][1]  = 505;	Phi_h_Bin_Values[7][23][2]  = 4871;
z_pT_Bin_Borders[7][24][0]  = 0.37;	z_pT_Bin_Borders[7][24][1]  = 0.31;	z_pT_Bin_Borders[7][24][2]  = 0.83;	z_pT_Bin_Borders[7][24][3]  = 0.6;	Phi_h_Bin_Values[7][24][0]  =  24;	Phi_h_Bin_Values[7][24][1]  = 529;	Phi_h_Bin_Values[7][24][2]  = 4895;
z_pT_Bin_Borders[7][25][0]  = 0.31;	z_pT_Bin_Borders[7][25][1]  = 0.27;	z_pT_Bin_Borders[7][25][2]  = 0.2;	z_pT_Bin_Borders[7][25][3]  = 0.05;	Phi_h_Bin_Values[7][25][0]  =  24;	Phi_h_Bin_Values[7][25][1]  = 553;	Phi_h_Bin_Values[7][25][2]  = 4919;
z_pT_Bin_Borders[7][26][0]  = 0.31;	z_pT_Bin_Borders[7][26][1]  = 0.27;	z_pT_Bin_Borders[7][26][2]  = 0.29;	z_pT_Bin_Borders[7][26][3]  = 0.2;	Phi_h_Bin_Values[7][26][0]  =  24;	Phi_h_Bin_Values[7][26][1]  = 577;	Phi_h_Bin_Values[7][26][2]  = 4943;
z_pT_Bin_Borders[7][27][0]  = 0.31;	z_pT_Bin_Borders[7][27][1]  = 0.27;	z_pT_Bin_Borders[7][27][2]  = 0.38;	z_pT_Bin_Borders[7][27][3]  = 0.29;	Phi_h_Bin_Values[7][27][0]  =  24;	Phi_h_Bin_Values[7][27][1]  = 601;	Phi_h_Bin_Values[7][27][2]  = 4967;
z_pT_Bin_Borders[7][28][0]  = 0.31;	z_pT_Bin_Borders[7][28][1]  = 0.27;	z_pT_Bin_Borders[7][28][2]  = 0.48;	z_pT_Bin_Borders[7][28][3]  = 0.38;	Phi_h_Bin_Values[7][28][0]  =  24;	Phi_h_Bin_Values[7][28][1]  = 625;	Phi_h_Bin_Values[7][28][2]  = 4991;
z_pT_Bin_Borders[7][29][0]  = 0.31;	z_pT_Bin_Borders[7][29][1]  = 0.27;	z_pT_Bin_Borders[7][29][2]  = 0.6;	z_pT_Bin_Borders[7][29][3]  = 0.48;	Phi_h_Bin_Values[7][29][0]  =  24;	Phi_h_Bin_Values[7][29][1]  = 649;	Phi_h_Bin_Values[7][29][2]  = 5015;
z_pT_Bin_Borders[7][30][0]  = 0.31;	z_pT_Bin_Borders[7][30][1]  = 0.27;	z_pT_Bin_Borders[7][30][2]  = 0.83;	z_pT_Bin_Borders[7][30][3]  = 0.6;	Phi_h_Bin_Values[7][30][0]  =  1;	Phi_h_Bin_Values[7][30][1]  = 673;	Phi_h_Bin_Values[7][30][2]  = 5039;
z_pT_Bin_Borders[7][31][0]  = 0.27;	z_pT_Bin_Borders[7][31][1]  = 0.22;	z_pT_Bin_Borders[7][31][2]  = 0.2;	z_pT_Bin_Borders[7][31][3]  = 0.05;	Phi_h_Bin_Values[7][31][0]  =  24;	Phi_h_Bin_Values[7][31][1]  = 674;	Phi_h_Bin_Values[7][31][2]  = 5040;
z_pT_Bin_Borders[7][32][0]  = 0.27;	z_pT_Bin_Borders[7][32][1]  = 0.22;	z_pT_Bin_Borders[7][32][2]  = 0.29;	z_pT_Bin_Borders[7][32][3]  = 0.2;	Phi_h_Bin_Values[7][32][0]  =  24;	Phi_h_Bin_Values[7][32][1]  = 698;	Phi_h_Bin_Values[7][32][2]  = 5064;
z_pT_Bin_Borders[7][33][0]  = 0.27;	z_pT_Bin_Borders[7][33][1]  = 0.22;	z_pT_Bin_Borders[7][33][2]  = 0.38;	z_pT_Bin_Borders[7][33][3]  = 0.29;	Phi_h_Bin_Values[7][33][0]  =  24;	Phi_h_Bin_Values[7][33][1]  = 722;	Phi_h_Bin_Values[7][33][2]  = 5088;
z_pT_Bin_Borders[7][34][0]  = 0.27;	z_pT_Bin_Borders[7][34][1]  = 0.22;	z_pT_Bin_Borders[7][34][2]  = 0.48;	z_pT_Bin_Borders[7][34][3]  = 0.38;	Phi_h_Bin_Values[7][34][0]  =  24;	Phi_h_Bin_Values[7][34][1]  = 746;	Phi_h_Bin_Values[7][34][2]  = 5112;
z_pT_Bin_Borders[7][35][0]  = 0.27;	z_pT_Bin_Borders[7][35][1]  = 0.22;	z_pT_Bin_Borders[7][35][2]  = 0.6;	z_pT_Bin_Borders[7][35][3]  = 0.48;	Phi_h_Bin_Values[7][35][0]  =  24;	Phi_h_Bin_Values[7][35][1]  = 770;	Phi_h_Bin_Values[7][35][2]  = 5136;
z_pT_Bin_Borders[7][36][0]  = 0.27;	z_pT_Bin_Borders[7][36][1]  = 0.22;	z_pT_Bin_Borders[7][36][2]  = 0.83;	z_pT_Bin_Borders[7][36][3]  = 0.6;	Phi_h_Bin_Values[7][36][0]  =  1;	Phi_h_Bin_Values[7][36][1]  = 794;	Phi_h_Bin_Values[7][36][2]  = 5160;
z_pT_Bin_Borders[8][1][0]   = 0.7;	z_pT_Bin_Borders[8][1][1]   = 0.56;	z_pT_Bin_Borders[8][1][2]   = 0.2;	z_pT_Bin_Borders[8][1][3]   = 0.05;	Phi_h_Bin_Values[8][1][0]   =  24;	Phi_h_Bin_Values[8][1][1]   = 0;	Phi_h_Bin_Values[8][1][2]   = 5161;
z_pT_Bin_Borders[8][2][0]   = 0.7;	z_pT_Bin_Borders[8][2][1]   = 0.56;	z_pT_Bin_Borders[8][2][2]   = 0.29;	z_pT_Bin_Borders[8][2][3]   = 0.2;	Phi_h_Bin_Values[8][2][0]   =  24;	Phi_h_Bin_Values[8][2][1]   = 24;	Phi_h_Bin_Values[8][2][2]   = 5185;
z_pT_Bin_Borders[8][3][0]   = 0.7;	z_pT_Bin_Borders[8][3][1]   = 0.56;	z_pT_Bin_Borders[8][3][2]   = 0.37;	z_pT_Bin_Borders[8][3][3]   = 0.29;	Phi_h_Bin_Values[8][3][0]   =  24;	Phi_h_Bin_Values[8][3][1]   = 48;	Phi_h_Bin_Values[8][3][2]   = 5209;
z_pT_Bin_Borders[8][4][0]   = 0.7;	z_pT_Bin_Borders[8][4][1]   = 0.56;	z_pT_Bin_Borders[8][4][2]   = 0.46;	z_pT_Bin_Borders[8][4][3]   = 0.37;	Phi_h_Bin_Values[8][4][0]   =  24;	Phi_h_Bin_Values[8][4][1]   = 72;	Phi_h_Bin_Values[8][4][2]   = 5233;
z_pT_Bin_Borders[8][5][0]   = 0.7;	z_pT_Bin_Borders[8][5][1]   = 0.56;	z_pT_Bin_Borders[8][5][2]   = 0.6;	z_pT_Bin_Borders[8][5][3]   = 0.46;	Phi_h_Bin_Values[8][5][0]   =  24;	Phi_h_Bin_Values[8][5][1]   = 96;	Phi_h_Bin_Values[8][5][2]   = 5257;
z_pT_Bin_Borders[8][6][0]   = 0.56;	z_pT_Bin_Borders[8][6][1]   = 0.49;	z_pT_Bin_Borders[8][6][2]   = 0.2;	z_pT_Bin_Borders[8][6][3]   = 0.05;	Phi_h_Bin_Values[8][6][0]   =  24;	Phi_h_Bin_Values[8][6][1]   = 120;	Phi_h_Bin_Values[8][6][2]   = 5281;
z_pT_Bin_Borders[8][7][0]   = 0.56;	z_pT_Bin_Borders[8][7][1]   = 0.49;	z_pT_Bin_Borders[8][7][2]   = 0.29;	z_pT_Bin_Borders[8][7][3]   = 0.2;	Phi_h_Bin_Values[8][7][0]   =  24;	Phi_h_Bin_Values[8][7][1]   = 144;	Phi_h_Bin_Values[8][7][2]   = 5305;
z_pT_Bin_Borders[8][8][0]   = 0.56;	z_pT_Bin_Borders[8][8][1]   = 0.49;	z_pT_Bin_Borders[8][8][2]   = 0.37;	z_pT_Bin_Borders[8][8][3]   = 0.29;	Phi_h_Bin_Values[8][8][0]   =  24;	Phi_h_Bin_Values[8][8][1]   = 168;	Phi_h_Bin_Values[8][8][2]   = 5329;
z_pT_Bin_Borders[8][9][0]   = 0.56;	z_pT_Bin_Borders[8][9][1]   = 0.49;	z_pT_Bin_Borders[8][9][2]   = 0.46;	z_pT_Bin_Borders[8][9][3]   = 0.37;	Phi_h_Bin_Values[8][9][0]   =  24;	Phi_h_Bin_Values[8][9][1]   = 192;	Phi_h_Bin_Values[8][9][2]   = 5353;
z_pT_Bin_Borders[8][10][0]  = 0.56;	z_pT_Bin_Borders[8][10][1]  = 0.49;	z_pT_Bin_Borders[8][10][2]  = 0.6;	z_pT_Bin_Borders[8][10][3]  = 0.46;	Phi_h_Bin_Values[8][10][0]  =  24;	Phi_h_Bin_Values[8][10][1]  = 216;	Phi_h_Bin_Values[8][10][2]  = 5377;
z_pT_Bin_Borders[8][11][0]  = 0.49;	z_pT_Bin_Borders[8][11][1]  = 0.44;	z_pT_Bin_Borders[8][11][2]  = 0.2;	z_pT_Bin_Borders[8][11][3]  = 0.05;	Phi_h_Bin_Values[8][11][0]  =  24;	Phi_h_Bin_Values[8][11][1]  = 240;	Phi_h_Bin_Values[8][11][2]  = 5401;
z_pT_Bin_Borders[8][12][0]  = 0.49;	z_pT_Bin_Borders[8][12][1]  = 0.44;	z_pT_Bin_Borders[8][12][2]  = 0.29;	z_pT_Bin_Borders[8][12][3]  = 0.2;	Phi_h_Bin_Values[8][12][0]  =  24;	Phi_h_Bin_Values[8][12][1]  = 264;	Phi_h_Bin_Values[8][12][2]  = 5425;
z_pT_Bin_Borders[8][13][0]  = 0.49;	z_pT_Bin_Borders[8][13][1]  = 0.44;	z_pT_Bin_Borders[8][13][2]  = 0.37;	z_pT_Bin_Borders[8][13][3]  = 0.29;	Phi_h_Bin_Values[8][13][0]  =  24;	Phi_h_Bin_Values[8][13][1]  = 288;	Phi_h_Bin_Values[8][13][2]  = 5449;
z_pT_Bin_Borders[8][14][0]  = 0.49;	z_pT_Bin_Borders[8][14][1]  = 0.44;	z_pT_Bin_Borders[8][14][2]  = 0.46;	z_pT_Bin_Borders[8][14][3]  = 0.37;	Phi_h_Bin_Values[8][14][0]  =  24;	Phi_h_Bin_Values[8][14][1]  = 312;	Phi_h_Bin_Values[8][14][2]  = 5473;
z_pT_Bin_Borders[8][15][0]  = 0.49;	z_pT_Bin_Borders[8][15][1]  = 0.44;	z_pT_Bin_Borders[8][15][2]  = 0.6;	z_pT_Bin_Borders[8][15][3]  = 0.46;	Phi_h_Bin_Values[8][15][0]  =  24;	Phi_h_Bin_Values[8][15][1]  = 336;	Phi_h_Bin_Values[8][15][2]  = 5497;
z_pT_Bin_Borders[8][16][0]  = 0.44;	z_pT_Bin_Borders[8][16][1]  = 0.39;	z_pT_Bin_Borders[8][16][2]  = 0.2;	z_pT_Bin_Borders[8][16][3]  = 0.05;	Phi_h_Bin_Values[8][16][0]  =  24;	Phi_h_Bin_Values[8][16][1]  = 360;	Phi_h_Bin_Values[8][16][2]  = 5521;
z_pT_Bin_Borders[8][17][0]  = 0.44;	z_pT_Bin_Borders[8][17][1]  = 0.39;	z_pT_Bin_Borders[8][17][2]  = 0.29;	z_pT_Bin_Borders[8][17][3]  = 0.2;	Phi_h_Bin_Values[8][17][0]  =  24;	Phi_h_Bin_Values[8][17][1]  = 384;	Phi_h_Bin_Values[8][17][2]  = 5545;
z_pT_Bin_Borders[8][18][0]  = 0.44;	z_pT_Bin_Borders[8][18][1]  = 0.39;	z_pT_Bin_Borders[8][18][2]  = 0.37;	z_pT_Bin_Borders[8][18][3]  = 0.29;	Phi_h_Bin_Values[8][18][0]  =  24;	Phi_h_Bin_Values[8][18][1]  = 408;	Phi_h_Bin_Values[8][18][2]  = 5569;
z_pT_Bin_Borders[8][19][0]  = 0.44;	z_pT_Bin_Borders[8][19][1]  = 0.39;	z_pT_Bin_Borders[8][19][2]  = 0.46;	z_pT_Bin_Borders[8][19][3]  = 0.37;	Phi_h_Bin_Values[8][19][0]  =  24;	Phi_h_Bin_Values[8][19][1]  = 432;	Phi_h_Bin_Values[8][19][2]  = 5593;
z_pT_Bin_Borders[8][20][0]  = 0.44;	z_pT_Bin_Borders[8][20][1]  = 0.39;	z_pT_Bin_Borders[8][20][2]  = 0.6;	z_pT_Bin_Borders[8][20][3]  = 0.46;	Phi_h_Bin_Values[8][20][0]  =  24;	Phi_h_Bin_Values[8][20][1]  = 456;	Phi_h_Bin_Values[8][20][2]  = 5617;
z_pT_Bin_Borders[8][21][0]  = 0.39;	z_pT_Bin_Borders[8][21][1]  = 0.36;	z_pT_Bin_Borders[8][21][2]  = 0.2;	z_pT_Bin_Borders[8][21][3]  = 0.05;	Phi_h_Bin_Values[8][21][0]  =  24;	Phi_h_Bin_Values[8][21][1]  = 480;	Phi_h_Bin_Values[8][21][2]  = 5641;
z_pT_Bin_Borders[8][22][0]  = 0.39;	z_pT_Bin_Borders[8][22][1]  = 0.36;	z_pT_Bin_Borders[8][22][2]  = 0.29;	z_pT_Bin_Borders[8][22][3]  = 0.2;	Phi_h_Bin_Values[8][22][0]  =  24;	Phi_h_Bin_Values[8][22][1]  = 504;	Phi_h_Bin_Values[8][22][2]  = 5665;
z_pT_Bin_Borders[8][23][0]  = 0.39;	z_pT_Bin_Borders[8][23][1]  = 0.36;	z_pT_Bin_Borders[8][23][2]  = 0.37;	z_pT_Bin_Borders[8][23][3]  = 0.29;	Phi_h_Bin_Values[8][23][0]  =  24;	Phi_h_Bin_Values[8][23][1]  = 528;	Phi_h_Bin_Values[8][23][2]  = 5689;
z_pT_Bin_Borders[8][24][0]  = 0.39;	z_pT_Bin_Borders[8][24][1]  = 0.36;	z_pT_Bin_Borders[8][24][2]  = 0.46;	z_pT_Bin_Borders[8][24][3]  = 0.37;	Phi_h_Bin_Values[8][24][0]  =  24;	Phi_h_Bin_Values[8][24][1]  = 552;	Phi_h_Bin_Values[8][24][2]  = 5713;
z_pT_Bin_Borders[8][25][0]  = 0.39;	z_pT_Bin_Borders[8][25][1]  = 0.36;	z_pT_Bin_Borders[8][25][2]  = 0.6;	z_pT_Bin_Borders[8][25][3]  = 0.46;	Phi_h_Bin_Values[8][25][0]  =  24;	Phi_h_Bin_Values[8][25][1]  = 576;	Phi_h_Bin_Values[8][25][2]  = 5737;
z_pT_Bin_Borders[8][26][0]  = 0.36;	z_pT_Bin_Borders[8][26][1]  = 0.33;	z_pT_Bin_Borders[8][26][2]  = 0.2;	z_pT_Bin_Borders[8][26][3]  = 0.05;	Phi_h_Bin_Values[8][26][0]  =  24;	Phi_h_Bin_Values[8][26][1]  = 600;	Phi_h_Bin_Values[8][26][2]  = 5761;
z_pT_Bin_Borders[8][27][0]  = 0.36;	z_pT_Bin_Borders[8][27][1]  = 0.33;	z_pT_Bin_Borders[8][27][2]  = 0.29;	z_pT_Bin_Borders[8][27][3]  = 0.2;	Phi_h_Bin_Values[8][27][0]  =  24;	Phi_h_Bin_Values[8][27][1]  = 624;	Phi_h_Bin_Values[8][27][2]  = 5785;
z_pT_Bin_Borders[8][28][0]  = 0.36;	z_pT_Bin_Borders[8][28][1]  = 0.33;	z_pT_Bin_Borders[8][28][2]  = 0.37;	z_pT_Bin_Borders[8][28][3]  = 0.29;	Phi_h_Bin_Values[8][28][0]  =  24;	Phi_h_Bin_Values[8][28][1]  = 648;	Phi_h_Bin_Values[8][28][2]  = 5809;
z_pT_Bin_Borders[8][29][0]  = 0.36;	z_pT_Bin_Borders[8][29][1]  = 0.33;	z_pT_Bin_Borders[8][29][2]  = 0.46;	z_pT_Bin_Borders[8][29][3]  = 0.37;	Phi_h_Bin_Values[8][29][0]  =  24;	Phi_h_Bin_Values[8][29][1]  = 672;	Phi_h_Bin_Values[8][29][2]  = 5833;
z_pT_Bin_Borders[8][30][0]  = 0.36;	z_pT_Bin_Borders[8][30][1]  = 0.33;	z_pT_Bin_Borders[8][30][2]  = 0.6;	z_pT_Bin_Borders[8][30][3]  = 0.46;	Phi_h_Bin_Values[8][30][0]  =  24;	Phi_h_Bin_Values[8][30][1]  = 696;	Phi_h_Bin_Values[8][30][2]  = 5857;
z_pT_Bin_Borders[8][31][0]  = 0.33;	z_pT_Bin_Borders[8][31][1]  = 0.27;	z_pT_Bin_Borders[8][31][2]  = 0.2;	z_pT_Bin_Borders[8][31][3]  = 0.05;	Phi_h_Bin_Values[8][31][0]  =  24;	Phi_h_Bin_Values[8][31][1]  = 720;	Phi_h_Bin_Values[8][31][2]  = 5881;
z_pT_Bin_Borders[8][32][0]  = 0.33;	z_pT_Bin_Borders[8][32][1]  = 0.27;	z_pT_Bin_Borders[8][32][2]  = 0.29;	z_pT_Bin_Borders[8][32][3]  = 0.2;	Phi_h_Bin_Values[8][32][0]  =  24;	Phi_h_Bin_Values[8][32][1]  = 744;	Phi_h_Bin_Values[8][32][2]  = 5905;
z_pT_Bin_Borders[8][33][0]  = 0.33;	z_pT_Bin_Borders[8][33][1]  = 0.27;	z_pT_Bin_Borders[8][33][2]  = 0.37;	z_pT_Bin_Borders[8][33][3]  = 0.29;	Phi_h_Bin_Values[8][33][0]  =  24;	Phi_h_Bin_Values[8][33][1]  = 768;	Phi_h_Bin_Values[8][33][2]  = 5929;
z_pT_Bin_Borders[8][34][0]  = 0.33;	z_pT_Bin_Borders[8][34][1]  = 0.27;	z_pT_Bin_Borders[8][34][2]  = 0.46;	z_pT_Bin_Borders[8][34][3]  = 0.37;	Phi_h_Bin_Values[8][34][0]  =  24;	Phi_h_Bin_Values[8][34][1]  = 792;	Phi_h_Bin_Values[8][34][2]  = 5953;
z_pT_Bin_Borders[8][35][0]  = 0.33;	z_pT_Bin_Borders[8][35][1]  = 0.27;	z_pT_Bin_Borders[8][35][2]  = 0.6;	z_pT_Bin_Borders[8][35][3]  = 0.46;	Phi_h_Bin_Values[8][35][0]  =  24;	Phi_h_Bin_Values[8][35][1]  = 816;	Phi_h_Bin_Values[8][35][2]  = 5977;
z_pT_Bin_Borders[9][1][0]   = 0.7;	z_pT_Bin_Borders[9][1][1]   = 0.42;	z_pT_Bin_Borders[9][1][2]   = 0.22;	z_pT_Bin_Borders[9][1][3]   = 0.05;	Phi_h_Bin_Values[9][1][0]   =  24;	Phi_h_Bin_Values[9][1][1]   = 0;	Phi_h_Bin_Values[9][1][2]   = 6001;
z_pT_Bin_Borders[9][2][0]   = 0.7;	z_pT_Bin_Borders[9][2][1]   = 0.42;	z_pT_Bin_Borders[9][2][2]   = 0.3;	z_pT_Bin_Borders[9][2][3]   = 0.22;	Phi_h_Bin_Values[9][2][0]   =  24;	Phi_h_Bin_Values[9][2][1]   = 24;	Phi_h_Bin_Values[9][2][2]   = 6025;
z_pT_Bin_Borders[9][3][0]   = 0.7;	z_pT_Bin_Borders[9][3][1]   = 0.42;	z_pT_Bin_Borders[9][3][2]   = 0.38;	z_pT_Bin_Borders[9][3][3]   = 0.3;	Phi_h_Bin_Values[9][3][0]   =  24;	Phi_h_Bin_Values[9][3][1]   = 48;	Phi_h_Bin_Values[9][3][2]   = 6049;
z_pT_Bin_Borders[9][4][0]   = 0.7;	z_pT_Bin_Borders[9][4][1]   = 0.42;	z_pT_Bin_Borders[9][4][2]   = 0.46;	z_pT_Bin_Borders[9][4][3]   = 0.38;	Phi_h_Bin_Values[9][4][0]   =  24;	Phi_h_Bin_Values[9][4][1]   = 72;	Phi_h_Bin_Values[9][4][2]   = 6073;
z_pT_Bin_Borders[9][5][0]   = 0.7;	z_pT_Bin_Borders[9][5][1]   = 0.42;	z_pT_Bin_Borders[9][5][2]   = 0.58;	z_pT_Bin_Borders[9][5][3]   = 0.46;	Phi_h_Bin_Values[9][5][0]   =  24;	Phi_h_Bin_Values[9][5][1]   = 96;	Phi_h_Bin_Values[9][5][2]   = 6097;
z_pT_Bin_Borders[9][6][0]   = 0.7;	z_pT_Bin_Borders[9][6][1]   = 0.42;	z_pT_Bin_Borders[9][6][2]   = 0.74;	z_pT_Bin_Borders[9][6][3]   = 0.58;	Phi_h_Bin_Values[9][6][0]   =  24;	Phi_h_Bin_Values[9][6][1]   = 120;	Phi_h_Bin_Values[9][6][2]   = 6121;
z_pT_Bin_Borders[9][7][0]   = 0.7;	z_pT_Bin_Borders[9][7][1]   = 0.42;	z_pT_Bin_Borders[9][7][2]   = 0.95;	z_pT_Bin_Borders[9][7][3]   = 0.74;	Phi_h_Bin_Values[9][7][0]   =  24;	Phi_h_Bin_Values[9][7][1]   = 144;	Phi_h_Bin_Values[9][7][2]   = 6145;
z_pT_Bin_Borders[9][8][0]   = 0.42;	z_pT_Bin_Borders[9][8][1]   = 0.3;	z_pT_Bin_Borders[9][8][2]   = 0.22;	z_pT_Bin_Borders[9][8][3]   = 0.05;	Phi_h_Bin_Values[9][8][0]   =  24;	Phi_h_Bin_Values[9][8][1]   = 168;	Phi_h_Bin_Values[9][8][2]   = 6169;
z_pT_Bin_Borders[9][9][0]   = 0.42;	z_pT_Bin_Borders[9][9][1]   = 0.3;	z_pT_Bin_Borders[9][9][2]   = 0.3;	z_pT_Bin_Borders[9][9][3]   = 0.22;	Phi_h_Bin_Values[9][9][0]   =  24;	Phi_h_Bin_Values[9][9][1]   = 192;	Phi_h_Bin_Values[9][9][2]   = 6193;
z_pT_Bin_Borders[9][10][0]  = 0.42;	z_pT_Bin_Borders[9][10][1]  = 0.3;	z_pT_Bin_Borders[9][10][2]  = 0.38;	z_pT_Bin_Borders[9][10][3]  = 0.3;	Phi_h_Bin_Values[9][10][0]  =  24;	Phi_h_Bin_Values[9][10][1]  = 216;	Phi_h_Bin_Values[9][10][2]  = 6217;
z_pT_Bin_Borders[9][11][0]  = 0.42;	z_pT_Bin_Borders[9][11][1]  = 0.3;	z_pT_Bin_Borders[9][11][2]  = 0.46;	z_pT_Bin_Borders[9][11][3]  = 0.38;	Phi_h_Bin_Values[9][11][0]  =  24;	Phi_h_Bin_Values[9][11][1]  = 240;	Phi_h_Bin_Values[9][11][2]  = 6241;
z_pT_Bin_Borders[9][12][0]  = 0.42;	z_pT_Bin_Borders[9][12][1]  = 0.3;	z_pT_Bin_Borders[9][12][2]  = 0.58;	z_pT_Bin_Borders[9][12][3]  = 0.46;	Phi_h_Bin_Values[9][12][0]  =  24;	Phi_h_Bin_Values[9][12][1]  = 264;	Phi_h_Bin_Values[9][12][2]  = 6265;
z_pT_Bin_Borders[9][13][0]  = 0.42;	z_pT_Bin_Borders[9][13][1]  = 0.3;	z_pT_Bin_Borders[9][13][2]  = 0.74;	z_pT_Bin_Borders[9][13][3]  = 0.58;	Phi_h_Bin_Values[9][13][0]  =  24;	Phi_h_Bin_Values[9][13][1]  = 288;	Phi_h_Bin_Values[9][13][2]  = 6289;
z_pT_Bin_Borders[9][14][0]  = 0.42;	z_pT_Bin_Borders[9][14][1]  = 0.3;	z_pT_Bin_Borders[9][14][2]  = 0.95;	z_pT_Bin_Borders[9][14][3]  = 0.74;	Phi_h_Bin_Values[9][14][0]  =  24;	Phi_h_Bin_Values[9][14][1]  = 312;	Phi_h_Bin_Values[9][14][2]  = 6313;
z_pT_Bin_Borders[9][15][0]  = 0.3;	z_pT_Bin_Borders[9][15][1]  = 0.24;	z_pT_Bin_Borders[9][15][2]  = 0.22;	z_pT_Bin_Borders[9][15][3]  = 0.05;	Phi_h_Bin_Values[9][15][0]  =  24;	Phi_h_Bin_Values[9][15][1]  = 336;	Phi_h_Bin_Values[9][15][2]  = 6337;
z_pT_Bin_Borders[9][16][0]  = 0.3;	z_pT_Bin_Borders[9][16][1]  = 0.24;	z_pT_Bin_Borders[9][16][2]  = 0.3;	z_pT_Bin_Borders[9][16][3]  = 0.22;	Phi_h_Bin_Values[9][16][0]  =  24;	Phi_h_Bin_Values[9][16][1]  = 360;	Phi_h_Bin_Values[9][16][2]  = 6361;
z_pT_Bin_Borders[9][17][0]  = 0.3;	z_pT_Bin_Borders[9][17][1]  = 0.24;	z_pT_Bin_Borders[9][17][2]  = 0.38;	z_pT_Bin_Borders[9][17][3]  = 0.3;	Phi_h_Bin_Values[9][17][0]  =  24;	Phi_h_Bin_Values[9][17][1]  = 384;	Phi_h_Bin_Values[9][17][2]  = 6385;
z_pT_Bin_Borders[9][18][0]  = 0.3;	z_pT_Bin_Borders[9][18][1]  = 0.24;	z_pT_Bin_Borders[9][18][2]  = 0.46;	z_pT_Bin_Borders[9][18][3]  = 0.38;	Phi_h_Bin_Values[9][18][0]  =  24;	Phi_h_Bin_Values[9][18][1]  = 408;	Phi_h_Bin_Values[9][18][2]  = 6409;
z_pT_Bin_Borders[9][19][0]  = 0.3;	z_pT_Bin_Borders[9][19][1]  = 0.24;	z_pT_Bin_Borders[9][19][2]  = 0.58;	z_pT_Bin_Borders[9][19][3]  = 0.46;	Phi_h_Bin_Values[9][19][0]  =  24;	Phi_h_Bin_Values[9][19][1]  = 432;	Phi_h_Bin_Values[9][19][2]  = 6433;
z_pT_Bin_Borders[9][20][0]  = 0.3;	z_pT_Bin_Borders[9][20][1]  = 0.24;	z_pT_Bin_Borders[9][20][2]  = 0.74;	z_pT_Bin_Borders[9][20][3]  = 0.58;	Phi_h_Bin_Values[9][20][0]  =  24;	Phi_h_Bin_Values[9][20][1]  = 456;	Phi_h_Bin_Values[9][20][2]  = 6457;
z_pT_Bin_Borders[9][21][0]  = 0.3;	z_pT_Bin_Borders[9][21][1]  = 0.24;	z_pT_Bin_Borders[9][21][2]  = 0.95;	z_pT_Bin_Borders[9][21][3]  = 0.74;	Phi_h_Bin_Values[9][21][0]  =  1;	Phi_h_Bin_Values[9][21][1]  = 480;	Phi_h_Bin_Values[9][21][2]  = 6481;
z_pT_Bin_Borders[9][22][0]  = 0.24;	z_pT_Bin_Borders[9][22][1]  = 0.2;	z_pT_Bin_Borders[9][22][2]  = 0.22;	z_pT_Bin_Borders[9][22][3]  = 0.05;	Phi_h_Bin_Values[9][22][0]  =  24;	Phi_h_Bin_Values[9][22][1]  = 481;	Phi_h_Bin_Values[9][22][2]  = 6482;
z_pT_Bin_Borders[9][23][0]  = 0.24;	z_pT_Bin_Borders[9][23][1]  = 0.2;	z_pT_Bin_Borders[9][23][2]  = 0.3;	z_pT_Bin_Borders[9][23][3]  = 0.22;	Phi_h_Bin_Values[9][23][0]  =  24;	Phi_h_Bin_Values[9][23][1]  = 505;	Phi_h_Bin_Values[9][23][2]  = 6506;
z_pT_Bin_Borders[9][24][0]  = 0.24;	z_pT_Bin_Borders[9][24][1]  = 0.2;	z_pT_Bin_Borders[9][24][2]  = 0.38;	z_pT_Bin_Borders[9][24][3]  = 0.3;	Phi_h_Bin_Values[9][24][0]  =  24;	Phi_h_Bin_Values[9][24][1]  = 529;	Phi_h_Bin_Values[9][24][2]  = 6530;
z_pT_Bin_Borders[9][25][0]  = 0.24;	z_pT_Bin_Borders[9][25][1]  = 0.2;	z_pT_Bin_Borders[9][25][2]  = 0.46;	z_pT_Bin_Borders[9][25][3]  = 0.38;	Phi_h_Bin_Values[9][25][0]  =  24;	Phi_h_Bin_Values[9][25][1]  = 553;	Phi_h_Bin_Values[9][25][2]  = 6554;
z_pT_Bin_Borders[9][26][0]  = 0.24;	z_pT_Bin_Borders[9][26][1]  = 0.2;	z_pT_Bin_Borders[9][26][2]  = 0.58;	z_pT_Bin_Borders[9][26][3]  = 0.46;	Phi_h_Bin_Values[9][26][0]  =  24;	Phi_h_Bin_Values[9][26][1]  = 577;	Phi_h_Bin_Values[9][26][2]  = 6578;
z_pT_Bin_Borders[9][27][0]  = 0.24;	z_pT_Bin_Borders[9][27][1]  = 0.2;	z_pT_Bin_Borders[9][27][2]  = 0.74;	z_pT_Bin_Borders[9][27][3]  = 0.58;	Phi_h_Bin_Values[9][27][0]  =  1;	Phi_h_Bin_Values[9][27][1]  = 601;	Phi_h_Bin_Values[9][27][2]  = 6602;
z_pT_Bin_Borders[9][28][0]  = 0.24;	z_pT_Bin_Borders[9][28][1]  = 0.2;	z_pT_Bin_Borders[9][28][2]  = 0.95;	z_pT_Bin_Borders[9][28][3]  = 0.74;	Phi_h_Bin_Values[9][28][0]  =  1;	Phi_h_Bin_Values[9][28][1]  = 602;	Phi_h_Bin_Values[9][28][2]  = 6603;
z_pT_Bin_Borders[9][29][0]  = 0.2;	z_pT_Bin_Borders[9][29][1]  = 0.16;	z_pT_Bin_Borders[9][29][2]  = 0.22;	z_pT_Bin_Borders[9][29][3]  = 0.05;	Phi_h_Bin_Values[9][29][0]  =  24;	Phi_h_Bin_Values[9][29][1]  = 603;	Phi_h_Bin_Values[9][29][2]  = 6604;
z_pT_Bin_Borders[9][30][0]  = 0.2;	z_pT_Bin_Borders[9][30][1]  = 0.16;	z_pT_Bin_Borders[9][30][2]  = 0.3;	z_pT_Bin_Borders[9][30][3]  = 0.22;	Phi_h_Bin_Values[9][30][0]  =  24;	Phi_h_Bin_Values[9][30][1]  = 627;	Phi_h_Bin_Values[9][30][2]  = 6628;
z_pT_Bin_Borders[9][31][0]  = 0.2;	z_pT_Bin_Borders[9][31][1]  = 0.16;	z_pT_Bin_Borders[9][31][2]  = 0.38;	z_pT_Bin_Borders[9][31][3]  = 0.3;	Phi_h_Bin_Values[9][31][0]  =  24;	Phi_h_Bin_Values[9][31][1]  = 651;	Phi_h_Bin_Values[9][31][2]  = 6652;
z_pT_Bin_Borders[9][32][0]  = 0.2;	z_pT_Bin_Borders[9][32][1]  = 0.16;	z_pT_Bin_Borders[9][32][2]  = 0.46;	z_pT_Bin_Borders[9][32][3]  = 0.38;	Phi_h_Bin_Values[9][32][0]  =  24;	Phi_h_Bin_Values[9][32][1]  = 675;	Phi_h_Bin_Values[9][32][2]  = 6676;
z_pT_Bin_Borders[9][33][0]  = 0.2;	z_pT_Bin_Borders[9][33][1]  = 0.16;	z_pT_Bin_Borders[9][33][2]  = 0.58;	z_pT_Bin_Borders[9][33][3]  = 0.46;	Phi_h_Bin_Values[9][33][0]  =  1;	Phi_h_Bin_Values[9][33][1]  = 699;	Phi_h_Bin_Values[9][33][2]  = 6700;
z_pT_Bin_Borders[9][34][0]  = 0.2;	z_pT_Bin_Borders[9][34][1]  = 0.16;	z_pT_Bin_Borders[9][34][2]  = 0.74;	z_pT_Bin_Borders[9][34][3]  = 0.58;	Phi_h_Bin_Values[9][34][0]  =  1;	Phi_h_Bin_Values[9][34][1]  = 700;	Phi_h_Bin_Values[9][34][2]  = 6701;
z_pT_Bin_Borders[9][35][0]  = 0.2;	z_pT_Bin_Borders[9][35][1]  = 0.16;	z_pT_Bin_Borders[9][35][2]  = 0.95;	z_pT_Bin_Borders[9][35][3]  = 0.74;	Phi_h_Bin_Values[9][35][0]  =  1;	Phi_h_Bin_Values[9][35][1]  = 701;	Phi_h_Bin_Values[9][35][2]  = 6702;
z_pT_Bin_Borders[10][1][0]  = 0.72;	z_pT_Bin_Borders[10][1][1]  = 0.5;	z_pT_Bin_Borders[10][1][2]  = 0.21;	z_pT_Bin_Borders[10][1][3]  = 0.05;	Phi_h_Bin_Values[10][1][0]  =  24;	Phi_h_Bin_Values[10][1][1]  = 0;	Phi_h_Bin_Values[10][1][2]  = 6703;
z_pT_Bin_Borders[10][2][0]  = 0.72;	z_pT_Bin_Borders[10][2][1]  = 0.5;	z_pT_Bin_Borders[10][2][2]  = 0.31;	z_pT_Bin_Borders[10][2][3]  = 0.21;	Phi_h_Bin_Values[10][2][0]  =  24;	Phi_h_Bin_Values[10][2][1]  = 24;	Phi_h_Bin_Values[10][2][2]  = 6727;
z_pT_Bin_Borders[10][3][0]  = 0.72;	z_pT_Bin_Borders[10][3][1]  = 0.5;	z_pT_Bin_Borders[10][3][2]  = 0.4;	z_pT_Bin_Borders[10][3][3]  = 0.31;	Phi_h_Bin_Values[10][3][0]  =  24;	Phi_h_Bin_Values[10][3][1]  = 48;	Phi_h_Bin_Values[10][3][2]  = 6751;
z_pT_Bin_Borders[10][4][0]  = 0.72;	z_pT_Bin_Borders[10][4][1]  = 0.5;	z_pT_Bin_Borders[10][4][2]  = 0.5;	z_pT_Bin_Borders[10][4][3]  = 0.4;	Phi_h_Bin_Values[10][4][0]  =  24;	Phi_h_Bin_Values[10][4][1]  = 72;	Phi_h_Bin_Values[10][4][2]  = 6775;
z_pT_Bin_Borders[10][5][0]  = 0.72;	z_pT_Bin_Borders[10][5][1]  = 0.5;	z_pT_Bin_Borders[10][5][2]  = 0.64;	z_pT_Bin_Borders[10][5][3]  = 0.5;	Phi_h_Bin_Values[10][5][0]  =  24;	Phi_h_Bin_Values[10][5][1]  = 96;	Phi_h_Bin_Values[10][5][2]  = 6799;
z_pT_Bin_Borders[10][6][0]  = 0.72;	z_pT_Bin_Borders[10][6][1]  = 0.5;	z_pT_Bin_Borders[10][6][2]  = 0.9;	z_pT_Bin_Borders[10][6][3]  = 0.64;	Phi_h_Bin_Values[10][6][0]  =  24;	Phi_h_Bin_Values[10][6][1]  = 120;	Phi_h_Bin_Values[10][6][2]  = 6823;
z_pT_Bin_Borders[10][7][0]  = 0.5;	z_pT_Bin_Borders[10][7][1]  = 0.4;	z_pT_Bin_Borders[10][7][2]  = 0.21;	z_pT_Bin_Borders[10][7][3]  = 0.05;	Phi_h_Bin_Values[10][7][0]  =  24;	Phi_h_Bin_Values[10][7][1]  = 144;	Phi_h_Bin_Values[10][7][2]  = 6847;
z_pT_Bin_Borders[10][8][0]  = 0.5;	z_pT_Bin_Borders[10][8][1]  = 0.4;	z_pT_Bin_Borders[10][8][2]  = 0.31;	z_pT_Bin_Borders[10][8][3]  = 0.21;	Phi_h_Bin_Values[10][8][0]  =  24;	Phi_h_Bin_Values[10][8][1]  = 168;	Phi_h_Bin_Values[10][8][2]  = 6871;
z_pT_Bin_Borders[10][9][0]  = 0.5;	z_pT_Bin_Borders[10][9][1]  = 0.4;	z_pT_Bin_Borders[10][9][2]  = 0.4;	z_pT_Bin_Borders[10][9][3]  = 0.31;	Phi_h_Bin_Values[10][9][0]  =  24;	Phi_h_Bin_Values[10][9][1]  = 192;	Phi_h_Bin_Values[10][9][2]  = 6895;
z_pT_Bin_Borders[10][10][0] = 0.5;	z_pT_Bin_Borders[10][10][1] = 0.4;	z_pT_Bin_Borders[10][10][2] = 0.5;	z_pT_Bin_Borders[10][10][3] = 0.4;	Phi_h_Bin_Values[10][10][0] =  24;	Phi_h_Bin_Values[10][10][1] = 216;	Phi_h_Bin_Values[10][10][2] = 6919;
z_pT_Bin_Borders[10][11][0] = 0.5;	z_pT_Bin_Borders[10][11][1] = 0.4;	z_pT_Bin_Borders[10][11][2] = 0.64;	z_pT_Bin_Borders[10][11][3] = 0.5;	Phi_h_Bin_Values[10][11][0] =  24;	Phi_h_Bin_Values[10][11][1] = 240;	Phi_h_Bin_Values[10][11][2] = 6943;
z_pT_Bin_Borders[10][12][0] = 0.5;	z_pT_Bin_Borders[10][12][1] = 0.4;	z_pT_Bin_Borders[10][12][2] = 0.9;	z_pT_Bin_Borders[10][12][3] = 0.64;	Phi_h_Bin_Values[10][12][0] =  24;	Phi_h_Bin_Values[10][12][1] = 264;	Phi_h_Bin_Values[10][12][2] = 6967;
z_pT_Bin_Borders[10][13][0] = 0.4;	z_pT_Bin_Borders[10][13][1] = 0.32;	z_pT_Bin_Borders[10][13][2] = 0.21;	z_pT_Bin_Borders[10][13][3] = 0.05;	Phi_h_Bin_Values[10][13][0] =  24;	Phi_h_Bin_Values[10][13][1] = 288;	Phi_h_Bin_Values[10][13][2] = 6991;
z_pT_Bin_Borders[10][14][0] = 0.4;	z_pT_Bin_Borders[10][14][1] = 0.32;	z_pT_Bin_Borders[10][14][2] = 0.31;	z_pT_Bin_Borders[10][14][3] = 0.21;	Phi_h_Bin_Values[10][14][0] =  24;	Phi_h_Bin_Values[10][14][1] = 312;	Phi_h_Bin_Values[10][14][2] = 7015;
z_pT_Bin_Borders[10][15][0] = 0.4;	z_pT_Bin_Borders[10][15][1] = 0.32;	z_pT_Bin_Borders[10][15][2] = 0.4;	z_pT_Bin_Borders[10][15][3] = 0.31;	Phi_h_Bin_Values[10][15][0] =  24;	Phi_h_Bin_Values[10][15][1] = 336;	Phi_h_Bin_Values[10][15][2] = 7039;
z_pT_Bin_Borders[10][16][0] = 0.4;	z_pT_Bin_Borders[10][16][1] = 0.32;	z_pT_Bin_Borders[10][16][2] = 0.5;	z_pT_Bin_Borders[10][16][3] = 0.4;	Phi_h_Bin_Values[10][16][0] =  24;	Phi_h_Bin_Values[10][16][1] = 360;	Phi_h_Bin_Values[10][16][2] = 7063;
z_pT_Bin_Borders[10][17][0] = 0.4;	z_pT_Bin_Borders[10][17][1] = 0.32;	z_pT_Bin_Borders[10][17][2] = 0.64;	z_pT_Bin_Borders[10][17][3] = 0.5;	Phi_h_Bin_Values[10][17][0] =  24;	Phi_h_Bin_Values[10][17][1] = 384;	Phi_h_Bin_Values[10][17][2] = 7087;
z_pT_Bin_Borders[10][18][0] = 0.4;	z_pT_Bin_Borders[10][18][1] = 0.32;	z_pT_Bin_Borders[10][18][2] = 0.9;	z_pT_Bin_Borders[10][18][3] = 0.64;	Phi_h_Bin_Values[10][18][0] =  24;	Phi_h_Bin_Values[10][18][1] = 408;	Phi_h_Bin_Values[10][18][2] = 7111;
z_pT_Bin_Borders[10][19][0] = 0.32;	z_pT_Bin_Borders[10][19][1] = 0.26;	z_pT_Bin_Borders[10][19][2] = 0.21;	z_pT_Bin_Borders[10][19][3] = 0.05;	Phi_h_Bin_Values[10][19][0] =  24;	Phi_h_Bin_Values[10][19][1] = 432;	Phi_h_Bin_Values[10][19][2] = 7135;
z_pT_Bin_Borders[10][20][0] = 0.32;	z_pT_Bin_Borders[10][20][1] = 0.26;	z_pT_Bin_Borders[10][20][2] = 0.31;	z_pT_Bin_Borders[10][20][3] = 0.21;	Phi_h_Bin_Values[10][20][0] =  24;	Phi_h_Bin_Values[10][20][1] = 456;	Phi_h_Bin_Values[10][20][2] = 7159;
z_pT_Bin_Borders[10][21][0] = 0.32;	z_pT_Bin_Borders[10][21][1] = 0.26;	z_pT_Bin_Borders[10][21][2] = 0.4;	z_pT_Bin_Borders[10][21][3] = 0.31;	Phi_h_Bin_Values[10][21][0] =  24;	Phi_h_Bin_Values[10][21][1] = 480;	Phi_h_Bin_Values[10][21][2] = 7183;
z_pT_Bin_Borders[10][22][0] = 0.32;	z_pT_Bin_Borders[10][22][1] = 0.26;	z_pT_Bin_Borders[10][22][2] = 0.5;	z_pT_Bin_Borders[10][22][3] = 0.4;	Phi_h_Bin_Values[10][22][0] =  24;	Phi_h_Bin_Values[10][22][1] = 504;	Phi_h_Bin_Values[10][22][2] = 7207;
z_pT_Bin_Borders[10][23][0] = 0.32;	z_pT_Bin_Borders[10][23][1] = 0.26;	z_pT_Bin_Borders[10][23][2] = 0.64;	z_pT_Bin_Borders[10][23][3] = 0.5;	Phi_h_Bin_Values[10][23][0] =  24;	Phi_h_Bin_Values[10][23][1] = 528;	Phi_h_Bin_Values[10][23][2] = 7231;
z_pT_Bin_Borders[10][24][0] = 0.32;	z_pT_Bin_Borders[10][24][1] = 0.26;	z_pT_Bin_Borders[10][24][2] = 0.9;	z_pT_Bin_Borders[10][24][3] = 0.64;	Phi_h_Bin_Values[10][24][0] =  1;	Phi_h_Bin_Values[10][24][1] = 552;	Phi_h_Bin_Values[10][24][2] = 7255;
z_pT_Bin_Borders[10][25][0] = 0.26;	z_pT_Bin_Borders[10][25][1] = 0.23;	z_pT_Bin_Borders[10][25][2] = 0.21;	z_pT_Bin_Borders[10][25][3] = 0.05;	Phi_h_Bin_Values[10][25][0] =  24;	Phi_h_Bin_Values[10][25][1] = 553;	Phi_h_Bin_Values[10][25][2] = 7256;
z_pT_Bin_Borders[10][26][0] = 0.26;	z_pT_Bin_Borders[10][26][1] = 0.23;	z_pT_Bin_Borders[10][26][2] = 0.31;	z_pT_Bin_Borders[10][26][3] = 0.21;	Phi_h_Bin_Values[10][26][0] =  24;	Phi_h_Bin_Values[10][26][1] = 577;	Phi_h_Bin_Values[10][26][2] = 7280;
z_pT_Bin_Borders[10][27][0] = 0.26;	z_pT_Bin_Borders[10][27][1] = 0.23;	z_pT_Bin_Borders[10][27][2] = 0.4;	z_pT_Bin_Borders[10][27][3] = 0.31;	Phi_h_Bin_Values[10][27][0] =  24;	Phi_h_Bin_Values[10][27][1] = 601;	Phi_h_Bin_Values[10][27][2] = 7304;
z_pT_Bin_Borders[10][28][0] = 0.26;	z_pT_Bin_Borders[10][28][1] = 0.23;	z_pT_Bin_Borders[10][28][2] = 0.5;	z_pT_Bin_Borders[10][28][3] = 0.4;	Phi_h_Bin_Values[10][28][0] =  24;	Phi_h_Bin_Values[10][28][1] = 625;	Phi_h_Bin_Values[10][28][2] = 7328;
z_pT_Bin_Borders[10][29][0] = 0.26;	z_pT_Bin_Borders[10][29][1] = 0.23;	z_pT_Bin_Borders[10][29][2] = 0.64;	z_pT_Bin_Borders[10][29][3] = 0.5;	Phi_h_Bin_Values[10][29][0] =  24;	Phi_h_Bin_Values[10][29][1] = 649;	Phi_h_Bin_Values[10][29][2] = 7352;
z_pT_Bin_Borders[10][30][0] = 0.26;	z_pT_Bin_Borders[10][30][1] = 0.23;	z_pT_Bin_Borders[10][30][2] = 0.9;	z_pT_Bin_Borders[10][30][3] = 0.64;	Phi_h_Bin_Values[10][30][0] =  1;	Phi_h_Bin_Values[10][30][1] = 673;	Phi_h_Bin_Values[10][30][2] = 7376;
z_pT_Bin_Borders[10][31][0] = 0.23;	z_pT_Bin_Borders[10][31][1] = 0.19;	z_pT_Bin_Borders[10][31][2] = 0.21;	z_pT_Bin_Borders[10][31][3] = 0.05;	Phi_h_Bin_Values[10][31][0] =  24;	Phi_h_Bin_Values[10][31][1] = 674;	Phi_h_Bin_Values[10][31][2] = 7377;
z_pT_Bin_Borders[10][32][0] = 0.23;	z_pT_Bin_Borders[10][32][1] = 0.19;	z_pT_Bin_Borders[10][32][2] = 0.31;	z_pT_Bin_Borders[10][32][3] = 0.21;	Phi_h_Bin_Values[10][32][0] =  24;	Phi_h_Bin_Values[10][32][1] = 698;	Phi_h_Bin_Values[10][32][2] = 7401;
z_pT_Bin_Borders[10][33][0] = 0.23;	z_pT_Bin_Borders[10][33][1] = 0.19;	z_pT_Bin_Borders[10][33][2] = 0.4;	z_pT_Bin_Borders[10][33][3] = 0.31;	Phi_h_Bin_Values[10][33][0] =  24;	Phi_h_Bin_Values[10][33][1] = 722;	Phi_h_Bin_Values[10][33][2] = 7425;
z_pT_Bin_Borders[10][34][0] = 0.23;	z_pT_Bin_Borders[10][34][1] = 0.19;	z_pT_Bin_Borders[10][34][2] = 0.5;	z_pT_Bin_Borders[10][34][3] = 0.4;	Phi_h_Bin_Values[10][34][0] =  24;	Phi_h_Bin_Values[10][34][1] = 746;	Phi_h_Bin_Values[10][34][2] = 7449;
z_pT_Bin_Borders[10][35][0] = 0.23;	z_pT_Bin_Borders[10][35][1] = 0.19;	z_pT_Bin_Borders[10][35][2] = 0.64;	z_pT_Bin_Borders[10][35][3] = 0.5;	Phi_h_Bin_Values[10][35][0] =  1;	Phi_h_Bin_Values[10][35][1] = 770;	Phi_h_Bin_Values[10][35][2] = 7473;
z_pT_Bin_Borders[10][36][0] = 0.23;	z_pT_Bin_Borders[10][36][1] = 0.19;	z_pT_Bin_Borders[10][36][2] = 0.9;	z_pT_Bin_Borders[10][36][3] = 0.64;	Phi_h_Bin_Values[10][36][0] =  1;	Phi_h_Bin_Values[10][36][1] = 771;	Phi_h_Bin_Values[10][36][2] = 7474;
z_pT_Bin_Borders[11][1][0]  = 0.73;	z_pT_Bin_Borders[11][1][1]  = 0.52;	z_pT_Bin_Borders[11][1][2]  = 0.2;	z_pT_Bin_Borders[11][1][3]  = 0.05;	Phi_h_Bin_Values[11][1][0]  =  24;	Phi_h_Bin_Values[11][1][1]  = 0;	Phi_h_Bin_Values[11][1][2]  = 7475;
z_pT_Bin_Borders[11][2][0]  = 0.73;	z_pT_Bin_Borders[11][2][1]  = 0.52;	z_pT_Bin_Borders[11][2][2]  = 0.3;	z_pT_Bin_Borders[11][2][3]  = 0.2;	Phi_h_Bin_Values[11][2][0]  =  24;	Phi_h_Bin_Values[11][2][1]  = 24;	Phi_h_Bin_Values[11][2][2]  = 7499;
z_pT_Bin_Borders[11][3][0]  = 0.73;	z_pT_Bin_Borders[11][3][1]  = 0.52;	z_pT_Bin_Borders[11][3][2]  = 0.4;	z_pT_Bin_Borders[11][3][3]  = 0.3;	Phi_h_Bin_Values[11][3][0]  =  24;	Phi_h_Bin_Values[11][3][1]  = 48;	Phi_h_Bin_Values[11][3][2]  = 7523;
z_pT_Bin_Borders[11][4][0]  = 0.73;	z_pT_Bin_Borders[11][4][1]  = 0.52;	z_pT_Bin_Borders[11][4][2]  = 0.53;	z_pT_Bin_Borders[11][4][3]  = 0.4;	Phi_h_Bin_Values[11][4][0]  =  24;	Phi_h_Bin_Values[11][4][1]  = 72;	Phi_h_Bin_Values[11][4][2]  = 7547;
z_pT_Bin_Borders[11][5][0]  = 0.73;	z_pT_Bin_Borders[11][5][1]  = 0.52;	z_pT_Bin_Borders[11][5][2]  = 0.69;	z_pT_Bin_Borders[11][5][3]  = 0.53;	Phi_h_Bin_Values[11][5][0]  =  24;	Phi_h_Bin_Values[11][5][1]  = 96;	Phi_h_Bin_Values[11][5][2]  = 7571;
z_pT_Bin_Borders[11][6][0]  = 0.52;	z_pT_Bin_Borders[11][6][1]  = 0.39;	z_pT_Bin_Borders[11][6][2]  = 0.2;	z_pT_Bin_Borders[11][6][3]  = 0.05;	Phi_h_Bin_Values[11][6][0]  =  24;	Phi_h_Bin_Values[11][6][1]  = 120;	Phi_h_Bin_Values[11][6][2]  = 7595;
z_pT_Bin_Borders[11][7][0]  = 0.52;	z_pT_Bin_Borders[11][7][1]  = 0.39;	z_pT_Bin_Borders[11][7][2]  = 0.3;	z_pT_Bin_Borders[11][7][3]  = 0.2;	Phi_h_Bin_Values[11][7][0]  =  24;	Phi_h_Bin_Values[11][7][1]  = 144;	Phi_h_Bin_Values[11][7][2]  = 7619;
z_pT_Bin_Borders[11][8][0]  = 0.52;	z_pT_Bin_Borders[11][8][1]  = 0.39;	z_pT_Bin_Borders[11][8][2]  = 0.4;	z_pT_Bin_Borders[11][8][3]  = 0.3;	Phi_h_Bin_Values[11][8][0]  =  24;	Phi_h_Bin_Values[11][8][1]  = 168;	Phi_h_Bin_Values[11][8][2]  = 7643;
z_pT_Bin_Borders[11][9][0]  = 0.52;	z_pT_Bin_Borders[11][9][1]  = 0.39;	z_pT_Bin_Borders[11][9][2]  = 0.53;	z_pT_Bin_Borders[11][9][3]  = 0.4;	Phi_h_Bin_Values[11][9][0]  =  24;	Phi_h_Bin_Values[11][9][1]  = 192;	Phi_h_Bin_Values[11][9][2]  = 7667;
z_pT_Bin_Borders[11][10][0] = 0.52;	z_pT_Bin_Borders[11][10][1] = 0.39;	z_pT_Bin_Borders[11][10][2] = 0.69;	z_pT_Bin_Borders[11][10][3] = 0.53;	Phi_h_Bin_Values[11][10][0] =  24;	Phi_h_Bin_Values[11][10][1] = 216;	Phi_h_Bin_Values[11][10][2] = 7691;
z_pT_Bin_Borders[11][11][0] = 0.39;	z_pT_Bin_Borders[11][11][1] = 0.32;	z_pT_Bin_Borders[11][11][2] = 0.2;	z_pT_Bin_Borders[11][11][3] = 0.05;	Phi_h_Bin_Values[11][11][0] =  24;	Phi_h_Bin_Values[11][11][1] = 240;	Phi_h_Bin_Values[11][11][2] = 7715;
z_pT_Bin_Borders[11][12][0] = 0.39;	z_pT_Bin_Borders[11][12][1] = 0.32;	z_pT_Bin_Borders[11][12][2] = 0.3;	z_pT_Bin_Borders[11][12][3] = 0.2;	Phi_h_Bin_Values[11][12][0] =  24;	Phi_h_Bin_Values[11][12][1] = 264;	Phi_h_Bin_Values[11][12][2] = 7739;
z_pT_Bin_Borders[11][13][0] = 0.39;	z_pT_Bin_Borders[11][13][1] = 0.32;	z_pT_Bin_Borders[11][13][2] = 0.4;	z_pT_Bin_Borders[11][13][3] = 0.3;	Phi_h_Bin_Values[11][13][0] =  24;	Phi_h_Bin_Values[11][13][1] = 288;	Phi_h_Bin_Values[11][13][2] = 7763;
z_pT_Bin_Borders[11][14][0] = 0.39;	z_pT_Bin_Borders[11][14][1] = 0.32;	z_pT_Bin_Borders[11][14][2] = 0.53;	z_pT_Bin_Borders[11][14][3] = 0.4;	Phi_h_Bin_Values[11][14][0] =  24;	Phi_h_Bin_Values[11][14][1] = 312;	Phi_h_Bin_Values[11][14][2] = 7787;
z_pT_Bin_Borders[11][15][0] = 0.39;	z_pT_Bin_Borders[11][15][1] = 0.32;	z_pT_Bin_Borders[11][15][2] = 0.69;	z_pT_Bin_Borders[11][15][3] = 0.53;	Phi_h_Bin_Values[11][15][0] =  24;	Phi_h_Bin_Values[11][15][1] = 336;	Phi_h_Bin_Values[11][15][2] = 7811;
z_pT_Bin_Borders[11][16][0] = 0.32;	z_pT_Bin_Borders[11][16][1] = 0.27;	z_pT_Bin_Borders[11][16][2] = 0.2;	z_pT_Bin_Borders[11][16][3] = 0.05;	Phi_h_Bin_Values[11][16][0] =  24;	Phi_h_Bin_Values[11][16][1] = 360;	Phi_h_Bin_Values[11][16][2] = 7835;
z_pT_Bin_Borders[11][17][0] = 0.32;	z_pT_Bin_Borders[11][17][1] = 0.27;	z_pT_Bin_Borders[11][17][2] = 0.3;	z_pT_Bin_Borders[11][17][3] = 0.2;	Phi_h_Bin_Values[11][17][0] =  24;	Phi_h_Bin_Values[11][17][1] = 384;	Phi_h_Bin_Values[11][17][2] = 7859;
z_pT_Bin_Borders[11][18][0] = 0.32;	z_pT_Bin_Borders[11][18][1] = 0.27;	z_pT_Bin_Borders[11][18][2] = 0.4;	z_pT_Bin_Borders[11][18][3] = 0.3;	Phi_h_Bin_Values[11][18][0] =  24;	Phi_h_Bin_Values[11][18][1] = 408;	Phi_h_Bin_Values[11][18][2] = 7883;
z_pT_Bin_Borders[11][19][0] = 0.32;	z_pT_Bin_Borders[11][19][1] = 0.27;	z_pT_Bin_Borders[11][19][2] = 0.53;	z_pT_Bin_Borders[11][19][3] = 0.4;	Phi_h_Bin_Values[11][19][0] =  24;	Phi_h_Bin_Values[11][19][1] = 432;	Phi_h_Bin_Values[11][19][2] = 7907;
z_pT_Bin_Borders[11][20][0] = 0.32;	z_pT_Bin_Borders[11][20][1] = 0.27;	z_pT_Bin_Borders[11][20][2] = 0.69;	z_pT_Bin_Borders[11][20][3] = 0.53;	Phi_h_Bin_Values[11][20][0] =  24;	Phi_h_Bin_Values[11][20][1] = 456;	Phi_h_Bin_Values[11][20][2] = 7931;
z_pT_Bin_Borders[11][21][0] = 0.27;	z_pT_Bin_Borders[11][21][1] = 0.22;	z_pT_Bin_Borders[11][21][2] = 0.2;	z_pT_Bin_Borders[11][21][3] = 0.05;	Phi_h_Bin_Values[11][21][0] =  24;	Phi_h_Bin_Values[11][21][1] = 480;	Phi_h_Bin_Values[11][21][2] = 7955;
z_pT_Bin_Borders[11][22][0] = 0.27;	z_pT_Bin_Borders[11][22][1] = 0.22;	z_pT_Bin_Borders[11][22][2] = 0.3;	z_pT_Bin_Borders[11][22][3] = 0.2;	Phi_h_Bin_Values[11][22][0] =  24;	Phi_h_Bin_Values[11][22][1] = 504;	Phi_h_Bin_Values[11][22][2] = 7979;
z_pT_Bin_Borders[11][23][0] = 0.27;	z_pT_Bin_Borders[11][23][1] = 0.22;	z_pT_Bin_Borders[11][23][2] = 0.4;	z_pT_Bin_Borders[11][23][3] = 0.3;	Phi_h_Bin_Values[11][23][0] =  24;	Phi_h_Bin_Values[11][23][1] = 528;	Phi_h_Bin_Values[11][23][2] = 8003;
z_pT_Bin_Borders[11][24][0] = 0.27;	z_pT_Bin_Borders[11][24][1] = 0.22;	z_pT_Bin_Borders[11][24][2] = 0.53;	z_pT_Bin_Borders[11][24][3] = 0.4;	Phi_h_Bin_Values[11][24][0] =  24;	Phi_h_Bin_Values[11][24][1] = 552;	Phi_h_Bin_Values[11][24][2] = 8027;
z_pT_Bin_Borders[11][25][0] = 0.27;	z_pT_Bin_Borders[11][25][1] = 0.22;	z_pT_Bin_Borders[11][25][2] = 0.69;	z_pT_Bin_Borders[11][25][3] = 0.53;	Phi_h_Bin_Values[11][25][0] =  1;	Phi_h_Bin_Values[11][25][1] = 576;	Phi_h_Bin_Values[11][25][2] = 8051;
z_pT_Bin_Borders[12][1][0]  = 0.7;	z_pT_Bin_Borders[12][1][1]  = 0.51;	z_pT_Bin_Borders[12][1][2]  = 0.2;	z_pT_Bin_Borders[12][1][3]  = 0.05;	Phi_h_Bin_Values[12][1][0]  =  24;	Phi_h_Bin_Values[12][1][1]  = 0;	Phi_h_Bin_Values[12][1][2]  = 8052;
z_pT_Bin_Borders[12][2][0]  = 0.7;	z_pT_Bin_Borders[12][2][1]  = 0.51;	z_pT_Bin_Borders[12][2][2]  = 0.28;	z_pT_Bin_Borders[12][2][3]  = 0.2;	Phi_h_Bin_Values[12][2][0]  =  24;	Phi_h_Bin_Values[12][2][1]  = 24;	Phi_h_Bin_Values[12][2][2]  = 8076;
z_pT_Bin_Borders[12][3][0]  = 0.7;	z_pT_Bin_Borders[12][3][1]  = 0.51;	z_pT_Bin_Borders[12][3][2]  = 0.36;	z_pT_Bin_Borders[12][3][3]  = 0.28;	Phi_h_Bin_Values[12][3][0]  =  24;	Phi_h_Bin_Values[12][3][1]  = 48;	Phi_h_Bin_Values[12][3][2]  = 8100;
z_pT_Bin_Borders[12][4][0]  = 0.7;	z_pT_Bin_Borders[12][4][1]  = 0.51;	z_pT_Bin_Borders[12][4][2]  = 0.45;	z_pT_Bin_Borders[12][4][3]  = 0.36;	Phi_h_Bin_Values[12][4][0]  =  24;	Phi_h_Bin_Values[12][4][1]  = 72;	Phi_h_Bin_Values[12][4][2]  = 8124;
z_pT_Bin_Borders[12][5][0]  = 0.7;	z_pT_Bin_Borders[12][5][1]  = 0.51;	z_pT_Bin_Borders[12][5][2]  = 0.6;	z_pT_Bin_Borders[12][5][3]  = 0.45;	Phi_h_Bin_Values[12][5][0]  =  1;	Phi_h_Bin_Values[12][5][1]  = 96;	Phi_h_Bin_Values[12][5][2]  = 8148;
z_pT_Bin_Borders[12][6][0]  = 0.51;	z_pT_Bin_Borders[12][6][1]  = 0.43;	z_pT_Bin_Borders[12][6][2]  = 0.2;	z_pT_Bin_Borders[12][6][3]  = 0.05;	Phi_h_Bin_Values[12][6][0]  =  24;	Phi_h_Bin_Values[12][6][1]  = 97;	Phi_h_Bin_Values[12][6][2]  = 8149;
z_pT_Bin_Borders[12][7][0]  = 0.51;	z_pT_Bin_Borders[12][7][1]  = 0.43;	z_pT_Bin_Borders[12][7][2]  = 0.28;	z_pT_Bin_Borders[12][7][3]  = 0.2;	Phi_h_Bin_Values[12][7][0]  =  24;	Phi_h_Bin_Values[12][7][1]  = 121;	Phi_h_Bin_Values[12][7][2]  = 8173;
z_pT_Bin_Borders[12][8][0]  = 0.51;	z_pT_Bin_Borders[12][8][1]  = 0.43;	z_pT_Bin_Borders[12][8][2]  = 0.36;	z_pT_Bin_Borders[12][8][3]  = 0.28;	Phi_h_Bin_Values[12][8][0]  =  24;	Phi_h_Bin_Values[12][8][1]  = 145;	Phi_h_Bin_Values[12][8][2]  = 8197;
z_pT_Bin_Borders[12][9][0]  = 0.51;	z_pT_Bin_Borders[12][9][1]  = 0.43;	z_pT_Bin_Borders[12][9][2]  = 0.45;	z_pT_Bin_Borders[12][9][3]  = 0.36;	Phi_h_Bin_Values[12][9][0]  =  24;	Phi_h_Bin_Values[12][9][1]  = 169;	Phi_h_Bin_Values[12][9][2]  = 8221;
z_pT_Bin_Borders[12][10][0] = 0.51;	z_pT_Bin_Borders[12][10][1] = 0.43;	z_pT_Bin_Borders[12][10][2] = 0.6;	z_pT_Bin_Borders[12][10][3] = 0.45;	Phi_h_Bin_Values[12][10][0] =  24;	Phi_h_Bin_Values[12][10][1] = 193;	Phi_h_Bin_Values[12][10][2] = 8245;
z_pT_Bin_Borders[12][11][0] = 0.43;	z_pT_Bin_Borders[12][11][1] = 0.37;	z_pT_Bin_Borders[12][11][2] = 0.2;	z_pT_Bin_Borders[12][11][3] = 0.05;	Phi_h_Bin_Values[12][11][0] =  24;	Phi_h_Bin_Values[12][11][1] = 217;	Phi_h_Bin_Values[12][11][2] = 8269;
z_pT_Bin_Borders[12][12][0] = 0.43;	z_pT_Bin_Borders[12][12][1] = 0.37;	z_pT_Bin_Borders[12][12][2] = 0.28;	z_pT_Bin_Borders[12][12][3] = 0.2;	Phi_h_Bin_Values[12][12][0] =  24;	Phi_h_Bin_Values[12][12][1] = 241;	Phi_h_Bin_Values[12][12][2] = 8293;
z_pT_Bin_Borders[12][13][0] = 0.43;	z_pT_Bin_Borders[12][13][1] = 0.37;	z_pT_Bin_Borders[12][13][2] = 0.36;	z_pT_Bin_Borders[12][13][3] = 0.28;	Phi_h_Bin_Values[12][13][0] =  24;	Phi_h_Bin_Values[12][13][1] = 265;	Phi_h_Bin_Values[12][13][2] = 8317;
z_pT_Bin_Borders[12][14][0] = 0.43;	z_pT_Bin_Borders[12][14][1] = 0.37;	z_pT_Bin_Borders[12][14][2] = 0.45;	z_pT_Bin_Borders[12][14][3] = 0.36;	Phi_h_Bin_Values[12][14][0] =  24;	Phi_h_Bin_Values[12][14][1] = 289;	Phi_h_Bin_Values[12][14][2] = 8341;
z_pT_Bin_Borders[12][15][0] = 0.43;	z_pT_Bin_Borders[12][15][1] = 0.37;	z_pT_Bin_Borders[12][15][2] = 0.6;	z_pT_Bin_Borders[12][15][3] = 0.45;	Phi_h_Bin_Values[12][15][0] =  24;	Phi_h_Bin_Values[12][15][1] = 313;	Phi_h_Bin_Values[12][15][2] = 8365;
z_pT_Bin_Borders[12][16][0] = 0.37;	z_pT_Bin_Borders[12][16][1] = 0.33;	z_pT_Bin_Borders[12][16][2] = 0.2;	z_pT_Bin_Borders[12][16][3] = 0.05;	Phi_h_Bin_Values[12][16][0] =  24;	Phi_h_Bin_Values[12][16][1] = 337;	Phi_h_Bin_Values[12][16][2] = 8389;
z_pT_Bin_Borders[12][17][0] = 0.37;	z_pT_Bin_Borders[12][17][1] = 0.33;	z_pT_Bin_Borders[12][17][2] = 0.28;	z_pT_Bin_Borders[12][17][3] = 0.2;	Phi_h_Bin_Values[12][17][0] =  24;	Phi_h_Bin_Values[12][17][1] = 361;	Phi_h_Bin_Values[12][17][2] = 8413;
z_pT_Bin_Borders[12][18][0] = 0.37;	z_pT_Bin_Borders[12][18][1] = 0.33;	z_pT_Bin_Borders[12][18][2] = 0.36;	z_pT_Bin_Borders[12][18][3] = 0.28;	Phi_h_Bin_Values[12][18][0] =  24;	Phi_h_Bin_Values[12][18][1] = 385;	Phi_h_Bin_Values[12][18][2] = 8437;
z_pT_Bin_Borders[12][19][0] = 0.37;	z_pT_Bin_Borders[12][19][1] = 0.33;	z_pT_Bin_Borders[12][19][2] = 0.45;	z_pT_Bin_Borders[12][19][3] = 0.36;	Phi_h_Bin_Values[12][19][0] =  24;	Phi_h_Bin_Values[12][19][1] = 409;	Phi_h_Bin_Values[12][19][2] = 8461;
z_pT_Bin_Borders[12][20][0] = 0.37;	z_pT_Bin_Borders[12][20][1] = 0.33;	z_pT_Bin_Borders[12][20][2] = 0.6;	z_pT_Bin_Borders[12][20][3] = 0.45;	Phi_h_Bin_Values[12][20][0] =  24;	Phi_h_Bin_Values[12][20][1] = 433;	Phi_h_Bin_Values[12][20][2] = 8485;
z_pT_Bin_Borders[12][21][0] = 0.33;	z_pT_Bin_Borders[12][21][1] = 0.27;	z_pT_Bin_Borders[12][21][2] = 0.2;	z_pT_Bin_Borders[12][21][3] = 0.05;	Phi_h_Bin_Values[12][21][0] =  24;	Phi_h_Bin_Values[12][21][1] = 457;	Phi_h_Bin_Values[12][21][2] = 8509;
z_pT_Bin_Borders[12][22][0] = 0.33;	z_pT_Bin_Borders[12][22][1] = 0.27;	z_pT_Bin_Borders[12][22][2] = 0.28;	z_pT_Bin_Borders[12][22][3] = 0.2;	Phi_h_Bin_Values[12][22][0] =  24;	Phi_h_Bin_Values[12][22][1] = 481;	Phi_h_Bin_Values[12][22][2] = 8533;
z_pT_Bin_Borders[12][23][0] = 0.33;	z_pT_Bin_Borders[12][23][1] = 0.27;	z_pT_Bin_Borders[12][23][2] = 0.36;	z_pT_Bin_Borders[12][23][3] = 0.28;	Phi_h_Bin_Values[12][23][0] =  24;	Phi_h_Bin_Values[12][23][1] = 505;	Phi_h_Bin_Values[12][23][2] = 8557;
z_pT_Bin_Borders[12][24][0] = 0.33;	z_pT_Bin_Borders[12][24][1] = 0.27;	z_pT_Bin_Borders[12][24][2] = 0.45;	z_pT_Bin_Borders[12][24][3] = 0.36;	Phi_h_Bin_Values[12][24][0] =  24;	Phi_h_Bin_Values[12][24][1] = 529;	Phi_h_Bin_Values[12][24][2] = 8581;
z_pT_Bin_Borders[12][25][0] = 0.33;	z_pT_Bin_Borders[12][25][1] = 0.27;	z_pT_Bin_Borders[12][25][2] = 0.6;	z_pT_Bin_Borders[12][25][3] = 0.45;	Phi_h_Bin_Values[12][25][0] =  24;	Phi_h_Bin_Values[12][25][1] = 553;	Phi_h_Bin_Values[12][25][2] = 8605;
z_pT_Bin_Borders[13][1][0]  = 0.72;	z_pT_Bin_Borders[13][1][1]  = 0.46;	z_pT_Bin_Borders[13][1][2]  = 0.22;	z_pT_Bin_Borders[13][1][3]  = 0.05;	Phi_h_Bin_Values[13][1][0]  =  24;	Phi_h_Bin_Values[13][1][1]  = 0;	Phi_h_Bin_Values[13][1][2]  = 8629;
z_pT_Bin_Borders[13][2][0]  = 0.72;	z_pT_Bin_Borders[13][2][1]  = 0.46;	z_pT_Bin_Borders[13][2][2]  = 0.34;	z_pT_Bin_Borders[13][2][3]  = 0.22;	Phi_h_Bin_Values[13][2][0]  =  24;	Phi_h_Bin_Values[13][2][1]  = 24;	Phi_h_Bin_Values[13][2][2]  = 8653;
z_pT_Bin_Borders[13][3][0]  = 0.72;	z_pT_Bin_Borders[13][3][1]  = 0.46;	z_pT_Bin_Borders[13][3][2]  = 0.44;	z_pT_Bin_Borders[13][3][3]  = 0.34;	Phi_h_Bin_Values[13][3][0]  =  24;	Phi_h_Bin_Values[13][3][1]  = 48;	Phi_h_Bin_Values[13][3][2]  = 8677;
z_pT_Bin_Borders[13][4][0]  = 0.72;	z_pT_Bin_Borders[13][4][1]  = 0.46;	z_pT_Bin_Borders[13][4][2]  = 0.58;	z_pT_Bin_Borders[13][4][3]  = 0.44;	Phi_h_Bin_Values[13][4][0]  =  24;	Phi_h_Bin_Values[13][4][1]  = 72;	Phi_h_Bin_Values[13][4][2]  = 8701;
z_pT_Bin_Borders[13][5][0]  = 0.72;	z_pT_Bin_Borders[13][5][1]  = 0.46;	z_pT_Bin_Borders[13][5][2]  = 0.9;	z_pT_Bin_Borders[13][5][3]  = 0.58;	Phi_h_Bin_Values[13][5][0]  =  24;	Phi_h_Bin_Values[13][5][1]  = 96;	Phi_h_Bin_Values[13][5][2]  = 8725;
z_pT_Bin_Borders[13][6][0]  = 0.46;	z_pT_Bin_Borders[13][6][1]  = 0.35;	z_pT_Bin_Borders[13][6][2]  = 0.22;	z_pT_Bin_Borders[13][6][3]  = 0.05;	Phi_h_Bin_Values[13][6][0]  =  24;	Phi_h_Bin_Values[13][6][1]  = 120;	Phi_h_Bin_Values[13][6][2]  = 8749;
z_pT_Bin_Borders[13][7][0]  = 0.46;	z_pT_Bin_Borders[13][7][1]  = 0.35;	z_pT_Bin_Borders[13][7][2]  = 0.34;	z_pT_Bin_Borders[13][7][3]  = 0.22;	Phi_h_Bin_Values[13][7][0]  =  24;	Phi_h_Bin_Values[13][7][1]  = 144;	Phi_h_Bin_Values[13][7][2]  = 8773;
z_pT_Bin_Borders[13][8][0]  = 0.46;	z_pT_Bin_Borders[13][8][1]  = 0.35;	z_pT_Bin_Borders[13][8][2]  = 0.44;	z_pT_Bin_Borders[13][8][3]  = 0.34;	Phi_h_Bin_Values[13][8][0]  =  24;	Phi_h_Bin_Values[13][8][1]  = 168;	Phi_h_Bin_Values[13][8][2]  = 8797;
z_pT_Bin_Borders[13][9][0]  = 0.46;	z_pT_Bin_Borders[13][9][1]  = 0.35;	z_pT_Bin_Borders[13][9][2]  = 0.58;	z_pT_Bin_Borders[13][9][3]  = 0.44;	Phi_h_Bin_Values[13][9][0]  =  24;	Phi_h_Bin_Values[13][9][1]  = 192;	Phi_h_Bin_Values[13][9][2]  = 8821;
z_pT_Bin_Borders[13][10][0] = 0.46;	z_pT_Bin_Borders[13][10][1] = 0.35;	z_pT_Bin_Borders[13][10][2] = 0.9;	z_pT_Bin_Borders[13][10][3] = 0.58;	Phi_h_Bin_Values[13][10][0] =  24;	Phi_h_Bin_Values[13][10][1] = 216;	Phi_h_Bin_Values[13][10][2] = 8845;
z_pT_Bin_Borders[13][11][0] = 0.35;	z_pT_Bin_Borders[13][11][1] = 0.29;	z_pT_Bin_Borders[13][11][2] = 0.22;	z_pT_Bin_Borders[13][11][3] = 0.05;	Phi_h_Bin_Values[13][11][0] =  24;	Phi_h_Bin_Values[13][11][1] = 240;	Phi_h_Bin_Values[13][11][2] = 8869;
z_pT_Bin_Borders[13][12][0] = 0.35;	z_pT_Bin_Borders[13][12][1] = 0.29;	z_pT_Bin_Borders[13][12][2] = 0.34;	z_pT_Bin_Borders[13][12][3] = 0.22;	Phi_h_Bin_Values[13][12][0] =  24;	Phi_h_Bin_Values[13][12][1] = 264;	Phi_h_Bin_Values[13][12][2] = 8893;
z_pT_Bin_Borders[13][13][0] = 0.35;	z_pT_Bin_Borders[13][13][1] = 0.29;	z_pT_Bin_Borders[13][13][2] = 0.44;	z_pT_Bin_Borders[13][13][3] = 0.34;	Phi_h_Bin_Values[13][13][0] =  24;	Phi_h_Bin_Values[13][13][1] = 288;	Phi_h_Bin_Values[13][13][2] = 8917;
z_pT_Bin_Borders[13][14][0] = 0.35;	z_pT_Bin_Borders[13][14][1] = 0.29;	z_pT_Bin_Borders[13][14][2] = 0.58;	z_pT_Bin_Borders[13][14][3] = 0.44;	Phi_h_Bin_Values[13][14][0] =  24;	Phi_h_Bin_Values[13][14][1] = 312;	Phi_h_Bin_Values[13][14][2] = 8941;
z_pT_Bin_Borders[13][15][0] = 0.35;	z_pT_Bin_Borders[13][15][1] = 0.29;	z_pT_Bin_Borders[13][15][2] = 0.9;	z_pT_Bin_Borders[13][15][3] = 0.58;	Phi_h_Bin_Values[13][15][0] =  24;	Phi_h_Bin_Values[13][15][1] = 336;	Phi_h_Bin_Values[13][15][2] = 8965;
z_pT_Bin_Borders[13][16][0] = 0.29;	z_pT_Bin_Borders[13][16][1] = 0.24;	z_pT_Bin_Borders[13][16][2] = 0.22;	z_pT_Bin_Borders[13][16][3] = 0.05;	Phi_h_Bin_Values[13][16][0] =  24;	Phi_h_Bin_Values[13][16][1] = 360;	Phi_h_Bin_Values[13][16][2] = 8989;
z_pT_Bin_Borders[13][17][0] = 0.29;	z_pT_Bin_Borders[13][17][1] = 0.24;	z_pT_Bin_Borders[13][17][2] = 0.34;	z_pT_Bin_Borders[13][17][3] = 0.22;	Phi_h_Bin_Values[13][17][0] =  24;	Phi_h_Bin_Values[13][17][1] = 384;	Phi_h_Bin_Values[13][17][2] = 9013;
z_pT_Bin_Borders[13][18][0] = 0.29;	z_pT_Bin_Borders[13][18][1] = 0.24;	z_pT_Bin_Borders[13][18][2] = 0.44;	z_pT_Bin_Borders[13][18][3] = 0.34;	Phi_h_Bin_Values[13][18][0] =  24;	Phi_h_Bin_Values[13][18][1] = 408;	Phi_h_Bin_Values[13][18][2] = 9037;
z_pT_Bin_Borders[13][19][0] = 0.29;	z_pT_Bin_Borders[13][19][1] = 0.24;	z_pT_Bin_Borders[13][19][2] = 0.58;	z_pT_Bin_Borders[13][19][3] = 0.44;	Phi_h_Bin_Values[13][19][0] =  24;	Phi_h_Bin_Values[13][19][1] = 432;	Phi_h_Bin_Values[13][19][2] = 9061;
z_pT_Bin_Borders[13][20][0] = 0.29;	z_pT_Bin_Borders[13][20][1] = 0.24;	z_pT_Bin_Borders[13][20][2] = 0.9;	z_pT_Bin_Borders[13][20][3] = 0.58;	Phi_h_Bin_Values[13][20][0] =  1;	Phi_h_Bin_Values[13][20][1] = 456;	Phi_h_Bin_Values[13][20][2] = 9085;
z_pT_Bin_Borders[13][21][0] = 0.24;	z_pT_Bin_Borders[13][21][1] = 0.2;	z_pT_Bin_Borders[13][21][2] = 0.22;	z_pT_Bin_Borders[13][21][3] = 0.05;	Phi_h_Bin_Values[13][21][0] =  24;	Phi_h_Bin_Values[13][21][1] = 457;	Phi_h_Bin_Values[13][21][2] = 9086;
z_pT_Bin_Borders[13][22][0] = 0.24;	z_pT_Bin_Borders[13][22][1] = 0.2;	z_pT_Bin_Borders[13][22][2] = 0.34;	z_pT_Bin_Borders[13][22][3] = 0.22;	Phi_h_Bin_Values[13][22][0] =  24;	Phi_h_Bin_Values[13][22][1] = 481;	Phi_h_Bin_Values[13][22][2] = 9110;
z_pT_Bin_Borders[13][23][0] = 0.24;	z_pT_Bin_Borders[13][23][1] = 0.2;	z_pT_Bin_Borders[13][23][2] = 0.44;	z_pT_Bin_Borders[13][23][3] = 0.34;	Phi_h_Bin_Values[13][23][0] =  24;	Phi_h_Bin_Values[13][23][1] = 505;	Phi_h_Bin_Values[13][23][2] = 9134;
z_pT_Bin_Borders[13][24][0] = 0.24;	z_pT_Bin_Borders[13][24][1] = 0.2;	z_pT_Bin_Borders[13][24][2] = 0.58;	z_pT_Bin_Borders[13][24][3] = 0.44;	Phi_h_Bin_Values[13][24][0] =  24;	Phi_h_Bin_Values[13][24][1] = 529;	Phi_h_Bin_Values[13][24][2] = 9158;
z_pT_Bin_Borders[13][25][0] = 0.24;	z_pT_Bin_Borders[13][25][1] = 0.2;	z_pT_Bin_Borders[13][25][2] = 0.9;	z_pT_Bin_Borders[13][25][3] = 0.58;	Phi_h_Bin_Values[13][25][0] =  1;	Phi_h_Bin_Values[13][25][1] = 553;	Phi_h_Bin_Values[13][25][2] = 9182;
z_pT_Bin_Borders[13][26][0] = 0.2;	z_pT_Bin_Borders[13][26][1] = 0.16;	z_pT_Bin_Borders[13][26][2] = 0.22;	z_pT_Bin_Borders[13][26][3] = 0.05;	Phi_h_Bin_Values[13][26][0] =  24;	Phi_h_Bin_Values[13][26][1] = 554;	Phi_h_Bin_Values[13][26][2] = 9183;
z_pT_Bin_Borders[13][27][0] = 0.2;	z_pT_Bin_Borders[13][27][1] = 0.16;	z_pT_Bin_Borders[13][27][2] = 0.34;	z_pT_Bin_Borders[13][27][3] = 0.22;	Phi_h_Bin_Values[13][27][0] =  24;	Phi_h_Bin_Values[13][27][1] = 578;	Phi_h_Bin_Values[13][27][2] = 9207;
z_pT_Bin_Borders[13][28][0] = 0.2;	z_pT_Bin_Borders[13][28][1] = 0.16;	z_pT_Bin_Borders[13][28][2] = 0.44;	z_pT_Bin_Borders[13][28][3] = 0.34;	Phi_h_Bin_Values[13][28][0] =  24;	Phi_h_Bin_Values[13][28][1] = 602;	Phi_h_Bin_Values[13][28][2] = 9231;
z_pT_Bin_Borders[13][29][0] = 0.2;	z_pT_Bin_Borders[13][29][1] = 0.16;	z_pT_Bin_Borders[13][29][2] = 0.58;	z_pT_Bin_Borders[13][29][3] = 0.44;	Phi_h_Bin_Values[13][29][0] =  1;	Phi_h_Bin_Values[13][29][1] = 626;	Phi_h_Bin_Values[13][29][2] = 9255;
z_pT_Bin_Borders[13][30][0] = 0.2;	z_pT_Bin_Borders[13][30][1] = 0.16;	z_pT_Bin_Borders[13][30][2] = 0.9;	z_pT_Bin_Borders[13][30][3] = 0.58;	Phi_h_Bin_Values[13][30][0] =  1;	Phi_h_Bin_Values[13][30][1] = 627;	Phi_h_Bin_Values[13][30][2] = 9256;
z_pT_Bin_Borders[14][1][0]  = 0.71;	z_pT_Bin_Borders[14][1][1]  = 0.5;	z_pT_Bin_Borders[14][1][2]  = 0.21;	z_pT_Bin_Borders[14][1][3]  = 0.05;	Phi_h_Bin_Values[14][1][0]  =  24;	Phi_h_Bin_Values[14][1][1]  = 0;	Phi_h_Bin_Values[14][1][2]  = 9257;
z_pT_Bin_Borders[14][2][0]  = 0.71;	z_pT_Bin_Borders[14][2][1]  = 0.5;	z_pT_Bin_Borders[14][2][2]  = 0.31;	z_pT_Bin_Borders[14][2][3]  = 0.21;	Phi_h_Bin_Values[14][2][0]  =  24;	Phi_h_Bin_Values[14][2][1]  = 24;	Phi_h_Bin_Values[14][2][2]  = 9281;
z_pT_Bin_Borders[14][3][0]  = 0.71;	z_pT_Bin_Borders[14][3][1]  = 0.5;	z_pT_Bin_Borders[14][3][2]  = 0.4;	z_pT_Bin_Borders[14][3][3]  = 0.31;	Phi_h_Bin_Values[14][3][0]  =  24;	Phi_h_Bin_Values[14][3][1]  = 48;	Phi_h_Bin_Values[14][3][2]  = 9305;
z_pT_Bin_Borders[14][4][0]  = 0.71;	z_pT_Bin_Borders[14][4][1]  = 0.5;	z_pT_Bin_Borders[14][4][2]  = 0.5;	z_pT_Bin_Borders[14][4][3]  = 0.4;	Phi_h_Bin_Values[14][4][0]  =  24;	Phi_h_Bin_Values[14][4][1]  = 72;	Phi_h_Bin_Values[14][4][2]  = 9329;
z_pT_Bin_Borders[14][5][0]  = 0.71;	z_pT_Bin_Borders[14][5][1]  = 0.5;	z_pT_Bin_Borders[14][5][2]  = 0.64;	z_pT_Bin_Borders[14][5][3]  = 0.5;	Phi_h_Bin_Values[14][5][0]  =  24;	Phi_h_Bin_Values[14][5][1]  = 96;	Phi_h_Bin_Values[14][5][2]  = 9353;
z_pT_Bin_Borders[14][6][0]  = 0.71;	z_pT_Bin_Borders[14][6][1]  = 0.5;	z_pT_Bin_Borders[14][6][2]  = 0.9;	z_pT_Bin_Borders[14][6][3]  = 0.64;	Phi_h_Bin_Values[14][6][0]  =  24;	Phi_h_Bin_Values[14][6][1]  = 120;	Phi_h_Bin_Values[14][6][2]  = 9377;
z_pT_Bin_Borders[14][7][0]  = 0.5;	z_pT_Bin_Borders[14][7][1]  = 0.39;	z_pT_Bin_Borders[14][7][2]  = 0.21;	z_pT_Bin_Borders[14][7][3]  = 0.05;	Phi_h_Bin_Values[14][7][0]  =  24;	Phi_h_Bin_Values[14][7][1]  = 144;	Phi_h_Bin_Values[14][7][2]  = 9401;
z_pT_Bin_Borders[14][8][0]  = 0.5;	z_pT_Bin_Borders[14][8][1]  = 0.39;	z_pT_Bin_Borders[14][8][2]  = 0.31;	z_pT_Bin_Borders[14][8][3]  = 0.21;	Phi_h_Bin_Values[14][8][0]  =  24;	Phi_h_Bin_Values[14][8][1]  = 168;	Phi_h_Bin_Values[14][8][2]  = 9425;
z_pT_Bin_Borders[14][9][0]  = 0.5;	z_pT_Bin_Borders[14][9][1]  = 0.39;	z_pT_Bin_Borders[14][9][2]  = 0.4;	z_pT_Bin_Borders[14][9][3]  = 0.31;	Phi_h_Bin_Values[14][9][0]  =  24;	Phi_h_Bin_Values[14][9][1]  = 192;	Phi_h_Bin_Values[14][9][2]  = 9449;
z_pT_Bin_Borders[14][10][0] = 0.5;	z_pT_Bin_Borders[14][10][1] = 0.39;	z_pT_Bin_Borders[14][10][2] = 0.5;	z_pT_Bin_Borders[14][10][3] = 0.4;	Phi_h_Bin_Values[14][10][0] =  24;	Phi_h_Bin_Values[14][10][1] = 216;	Phi_h_Bin_Values[14][10][2] = 9473;
z_pT_Bin_Borders[14][11][0] = 0.5;	z_pT_Bin_Borders[14][11][1] = 0.39;	z_pT_Bin_Borders[14][11][2] = 0.64;	z_pT_Bin_Borders[14][11][3] = 0.5;	Phi_h_Bin_Values[14][11][0] =  24;	Phi_h_Bin_Values[14][11][1] = 240;	Phi_h_Bin_Values[14][11][2] = 9497;
z_pT_Bin_Borders[14][12][0] = 0.5;	z_pT_Bin_Borders[14][12][1] = 0.39;	z_pT_Bin_Borders[14][12][2] = 0.9;	z_pT_Bin_Borders[14][12][3] = 0.64;	Phi_h_Bin_Values[14][12][0] =  24;	Phi_h_Bin_Values[14][12][1] = 264;	Phi_h_Bin_Values[14][12][2] = 9521;
z_pT_Bin_Borders[14][13][0] = 0.39;	z_pT_Bin_Borders[14][13][1] = 0.32;	z_pT_Bin_Borders[14][13][2] = 0.21;	z_pT_Bin_Borders[14][13][3] = 0.05;	Phi_h_Bin_Values[14][13][0] =  24;	Phi_h_Bin_Values[14][13][1] = 288;	Phi_h_Bin_Values[14][13][2] = 9545;
z_pT_Bin_Borders[14][14][0] = 0.39;	z_pT_Bin_Borders[14][14][1] = 0.32;	z_pT_Bin_Borders[14][14][2] = 0.31;	z_pT_Bin_Borders[14][14][3] = 0.21;	Phi_h_Bin_Values[14][14][0] =  24;	Phi_h_Bin_Values[14][14][1] = 312;	Phi_h_Bin_Values[14][14][2] = 9569;
z_pT_Bin_Borders[14][15][0] = 0.39;	z_pT_Bin_Borders[14][15][1] = 0.32;	z_pT_Bin_Borders[14][15][2] = 0.4;	z_pT_Bin_Borders[14][15][3] = 0.31;	Phi_h_Bin_Values[14][15][0] =  24;	Phi_h_Bin_Values[14][15][1] = 336;	Phi_h_Bin_Values[14][15][2] = 9593;
z_pT_Bin_Borders[14][16][0] = 0.39;	z_pT_Bin_Borders[14][16][1] = 0.32;	z_pT_Bin_Borders[14][16][2] = 0.5;	z_pT_Bin_Borders[14][16][3] = 0.4;	Phi_h_Bin_Values[14][16][0] =  24;	Phi_h_Bin_Values[14][16][1] = 360;	Phi_h_Bin_Values[14][16][2] = 9617;
z_pT_Bin_Borders[14][17][0] = 0.39;	z_pT_Bin_Borders[14][17][1] = 0.32;	z_pT_Bin_Borders[14][17][2] = 0.64;	z_pT_Bin_Borders[14][17][3] = 0.5;	Phi_h_Bin_Values[14][17][0] =  24;	Phi_h_Bin_Values[14][17][1] = 384;	Phi_h_Bin_Values[14][17][2] = 9641;
z_pT_Bin_Borders[14][18][0] = 0.39;	z_pT_Bin_Borders[14][18][1] = 0.32;	z_pT_Bin_Borders[14][18][2] = 0.9;	z_pT_Bin_Borders[14][18][3] = 0.64;	Phi_h_Bin_Values[14][18][0] =  24;	Phi_h_Bin_Values[14][18][1] = 408;	Phi_h_Bin_Values[14][18][2] = 9665;
z_pT_Bin_Borders[14][19][0] = 0.32;	z_pT_Bin_Borders[14][19][1] = 0.27;	z_pT_Bin_Borders[14][19][2] = 0.21;	z_pT_Bin_Borders[14][19][3] = 0.05;	Phi_h_Bin_Values[14][19][0] =  24;	Phi_h_Bin_Values[14][19][1] = 432;	Phi_h_Bin_Values[14][19][2] = 9689;
z_pT_Bin_Borders[14][20][0] = 0.32;	z_pT_Bin_Borders[14][20][1] = 0.27;	z_pT_Bin_Borders[14][20][2] = 0.31;	z_pT_Bin_Borders[14][20][3] = 0.21;	Phi_h_Bin_Values[14][20][0] =  24;	Phi_h_Bin_Values[14][20][1] = 456;	Phi_h_Bin_Values[14][20][2] = 9713;
z_pT_Bin_Borders[14][21][0] = 0.32;	z_pT_Bin_Borders[14][21][1] = 0.27;	z_pT_Bin_Borders[14][21][2] = 0.4;	z_pT_Bin_Borders[14][21][3] = 0.31;	Phi_h_Bin_Values[14][21][0] =  24;	Phi_h_Bin_Values[14][21][1] = 480;	Phi_h_Bin_Values[14][21][2] = 9737;
z_pT_Bin_Borders[14][22][0] = 0.32;	z_pT_Bin_Borders[14][22][1] = 0.27;	z_pT_Bin_Borders[14][22][2] = 0.5;	z_pT_Bin_Borders[14][22][3] = 0.4;	Phi_h_Bin_Values[14][22][0] =  24;	Phi_h_Bin_Values[14][22][1] = 504;	Phi_h_Bin_Values[14][22][2] = 9761;
z_pT_Bin_Borders[14][23][0] = 0.32;	z_pT_Bin_Borders[14][23][1] = 0.27;	z_pT_Bin_Borders[14][23][2] = 0.64;	z_pT_Bin_Borders[14][23][3] = 0.5;	Phi_h_Bin_Values[14][23][0] =  24;	Phi_h_Bin_Values[14][23][1] = 528;	Phi_h_Bin_Values[14][23][2] = 9785;
z_pT_Bin_Borders[14][24][0] = 0.32;	z_pT_Bin_Borders[14][24][1] = 0.27;	z_pT_Bin_Borders[14][24][2] = 0.9;	z_pT_Bin_Borders[14][24][3] = 0.64;	Phi_h_Bin_Values[14][24][0] =  1;	Phi_h_Bin_Values[14][24][1] = 552;	Phi_h_Bin_Values[14][24][2] = 9809;
z_pT_Bin_Borders[14][25][0] = 0.27;	z_pT_Bin_Borders[14][25][1] = 0.23;	z_pT_Bin_Borders[14][25][2] = 0.21;	z_pT_Bin_Borders[14][25][3] = 0.05;	Phi_h_Bin_Values[14][25][0] =  24;	Phi_h_Bin_Values[14][25][1] = 553;	Phi_h_Bin_Values[14][25][2] = 9810;
z_pT_Bin_Borders[14][26][0] = 0.27;	z_pT_Bin_Borders[14][26][1] = 0.23;	z_pT_Bin_Borders[14][26][2] = 0.31;	z_pT_Bin_Borders[14][26][3] = 0.21;	Phi_h_Bin_Values[14][26][0] =  24;	Phi_h_Bin_Values[14][26][1] = 577;	Phi_h_Bin_Values[14][26][2] = 9834;
z_pT_Bin_Borders[14][27][0] = 0.27;	z_pT_Bin_Borders[14][27][1] = 0.23;	z_pT_Bin_Borders[14][27][2] = 0.4;	z_pT_Bin_Borders[14][27][3] = 0.31;	Phi_h_Bin_Values[14][27][0] =  24;	Phi_h_Bin_Values[14][27][1] = 601;	Phi_h_Bin_Values[14][27][2] = 9858;
z_pT_Bin_Borders[14][28][0] = 0.27;	z_pT_Bin_Borders[14][28][1] = 0.23;	z_pT_Bin_Borders[14][28][2] = 0.5;	z_pT_Bin_Borders[14][28][3] = 0.4;	Phi_h_Bin_Values[14][28][0] =  24;	Phi_h_Bin_Values[14][28][1] = 625;	Phi_h_Bin_Values[14][28][2] = 9882;
z_pT_Bin_Borders[14][29][0] = 0.27;	z_pT_Bin_Borders[14][29][1] = 0.23;	z_pT_Bin_Borders[14][29][2] = 0.64;	z_pT_Bin_Borders[14][29][3] = 0.5;	Phi_h_Bin_Values[14][29][0] =  24;	Phi_h_Bin_Values[14][29][1] = 649;	Phi_h_Bin_Values[14][29][2] = 9906;
z_pT_Bin_Borders[14][30][0] = 0.27;	z_pT_Bin_Borders[14][30][1] = 0.23;	z_pT_Bin_Borders[14][30][2] = 0.9;	z_pT_Bin_Borders[14][30][3] = 0.64;	Phi_h_Bin_Values[14][30][0] =  1;	Phi_h_Bin_Values[14][30][1] = 673;	Phi_h_Bin_Values[14][30][2] = 9930;
z_pT_Bin_Borders[14][31][0] = 0.23;	z_pT_Bin_Borders[14][31][1] = 0.19;	z_pT_Bin_Borders[14][31][2] = 0.21;	z_pT_Bin_Borders[14][31][3] = 0.05;	Phi_h_Bin_Values[14][31][0] =  24;	Phi_h_Bin_Values[14][31][1] = 674;	Phi_h_Bin_Values[14][31][2] = 9931;
z_pT_Bin_Borders[14][32][0] = 0.23;	z_pT_Bin_Borders[14][32][1] = 0.19;	z_pT_Bin_Borders[14][32][2] = 0.31;	z_pT_Bin_Borders[14][32][3] = 0.21;	Phi_h_Bin_Values[14][32][0] =  24;	Phi_h_Bin_Values[14][32][1] = 698;	Phi_h_Bin_Values[14][32][2] = 9955;
z_pT_Bin_Borders[14][33][0] = 0.23;	z_pT_Bin_Borders[14][33][1] = 0.19;	z_pT_Bin_Borders[14][33][2] = 0.4;	z_pT_Bin_Borders[14][33][3] = 0.31;	Phi_h_Bin_Values[14][33][0] =  24;	Phi_h_Bin_Values[14][33][1] = 722;	Phi_h_Bin_Values[14][33][2] = 9979;
z_pT_Bin_Borders[14][34][0] = 0.23;	z_pT_Bin_Borders[14][34][1] = 0.19;	z_pT_Bin_Borders[14][34][2] = 0.5;	z_pT_Bin_Borders[14][34][3] = 0.4;	Phi_h_Bin_Values[14][34][0] =  24;	Phi_h_Bin_Values[14][34][1] = 746;	Phi_h_Bin_Values[14][34][2] = 10003;
z_pT_Bin_Borders[14][35][0] = 0.23;	z_pT_Bin_Borders[14][35][1] = 0.19;	z_pT_Bin_Borders[14][35][2] = 0.64;	z_pT_Bin_Borders[14][35][3] = 0.5;	Phi_h_Bin_Values[14][35][0] =  1;	Phi_h_Bin_Values[14][35][1] = 770;	Phi_h_Bin_Values[14][35][2] = 10027;
z_pT_Bin_Borders[14][36][0] = 0.23;	z_pT_Bin_Borders[14][36][1] = 0.19;	z_pT_Bin_Borders[14][36][2] = 0.9;	z_pT_Bin_Borders[14][36][3] = 0.64;	Phi_h_Bin_Values[14][36][0] =  1;	Phi_h_Bin_Values[14][36][1] = 771;	Phi_h_Bin_Values[14][36][2] = 10028;
z_pT_Bin_Borders[15][1][0]  = 0.73;	z_pT_Bin_Borders[15][1][1]  = 0.49;	z_pT_Bin_Borders[15][1][2]  = 0.22;	z_pT_Bin_Borders[15][1][3]  = 0.05;	Phi_h_Bin_Values[15][1][0]  =  24;	Phi_h_Bin_Values[15][1][1]  = 0;	Phi_h_Bin_Values[15][1][2]  = 10029;
z_pT_Bin_Borders[15][2][0]  = 0.73;	z_pT_Bin_Borders[15][2][1]  = 0.49;	z_pT_Bin_Borders[15][2][2]  = 0.32;	z_pT_Bin_Borders[15][2][3]  = 0.22;	Phi_h_Bin_Values[15][2][0]  =  24;	Phi_h_Bin_Values[15][2][1]  = 24;	Phi_h_Bin_Values[15][2][2]  = 10053;
z_pT_Bin_Borders[15][3][0]  = 0.73;	z_pT_Bin_Borders[15][3][1]  = 0.49;	z_pT_Bin_Borders[15][3][2]  = 0.42;	z_pT_Bin_Borders[15][3][3]  = 0.32;	Phi_h_Bin_Values[15][3][0]  =  24;	Phi_h_Bin_Values[15][3][1]  = 48;	Phi_h_Bin_Values[15][3][2]  = 10077;
z_pT_Bin_Borders[15][4][0]  = 0.73;	z_pT_Bin_Borders[15][4][1]  = 0.49;	z_pT_Bin_Borders[15][4][2]  = 0.55;	z_pT_Bin_Borders[15][4][3]  = 0.42;	Phi_h_Bin_Values[15][4][0]  =  24;	Phi_h_Bin_Values[15][4][1]  = 72;	Phi_h_Bin_Values[15][4][2]  = 10101;
z_pT_Bin_Borders[15][5][0]  = 0.73;	z_pT_Bin_Borders[15][5][1]  = 0.49;	z_pT_Bin_Borders[15][5][2]  = 0.8;	z_pT_Bin_Borders[15][5][3]  = 0.55;	Phi_h_Bin_Values[15][5][0]  =  1;	Phi_h_Bin_Values[15][5][1]  = 96;	Phi_h_Bin_Values[15][5][2]  = 10125;
z_pT_Bin_Borders[15][6][0]  = 0.49;	z_pT_Bin_Borders[15][6][1]  = 0.4;	z_pT_Bin_Borders[15][6][2]  = 0.22;	z_pT_Bin_Borders[15][6][3]  = 0.05;	Phi_h_Bin_Values[15][6][0]  =  24;	Phi_h_Bin_Values[15][6][1]  = 97;	Phi_h_Bin_Values[15][6][2]  = 10126;
z_pT_Bin_Borders[15][7][0]  = 0.49;	z_pT_Bin_Borders[15][7][1]  = 0.4;	z_pT_Bin_Borders[15][7][2]  = 0.32;	z_pT_Bin_Borders[15][7][3]  = 0.22;	Phi_h_Bin_Values[15][7][0]  =  24;	Phi_h_Bin_Values[15][7][1]  = 121;	Phi_h_Bin_Values[15][7][2]  = 10150;
z_pT_Bin_Borders[15][8][0]  = 0.49;	z_pT_Bin_Borders[15][8][1]  = 0.4;	z_pT_Bin_Borders[15][8][2]  = 0.42;	z_pT_Bin_Borders[15][8][3]  = 0.32;	Phi_h_Bin_Values[15][8][0]  =  24;	Phi_h_Bin_Values[15][8][1]  = 145;	Phi_h_Bin_Values[15][8][2]  = 10174;
z_pT_Bin_Borders[15][9][0]  = 0.49;	z_pT_Bin_Borders[15][9][1]  = 0.4;	z_pT_Bin_Borders[15][9][2]  = 0.55;	z_pT_Bin_Borders[15][9][3]  = 0.42;	Phi_h_Bin_Values[15][9][0]  =  24;	Phi_h_Bin_Values[15][9][1]  = 169;	Phi_h_Bin_Values[15][9][2]  = 10198;
z_pT_Bin_Borders[15][10][0] = 0.49;	z_pT_Bin_Borders[15][10][1] = 0.4;	z_pT_Bin_Borders[15][10][2] = 0.8;	z_pT_Bin_Borders[15][10][3] = 0.55;	Phi_h_Bin_Values[15][10][0] =  24;	Phi_h_Bin_Values[15][10][1] = 193;	Phi_h_Bin_Values[15][10][2] = 10222;
z_pT_Bin_Borders[15][11][0] = 0.4;	z_pT_Bin_Borders[15][11][1] = 0.32;	z_pT_Bin_Borders[15][11][2] = 0.22;	z_pT_Bin_Borders[15][11][3] = 0.05;	Phi_h_Bin_Values[15][11][0] =  24;	Phi_h_Bin_Values[15][11][1] = 217;	Phi_h_Bin_Values[15][11][2] = 10246;
z_pT_Bin_Borders[15][12][0] = 0.4;	z_pT_Bin_Borders[15][12][1] = 0.32;	z_pT_Bin_Borders[15][12][2] = 0.32;	z_pT_Bin_Borders[15][12][3] = 0.22;	Phi_h_Bin_Values[15][12][0] =  24;	Phi_h_Bin_Values[15][12][1] = 241;	Phi_h_Bin_Values[15][12][2] = 10270;
z_pT_Bin_Borders[15][13][0] = 0.4;	z_pT_Bin_Borders[15][13][1] = 0.32;	z_pT_Bin_Borders[15][13][2] = 0.42;	z_pT_Bin_Borders[15][13][3] = 0.32;	Phi_h_Bin_Values[15][13][0] =  24;	Phi_h_Bin_Values[15][13][1] = 265;	Phi_h_Bin_Values[15][13][2] = 10294;
z_pT_Bin_Borders[15][14][0] = 0.4;	z_pT_Bin_Borders[15][14][1] = 0.32;	z_pT_Bin_Borders[15][14][2] = 0.55;	z_pT_Bin_Borders[15][14][3] = 0.42;	Phi_h_Bin_Values[15][14][0] =  24;	Phi_h_Bin_Values[15][14][1] = 289;	Phi_h_Bin_Values[15][14][2] = 10318;
z_pT_Bin_Borders[15][15][0] = 0.4;	z_pT_Bin_Borders[15][15][1] = 0.32;	z_pT_Bin_Borders[15][15][2] = 0.8;	z_pT_Bin_Borders[15][15][3] = 0.55;	Phi_h_Bin_Values[15][15][0] =  24;	Phi_h_Bin_Values[15][15][1] = 313;	Phi_h_Bin_Values[15][15][2] = 10342;
z_pT_Bin_Borders[15][16][0] = 0.32;	z_pT_Bin_Borders[15][16][1] = 0.27;	z_pT_Bin_Borders[15][16][2] = 0.22;	z_pT_Bin_Borders[15][16][3] = 0.05;	Phi_h_Bin_Values[15][16][0] =  24;	Phi_h_Bin_Values[15][16][1] = 337;	Phi_h_Bin_Values[15][16][2] = 10366;
z_pT_Bin_Borders[15][17][0] = 0.32;	z_pT_Bin_Borders[15][17][1] = 0.27;	z_pT_Bin_Borders[15][17][2] = 0.32;	z_pT_Bin_Borders[15][17][3] = 0.22;	Phi_h_Bin_Values[15][17][0] =  24;	Phi_h_Bin_Values[15][17][1] = 361;	Phi_h_Bin_Values[15][17][2] = 10390;
z_pT_Bin_Borders[15][18][0] = 0.32;	z_pT_Bin_Borders[15][18][1] = 0.27;	z_pT_Bin_Borders[15][18][2] = 0.42;	z_pT_Bin_Borders[15][18][3] = 0.32;	Phi_h_Bin_Values[15][18][0] =  24;	Phi_h_Bin_Values[15][18][1] = 385;	Phi_h_Bin_Values[15][18][2] = 10414;
z_pT_Bin_Borders[15][19][0] = 0.32;	z_pT_Bin_Borders[15][19][1] = 0.27;	z_pT_Bin_Borders[15][19][2] = 0.55;	z_pT_Bin_Borders[15][19][3] = 0.42;	Phi_h_Bin_Values[15][19][0] =  24;	Phi_h_Bin_Values[15][19][1] = 409;	Phi_h_Bin_Values[15][19][2] = 10438;
z_pT_Bin_Borders[15][20][0] = 0.32;	z_pT_Bin_Borders[15][20][1] = 0.27;	z_pT_Bin_Borders[15][20][2] = 0.8;	z_pT_Bin_Borders[15][20][3] = 0.55;	Phi_h_Bin_Values[15][20][0] =  1;	Phi_h_Bin_Values[15][20][1] = 433;	Phi_h_Bin_Values[15][20][2] = 10462;
z_pT_Bin_Borders[15][21][0] = 0.27;	z_pT_Bin_Borders[15][21][1] = 0.22;	z_pT_Bin_Borders[15][21][2] = 0.22;	z_pT_Bin_Borders[15][21][3] = 0.05;	Phi_h_Bin_Values[15][21][0] =  24;	Phi_h_Bin_Values[15][21][1] = 434;	Phi_h_Bin_Values[15][21][2] = 10463;
z_pT_Bin_Borders[15][22][0] = 0.27;	z_pT_Bin_Borders[15][22][1] = 0.22;	z_pT_Bin_Borders[15][22][2] = 0.32;	z_pT_Bin_Borders[15][22][3] = 0.22;	Phi_h_Bin_Values[15][22][0] =  24;	Phi_h_Bin_Values[15][22][1] = 458;	Phi_h_Bin_Values[15][22][2] = 10487;
z_pT_Bin_Borders[15][23][0] = 0.27;	z_pT_Bin_Borders[15][23][1] = 0.22;	z_pT_Bin_Borders[15][23][2] = 0.42;	z_pT_Bin_Borders[15][23][3] = 0.32;	Phi_h_Bin_Values[15][23][0] =  24;	Phi_h_Bin_Values[15][23][1] = 482;	Phi_h_Bin_Values[15][23][2] = 10511;
z_pT_Bin_Borders[15][24][0] = 0.27;	z_pT_Bin_Borders[15][24][1] = 0.22;	z_pT_Bin_Borders[15][24][2] = 0.55;	z_pT_Bin_Borders[15][24][3] = 0.42;	Phi_h_Bin_Values[15][24][0] =  24;	Phi_h_Bin_Values[15][24][1] = 506;	Phi_h_Bin_Values[15][24][2] = 10535;
z_pT_Bin_Borders[15][25][0] = 0.27;	z_pT_Bin_Borders[15][25][1] = 0.22;	z_pT_Bin_Borders[15][25][2] = 0.8;	z_pT_Bin_Borders[15][25][3] = 0.55;	Phi_h_Bin_Values[15][25][0] =  1;	Phi_h_Bin_Values[15][25][1] = 530;	Phi_h_Bin_Values[15][25][2] = 10559;
z_pT_Bin_Borders[16][1][0]  = 0.67;	z_pT_Bin_Borders[16][1][1]  = 0.42;	z_pT_Bin_Borders[16][1][2]  = 0.22;	z_pT_Bin_Borders[16][1][3]  = 0.05;	Phi_h_Bin_Values[16][1][0]  =  24;	Phi_h_Bin_Values[16][1][1]  = 0;	Phi_h_Bin_Values[16][1][2]  = 10560;
z_pT_Bin_Borders[16][2][0]  = 0.67;	z_pT_Bin_Borders[16][2][1]  = 0.42;	z_pT_Bin_Borders[16][2][2]  = 0.32;	z_pT_Bin_Borders[16][2][3]  = 0.22;	Phi_h_Bin_Values[16][2][0]  =  24;	Phi_h_Bin_Values[16][2][1]  = 24;	Phi_h_Bin_Values[16][2][2]  = 10584;
z_pT_Bin_Borders[16][3][0]  = 0.67;	z_pT_Bin_Borders[16][3][1]  = 0.42;	z_pT_Bin_Borders[16][3][2]  = 0.42;	z_pT_Bin_Borders[16][3][3]  = 0.32;	Phi_h_Bin_Values[16][3][0]  =  24;	Phi_h_Bin_Values[16][3][1]  = 48;	Phi_h_Bin_Values[16][3][2]  = 10608;
z_pT_Bin_Borders[16][4][0]  = 0.67;	z_pT_Bin_Borders[16][4][1]  = 0.42;	z_pT_Bin_Borders[16][4][2]  = 0.52;	z_pT_Bin_Borders[16][4][3]  = 0.42;	Phi_h_Bin_Values[16][4][0]  =  24;	Phi_h_Bin_Values[16][4][1]  = 72;	Phi_h_Bin_Values[16][4][2]  = 10632;
z_pT_Bin_Borders[16][5][0]  = 0.67;	z_pT_Bin_Borders[16][5][1]  = 0.42;	z_pT_Bin_Borders[16][5][2]  = 0.66;	z_pT_Bin_Borders[16][5][3]  = 0.52;	Phi_h_Bin_Values[16][5][0]  =  24;	Phi_h_Bin_Values[16][5][1]  = 96;	Phi_h_Bin_Values[16][5][2]  = 10656;
z_pT_Bin_Borders[16][6][0]  = 0.67;	z_pT_Bin_Borders[16][6][1]  = 0.42;	z_pT_Bin_Borders[16][6][2]  = 0.9;	z_pT_Bin_Borders[16][6][3]  = 0.66;	Phi_h_Bin_Values[16][6][0]  =  24;	Phi_h_Bin_Values[16][6][1]  = 120;	Phi_h_Bin_Values[16][6][2]  = 10680;
z_pT_Bin_Borders[16][7][0]  = 0.42;	z_pT_Bin_Borders[16][7][1]  = 0.31;	z_pT_Bin_Borders[16][7][2]  = 0.22;	z_pT_Bin_Borders[16][7][3]  = 0.05;	Phi_h_Bin_Values[16][7][0]  =  24;	Phi_h_Bin_Values[16][7][1]  = 144;	Phi_h_Bin_Values[16][7][2]  = 10704;
z_pT_Bin_Borders[16][8][0]  = 0.42;	z_pT_Bin_Borders[16][8][1]  = 0.31;	z_pT_Bin_Borders[16][8][2]  = 0.32;	z_pT_Bin_Borders[16][8][3]  = 0.22;	Phi_h_Bin_Values[16][8][0]  =  24;	Phi_h_Bin_Values[16][8][1]  = 168;	Phi_h_Bin_Values[16][8][2]  = 10728;
z_pT_Bin_Borders[16][9][0]  = 0.42;	z_pT_Bin_Borders[16][9][1]  = 0.31;	z_pT_Bin_Borders[16][9][2]  = 0.42;	z_pT_Bin_Borders[16][9][3]  = 0.32;	Phi_h_Bin_Values[16][9][0]  =  24;	Phi_h_Bin_Values[16][9][1]  = 192;	Phi_h_Bin_Values[16][9][2]  = 10752;
z_pT_Bin_Borders[16][10][0] = 0.42;	z_pT_Bin_Borders[16][10][1] = 0.31;	z_pT_Bin_Borders[16][10][2] = 0.52;	z_pT_Bin_Borders[16][10][3] = 0.42;	Phi_h_Bin_Values[16][10][0] =  24;	Phi_h_Bin_Values[16][10][1] = 216;	Phi_h_Bin_Values[16][10][2] = 10776;
z_pT_Bin_Borders[16][11][0] = 0.42;	z_pT_Bin_Borders[16][11][1] = 0.31;	z_pT_Bin_Borders[16][11][2] = 0.66;	z_pT_Bin_Borders[16][11][3] = 0.52;	Phi_h_Bin_Values[16][11][0] =  24;	Phi_h_Bin_Values[16][11][1] = 240;	Phi_h_Bin_Values[16][11][2] = 10800;
z_pT_Bin_Borders[16][12][0] = 0.42;	z_pT_Bin_Borders[16][12][1] = 0.31;	z_pT_Bin_Borders[16][12][2] = 0.9;	z_pT_Bin_Borders[16][12][3] = 0.66;	Phi_h_Bin_Values[16][12][0] =  24;	Phi_h_Bin_Values[16][12][1] = 264;	Phi_h_Bin_Values[16][12][2] = 10824;
z_pT_Bin_Borders[16][13][0] = 0.31;	z_pT_Bin_Borders[16][13][1] = 0.24;	z_pT_Bin_Borders[16][13][2] = 0.22;	z_pT_Bin_Borders[16][13][3] = 0.05;	Phi_h_Bin_Values[16][13][0] =  24;	Phi_h_Bin_Values[16][13][1] = 288;	Phi_h_Bin_Values[16][13][2] = 10848;
z_pT_Bin_Borders[16][14][0] = 0.31;	z_pT_Bin_Borders[16][14][1] = 0.24;	z_pT_Bin_Borders[16][14][2] = 0.32;	z_pT_Bin_Borders[16][14][3] = 0.22;	Phi_h_Bin_Values[16][14][0] =  24;	Phi_h_Bin_Values[16][14][1] = 312;	Phi_h_Bin_Values[16][14][2] = 10872;
z_pT_Bin_Borders[16][15][0] = 0.31;	z_pT_Bin_Borders[16][15][1] = 0.24;	z_pT_Bin_Borders[16][15][2] = 0.42;	z_pT_Bin_Borders[16][15][3] = 0.32;	Phi_h_Bin_Values[16][15][0] =  24;	Phi_h_Bin_Values[16][15][1] = 336;	Phi_h_Bin_Values[16][15][2] = 10896;
z_pT_Bin_Borders[16][16][0] = 0.31;	z_pT_Bin_Borders[16][16][1] = 0.24;	z_pT_Bin_Borders[16][16][2] = 0.52;	z_pT_Bin_Borders[16][16][3] = 0.42;	Phi_h_Bin_Values[16][16][0] =  24;	Phi_h_Bin_Values[16][16][1] = 360;	Phi_h_Bin_Values[16][16][2] = 10920;
z_pT_Bin_Borders[16][17][0] = 0.31;	z_pT_Bin_Borders[16][17][1] = 0.24;	z_pT_Bin_Borders[16][17][2] = 0.66;	z_pT_Bin_Borders[16][17][3] = 0.52;	Phi_h_Bin_Values[16][17][0] =  24;	Phi_h_Bin_Values[16][17][1] = 384;	Phi_h_Bin_Values[16][17][2] = 10944;
z_pT_Bin_Borders[16][18][0] = 0.31;	z_pT_Bin_Borders[16][18][1] = 0.24;	z_pT_Bin_Borders[16][18][2] = 0.9;	z_pT_Bin_Borders[16][18][3] = 0.66;	Phi_h_Bin_Values[16][18][0] =  1;	Phi_h_Bin_Values[16][18][1] = 408;	Phi_h_Bin_Values[16][18][2] = 10968;
z_pT_Bin_Borders[16][19][0] = 0.24;	z_pT_Bin_Borders[16][19][1] = 0.2;	z_pT_Bin_Borders[16][19][2] = 0.22;	z_pT_Bin_Borders[16][19][3] = 0.05;	Phi_h_Bin_Values[16][19][0] =  24;	Phi_h_Bin_Values[16][19][1] = 409;	Phi_h_Bin_Values[16][19][2] = 10969;
z_pT_Bin_Borders[16][20][0] = 0.24;	z_pT_Bin_Borders[16][20][1] = 0.2;	z_pT_Bin_Borders[16][20][2] = 0.32;	z_pT_Bin_Borders[16][20][3] = 0.22;	Phi_h_Bin_Values[16][20][0] =  24;	Phi_h_Bin_Values[16][20][1] = 433;	Phi_h_Bin_Values[16][20][2] = 10993;
z_pT_Bin_Borders[16][21][0] = 0.24;	z_pT_Bin_Borders[16][21][1] = 0.2;	z_pT_Bin_Borders[16][21][2] = 0.42;	z_pT_Bin_Borders[16][21][3] = 0.32;	Phi_h_Bin_Values[16][21][0] =  24;	Phi_h_Bin_Values[16][21][1] = 457;	Phi_h_Bin_Values[16][21][2] = 11017;
z_pT_Bin_Borders[16][22][0] = 0.24;	z_pT_Bin_Borders[16][22][1] = 0.2;	z_pT_Bin_Borders[16][22][2] = 0.52;	z_pT_Bin_Borders[16][22][3] = 0.42;	Phi_h_Bin_Values[16][22][0] =  24;	Phi_h_Bin_Values[16][22][1] = 481;	Phi_h_Bin_Values[16][22][2] = 11041;
z_pT_Bin_Borders[16][23][0] = 0.24;	z_pT_Bin_Borders[16][23][1] = 0.2;	z_pT_Bin_Borders[16][23][2] = 0.66;	z_pT_Bin_Borders[16][23][3] = 0.52;	Phi_h_Bin_Values[16][23][0] =  1;	Phi_h_Bin_Values[16][23][1] = 505;	Phi_h_Bin_Values[16][23][2] = 11065;
z_pT_Bin_Borders[16][24][0] = 0.24;	z_pT_Bin_Borders[16][24][1] = 0.2;	z_pT_Bin_Borders[16][24][2] = 0.9;	z_pT_Bin_Borders[16][24][3] = 0.66;	Phi_h_Bin_Values[16][24][0] =  1;	Phi_h_Bin_Values[16][24][1] = 506;	Phi_h_Bin_Values[16][24][2] = 11066;
z_pT_Bin_Borders[16][25][0] = 0.2;	z_pT_Bin_Borders[16][25][1] = 0.16;	z_pT_Bin_Borders[16][25][2] = 0.22;	z_pT_Bin_Borders[16][25][3] = 0.05;	Phi_h_Bin_Values[16][25][0] =  24;	Phi_h_Bin_Values[16][25][1] = 507;	Phi_h_Bin_Values[16][25][2] = 11067;
z_pT_Bin_Borders[16][26][0] = 0.2;	z_pT_Bin_Borders[16][26][1] = 0.16;	z_pT_Bin_Borders[16][26][2] = 0.32;	z_pT_Bin_Borders[16][26][3] = 0.22;	Phi_h_Bin_Values[16][26][0] =  24;	Phi_h_Bin_Values[16][26][1] = 531;	Phi_h_Bin_Values[16][26][2] = 11091;
z_pT_Bin_Borders[16][27][0] = 0.2;	z_pT_Bin_Borders[16][27][1] = 0.16;	z_pT_Bin_Borders[16][27][2] = 0.42;	z_pT_Bin_Borders[16][27][3] = 0.32;	Phi_h_Bin_Values[16][27][0] =  24;	Phi_h_Bin_Values[16][27][1] = 555;	Phi_h_Bin_Values[16][27][2] = 11115;
z_pT_Bin_Borders[16][28][0] = 0.2;	z_pT_Bin_Borders[16][28][1] = 0.16;	z_pT_Bin_Borders[16][28][2] = 0.52;	z_pT_Bin_Borders[16][28][3] = 0.42;	Phi_h_Bin_Values[16][28][0] =  1;	Phi_h_Bin_Values[16][28][1] = 579;	Phi_h_Bin_Values[16][28][2] = 11139;
z_pT_Bin_Borders[16][29][0] = 0.2;	z_pT_Bin_Borders[16][29][1] = 0.16;	z_pT_Bin_Borders[16][29][2] = 0.66;	z_pT_Bin_Borders[16][29][3] = 0.52;	Phi_h_Bin_Values[16][29][0] =  1;	Phi_h_Bin_Values[16][29][1] = 580;	Phi_h_Bin_Values[16][29][2] = 11140;
z_pT_Bin_Borders[16][30][0] = 0.2;	z_pT_Bin_Borders[16][30][1] = 0.16;	z_pT_Bin_Borders[16][30][2] = 0.9;	z_pT_Bin_Borders[16][30][3] = 0.66;	Phi_h_Bin_Values[16][30][0] =  1;	Phi_h_Bin_Values[16][30][1] = 581;	Phi_h_Bin_Values[16][30][2] = 11141;
z_pT_Bin_Borders[17][1][0]  = 0.68;	z_pT_Bin_Borders[17][1][1]  = 0.44;	z_pT_Bin_Borders[17][1][2]  = 0.19;	z_pT_Bin_Borders[17][1][3]  = 0.05;	Phi_h_Bin_Values[17][1][0]  =  24;	Phi_h_Bin_Values[17][1][1]  = 0;	Phi_h_Bin_Values[17][1][2]  = 11142;
z_pT_Bin_Borders[17][2][0]  = 0.68;	z_pT_Bin_Borders[17][2][1]  = 0.44;	z_pT_Bin_Borders[17][2][2]  = 0.28;	z_pT_Bin_Borders[17][2][3]  = 0.19;	Phi_h_Bin_Values[17][2][0]  =  24;	Phi_h_Bin_Values[17][2][1]  = 24;	Phi_h_Bin_Values[17][2][2]  = 11166;
z_pT_Bin_Borders[17][3][0]  = 0.68;	z_pT_Bin_Borders[17][3][1]  = 0.44;	z_pT_Bin_Borders[17][3][2]  = 0.37;	z_pT_Bin_Borders[17][3][3]  = 0.28;	Phi_h_Bin_Values[17][3][0]  =  24;	Phi_h_Bin_Values[17][3][1]  = 48;	Phi_h_Bin_Values[17][3][2]  = 11190;
z_pT_Bin_Borders[17][4][0]  = 0.68;	z_pT_Bin_Borders[17][4][1]  = 0.44;	z_pT_Bin_Borders[17][4][2]  = 0.45;	z_pT_Bin_Borders[17][4][3]  = 0.37;	Phi_h_Bin_Values[17][4][0]  =  24;	Phi_h_Bin_Values[17][4][1]  = 72;	Phi_h_Bin_Values[17][4][2]  = 11214;
z_pT_Bin_Borders[17][5][0]  = 0.68;	z_pT_Bin_Borders[17][5][1]  = 0.44;	z_pT_Bin_Borders[17][5][2]  = 0.55;	z_pT_Bin_Borders[17][5][3]  = 0.45;	Phi_h_Bin_Values[17][5][0]  =  24;	Phi_h_Bin_Values[17][5][1]  = 96;	Phi_h_Bin_Values[17][5][2]  = 11238;
z_pT_Bin_Borders[17][6][0]  = 0.68;	z_pT_Bin_Borders[17][6][1]  = 0.44;	z_pT_Bin_Borders[17][6][2]  = 0.73;	z_pT_Bin_Borders[17][6][3]  = 0.55;	Phi_h_Bin_Values[17][6][0]  =  24;	Phi_h_Bin_Values[17][6][1]  = 120;	Phi_h_Bin_Values[17][6][2]  = 11262;
z_pT_Bin_Borders[17][7][0]  = 0.44;	z_pT_Bin_Borders[17][7][1]  = 0.34;	z_pT_Bin_Borders[17][7][2]  = 0.19;	z_pT_Bin_Borders[17][7][3]  = 0.05;	Phi_h_Bin_Values[17][7][0]  =  24;	Phi_h_Bin_Values[17][7][1]  = 144;	Phi_h_Bin_Values[17][7][2]  = 11286;
z_pT_Bin_Borders[17][8][0]  = 0.44;	z_pT_Bin_Borders[17][8][1]  = 0.34;	z_pT_Bin_Borders[17][8][2]  = 0.28;	z_pT_Bin_Borders[17][8][3]  = 0.19;	Phi_h_Bin_Values[17][8][0]  =  24;	Phi_h_Bin_Values[17][8][1]  = 168;	Phi_h_Bin_Values[17][8][2]  = 11310;
z_pT_Bin_Borders[17][9][0]  = 0.44;	z_pT_Bin_Borders[17][9][1]  = 0.34;	z_pT_Bin_Borders[17][9][2]  = 0.37;	z_pT_Bin_Borders[17][9][3]  = 0.28;	Phi_h_Bin_Values[17][9][0]  =  24;	Phi_h_Bin_Values[17][9][1]  = 192;	Phi_h_Bin_Values[17][9][2]  = 11334;
z_pT_Bin_Borders[17][10][0] = 0.44;	z_pT_Bin_Borders[17][10][1] = 0.34;	z_pT_Bin_Borders[17][10][2] = 0.45;	z_pT_Bin_Borders[17][10][3] = 0.37;	Phi_h_Bin_Values[17][10][0] =  24;	Phi_h_Bin_Values[17][10][1] = 216;	Phi_h_Bin_Values[17][10][2] = 11358;
z_pT_Bin_Borders[17][11][0] = 0.44;	z_pT_Bin_Borders[17][11][1] = 0.34;	z_pT_Bin_Borders[17][11][2] = 0.55;	z_pT_Bin_Borders[17][11][3] = 0.45;	Phi_h_Bin_Values[17][11][0] =  24;	Phi_h_Bin_Values[17][11][1] = 240;	Phi_h_Bin_Values[17][11][2] = 11382;
z_pT_Bin_Borders[17][12][0] = 0.44;	z_pT_Bin_Borders[17][12][1] = 0.34;	z_pT_Bin_Borders[17][12][2] = 0.73;	z_pT_Bin_Borders[17][12][3] = 0.55;	Phi_h_Bin_Values[17][12][0] =  24;	Phi_h_Bin_Values[17][12][1] = 264;	Phi_h_Bin_Values[17][12][2] = 11406;
z_pT_Bin_Borders[17][13][0] = 0.34;	z_pT_Bin_Borders[17][13][1] = 0.28;	z_pT_Bin_Borders[17][13][2] = 0.19;	z_pT_Bin_Borders[17][13][3] = 0.05;	Phi_h_Bin_Values[17][13][0] =  24;	Phi_h_Bin_Values[17][13][1] = 288;	Phi_h_Bin_Values[17][13][2] = 11430;
z_pT_Bin_Borders[17][14][0] = 0.34;	z_pT_Bin_Borders[17][14][1] = 0.28;	z_pT_Bin_Borders[17][14][2] = 0.28;	z_pT_Bin_Borders[17][14][3] = 0.19;	Phi_h_Bin_Values[17][14][0] =  24;	Phi_h_Bin_Values[17][14][1] = 312;	Phi_h_Bin_Values[17][14][2] = 11454;
z_pT_Bin_Borders[17][15][0] = 0.34;	z_pT_Bin_Borders[17][15][1] = 0.28;	z_pT_Bin_Borders[17][15][2] = 0.37;	z_pT_Bin_Borders[17][15][3] = 0.28;	Phi_h_Bin_Values[17][15][0] =  24;	Phi_h_Bin_Values[17][15][1] = 336;	Phi_h_Bin_Values[17][15][2] = 11478;
z_pT_Bin_Borders[17][16][0] = 0.34;	z_pT_Bin_Borders[17][16][1] = 0.28;	z_pT_Bin_Borders[17][16][2] = 0.45;	z_pT_Bin_Borders[17][16][3] = 0.37;	Phi_h_Bin_Values[17][16][0] =  24;	Phi_h_Bin_Values[17][16][1] = 360;	Phi_h_Bin_Values[17][16][2] = 11502;
z_pT_Bin_Borders[17][17][0] = 0.34;	z_pT_Bin_Borders[17][17][1] = 0.28;	z_pT_Bin_Borders[17][17][2] = 0.55;	z_pT_Bin_Borders[17][17][3] = 0.45;	Phi_h_Bin_Values[17][17][0] =  24;	Phi_h_Bin_Values[17][17][1] = 384;	Phi_h_Bin_Values[17][17][2] = 11526;
z_pT_Bin_Borders[17][18][0] = 0.34;	z_pT_Bin_Borders[17][18][1] = 0.28;	z_pT_Bin_Borders[17][18][2] = 0.73;	z_pT_Bin_Borders[17][18][3] = 0.55;	Phi_h_Bin_Values[17][18][0] =  24;	Phi_h_Bin_Values[17][18][1] = 408;	Phi_h_Bin_Values[17][18][2] = 11550;
z_pT_Bin_Borders[17][19][0] = 0.28;	z_pT_Bin_Borders[17][19][1] = 0.23;	z_pT_Bin_Borders[17][19][2] = 0.19;	z_pT_Bin_Borders[17][19][3] = 0.05;	Phi_h_Bin_Values[17][19][0] =  24;	Phi_h_Bin_Values[17][19][1] = 432;	Phi_h_Bin_Values[17][19][2] = 11574;
z_pT_Bin_Borders[17][20][0] = 0.28;	z_pT_Bin_Borders[17][20][1] = 0.23;	z_pT_Bin_Borders[17][20][2] = 0.28;	z_pT_Bin_Borders[17][20][3] = 0.19;	Phi_h_Bin_Values[17][20][0] =  24;	Phi_h_Bin_Values[17][20][1] = 456;	Phi_h_Bin_Values[17][20][2] = 11598;
z_pT_Bin_Borders[17][21][0] = 0.28;	z_pT_Bin_Borders[17][21][1] = 0.23;	z_pT_Bin_Borders[17][21][2] = 0.37;	z_pT_Bin_Borders[17][21][3] = 0.28;	Phi_h_Bin_Values[17][21][0] =  24;	Phi_h_Bin_Values[17][21][1] = 480;	Phi_h_Bin_Values[17][21][2] = 11622;
z_pT_Bin_Borders[17][22][0] = 0.28;	z_pT_Bin_Borders[17][22][1] = 0.23;	z_pT_Bin_Borders[17][22][2] = 0.45;	z_pT_Bin_Borders[17][22][3] = 0.37;	Phi_h_Bin_Values[17][22][0] =  24;	Phi_h_Bin_Values[17][22][1] = 504;	Phi_h_Bin_Values[17][22][2] = 11646;
z_pT_Bin_Borders[17][23][0] = 0.28;	z_pT_Bin_Borders[17][23][1] = 0.23;	z_pT_Bin_Borders[17][23][2] = 0.55;	z_pT_Bin_Borders[17][23][3] = 0.45;	Phi_h_Bin_Values[17][23][0] =  24;	Phi_h_Bin_Values[17][23][1] = 528;	Phi_h_Bin_Values[17][23][2] = 11670;
z_pT_Bin_Borders[17][24][0] = 0.28;	z_pT_Bin_Borders[17][24][1] = 0.23;	z_pT_Bin_Borders[17][24][2] = 0.73;	z_pT_Bin_Borders[17][24][3] = 0.55;	Phi_h_Bin_Values[17][24][0] =  1;	Phi_h_Bin_Values[17][24][1] = 552;	Phi_h_Bin_Values[17][24][2] = 11694;
z_pT_Bin_Borders[17][25][0] = 0.23;	z_pT_Bin_Borders[17][25][1] = 0.19;	z_pT_Bin_Borders[17][25][2] = 0.19;	z_pT_Bin_Borders[17][25][3] = 0.05;	Phi_h_Bin_Values[17][25][0] =  24;	Phi_h_Bin_Values[17][25][1] = 553;	Phi_h_Bin_Values[17][25][2] = 11695;
z_pT_Bin_Borders[17][26][0] = 0.23;	z_pT_Bin_Borders[17][26][1] = 0.19;	z_pT_Bin_Borders[17][26][2] = 0.28;	z_pT_Bin_Borders[17][26][3] = 0.19;	Phi_h_Bin_Values[17][26][0] =  24;	Phi_h_Bin_Values[17][26][1] = 577;	Phi_h_Bin_Values[17][26][2] = 11719;
z_pT_Bin_Borders[17][27][0] = 0.23;	z_pT_Bin_Borders[17][27][1] = 0.19;	z_pT_Bin_Borders[17][27][2] = 0.37;	z_pT_Bin_Borders[17][27][3] = 0.28;	Phi_h_Bin_Values[17][27][0] =  24;	Phi_h_Bin_Values[17][27][1] = 601;	Phi_h_Bin_Values[17][27][2] = 11743;
z_pT_Bin_Borders[17][28][0] = 0.23;	z_pT_Bin_Borders[17][28][1] = 0.19;	z_pT_Bin_Borders[17][28][2] = 0.45;	z_pT_Bin_Borders[17][28][3] = 0.37;	Phi_h_Bin_Values[17][28][0] =  24;	Phi_h_Bin_Values[17][28][1] = 625;	Phi_h_Bin_Values[17][28][2] = 11767;
z_pT_Bin_Borders[17][29][0] = 0.23;	z_pT_Bin_Borders[17][29][1] = 0.19;	z_pT_Bin_Borders[17][29][2] = 0.55;	z_pT_Bin_Borders[17][29][3] = 0.45;	Phi_h_Bin_Values[17][29][0] =  1;	Phi_h_Bin_Values[17][29][1] = 649;	Phi_h_Bin_Values[17][29][2] = 11791;
z_pT_Bin_Borders[17][30][0] = 0.23;	z_pT_Bin_Borders[17][30][1] = 0.19;	z_pT_Bin_Borders[17][30][2] = 0.73;	z_pT_Bin_Borders[17][30][3] = 0.55;	Phi_h_Bin_Values[17][30][0] =  1;	Phi_h_Bin_Values[17][30][1] = 650;	Phi_h_Bin_Values[17][30][2] = 11792;
Phi_h_Bin_Values[18][1][0] = 1; Phi_h_Bin_Values[18][1][1] = 1; Phi_h_Bin_Values[18][1][2] = 11793;
Phi_h_Bin_Values[19][1][0] = 1; Phi_h_Bin_Values[19][1][1] = 1; Phi_h_Bin_Values[19][1][2] = 11794;
Phi_h_Bin_Values[20][1][0] = 1; Phi_h_Bin_Values[20][1][1] = 1; Phi_h_Bin_Values[20][1][2] = 11795;
Phi_h_Bin_Values[21][1][0] = 1; Phi_h_Bin_Values[21][1][1] = 1; Phi_h_Bin_Values[21][1][2] = 11796;
Phi_h_Bin_Values[22][1][0] = 1; Phi_h_Bin_Values[22][1][1] = 1; Phi_h_Bin_Values[22][1][2] = 11797;
Phi_h_Bin_Values[23][1][0] = 1; Phi_h_Bin_Values[23][1][1] = 1; Phi_h_Bin_Values[23][1][2] = 11798;
Phi_h_Bin_Values[24][1][0] = 1; Phi_h_Bin_Values[24][1][1] = 1; Phi_h_Bin_Values[24][1][2] = 11799;
Phi_h_Bin_Values[25][1][0] = 1; Phi_h_Bin_Values[25][1][1] = 1; Phi_h_Bin_Values[25][1][2] = 11800;
Phi_h_Bin_Values[26][1][0] = 1; Phi_h_Bin_Values[26][1][1] = 1; Phi_h_Bin_Values[26][1][2] = 11801;
Phi_h_Bin_Values[27][1][0] = 1; Phi_h_Bin_Values[27][1][1] = 1; Phi_h_Bin_Values[27][1][2] = 11802;
Phi_h_Bin_Values[28][1][0] = 1; Phi_h_Bin_Values[28][1][1] = 1; Phi_h_Bin_Values[28][1][2] = 11803;
Phi_h_Bin_Values[29][1][0] = 1; Phi_h_Bin_Values[29][1][1] = 1; Phi_h_Bin_Values[29][1][2] = 11804;
Phi_h_Bin_Values[30][1][0] = 1; Phi_h_Bin_Values[30][1][1] = 1; Phi_h_Bin_Values[30][1][2] = 11805;
Phi_h_Bin_Values[31][1][0] = 1; Phi_h_Bin_Values[31][1][1] = 1; Phi_h_Bin_Values[31][1][2] = 11806;
Phi_h_Bin_Values[32][1][0] = 1; Phi_h_Bin_Values[32][1][1] = 1; Phi_h_Bin_Values[32][1][2] = 11807;
Phi_h_Bin_Values[33][1][0] = 1; Phi_h_Bin_Values[33][1][1] = 1; Phi_h_Bin_Values[33][1][2] = 11808;
Phi_h_Bin_Values[34][1][0] = 1; Phi_h_Bin_Values[34][1][1] = 1; Phi_h_Bin_Values[34][1][2] = 11809;
Phi_h_Bin_Values[35][1][0] = 1; Phi_h_Bin_Values[35][1][1] = 1; Phi_h_Bin_Values[35][1][2] = 11810;
Phi_h_Bin_Values[36][1][0] = 1; Phi_h_Bin_Values[36][1][1] = 1; Phi_h_Bin_Values[36][1][2] = 11811;
Phi_h_Bin_Values[37][1][0] = 1; Phi_h_Bin_Values[37][1][1] = 1; Phi_h_Bin_Values[37][1][2] = 11812;
Phi_h_Bin_Values[38][1][0] = 1; Phi_h_Bin_Values[38][1][1] = 1; Phi_h_Bin_Values[38][1][2] = 11813;
Phi_h_Bin_Values[39][1][0] = 1; Phi_h_Bin_Values[39][1][1] = 1; Phi_h_Bin_Values[39][1][2] = 11814;
auto Find_z_pT_Bin = [&](int Q2_y_Bin_Num_Value, double Z_Value, double PT_Value){
    int z_pT_Bin_Max = 1;
    // 'z_pT_Bin_Max' Includes both the main kinematic bins AND the overflow/migration bins
    if(Q2_y_Bin_Num_Value ==  1){z_pT_Bin_Max = 35;}
    if(Q2_y_Bin_Num_Value ==  2){z_pT_Bin_Max = 36;}
    if(Q2_y_Bin_Num_Value ==  3){z_pT_Bin_Max = 30;}
    if(Q2_y_Bin_Num_Value ==  4){z_pT_Bin_Max = 36;}
    if(Q2_y_Bin_Num_Value ==  5){z_pT_Bin_Max = 36;}
    if(Q2_y_Bin_Num_Value ==  6){z_pT_Bin_Max = 30;}
    if(Q2_y_Bin_Num_Value ==  7){z_pT_Bin_Max = 36;}
    if(Q2_y_Bin_Num_Value ==  8){z_pT_Bin_Max = 35;}
    if(Q2_y_Bin_Num_Value ==  9){z_pT_Bin_Max = 35;}
    if(Q2_y_Bin_Num_Value == 10){z_pT_Bin_Max = 36;}
    if(Q2_y_Bin_Num_Value == 11){z_pT_Bin_Max = 25;}
    if(Q2_y_Bin_Num_Value == 12){z_pT_Bin_Max = 25;}
    if(Q2_y_Bin_Num_Value == 13){z_pT_Bin_Max = 30;}
    if(Q2_y_Bin_Num_Value == 14){z_pT_Bin_Max = 36;}
    if(Q2_y_Bin_Num_Value == 15){z_pT_Bin_Max = 25;}
    if(Q2_y_Bin_Num_Value == 16){z_pT_Bin_Max = 30;}
    if(Q2_y_Bin_Num_Value == 17){z_pT_Bin_Max = 30;}
    
    if(Q2_y_Bin_Num_Value < 1 || Q2_y_Bin_Num_Value > 17){return 0;} // The overflow Q2-y bins do not have defined z-pT bins
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
    return 0; // Event to go into z-pT overflow bins
};
auto Find_phi_h_Bin  = [&](int Q2_y_Bin_Num_Value, int Z_PT_Bin_Num_Value, double PHI_H_Value){
    int Num_PHI_BINS = Phi_h_Bin_Values[Q2_y_Bin_Num_Value][Z_PT_Bin_Num_Value][0];
    if(Num_PHI_BINS <= 1){return Num_PHI_BINS;}
    else{
        double bin_size = 360/Num_PHI_BINS;
        int PHI_BIN     = (PHI_H_Value/bin_size) + 1;
        if(PHI_H_Value == 360){PHI_BIN = Num_PHI_BINS;} // Include 360 in the last phi_h bin
        return PHI_BIN;
    }
    return -1; // ERROR: Events should not return -1
};
'''

New_Integrated_z_pT_and_MultiDim_Binning_Code = '''
int Integrate_Phi_h_Bin_Values[18][26][3];
 // Integrate_Phi_h_Bin_Values[Q2_y_Bin][z_pT_Bin][Dimension]
    // Dimension = 0 -> Number of phi_h bins (24)
    // Dimension = 1 -> Number of combined z_pT + phi_h bins        (used for 3D unfolding - add the appropiate phi_h bin number to these values to get the 3D bin number - resets with every new Q2-y bin)
    // Dimension = 2 -> Number of combined Q2_y + z_pT + phi_h bins (used for 5D unfolding - add the appropiate phi_h bin number to these values to get the 5D bin number - does not resets with new bins)
    // (Total of 18 Q2-y bins without overflow bins)
Integrate_Phi_h_Bin_Values[1][1][0]   =  24;	Integrate_Phi_h_Bin_Values[1][1][1]   =   24;	Integrate_Phi_h_Bin_Values[1][1][2]   =     24;
Integrate_Phi_h_Bin_Values[1][2][0]   =  24;	Integrate_Phi_h_Bin_Values[1][2][1]   =   48;	Integrate_Phi_h_Bin_Values[1][2][2]   =     48;
Integrate_Phi_h_Bin_Values[1][3][0]   =  24;	Integrate_Phi_h_Bin_Values[1][3][1]   =   72;	Integrate_Phi_h_Bin_Values[1][3][2]   =     72;
Integrate_Phi_h_Bin_Values[1][4][0]   =  24;	Integrate_Phi_h_Bin_Values[1][4][1]   =   96;	Integrate_Phi_h_Bin_Values[1][4][2]   =     96;
Integrate_Phi_h_Bin_Values[1][5][0]   =  24;	Integrate_Phi_h_Bin_Values[1][5][1]   =  120;	Integrate_Phi_h_Bin_Values[1][5][2]   =    120;
Integrate_Phi_h_Bin_Values[1][6][0]   =  24;	Integrate_Phi_h_Bin_Values[1][6][1]   =  144;	Integrate_Phi_h_Bin_Values[1][6][2]   =    144;
Integrate_Phi_h_Bin_Values[1][7][0]   =  24;	Integrate_Phi_h_Bin_Values[1][7][1]   =  168;	Integrate_Phi_h_Bin_Values[1][7][2]   =    168;
Integrate_Phi_h_Bin_Values[1][8][0]   =  24;	Integrate_Phi_h_Bin_Values[1][8][1]   =  192;	Integrate_Phi_h_Bin_Values[1][8][2]   =    192;
Integrate_Phi_h_Bin_Values[1][9][0]   =  24;	Integrate_Phi_h_Bin_Values[1][9][1]   =  216;	Integrate_Phi_h_Bin_Values[1][9][2]   =    216;
Integrate_Phi_h_Bin_Values[1][10][0]  =  24;	Integrate_Phi_h_Bin_Values[1][10][1]  =  240;	Integrate_Phi_h_Bin_Values[1][10][2]  =    240;
Integrate_Phi_h_Bin_Values[1][11][0]  =  24;	Integrate_Phi_h_Bin_Values[1][11][1]  =  264;	Integrate_Phi_h_Bin_Values[1][11][2]  =    264;
Integrate_Phi_h_Bin_Values[1][12][0]  =  24;	Integrate_Phi_h_Bin_Values[1][12][1]  =  288;	Integrate_Phi_h_Bin_Values[1][12][2]  =    288;
Integrate_Phi_h_Bin_Values[1][13][0]  =  24;	Integrate_Phi_h_Bin_Values[1][13][1]  =  312;	Integrate_Phi_h_Bin_Values[1][13][2]  =    312;
Integrate_Phi_h_Bin_Values[1][14][0]  =  24;	Integrate_Phi_h_Bin_Values[1][14][1]  =  336;	Integrate_Phi_h_Bin_Values[1][14][2]  =    336;
Integrate_Phi_h_Bin_Values[1][15][0]  =  24;	Integrate_Phi_h_Bin_Values[1][15][1]  =  360;	Integrate_Phi_h_Bin_Values[1][15][2]  =    360;
Integrate_Phi_h_Bin_Values[1][16][0]  =  24;	Integrate_Phi_h_Bin_Values[1][16][1]  =  384;	Integrate_Phi_h_Bin_Values[1][16][2]  =    384;
Integrate_Phi_h_Bin_Values[1][17][0]  =  24;	Integrate_Phi_h_Bin_Values[1][17][1]  =  408;	Integrate_Phi_h_Bin_Values[1][17][2]  =    408;
Integrate_Phi_h_Bin_Values[1][18][0]  =  24;	Integrate_Phi_h_Bin_Values[1][18][1]  =  432;	Integrate_Phi_h_Bin_Values[1][18][2]  =    432;
Integrate_Phi_h_Bin_Values[1][19][0]  =  24;	Integrate_Phi_h_Bin_Values[1][19][1]  =  456;	Integrate_Phi_h_Bin_Values[1][19][2]  =    456;
Integrate_Phi_h_Bin_Values[1][20][0]  =  24;	Integrate_Phi_h_Bin_Values[1][20][1]  =  480;	Integrate_Phi_h_Bin_Values[1][20][2]  =    480;
Integrate_Phi_h_Bin_Values[1][21][0]  =  24;	Integrate_Phi_h_Bin_Values[1][21][1]  =  504;	Integrate_Phi_h_Bin_Values[1][21][2]  =    504;
Integrate_Phi_h_Bin_Values[1][22][0]  =  24;	Integrate_Phi_h_Bin_Values[1][22][1]  =  528;	Integrate_Phi_h_Bin_Values[1][22][2]  =    528;
Integrate_Phi_h_Bin_Values[1][23][0]  =  24;	Integrate_Phi_h_Bin_Values[1][23][1]  =  552;	Integrate_Phi_h_Bin_Values[1][23][2]  =    552;
Integrate_Phi_h_Bin_Values[1][24][0]  =  24;	Integrate_Phi_h_Bin_Values[1][24][1]  =  576;	Integrate_Phi_h_Bin_Values[1][24][2]  =    576;
Integrate_Phi_h_Bin_Values[1][25][0]  =  24;	Integrate_Phi_h_Bin_Values[1][25][1]  =  600;	Integrate_Phi_h_Bin_Values[1][25][2]  =    600;
Integrate_Phi_h_Bin_Values[2][1][0]   =  24;	Integrate_Phi_h_Bin_Values[2][1][1]   =   24;	Integrate_Phi_h_Bin_Values[2][1][2]   =    624;
Integrate_Phi_h_Bin_Values[2][2][0]   =  24;	Integrate_Phi_h_Bin_Values[2][2][1]   =   48;	Integrate_Phi_h_Bin_Values[2][2][2]   =    648;
Integrate_Phi_h_Bin_Values[2][3][0]   =  24;	Integrate_Phi_h_Bin_Values[2][3][1]   =   72;	Integrate_Phi_h_Bin_Values[2][3][2]   =    672;
Integrate_Phi_h_Bin_Values[2][4][0]   =  24;	Integrate_Phi_h_Bin_Values[2][4][1]   =   96;	Integrate_Phi_h_Bin_Values[2][4][2]   =    696;
Integrate_Phi_h_Bin_Values[2][5][0]   =  24;	Integrate_Phi_h_Bin_Values[2][5][1]   =  120;	Integrate_Phi_h_Bin_Values[2][5][2]   =    720;
Integrate_Phi_h_Bin_Values[2][6][0]   =  24;	Integrate_Phi_h_Bin_Values[2][6][1]   =  144;	Integrate_Phi_h_Bin_Values[2][6][2]   =    744;
Integrate_Phi_h_Bin_Values[2][7][0]   =  24;	Integrate_Phi_h_Bin_Values[2][7][1]   =  168;	Integrate_Phi_h_Bin_Values[2][7][2]   =    768;
Integrate_Phi_h_Bin_Values[2][8][0]   =  24;	Integrate_Phi_h_Bin_Values[2][8][1]   =  192;	Integrate_Phi_h_Bin_Values[2][8][2]   =    792;
Integrate_Phi_h_Bin_Values[2][9][0]   =  24;	Integrate_Phi_h_Bin_Values[2][9][1]   =  216;	Integrate_Phi_h_Bin_Values[2][9][2]   =    816;
Integrate_Phi_h_Bin_Values[2][10][0]  =  24;	Integrate_Phi_h_Bin_Values[2][10][1]  =  240;	Integrate_Phi_h_Bin_Values[2][10][2]  =    840;
Integrate_Phi_h_Bin_Values[2][11][0]  =  24;	Integrate_Phi_h_Bin_Values[2][11][1]  =  264;	Integrate_Phi_h_Bin_Values[2][11][2]  =    864;
Integrate_Phi_h_Bin_Values[2][12][0]  =  24;	Integrate_Phi_h_Bin_Values[2][12][1]  =  288;	Integrate_Phi_h_Bin_Values[2][12][2]  =    888;
Integrate_Phi_h_Bin_Values[2][13][0]  =  24;	Integrate_Phi_h_Bin_Values[2][13][1]  =  312;	Integrate_Phi_h_Bin_Values[2][13][2]  =    912;
Integrate_Phi_h_Bin_Values[2][14][0]  =  24;	Integrate_Phi_h_Bin_Values[2][14][1]  =  336;	Integrate_Phi_h_Bin_Values[2][14][2]  =    936;
Integrate_Phi_h_Bin_Values[2][15][0]  =  24;	Integrate_Phi_h_Bin_Values[2][15][1]  =  360;	Integrate_Phi_h_Bin_Values[2][15][2]  =    960;
Integrate_Phi_h_Bin_Values[2][16][0]  =  24;	Integrate_Phi_h_Bin_Values[2][16][1]  =  384;	Integrate_Phi_h_Bin_Values[2][16][2]  =    984;
Integrate_Phi_h_Bin_Values[2][17][0]  =  24;	Integrate_Phi_h_Bin_Values[2][17][1]  =  408;	Integrate_Phi_h_Bin_Values[2][17][2]  =   1008;
Integrate_Phi_h_Bin_Values[2][18][0]  =  24;	Integrate_Phi_h_Bin_Values[2][18][1]  =  432;	Integrate_Phi_h_Bin_Values[2][18][2]  =   1032;
Integrate_Phi_h_Bin_Values[2][19][0]  =  24;	Integrate_Phi_h_Bin_Values[2][19][1]  =  456;	Integrate_Phi_h_Bin_Values[2][19][2]  =   1056;
Integrate_Phi_h_Bin_Values[2][20][0]  =  24;	Integrate_Phi_h_Bin_Values[2][20][1]  =  480;	Integrate_Phi_h_Bin_Values[2][20][2]  =   1080;
Integrate_Phi_h_Bin_Values[2][21][0]  =  24;	Integrate_Phi_h_Bin_Values[2][21][1]  =  504;	Integrate_Phi_h_Bin_Values[2][21][2]  =   1104;
Integrate_Phi_h_Bin_Values[2][22][0]  =  24;	Integrate_Phi_h_Bin_Values[2][22][1]  =  528;	Integrate_Phi_h_Bin_Values[2][22][2]  =   1128;
Integrate_Phi_h_Bin_Values[2][23][0]  =  24;	Integrate_Phi_h_Bin_Values[2][23][1]  =  552;	Integrate_Phi_h_Bin_Values[2][23][2]  =   1152;
Integrate_Phi_h_Bin_Values[2][24][0]  =  24;	Integrate_Phi_h_Bin_Values[2][24][1]  =  576;	Integrate_Phi_h_Bin_Values[2][24][2]  =   1176;
Integrate_Phi_h_Bin_Values[2][25][0]  =  24;	Integrate_Phi_h_Bin_Values[2][25][1]  =  600;	Integrate_Phi_h_Bin_Values[2][25][2]  =   1200;
Integrate_Phi_h_Bin_Values[3][1][0]   =  24;	Integrate_Phi_h_Bin_Values[3][1][1]   =   24;	Integrate_Phi_h_Bin_Values[3][1][2]   =   1224;
Integrate_Phi_h_Bin_Values[3][2][0]   =  24;	Integrate_Phi_h_Bin_Values[3][2][1]   =   48;	Integrate_Phi_h_Bin_Values[3][2][2]   =   1248;
Integrate_Phi_h_Bin_Values[3][3][0]   =  24;	Integrate_Phi_h_Bin_Values[3][3][1]   =   72;	Integrate_Phi_h_Bin_Values[3][3][2]   =   1272;
Integrate_Phi_h_Bin_Values[3][4][0]   =  24;	Integrate_Phi_h_Bin_Values[3][4][1]   =   96;	Integrate_Phi_h_Bin_Values[3][4][2]   =   1296;
Integrate_Phi_h_Bin_Values[3][5][0]   =  24;	Integrate_Phi_h_Bin_Values[3][5][1]   =  120;	Integrate_Phi_h_Bin_Values[3][5][2]   =   1320;
Integrate_Phi_h_Bin_Values[3][6][0]   =  24;	Integrate_Phi_h_Bin_Values[3][6][1]   =  144;	Integrate_Phi_h_Bin_Values[3][6][2]   =   1344;
Integrate_Phi_h_Bin_Values[3][7][0]   =  24;	Integrate_Phi_h_Bin_Values[3][7][1]   =  168;	Integrate_Phi_h_Bin_Values[3][7][2]   =   1368;
Integrate_Phi_h_Bin_Values[3][8][0]   =  24;	Integrate_Phi_h_Bin_Values[3][8][1]   =  192;	Integrate_Phi_h_Bin_Values[3][8][2]   =   1392;
Integrate_Phi_h_Bin_Values[3][9][0]   =  24;	Integrate_Phi_h_Bin_Values[3][9][1]   =  216;	Integrate_Phi_h_Bin_Values[3][9][2]   =   1416;
Integrate_Phi_h_Bin_Values[3][10][0]  =  24;	Integrate_Phi_h_Bin_Values[3][10][1]  =  240;	Integrate_Phi_h_Bin_Values[3][10][2]  =   1440;
Integrate_Phi_h_Bin_Values[3][11][0]  =  24;	Integrate_Phi_h_Bin_Values[3][11][1]  =  264;	Integrate_Phi_h_Bin_Values[3][11][2]  =   1464;
Integrate_Phi_h_Bin_Values[3][12][0]  =  24;	Integrate_Phi_h_Bin_Values[3][12][1]  =  288;	Integrate_Phi_h_Bin_Values[3][12][2]  =   1488;
Integrate_Phi_h_Bin_Values[3][13][0]  =  24;	Integrate_Phi_h_Bin_Values[3][13][1]  =  312;	Integrate_Phi_h_Bin_Values[3][13][2]  =   1512;
Integrate_Phi_h_Bin_Values[3][14][0]  =  24;	Integrate_Phi_h_Bin_Values[3][14][1]  =  336;	Integrate_Phi_h_Bin_Values[3][14][2]  =   1536;
Integrate_Phi_h_Bin_Values[3][15][0]  =  24;	Integrate_Phi_h_Bin_Values[3][15][1]  =  360;	Integrate_Phi_h_Bin_Values[3][15][2]  =   1560;
Integrate_Phi_h_Bin_Values[3][16][0]  =  24;	Integrate_Phi_h_Bin_Values[3][16][1]  =  384;	Integrate_Phi_h_Bin_Values[3][16][2]  =   1584;
Integrate_Phi_h_Bin_Values[3][17][0]  =  24;	Integrate_Phi_h_Bin_Values[3][17][1]  =  408;	Integrate_Phi_h_Bin_Values[3][17][2]  =   1608;
Integrate_Phi_h_Bin_Values[3][18][0]  =  24;	Integrate_Phi_h_Bin_Values[3][18][1]  =  432;	Integrate_Phi_h_Bin_Values[3][18][2]  =   1632;
Integrate_Phi_h_Bin_Values[3][19][0]  =  24;	Integrate_Phi_h_Bin_Values[3][19][1]  =  456;	Integrate_Phi_h_Bin_Values[3][19][2]  =   1656;
Integrate_Phi_h_Bin_Values[3][20][0]  =  24;	Integrate_Phi_h_Bin_Values[3][20][1]  =  480;	Integrate_Phi_h_Bin_Values[3][20][2]  =   1680;
Integrate_Phi_h_Bin_Values[3][21][0]  =  24;	Integrate_Phi_h_Bin_Values[3][21][1]  =  504;	Integrate_Phi_h_Bin_Values[3][21][2]  =   1704;
Integrate_Phi_h_Bin_Values[3][22][0]  =  24;	Integrate_Phi_h_Bin_Values[3][22][1]  =  528;	Integrate_Phi_h_Bin_Values[3][22][2]  =   1728;
Integrate_Phi_h_Bin_Values[3][23][0]  =  24;	Integrate_Phi_h_Bin_Values[3][23][1]  =  552;	Integrate_Phi_h_Bin_Values[3][23][2]  =   1752;
Integrate_Phi_h_Bin_Values[3][24][0]  =  24;	Integrate_Phi_h_Bin_Values[3][24][1]  =  576;	Integrate_Phi_h_Bin_Values[3][24][2]  =   1776;
Integrate_Phi_h_Bin_Values[3][25][0]  =  24;	Integrate_Phi_h_Bin_Values[3][25][1]  =  600;	Integrate_Phi_h_Bin_Values[3][25][2]  =   1800;
Integrate_Phi_h_Bin_Values[4][1][0]   =  24;	Integrate_Phi_h_Bin_Values[4][1][1]   =   24;	Integrate_Phi_h_Bin_Values[4][1][2]   =   1824;
Integrate_Phi_h_Bin_Values[4][2][0]   =  24;	Integrate_Phi_h_Bin_Values[4][2][1]   =   48;	Integrate_Phi_h_Bin_Values[4][2][2]   =   1848;
Integrate_Phi_h_Bin_Values[4][3][0]   =  24;	Integrate_Phi_h_Bin_Values[4][3][1]   =   72;	Integrate_Phi_h_Bin_Values[4][3][2]   =   1872;
Integrate_Phi_h_Bin_Values[4][4][0]   =  24;	Integrate_Phi_h_Bin_Values[4][4][1]   =   96;	Integrate_Phi_h_Bin_Values[4][4][2]   =   1896;
Integrate_Phi_h_Bin_Values[4][5][0]   =  24;	Integrate_Phi_h_Bin_Values[4][5][1]   =  120;	Integrate_Phi_h_Bin_Values[4][5][2]   =   1920;
Integrate_Phi_h_Bin_Values[4][6][0]   =  24;	Integrate_Phi_h_Bin_Values[4][6][1]   =  144;	Integrate_Phi_h_Bin_Values[4][6][2]   =   1944;
Integrate_Phi_h_Bin_Values[4][7][0]   =  24;	Integrate_Phi_h_Bin_Values[4][7][1]   =  168;	Integrate_Phi_h_Bin_Values[4][7][2]   =   1968;
Integrate_Phi_h_Bin_Values[4][8][0]   =  24;	Integrate_Phi_h_Bin_Values[4][8][1]   =  192;	Integrate_Phi_h_Bin_Values[4][8][2]   =   1992;
Integrate_Phi_h_Bin_Values[4][9][0]   =  24;	Integrate_Phi_h_Bin_Values[4][9][1]   =  216;	Integrate_Phi_h_Bin_Values[4][9][2]   =   2016;
Integrate_Phi_h_Bin_Values[4][10][0]  =  24;	Integrate_Phi_h_Bin_Values[4][10][1]  =  240;	Integrate_Phi_h_Bin_Values[4][10][2]  =   2040;
Integrate_Phi_h_Bin_Values[4][11][0]  =  24;	Integrate_Phi_h_Bin_Values[4][11][1]  =  264;	Integrate_Phi_h_Bin_Values[4][11][2]  =   2064;
Integrate_Phi_h_Bin_Values[4][12][0]  =  24;	Integrate_Phi_h_Bin_Values[4][12][1]  =  288;	Integrate_Phi_h_Bin_Values[4][12][2]  =   2088;
Integrate_Phi_h_Bin_Values[4][13][0]  =  24;	Integrate_Phi_h_Bin_Values[4][13][1]  =  312;	Integrate_Phi_h_Bin_Values[4][13][2]  =   2112;
Integrate_Phi_h_Bin_Values[4][14][0]  =  24;	Integrate_Phi_h_Bin_Values[4][14][1]  =  336;	Integrate_Phi_h_Bin_Values[4][14][2]  =   2136;
Integrate_Phi_h_Bin_Values[4][15][0]  =  24;	Integrate_Phi_h_Bin_Values[4][15][1]  =  360;	Integrate_Phi_h_Bin_Values[4][15][2]  =   2160;
Integrate_Phi_h_Bin_Values[4][16][0]  =  24;	Integrate_Phi_h_Bin_Values[4][16][1]  =  384;	Integrate_Phi_h_Bin_Values[4][16][2]  =   2184;
Integrate_Phi_h_Bin_Values[4][17][0]  =  24;	Integrate_Phi_h_Bin_Values[4][17][1]  =  408;	Integrate_Phi_h_Bin_Values[4][17][2]  =   2208;
Integrate_Phi_h_Bin_Values[4][18][0]  =  24;	Integrate_Phi_h_Bin_Values[4][18][1]  =  432;	Integrate_Phi_h_Bin_Values[4][18][2]  =   2232;
Integrate_Phi_h_Bin_Values[4][19][0]  =  24;	Integrate_Phi_h_Bin_Values[4][19][1]  =  456;	Integrate_Phi_h_Bin_Values[4][19][2]  =   2256;
Integrate_Phi_h_Bin_Values[4][20][0]  =  24;	Integrate_Phi_h_Bin_Values[4][20][1]  =  480;	Integrate_Phi_h_Bin_Values[4][20][2]  =   2280;
Integrate_Phi_h_Bin_Values[4][21][0]  =  24;	Integrate_Phi_h_Bin_Values[4][21][1]  =  504;	Integrate_Phi_h_Bin_Values[4][21][2]  =   2304;
Integrate_Phi_h_Bin_Values[4][22][0]  =  24;	Integrate_Phi_h_Bin_Values[4][22][1]  =  528;	Integrate_Phi_h_Bin_Values[4][22][2]  =   2328;
Integrate_Phi_h_Bin_Values[4][23][0]  =  24;	Integrate_Phi_h_Bin_Values[4][23][1]  =  552;	Integrate_Phi_h_Bin_Values[4][23][2]  =   2352;
Integrate_Phi_h_Bin_Values[4][24][0]  =  24;	Integrate_Phi_h_Bin_Values[4][24][1]  =  576;	Integrate_Phi_h_Bin_Values[4][24][2]  =   2376;
Integrate_Phi_h_Bin_Values[4][25][0]  =  24;	Integrate_Phi_h_Bin_Values[4][25][1]  =  600;	Integrate_Phi_h_Bin_Values[4][25][2]  =   2400;
Integrate_Phi_h_Bin_Values[5][1][0]   =  24;	Integrate_Phi_h_Bin_Values[5][1][1]   =   24;	Integrate_Phi_h_Bin_Values[5][1][2]   =   2424;
Integrate_Phi_h_Bin_Values[5][2][0]   =  24;	Integrate_Phi_h_Bin_Values[5][2][1]   =   48;	Integrate_Phi_h_Bin_Values[5][2][2]   =   2448;
Integrate_Phi_h_Bin_Values[5][3][0]   =  24;	Integrate_Phi_h_Bin_Values[5][3][1]   =   72;	Integrate_Phi_h_Bin_Values[5][3][2]   =   2472;
Integrate_Phi_h_Bin_Values[5][4][0]   =  24;	Integrate_Phi_h_Bin_Values[5][4][1]   =   96;	Integrate_Phi_h_Bin_Values[5][4][2]   =   2496;
Integrate_Phi_h_Bin_Values[5][5][0]   =  24;	Integrate_Phi_h_Bin_Values[5][5][1]   =  120;	Integrate_Phi_h_Bin_Values[5][5][2]   =   2520;
Integrate_Phi_h_Bin_Values[5][6][0]   =  24;	Integrate_Phi_h_Bin_Values[5][6][1]   =  144;	Integrate_Phi_h_Bin_Values[5][6][2]   =   2544;
Integrate_Phi_h_Bin_Values[5][7][0]   =  24;	Integrate_Phi_h_Bin_Values[5][7][1]   =  168;	Integrate_Phi_h_Bin_Values[5][7][2]   =   2568;
Integrate_Phi_h_Bin_Values[5][8][0]   =  24;	Integrate_Phi_h_Bin_Values[5][8][1]   =  192;	Integrate_Phi_h_Bin_Values[5][8][2]   =   2592;
Integrate_Phi_h_Bin_Values[5][9][0]   =  24;	Integrate_Phi_h_Bin_Values[5][9][1]   =  216;	Integrate_Phi_h_Bin_Values[5][9][2]   =   2616;
Integrate_Phi_h_Bin_Values[5][10][0]  =  24;	Integrate_Phi_h_Bin_Values[5][10][1]  =  240;	Integrate_Phi_h_Bin_Values[5][10][2]  =   2640;
Integrate_Phi_h_Bin_Values[5][11][0]  =  24;	Integrate_Phi_h_Bin_Values[5][11][1]  =  264;	Integrate_Phi_h_Bin_Values[5][11][2]  =   2664;
Integrate_Phi_h_Bin_Values[5][12][0]  =  24;	Integrate_Phi_h_Bin_Values[5][12][1]  =  288;	Integrate_Phi_h_Bin_Values[5][12][2]  =   2688;
Integrate_Phi_h_Bin_Values[5][13][0]  =  24;	Integrate_Phi_h_Bin_Values[5][13][1]  =  312;	Integrate_Phi_h_Bin_Values[5][13][2]  =   2712;
Integrate_Phi_h_Bin_Values[5][14][0]  =  24;	Integrate_Phi_h_Bin_Values[5][14][1]  =  336;	Integrate_Phi_h_Bin_Values[5][14][2]  =   2736;
Integrate_Phi_h_Bin_Values[5][15][0]  =  24;	Integrate_Phi_h_Bin_Values[5][15][1]  =  360;	Integrate_Phi_h_Bin_Values[5][15][2]  =   2760;
Integrate_Phi_h_Bin_Values[5][16][0]  =  24;	Integrate_Phi_h_Bin_Values[5][16][1]  =  384;	Integrate_Phi_h_Bin_Values[5][16][2]  =   2784;
Integrate_Phi_h_Bin_Values[5][17][0]  =  24;	Integrate_Phi_h_Bin_Values[5][17][1]  =  408;	Integrate_Phi_h_Bin_Values[5][17][2]  =   2808;
Integrate_Phi_h_Bin_Values[5][18][0]  =  24;	Integrate_Phi_h_Bin_Values[5][18][1]  =  432;	Integrate_Phi_h_Bin_Values[5][18][2]  =   2832;
Integrate_Phi_h_Bin_Values[5][19][0]  =  24;	Integrate_Phi_h_Bin_Values[5][19][1]  =  456;	Integrate_Phi_h_Bin_Values[5][19][2]  =   2856;
Integrate_Phi_h_Bin_Values[5][20][0]  =  24;	Integrate_Phi_h_Bin_Values[5][20][1]  =  480;	Integrate_Phi_h_Bin_Values[5][20][2]  =   2880;
Integrate_Phi_h_Bin_Values[5][21][0]  =  24;	Integrate_Phi_h_Bin_Values[5][21][1]  =  504;	Integrate_Phi_h_Bin_Values[5][21][2]  =   2904;
Integrate_Phi_h_Bin_Values[5][22][0]  =  24;	Integrate_Phi_h_Bin_Values[5][22][1]  =  528;	Integrate_Phi_h_Bin_Values[5][22][2]  =   2928;
Integrate_Phi_h_Bin_Values[5][23][0]  =  24;	Integrate_Phi_h_Bin_Values[5][23][1]  =  552;	Integrate_Phi_h_Bin_Values[5][23][2]  =   2952;
Integrate_Phi_h_Bin_Values[5][24][0]  =  24;	Integrate_Phi_h_Bin_Values[5][24][1]  =  576;	Integrate_Phi_h_Bin_Values[5][24][2]  =   2976;
Integrate_Phi_h_Bin_Values[5][25][0]  =  24;	Integrate_Phi_h_Bin_Values[5][25][1]  =  600;	Integrate_Phi_h_Bin_Values[5][25][2]  =   3000;
Integrate_Phi_h_Bin_Values[6][1][0]   =  24;	Integrate_Phi_h_Bin_Values[6][1][1]   =   24;	Integrate_Phi_h_Bin_Values[6][1][2]   =   3024;
Integrate_Phi_h_Bin_Values[6][2][0]   =  24;	Integrate_Phi_h_Bin_Values[6][2][1]   =   48;	Integrate_Phi_h_Bin_Values[6][2][2]   =   3048;
Integrate_Phi_h_Bin_Values[6][3][0]   =  24;	Integrate_Phi_h_Bin_Values[6][3][1]   =   72;	Integrate_Phi_h_Bin_Values[6][3][2]   =   3072;
Integrate_Phi_h_Bin_Values[6][4][0]   =  24;	Integrate_Phi_h_Bin_Values[6][4][1]   =   96;	Integrate_Phi_h_Bin_Values[6][4][2]   =   3096;
Integrate_Phi_h_Bin_Values[6][5][0]   =  24;	Integrate_Phi_h_Bin_Values[6][5][1]   =  120;	Integrate_Phi_h_Bin_Values[6][5][2]   =   3120;
Integrate_Phi_h_Bin_Values[6][6][0]   =  24;	Integrate_Phi_h_Bin_Values[6][6][1]   =  144;	Integrate_Phi_h_Bin_Values[6][6][2]   =   3144;
Integrate_Phi_h_Bin_Values[6][7][0]   =  24;	Integrate_Phi_h_Bin_Values[6][7][1]   =  168;	Integrate_Phi_h_Bin_Values[6][7][2]   =   3168;
Integrate_Phi_h_Bin_Values[6][8][0]   =  24;	Integrate_Phi_h_Bin_Values[6][8][1]   =  192;	Integrate_Phi_h_Bin_Values[6][8][2]   =   3192;
Integrate_Phi_h_Bin_Values[6][9][0]   =  24;	Integrate_Phi_h_Bin_Values[6][9][1]   =  216;	Integrate_Phi_h_Bin_Values[6][9][2]   =   3216;
Integrate_Phi_h_Bin_Values[6][10][0]  =  24;	Integrate_Phi_h_Bin_Values[6][10][1]  =  240;	Integrate_Phi_h_Bin_Values[6][10][2]  =   3240;
Integrate_Phi_h_Bin_Values[6][11][0]  =  24;	Integrate_Phi_h_Bin_Values[6][11][1]  =  264;	Integrate_Phi_h_Bin_Values[6][11][2]  =   3264;
Integrate_Phi_h_Bin_Values[6][12][0]  =  24;	Integrate_Phi_h_Bin_Values[6][12][1]  =  288;	Integrate_Phi_h_Bin_Values[6][12][2]  =   3288;
Integrate_Phi_h_Bin_Values[6][13][0]  =  24;	Integrate_Phi_h_Bin_Values[6][13][1]  =  312;	Integrate_Phi_h_Bin_Values[6][13][2]  =   3312;
Integrate_Phi_h_Bin_Values[6][14][0]  =  24;	Integrate_Phi_h_Bin_Values[6][14][1]  =  336;	Integrate_Phi_h_Bin_Values[6][14][2]  =   3336;
Integrate_Phi_h_Bin_Values[6][15][0]  =  24;	Integrate_Phi_h_Bin_Values[6][15][1]  =  360;	Integrate_Phi_h_Bin_Values[6][15][2]  =   3360;
Integrate_Phi_h_Bin_Values[6][16][0]  =  24;	Integrate_Phi_h_Bin_Values[6][16][1]  =  384;	Integrate_Phi_h_Bin_Values[6][16][2]  =   3384;
Integrate_Phi_h_Bin_Values[6][17][0]  =  24;	Integrate_Phi_h_Bin_Values[6][17][1]  =  408;	Integrate_Phi_h_Bin_Values[6][17][2]  =   3408;
Integrate_Phi_h_Bin_Values[6][18][0]  =  24;	Integrate_Phi_h_Bin_Values[6][18][1]  =  432;	Integrate_Phi_h_Bin_Values[6][18][2]  =   3432;
Integrate_Phi_h_Bin_Values[6][19][0]  =  24;	Integrate_Phi_h_Bin_Values[6][19][1]  =  456;	Integrate_Phi_h_Bin_Values[6][19][2]  =   3456;
Integrate_Phi_h_Bin_Values[6][20][0]  =  24;	Integrate_Phi_h_Bin_Values[6][20][1]  =  480;	Integrate_Phi_h_Bin_Values[6][20][2]  =   3480;
Integrate_Phi_h_Bin_Values[6][21][0]  =  24;	Integrate_Phi_h_Bin_Values[6][21][1]  =  504;	Integrate_Phi_h_Bin_Values[6][21][2]  =   3504;
Integrate_Phi_h_Bin_Values[6][22][0]  =  24;	Integrate_Phi_h_Bin_Values[6][22][1]  =  528;	Integrate_Phi_h_Bin_Values[6][22][2]  =   3528;
Integrate_Phi_h_Bin_Values[6][23][0]  =  24;	Integrate_Phi_h_Bin_Values[6][23][1]  =  552;	Integrate_Phi_h_Bin_Values[6][23][2]  =   3552;
Integrate_Phi_h_Bin_Values[6][24][0]  =  24;	Integrate_Phi_h_Bin_Values[6][24][1]  =  576;	Integrate_Phi_h_Bin_Values[6][24][2]  =   3576;
Integrate_Phi_h_Bin_Values[6][25][0]  =  24;	Integrate_Phi_h_Bin_Values[6][25][1]  =  600;	Integrate_Phi_h_Bin_Values[6][25][2]  =   3600;
Integrate_Phi_h_Bin_Values[7][1][0]   =  24;	Integrate_Phi_h_Bin_Values[7][1][1]   =   24;	Integrate_Phi_h_Bin_Values[7][1][2]   =   3624;
Integrate_Phi_h_Bin_Values[7][2][0]   =  24;	Integrate_Phi_h_Bin_Values[7][2][1]   =   48;	Integrate_Phi_h_Bin_Values[7][2][2]   =   3648;
Integrate_Phi_h_Bin_Values[7][3][0]   =  24;	Integrate_Phi_h_Bin_Values[7][3][1]   =   72;	Integrate_Phi_h_Bin_Values[7][3][2]   =   3672;
Integrate_Phi_h_Bin_Values[7][4][0]   =  24;	Integrate_Phi_h_Bin_Values[7][4][1]   =   96;	Integrate_Phi_h_Bin_Values[7][4][2]   =   3696;
Integrate_Phi_h_Bin_Values[7][5][0]   =  24;	Integrate_Phi_h_Bin_Values[7][5][1]   =  120;	Integrate_Phi_h_Bin_Values[7][5][2]   =   3720;
Integrate_Phi_h_Bin_Values[7][6][0]   =  24;	Integrate_Phi_h_Bin_Values[7][6][1]   =  144;	Integrate_Phi_h_Bin_Values[7][6][2]   =   3744;
Integrate_Phi_h_Bin_Values[7][7][0]   =  24;	Integrate_Phi_h_Bin_Values[7][7][1]   =  168;	Integrate_Phi_h_Bin_Values[7][7][2]   =   3768;
Integrate_Phi_h_Bin_Values[7][8][0]   =  24;	Integrate_Phi_h_Bin_Values[7][8][1]   =  192;	Integrate_Phi_h_Bin_Values[7][8][2]   =   3792;
Integrate_Phi_h_Bin_Values[7][9][0]   =  24;	Integrate_Phi_h_Bin_Values[7][9][1]   =  216;	Integrate_Phi_h_Bin_Values[7][9][2]   =   3816;
Integrate_Phi_h_Bin_Values[7][10][0]  =  24;	Integrate_Phi_h_Bin_Values[7][10][1]  =  240;	Integrate_Phi_h_Bin_Values[7][10][2]  =   3840;
Integrate_Phi_h_Bin_Values[7][11][0]  =  24;	Integrate_Phi_h_Bin_Values[7][11][1]  =  264;	Integrate_Phi_h_Bin_Values[7][11][2]  =   3864;
Integrate_Phi_h_Bin_Values[7][12][0]  =  24;	Integrate_Phi_h_Bin_Values[7][12][1]  =  288;	Integrate_Phi_h_Bin_Values[7][12][2]  =   3888;
Integrate_Phi_h_Bin_Values[7][13][0]  =  24;	Integrate_Phi_h_Bin_Values[7][13][1]  =  312;	Integrate_Phi_h_Bin_Values[7][13][2]  =   3912;
Integrate_Phi_h_Bin_Values[7][14][0]  =  24;	Integrate_Phi_h_Bin_Values[7][14][1]  =  336;	Integrate_Phi_h_Bin_Values[7][14][2]  =   3936;
Integrate_Phi_h_Bin_Values[7][15][0]  =  24;	Integrate_Phi_h_Bin_Values[7][15][1]  =  360;	Integrate_Phi_h_Bin_Values[7][15][2]  =   3960;
Integrate_Phi_h_Bin_Values[7][16][0]  =  24;	Integrate_Phi_h_Bin_Values[7][16][1]  =  384;	Integrate_Phi_h_Bin_Values[7][16][2]  =   3984;
Integrate_Phi_h_Bin_Values[7][17][0]  =  24;	Integrate_Phi_h_Bin_Values[7][17][1]  =  408;	Integrate_Phi_h_Bin_Values[7][17][2]  =   4008;
Integrate_Phi_h_Bin_Values[7][18][0]  =  24;	Integrate_Phi_h_Bin_Values[7][18][1]  =  432;	Integrate_Phi_h_Bin_Values[7][18][2]  =   4032;
Integrate_Phi_h_Bin_Values[7][19][0]  =  24;	Integrate_Phi_h_Bin_Values[7][19][1]  =  456;	Integrate_Phi_h_Bin_Values[7][19][2]  =   4056;
Integrate_Phi_h_Bin_Values[7][20][0]  =  24;	Integrate_Phi_h_Bin_Values[7][20][1]  =  480;	Integrate_Phi_h_Bin_Values[7][20][2]  =   4080;
Integrate_Phi_h_Bin_Values[7][21][0]  =  24;	Integrate_Phi_h_Bin_Values[7][21][1]  =  504;	Integrate_Phi_h_Bin_Values[7][21][2]  =   4104;
Integrate_Phi_h_Bin_Values[7][22][0]  =  24;	Integrate_Phi_h_Bin_Values[7][22][1]  =  528;	Integrate_Phi_h_Bin_Values[7][22][2]  =   4128;
Integrate_Phi_h_Bin_Values[7][23][0]  =  24;	Integrate_Phi_h_Bin_Values[7][23][1]  =  552;	Integrate_Phi_h_Bin_Values[7][23][2]  =   4152;
Integrate_Phi_h_Bin_Values[7][24][0]  =  24;	Integrate_Phi_h_Bin_Values[7][24][1]  =  576;	Integrate_Phi_h_Bin_Values[7][24][2]  =   4176;
Integrate_Phi_h_Bin_Values[7][25][0]  =  24;	Integrate_Phi_h_Bin_Values[7][25][1]  =  600;	Integrate_Phi_h_Bin_Values[7][25][2]  =   4200;
Integrate_Phi_h_Bin_Values[8][1][0]   =  24;	Integrate_Phi_h_Bin_Values[8][1][1]   =   24;	Integrate_Phi_h_Bin_Values[8][1][2]   =   4224;
Integrate_Phi_h_Bin_Values[8][2][0]   =  24;	Integrate_Phi_h_Bin_Values[8][2][1]   =   48;	Integrate_Phi_h_Bin_Values[8][2][2]   =   4248;
Integrate_Phi_h_Bin_Values[8][3][0]   =  24;	Integrate_Phi_h_Bin_Values[8][3][1]   =   72;	Integrate_Phi_h_Bin_Values[8][3][2]   =   4272;
Integrate_Phi_h_Bin_Values[8][4][0]   =  24;	Integrate_Phi_h_Bin_Values[8][4][1]   =   96;	Integrate_Phi_h_Bin_Values[8][4][2]   =   4296;
Integrate_Phi_h_Bin_Values[8][5][0]   =  24;	Integrate_Phi_h_Bin_Values[8][5][1]   =  120;	Integrate_Phi_h_Bin_Values[8][5][2]   =   4320;
Integrate_Phi_h_Bin_Values[8][6][0]   =  24;	Integrate_Phi_h_Bin_Values[8][6][1]   =  144;	Integrate_Phi_h_Bin_Values[8][6][2]   =   4344;
Integrate_Phi_h_Bin_Values[8][7][0]   =  24;	Integrate_Phi_h_Bin_Values[8][7][1]   =  168;	Integrate_Phi_h_Bin_Values[8][7][2]   =   4368;
Integrate_Phi_h_Bin_Values[8][8][0]   =  24;	Integrate_Phi_h_Bin_Values[8][8][1]   =  192;	Integrate_Phi_h_Bin_Values[8][8][2]   =   4392;
Integrate_Phi_h_Bin_Values[8][9][0]   =  24;	Integrate_Phi_h_Bin_Values[8][9][1]   =  216;	Integrate_Phi_h_Bin_Values[8][9][2]   =   4416;
Integrate_Phi_h_Bin_Values[8][10][0]  =  24;	Integrate_Phi_h_Bin_Values[8][10][1]  =  240;	Integrate_Phi_h_Bin_Values[8][10][2]  =   4440;
Integrate_Phi_h_Bin_Values[8][11][0]  =  24;	Integrate_Phi_h_Bin_Values[8][11][1]  =  264;	Integrate_Phi_h_Bin_Values[8][11][2]  =   4464;
Integrate_Phi_h_Bin_Values[8][12][0]  =  24;	Integrate_Phi_h_Bin_Values[8][12][1]  =  288;	Integrate_Phi_h_Bin_Values[8][12][2]  =   4488;
Integrate_Phi_h_Bin_Values[8][13][0]  =  24;	Integrate_Phi_h_Bin_Values[8][13][1]  =  312;	Integrate_Phi_h_Bin_Values[8][13][2]  =   4512;
Integrate_Phi_h_Bin_Values[8][14][0]  =  24;	Integrate_Phi_h_Bin_Values[8][14][1]  =  336;	Integrate_Phi_h_Bin_Values[8][14][2]  =   4536;
Integrate_Phi_h_Bin_Values[8][15][0]  =  24;	Integrate_Phi_h_Bin_Values[8][15][1]  =  360;	Integrate_Phi_h_Bin_Values[8][15][2]  =   4560;
Integrate_Phi_h_Bin_Values[8][16][0]  =  24;	Integrate_Phi_h_Bin_Values[8][16][1]  =  384;	Integrate_Phi_h_Bin_Values[8][16][2]  =   4584;
Integrate_Phi_h_Bin_Values[8][17][0]  =  24;	Integrate_Phi_h_Bin_Values[8][17][1]  =  408;	Integrate_Phi_h_Bin_Values[8][17][2]  =   4608;
Integrate_Phi_h_Bin_Values[8][18][0]  =  24;	Integrate_Phi_h_Bin_Values[8][18][1]  =  432;	Integrate_Phi_h_Bin_Values[8][18][2]  =   4632;
Integrate_Phi_h_Bin_Values[8][19][0]  =  24;	Integrate_Phi_h_Bin_Values[8][19][1]  =  456;	Integrate_Phi_h_Bin_Values[8][19][2]  =   4656;
Integrate_Phi_h_Bin_Values[8][20][0]  =  24;	Integrate_Phi_h_Bin_Values[8][20][1]  =  480;	Integrate_Phi_h_Bin_Values[8][20][2]  =   4680;
Integrate_Phi_h_Bin_Values[8][21][0]  =  24;	Integrate_Phi_h_Bin_Values[8][21][1]  =  504;	Integrate_Phi_h_Bin_Values[8][21][2]  =   4704;
Integrate_Phi_h_Bin_Values[8][22][0]  =  24;	Integrate_Phi_h_Bin_Values[8][22][1]  =  528;	Integrate_Phi_h_Bin_Values[8][22][2]  =   4728;
Integrate_Phi_h_Bin_Values[8][23][0]  =  24;	Integrate_Phi_h_Bin_Values[8][23][1]  =  552;	Integrate_Phi_h_Bin_Values[8][23][2]  =   4752;
Integrate_Phi_h_Bin_Values[8][24][0]  =  24;	Integrate_Phi_h_Bin_Values[8][24][1]  =  576;	Integrate_Phi_h_Bin_Values[8][24][2]  =   4776;
Integrate_Phi_h_Bin_Values[8][25][0]  =  24;	Integrate_Phi_h_Bin_Values[8][25][1]  =  600;	Integrate_Phi_h_Bin_Values[8][25][2]  =   4800;
Integrate_Phi_h_Bin_Values[9][1][0]   =  24;	Integrate_Phi_h_Bin_Values[9][1][1]   =   24;	Integrate_Phi_h_Bin_Values[9][1][2]   =   4824;
Integrate_Phi_h_Bin_Values[9][2][0]   =  24;	Integrate_Phi_h_Bin_Values[9][2][1]   =   48;	Integrate_Phi_h_Bin_Values[9][2][2]   =   4848;
Integrate_Phi_h_Bin_Values[9][3][0]   =  24;	Integrate_Phi_h_Bin_Values[9][3][1]   =   72;	Integrate_Phi_h_Bin_Values[9][3][2]   =   4872;
Integrate_Phi_h_Bin_Values[9][4][0]   =  24;	Integrate_Phi_h_Bin_Values[9][4][1]   =   96;	Integrate_Phi_h_Bin_Values[9][4][2]   =   4896;
Integrate_Phi_h_Bin_Values[9][5][0]   =  24;	Integrate_Phi_h_Bin_Values[9][5][1]   =  120;	Integrate_Phi_h_Bin_Values[9][5][2]   =   4920;
Integrate_Phi_h_Bin_Values[9][6][0]   =  24;	Integrate_Phi_h_Bin_Values[9][6][1]   =  144;	Integrate_Phi_h_Bin_Values[9][6][2]   =   4944;
Integrate_Phi_h_Bin_Values[9][7][0]   =  24;	Integrate_Phi_h_Bin_Values[9][7][1]   =  168;	Integrate_Phi_h_Bin_Values[9][7][2]   =   4968;
Integrate_Phi_h_Bin_Values[9][8][0]   =  24;	Integrate_Phi_h_Bin_Values[9][8][1]   =  192;	Integrate_Phi_h_Bin_Values[9][8][2]   =   4992;
Integrate_Phi_h_Bin_Values[9][9][0]   =  24;	Integrate_Phi_h_Bin_Values[9][9][1]   =  216;	Integrate_Phi_h_Bin_Values[9][9][2]   =   5016;
Integrate_Phi_h_Bin_Values[9][10][0]  =  24;	Integrate_Phi_h_Bin_Values[9][10][1]  =  240;	Integrate_Phi_h_Bin_Values[9][10][2]  =   5040;
Integrate_Phi_h_Bin_Values[9][11][0]  =  24;	Integrate_Phi_h_Bin_Values[9][11][1]  =  264;	Integrate_Phi_h_Bin_Values[9][11][2]  =   5064;
Integrate_Phi_h_Bin_Values[9][12][0]  =  24;	Integrate_Phi_h_Bin_Values[9][12][1]  =  288;	Integrate_Phi_h_Bin_Values[9][12][2]  =   5088;
Integrate_Phi_h_Bin_Values[9][13][0]  =  24;	Integrate_Phi_h_Bin_Values[9][13][1]  =  312;	Integrate_Phi_h_Bin_Values[9][13][2]  =   5112;
Integrate_Phi_h_Bin_Values[9][14][0]  =  24;	Integrate_Phi_h_Bin_Values[9][14][1]  =  336;	Integrate_Phi_h_Bin_Values[9][14][2]  =   5136;
Integrate_Phi_h_Bin_Values[9][15][0]  =  24;	Integrate_Phi_h_Bin_Values[9][15][1]  =  360;	Integrate_Phi_h_Bin_Values[9][15][2]  =   5160;
Integrate_Phi_h_Bin_Values[9][16][0]  =  24;	Integrate_Phi_h_Bin_Values[9][16][1]  =  384;	Integrate_Phi_h_Bin_Values[9][16][2]  =   5184;
Integrate_Phi_h_Bin_Values[9][17][0]  =  24;	Integrate_Phi_h_Bin_Values[9][17][1]  =  408;	Integrate_Phi_h_Bin_Values[9][17][2]  =   5208;
Integrate_Phi_h_Bin_Values[9][18][0]  =  24;	Integrate_Phi_h_Bin_Values[9][18][1]  =  432;	Integrate_Phi_h_Bin_Values[9][18][2]  =   5232;
Integrate_Phi_h_Bin_Values[9][19][0]  =  24;	Integrate_Phi_h_Bin_Values[9][19][1]  =  456;	Integrate_Phi_h_Bin_Values[9][19][2]  =   5256;
Integrate_Phi_h_Bin_Values[9][20][0]  =  24;	Integrate_Phi_h_Bin_Values[9][20][1]  =  480;	Integrate_Phi_h_Bin_Values[9][20][2]  =   5280;
Integrate_Phi_h_Bin_Values[9][21][0]  =  24;	Integrate_Phi_h_Bin_Values[9][21][1]  =  504;	Integrate_Phi_h_Bin_Values[9][21][2]  =   5304;
Integrate_Phi_h_Bin_Values[9][22][0]  =  24;	Integrate_Phi_h_Bin_Values[9][22][1]  =  528;	Integrate_Phi_h_Bin_Values[9][22][2]  =   5328;
Integrate_Phi_h_Bin_Values[9][23][0]  =  24;	Integrate_Phi_h_Bin_Values[9][23][1]  =  552;	Integrate_Phi_h_Bin_Values[9][23][2]  =   5352;
Integrate_Phi_h_Bin_Values[9][24][0]  =  24;	Integrate_Phi_h_Bin_Values[9][24][1]  =  576;	Integrate_Phi_h_Bin_Values[9][24][2]  =   5376;
Integrate_Phi_h_Bin_Values[9][25][0]  =  24;	Integrate_Phi_h_Bin_Values[9][25][1]  =  600;	Integrate_Phi_h_Bin_Values[9][25][2]  =   5400;
Integrate_Phi_h_Bin_Values[10][1][0]  =  24;	Integrate_Phi_h_Bin_Values[10][1][1]  =   24;	Integrate_Phi_h_Bin_Values[10][1][2]  =   5424;
Integrate_Phi_h_Bin_Values[10][2][0]  =  24;	Integrate_Phi_h_Bin_Values[10][2][1]  =   48;	Integrate_Phi_h_Bin_Values[10][2][2]  =   5448;
Integrate_Phi_h_Bin_Values[10][3][0]  =  24;	Integrate_Phi_h_Bin_Values[10][3][1]  =   72;	Integrate_Phi_h_Bin_Values[10][3][2]  =   5472;
Integrate_Phi_h_Bin_Values[10][4][0]  =  24;	Integrate_Phi_h_Bin_Values[10][4][1]  =   96;	Integrate_Phi_h_Bin_Values[10][4][2]  =   5496;
Integrate_Phi_h_Bin_Values[10][5][0]  =  24;	Integrate_Phi_h_Bin_Values[10][5][1]  =  120;	Integrate_Phi_h_Bin_Values[10][5][2]  =   5520;
Integrate_Phi_h_Bin_Values[10][6][0]  =  24;	Integrate_Phi_h_Bin_Values[10][6][1]  =  144;	Integrate_Phi_h_Bin_Values[10][6][2]  =   5544;
Integrate_Phi_h_Bin_Values[10][7][0]  =  24;	Integrate_Phi_h_Bin_Values[10][7][1]  =  168;	Integrate_Phi_h_Bin_Values[10][7][2]  =   5568;
Integrate_Phi_h_Bin_Values[10][8][0]  =  24;	Integrate_Phi_h_Bin_Values[10][8][1]  =  192;	Integrate_Phi_h_Bin_Values[10][8][2]  =   5592;
Integrate_Phi_h_Bin_Values[10][9][0]  =  24;	Integrate_Phi_h_Bin_Values[10][9][1]  =  216;	Integrate_Phi_h_Bin_Values[10][9][2]  =   5616;
Integrate_Phi_h_Bin_Values[10][10][0] =  24;	Integrate_Phi_h_Bin_Values[10][10][1] =  240;	Integrate_Phi_h_Bin_Values[10][10][2] =   5640;
Integrate_Phi_h_Bin_Values[10][11][0] =  24;	Integrate_Phi_h_Bin_Values[10][11][1] =  264;	Integrate_Phi_h_Bin_Values[10][11][2] =   5664;
Integrate_Phi_h_Bin_Values[10][12][0] =  24;	Integrate_Phi_h_Bin_Values[10][12][1] =  288;	Integrate_Phi_h_Bin_Values[10][12][2] =   5688;
Integrate_Phi_h_Bin_Values[10][13][0] =  24;	Integrate_Phi_h_Bin_Values[10][13][1] =  312;	Integrate_Phi_h_Bin_Values[10][13][2] =   5712;
Integrate_Phi_h_Bin_Values[10][14][0] =  24;	Integrate_Phi_h_Bin_Values[10][14][1] =  336;	Integrate_Phi_h_Bin_Values[10][14][2] =   5736;
Integrate_Phi_h_Bin_Values[10][15][0] =  24;	Integrate_Phi_h_Bin_Values[10][15][1] =  360;	Integrate_Phi_h_Bin_Values[10][15][2] =   5760;
Integrate_Phi_h_Bin_Values[10][16][0] =  24;	Integrate_Phi_h_Bin_Values[10][16][1] =  384;	Integrate_Phi_h_Bin_Values[10][16][2] =   5784;
Integrate_Phi_h_Bin_Values[10][17][0] =  24;	Integrate_Phi_h_Bin_Values[10][17][1] =  408;	Integrate_Phi_h_Bin_Values[10][17][2] =   5808;
Integrate_Phi_h_Bin_Values[10][18][0] =  24;	Integrate_Phi_h_Bin_Values[10][18][1] =  432;	Integrate_Phi_h_Bin_Values[10][18][2] =   5832;
Integrate_Phi_h_Bin_Values[10][19][0] =  24;	Integrate_Phi_h_Bin_Values[10][19][1] =  456;	Integrate_Phi_h_Bin_Values[10][19][2] =   5856;
Integrate_Phi_h_Bin_Values[10][20][0] =  24;	Integrate_Phi_h_Bin_Values[10][20][1] =  480;	Integrate_Phi_h_Bin_Values[10][20][2] =   5880;
Integrate_Phi_h_Bin_Values[10][21][0] =  24;	Integrate_Phi_h_Bin_Values[10][21][1] =  504;	Integrate_Phi_h_Bin_Values[10][21][2] =   5904;
Integrate_Phi_h_Bin_Values[10][22][0] =  24;	Integrate_Phi_h_Bin_Values[10][22][1] =  528;	Integrate_Phi_h_Bin_Values[10][22][2] =   5928;
Integrate_Phi_h_Bin_Values[10][23][0] =  24;	Integrate_Phi_h_Bin_Values[10][23][1] =  552;	Integrate_Phi_h_Bin_Values[10][23][2] =   5952;
Integrate_Phi_h_Bin_Values[10][24][0] =  24;	Integrate_Phi_h_Bin_Values[10][24][1] =  576;	Integrate_Phi_h_Bin_Values[10][24][2] =   5976;
Integrate_Phi_h_Bin_Values[10][25][0] =  24;	Integrate_Phi_h_Bin_Values[10][25][1] =  600;	Integrate_Phi_h_Bin_Values[10][25][2] =   6000;
Integrate_Phi_h_Bin_Values[11][1][0]  =  24;	Integrate_Phi_h_Bin_Values[11][1][1]  =   24;	Integrate_Phi_h_Bin_Values[11][1][2]  =   6024;
Integrate_Phi_h_Bin_Values[11][2][0]  =  24;	Integrate_Phi_h_Bin_Values[11][2][1]  =   48;	Integrate_Phi_h_Bin_Values[11][2][2]  =   6048;
Integrate_Phi_h_Bin_Values[11][3][0]  =  24;	Integrate_Phi_h_Bin_Values[11][3][1]  =   72;	Integrate_Phi_h_Bin_Values[11][3][2]  =   6072;
Integrate_Phi_h_Bin_Values[11][4][0]  =  24;	Integrate_Phi_h_Bin_Values[11][4][1]  =   96;	Integrate_Phi_h_Bin_Values[11][4][2]  =   6096;
Integrate_Phi_h_Bin_Values[11][5][0]  =  24;	Integrate_Phi_h_Bin_Values[11][5][1]  =  120;	Integrate_Phi_h_Bin_Values[11][5][2]  =   6120;
Integrate_Phi_h_Bin_Values[11][6][0]  =  24;	Integrate_Phi_h_Bin_Values[11][6][1]  =  144;	Integrate_Phi_h_Bin_Values[11][6][2]  =   6144;
Integrate_Phi_h_Bin_Values[11][7][0]  =  24;	Integrate_Phi_h_Bin_Values[11][7][1]  =  168;	Integrate_Phi_h_Bin_Values[11][7][2]  =   6168;
Integrate_Phi_h_Bin_Values[11][8][0]  =  24;	Integrate_Phi_h_Bin_Values[11][8][1]  =  192;	Integrate_Phi_h_Bin_Values[11][8][2]  =   6192;
Integrate_Phi_h_Bin_Values[11][9][0]  =  24;	Integrate_Phi_h_Bin_Values[11][9][1]  =  216;	Integrate_Phi_h_Bin_Values[11][9][2]  =   6216;
Integrate_Phi_h_Bin_Values[11][10][0] =  24;	Integrate_Phi_h_Bin_Values[11][10][1] =  240;	Integrate_Phi_h_Bin_Values[11][10][2] =   6240;
Integrate_Phi_h_Bin_Values[11][11][0] =  24;	Integrate_Phi_h_Bin_Values[11][11][1] =  264;	Integrate_Phi_h_Bin_Values[11][11][2] =   6264;
Integrate_Phi_h_Bin_Values[11][12][0] =  24;	Integrate_Phi_h_Bin_Values[11][12][1] =  288;	Integrate_Phi_h_Bin_Values[11][12][2] =   6288;
Integrate_Phi_h_Bin_Values[11][13][0] =  24;	Integrate_Phi_h_Bin_Values[11][13][1] =  312;	Integrate_Phi_h_Bin_Values[11][13][2] =   6312;
Integrate_Phi_h_Bin_Values[11][14][0] =  24;	Integrate_Phi_h_Bin_Values[11][14][1] =  336;	Integrate_Phi_h_Bin_Values[11][14][2] =   6336;
Integrate_Phi_h_Bin_Values[11][15][0] =  24;	Integrate_Phi_h_Bin_Values[11][15][1] =  360;	Integrate_Phi_h_Bin_Values[11][15][2] =   6360;
Integrate_Phi_h_Bin_Values[11][16][0] =  24;	Integrate_Phi_h_Bin_Values[11][16][1] =  384;	Integrate_Phi_h_Bin_Values[11][16][2] =   6384;
Integrate_Phi_h_Bin_Values[11][17][0] =  24;	Integrate_Phi_h_Bin_Values[11][17][1] =  408;	Integrate_Phi_h_Bin_Values[11][17][2] =   6408;
Integrate_Phi_h_Bin_Values[11][18][0] =  24;	Integrate_Phi_h_Bin_Values[11][18][1] =  432;	Integrate_Phi_h_Bin_Values[11][18][2] =   6432;
Integrate_Phi_h_Bin_Values[11][19][0] =  24;	Integrate_Phi_h_Bin_Values[11][19][1] =  456;	Integrate_Phi_h_Bin_Values[11][19][2] =   6456;
Integrate_Phi_h_Bin_Values[11][20][0] =  24;	Integrate_Phi_h_Bin_Values[11][20][1] =  480;	Integrate_Phi_h_Bin_Values[11][20][2] =   6480;
Integrate_Phi_h_Bin_Values[11][21][0] =  24;	Integrate_Phi_h_Bin_Values[11][21][1] =  504;	Integrate_Phi_h_Bin_Values[11][21][2] =   6504;
Integrate_Phi_h_Bin_Values[11][22][0] =  24;	Integrate_Phi_h_Bin_Values[11][22][1] =  528;	Integrate_Phi_h_Bin_Values[11][22][2] =   6528;
Integrate_Phi_h_Bin_Values[11][23][0] =  24;	Integrate_Phi_h_Bin_Values[11][23][1] =  552;	Integrate_Phi_h_Bin_Values[11][23][2] =   6552;
Integrate_Phi_h_Bin_Values[11][24][0] =  24;	Integrate_Phi_h_Bin_Values[11][24][1] =  576;	Integrate_Phi_h_Bin_Values[11][24][2] =   6576;
Integrate_Phi_h_Bin_Values[11][25][0] =  24;	Integrate_Phi_h_Bin_Values[11][25][1] =  600;	Integrate_Phi_h_Bin_Values[11][25][2] =   6600;
Integrate_Phi_h_Bin_Values[12][1][0]  =  24;	Integrate_Phi_h_Bin_Values[12][1][1]  =   24;	Integrate_Phi_h_Bin_Values[12][1][2]  =   6624;
Integrate_Phi_h_Bin_Values[12][2][0]  =  24;	Integrate_Phi_h_Bin_Values[12][2][1]  =   48;	Integrate_Phi_h_Bin_Values[12][2][2]  =   6648;
Integrate_Phi_h_Bin_Values[12][3][0]  =  24;	Integrate_Phi_h_Bin_Values[12][3][1]  =   72;	Integrate_Phi_h_Bin_Values[12][3][2]  =   6672;
Integrate_Phi_h_Bin_Values[12][4][0]  =  24;	Integrate_Phi_h_Bin_Values[12][4][1]  =   96;	Integrate_Phi_h_Bin_Values[12][4][2]  =   6696;
Integrate_Phi_h_Bin_Values[12][5][0]  =  24;	Integrate_Phi_h_Bin_Values[12][5][1]  =  120;	Integrate_Phi_h_Bin_Values[12][5][2]  =   6720;
Integrate_Phi_h_Bin_Values[12][6][0]  =  24;	Integrate_Phi_h_Bin_Values[12][6][1]  =  144;	Integrate_Phi_h_Bin_Values[12][6][2]  =   6744;
Integrate_Phi_h_Bin_Values[12][7][0]  =  24;	Integrate_Phi_h_Bin_Values[12][7][1]  =  168;	Integrate_Phi_h_Bin_Values[12][7][2]  =   6768;
Integrate_Phi_h_Bin_Values[12][8][0]  =  24;	Integrate_Phi_h_Bin_Values[12][8][1]  =  192;	Integrate_Phi_h_Bin_Values[12][8][2]  =   6792;
Integrate_Phi_h_Bin_Values[12][9][0]  =  24;	Integrate_Phi_h_Bin_Values[12][9][1]  =  216;	Integrate_Phi_h_Bin_Values[12][9][2]  =   6816;
Integrate_Phi_h_Bin_Values[12][10][0] =  24;	Integrate_Phi_h_Bin_Values[12][10][1] =  240;	Integrate_Phi_h_Bin_Values[12][10][2] =   6840;
Integrate_Phi_h_Bin_Values[12][11][0] =  24;	Integrate_Phi_h_Bin_Values[12][11][1] =  264;	Integrate_Phi_h_Bin_Values[12][11][2] =   6864;
Integrate_Phi_h_Bin_Values[12][12][0] =  24;	Integrate_Phi_h_Bin_Values[12][12][1] =  288;	Integrate_Phi_h_Bin_Values[12][12][2] =   6888;
Integrate_Phi_h_Bin_Values[12][13][0] =  24;	Integrate_Phi_h_Bin_Values[12][13][1] =  312;	Integrate_Phi_h_Bin_Values[12][13][2] =   6912;
Integrate_Phi_h_Bin_Values[12][14][0] =  24;	Integrate_Phi_h_Bin_Values[12][14][1] =  336;	Integrate_Phi_h_Bin_Values[12][14][2] =   6936;
Integrate_Phi_h_Bin_Values[12][15][0] =  24;	Integrate_Phi_h_Bin_Values[12][15][1] =  360;	Integrate_Phi_h_Bin_Values[12][15][2] =   6960;
Integrate_Phi_h_Bin_Values[12][16][0] =  24;	Integrate_Phi_h_Bin_Values[12][16][1] =  384;	Integrate_Phi_h_Bin_Values[12][16][2] =   6984;
Integrate_Phi_h_Bin_Values[12][17][0] =  24;	Integrate_Phi_h_Bin_Values[12][17][1] =  408;	Integrate_Phi_h_Bin_Values[12][17][2] =   7008;
Integrate_Phi_h_Bin_Values[12][18][0] =  24;	Integrate_Phi_h_Bin_Values[12][18][1] =  432;	Integrate_Phi_h_Bin_Values[12][18][2] =   7032;
Integrate_Phi_h_Bin_Values[12][19][0] =  24;	Integrate_Phi_h_Bin_Values[12][19][1] =  456;	Integrate_Phi_h_Bin_Values[12][19][2] =   7056;
Integrate_Phi_h_Bin_Values[12][20][0] =  24;	Integrate_Phi_h_Bin_Values[12][20][1] =  480;	Integrate_Phi_h_Bin_Values[12][20][2] =   7080;
Integrate_Phi_h_Bin_Values[12][21][0] =  24;	Integrate_Phi_h_Bin_Values[12][21][1] =  504;	Integrate_Phi_h_Bin_Values[12][21][2] =   7104;
Integrate_Phi_h_Bin_Values[12][22][0] =  24;	Integrate_Phi_h_Bin_Values[12][22][1] =  528;	Integrate_Phi_h_Bin_Values[12][22][2] =   7128;
Integrate_Phi_h_Bin_Values[12][23][0] =  24;	Integrate_Phi_h_Bin_Values[12][23][1] =  552;	Integrate_Phi_h_Bin_Values[12][23][2] =   7152;
Integrate_Phi_h_Bin_Values[12][24][0] =  24;	Integrate_Phi_h_Bin_Values[12][24][1] =  576;	Integrate_Phi_h_Bin_Values[12][24][2] =   7176;
Integrate_Phi_h_Bin_Values[12][25][0] =  24;	Integrate_Phi_h_Bin_Values[12][25][1] =  600;	Integrate_Phi_h_Bin_Values[12][25][2] =   7200;
Integrate_Phi_h_Bin_Values[13][1][0]  =  24;	Integrate_Phi_h_Bin_Values[13][1][1]  =   24;	Integrate_Phi_h_Bin_Values[13][1][2]  =   7224;
Integrate_Phi_h_Bin_Values[13][2][0]  =  24;	Integrate_Phi_h_Bin_Values[13][2][1]  =   48;	Integrate_Phi_h_Bin_Values[13][2][2]  =   7248;
Integrate_Phi_h_Bin_Values[13][3][0]  =  24;	Integrate_Phi_h_Bin_Values[13][3][1]  =   72;	Integrate_Phi_h_Bin_Values[13][3][2]  =   7272;
Integrate_Phi_h_Bin_Values[13][4][0]  =  24;	Integrate_Phi_h_Bin_Values[13][4][1]  =   96;	Integrate_Phi_h_Bin_Values[13][4][2]  =   7296;
Integrate_Phi_h_Bin_Values[13][5][0]  =  24;	Integrate_Phi_h_Bin_Values[13][5][1]  =  120;	Integrate_Phi_h_Bin_Values[13][5][2]  =   7320;
Integrate_Phi_h_Bin_Values[13][6][0]  =  24;	Integrate_Phi_h_Bin_Values[13][6][1]  =  144;	Integrate_Phi_h_Bin_Values[13][6][2]  =   7344;
Integrate_Phi_h_Bin_Values[13][7][0]  =  24;	Integrate_Phi_h_Bin_Values[13][7][1]  =  168;	Integrate_Phi_h_Bin_Values[13][7][2]  =   7368;
Integrate_Phi_h_Bin_Values[13][8][0]  =  24;	Integrate_Phi_h_Bin_Values[13][8][1]  =  192;	Integrate_Phi_h_Bin_Values[13][8][2]  =   7392;
Integrate_Phi_h_Bin_Values[13][9][0]  =  24;	Integrate_Phi_h_Bin_Values[13][9][1]  =  216;	Integrate_Phi_h_Bin_Values[13][9][2]  =   7416;
Integrate_Phi_h_Bin_Values[13][10][0] =  24;	Integrate_Phi_h_Bin_Values[13][10][1] =  240;	Integrate_Phi_h_Bin_Values[13][10][2] =   7440;
Integrate_Phi_h_Bin_Values[13][11][0] =  24;	Integrate_Phi_h_Bin_Values[13][11][1] =  264;	Integrate_Phi_h_Bin_Values[13][11][2] =   7464;
Integrate_Phi_h_Bin_Values[13][12][0] =  24;	Integrate_Phi_h_Bin_Values[13][12][1] =  288;	Integrate_Phi_h_Bin_Values[13][12][2] =   7488;
Integrate_Phi_h_Bin_Values[13][13][0] =  24;	Integrate_Phi_h_Bin_Values[13][13][1] =  312;	Integrate_Phi_h_Bin_Values[13][13][2] =   7512;
Integrate_Phi_h_Bin_Values[13][14][0] =  24;	Integrate_Phi_h_Bin_Values[13][14][1] =  336;	Integrate_Phi_h_Bin_Values[13][14][2] =   7536;
Integrate_Phi_h_Bin_Values[13][15][0] =  24;	Integrate_Phi_h_Bin_Values[13][15][1] =  360;	Integrate_Phi_h_Bin_Values[13][15][2] =   7560;
Integrate_Phi_h_Bin_Values[13][16][0] =  24;	Integrate_Phi_h_Bin_Values[13][16][1] =  384;	Integrate_Phi_h_Bin_Values[13][16][2] =   7584;
Integrate_Phi_h_Bin_Values[13][17][0] =  24;	Integrate_Phi_h_Bin_Values[13][17][1] =  408;	Integrate_Phi_h_Bin_Values[13][17][2] =   7608;
Integrate_Phi_h_Bin_Values[13][18][0] =  24;	Integrate_Phi_h_Bin_Values[13][18][1] =  432;	Integrate_Phi_h_Bin_Values[13][18][2] =   7632;
Integrate_Phi_h_Bin_Values[13][19][0] =  24;	Integrate_Phi_h_Bin_Values[13][19][1] =  456;	Integrate_Phi_h_Bin_Values[13][19][2] =   7656;
Integrate_Phi_h_Bin_Values[13][20][0] =  24;	Integrate_Phi_h_Bin_Values[13][20][1] =  480;	Integrate_Phi_h_Bin_Values[13][20][2] =   7680;
Integrate_Phi_h_Bin_Values[13][21][0] =  24;	Integrate_Phi_h_Bin_Values[13][21][1] =  504;	Integrate_Phi_h_Bin_Values[13][21][2] =   7704;
Integrate_Phi_h_Bin_Values[13][22][0] =  24;	Integrate_Phi_h_Bin_Values[13][22][1] =  528;	Integrate_Phi_h_Bin_Values[13][22][2] =   7728;
Integrate_Phi_h_Bin_Values[13][23][0] =  24;	Integrate_Phi_h_Bin_Values[13][23][1] =  552;	Integrate_Phi_h_Bin_Values[13][23][2] =   7752;
Integrate_Phi_h_Bin_Values[13][24][0] =  24;	Integrate_Phi_h_Bin_Values[13][24][1] =  576;	Integrate_Phi_h_Bin_Values[13][24][2] =   7776;
Integrate_Phi_h_Bin_Values[13][25][0] =  24;	Integrate_Phi_h_Bin_Values[13][25][1] =  600;	Integrate_Phi_h_Bin_Values[13][25][2] =   7800;
Integrate_Phi_h_Bin_Values[14][1][0]  =  24;	Integrate_Phi_h_Bin_Values[14][1][1]  =   24;	Integrate_Phi_h_Bin_Values[14][1][2]  =   7824;
Integrate_Phi_h_Bin_Values[14][2][0]  =  24;	Integrate_Phi_h_Bin_Values[14][2][1]  =   48;	Integrate_Phi_h_Bin_Values[14][2][2]  =   7848;
Integrate_Phi_h_Bin_Values[14][3][0]  =  24;	Integrate_Phi_h_Bin_Values[14][3][1]  =   72;	Integrate_Phi_h_Bin_Values[14][3][2]  =   7872;
Integrate_Phi_h_Bin_Values[14][4][0]  =  24;	Integrate_Phi_h_Bin_Values[14][4][1]  =   96;	Integrate_Phi_h_Bin_Values[14][4][2]  =   7896;
Integrate_Phi_h_Bin_Values[14][5][0]  =  24;	Integrate_Phi_h_Bin_Values[14][5][1]  =  120;	Integrate_Phi_h_Bin_Values[14][5][2]  =   7920;
Integrate_Phi_h_Bin_Values[14][6][0]  =  24;	Integrate_Phi_h_Bin_Values[14][6][1]  =  144;	Integrate_Phi_h_Bin_Values[14][6][2]  =   7944;
Integrate_Phi_h_Bin_Values[14][7][0]  =  24;	Integrate_Phi_h_Bin_Values[14][7][1]  =  168;	Integrate_Phi_h_Bin_Values[14][7][2]  =   7968;
Integrate_Phi_h_Bin_Values[14][8][0]  =  24;	Integrate_Phi_h_Bin_Values[14][8][1]  =  192;	Integrate_Phi_h_Bin_Values[14][8][2]  =   7992;
Integrate_Phi_h_Bin_Values[14][9][0]  =  24;	Integrate_Phi_h_Bin_Values[14][9][1]  =  216;	Integrate_Phi_h_Bin_Values[14][9][2]  =   8016;
Integrate_Phi_h_Bin_Values[14][10][0] =  24;	Integrate_Phi_h_Bin_Values[14][10][1] =  240;	Integrate_Phi_h_Bin_Values[14][10][2] =   8040;
Integrate_Phi_h_Bin_Values[14][11][0] =  24;	Integrate_Phi_h_Bin_Values[14][11][1] =  264;	Integrate_Phi_h_Bin_Values[14][11][2] =   8064;
Integrate_Phi_h_Bin_Values[14][12][0] =  24;	Integrate_Phi_h_Bin_Values[14][12][1] =  288;	Integrate_Phi_h_Bin_Values[14][12][2] =   8088;
Integrate_Phi_h_Bin_Values[14][13][0] =  24;	Integrate_Phi_h_Bin_Values[14][13][1] =  312;	Integrate_Phi_h_Bin_Values[14][13][2] =   8112;
Integrate_Phi_h_Bin_Values[14][14][0] =  24;	Integrate_Phi_h_Bin_Values[14][14][1] =  336;	Integrate_Phi_h_Bin_Values[14][14][2] =   8136;
Integrate_Phi_h_Bin_Values[14][15][0] =  24;	Integrate_Phi_h_Bin_Values[14][15][1] =  360;	Integrate_Phi_h_Bin_Values[14][15][2] =   8160;
Integrate_Phi_h_Bin_Values[14][16][0] =  24;	Integrate_Phi_h_Bin_Values[14][16][1] =  384;	Integrate_Phi_h_Bin_Values[14][16][2] =   8184;
Integrate_Phi_h_Bin_Values[14][17][0] =  24;	Integrate_Phi_h_Bin_Values[14][17][1] =  408;	Integrate_Phi_h_Bin_Values[14][17][2] =   8208;
Integrate_Phi_h_Bin_Values[14][18][0] =  24;	Integrate_Phi_h_Bin_Values[14][18][1] =  432;	Integrate_Phi_h_Bin_Values[14][18][2] =   8232;
Integrate_Phi_h_Bin_Values[14][19][0] =  24;	Integrate_Phi_h_Bin_Values[14][19][1] =  456;	Integrate_Phi_h_Bin_Values[14][19][2] =   8256;
Integrate_Phi_h_Bin_Values[14][20][0] =  24;	Integrate_Phi_h_Bin_Values[14][20][1] =  480;	Integrate_Phi_h_Bin_Values[14][20][2] =   8280;
Integrate_Phi_h_Bin_Values[14][21][0] =  24;	Integrate_Phi_h_Bin_Values[14][21][1] =  504;	Integrate_Phi_h_Bin_Values[14][21][2] =   8304;
Integrate_Phi_h_Bin_Values[14][22][0] =  24;	Integrate_Phi_h_Bin_Values[14][22][1] =  528;	Integrate_Phi_h_Bin_Values[14][22][2] =   8328;
Integrate_Phi_h_Bin_Values[14][23][0] =  24;	Integrate_Phi_h_Bin_Values[14][23][1] =  552;	Integrate_Phi_h_Bin_Values[14][23][2] =   8352;
Integrate_Phi_h_Bin_Values[14][24][0] =  24;	Integrate_Phi_h_Bin_Values[14][24][1] =  576;	Integrate_Phi_h_Bin_Values[14][24][2] =   8376;
Integrate_Phi_h_Bin_Values[14][25][0] =  24;	Integrate_Phi_h_Bin_Values[14][25][1] =  600;	Integrate_Phi_h_Bin_Values[14][25][2] =   8400;
Integrate_Phi_h_Bin_Values[15][1][0]  =  24;	Integrate_Phi_h_Bin_Values[15][1][1]  =   24;	Integrate_Phi_h_Bin_Values[15][1][2]  =   8424;
Integrate_Phi_h_Bin_Values[15][2][0]  =  24;	Integrate_Phi_h_Bin_Values[15][2][1]  =   48;	Integrate_Phi_h_Bin_Values[15][2][2]  =   8448;
Integrate_Phi_h_Bin_Values[15][3][0]  =  24;	Integrate_Phi_h_Bin_Values[15][3][1]  =   72;	Integrate_Phi_h_Bin_Values[15][3][2]  =   8472;
Integrate_Phi_h_Bin_Values[15][4][0]  =  24;	Integrate_Phi_h_Bin_Values[15][4][1]  =   96;	Integrate_Phi_h_Bin_Values[15][4][2]  =   8496;
Integrate_Phi_h_Bin_Values[15][5][0]  =  24;	Integrate_Phi_h_Bin_Values[15][5][1]  =  120;	Integrate_Phi_h_Bin_Values[15][5][2]  =   8520;
Integrate_Phi_h_Bin_Values[15][6][0]  =  24;	Integrate_Phi_h_Bin_Values[15][6][1]  =  144;	Integrate_Phi_h_Bin_Values[15][6][2]  =   8544;
Integrate_Phi_h_Bin_Values[15][7][0]  =  24;	Integrate_Phi_h_Bin_Values[15][7][1]  =  168;	Integrate_Phi_h_Bin_Values[15][7][2]  =   8568;
Integrate_Phi_h_Bin_Values[15][8][0]  =  24;	Integrate_Phi_h_Bin_Values[15][8][1]  =  192;	Integrate_Phi_h_Bin_Values[15][8][2]  =   8592;
Integrate_Phi_h_Bin_Values[15][9][0]  =  24;	Integrate_Phi_h_Bin_Values[15][9][1]  =  216;	Integrate_Phi_h_Bin_Values[15][9][2]  =   8616;
Integrate_Phi_h_Bin_Values[15][10][0] =  24;	Integrate_Phi_h_Bin_Values[15][10][1] =  240;	Integrate_Phi_h_Bin_Values[15][10][2] =   8640;
Integrate_Phi_h_Bin_Values[15][11][0] =  24;	Integrate_Phi_h_Bin_Values[15][11][1] =  264;	Integrate_Phi_h_Bin_Values[15][11][2] =   8664;
Integrate_Phi_h_Bin_Values[15][12][0] =  24;	Integrate_Phi_h_Bin_Values[15][12][1] =  288;	Integrate_Phi_h_Bin_Values[15][12][2] =   8688;
Integrate_Phi_h_Bin_Values[15][13][0] =  24;	Integrate_Phi_h_Bin_Values[15][13][1] =  312;	Integrate_Phi_h_Bin_Values[15][13][2] =   8712;
Integrate_Phi_h_Bin_Values[15][14][0] =  24;	Integrate_Phi_h_Bin_Values[15][14][1] =  336;	Integrate_Phi_h_Bin_Values[15][14][2] =   8736;
Integrate_Phi_h_Bin_Values[15][15][0] =  24;	Integrate_Phi_h_Bin_Values[15][15][1] =  360;	Integrate_Phi_h_Bin_Values[15][15][2] =   8760;
Integrate_Phi_h_Bin_Values[15][16][0] =  24;	Integrate_Phi_h_Bin_Values[15][16][1] =  384;	Integrate_Phi_h_Bin_Values[15][16][2] =   8784;
Integrate_Phi_h_Bin_Values[15][17][0] =  24;	Integrate_Phi_h_Bin_Values[15][17][1] =  408;	Integrate_Phi_h_Bin_Values[15][17][2] =   8808;
Integrate_Phi_h_Bin_Values[15][18][0] =  24;	Integrate_Phi_h_Bin_Values[15][18][1] =  432;	Integrate_Phi_h_Bin_Values[15][18][2] =   8832;
Integrate_Phi_h_Bin_Values[15][19][0] =  24;	Integrate_Phi_h_Bin_Values[15][19][1] =  456;	Integrate_Phi_h_Bin_Values[15][19][2] =   8856;
Integrate_Phi_h_Bin_Values[15][20][0] =  24;	Integrate_Phi_h_Bin_Values[15][20][1] =  480;	Integrate_Phi_h_Bin_Values[15][20][2] =   8880;
Integrate_Phi_h_Bin_Values[15][21][0] =  24;	Integrate_Phi_h_Bin_Values[15][21][1] =  504;	Integrate_Phi_h_Bin_Values[15][21][2] =   8904;
Integrate_Phi_h_Bin_Values[15][22][0] =  24;	Integrate_Phi_h_Bin_Values[15][22][1] =  528;	Integrate_Phi_h_Bin_Values[15][22][2] =   8928;
Integrate_Phi_h_Bin_Values[15][23][0] =  24;	Integrate_Phi_h_Bin_Values[15][23][1] =  552;	Integrate_Phi_h_Bin_Values[15][23][2] =   8952;
Integrate_Phi_h_Bin_Values[15][24][0] =  24;	Integrate_Phi_h_Bin_Values[15][24][1] =  576;	Integrate_Phi_h_Bin_Values[15][24][2] =   8976;
Integrate_Phi_h_Bin_Values[15][25][0] =  24;	Integrate_Phi_h_Bin_Values[15][25][1] =  600;	Integrate_Phi_h_Bin_Values[15][25][2] =   9000;
Integrate_Phi_h_Bin_Values[16][1][0]  =  24;	Integrate_Phi_h_Bin_Values[16][1][1]  =   24;	Integrate_Phi_h_Bin_Values[16][1][2]  =   9024;
Integrate_Phi_h_Bin_Values[16][2][0]  =  24;	Integrate_Phi_h_Bin_Values[16][2][1]  =   48;	Integrate_Phi_h_Bin_Values[16][2][2]  =   9048;
Integrate_Phi_h_Bin_Values[16][3][0]  =  24;	Integrate_Phi_h_Bin_Values[16][3][1]  =   72;	Integrate_Phi_h_Bin_Values[16][3][2]  =   9072;
Integrate_Phi_h_Bin_Values[16][4][0]  =  24;	Integrate_Phi_h_Bin_Values[16][4][1]  =   96;	Integrate_Phi_h_Bin_Values[16][4][2]  =   9096;
Integrate_Phi_h_Bin_Values[16][5][0]  =  24;	Integrate_Phi_h_Bin_Values[16][5][1]  =  120;	Integrate_Phi_h_Bin_Values[16][5][2]  =   9120;
Integrate_Phi_h_Bin_Values[16][6][0]  =  24;	Integrate_Phi_h_Bin_Values[16][6][1]  =  144;	Integrate_Phi_h_Bin_Values[16][6][2]  =   9144;
Integrate_Phi_h_Bin_Values[16][7][0]  =  24;	Integrate_Phi_h_Bin_Values[16][7][1]  =  168;	Integrate_Phi_h_Bin_Values[16][7][2]  =   9168;
Integrate_Phi_h_Bin_Values[16][8][0]  =  24;	Integrate_Phi_h_Bin_Values[16][8][1]  =  192;	Integrate_Phi_h_Bin_Values[16][8][2]  =   9192;
Integrate_Phi_h_Bin_Values[16][9][0]  =  24;	Integrate_Phi_h_Bin_Values[16][9][1]  =  216;	Integrate_Phi_h_Bin_Values[16][9][2]  =   9216;
Integrate_Phi_h_Bin_Values[16][10][0] =  24;	Integrate_Phi_h_Bin_Values[16][10][1] =  240;	Integrate_Phi_h_Bin_Values[16][10][2] =   9240;
Integrate_Phi_h_Bin_Values[16][11][0] =  24;	Integrate_Phi_h_Bin_Values[16][11][1] =  264;	Integrate_Phi_h_Bin_Values[16][11][2] =   9264;
Integrate_Phi_h_Bin_Values[16][12][0] =  24;	Integrate_Phi_h_Bin_Values[16][12][1] =  288;	Integrate_Phi_h_Bin_Values[16][12][2] =   9288;
Integrate_Phi_h_Bin_Values[16][13][0] =  24;	Integrate_Phi_h_Bin_Values[16][13][1] =  312;	Integrate_Phi_h_Bin_Values[16][13][2] =   9312;
Integrate_Phi_h_Bin_Values[16][14][0] =  24;	Integrate_Phi_h_Bin_Values[16][14][1] =  336;	Integrate_Phi_h_Bin_Values[16][14][2] =   9336;
Integrate_Phi_h_Bin_Values[16][15][0] =  24;	Integrate_Phi_h_Bin_Values[16][15][1] =  360;	Integrate_Phi_h_Bin_Values[16][15][2] =   9360;
Integrate_Phi_h_Bin_Values[16][16][0] =  24;	Integrate_Phi_h_Bin_Values[16][16][1] =  384;	Integrate_Phi_h_Bin_Values[16][16][2] =   9384;
Integrate_Phi_h_Bin_Values[16][17][0] =  24;	Integrate_Phi_h_Bin_Values[16][17][1] =  408;	Integrate_Phi_h_Bin_Values[16][17][2] =   9408;
Integrate_Phi_h_Bin_Values[16][18][0] =  24;	Integrate_Phi_h_Bin_Values[16][18][1] =  432;	Integrate_Phi_h_Bin_Values[16][18][2] =   9432;
Integrate_Phi_h_Bin_Values[16][19][0] =  24;	Integrate_Phi_h_Bin_Values[16][19][1] =  456;	Integrate_Phi_h_Bin_Values[16][19][2] =   9456;
Integrate_Phi_h_Bin_Values[16][20][0] =  24;	Integrate_Phi_h_Bin_Values[16][20][1] =  480;	Integrate_Phi_h_Bin_Values[16][20][2] =   9480;
Integrate_Phi_h_Bin_Values[16][21][0] =  24;	Integrate_Phi_h_Bin_Values[16][21][1] =  504;	Integrate_Phi_h_Bin_Values[16][21][2] =   9504;
Integrate_Phi_h_Bin_Values[16][22][0] =  24;	Integrate_Phi_h_Bin_Values[16][22][1] =  528;	Integrate_Phi_h_Bin_Values[16][22][2] =   9528;
Integrate_Phi_h_Bin_Values[16][23][0] =  24;	Integrate_Phi_h_Bin_Values[16][23][1] =  552;	Integrate_Phi_h_Bin_Values[16][23][2] =   9552;
Integrate_Phi_h_Bin_Values[16][24][0] =  24;	Integrate_Phi_h_Bin_Values[16][24][1] =  576;	Integrate_Phi_h_Bin_Values[16][24][2] =   9576;
Integrate_Phi_h_Bin_Values[16][25][0] =  24;	Integrate_Phi_h_Bin_Values[16][25][1] =  600;	Integrate_Phi_h_Bin_Values[16][25][2] =   9600;
Integrate_Phi_h_Bin_Values[17][1][0]  =  24;	Integrate_Phi_h_Bin_Values[17][1][1]  =   24;	Integrate_Phi_h_Bin_Values[17][1][2]  =   9624;
Integrate_Phi_h_Bin_Values[17][2][0]  =  24;	Integrate_Phi_h_Bin_Values[17][2][1]  =   48;	Integrate_Phi_h_Bin_Values[17][2][2]  =   9648;
Integrate_Phi_h_Bin_Values[17][3][0]  =  24;	Integrate_Phi_h_Bin_Values[17][3][1]  =   72;	Integrate_Phi_h_Bin_Values[17][3][2]  =   9672;
Integrate_Phi_h_Bin_Values[17][4][0]  =  24;	Integrate_Phi_h_Bin_Values[17][4][1]  =   96;	Integrate_Phi_h_Bin_Values[17][4][2]  =   9696;
Integrate_Phi_h_Bin_Values[17][5][0]  =  24;	Integrate_Phi_h_Bin_Values[17][5][1]  =  120;	Integrate_Phi_h_Bin_Values[17][5][2]  =   9720;
Integrate_Phi_h_Bin_Values[17][6][0]  =  24;	Integrate_Phi_h_Bin_Values[17][6][1]  =  144;	Integrate_Phi_h_Bin_Values[17][6][2]  =   9744;
Integrate_Phi_h_Bin_Values[17][7][0]  =  24;	Integrate_Phi_h_Bin_Values[17][7][1]  =  168;	Integrate_Phi_h_Bin_Values[17][7][2]  =   9768;
Integrate_Phi_h_Bin_Values[17][8][0]  =  24;	Integrate_Phi_h_Bin_Values[17][8][1]  =  192;	Integrate_Phi_h_Bin_Values[17][8][2]  =   9792;
Integrate_Phi_h_Bin_Values[17][9][0]  =  24;	Integrate_Phi_h_Bin_Values[17][9][1]  =  216;	Integrate_Phi_h_Bin_Values[17][9][2]  =   9816;
Integrate_Phi_h_Bin_Values[17][10][0] =  24;	Integrate_Phi_h_Bin_Values[17][10][1] =  240;	Integrate_Phi_h_Bin_Values[17][10][2] =   9840;
Integrate_Phi_h_Bin_Values[17][11][0] =  24;	Integrate_Phi_h_Bin_Values[17][11][1] =  264;	Integrate_Phi_h_Bin_Values[17][11][2] =   9864;
Integrate_Phi_h_Bin_Values[17][12][0] =  24;	Integrate_Phi_h_Bin_Values[17][12][1] =  288;	Integrate_Phi_h_Bin_Values[17][12][2] =   9888;
Integrate_Phi_h_Bin_Values[17][13][0] =  24;	Integrate_Phi_h_Bin_Values[17][13][1] =  312;	Integrate_Phi_h_Bin_Values[17][13][2] =   9912;
Integrate_Phi_h_Bin_Values[17][14][0] =  24;	Integrate_Phi_h_Bin_Values[17][14][1] =  336;	Integrate_Phi_h_Bin_Values[17][14][2] =   9936;
Integrate_Phi_h_Bin_Values[17][15][0] =  24;	Integrate_Phi_h_Bin_Values[17][15][1] =  360;	Integrate_Phi_h_Bin_Values[17][15][2] =   9960;
Integrate_Phi_h_Bin_Values[17][16][0] =  24;	Integrate_Phi_h_Bin_Values[17][16][1] =  384;	Integrate_Phi_h_Bin_Values[17][16][2] =   9984;
Integrate_Phi_h_Bin_Values[17][17][0] =  24;	Integrate_Phi_h_Bin_Values[17][17][1] =  408;	Integrate_Phi_h_Bin_Values[17][17][2] =  10008;
Integrate_Phi_h_Bin_Values[17][18][0] =  24;	Integrate_Phi_h_Bin_Values[17][18][1] =  432;	Integrate_Phi_h_Bin_Values[17][18][2] =  10032;
Integrate_Phi_h_Bin_Values[17][19][0] =  24;	Integrate_Phi_h_Bin_Values[17][19][1] =  456;	Integrate_Phi_h_Bin_Values[17][19][2] =  10056;
Integrate_Phi_h_Bin_Values[17][20][0] =  24;	Integrate_Phi_h_Bin_Values[17][20][1] =  480;	Integrate_Phi_h_Bin_Values[17][20][2] =  10080;
Integrate_Phi_h_Bin_Values[17][21][0] =  24;	Integrate_Phi_h_Bin_Values[17][21][1] =  504;	Integrate_Phi_h_Bin_Values[17][21][2] =  10104;
Integrate_Phi_h_Bin_Values[17][22][0] =  24;	Integrate_Phi_h_Bin_Values[17][22][1] =  528;	Integrate_Phi_h_Bin_Values[17][22][2] =  10128;
Integrate_Phi_h_Bin_Values[17][23][0] =  24;	Integrate_Phi_h_Bin_Values[17][23][1] =  552;	Integrate_Phi_h_Bin_Values[17][23][2] =  10152;
Integrate_Phi_h_Bin_Values[17][24][0] =  24;	Integrate_Phi_h_Bin_Values[17][24][1] =  576;	Integrate_Phi_h_Bin_Values[17][24][2] =  10176;
Integrate_Phi_h_Bin_Values[17][25][0] =  24;	Integrate_Phi_h_Bin_Values[17][25][1] =  600;	Integrate_Phi_h_Bin_Values[17][25][2] =  10200;'''








###########################################################################################################################################################################
###########################################################################################################################################################################
###########################################################################################################################################################################
###########################################################################################################################################################################
###########################################################################################################################################################################










# Correction_Code_Full_In = """
# auto dppC = [&](float Px, float Py, float Pz, int sec, int ivec, int corON){
#     // corON == 0 --> DOES NOT apply the momentum corrections (i.e., turns the corrections 'off')
#     // corON == 1 --> Applies the (Pass 1) momentum corrections for the experimental (real) data
#     // corON == 2 --> Applies the (Pass 1) momentum corrections for the Monte Carlo (simulated) data
#     // corON == 3 --> Applies the (Pass 2) momentum corrections for the experimental (real) data
#     // corON == 4 --> Applies the (Pass 2) momentum corrections for the Monte Carlo (simulated) data
#     if(corON == 0){ // Momentum Corrections are OFF
#         double dp = 0;
#         return dp;
#     }
#     else{ // corON != 0 --> Applies the momentum corrections (i.e., turns the corrections 'on')
#         // ivec = 0 --> Electron Corrections
#         // ivec = 1 --> π+ Corrections
#         // ivec = 2 --> π- Corrections
#         // ivec = 3 --> Proton Corrections
#         // Momentum Magnitude
#         double pp = sqrt(Px*Px + Py*Py + Pz*Pz);
#         // Initializing the correction factor
#         double dp = 0;
#         // Defining Phi Angle
#         double Phi = (180/3.1415926)*atan2(Py, Px);
#         // (Initial) Shift of the Phi Angle (done to realign sectors whose data is separated when plotted from ±180˚)
#         if(((sec == 4 || sec == 3) && Phi < 0) || (sec > 4 && Phi < 90)){
#             Phi += 360;
#         }
#         // Getting Local Phi Angle
#         double PhiLocal = Phi - (sec - 1)*60;
#         // Applying Shift Functions to Phi Angles (local shifted phi = phi)
#         double phi = PhiLocal;
#         // For Electron Shift
#         if(ivec == 0){
#             phi = PhiLocal - 30/pp;
#         }
#         // For π+ Pion/Proton Shift
#         if(ivec == 1 || ivec == 3){
#             phi = PhiLocal + (32/(pp-0.05));
#         }
#         // For π- Pion Shift
#         if(ivec == 2){
#             phi = PhiLocal - (32/(pp-0.05));
#         }
#         if(corON == 2){ // Pass 1 Monte Carlo Simulated Corrections
#             // Not Sector or Angle dependent (as of 3-21-2023)
#             // Both particles were corrected at the same time using Extra_Name = "Multi_Dimension_Unfold_V1_"
#             // Used ∆P = GEN - REC so the other particle does not affect how much the correction is needed
#             if(ivec == 0){ // Electron Corrections
#                 // // For MC REC (Unsmeared) ∆P(Electron) Vs Momentum Correction Equation:
#                 // dp = (-8.2310e-04)*pp*pp + (9.0877e-03)*pp + (-1.5853e-02);
#                 // From Normal ∆P corrections:
#                 // For MC REC (Unsmeared) ∆P(Electron) Vs Momentum Correction Equation:
#                 dp = (-6.9141e-04)*pp*pp + (5.5852e-03)*pp + (-5.2144e-03);
#                 // Corrected after the pion
#             }
#             if(ivec == 1){ // Pi+ Pion Corrections
#                 // For MC REC (Unsmeared) ∆P(Pi+ Pion) Vs Momentum Correction Equation:
#                 dp = (-7.3067e-05)*pp*pp + (-8.1215e-06)*pp + (4.2144e-03);
#                 // From Normal ∆P corrections:
#                 // For MC REC (Unsmeared) ∆P(Pi+ Pion) Vs Momentum Correction Equation:
#                 dp = (-1.8752e-03)*pp*pp + (1.0679e-02)*pp +  (2.5653e-03);
#                 // Corrected before the electron
#                 // Cannot use iterative corrections as of 7-8-2023 due to the corrections being applied automatically so that dp is no longer a function of the same pp
#                 // dp = dp + (-1.8949e-03)*pp*pp + (9.3060e-03)*pp + (-9.7925e-03);
#             }
#             return dp/pp;
#         }
#         else{
#             if(corON == 1){ // Pass 1 Data Momentum Corrections
#                 //////////////////////////////////////////////////////////////////////////////////
#                 //==============================================================================//
#                 //==========//==========//     Electron Corrections     //==========//==========//
#                 //==============================================================================//
#                 //////////////////////////////////////////////////////////////////////////////////
#                 if(ivec == 0){
#                     if(sec == 1){
#                         dp = ((-4.3303e-06)*phi*phi +  (1.1006e-04)*phi + (-5.7235e-04))*pp*pp +  ((3.2555e-05)*phi*phi +  (-0.0014559)*phi +   (0.0014878))*pp + ((-1.9577e-05)*phi*phi +   (0.0017996)*phi + (0.025963));
#                     }
#                     if(sec == 2){
#                         dp = ((-9.8045e-07)*phi*phi +  (6.7395e-05)*phi + (-4.6757e-05))*pp*pp + ((-1.4958e-05)*phi*phi +  (-0.0011191)*phi +  (-0.0025143))*pp +  ((1.2699e-04)*phi*phi +   (0.0033121)*phi + (0.020819));
#                     }
#                     if(sec == 3){
#                         dp = ((-5.9459e-07)*phi*phi + (-2.8289e-05)*phi + (-4.3541e-04))*pp*pp + ((-1.5025e-05)*phi*phi +  (5.7730e-04)*phi +  (-0.0077582))*pp +  ((7.3348e-05)*phi*phi +   (-0.001102)*phi + (0.057052));
#                     }
#                     if(sec == 4){
#                         dp = ((-2.2714e-06)*phi*phi + (-3.0360e-05)*phi + (-8.9322e-04))*pp*pp +  ((2.9737e-05)*phi*phi +  (5.1142e-04)*phi +   (0.0045641))*pp + ((-1.0582e-04)*phi*phi + (-5.6852e-04)*phi + (0.027506));
#                     }
#                     if(sec == 5){
#                         dp = ((-1.1490e-06)*phi*phi + (-6.2147e-06)*phi + (-4.7235e-04))*pp*pp +  ((3.7039e-06)*phi*phi + (-1.5943e-04)*phi + (-8.5238e-04))*pp +  ((4.4069e-05)*phi*phi +   (0.0014152)*phi + (0.031933));
#                     }
#                     if(sec == 6){
#                         dp =  ((1.1076e-06)*phi*phi +  (4.0156e-05)*phi + (-1.6341e-04))*pp*pp + ((-2.8613e-05)*phi*phi + (-5.1861e-04)*phi +  (-0.0056437))*pp +  ((1.2419e-04)*phi*phi +  (4.9084e-04)*phi + (0.049976));
#                     }
#                 }
#                 //////////////////////////////////////////////////////////////////////////////////
#                 //==============================================================================//
#                 //==========//==========//  Electron Corrections (End)  //==========//==========//
#                 //==============================================================================//
#                 //////////////////////////////////////////////////////////////////////////////////
#                 /////////////////////////////////////////////////////////////////////////////////
#                 //=============================================================================//
#                 //==========//==========//     π+ Pion Corrections     //==========//==========//
#                 //=============================================================================//
#                 /////////////////////////////////////////////////////////////////////////////////
#                 if(ivec == 1){
#                     if(sec == 1){
#                         dp =      ((-5.4904e-07)*phi*phi + (-1.4436e-05)*phi +  (3.1534e-04))*pp*pp +  ((3.8231e-06)*phi*phi +  (3.6582e-04)*phi +  (-0.0046759))*pp + ((-5.4913e-06)*phi*phi + (-4.0157e-04)*phi + (0.010767));
#                         dp = dp +  ((6.1103e-07)*phi*phi +  (5.5291e-06)*phi + (-1.9120e-04))*pp*pp + ((-3.2300e-06)*phi*phi +  (1.5377e-05)*phi +  (7.5279e-04))*pp +  ((2.1434e-06)*phi*phi + (-6.9572e-06)*phi + (-7.9333e-05));
#                         dp = dp + ((-1.3049e-06)*phi*phi +  (1.1295e-05)*phi +  (4.5797e-04))*pp*pp +  ((9.3122e-06)*phi*phi + (-5.1074e-05)*phi +  (-0.0030757))*pp + ((-1.3102e-05)*phi*phi +  (2.2153e-05)*phi + (0.0040938));
#                     }
#                     if(sec == 2){
#                         dp =      ((-1.0087e-06)*phi*phi +  (2.1319e-05)*phi +  (7.8641e-04))*pp*pp +  ((6.7485e-06)*phi*phi +  (7.3716e-05)*phi +  (-0.0094591))*pp + ((-1.1820e-05)*phi*phi + (-3.8103e-04)*phi + (0.018936));
#                         dp = dp +  ((8.8155e-07)*phi*phi + (-2.8257e-06)*phi + (-2.6729e-04))*pp*pp + ((-5.4499e-06)*phi*phi +  (3.8397e-05)*phi +   (0.0015914))*pp +  ((6.8926e-06)*phi*phi + (-5.9386e-05)*phi + (-0.0021749));
#                         dp = dp + ((-2.0147e-07)*phi*phi +  (1.1061e-05)*phi +  (3.8827e-04))*pp*pp +  ((4.9294e-07)*phi*phi + (-6.0257e-05)*phi +  (-0.0022087))*pp +  ((9.8548e-07)*phi*phi +  (5.9047e-05)*phi + (0.0022905));
#                     }
#                     if(sec == 3){
#                         dp =       ((8.6722e-08)*phi*phi + (-1.7975e-05)*phi +  (4.8118e-05))*pp*pp +  ((2.6273e-06)*phi*phi +  (3.1453e-05)*phi +  (-0.0015943))*pp + ((-6.4463e-06)*phi*phi + (-5.8990e-05)*phi + (0.0041703));
#                         dp = dp +  ((9.6317e-07)*phi*phi + (-1.7659e-06)*phi + (-8.8318e-05))*pp*pp + ((-5.1346e-06)*phi*phi +  (8.3318e-06)*phi +  (3.7723e-04))*pp +  ((3.9548e-06)*phi*phi + (-6.9614e-05)*phi + (2.1393e-04));
#                         dp = dp +  ((5.6438e-07)*phi*phi +  (8.1678e-06)*phi + (-9.4406e-05))*pp*pp + ((-3.9074e-06)*phi*phi + (-6.5174e-05)*phi +  (5.4218e-04))*pp +  ((6.3198e-06)*phi*phi +  (1.0611e-04)*phi + (-4.5749e-04));
#                     }
#                     if(sec == 4){
#                         dp =       ((4.3406e-07)*phi*phi + (-4.9036e-06)*phi +  (2.3064e-04))*pp*pp +  ((1.3624e-06)*phi*phi +  (3.2907e-05)*phi +  (-0.0034872))*pp + ((-5.1017e-06)*phi*phi +  (2.4593e-05)*phi + (0.0092479));
#                         dp = dp +  ((6.0218e-07)*phi*phi + (-1.4383e-05)*phi + (-3.1999e-05))*pp*pp + ((-1.1243e-06)*phi*phi +  (9.3884e-05)*phi + (-4.1985e-04))*pp + ((-1.8808e-06)*phi*phi + (-1.2222e-04)*phi + (0.0014037));
#                         dp = dp + ((-2.5490e-07)*phi*phi + (-8.5120e-07)*phi +  (7.9109e-05))*pp*pp +  ((2.5879e-06)*phi*phi +  (8.6108e-06)*phi + (-5.1533e-04))*pp + ((-4.4521e-06)*phi*phi + (-1.7012e-05)*phi + (7.4848e-04));
#                     }
#                     if(sec == 5){
#                         dp =       ((2.4292e-07)*phi*phi +  (8.8741e-06)*phi +  (2.9482e-04))*pp*pp +  ((3.7229e-06)*phi*phi +  (7.3215e-06)*phi +  (-0.0050685))*pp + ((-1.1974e-05)*phi*phi + (-1.3043e-04)*phi + (0.0078836));
#                         dp = dp +  ((1.0867e-06)*phi*phi + (-7.7630e-07)*phi + (-4.4930e-05))*pp*pp + ((-5.6564e-06)*phi*phi + (-1.3417e-05)*phi +  (2.5224e-04))*pp +  ((6.8460e-06)*phi*phi +  (9.0495e-05)*phi + (-4.6587e-04));
#                         dp = dp +  ((8.5720e-07)*phi*phi + (-6.7464e-06)*phi + (-4.0944e-05))*pp*pp + ((-4.7370e-06)*phi*phi +  (5.8808e-05)*phi +  (1.9047e-04))*pp +  ((5.7404e-06)*phi*phi + (-1.1105e-04)*phi + (-1.9392e-04));
#                     }
#                     if(sec == 6){
#                         dp =       ((2.1191e-06)*phi*phi + (-3.3710e-05)*phi +  (2.5741e-04))*pp*pp + ((-1.2915e-05)*phi*phi +  (2.3753e-04)*phi + (-2.6882e-04))*pp +  ((2.2676e-05)*phi*phi + (-2.3115e-04)*phi + (-0.001283));
#                         dp = dp +  ((6.0270e-07)*phi*phi + (-6.8200e-06)*phi +  (1.3103e-04))*pp*pp + ((-1.8745e-06)*phi*phi +  (3.8646e-05)*phi + (-8.8056e-04))*pp +  ((2.0885e-06)*phi*phi + (-3.4932e-05)*phi + (4.5895e-04));
#                         dp = dp +  ((4.7349e-08)*phi*phi + (-5.7528e-06)*phi + (-3.4097e-06))*pp*pp +  ((1.7731e-06)*phi*phi +  (3.5865e-05)*phi + (-5.7881e-04))*pp + ((-9.7008e-06)*phi*phi + (-4.1836e-05)*phi + (0.0035403));
#                     }
#                 }
#                 /////////////////////////////////////////////////////////////////////////////////
#                 //=============================================================================//
#                 //==========//==========//  π+ Pion Corrections (End)  //==========//==========//
#                 //=============================================================================//
#                 /////////////////////////////////////////////////////////////////////////////////
#                 /////////////////////////////////////////////////////////////////////////////////
#                 //=============================================================================//
#                 //==========//==========//     π- Pion Corrections     //==========//==========//
#                 //=============================================================================//
#                 /////////////////////////////////////////////////////////////////////////////////
#                 if(ivec == 2){
#                     if(sec == 1){
#                         dp = ((-4.0192658422317425e-06)*phi*phi - (2.660222128967742e-05)*phi + 0.004774434682983547)*pp*pp;
#                         dp = dp + ((1.9549520962477972e-05)*phi*phi - 0.0002456062756770577*phi - 0.03787692408323466)*pp; 
#                         dp = dp + (-2.128953094937459e-05)*phi*phi + 0.0002461708852239913*phi + 0.08060704449822174 - 0.01;
#                     }
#                     if(sec == 2){
#                         dp = ((1.193010521758372e-05)*phi*phi - (5.996221756031922e-05)*phi + 0.0009093437955814359)*pp*pp;
#                         dp = dp + ((-4.89113824430594e-05)*phi*phi + 0.00021676479488147118*phi - 0.01861892053916726)*pp;  
#                         dp = dp + (4.446394152208071e-05)*phi*phi - (3.6592784167335244e-05)*phi + 0.05498710249944096 - 0.01;
#                     }
#                     if(sec == 3){
#                         dp = ((-1.6596664895992133e-07)*phi*phi + (6.317189710683516e-05)*phi + 0.0016364212312654086)*pp*pp;
#                         dp = dp + ((-2.898409777520318e-07)*phi*phi - 0.00014531513577533802*phi - 0.025456145839203827)*pp;  
#                         dp = dp + (2.6432552410603506e-06)*phi*phi + 0.00018447151306275443*phi + 0.06442602664627255 - 0.01;
#                     }
#                     if(sec == 4){
#                         dp = ((2.4035259647558634e-07)*phi*phi - (8.649647351491232e-06)*phi + 0.004558993439848128)*pp*pp;
#                         dp = dp + ((-5.981498144060984e-06)*phi*phi + 0.00010582131454222416*phi - 0.033572004651981686)*pp;  
#                         dp = dp + (8.70140266889548e-06)*phi*phi - 0.00020137414379966883*phi + 0.07258774523336173 - 0.01;   
#                     }
#                     if(sec == 5){
#                         dp = ((2.5817024702834863e-06)*phi*phi + 0.00010132810066914441*phi + 0.003397314538804711)*pp*pp;
#                         dp = dp + ((-1.5116941263931812e-05)*phi*phi - 0.00040679799541839254*phi - 0.028144285760769876)*pp;  
#                         dp = dp + (1.4701931057951464e-05)*phi*phi + 0.0002426350390593454*phi + 0.06781682510174941 - 0.01;
#                     }
#                     if(sec == 6){
#                         dp = ((-8.196823669099362e-07)*phi*phi - (5.280412421933636e-05)*phi + 0.0018457238328451137)*pp*pp;
#                         dp = dp + ((5.2675062282094536e-06)*phi*phi + 0.0001515803461044587*phi - 0.02294371578470564)*pp;  
#                         dp = dp + (-9.459454671739747e-06)*phi*phi - 0.0002389523716779765*phi + 0.06428970810739926 - 0.01;
#                     }
#                 }
#                 /////////////////////////////////////////////////////////////////////////////////
#                 //=============================================================================//
#                 //==========//==========//  π- Pion Corrections (End)  //==========//==========//
#                 //=============================================================================//
#                 /////////////////////////////////////////////////////////////////////////////////
#                 //////////////////////////////////////////////////////////////////////////////////
#                 //==============================================================================//
#                 //==========//==========//      Proton Corrections      //==========//==========//
#                 //==============================================================================//
#                 //////////////////////////////////////////////////////////////////////////////////
#                 if(ivec == 3){
#                     if(sec == 1){
#                         dp = (5.415e-04)*pp*pp + (-1.0262e-02)*pp + (7.78075e-03);
#                         dp = dp + ((1.2129e-04)*pp*pp + (1.5373e-04)*pp + (-2.7084e-04));
#                     }
#                     if(sec == 2){
#                         dp = (-9.5439e-04)*pp*pp + (-2.86273e-03)*pp + (3.38149e-03);
#                         dp = dp + ((-1.6890e-03)*pp*pp + (4.3744e-03)*pp + (-2.1218e-03));
#                     }
#                     if(sec == 3){
#                         dp = (-5.5541e-04)*pp*pp + (-7.69739e-03)*pp + (5.7692e-03);
#                         dp = dp + ((7.6422e-04)*pp*pp + (-1.5425e-03)*pp + (5.4255e-04));
#                     }
#                     if(sec == 4){
#                         dp = (-1.944e-04)*pp*pp + (-5.77104e-03)*pp + (3.42399e-03);
#                         dp = dp + ((1.1174e-03)*pp*pp + (-3.2747e-03)*pp + (2.3687e-03));
#                     }
#                     if(sec == 5){
#                         dp = (1.54009e-03)*pp*pp + (-1.69437e-02)*pp + (1.04656e-02);
#                         dp = dp + ((-2.1067e-04)*pp*pp + (1.2266e-03)*pp + (-1.0553e-03));
#                     }
#                     if(sec == 6){
#                         dp = (2.38182e-03)*pp*pp + (-2.07301e-02)*pp + (1.72325e-02);
#                         dp = dp + ((-3.6002e-04)*pp*pp + (8.9582e-04)*pp + (-1.0093e-03));
#                     }
#                 }
#                 //////////////////////////////////////////////////////////////////////////////////
#                 //==============================================================================//
#                 //==========//==========//   Proton Corrections (End)   //==========//==========//
#                 //==============================================================================//
#                 //////////////////////////////////////////////////////////////////////////////////
#                 return dp/pp;
#             }
#             else{
#                 if(corON == 3){ // Pass 2 Data Momentum Corrections
#                     //////////////////////////////////////////////////////////////////////////////////
#                     //==============================================================================//
#                     //==========//==========//     Electron Corrections     //==========//==========//
#                     //==============================================================================//
#                     //////////////////////////////////////////////////////////////////////////////////
#                     if(ivec == 0){
#                         if(sec == 1){
#                             dp =      ((-2.9814e-06)*phi*phi + (-1.3177e-06)*phi + (-3.9424e-04))*pp*pp +  ((3.1475e-05)*phi*phi + (-1.7967e-04)*phi +  (3.7474e-04))*pp + ((-6.5941e-05)*phi*phi +  (8.3099e-04)*phi + (0.032777));
#                             dp = dp +  ((2.1054e-07)*phi*phi + (-2.2491e-05)*phi + (-8.5798e-05))*pp*pp + ((-7.1256e-06)*phi*phi +  (1.9323e-04)*phi +   (0.0014213))*pp +  ((3.4079e-05)*phi*phi + (-3.7406e-04)*phi + (-0.0050973));
#                             dp = dp + ((-4.4455e-06)*phi*phi +  (5.2006e-06)*phi +  (5.2186e-04))*pp*pp +  ((5.4746e-05)*phi*phi + (-1.0079e-04)*phi +  (-0.0069383))*pp + ((-1.5578e-04)*phi*phi +  (3.5947e-04)*phi + (0.024074));
#                             dp = dp + ((-2.6078e-06)*phi*phi + (-4.3875e-06)*phi +  (2.5482e-04))*pp*pp +  ((3.2246e-05)*phi*phi +  (6.6817e-05)*phi +    (-0.00348))*pp + ((-9.4096e-05)*phi*phi + (-2.2928e-04)*phi + (0.01352));
#                         }
#                         if(sec == 2){
#                             dp =      ((-9.1199e-08)*phi*phi +  (1.5504e-05)*phi + (-8.6526e-04))*pp*pp + ((-1.4237e-05)*phi*phi + (-3.8364e-04)*phi +   (0.0065896))*pp +  ((9.4995e-05)*phi*phi +   (0.0013291)*phi + (-0.0014618));
#                             dp = dp + ((-2.6120e-06)*phi*phi + (-1.7473e-05)*phi + (-4.4569e-05))*pp*pp +  ((3.0510e-05)*phi*phi +  (1.6557e-04)*phi +  (3.7791e-04))*pp + ((-8.3982e-05)*phi*phi + (-3.9073e-04)*phi + (-7.4750e-04));
#                             dp = dp + ((-5.0891e-06)*phi*phi + (-2.0499e-05)*phi +  (3.3179e-04))*pp*pp +  ((6.1969e-05)*phi*phi +  (2.2982e-04)*phi +  (-0.0046372))*pp + ((-1.7498e-04)*phi*phi + (-5.9972e-04)*phi + (0.018597));
#                             dp = dp +  ((5.0347e-08)*phi*phi +  (6.5833e-08)*phi +  (1.5151e-04))*pp*pp + ((-2.8341e-06)*phi*phi + (-2.5084e-05)*phi +  (-0.0020883))*pp +  ((1.6091e-05)*phi*phi +  (2.4040e-04)*phi + (0.0089674));
#                         }
#                         if(sec == 3){
#                             dp =      ((-1.7128e-06)*phi*phi +  (3.6506e-05)*phi + (-5.0322e-04))*pp*pp +  ((1.1945e-05)*phi*phi + (-4.3094e-04)*phi +   (0.0025542))*pp +  ((6.9253e-06)*phi*phi +  (9.8027e-04)*phi + (0.0062225));
#                             dp = dp + ((-1.2384e-08)*phi*phi + (-1.2878e-05)*phi + (-1.5680e-04))*pp*pp + ((-7.6080e-06)*phi*phi +  (2.0174e-04)*phi +   (0.0022586))*pp +  ((4.8887e-05)*phi*phi + (-7.6605e-04)*phi + (-0.0076052));
#                             dp = dp + ((-3.9399e-06)*phi*phi + (-1.1728e-05)*phi + (-1.7596e-04))*pp*pp +  ((4.7853e-05)*phi*phi +  (1.5792e-04)*phi +   (0.0016687))*pp + ((-1.4504e-04)*phi*phi + (-4.8236e-04)*phi + (0.0016249));
#                             dp = dp +  ((5.4972e-07)*phi*phi + (-2.3883e-05)*phi +  (1.5269e-04))*pp*pp + ((-6.9613e-06)*phi*phi +  (2.7983e-04)*phi +  (-0.0029828))*pp + ((-1.2184e-06)*phi*phi + (-7.9843e-04)*phi + (0.017712));
#                         }
#                         if(sec == 4){
#                             dp =      ((-3.4682e-06)*phi*phi +  (2.2003e-05)*phi +  (5.7129e-04))*pp*pp +  ((4.1493e-05)*phi*phi + (-1.4497e-04)*phi +   (-0.010517))*pp + ((-1.0323e-04)*phi*phi + (-2.7535e-04)*phi + (0.062998));
#                             dp = dp +  ((1.1756e-06)*phi*phi +  (9.2843e-06)*phi + (-3.8049e-04))*pp*pp + ((-1.5805e-05)*phi*phi + (-6.8510e-05)*phi +   (0.0039821))*pp +  ((3.5444e-05)*phi*phi + (-1.3072e-04)*phi + (-0.0052522));
#                             dp = dp + ((-9.1117e-09)*phi*phi +  (1.2690e-05)*phi + (-3.6216e-04))*pp*pp + ((-1.4697e-06)*phi*phi + (-1.7092e-04)*phi +   (0.0044829))*pp +  ((1.7339e-05)*phi*phi +  (6.4128e-04)*phi + (-0.010911));
#                             dp = dp + ((-1.6261e-06)*phi*phi + (-2.1688e-05)*phi +  (2.9801e-04))*pp*pp +  ((2.4431e-05)*phi*phi +  (2.5886e-04)*phi +  (-0.0039035))*pp + ((-9.5725e-05)*phi*phi + (-5.2092e-04)*phi + (0.013865));
#                         }
#                         if(sec == 5){
#                             dp =       ((8.6648e-07)*phi*phi +  (2.5573e-05)*phi +  (6.5377e-05))*pp*pp + ((-1.0315e-05)*phi*phi + (-3.5840e-04)*phi +  (-0.0066741))*pp +  ((2.1142e-05)*phi*phi +  (5.8774e-04)*phi + (0.045555));
#                             dp = dp +  ((1.3520e-06)*phi*phi + (-2.2701e-06)*phi + (-1.4880e-04))*pp*pp + ((-1.7672e-05)*phi*phi + (-7.3631e-06)*phi +   (0.0018864))*pp +  ((5.2958e-05)*phi*phi +  (4.8608e-05)*phi + (-0.005351));
#                             dp = dp + ((-1.6660e-06)*phi*phi +  (1.2066e-05)*phi +  (2.5740e-04))*pp*pp +  ((2.1087e-05)*phi*phi + (-2.2948e-04)*phi +  (-0.0034624))*pp + ((-6.1307e-05)*phi*phi +  (8.9383e-04)*phi + (0.014613));
#                             dp = dp +  ((2.5118e-07)*phi*phi + (-9.5617e-06)*phi +  (1.8624e-04))*pp*pp + ((-3.0324e-06)*phi*phi +  (7.8390e-05)*phi +  (-0.0026539))*pp +  ((5.7233e-06)*phi*phi +  (2.6912e-05)*phi + (0.011676));
#                         }
#                         if(sec == 6){
#                             dp =       ((2.2827e-06)*phi*phi + (-8.3888e-06)*phi + (-3.2263e-04))*pp*pp + ((-3.6229e-05)*phi*phi +  (1.2242e-04)*phi + (-4.8752e-04))*pp +  ((1.4049e-04)*phi*phi + (-5.0717e-04)*phi + (0.021858));
#                             dp = dp + ((-2.1844e-06)*phi*phi + (-4.4769e-06)*phi + (-3.0654e-05))*pp*pp +  ((2.6552e-05)*phi*phi +  (1.8092e-05)*phi +  (5.2104e-04))*pp + ((-7.6253e-05)*phi*phi +  (5.1816e-05)*phi + (-0.001956));
#                             dp = dp + ((-1.9016e-06)*phi*phi +  (1.2110e-05)*phi +  (2.6684e-04))*pp*pp +  ((2.4525e-05)*phi*phi + (-1.1772e-04)*phi +  (-0.0034957))*pp + ((-7.8749e-05)*phi*phi +  (2.3031e-04)*phi + (0.015083));
#                             dp = dp + ((-1.5191e-07)*phi*phi +  (8.7979e-06)*phi +  (6.5120e-05))*pp*pp +  ((2.1214e-06)*phi*phi + (-8.5858e-05)*phi +  (-0.0013935))*pp + ((-1.3211e-05)*phi*phi +  (1.5676e-04)*phi + (0.0097685));
#                         }
#                     }
#                     //////////////////////////////////////////////////////////////////////////////////
#                     //==============================================================================//
#                     //==========//==========//  Electron Corrections (End)  //==========//==========//
#                     //==============================================================================//
#                     //////////////////////////////////////////////////////////////////////////////////
#                     /////////////////////////////////////////////////////////////////////////////////
#                     //=============================================================================//
#                     //==========//==========//     π+ Pion Corrections     //==========//==========//
#                     //=============================================================================//
#                     /////////////////////////////////////////////////////////////////////////////////
#                     if(ivec == 1){
#                         if(sec == 1){
#                             dp =       ((1.0111e-06)*phi*phi +  (5.5576e-05)*phi + (-2.0734e-04))*pp*pp + ((-4.7499e-06)*phi*phi + (-6.3800e-04)*phi +   (0.0017997))*pp + ((-3.6325e-06)*phi*phi +  (1.0091e-04)*phi + (-4.1379e-04));
#                             dp = dp +  ((9.6529e-07)*phi*phi + (-6.3808e-06)*phi +  (1.6481e-04))*pp*pp + ((-7.4268e-06)*phi*phi +  (1.4101e-04)*phi +  (-0.0030306))*pp +  ((1.0624e-05)*phi*phi + (-1.7095e-04)*phi + (0.010411));
#                             dp = dp + ((-6.2255e-07)*phi*phi +  (1.0214e-06)*phi +  (2.5344e-04))*pp*pp +  ((7.9815e-06)*phi*phi +  (3.3594e-05)*phi +  (-0.0027925))*pp + ((-1.8099e-05)*phi*phi + (-5.4133e-05)*phi + (0.0071398));
#                             dp = dp + ((-1.5386e-08)*phi*phi + (-3.0703e-06)*phi + (-6.3720e-05))*pp*pp +  ((1.3492e-06)*phi*phi +  (5.6471e-05)*phi +  (3.5015e-04))*pp + ((-8.2798e-07)*phi*phi + (-1.0091e-04)*phi + (-0.0016961));
#                         }
#                         if(sec == 2){
#                             dp =       ((3.2353e-06)*phi*phi +  (3.2231e-05)*phi + (-5.2636e-04))*pp*pp + ((-2.1611e-05)*phi*phi + (-3.6647e-04)*phi +   (0.0046012))*pp +  ((1.9479e-05)*phi*phi +  (4.8691e-05)*phi + (-0.0077236));
#                             dp = dp + ((-8.0014e-07)*phi*phi +  (9.0447e-06)*phi +  (6.3132e-04))*pp*pp +  ((8.1699e-06)*phi*phi +  (6.3365e-05)*phi +  (-0.0072546))*pp + ((-7.7759e-06)*phi*phi + (-3.1762e-04)*phi + (0.012731));
#                             dp = dp + ((-1.2641e-06)*phi*phi + (-1.5281e-06)*phi +  (3.2149e-04))*pp*pp +  ((9.2496e-06)*phi*phi +  (5.0090e-05)*phi +   (-0.002904))*pp + ((-1.4918e-05)*phi*phi + (-1.2946e-04)*phi + (0.0066272));
#                             dp = dp + ((-5.8884e-07)*phi*phi +  (1.0919e-05)*phi +  (9.1370e-05))*pp*pp +  ((7.5700e-06)*phi*phi + (-9.0078e-05)*phi +   (-0.001896))*pp + ((-1.8800e-05)*phi*phi +  (1.2259e-04)*phi + (0.0034845));
#                         }
#                         if(sec == 3){
#                             dp =      ((-5.0785e-08)*phi*phi + (-1.2543e-05)*phi + (-6.5541e-05))*pp*pp + ((-2.9050e-06)*phi*phi +  (1.6694e-04)*phi + (-1.6092e-06))*pp +  ((8.7479e-06)*phi*phi + (-1.4064e-04)*phi + (-0.0019552));
#                             dp = dp + ((-1.0293e-07)*phi*phi +  (5.9311e-06)*phi +  (3.4851e-04))*pp*pp +  ((4.7281e-06)*phi*phi + (-1.1553e-04)*phi +  (-0.0041831))*pp + ((-1.4566e-05)*phi*phi +  (1.4323e-04)*phi + (0.01277));
#                             dp = dp +  ((2.4281e-07)*phi*phi + (-1.2261e-06)*phi +  (4.4800e-05))*pp*pp + ((-1.4789e-07)*phi*phi + (-1.2145e-05)*phi + (-5.5506e-04))*pp + ((-3.7526e-07)*phi*phi +  (3.6310e-05)*phi + (0.001157));
#                             dp = dp + ((-7.0691e-07)*phi*phi + (-6.6656e-06)*phi +  (2.5692e-04))*pp*pp +  ((6.6035e-06)*phi*phi +  (5.3531e-05)*phi +  (-0.0030788))*pp + ((-1.0673e-05)*phi*phi + (-1.1955e-04)*phi + (0.0039758));
#                         }
#                         if(sec == 4){
#                             dp =       ((6.8155e-07)*phi*phi +  (4.1069e-06)*phi + (-5.7928e-04))*pp*pp + ((-7.9321e-06)*phi*phi + (-1.1182e-05)*phi +   (0.0057558))*pp +  ((1.6317e-05)*phi*phi + (-2.3502e-05)*phi + (-0.015802));
#                             dp = dp + ((-3.8735e-07)*phi*phi + (-1.4431e-05)*phi +  (8.2589e-04))*pp*pp +  ((1.0733e-05)*phi*phi +  (6.8166e-05)*phi +    (-0.00904))*pp + ((-3.4539e-05)*phi*phi +  (5.0404e-05)*phi + (0.026127));
#                             dp = dp +  ((2.2241e-07)*phi*phi + (-1.0564e-05)*phi +  (3.5392e-04))*pp*pp + ((-5.9992e-07)*phi*phi +  (5.5053e-05)*phi +  (-0.0025682))*pp +  ((5.4840e-06)*phi*phi +  (6.0706e-06)*phi + (0.0031961));
#                             dp = dp +  ((4.2134e-07)*phi*phi + (-7.2136e-06)*phi + (-6.6800e-05))*pp*pp + ((-3.8195e-06)*phi*phi +  (6.2408e-05)*phi +  (2.0413e-04))*pp +  ((9.2423e-06)*phi*phi + (-1.1143e-04)*phi + (-0.0027527));
#                         }
#                         if(sec == 5){
#                             dp =      ((-9.8062e-07)*phi*phi +  (1.8881e-05)*phi + (-4.3191e-04))*pp*pp +  ((5.8950e-06)*phi*phi + (-1.8007e-04)*phi +   (0.0054105))*pp + ((-1.6796e-05)*phi*phi + (-8.0562e-05)*phi + (-0.013527));
#                             dp = dp +  ((1.1929e-08)*phi*phi +  (4.0469e-06)*phi +   (0.0015612))*pp*pp +  ((4.4733e-06)*phi*phi + (-3.5644e-05)*phi +   (-0.015765))*pp + ((-5.6667e-06)*phi*phi +  (8.1663e-05)*phi + (0.02723));
#                             dp = dp +  ((3.8356e-07)*phi*phi +  (3.3064e-06)*phi +  (1.2935e-04))*pp*pp + ((-4.5853e-07)*phi*phi + (-3.2460e-05)*phi +  (-0.0018519))*pp + ((-2.7462e-06)*phi*phi +  (7.2391e-05)*phi + (0.0060517));
#                             dp = dp +  ((7.6080e-07)*phi*phi + (-4.1006e-06)*phi + (-9.5440e-05))*pp*pp + ((-7.0970e-06)*phi*phi +  (6.1629e-05)*phi +  (3.5178e-04))*pp +  ((1.6766e-05)*phi*phi + (-1.8855e-04)*phi + (-0.0021373));
#                         }
#                         if(sec == 6){
#                             dp =       ((4.8744e-07)*phi*phi +  (8.0932e-05)*phi + (-8.0001e-04))*pp*pp + ((-3.6221e-06)*phi*phi + (-5.9260e-04)*phi +   (0.0049435))*pp +  ((3.4766e-06)*phi*phi +  (3.9113e-04)*phi + (-0.013482));
#                             dp = dp +  ((1.3205e-06)*phi*phi + (-3.4827e-05)*phi +   (0.0014486))*pp*pp + ((-7.2797e-06)*phi*phi +  (2.2309e-04)*phi +  (-0.0091902))*pp +  ((8.5223e-06)*phi*phi + (-1.5744e-04)*phi + (0.018861));
#                             dp = dp +  ((1.1602e-06)*phi*phi + (-1.9015e-05)*phi + (-3.6810e-05))*pp*pp + ((-6.8771e-06)*phi*phi +  (1.4793e-04)*phi +  (1.8771e-04))*pp +  ((2.6825e-06)*phi*phi + (-2.0166e-04)*phi + (0.0037471));
#                             dp = dp + ((-1.0246e-06)*phi*phi + (-1.3784e-05)*phi +  (6.4560e-05))*pp*pp +  ((9.8205e-06)*phi*phi +  (1.4208e-04)*phi +   (-0.001803))*pp + ((-1.3982e-05)*phi*phi + (-2.5638e-04)*phi + (0.0027303));
#                         }
#                     }
#                     /////////////////////////////////////////////////////////////////////////////////
#                     //=============================================================================//
#                     //==========//==========//  π+ Pion Corrections (End)  //==========//==========//
#                     //=============================================================================//
#                     /////////////////////////////////////////////////////////////////////////////////
#                     return dp/pp;
#                 }
#                 else{// Pass 2 Monte Carlo Simulated Corrections (corON == 4)
#                     // No Pass 2 MC Corrections as of 3/26/2024
#                     dp = 0;
#                     return dp/pp;
#                 }
#             }
#         }
#     }
# };"""

Correction_Code_Full_In = """

double dppC(float Px, float Py, float Pz, int sec, int ivec, int corON) {
    
    // 'Px'/'Py'/'Pz'   ==> Corresponds to the Cartesian Components of the particle momentum being corrected
    // 'sec'            ==> Corresponds to the Forward Detector Sectors where the given particle is detected (6 total)
    // 'ivec'           ==> Corresponds to the particle being corrected (See below)    
        // (*) ivec = 0 --> Electron Corrections
        // (*) ivec = 1 --> Pi+ Corrections
    // 'corON' ==> Controls which version of the particle correction is used
        // Includes:
            // (*) Correction On/Off
            // (*) Pass Version
            // (*) Data Set (Experimental or Monte Carlo)
        // corON == 0 --> DOES NOT apply the momentum corrections (i.e., turns the corrections 'off')
        // corON == 1 --> Fall  2018 - Pass 1 (Experimental Data)
        // corON == 2 --> Applies the (Pass 1) momentum corrections for the Monte Carlo (simulated) data
        // corON == 3 --> Fall  2018 - Pass 2 (Experimental Data)
        // corON == 4 --> Applies the (Pass 2) momentum corrections for the Monte Carlo (simulated) data
            // Not Available as of 8/30/2024

    // Momentum Magnitude
    double pp = sqrt(Px*Px + Py*Py + Pz*Pz);

    // Initializing the correction factor
    double dp = 0;

    // Defining Phi Angle
    double Phi = (180/3.1415926)*atan2(Py, Px);

    // Central Detector Corrections Not Included (Yet)

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
    
    if(corON == 2){ // Pass 1 Monte Carlo Simulated Corrections
        // Not Sector or Angle dependent (as of 3-21-2023)
        // Both particles were corrected at the same time using Extra_Name = "Multi_Dimension_Unfold_V1_"
        // Used ∆P = GEN - REC so the other particle does not affect how much the correction is needed
        if(ivec == 0){ // Electron Corrections
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
        }
        return dp/pp;
    }
    else{
        ////////////////////////////////////////////////////////////////////////////////////////////////
        //===============//===============//     No Corrections     //===============//===============//
        ////////////////////////////////////////////////////////////////////////////////////////////////
        if(corON == 0 || corON == 4){ // No Momentum Corrections (Also no Pass 2 Monte Carlo Momentum Corrections)
            return dp/pp;
        }
        ////////////////////////////////////////////////////////////////////////////////////////////////
        //==============//==============//    No Corrections (End)    //==============//==============//
        ////////////////////////////////////////////////////////////////////////////////////////////////


        //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        //==================================================================================================================================//
        //=======================//=======================//     Electron Corrections     //=======================//=======================//
        //==================================================================================================================================//
        //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        if(corON != 0 && ivec == 0){
            if(corON == 1){ // Fall 2018 - Pass 1 Corrections
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

            if(corON == 3){ // Fall 2018 - Pass 2 Corrections
                if(sec == 1){
                    dp            =                ((-9.82416e-06)*phi*phi +            (-2.29956e-05)*phi +  (0.00029664199999999996))*pp*pp +           ((0.0001113414)*phi*phi +  (-2.041300000000001e-05)*phi +            (-0.00862226))*pp +            ((-0.000281738)*phi*phi +             (0.00058712)*phi +              (0.0652737));
                    if(pp < 7){dp = dp +            ((-3.4001e-06)*phi*phi +             (-2.2885e-05)*phi +              (9.9705e-04))*pp*pp +             ((2.1840e-05)*phi*phi +              (2.4238e-04)*phi +             (-0.0091904))*pp +             ((-2.9180e-05)*phi*phi +            (-6.4496e-04)*phi +               (0.022505));}
                    else{      dp = dp +            ((-6.3656e-05)*phi*phi +              (1.7266e-04)*phi +              (-0.0017909))*pp*pp +                ((0.00104)*phi*phi +              (-0.0028401)*phi +                (0.02981))*pp +              ((-0.0041995)*phi*phi +               (0.011537)*phi +                (-0.1196));}
                    dp            = dp + ((3.2780000000000006e-07)*phi*phi +              (6.7084e-07)*phi +  (-4.390000000000004e-05))*pp*pp + ((-7.230999999999999e-06)*phi*phi +            (-2.37482e-05)*phi +  (0.0004909000000000007))*pp +   ((3.285299999999999e-05)*phi*phi +            (9.63723e-05)*phi +               (-0.00115));
                }
                if(sec == 2){
                    dp            =               ((-7.741952e-06)*phi*phi + (-2.2402167000000004e-05)*phi + (-0.00042652900000000004))*pp*pp +            ((7.54079e-05)*phi*phi + (-1.3333999999999984e-05)*phi +  (0.0002420100000000004))*pp +            ((-0.000147876)*phi*phi +             (0.00057905)*phi +              (0.0253551));
                    if(pp < 7){dp = dp +             ((5.3611e-06)*phi*phi +              (8.1979e-06)*phi +              (5.9789e-04))*pp*pp +            ((-4.8185e-05)*phi*phi +             (-1.5188e-04)*phi +             (-0.0084675))*pp +              ((9.2324e-05)*phi*phi +             (6.4420e-04)*phi +               (0.026792));}
                    else{      dp = dp +            ((-6.1139e-05)*phi*phi +              (5.4087e-06)*phi +              (-0.0021284))*pp*pp +              ((0.0010007)*phi*phi +              (9.3492e-05)*phi +               (0.039813))*pp +              ((-0.0040434)*phi*phi +             (-0.0010953)*phi +               (-0.18112));}
                    dp            = dp +           ((6.221217e-07)*phi*phi +  (1.9596000000000003e-06)*phi +              (-9.826e-05))*pp*pp +           ((-1.28576e-05)*phi*phi +            (-4.36589e-05)*phi +             (0.00130342))*pp +             ((5.80399e-05)*phi*phi +            (0.000215388)*phi + (-0.0040414000000000005));
                }
                if(sec == 3){
                    dp            =      ((-5.115364000000001e-06)*phi*phi + (-1.1983000000000004e-05)*phi +  (-0.0006832899999999999))*pp*pp +            ((4.52287e-05)*phi*phi +  (0.00020855000000000003)*phi +  (0.0034986999999999996))*pp +  ((-9.044610000000001e-05)*phi*phi +            (-0.00106657)*phi +   (0.017954199999999997));
                    if(pp < 7){dp = dp +             ((9.9281e-07)*phi*phi +              (3.4879e-06)*phi +               (0.0011673))*pp*pp +            ((-2.0071e-05)*phi*phi +             (-3.1362e-05)*phi +              (-0.012329))*pp +              ((6.9463e-05)*phi*phi +             (3.5102e-05)*phi +               (0.037505));}
                    else{      dp = dp +            ((-3.2178e-06)*phi*phi +              (4.0630e-05)*phi +               (-0.005209))*pp*pp +             ((2.0884e-05)*phi*phi +             (-6.8800e-04)*phi +               (0.086513))*pp +              ((3.9530e-05)*phi*phi +              (0.0029306)*phi +                (-0.3507));}
                    dp            = dp + ((-4.045999999999999e-07)*phi*phi + (-1.3115999999999994e-06)*phi +  (3.9510000000000006e-05))*pp*pp +              ((5.521e-06)*phi*phi +  (2.4436999999999997e-05)*phi +             (-0.0016887))*pp + ((-1.0962999999999997e-05)*phi*phi +           (-0.000151944)*phi +   (0.009313599999999998));
                }
                if(sec == 4){
                    dp            =     ((-3.9278116999999996e-06)*phi*phi +  (2.2289300000000004e-05)*phi +  (0.00012665000000000002))*pp*pp + ((4.8649299999999995e-05)*phi*phi +             (-0.00012554)*phi +  (-0.005955500000000001))*pp + ((-0.00014617199999999997)*phi*phi +            (-0.00028571)*phi +              (0.0606998));
                    if(pp < 7){dp = dp +            ((-4.8455e-06)*phi*phi +             (-1.2074e-05)*phi +               (0.0013221))*pp*pp +             ((3.2207e-05)*phi*phi +              (1.3144e-04)*phi +              (-0.010451))*pp +             ((-3.7365e-05)*phi*phi +            (-4.2344e-04)*phi +               (0.019952));}
                    else{      dp = dp +            ((-3.9554e-05)*phi*phi +              (5.5496e-06)*phi +              (-0.0058293))*pp*pp +             ((6.5077e-04)*phi*phi +              (2.6735e-05)*phi +               (0.095025))*pp +              ((-0.0026457)*phi*phi +            (-6.1394e-04)*phi +                (-0.3793));}
                    dp            = dp +          ((-4.593089e-07)*phi*phi +             (1.40673e-05)*phi +                (6.69e-05))*pp*pp +             ((4.0239e-06)*phi*phi +            (-0.000180863)*phi + (-0.0008272199999999999))*pp + ((-5.1310000000000005e-06)*phi*phi +             (0.00049748)*phi +             (0.00255231));
                }
                if(sec == 5){
                    dp            =       ((8.036599999999999e-07)*phi*phi +             (2.58072e-05)*phi +             (0.000360217))*pp*pp + ((-9.932400000000002e-06)*phi*phi +           (-0.0005168531)*phi +              (-0.010904))*pp +  ((1.8516299999999998e-05)*phi*phi +  (0.0015570900000000001)*phi +               (0.066493));
                    if(pp < 7){dp = dp +             ((7.7156e-07)*phi*phi +             (-3.9566e-05)*phi +             (-2.3589e-04))*pp*pp +            ((-9.8309e-06)*phi*phi +              (3.7353e-04)*phi +              (0.0020382))*pp +              ((2.9506e-05)*phi*phi +            (-8.0409e-04)*phi +             (-0.0045615));}
                    else{      dp = dp +            ((-3.2410e-05)*phi*phi +             (-4.3301e-05)*phi +              (-0.0028742))*pp*pp +             ((5.3787e-04)*phi*phi +              (6.8921e-04)*phi +               (0.049578))*pp +              ((-0.0021955)*phi*phi +             (-0.0027698)*phi +               (-0.21142));}
                    dp            = dp +            ((-1.2151e-06)*phi*phi +             (-8.5087e-06)*phi +               (4.968e-05))*pp*pp +            ((1.46998e-05)*phi*phi +             (0.000115047)*phi +            (-0.00039269))*pp + ((-4.0368600000000005e-05)*phi*phi +            (-0.00037078)*phi +             (0.00073998));
                }
                if(sec == 6){
                    dp            =     ((-1.9552099999999998e-06)*phi*phi +   (8.042199999999997e-06)*phi + (-2.1324000000000028e-05))*pp*pp + ((1.6969399999999997e-05)*phi*phi +  (-6.306600000000001e-05)*phi +            (-0.00485568))*pp +             ((-2.7723e-05)*phi*phi + (-6.828400000000003e-05)*phi +              (0.0447535));
                    if(pp < 7){dp = dp +            ((-8.2535e-07)*phi*phi +              (9.1433e-06)*phi +              (3.5395e-04))*pp*pp +            ((-3.4272e-06)*phi*phi +             (-1.3012e-04)*phi +             (-0.0030724))*pp +              ((4.9211e-05)*phi*phi +             (4.5807e-04)*phi +              (0.0058932));}
                    else{      dp = dp +            ((-4.9760e-05)*phi*phi +             (-7.2903e-05)*phi +              (-0.0020453))*pp*pp +             ((8.0918e-04)*phi*phi +               (0.0011688)*phi +               (0.037042))*pp +              ((-0.0032504)*phi*phi +             (-0.0046169)*phi +               (-0.16331));}
                    dp            = dp + ((-7.153000000000002e-07)*phi*phi +             (1.62859e-05)*phi +               (8.129e-05))*pp*pp + ((7.2249999999999994e-06)*phi*phi +            (-0.000178946)*phi + (-0.0009485399999999999))*pp + ((-1.3018000000000003e-05)*phi*phi + (0.00046643000000000005)*phi +             (0.00266508));
                }
            }
        }
        ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        //====================================================================================================================================//
        //======================//======================//     Electron Corrections (End)     //======================//======================//
        //====================================================================================================================================//
        ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



        ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        //========================================================================================================================================================//
        //==============================//==============================//     π+ Corrections     //==============================//==============================//
        //========================================================================================================================================================//
        ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        if(corON != 0 && ivec == 1){
            if(corON == 1){ // Fall 2018 - Pass 1 Corrections
                if(sec == 1){
                    dp =      ((-5.4904e-07)*phi*phi + (-1.4436e-05)*phi +  (3.1534e-04))*pp*pp +  ((3.8231e-06)*phi*phi +  (3.6582e-04)*phi +  (-0.0046759))*pp + ((-5.4913e-06)*phi*phi + (-4.0157e-04)*phi +    (0.010767));
                    dp = dp +  ((6.1103e-07)*phi*phi +  (5.5291e-06)*phi + (-1.9120e-04))*pp*pp + ((-3.2300e-06)*phi*phi +  (1.5377e-05)*phi +  (7.5279e-04))*pp +  ((2.1434e-06)*phi*phi + (-6.9572e-06)*phi + (-7.9333e-05));
                    dp = dp + ((-1.3049e-06)*phi*phi +  (1.1295e-05)*phi +  (4.5797e-04))*pp*pp +  ((9.3122e-06)*phi*phi + (-5.1074e-05)*phi +  (-0.0030757))*pp + ((-1.3102e-05)*phi*phi +  (2.2153e-05)*phi +   (0.0040938));
                }
                if(sec == 2){
                    dp =      ((-1.0087e-06)*phi*phi +  (2.1319e-05)*phi +  (7.8641e-04))*pp*pp +  ((6.7485e-06)*phi*phi +  (7.3716e-05)*phi +  (-0.0094591))*pp + ((-1.1820e-05)*phi*phi + (-3.8103e-04)*phi +    (0.018936));
                    dp = dp +  ((8.8155e-07)*phi*phi + (-2.8257e-06)*phi + (-2.6729e-04))*pp*pp + ((-5.4499e-06)*phi*phi +  (3.8397e-05)*phi +   (0.0015914))*pp +  ((6.8926e-06)*phi*phi + (-5.9386e-05)*phi +  (-0.0021749));
                    dp = dp + ((-2.0147e-07)*phi*phi +  (1.1061e-05)*phi +  (3.8827e-04))*pp*pp +  ((4.9294e-07)*phi*phi + (-6.0257e-05)*phi +  (-0.0022087))*pp +  ((9.8548e-07)*phi*phi +  (5.9047e-05)*phi +   (0.0022905));
                }
                if(sec == 3){
                    dp =       ((8.6722e-08)*phi*phi + (-1.7975e-05)*phi +  (4.8118e-05))*pp*pp +  ((2.6273e-06)*phi*phi +  (3.1453e-05)*phi +  (-0.0015943))*pp + ((-6.4463e-06)*phi*phi + (-5.8990e-05)*phi +   (0.0041703));
                    dp = dp +  ((9.6317e-07)*phi*phi + (-1.7659e-06)*phi + (-8.8318e-05))*pp*pp + ((-5.1346e-06)*phi*phi +  (8.3318e-06)*phi +  (3.7723e-04))*pp +  ((3.9548e-06)*phi*phi + (-6.9614e-05)*phi +  (2.1393e-04));
                    dp = dp +  ((5.6438e-07)*phi*phi +  (8.1678e-06)*phi + (-9.4406e-05))*pp*pp + ((-3.9074e-06)*phi*phi + (-6.5174e-05)*phi +  (5.4218e-04))*pp +  ((6.3198e-06)*phi*phi +  (1.0611e-04)*phi + (-4.5749e-04));
                }
                if(sec == 4){
                    dp =       ((4.3406e-07)*phi*phi + (-4.9036e-06)*phi +  (2.3064e-04))*pp*pp +  ((1.3624e-06)*phi*phi +  (3.2907e-05)*phi +  (-0.0034872))*pp + ((-5.1017e-06)*phi*phi +  (2.4593e-05)*phi +   (0.0092479));
                    dp = dp +  ((6.0218e-07)*phi*phi + (-1.4383e-05)*phi + (-3.1999e-05))*pp*pp + ((-1.1243e-06)*phi*phi +  (9.3884e-05)*phi + (-4.1985e-04))*pp + ((-1.8808e-06)*phi*phi + (-1.2222e-04)*phi +   (0.0014037));
                    dp = dp + ((-2.5490e-07)*phi*phi + (-8.5120e-07)*phi +  (7.9109e-05))*pp*pp +  ((2.5879e-06)*phi*phi +  (8.6108e-06)*phi + (-5.1533e-04))*pp + ((-4.4521e-06)*phi*phi + (-1.7012e-05)*phi +  (7.4848e-04));
                }
                if(sec == 5){
                    dp =       ((2.4292e-07)*phi*phi +  (8.8741e-06)*phi +  (2.9482e-04))*pp*pp +  ((3.7229e-06)*phi*phi +  (7.3215e-06)*phi +  (-0.0050685))*pp + ((-1.1974e-05)*phi*phi + (-1.3043e-04)*phi +   (0.0078836));
                    dp = dp +  ((1.0867e-06)*phi*phi + (-7.7630e-07)*phi + (-4.4930e-05))*pp*pp + ((-5.6564e-06)*phi*phi + (-1.3417e-05)*phi +  (2.5224e-04))*pp +  ((6.8460e-06)*phi*phi +  (9.0495e-05)*phi + (-4.6587e-04));
                    dp = dp +  ((8.5720e-07)*phi*phi + (-6.7464e-06)*phi + (-4.0944e-05))*pp*pp + ((-4.7370e-06)*phi*phi +  (5.8808e-05)*phi +  (1.9047e-04))*pp +  ((5.7404e-06)*phi*phi + (-1.1105e-04)*phi + (-1.9392e-04));
                }
                if(sec == 6){
                    dp =       ((2.1191e-06)*phi*phi + (-3.3710e-05)*phi +  (2.5741e-04))*pp*pp + ((-1.2915e-05)*phi*phi +  (2.3753e-04)*phi + (-2.6882e-04))*pp +  ((2.2676e-05)*phi*phi + (-2.3115e-04)*phi +   (-0.001283));
                    dp = dp +  ((6.0270e-07)*phi*phi + (-6.8200e-06)*phi +  (1.3103e-04))*pp*pp + ((-1.8745e-06)*phi*phi +  (3.8646e-05)*phi + (-8.8056e-04))*pp +  ((2.0885e-06)*phi*phi + (-3.4932e-05)*phi +  (4.5895e-04));
                    dp = dp +  ((4.7349e-08)*phi*phi + (-5.7528e-06)*phi + (-3.4097e-06))*pp*pp +  ((1.7731e-06)*phi*phi +  (3.5865e-05)*phi + (-5.7881e-04))*pp + ((-9.7008e-06)*phi*phi + (-4.1836e-05)*phi +   (0.0035403));
                }
            }

            if(corON == 3){ // Fall 2018 - Pass 2 Corrections
                if(sec == 1){
                    dp              =           ((1.338454e-06)*phi*phi +   (4.714629999999999e-05)*phi +  (0.00014719))*pp*pp + ((-2.8460000000000004e-06)*phi*phi +            (-0.000406925)*phi +           (-0.00367325))*pp +           ((-1.193548e-05)*phi*phi +            (-0.000225083)*phi +           (0.01544091));
                    if(pp < 2.5){dp = dp +        ((1.0929e-05)*phi*phi +             (-3.8002e-04)*phi +    (-0.01412))*pp*pp +             ((-2.8491e-05)*phi*phi +              (5.0952e-04)*phi +              (0.037728))*pp +              ((1.6927e-05)*phi*phi +              (1.8165e-04)*phi +            (-0.027772));}
                    else{        dp = dp +        ((4.3191e-07)*phi*phi +             (-9.0581e-05)*phi +  (-0.0011766))*pp*pp +             ((-3.6232e-06)*phi*phi +               (0.0010342)*phi +              (0.012454))*pp +              ((1.2235e-05)*phi*phi +              (-0.0025855)*phi +            (-0.035323));}
                    dp              = dp +       ((-3.7494e-07)*phi*phi +             (-1.5439e-06)*phi +  (4.2760e-05))*pp*pp +              ((3.5348e-06)*phi*phi +              (4.8165e-05)*phi +           (-2.3799e-04))*pp +             ((-8.2116e-06)*phi*phi +             (-7.1750e-05)*phi +           (1.5984e-04));
                }
                if(sec == 2){
                    dp              =             ((5.8222e-07)*phi*phi +  (5.0666599999999994e-05)*phi +  (0.00051782))*pp*pp +              ((3.3785e-06)*phi*phi +            (-0.000343093)*phi + (-0.007453400000000001))*pp + ((-2.2014899999999998e-05)*phi*phi + (-0.00027579899999999997)*phi + (0.015119099999999998));
                    if(pp < 2.5){dp = dp +        ((9.2373e-06)*phi*phi +             (-3.3151e-04)*phi +   (-0.019254))*pp*pp +             ((-2.7546e-05)*phi*phi +              (5.3915e-04)*phi +              (0.052516))*pp +              ((2.5220e-05)*phi*phi +              (7.5362e-05)*phi +            (-0.033504));}
                    else{        dp = dp +        ((2.2654e-08)*phi*phi +             (-8.8436e-05)*phi +  (-0.0013542))*pp*pp +              ((3.0630e-07)*phi*phi +              (9.4319e-04)*phi +                (0.0147))*pp +             ((-3.5941e-06)*phi*phi +              (-0.0022473)*phi +            (-0.036874));}
                    dp              = dp +        ((4.3694e-07)*phi*phi +              (1.1476e-05)*phi +  (1.1123e-04))*pp*pp +             ((-2.4617e-06)*phi*phi +             (-7.5353e-05)*phi +           (-6.2511e-04))*pp +             ((-1.0387e-06)*phi*phi +              (5.8447e-05)*phi +           (6.4986e-04));
                }
                if(sec == 3){
                    dp              =           ((-6.17815e-07)*phi*phi + (-1.4503600000000001e-05)*phi + (0.000584689))*pp*pp +             ((8.27871e-06)*phi*phi +              (9.2796e-05)*phi +         (-0.0078185692))*pp + ((-1.6866360000000002e-05)*phi*phi +  (-8.065000000000001e-05)*phi +            (0.0159476));
                    if(pp < 2.5){dp = dp +        ((1.8595e-06)*phi*phi +              (3.6900e-04)*phi +  (-0.0099622))*pp*pp +              ((8.4410e-06)*phi*phi +              (-0.0010457)*phi +              (0.027038))*pp +             ((-1.2191e-05)*phi*phi +              (6.0203e-04)*phi +            (-0.019176));}
                    else{        dp = dp +        ((6.8265e-07)*phi*phi +              (3.0246e-05)*phi +  (-0.0011116))*pp*pp +             ((-4.8481e-06)*phi*phi +             (-3.7082e-04)*phi +              (0.011452))*pp +              ((7.2478e-06)*phi*phi +              (9.9858e-04)*phi +            (-0.027972));}
                    dp              = dp +        ((1.8639e-07)*phi*phi +              (4.9444e-06)*phi + (-2.9030e-05))*pp*pp +             ((-1.3752e-06)*phi*phi +             (-3.3709e-05)*phi +            (3.8288e-04))*pp +              ((1.0113e-06)*phi*phi +              (5.1273e-05)*phi +          (-6.7844e-04));
                }
                if(sec == 4){
                    dp              =  ((9.379499999999998e-07)*phi*phi + (-2.8101700000000002e-05)*phi +  (0.00053373))*pp*pp + ((-1.6185199999999991e-06)*phi*phi +  (0.00017444500000000001)*phi + (-0.005648269999999999))*pp +  ((-3.495700000000003e-06)*phi*phi +  (-7.845739999999999e-05)*phi + (0.010768400000000001));
                    if(pp < 2.5){dp = dp +        ((9.5779e-06)*phi*phi +              (3.5339e-04)*phi +    (-0.01054))*pp*pp +             ((-1.8077e-05)*phi*phi +              (-0.0010543)*phi +              (0.028379))*pp +              ((3.1773e-06)*phi*phi +              (5.6223e-04)*phi +            (-0.018865));}
                    else{        dp = dp +        ((7.7000e-07)*phi*phi +              (4.1000e-06)*phi +  (-0.0010144))*pp*pp +             ((-8.1960e-06)*phi*phi +             (-4.7753e-05)*phi +              (0.010594))*pp +              ((2.0716e-05)*phi*phi +              (1.2151e-04)*phi +            (-0.028619));}
                    dp              = dp +        ((4.8394e-07)*phi*phi +              (3.6342e-06)*phi + (-2.0136e-04))*pp*pp +             ((-3.2757e-06)*phi*phi +             (-3.5397e-05)*phi +             (0.0015599))*pp +              ((3.2095e-06)*phi*phi +              (7.9013e-05)*phi +            (-0.002012));
                }
                if(sec == 5){
                    dp              = ((1.7566900000000006e-07)*phi*phi +             (2.21337e-05)*phi +   (0.0011632))*pp*pp +   ((2.812770000000001e-06)*phi*phi + (-0.00018654499999999998)*phi + (-0.011854620000000001))*pp +  ((-8.442900000000003e-06)*phi*phi + (-0.00011505800000000001)*phi +            (0.0176174));
                    if(pp < 2.5){dp = dp +        ((3.3685e-05)*phi*phi +              (2.8972e-04)*phi +   (-0.017862))*pp*pp +             ((-8.4089e-05)*phi*phi +             (-9.8038e-04)*phi +              (0.050405))*pp +              ((4.3478e-05)*phi*phi +              (6.9924e-04)*phi +            (-0.033066));}
                    else{        dp = dp +        ((4.6106e-07)*phi*phi +             (-3.6786e-05)*phi +  (-0.0015894))*pp*pp +             ((-4.4217e-06)*phi*phi +              (3.7321e-04)*phi +              (0.015917))*pp +              ((7.5188e-06)*phi*phi +             (-8.0676e-04)*phi +            (-0.036944));}
                    dp              = dp +        ((4.3113e-07)*phi*phi +              (2.6869e-06)*phi + (-2.1326e-04))*pp*pp +             ((-3.1063e-06)*phi*phi +             (-2.7152e-05)*phi +             (0.0017964))*pp +              ((3.1946e-06)*phi*phi +              (4.2059e-05)*phi +           (-0.0031325));
                }
                if(sec == 6){
                    dp              =            ((1.94354e-06)*phi*phi +  (1.3306000000000006e-05)*phi +  (0.00067634))*pp*pp +             ((-7.9584e-06)*phi*phi +  (-7.949999999999998e-05)*phi + (-0.005861990000000001))*pp +   ((6.994000000000005e-07)*phi*phi +             (-0.00022435)*phi +            (0.0118564));
                    if(pp < 2.5){dp = dp +        ((1.7381e-05)*phi*phi +              (5.4630e-04)*phi +   (-0.019637))*pp*pp +             ((-3.8681e-05)*phi*phi +              (-0.0017358)*phi +                (0.0565))*pp +              ((1.2268e-05)*phi*phi +               (0.0011412)*phi +            (-0.035608));}
                    else{        dp = dp +       ((-8.9398e-08)*phi*phi +             (-1.2347e-05)*phi +  (-0.0018442))*pp*pp +              ((7.8164e-08)*phi*phi +              (1.3063e-04)*phi +               (0.01783))*pp +              ((8.2374e-06)*phi*phi +             (-3.5862e-04)*phi +            (-0.047011));}
                    dp              = dp +        ((4.9123e-07)*phi*phi +              (5.1828e-06)*phi + (-1.3898e-04))*pp*pp +             ((-3.4108e-06)*phi*phi +             (-5.0009e-05)*phi +             (0.0014879))*pp +              ((4.0320e-06)*phi*phi +              (6.5853e-05)*phi +           (-0.0032227));
                }
            }
        }
        //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        //==============================================================================================================================================================//
        //==============================//==============================//     π+ Corrections (End)     //==============================//==============================//
        //==============================================================================================================================================================//
        //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    }

    return dp/pp;
};"""








###########################################################################################################################################################################
###########################################################################################################################################################################
###########################################################################################################################################################################
###########################################################################################################################################################################
###########################################################################################################################################################################










Rotation_Matrix = """
/////////////////////////////////////////////          Rotation Matrix          /////////////////////////////////////////////

TLorentzVector Rot_Matrix(TLorentzVector vector, int Lab2CM_or_CM2Lab, double Theta_Rot, double Phi_Rot) {
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









############################################################################
#----------#      π+ Pion Energy Loss Corrections (Pass 2)      #----------#
############################################################################
Pion_Energy_Loss_Cor_Function = """
double eloss_pip_In_Forward(double pion_p, double pip_theta){
    double pion_det = 2;
    bool outbending = false;
    // momentum loss correction for low momentum pions:
    // input: p = pion momentum in GeV, pip_theta = pion theta in degree, 
    //        pion_det = pion detector (2 = FD, 3 = CD),  outbending = torus polarity
    // output: dp_pion = generated momentum - reconstructed momentum = momentum loss (+) / gain (-)

    double dp_pion = 0.0;

    if(outbending == false){ // INBENDING
        if(pion_det == 2){   // Forward Detector
            if(pip_theta < 27){                                       dp_pion =  0.00342646 + (-0.00282934) *pion_p + (0.00205983)   *pow(pion_p,2) + (-0.00043158)  *pow(pion_p,3) + (0) *pow(pion_p,4);}
            if(pip_theta < 27 && pion_p >= 2.5){                      dp_pion =  0.00342646 + (-0.00282934) *2.5    + (0.00205983)   *pow(2.5,2)    + (-0.00043158)  *pow(2.5,3)    + (0) *pow(2.5,4);}
            if(pip_theta > 27 && pip_theta < 28){                     dp_pion =  0.00328565 + (-0.00376042) *pion_p + (0.00433886)   *pow(pion_p,2) + (-0.00141614)  *pow(pion_p,3) + (0) *pow(pion_p,4);}
            if(pip_theta > 27 && pip_theta < 28 && pion_p >= 1.83){   dp_pion =  0.00328565 + (-0.00376042) *1.83   + (0.00433886)   *pow(1.83,2)   + (-0.00141614)  *pow(1.83,3)   + (0) *pow(1.83,4);}
            if(pip_theta > 28 && pip_theta < 29){                     dp_pion =  0.00328579 + (-0.00281121) *pion_p + (0.00342749)   *pow(pion_p,2) + (-0.000932614) *pow(pion_p,3) + (0) *pow(pion_p,4);}
            if(pip_theta > 28 && pip_theta < 29 && pion_p >= 2){      dp_pion =  0.00328579 + (-0.00281121) *2      + (0.00342749)   *pow(2,2)      + (-0.000932614) *pow(2,3)      + (0) *pow(2,4);}
            if(pip_theta > 29 && pip_theta < 30){                     dp_pion =  0.00167358 + (0.00441871)  *pion_p + (-0.000834667) *pow(pion_p,2) + (-0.000137968) *pow(pion_p,3) + (0) *pow(pion_p,4);}
            if(pip_theta > 29 && pip_theta < 30 && pion_p >= 1.9){    dp_pion =  0.00167358 + (0.00441871)  *1.9    + (-0.000834667) *pow(1.9,2)    + (-0.000137968) *pow(1.9,3)    + (0) *pow(1.9,4);}
            if(pip_theta > 30 && pip_theta < 31){                     dp_pion =  0.00274159 + (0.00635686)  *pion_p + (-0.00380977)  *pow(pion_p,2) + (0.00071627)   *pow(pion_p,3) + (0) *pow(pion_p,4);}
            if(pip_theta > 30 && pip_theta < 31 && pion_p >= 1.9){    dp_pion =  0.00274159 + (0.00635686)  *1.9    + (-0.00380977)  *pow(1.9,2)    + (0.00071627)   *pow(1.9,3)    + (0) *pow(1.9,4);}
            if(pip_theta > 31 && pip_theta < 32){                     dp_pion =  0.00450241 + (0.00248969)  *pion_p + (-0.00336795)  *pow(pion_p,2) + (0.00111193)   *pow(pion_p,3) + (0) *pow(pion_p,4);}
            if(pip_theta > 31 && pip_theta < 32 && pion_p >= 1.8){    dp_pion =  0.00450241 + (0.00248969)  *1.8    + (-0.00336795)  *pow(1.8,2)    + (0.00111193)   *pow(1.8,3)    + (0) *pow(1.8,4);}
            if(pip_theta > 32 && pip_theta < 33){                     dp_pion =  0.00505593 + (-0.00246203) *pion_p + (0.00172984)   *pow(pion_p,2) + (-0.000406701) *pow(pion_p,3) + (0) *pow(pion_p,4);}
            if(pip_theta > 32 && pip_theta < 33 && pion_p >= 1.8){    dp_pion =  0.00505593 + (-0.00246203) *1.8    + (0.00172984)   *pow(1.8,2)    + (-0.000406701) *pow(1.8,3)    + (0) *pow(1.8,4);}
            if(pip_theta > 33 && pip_theta < 34){                     dp_pion =  0.00273402 + (0.00440449)  *pion_p + (-0.00373488)  *pow(pion_p,2) + (0.000996612)  *pow(pion_p,3) + (0) *pow(pion_p,4);}
            if(pip_theta > 33 && pip_theta < 34 && pion_p >= 1.8){    dp_pion =  0.00273402 + (0.00440449)  *1.8    + (-0.00373488)  *pow(1.8,2)    + (0.000996612)  *pow(1.8,3)    + (0) *pow(1.8,4);}
            if(pip_theta > 34 && pip_theta < 35){                     dp_pion =  0.00333542 + (0.00439874)  *pion_p + (-0.00397776)  *pow(pion_p,2) + (0.00105586)   *pow(pion_p,3) + (0) *pow(pion_p,4);}
            if(pip_theta > 34 && pip_theta < 35 && pion_p >= 1.8){    dp_pion =  0.00333542 + (0.00439874)  *1.8    + (-0.00397776)  *pow(1.8,2)    + (0.00105586)   *pow(1.8,3)    + (0) *pow(1.8,4);}
            if(pip_theta > 35 && pip_theta < 36){                     dp_pion =  0.00354663 + (0.00565397)  *pion_p + (-0.00513503)  *pow(pion_p,2) + (0.00153346)   *pow(pion_p,3) + (0) *pow(pion_p,4);}
            if(pip_theta > 35 && pip_theta < 36 && pion_p >= 1.8){    dp_pion =  0.00354663 + (0.00565397)  *1.8    + (-0.00513503)  *pow(1.8,2)    + (0.00153346)   *pow(1.8,3)    + (0) *pow(1.8,4);}
            if(pip_theta > 36 && pip_theta < 37){                     dp_pion =  0.00333909 + (0.00842367)  *pion_p + (-0.0077321)   *pow(pion_p,2) + (0.0022489)    *pow(pion_p,3) + (0) *pow(pion_p,4);}
            if(pip_theta > 36 && pip_theta < 37 && pion_p >= 1.8){    dp_pion =  0.00333909 + (0.00842367)  *1.8    + (-0.0077321)   *pow(1.8,2)    + (0.0022489)    *pow(1.8,3)    + (0) *pow(1.8,4);}
            if(pip_theta > 37 && pip_theta < 38){                     dp_pion =  0.00358828 + (0.0112108)   *pion_p + (-0.0133854)   *pow(pion_p,2) + (0.00486924)   *pow(pion_p,3) + (0) *pow(pion_p,4);}
            if(pip_theta > 37 && pip_theta < 38 && pion_p >= 1.4){    dp_pion =  0.00358828 + (0.0112108)   *1.4    + (-0.0133854)   *pow(1.4,2)    + (0.00486924)   *pow(1.4,3)    + (0) *pow(1.4,4);}
            if(pip_theta > 38 && pip_theta < 39){                     dp_pion =  0.00354343 + (0.0117121)   *pion_p + (-0.0129649)   *pow(pion_p,2) + (0.00455602)   *pow(pion_p,3) + (0) *pow(pion_p,4);}
            if(pip_theta > 38 && pip_theta < 39 && pion_p >= 1.3){    dp_pion =  0.00354343 + (0.0117121)   *1.3    + (-0.0129649)   *pow(1.3,2)    + (0.00455602)   *pow(1.3,3)    + (0) *pow(1.3,4);}
            if(pip_theta > 39 && pip_theta < 40){                     dp_pion = -0.00194951 + (0.0409713)   *pion_p + (-0.0595861)   *pow(pion_p,2) + (0.0281588)    *pow(pion_p,3) + (0) *pow(pion_p,4);}
            if(pip_theta > 39 && pip_theta < 40 && pion_p >= 0.9){    dp_pion = -0.00194951 + (0.0409713)   *0.9    + (-0.0595861)   *pow(0.9,2)    + (0.0281588)    *pow(0.9,3)    + (0) *pow(0.9,4);}
            if(pip_theta > 40 && pip_theta < 41){                     dp_pion = -0.0099217  + (0.0808096)   *pion_p + (-0.119836)    *pow(pion_p,2) + (0.0559553)    *pow(pion_p,3) + (0) *pow(pion_p,4);}
            if(pip_theta > 40 && pip_theta < 41 && pion_p >= 0.75){   dp_pion = -0.0099217  + (0.0808096)   *0.75   + (-0.119836)    *pow(0.75,2)   + (0.0559553)    *pow(0.75,3)   + (0) *pow(0.75,4);}
            if(pip_theta > 41 && pip_theta < 42){                     dp_pion =  0.00854898 + (0.00025037)  *pion_p + (-0.0113992)   *pow(pion_p,2) + (0.0145178)    *pow(pion_p,3) + (0) *pow(pion_p,4);}
            if(pip_theta > 41 && pip_theta < 42 && pion_p >= 0.65){   dp_pion =  0.00854898 + (0.00025037)  *0.65   + (-0.0113992)   *pow(0.65,2)   + (0.0145178)    *pow(0.65,3)   + (0) *pow(0.65,4);}
            if(pip_theta > 42){                                       dp_pion =  0.00564818 + (0.00706606)  *pion_p + (0.0042602)    *pow(pion_p,2) + (-0.01141)     *pow(pion_p,3) + (0) *pow(pion_p,4);}
            if(pip_theta > 42 && pion_p >= 0.65){                     dp_pion =  0.00564818 + (0.00706606)  *0.65   + (0.0042602)    *pow(0.65,2)   + (-0.01141)     *pow(0.65,3)   + (0) *pow(0.65,4);}
        }
        if(pion_det == 3){  // Central Detector
            if(pip_theta < 39){                                       dp_pion = -0.045      + (-0.102652) + (0.455589) *pion_p + (-0.671635)   *pow(pion_p,2) + (0.303814)   *pow(pion_p,3);}
            if(pip_theta < 39  && pion_p >= 0.7){                     dp_pion = -0.045      + (-0.102652) + (0.455589) *0.7    + (-0.671635)   *pow(0.7,2)    + (0.303814)   *pow(0.7,3);}
            if(pip_theta > 39  && pip_theta < 40){                    dp_pion =  0.0684552  + (-0.766492)              *pion_p + (1.73092)     *pow(pion_p,2) + (-1.46215)   *pow(pion_p,3) + (0.420127) *pow(pion_p,4);}
            if(pip_theta > 39  && pip_theta < 40 && pion_p >= 1.4){   dp_pion =  0.0684552  + (-0.766492)              *1.4    + (1.73092)     *pow(1.4,2)    + (-1.46215)   *pow(1.4,3)    + (0.420127) *pow(1.4,4);}
            if(pip_theta > 40  && pip_theta < 41){                    dp_pion =  0.751549   + (-7.4593)                *pion_p + (26.8037)     *pow(pion_p,2) + (-47.1576)   *pow(pion_p,3) + (43.8527)  *pow(pion_p,4) + (-20.7039) *pow(pion_p,5) + (3.90931)  *pow(pion_p,6);}
            if(pip_theta > 40  && pip_theta < 41 && pion_p >= 1.45){  dp_pion =  0.751549   + (-7.4593)                *1.45   + (26.8037)     *pow(1.45,2)   + (-47.1576)   *pow(1.45,3)   + (43.8527)  *pow(1.45,4)   + (-20.7039) *pow(1.45,5)   + (3.90931)  *pow(1.45,6);}
            if(pip_theta > 41  && pip_theta < 42){                    dp_pion = -1.35043    + (10.0788)                *pion_p + (-30.4829)    *pow(pion_p,2) + (47.7792)    *pow(pion_p,3) + (-40.996)  *pow(pion_p,4) + (18.2662)  *pow(pion_p,5) + (-3.30449) *pow(pion_p,6);}
            if(pip_theta > 41  && pip_theta < 42 && pion_p >= 1.2){   dp_pion = -1.35043    + (10.0788)                *1.2    + (-30.4829)    *pow(1.2,2)    + (47.7792)    *pow(1.2,3)    + (-40.996)  *pow(1.2,4)    + (18.2662)  *pow(1.2,5)    + (-3.30449) *pow(1.2,6);}
            if(pip_theta > 42  && pip_theta < 43){                    dp_pion = -0.0231195  + (0.0744589)              *pion_p + (-0.0807029)  *pow(pion_p,2) + (0.0264266)  *pow(pion_p,3) + (0)        *pow(pion_p,4);}
            if(pip_theta > 42  && pip_theta < 43 && pion_p >= 1.3){   dp_pion = -0.0231195  + (0.0744589)              *1.3    + (-0.0807029)  *pow(1.3,2)    + (0.0264266)  *pow(1.3,3)    + (0)        *pow(1.3,4);}
            if(pip_theta > 43  && pip_theta < 44){                    dp_pion = -0.00979928 + (0.0351043)              *pion_p + (-0.0365865)  *pow(pion_p,2) + (0.00977218) *pow(pion_p,3) + (0)        *pow(pion_p,4);}
            if(pip_theta > 43  && pip_theta < 44 && pion_p >= 1.1){   dp_pion = -0.00979928 + (0.0351043)              *1.1    + (-0.0365865)  *pow(1.1,2)    + (0.00977218) *pow(1.1,3)    + (0)        *pow(1.1,4);}
            if(pip_theta > 44  && pip_theta < 45){                    dp_pion =  0.00108491 + (-0.00924885)            *pion_p + (0.0216431)   *pow(pion_p,2) + (-0.0137762) *pow(pion_p,3) + (0)        *pow(pion_p,4);}
            if(pip_theta > 44  && pip_theta < 45 && pion_p >= 1.1){   dp_pion =  0.00108491 + (-0.00924885)            *1.1    + (0.0216431)   *pow(1.1,2)    + (-0.0137762) *pow(1.1,3)    + (0)        *pow(1.1,4);}
            if(pip_theta > 45  && pip_theta < 55){                    dp_pion =  0.0092263  + (-0.0676178)             *pion_p + (0.168778)    *pow(pion_p,2) + (-0.167463)  *pow(pion_p,3) + (0.05661)  *pow(pion_p,4);}
            if(pip_theta > 45  && pip_theta < 55 && pion_p >= 1.3){   dp_pion =  0.0092263  + (-0.0676178)             *1.3    + (0.168778)    *pow(1.3,2)    + (-0.167463)  *pow(1.3,3)    + (0.05661)  *pow(1.3,4);}
            if(pip_theta > 55  && pip_theta < 65){                    dp_pion =  0.00805642 + (-0.0670962)             *pion_p + (0.188536)    *pow(pion_p,2) + (-0.20571)   *pow(pion_p,3) + (0.0765)   *pow(pion_p,4);}
            if(pip_theta > 55  && pip_theta < 65 && pion_p >= 1.05){  dp_pion =  0.00805642 + (-0.0670962)             *1.05   + (0.188536)    *pow(1.05,2)   + (-0.20571)   *pow(1.05,3)   + (0.0765)   *pow(1.05,4);}
            if(pip_theta > 65  && pip_theta < 75){                    dp_pion =  0.00312202 + (-0.0269717)             *pion_p + (0.0715236)   *pow(pion_p,2) + (-0.0545622) *pow(pion_p,3) + (0)        *pow(pion_p,4);}
            if(pip_theta > 65  && pip_theta < 75 && pion_p >= 0.75){  dp_pion =  0.00312202 + (-0.0269717)             *0.75   + (0.0715236)   *pow(0.75,2)   + (-0.0545622) *pow(0.75,3)   + (0)        *pow(0.75,4);}
            if(pip_theta > 75  && pip_theta < 85){                    dp_pion =  0.00424971 + (-0.0367683)             *pion_p + (0.10417)     *pow(pion_p,2) + (-0.0899651) *pow(pion_p,3) + (0)        *pow(pion_p,4);}
            if(pip_theta > 75  && pip_theta < 85 && pion_p >= 0.65){  dp_pion =  0.00424971 + (-0.0367683)             *0.65   + (0.10417)     *pow(0.65,2)   + (-0.0899651) *pow(0.65,3)   + (0)        *pow(0.65,4);}
            if(pip_theta > 85  && pip_theta < 95){                    dp_pion =  0.00654123 + (-0.0517915)             *pion_p + (0.147888)    *pow(pion_p,2) + (-0.14253)   *pow(pion_p,3) + (0)        *pow(pion_p,4);}
            if(pip_theta > 85  && pip_theta < 95 && pion_p >= 0.5){   dp_pion =  0.00654123 + (-0.0517915)             *0.5    + (0.147888)    *pow(0.5,2)    + (-0.14253)   *pow(0.5,3)    + (0)        *pow(0.5,4);}
            if(pip_theta > 95  && pip_theta < 105){                   dp_pion = -0.00111721 + (0.00478119)             *pion_p + (0.0158753)   *pow(pion_p,2) + (-0.052902)  *pow(pion_p,3) + (0)        *pow(pion_p,4);}
            if(pip_theta > 95  && pip_theta < 105 && pion_p >= 0.45){ dp_pion = -0.00111721 + (0.00478119)             *0.45   + (0.0158753)   *pow(0.45,2)   + (-0.052902)  *pow(0.45,3)   + (0)        *pow(0.45,4);}
            if(pip_theta > 105 && pip_theta < 115){                   dp_pion = -0.00239839 + (0.00790738)             *pion_p + (0.0311713)   *pow(pion_p,2) + (-0.104157)  *pow(pion_p,3) + (0)        *pow(pion_p,4);}
            if(pip_theta > 105 && pip_theta < 115 && pion_p >= 0.35){ dp_pion = -0.00239839 + (0.00790738)             *0.35   + (0.0311713)   *pow(0.35,2)   + (-0.104157)  *pow(0.35,3)   + (0)        *pow(0.35,4);}
            if(pip_theta > 115 && pip_theta < 125){                   dp_pion = -0.00778793 + (0.0256774)              *pion_p + (0.0932503)   *pow(pion_p,2) + (-0.32771)   *pow(pion_p,3) + (0)        *pow(pion_p,4);}
            if(pip_theta > 115 && pip_theta < 125 && pion_p >= 0.35){ dp_pion = -0.00778793 + (0.0256774)              *0.35   + (0.0932503)   *pow(0.35,2)   + (-0.32771)   *pow(0.35,3)   + (0)        *pow(0.35,4);}
            if(pip_theta > 125 && pip_theta < 135){                   dp_pion = -0.00292778 + (-0.00536697)            *pion_p + (-0.00414351) *pow(pion_p,2) + (0.0196431)  *pow(pion_p,3) + (0)        *pow(pion_p,4);}
            if(pip_theta > 125 && pip_theta < 135 && pion_p >= 0.35){ dp_pion = -0.00292778 + (-0.00536697)            *0.35   + (-0.00414351) *pow(0.35,2)   + (0.0196431)  *pow(0.35,3)   + (0)        *pow(0.35,4);}
        }
    }
    if(outbending == true){ // OUTBENDING
        if(pion_det == 2){  // Forward Detector
            if(pip_theta < 27){                                       dp_pion = 0.00389945  + (-0.004062)    *pion_p + (0.00321842)  *pow(pion_p,2) + (-0.000698299) *pow(pion_p,3) + (0)          *pow(pion_p,4);}
            if(pip_theta < 27 && pion_p >= 2.3){                      dp_pion = 0.00389945  + (-0.004062)    *2.3    + (0.00321842)  *pow(2.3,2)    + (-0.000698299) *pow(2.3,3)    + (0)          *pow(2.3,4);}
            if(pip_theta > 27 && pip_theta < 28){                     dp_pion = 0.00727132  + (-0.0117989)   *pion_p + (0.00962999)  *pow(pion_p,2) + (-0.00267005)  *pow(pion_p,3) + (0)          *pow(pion_p,4);}
            if(pip_theta > 27 && pip_theta < 28 && pion_p >= 1.7){    dp_pion = 0.00727132  + (-0.0117989)   *1.7    + (0.00962999)  *pow(1.7,2)    + (-0.00267005)  *pow(1.7,3)    + (0)          *pow(1.7,4);}
            if(pip_theta > 28 && pip_theta < 29){                     dp_pion = 0.00844551  + (-0.0128097)   *pion_p + (0.00945956)  *pow(pion_p,2) + (-0.00237992)  *pow(pion_p,3) + (0)          *pow(pion_p,4);}
            if(pip_theta > 28 && pip_theta < 29 && pion_p >= 2){      dp_pion = 0.00844551  + (-0.0128097)   *2      + (0.00945956)  *pow(2,2)      + (-0.00237992)  *pow(2,3)      + (0)          *pow(2,4);}
            if(pip_theta > 29 && pip_theta < 30){                     dp_pion = 0.00959007  + (-0.0139218)   *pion_p + (0.0122966)   *pow(pion_p,2) + (-0.0034012)   *pow(pion_p,3) + (0)          *pow(pion_p,4);}
            if(pip_theta > 29 && pip_theta < 30 && pion_p >= 1.9){    dp_pion = 0.00959007  + (-0.0139218)   *1.9    + (0.0122966)   *pow(1.9,2)    + (-0.0034012)   *pow(1.9,3)    + (0)          *pow(1.9,4);}
            if(pip_theta > 30 && pip_theta < 31){                     dp_pion = 0.00542816  + (-5.10739e-05) *pion_p + (0.000572038) *pow(pion_p,2) + (-0.000488883) *pow(pion_p,3) + (0)          *pow(pion_p,4);}
            if(pip_theta > 30 && pip_theta < 31 && pion_p >= 1.9){    dp_pion = 0.00542816  + (-5.10739e-05) *1.9    + (0.000572038) *pow(1.9,2)    + (-0.000488883) *pow(1.9,3)    + (0)          *pow(1.9,4);}
            if(pip_theta > 31 && pip_theta < 32){                     dp_pion = 0.0060391   + (-0.000516936) *pion_p + (-0.00286595) *pow(pion_p,2) + (0.00136604)   *pow(pion_p,3) + (0)          *pow(pion_p,4);}
            if(pip_theta > 31 && pip_theta < 32 && pion_p >= 1.8){    dp_pion = 0.0060391   + (-0.000516936) *1.8    + (-0.00286595) *pow(1.8,2)    + (0.00136604)   *pow(1.8,3)    + (0)          *pow(1.8,4);}
            if(pip_theta > 32 && pip_theta < 33){                     dp_pion = 0.0140305   + (-0.0285832)   *pion_p + (0.0248799)   *pow(pion_p,2) + (-0.00701311)  *pow(pion_p,3) + (0)          *pow(pion_p,4);}
            if(pip_theta > 32 && pip_theta < 33 && pion_p >= 1.6){    dp_pion = 0.0140305   + (-0.0285832)   *1.6    + (0.0248799)   *pow(1.6,2)    + (-0.00701311)  *pow(1.6,3)    + (0)          *pow(1.6,4);}
            if(pip_theta > 33 && pip_theta < 34){                     dp_pion = 0.010815    + (-0.0194244)   *pion_p + (0.0174474)   *pow(pion_p,2) + (-0.0049764)   *pow(pion_p,3) + (0)          *pow(pion_p,4);}
            if(pip_theta > 33 && pip_theta < 34 && pion_p >= 1.5){    dp_pion = 0.010815    + (-0.0194244)   *1.5    + (0.0174474)   *pow(1.5,2)    + (-0.0049764)   *pow(1.5,3)    + (0)          *pow(1.5,4);}
            if(pip_theta > 34 && pip_theta < 35){                     dp_pion = 0.0105522   + (-0.0176248)   *pion_p + (0.0161142)   *pow(pion_p,2) + (-0.00472288)  *pow(pion_p,3) + (0)          *pow(pion_p,4);}
            if(pip_theta > 34 && pip_theta < 35 && pion_p >= 1.6){    dp_pion = 0.0105522   + (-0.0176248)   *1.6    + (0.0161142)   *pow(1.6,2)    + (-0.00472288)  *pow(1.6,3)    + (0)          *pow(1.6,4);}
            if(pip_theta > 35 && pip_theta < 36){                     dp_pion = 0.0103938   + (-0.0164003)   *pion_p + (0.0164045)   *pow(pion_p,2) + (-0.00517012)  *pow(pion_p,3) + (0)          *pow(pion_p,4);}
            if(pip_theta > 35 && pip_theta < 36 && pion_p >= 1.5){    dp_pion = 0.0103938   + (-0.0164003)   *1.5    + (0.0164045)   *pow(1.5,2)    + (-0.00517012)  *pow(1.5,3)    + (0)          *pow(1.5,4);}
            if(pip_theta > 36 && pip_theta < 37){                     dp_pion = 0.0441471   + (-0.183937)    *pion_p + (0.338784)    *pow(pion_p,2) + (-0.298985)    *pow(pion_p,3) + (0.126905)   *pow(pion_p,4) + (-0.0208286) *pow(pion_p,5);}
            if(pip_theta > 36 && pip_theta < 37 && pion_p >= 1.8){    dp_pion = 0.0441471   + (-0.183937)    *1.8    + (0.338784)    *pow(1.8,2)    + (-0.298985)    *pow(1.8,3)    + (0.126905)   *pow(1.8,4)    + (-0.0208286) *pow(1.8,5);}
            if(pip_theta > 37 && pip_theta < 38){                     dp_pion = 0.0726119   + (-0.345004)    *pion_p + (0.697789)    *pow(pion_p,2) + (-0.685948)    *pow(pion_p,3) + (0.327195)   *pow(pion_p,4) + (-0.0605621) *pow(pion_p,5);}
            if(pip_theta > 37 && pip_theta < 38 && pion_p >= 1.7){    dp_pion = 0.0726119   + (-0.345004)    *1.7    + (0.697789)    *pow(1.7,2)    + (-0.685948)    *pow(1.7,3)    + (0.327195)   *pow(1.7,4)    + (-0.0605621) *pow(1.7,5);}
            if(pip_theta > 38 && pip_theta < 39){                     dp_pion = 0.0247648   + (-0.0797376)   *pion_p + (0.126535)    *pow(pion_p,2) + (-0.086545)    *pow(pion_p,3) + (0.0219304)  *pow(pion_p,4);}
            if(pip_theta > 38 && pip_theta < 39 && pion_p >= 1.6){    dp_pion = 0.0247648   + (-0.0797376)   *1.6    + (0.126535)    *pow(1.6,2)    + (-0.086545)    *pow(1.6,3)    + (0.0219304)  *pow(1.6,4);}
            if(pip_theta > 39 && pip_theta < 40){                     dp_pion = 0.0208867   + (-0.0492068)   *pion_p + (0.0543187)   *pow(pion_p,2) + (-0.0183393)   *pow(pion_p,3) + (0)          *pow(pion_p,4);}
            if(pip_theta > 39 && pip_theta < 40 && pion_p >= 1.2){    dp_pion = 0.0208867   + (-0.0492068)   *1.2    + (0.0543187)   *pow(1.2,2)    + (-0.0183393)   *pow(1.2,3)    + (0)          *pow(1.2,4);}
            if(pip_theta > 40 && pip_theta < 41){                     dp_pion = 0.0148655   + (-0.0203483)   *pion_p + (0.00835867)  *pow(pion_p,2) + (0.00697134)   *pow(pion_p,3) + (0)          *pow(pion_p,4);}
            if(pip_theta > 40 && pip_theta < 41 && pion_p >= 1.0){    dp_pion = 0.0148655   + (-0.0203483)   *1.0    + (0.00835867)  *pow(1.0,2)    + (0.00697134)   *pow(1.0,3)    + (0)          *pow(1.0,4);}
            if(pip_theta > 41 && pip_theta < 42){                     dp_pion = 0.0223585   + (-0.0365262)   *pion_p + (-0.0150027)  *pow(pion_p,2) + (0.0854164)    *pow(pion_p,3) + (-0.0462718) *pow(pion_p,4);}
            if(pip_theta > 41 && pip_theta < 42 && pion_p >= 0.7){    dp_pion = 0.007617;}
            if(pip_theta > 42){                                       dp_pion = 0.0152373   + (-0.0106377)   *pion_p + (-0.0257573)  *pow(pion_p,2) + (0.0344851)    *pow(pion_p,3) + (0)          *pow(pion_p,4);}
            if(pip_theta > 42 && pion_p >= 0.75){                     dp_pion = 0.0152373   + (-0.0106377)   *0.75   + (-0.0257573)  *pow(0.75,2)   + (0.0344851)    *pow(0.75,3)   + (0)          *pow(0.75,4);}
        }
        if(pion_det == 3){ // Central Detector
            if(pip_theta < 39){                                       dp_pion = -0.05        + (-0.0758897) + (0.362231) *pion_p + (-0.542404)   *pow(pion_p,2) + (0.241344)   *pow(pion_p,3);}
            if(pip_theta < 39  && pion_p >= 0.8){                     dp_pion = -0.05        + (-0.0758897) + (0.362231) *0.8    + (-0.542404)   *pow(0.8,2)    + (0.241344)   *pow(0.8,3);}
            if(pip_theta > 39  && pip_theta < 40){                    dp_pion =  0.0355259   + (-0.589712)               *pion_p + (1.4206)      *pow(pion_p,2) + (-1.24179)   *pow(pion_p,3) + (0.365524)  *pow(pion_p,4);}
            if(pip_theta > 39  && pip_theta < 40  && pion_p >= 1.35){ dp_pion =  0.0355259   + (-0.589712)               *1.35   + (1.4206)      *pow(1.35,2)   + (-1.24179)   *pow(1.35,3)   + (0.365524)  *pow(1.35,4);}
            if(pip_theta > 40  && pip_theta < 41){                    dp_pion = -0.252336    + (1.02032)                 *pion_p + (-1.51461)    *pow(pion_p,2) + (0.967772)   *pow(pion_p,3) + (-0.226028) *pow(pion_p,4);}
            if(pip_theta > 40  && pip_theta < 41  && pion_p >= 1.4){  dp_pion = -0.252336    + (1.02032)                 *1.4    + (-1.51461)    *pow(1.4,2)    + (0.967772)   *pow(1.4,3)    + (-0.226028) *pow(1.4,4);}
            if(pip_theta > 41  && pip_theta < 42){                    dp_pion = -0.710129    + (4.49613)                 *pion_p + (-11.01)      *pow(pion_p,2) + (12.9945)    *pow(pion_p,3) + (-7.41641)  *pow(pion_p,4) + (1.63923)   *pow(pion_p,5);}
            if(pip_theta > 41  && pip_theta < 42  && pion_p >= 1.2){  dp_pion = -0.710129    + (4.49613)                 *1.2    + (-11.01)      *pow(1.2,2)    + (12.9945)    *pow(1.2,3)    + (-7.41641)  *pow(1.2,4)    + (1.63923)   *pow(1.2,5);}
            if(pip_theta > 42  && pip_theta < 43){                    dp_pion = -0.0254912   + (0.0851432)               *pion_p + (-0.0968583)  *pow(pion_p,2) + (0.0350334)  *pow(pion_p,3) + (0)         *pow(pion_p,4);}
            if(pip_theta > 42  && pip_theta < 43  && pion_p >= 1.2){  dp_pion = -0.0254912   + (0.0851432)               *1.2    + (-0.0968583)  *pow(1.2,2)    + (0.0350334)  *pow(1.2,3)    + (0)         *pow(1.2,4);}
            if(pip_theta > 43  && pip_theta < 44){                    dp_pion = -0.0115965   + (0.0438726)               *pion_p + (-0.0500474)  *pow(pion_p,2) + (0.0163627)  *pow(pion_p,3) + (0)         *pow(pion_p,4);}
            if(pip_theta > 43  && pip_theta < 44  && pion_p >= 1.4){  dp_pion = -0.0115965   + (0.0438726)               *1.4    + (-0.0500474)  *pow(1.4,2)    + (0.0163627)  *pow(1.4,3)    + (0)         *pow(1.4,4);}
            if(pip_theta > 44  && pip_theta < 45){                    dp_pion =  0.00273414  + (-0.01851)                *pion_p + (0.0377032)   *pow(pion_p,2) + (-0.0226696) *pow(pion_p,3) + (0)         *pow(pion_p,4);}
            if(pip_theta > 44  && pip_theta < 45  && pion_p >= 1){    dp_pion =  0.00273414  + (-0.01851)                *1      + (0.0377032)   *pow(1,2)      + (-0.0226696) *pow(1,3)      + (0)         *pow(1,4);}
            if(pip_theta > 45  && pip_theta < 55){                    dp_pion =  0.0271952   + (-0.25981)                *pion_p + (0.960051)    *pow(pion_p,2) + (-1.76651)   *pow(pion_p,3) + (1.72872)   *pow(pion_p,4) + (-0.856946) *pow(pion_p,5) + (0.167564) *pow(pion_p,6);}
            if(pip_theta > 45  && pip_theta < 55  && pion_p >= 1.4){  dp_pion =  0.0271952   + (-0.25981)                *1.4    + (0.960051)    *pow(1.4,2)    + (-1.76651)   *pow(1.4,3)    + (1.72872)   *pow(1.4,4)    + (-0.856946) *pow(1.4,5)    + (0.167564) *pow(1.4,6);}
            if(pip_theta > 55  && pip_theta < 65){                    dp_pion =  0.00734975  + (-0.0598841)              *pion_p + (0.161495)    *pow(pion_p,2) + (-0.1629)    *pow(pion_p,3) + (0.0530098) *pow(pion_p,4);}
            if(pip_theta > 55  && pip_theta < 65  && pion_p >= 1.2){  dp_pion =  0.00734975  + (-0.0598841)              *1.2    + (0.161495)    *pow(1.2,2)    + (-0.1629)    *pow(1.2,3)    + (0.0530098) *pow(1.2,4);}
            if(pip_theta > 65  && pip_theta < 75){                    dp_pion =  0.00321351  + (-0.0289322)              *pion_p + (0.0786484)   *pow(pion_p,2) + (-0.0607041) *pow(pion_p,3) + (0)         *pow(pion_p,4);}
            if(pip_theta > 65  && pip_theta < 75  && pion_p >= 0.95){ dp_pion =  0.00321351  + (-0.0289322)              *0.95   + (0.0786484)   *pow(0.95,2)   + (-0.0607041) *pow(0.95,3)   + (0)         *pow(0.95,4);}
            if(pip_theta > 75  && pip_theta < 85){                    dp_pion =  0.00644253  + (-0.0543896)              *pion_p + (0.148933)    *pow(pion_p,2) + (-0.1256)    *pow(pion_p,3) + (0)         *pow(pion_p,4);}
            if(pip_theta > 75  && pip_theta < 85  && pion_p >= 0.7){  dp_pion =  0.00644253  + (-0.0543896)              *0.7    + (0.148933)    *pow(0.7,2)    + (-0.1256)    *pow(0.7,3)    + (0)         *pow(0.7,4);}
            if(pip_theta > 85  && pip_theta < 95){                    dp_pion =  0.00671152  + (-0.0537269)              *pion_p + (0.154509)    *pow(pion_p,2) + (-0.147667)  *pow(pion_p,3) + (0)         *pow(pion_p,4);}
            if(pip_theta > 85  && pip_theta < 95  && pion_p >= 0.65){ dp_pion =  0.00671152  + (-0.0537269)              *0.65   + (0.154509)    *pow(0.65,2)   + (-0.147667)  *pow(0.65,3)   + (0)         *pow(0.65,4);}
            if(pip_theta > 95  && pip_theta < 105){                   dp_pion = -0.000709077 + (0.00331818)              *pion_p + (0.0109241)   *pow(pion_p,2) + (-0.0351682) *pow(pion_p,3) + (0)         *pow(pion_p,4);}
            if(pip_theta > 95  && pip_theta < 105 && pion_p >= 0.45){ dp_pion = -0.000709077 + (0.00331818)              *0.45   + (0.0109241)   *pow(0.45,2)   + (-0.0351682) *pow(0.45,3)   + (0)         *pow(0.45,4);}
            if(pip_theta > 105 && pip_theta < 115){                   dp_pion = -0.00260164  + (0.00846919)              *pion_p + (0.0315497)   *pow(pion_p,2) + (-0.105756)  *pow(pion_p,3) + (0)         *pow(pion_p,4);}
            if(pip_theta > 105 && pip_theta < 115 && pion_p >= 0.45){ dp_pion = -0.00260164  + (0.00846919)              *0.45   + (0.0315497)   *pow(0.45,2)   + (-0.105756)  *pow(0.45,3)   + (0)         *pow(0.45,4);}
            if(pip_theta > 115 && pip_theta < 125){                   dp_pion = -0.00544336  + (0.018256)                *pion_p + (0.0664618)   *pow(pion_p,2) + (-0.240312)  *pow(pion_p,3) + (0)         *pow(pion_p,4);}
            if(pip_theta > 115 && pip_theta < 125 && pion_p >= 0.45){ dp_pion = -0.00544336  + (0.018256)                *0.45   + (0.0664618)   *pow(0.45,2)   + (-0.240312)  *pow(0.45,3)   + (0)         *pow(0.45,4);}
            if(pip_theta > 125 && pip_theta < 135){                   dp_pion = -0.00281073  + (-0.00495863)             *pion_p + (-0.00362356) *pow(pion_p,2) + (0.0178764)  *pow(pion_p,3) + (0)         *pow(pion_p,4);}
            if(pip_theta > 125 && pip_theta < 135 && pion_p >= 0.35){ dp_pion = -0.00281073  + (-0.00495863)             *0.35   + (-0.00362356) *pow(0.35,2)   + (0.0178764)  *pow(0.35,3)   + (0)         *pow(0.35,4);}
        }
    }

    return dp_pion;
};"""









###########################################################################################################################################################################
###########################################################################################################################################################################
###########################################################################################################################################################################
###########################################################################################################################################################################
###########################################################################################################################################################################









# Up-to-date as of: 4/12/2024
def smearing_function_SF(smear_factor=0.75, Use_Pass_2_Function=False):
    if(Use_Pass_2_Function):
        smearing_function = "".join(["""
        //=======================================================================//
        //=================// Sigma Smearing Factor (Pass 2) //==================//
        //=======================================================================//
        auto smear_func = [&](TLorentzVector V4, int ivec){
            // True generated values (i.e., values of the unsmeared TLorentzVector)
            double M_rec   = V4.M();
            double P_rec   = V4.P();
            double Th_rec  = V4.Theta();
            double Phi_rec = V4.Phi();
            
            double Smear_SF_Theta = 0;
            // if(ivec == 0){ // Electron
            //     Smear_SF_Theta = (2.9693e-05)*(TMath::RadToDeg()*Th_rec)*(TMath::RadToDeg()*Th_rec) + (-1.3409e-03)*(TMath::RadToDeg()*Th_rec) + (0.01712);
            //     if(Smear_SF_Theta < 0){Smear_SF_Theta = 0;}
            // }
            // if(ivec == 1){ // Pi+ Pion
            //     Smear_SF_Theta = (2.4652e-05)*(TMath::RadToDeg()*Th_rec)*(TMath::RadToDeg()*Th_rec) + (-3.0371e-04)*(TMath::RadToDeg()*Th_rec) + (4.3560e-04);
            //     if(Smear_SF_Theta < 0){Smear_SF_Theta = 0;}
            // }
            // if(ivec == 0){ // Electron
            //     Smear_SF_Theta = (-5.4842e-05)*(TMath::RadToDeg()*Th_rec)*(TMath::RadToDeg()*Th_rec) + (2.1920e-03)*(TMath::RadToDeg()*Th_rec) + (-8.6631e-03);
            //     if(Smear_SF_Theta < 0){Smear_SF_Theta = 0;}
            // }
            // if(ivec == 0){ // Electron
            //     // Smear_SF_Theta = (-3.6737e-05)*(TMath::RadToDeg()*Th_rec)*(TMath::RadToDeg()*Th_rec) + (1.2103e-03)*(TMath::RadToDeg()*Th_rec) + (-2.6782e-03);
            //     // Smear_SF_Theta = (-4.3310e-05)*(TMath::RadToDeg()*Th_rec)*(TMath::RadToDeg()*Th_rec) + (1.4627e-03)*(TMath::RadToDeg()*Th_rec) + (-5.2904e-03);
            //     Smear_SF_Theta = (-4.0439e-05)*(TMath::RadToDeg()*Th_rec)*(TMath::RadToDeg()*Th_rec) + (1.3799e-03)*(TMath::RadToDeg()*Th_rec) + (-4.6519e-03);
            //     Smear_SF_Theta = 0.5*Smear_SF_Theta;
            //     if(Smear_SF_Theta < 0){Smear_SF_Theta = 0;}
            // }
            // if(ivec == 1){ // Pi+ Pion
            //     Smear_SF_Theta = (4.0905e-06)*(TMath::RadToDeg()*Th_rec)*(TMath::RadToDeg()*Th_rec) + (2.0371e-04)*(TMath::RadToDeg()*Th_rec) + (0.01161);
            //     if(Smear_SF_Theta < 0){Smear_SF_Theta = 0;}
            // }
            // if(ivec == 1){ // Pi+ Pion
            //     Smear_SF_Theta = (-1.2573e-05)*(TMath::RadToDeg()*Th_rec)*(TMath::RadToDeg()*Th_rec) + (1.7345e-03)*(TMath::RadToDeg()*Th_rec) + (-0.01872);
            //     if(Smear_SF_Theta < 0){Smear_SF_Theta = 0;}
            // }
            if(ivec == 1){ // Pi+ Pion
                Smear_SF_Theta = (-1.6512e-05)*(TMath::RadToDeg()*Th_rec)*(TMath::RadToDeg()*Th_rec) + (1.6159e-03)*(TMath::RadToDeg()*Th_rec) + (-0.01402);
                if(Smear_SF_Theta < 0){Smear_SF_Theta = 0;}
            }
            if(ivec == 0){ // Electron
                Smear_SF_Theta = (-7.6697e-05)*(TMath::RadToDeg()*Th_rec)*(TMath::RadToDeg()*Th_rec) + (2.7102e-03)*(TMath::RadToDeg()*Th_rec) + (-0.01402);
                Smear_SF_Theta = 0.65*Smear_SF_Theta;
                if(Smear_SF_Theta < 0){Smear_SF_Theta = 0;}
            }
            
            
            // Calculate resolutions
            double smear_factor = """, str(smear_factor), """;
            // double P_new_rec    = P_rec   +   (P_rec)*Smear_SF_Theta*smear_factor*(gRandom->Gaus(0,1));
            // double Th_new_rec   = Th_rec  +  (Th_rec)*Smear_SF_Theta*smear_factor*(gRandom->Gaus(0,1));
            // double Phi_new_rec  = Phi_rec + (Phi_rec)*Smear_SF_Theta*smear_factor*(gRandom->Gaus(0,1));
            
            double P_new_rec   = P_rec   + gRandom->Gaus(0,   (P_rec)*Smear_SF_Theta*smear_factor);
            // double Th_new_rec  = Th_rec  + gRandom->Gaus(0,  (Th_rec)*Smear_SF_Theta*smear_factor);
            // double Phi_new_rec = Phi_rec + gRandom->Gaus(0, (Phi_rec)*Smear_SF_Theta*smear_factor);
            double Th_new_rec  = Th_rec;
            double Phi_new_rec = Phi_rec;
            
            double Extra_Smear_SF_Theta = 0;
            if(ivec == 1){ // Pi+ Pion
                Extra_Smear_SF_Theta = (-2.2728e-05)*(TMath::RadToDeg()*Th_rec)*(TMath::RadToDeg()*Th_rec) + (1.9750e-03)*(TMath::RadToDeg()*Th_rec) + (-0.02847);
                if(Extra_Smear_SF_Theta < 0){Extra_Smear_SF_Theta = 0;}
                P_new_rec = P_new_rec + gRandom->Gaus(0,(P_new_rec)*Extra_Smear_SF_Theta*smear_factor);
            }
            
            // Making the smeared TLorentzVector:
            TLorentzVector V4_smear(V4.X(), V4.Y(), V4.Z(), V4.E());
            V4_smear.SetE(TMath::Sqrt(P_new_rec*P_new_rec + M_rec*M_rec));
            V4_smear.SetRho(   P_new_rec);
            V4_smear.SetTheta(Th_new_rec);
            V4_smear.SetPhi( Phi_new_rec);
            return V4_smear;
        };"""])
        smearing_function = "".join(["""
        //=======================================================================//
        //=================// Sigma Smearing Factor (Pass 2) //==================//
        //=======================================================================//
        // bool stop_over_smear = (pip > 4.5) || (pipth < 12.5);
        bool stop_over_smear = (pipth < 12.5);
        bool less_over_smear = (pip > 4.5) || (pipth < 20);
        // bool stop_over_smear = (pipth < 15);
        auto smear_func = [&](TLorentzVector V4, int ivec, bool stop_over_smear, bool less_over_smear){
            // True generated values (i.e., values of the unsmeared TLorentzVector)
            double M_rec   = V4.M();
            double P_rec   = V4.P();
            double Th_rec  = V4.Theta();
            double Phi_rec = V4.Phi();

            double Smear_SF_Theta = 0;
            // if(ivec == 0){ // Electron
            //     Smear_SF_Theta = (2.9693e-05)*(TMath::RadToDeg()*Th_rec)*(TMath::RadToDeg()*Th_rec) + (-1.3409e-03)*(TMath::RadToDeg()*Th_rec) + (0.01712);
            //     if(Smear_SF_Theta < 0){Smear_SF_Theta = 0;}
            // }
            // if(ivec == 1){ // Pi+ Pion
            //     Smear_SF_Theta = (2.4652e-05)*(TMath::RadToDeg()*Th_rec)*(TMath::RadToDeg()*Th_rec) + (-3.0371e-04)*(TMath::RadToDeg()*Th_rec) + (4.3560e-04);
            //     if(Smear_SF_Theta < 0){Smear_SF_Theta = 0;}
            // }
            // if(ivec == 0){ // Electron
            //     Smear_SF_Theta = (-5.4842e-05)*(TMath::RadToDeg()*Th_rec)*(TMath::RadToDeg()*Th_rec) + (2.1920e-03)*(TMath::RadToDeg()*Th_rec) + (-8.6631e-03);
            //     if(Smear_SF_Theta < 0){Smear_SF_Theta = 0;}
            // }
            // if(ivec == 0){ // Electron
            //     // Smear_SF_Theta = (-3.6737e-05)*(TMath::RadToDeg()*Th_rec)*(TMath::RadToDeg()*Th_rec) + (1.2103e-03)*(TMath::RadToDeg()*Th_rec) + (-2.6782e-03);
            //     // Smear_SF_Theta = (-4.3310e-05)*(TMath::RadToDeg()*Th_rec)*(TMath::RadToDeg()*Th_rec) + (1.4627e-03)*(TMath::RadToDeg()*Th_rec) + (-5.2904e-03);
            //     Smear_SF_Theta = (-4.0439e-05)*(TMath::RadToDeg()*Th_rec)*(TMath::RadToDeg()*Th_rec) + (1.3799e-03)*(TMath::RadToDeg()*Th_rec) + (-4.6519e-03);
            //     Smear_SF_Theta = 0.5*Smear_SF_Theta;
            //     if(Smear_SF_Theta < 0){Smear_SF_Theta = 0;}
            // }
            // if(ivec == 1){ // Pi+ Pion
            //     Smear_SF_Theta = (4.0905e-06)*(TMath::RadToDeg()*Th_rec)*(TMath::RadToDeg()*Th_rec) + (2.0371e-04)*(TMath::RadToDeg()*Th_rec) + (0.01161);
            //     if(Smear_SF_Theta < 0){Smear_SF_Theta = 0;}
            // }
            // if(ivec == 1){ // Pi+ Pion
            //     Smear_SF_Theta = (-1.2573e-05)*(TMath::RadToDeg()*Th_rec)*(TMath::RadToDeg()*Th_rec) + (1.7345e-03)*(TMath::RadToDeg()*Th_rec) + (-0.01872);
            //     if(Smear_SF_Theta < 0){Smear_SF_Theta = 0;}
            // }
            if(ivec == 1){ // Pi+ Pion
                Smear_SF_Theta = (-1.6512e-05)*(TMath::RadToDeg()*Th_rec)*(TMath::RadToDeg()*Th_rec) + (1.6159e-03)*(TMath::RadToDeg()*Th_rec) + (-0.01402);
                if(Smear_SF_Theta < 0){Smear_SF_Theta = 0;}
            }
            if(ivec == 0){ // Electron
                Smear_SF_Theta = (-7.6697e-05)*(TMath::RadToDeg()*Th_rec)*(TMath::RadToDeg()*Th_rec) + (2.7102e-03)*(TMath::RadToDeg()*Th_rec) + (-0.01402);
                // Smear_SF_Theta = 0.65*Smear_SF_Theta;
                Smear_SF_Theta = 0.95*Smear_SF_Theta;
                if(Smear_SF_Theta < 0){Smear_SF_Theta = 0;}
            }


            if(stop_over_smear && ivec == 0){ // Stop the electron from over-smearing the pion
                // Smear_SF_Theta = 0;
                // Smear_SF_Theta = 0.05*Smear_SF_Theta;
                Smear_SF_Theta = 0.10*Smear_SF_Theta;
            }
            else{
                // Stop the electron from over-smearing the pion (less significant version)
                // if(less_over_smear && ivec == 0){Smear_SF_Theta = 0.65*Smear_SF_Theta;}
                if(less_over_smear && ivec == 0){Smear_SF_Theta = 0.71*Smear_SF_Theta;}
            }

            // Calculate resolutions
            double smear_factor = """, str(smear_factor), """;
            double P_new_rec   = P_rec   + gRandom->Gaus(0,   (P_rec)*Smear_SF_Theta*smear_factor);
            // double Th_new_rec  = Th_rec  + gRandom->Gaus(0,  (Th_rec)*Smear_SF_Theta*smear_factor);
            // double Phi_new_rec = Phi_rec + gRandom->Gaus(0, (Phi_rec)*Smear_SF_Theta*smear_factor);
            double Th_new_rec  = Th_rec;
            double Phi_new_rec = Phi_rec;

            // double Extra_Smear_SF_Theta = 0;
            // if(ivec == 1){ // Pi+ Pion
            //     Extra_Smear_SF_Theta = (-2.2728e-05)*(TMath::RadToDeg()*Th_rec)*(TMath::RadToDeg()*Th_rec) + (1.9750e-03)*(TMath::RadToDeg()*Th_rec) + (-0.02847);
            //     if((Extra_Smear_SF_Theta < 0) || (stop_over_smear)){Extra_Smear_SF_Theta = 0;}
            //     // stop_over_smear was added to keep that region consistent with the original pion smearing
            //     P_new_rec = P_new_rec + gRandom->Gaus(0,(P_new_rec)*Extra_Smear_SF_Theta*smear_factor);
            // }

            // Making the smeared TLorentzVector:
            TLorentzVector V4_smear(V4.X(), V4.Y(), V4.Z(), V4.E());
            V4_smear.SetE(TMath::Sqrt(P_new_rec*P_new_rec + M_rec*M_rec));
            V4_smear.SetRho(   P_new_rec);
            V4_smear.SetTheta(Th_new_rec);
            V4_smear.SetPhi( Phi_new_rec);
            return V4_smear;
        };"""])
    else:
        smearing_function = "".join(["""
        //=======================================================================//
        //=================// Sigma Smearing Factor (Pass 1) //==================//
        //=======================================================================//
        bool stop_over_smear = (pipth < 12.5);
        bool less_over_smear = (pip > 4);
        auto smear_func = [&](TLorentzVector V4, int ivec, bool stop_over_smear, bool less_over_smear){
            // True generated values (i.e., values of the unsmeared TLorentzVector)
            double M_rec   = V4.M();
            double P_rec   = V4.P();
            double Th_rec  = V4.Theta();
            double Phi_rec = V4.Phi();
            
            double Smear_SF_Theta = 0;            
            if(ivec == 0){ // Electron
                Smear_SF_Theta = (1.4242e-05)*(TMath::RadToDeg()*Th_rec)*(TMath::RadToDeg()*Th_rec) + (-4.0322e-05)*(TMath::RadToDeg()*Th_rec) + (2.0106e-03);
                if(Smear_SF_Theta < 0){Smear_SF_Theta = 0;}
            }
            if(ivec == 1){ // Pi+ Pion
                Smear_SF_Theta = (-9.3972e-06)*(TMath::RadToDeg()*Th_rec)*(TMath::RadToDeg()*Th_rec) + (1.0138e-03)*(TMath::RadToDeg()*Th_rec) + (-4.4572e-03);
                if(Smear_SF_Theta < 0){Smear_SF_Theta = 0;}
            }
            
            if(stop_over_smear && ivec == 0){ // Stop the electron from over-smearing the pion
                // Smear_SF_Theta = 0;
                Smear_SF_Theta = 0.05*Smear_SF_Theta;
            }
            else{
                // Stop the electron from over-smearing the pion (less significant version)
                if(less_over_smear && ivec == 0){Smear_SF_Theta = 0.70*Smear_SF_Theta;}
                // Reduce the pion smearing to avoid over-smearing
                if(less_over_smear && ivec == 1){Smear_SF_Theta = 0.70*Smear_SF_Theta;}
            }
            
            // Calculate resolutions
            double smear_factor = """, str(smear_factor), """;
            double P_new_rec   = P_rec   + gRandom->Gaus(0,   (P_rec)*Smear_SF_Theta*smear_factor);
            // double Th_new_rec  = Th_rec  + gRandom->Gaus(0,  (Th_rec)*Smear_SF_Theta*smear_factor);
            // double Phi_new_rec = Phi_rec + gRandom->Gaus(0, (Phi_rec)*Smear_SF_Theta*smear_factor);
            double Th_new_rec  = Th_rec;
            double Phi_new_rec = Phi_rec;

            // Making the smeared TLorentzVector:
            TLorentzVector V4_smear(V4.X(), V4.Y(), V4.Z(), V4.E());
            V4_smear.SetE(TMath::Sqrt(P_new_rec*P_new_rec + M_rec*M_rec));
            V4_smear.SetRho(   P_new_rec);
            V4_smear.SetTheta(Th_new_rec);
            V4_smear.SetPhi( Phi_new_rec);
            return V4_smear;
        };"""])
        # smearing_function = "".join(["""
        # //=======================================================================//
        # //=================//      Sigma Smearing Factor      //=================//
        # //=======================================================================//
        # auto smear_func = [&](TLorentzVector V4, int ivec){
        #     // True generated values (i.e., values of the unsmeared TLorentzVector)
        #     double M_rec   = V4.M();
        #     double P_rec   = V4.P();
        #     double Th_rec  = V4.Theta();
        #     double Phi_rec = V4.Phi();
        #     double Smear_SF_Theta = 0;
        #     if(ivec == 0){ // Electron
        #         // Smear_SF_Theta    = (-2.0472e-05)*(TMath::RadToDeg()*Th_rec)*(TMath::RadToDeg()*Th_rec) + (8.7962e-04)*(TMath::RadToDeg()*Th_rec) + (-5.8595e-03);
        #         Smear_SF_Theta       = (-3.1431e-05)*(TMath::RadToDeg()*Th_rec)*(TMath::RadToDeg()*Th_rec) + (1.0284e-03)*(TMath::RadToDeg()*Th_rec) + (-4.0027e-03);
        #     }
        #     if(ivec == 1){ // Pi+ Pion
        #         // Smear_SF_Theta    = (-2.4939e-06)*(TMath::RadToDeg()*Th_rec)*(TMath::RadToDeg()*Th_rec) + (5.8277e-04)*(TMath::RadToDeg()*Th_rec) + (-5.8521e-03);
        #         Smear_SF_Theta       = (-1.6434e-06)*(TMath::RadToDeg()*Th_rec)*(TMath::RadToDeg()*Th_rec) + (5.1530e-04)*(TMath::RadToDeg()*Th_rec) + (-4.4158e-03);
        #     }
        #     // Calculate resolutions
        #     double smear_factor = 0.75;
        #     double P_new_rec    = P_rec   +   (P_rec)*Smear_SF_Theta*smear_factor*(gRandom->Gaus(0,1));
        #     double Th_new_rec   = Th_rec  +  (Th_rec)*Smear_SF_Theta*smear_factor*(gRandom->Gaus(0,1));
        #     double Phi_new_rec  = Phi_rec + (Phi_rec)*Smear_SF_Theta*smear_factor*(gRandom->Gaus(0,1));
        #     Th_new_rec  = Th_rec;
        #     Phi_new_rec = Phi_rec;
        #     double Extra_Smear_SF_Theta = 0;
        #     if(ivec == 1){ // Pi+ Pion
        #         Extra_Smear_SF_Theta = (2.2747e-06)*(TMath::RadToDeg()*Th_rec)*(TMath::RadToDeg()*Th_rec) + (3.0985e-04)*(TMath::RadToDeg()*Th_rec) + (-5.1206e-03);
        #         P_new_rec      = P_new_rec   +   (P_new_rec)*Extra_Smear_SF_Theta*smear_factor*(gRandom->Gaus(0,1));
        #         // Th_new_rec  = Th_new_rec  +  (Th_new_rec)*Extra_Smear_SF_Theta*smear_factor*(gRandom->Gaus(0,1));
        #         // Phi_new_rec = Phi_new_rec + (Phi_new_rec)*Extra_Smear_SF_Theta*smear_factor*(gRandom->Gaus(0,1));
        #     }
        #     if(ivec == 0){ // Electron
        #         Extra_Smear_SF_Theta = (-2.1655e-05)*(TMath::RadToDeg()*Th_rec)*(TMath::RadToDeg()*Th_rec) + (7.6626e-04)*(TMath::RadToDeg()*Th_rec) + (-3.8613e-03);
        #         P_new_rec      = P_new_rec   +   (P_new_rec)*Extra_Smear_SF_Theta*smear_factor*(gRandom->Gaus(0,1));
        #         // Th_new_rec  = Th_new_rec  +  (Th_new_rec)*Extra_Smear_SF_Theta*smear_factor*(gRandom->Gaus(0,1));
        #         // Phi_new_rec = Phi_new_rec + (Phi_new_rec)*Extra_Smear_SF_Theta*smear_factor*(gRandom->Gaus(0,1));
        #     }
        #     smear_factor = """, str(smear_factor), """;
        #     if(ivec == 1){ // Pi+ Pion
        #         Extra_Smear_SF_Theta = (-2.3228e-06)*(TMath::RadToDeg()*Th_rec)*(TMath::RadToDeg()*Th_rec) + (4.8641e-04)*(TMath::RadToDeg()*Th_rec) + (-7.2059e-03);
        #         P_new_rec      = P_new_rec   +   (P_new_rec)*Extra_Smear_SF_Theta*smear_factor*(gRandom->Gaus(0,1));
        #         // Th_new_rec  = Th_new_rec  +  (Th_new_rec)*Extra_Smear_SF_Theta*smear_factor*(gRandom->Gaus(0,1));
        #         // Phi_new_rec = Phi_new_rec + (Phi_new_rec)*Extra_Smear_SF_Theta*smear_factor*(gRandom->Gaus(0,1));
        #     }
        #     // Making the smeared TLorentzVector:
        #     TLorentzVector V4_smear(V4.X(), V4.Y(), V4.Z(), V4.E());
        #     V4_smear.SetE(TMath::Sqrt(P_new_rec*P_new_rec + M_rec*M_rec));
        #     V4_smear.SetRho(   P_new_rec);
        #     V4_smear.SetTheta(Th_new_rec);
        #     V4_smear.SetPhi( Phi_new_rec);
        #     return V4_smear;
        # };"""])
    
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
def BG_Cut_Function(dataframe="mdf"):
    if(dataframe in ["rdf"]):
        return ""
    else:
        Background_Cuts_MC = ""
        # List_of_Cuts = ["MM_gen < 1.5", "PID_el != 11", "PID_pip != 211"]
        List_of_Cuts = []
        List_of_Cuts.append("MM_gen < 1.5")
        List_of_Cuts.append("PID_el  != 11  && PID_el  != 0") # Identifies the particles that were matched but to the wrong particle
        List_of_Cuts.append("PID_pip != 211 && PID_pip != 0") # Identifies the particles that were matched but to the wrong particle
        List_of_Cuts.append("PID_el  == 0")                   # Identifies unmatched particles
        List_of_Cuts.append("PID_pip == 0")                   # Identifies unmatched particles
        for cuts in List_of_Cuts:
            if(dataframe in ["gdf"]):
                if("PID" in str(cuts)):
                    continue
                else:
                    cuts = str(cuts.replace("_gen", ""))
            if(Background_Cuts_MC in [""]):
                Background_Cuts_MC = f"({cuts})"
            else:
                Background_Cuts_MC = "".join([str(Background_Cuts_MC), " || (", str(cuts), ")"])
        return Background_Cuts_MC
    return "ERROR"









###########################################################################################################################################################################
###########################################################################################################################################################################
###########################################################################################################################################################################
###########################################################################################################################################################################
###########################################################################################################################################################################










# # # Up-to-date as of: 5/29/2024
# # New_Fiducial_Sector_Cuts = '''bool New_Fiducial_Sector_Cuts = ! ((((Hx*Hx) + (Hy*Hy)) < (325*325)) && (!((Hy > (-0.4803)*Hx + (19.0945)) && (Hy < (0.5236)*Hx + (-27.0866)))) && (!((Hy > (0.6749)*Hx + (17.7778)) && (Hy < (33.832)*Hx + (-877.4638)))) && (!((Hy > (-0.6442)*Hx + (29.6081)) && (Hy < (-19.0013)*Hx + (-430.0535)))) && (!((Hy > (0.4717)*Hx + (16.5094)) && (Hy < (-0.4717)*Hx + (-16.5094)))) && (!((Hy < (0.669)*Hx + (-26.0705)) && (Hy > (12.6372)*Hx + (301.8584)))) && (!((Hy < (-0.5909)*Hx + (-32.4477)) && (Hy > (-21.0059)*Hx + (363.1938))))) || (((Hx*Hx) + (Hy*Hy)) > (325*325));
# # return New_Fiducial_Sector_Cuts;'''

# # Up-to-date as of: 5/31/2024
# New_Fiducial_Sector_Cuts = """
# if((((Hx)*(Hx) + (Hy)*(Hy)) > (325)*(325)) || (((Hx)*(Hx) + (Hy)*(Hy)) < (75)*(75))){
#     return false;
# }
# else{
#     bool Fiducial_PCAL_Cuts =                        (((Hx)*(Hx) + (Hy)*(Hy)) < (325)*(325));
#     Fiducial_PCAL_Cuts      =  Fiducial_PCAL_Cuts && !((Hy >     (-0.5)*Hx +     (25.0)) && (Hy <   (0.5241)*Hx +   (-27.2289)));
#     Fiducial_PCAL_Cuts      =  Fiducial_PCAL_Cuts && !((Hy >   (0.6439)*Hx +   (26.145)) && (Hy <  (76.7615)*Hx + (-2409.6186)));
#     Fiducial_PCAL_Cuts      =  Fiducial_PCAL_Cuts && !((Hy >  (-0.6292)*Hx +  (33.7585)) && (Hy < (-23.2943)*Hx +  (-601.7726)));
#     Fiducial_PCAL_Cuts      =  Fiducial_PCAL_Cuts && !((Hy >      (0.5)*Hx +     (25.0)) && (Hy <     (-0.5)*Hx +      (-25.0)));
#     Fiducial_PCAL_Cuts      =  Fiducial_PCAL_Cuts && !((Hy <  ( 0.6494)*Hx + (-31.1688)) && (Hy >  (13.3333)*Hx +   (336.6667)));
#     Fiducial_PCAL_Cuts      =  Fiducial_PCAL_Cuts && !((Hy <  (-0.5796)*Hx + (-35.5102)) && (Hy >    (-35.0)*Hx +      (825.0)));
#     Fiducial_PCAL_Cuts      = !Fiducial_PCAL_Cuts;
#     return Fiducial_PCAL_Cuts;
# }
# """

# # Up-to-date as of: 6/12/2024
# New_Fiducial_Pip_Sector_Cuts = """
# if((((Hx_pip)*(Hx_pip) + (Hy_pip)*(Hy_pip)) > (20.5)*(20.5)) || (((Hx_pip)*(Hx_pip) + (Hy_pip)*(Hy_pip)) < (5.2)*(5.2))){
#     return false;
# }
# else{
#     bool Fiducial_DC_Cuts =                      (((Hx_pip)*(Hx_pip) + (Hy_pip)*(Hy_pip)) < (20.5)*(20.5));
#     Fiducial_DC_Cuts      =  Fiducial_DC_Cuts && !((Hy_pip > (-0.3379)*Hx_pip  + (0.5954))  && (Hy_pip <   (0.6801)*Hx_pip + (-2.1023)));
#     Fiducial_DC_Cuts      =  Fiducial_DC_Cuts && !((Hy_pip > (-56.375)*Hx_pip  + (95.4688)) && (Hy_pip >   (0.8029)*Hx_pip + (1.1253)));
#     Fiducial_DC_Cuts      =  Fiducial_DC_Cuts && !((Hy_pip > (-0.5307)*Hx_pip  + (1.7336))  && (Hy_pip <  (-5.7821)*Hx_pip + (-5.3558)));
#     Fiducial_DC_Cuts      =  Fiducial_DC_Cuts && !((Hy_pip >  (0.5805)*Hx_pip  + (0.69))    && (Hy_pip <  (-0.4095)*Hx_pip + (-1.3394)));
#     Fiducial_DC_Cuts      =  Fiducial_DC_Cuts && !((Hy_pip <  (0.9324)*Hx_pip  + (-0.3521)) && (Hy_pip < (-12.8857)*Hx_pip + (-31.4429)));
#     Fiducial_DC_Cuts      =  Fiducial_DC_Cuts && !((Hy_pip < (-0.4617)*Hx_pip  + (-1.7652)) && (Hy_pip >  (-5.7595)*Hx_pip + (3.7975)));
#     Fiducial_DC_Cuts      = !Fiducial_DC_Cuts;
#     return Fiducial_DC_Cuts;
# }
# """
# # Up-to-date as of: 7/3/2024 (new hipo.root files - V4)
# # New_Fiducial_Pip_Sector_Cuts = """
# # if((((pip_x_DC)*(pip_x_DC) + (pip_y_DC)*(pip_y_DC)) > (20.5)*(20.5)) || (((pip_x_DC)*(pip_x_DC) + (pip_y_DC)*(pip_y_DC)) < (5.2)*(5.2))){
# #     return false;
# # }
# # else{
# #     bool Fiducial_DC_Cuts =                      (((pip_x_DC)*(pip_x_DC) + (pip_y_DC)*(pip_y_DC)) < (20.5)*(20.5));
# #     Fiducial_DC_Cuts      =  Fiducial_DC_Cuts && !((pip_y_DC > (-0.3379)*pip_x_DC  + (0.5954))  && (pip_y_DC <   (0.6801)*pip_x_DC + (-2.1023)));
# #     Fiducial_DC_Cuts      =  Fiducial_DC_Cuts && !((pip_y_DC > (-56.375)*pip_x_DC  + (95.4688)) && (pip_y_DC >   (0.8029)*pip_x_DC + (1.1253)));
# #     Fiducial_DC_Cuts      =  Fiducial_DC_Cuts && !((pip_y_DC > (-0.5307)*pip_x_DC  + (1.7336))  && (pip_y_DC <  (-5.7821)*pip_x_DC + (-5.3558)));
# #     Fiducial_DC_Cuts      =  Fiducial_DC_Cuts && !((pip_y_DC >  (0.5805)*pip_x_DC  + (0.69))    && (pip_y_DC <  (-0.4095)*pip_x_DC + (-1.3394)));
# #     Fiducial_DC_Cuts      =  Fiducial_DC_Cuts && !((pip_y_DC <  (0.9324)*pip_x_DC  + (-0.3521)) && (pip_y_DC < (-12.8857)*pip_x_DC + (-31.4429)));
# #     Fiducial_DC_Cuts      =  Fiducial_DC_Cuts && !((pip_y_DC < (-0.4617)*pip_x_DC  + (-1.7652)) && (pip_y_DC >  (-5.7595)*pip_x_DC + (3.7975)));
# #     Fiducial_DC_Cuts      = !Fiducial_DC_Cuts;
# #     return Fiducial_DC_Cuts;
# # }
# # """

# # Up-to-date as of: 8/2/2024 (new hipo.root files - V5)
# New_Fiducial_Pip_Sector_Cuts = """
# double angle(double x1, double y1, double x2, double y2) {
#     return std::atan2(y2 - y1, x2 - x1);
# }
# bool is_point_in_polygon(double x, double y, const std::vector<std::pair<double, double>>& polygon) {
#     int num_vertices = polygon.size();
#     double winding_number = 0.0;
#     for (int i = 0; i < num_vertices; ++i) {
#         double x1 = polygon[i].first;
#         double y1 = polygon[i].second;
#         double x2 = polygon[(i + 1) % num_vertices].first;
#         double y2 = polygon[(i + 1) % num_vertices].second;
#         double a1 = angle(x, y, x1, y1);
#         double a2 = angle(x, y, x2, y2);
#         double angle_diff = a2 - a1;
#         if(angle_diff > M_PI){angle_diff -= 2 * M_PI;} else if(angle_diff < -M_PI){angle_diff += 2 * M_PI;}
#         winding_number += angle_diff;
#     }
#     return std::abs(winding_number) > M_PI;
# }

# bool polygon_cut(double Hx_pip, double Hy_pip) {
#     std::vector<std::vector<std::pair<double, double>>> polygons = {
#         {{425, 220}, {425, -225}, {385, -225}, {100, -40}, {100, 0}, {140, 0}, {180, -65}, {220, -87}, {350, -161}, {351, -90}, {356, -90}, {360, -130}, {360, -167}, {380, -180}, {381, -100}, {380, 189}, {250, 110}, {230, 101}, {200, 80}, {165, 50}, {150, 20}, {140, 10}, {140, 0}, {100, 0}, {100, 40}, {380, 220}},
#         {{50, 460}, {0, 460}, {0, 80}, {50, 60}, {70, 120}, {55, 125}, {50, 145}, {276, 281}, {275, 283}, {50, 150}, {30, 180}, {30, 250}, {30, 325}, {25, 330}, {27, 425}, {275, 283}, {276, 281}, {350, 240}, {300, 215}, {250, 185}, {150, 122}, {140, 120}, {115, 120}, {175, 160}, {160, 155}, {100, 120}, {70, 120}, {50, 60}, {100, 40}, {380, 220}, {425, 220}, {425, 250}},
#         {{-50, 460}, {0, 460}, {0, 80}, {-50, 60}, {-70, 120}, {-30, 190}, {-28, 222}, {-40, 300}, {-40, 418}, {-338, 247}, {-338, 230}, {-310, 225}, {-212, 165}, {-200, 150}, {-125, 115}, {-70, 120}, {-50, 60}, {-100, 40}, {-380, 220}, {-425, 220}, {-425, 250}},
#         {{-425, -225}, {-365, -225}, {-100, -40}, {-100, 0}, {-135, 0}, {-150, -25}, {-170, -60}, {-210, -87}, {-382, -190}, {-382, 179}, {-200, 75}, {-200, 85}, {-155, 30}, {-135, 0}, {-100, 0}, {-100, 40}, {-380, 220}, {-425, 220}},
#         {{-50, -460}, {0, -460}, {0, -80}, {-50, -60}, {-75, -115}, {-50, -150}, {-35, -170}, {-30, -200}, {-25, -410}, {-50, -415}, {-250, -297}, {-300, -266}, {-340, -240}, {-250, -195}, {-220, -170}, {-190, -150}, {-150, -125}, {-75, -115}, {-50, -60}, {-100, -40}, {-365, -225}, {-425, -225}, {-425, -250}},
#         {{0, -460}, {0, -80}, {50, -60}, {75, -115}, {60, -135}, {29, -200}, {28, -250}, {32, -250}, {36, -265}, {37, -410}, {100, -375}, {145, -350}, {200, -320}, {240, -300}, {330, -250}, {350, -235}, {220, -165}, {205, -155}, {210, -150}, {150, -120}, {130, -115}, {75, -115}, {50, -60}, {100, -40}, {385, -225}, {425, -225}, {425, -250}, {20, -460}}
#     };
#     for (const auto& poly : polygons) {
#         if(is_point_in_polygon(Hx_pip, Hy_pip, poly)){
#             return false; // Point is inside a polygon, filter it out
#         }
#     }
#     return true; // Point is outside all polygons
# }
# return polygon_cut(Hx_pip, Hy_pip);
# """


# Up-to-date as of: 8/30/2024
    # Note: The Pion cuts are "PRELIMINARY ONLY" - Are to be replaced once the Electron cuts have been applied
# New_Fiducial_DC_Cuts_Functions = """
# auto Polygon_Layers = std::map<std::string, std::vector<std::pair<double, double>>>{
#     {"Layer_6__ele", {{-65,  0}, {-65,  -3}, {13,   -41}, {14,   -40}, {19,    0}, {13,  42}, {-65,   2}, {-65,  0}}},
#     {"Layer_18_ele", {{-105, 0}, {-94,  -8}, {15,   -62}, {25,     0}, {15,   63}, {-92,  9}, {-105,  0}}},
#     {"Layer_36_ele", {{-170, 0}, {-169, -5}, {-100, -36}, {5,    -81}, {18,    0}, {5,   85}, {-75,  49}, {-170, 3}, {-170, 0}}},
#     {"Layer_6__pip", {{-86,  0}, {-86,  -6}, {-78,   -6}, {-78,  -10}, {-74, -14}, {14, -58}, {22,  -58}, {22, -46}, {42,   0}, {20, 56}, {-20,  37}, {-60,  18}, {-80,  8}, {-86,   0}}},
#     {"Layer_18_pip", {{-125, 0}, {-125, -7}, {-118,  -8}, {-80,  -32}, {-50, -47}, {0,  -73}, {30,  -89}, {55,   0}, {32,  91}, {0,  74}, {-80,  33}, {-114, 13}, {-119, 8}, {-124,  8}, {-125,  0}}},
#     {"Layer_36_pip", {{-155, 0}, {-150, -6}, {-125, -29}, {-100, -45}, {-50, -71}, {0,  -98}, {74, -140}, {76, -86}, {94,   0}, {76, 96}, {72,  141}, {-10,  96}, {-50, 74}, {-110, 43}, {-142, 16}, {-147, 11}, {-150, 8}, {-154, 6}, {-155, 0}}}
# };
# bool is_point_in_polygon(double x, double y, const std::vector<std::pair<double, double>>& polygon) {
#     double winding_number = 0.0;
#     int num_vertices = polygon.size();
#     for (int i = 0; i < num_vertices; ++i) {
#         double x1 = polygon[i].first;
#         double y1 = polygon[i].second;
#         double x2 = polygon[(i + 1) % num_vertices].first;
#         double y2 = polygon[(i + 1) % num_vertices].second;
#         double a1 = atan2(y1 - y, x1 - x);
#         double a2 = atan2(y2 - y, x2 - x);
#         double angle_diff = a2 - a1;
#         if(angle_diff > 3.1415926){
#             angle_diff -= 2 * 3.1415926;
#         } else if(angle_diff < -3.1415926){
#             angle_diff += 2 * 3.1415926;
#         }
#         winding_number += angle_diff;
#     }
#     return (std::abs(winding_number) > 3.1415926);
# }
# """

from MyCommonAnalysisFunction_richcap import color

# New Fiducial Cuts for the electron/pion
    # Sangbaek_and_Valerii_Fiducial_Cuts() used cuts based on Sangbaek's code but developed by Valerii
    # Up-to-date as of: 7/26/2024
        # Changed variable names and added for both the electron and pion
def Sangbaek_and_Valerii_Fiducial_Cuts(Data_Frame_Input, fidlevel='mid', Particle="ele", Cut_Flag=False, show_cut_code=False):
    for layer in [6, 18, 36]:
        # Checking Dataframe for correct columns
        if(Particle not in ["ele", "pip"]):
            print(f"{color.Error}Invalid Input for 'Particle'.\n{color.END_R}\tParticle = {color.UNDERLINE}{Particle}{color.END_R} (Must be either 'ele' or 'pip')\n\t{color.END_B}Defaulting to 'ele'{color.END}")
            Particle = "ele"
        if(any(needed_col not in Data_Frame_Input.GetColumnNames()   for needed_col in [f"{Particle}_x_DC_{layer}", f"{Particle}_y_DC_{layer}", f"{Particle}_z_DC_{layer}"])):
            print(f"{color.Error}\nMissing very important variable(s) for the (new) fiducial cuts from Valerii (Cannot make cuts)\n{color.END}")
            print(f"{color.BOLD}Variables available:{color.END}")
            col_num = 1
            for column_name in Data_Frame_Input.GetColumnNames():
                print(f"{col_num})\t{column_name}")
                col_num += 1
            del col_num
            return Data_Frame_Input
        elif(any(needed_col not in Data_Frame_Input.GetColumnNames() for needed_col in [f"{Particle}_y_DC_{layer}_rot", f"{Particle}_x_DC_{layer}_rot"])):
            sector = "pipsec" if(Particle in ["pip"]) else "esec"
            Data_Frame_Input = Data_Frame_Input.Define(f"{Particle}_y_DC_{layer}_rot", f"""
            auto {Particle}_y_DC_{layer}_rot_temp = {Particle}_y_DC_{layer};
            // 60 degrees per sector
            auto Angle_rot  = TMath::DegToRad()*(60)*({sector} - 1);
            {Particle}_y_DC_{layer}_rot_temp = ({Particle}_y_DC_{layer}*(TMath::Cos(Angle_rot))) - ({Particle}_x_DC_{layer}*(TMath::Sin(Angle_rot)));
            return {Particle}_y_DC_{layer}_rot_temp;
            """)
            Data_Frame_Input = Data_Frame_Input.Define(f"{Particle}_x_DC_{layer}_rot", f"""
            auto {Particle}_x_DC_{layer}_rot_temp = {Particle}_x_DC_{layer};
            // 60 degrees per sector
            auto Angle_rot  = TMath::DegToRad()*(60)*({sector} - 1);
            {Particle}_x_DC_{layer}_rot_temp = ({Particle}_y_DC_{layer}*(TMath::Sin(Angle_rot))) + ({Particle}_x_DC_{layer}*(TMath::Cos(Angle_rot)));
            {Particle}_x_DC_{layer}_rot_temp = (TMath::Sin(-25/57.2958))*{Particle}_z_DC_{layer} + (TMath::Cos(-25/57.2958))*{Particle}_x_DC_{layer}_rot_temp;
            return {Particle}_x_DC_{layer}_rot_temp;
            """)
            if(show_cut_code):
                print(f"""
Variable Def {color.BOLD}{Particle}_y_DC_{layer}_rot:{color.END} {{
    auto {Particle}_y_DC_{layer}_rot_temp = {Particle}_y_DC_{layer};
    // 60 degrees per sector
    auto Angle_rot  = TMath::DegToRad()*(60)*({sector} - 1);
    {Particle}_y_DC_{layer}_rot_temp = ({Particle}_y_DC_{layer}*(TMath::Cos(Angle_rot))) - ({Particle}_x_DC_{layer}*(TMath::Sin(Angle_rot)));
    return {Particle}_y_DC_{layer}_rot_temp;
}}
Variable Def {color.BOLD}{Particle}_x_DC_{layer}_rot:{color.END} {{
    auto {Particle}_x_DC_{layer}_rot_temp = {Particle}_x_DC_{layer};
    // 60 degrees per sector
    auto Angle_rot  = TMath::DegToRad()*(60)*({sector} - 1);
    {Particle}_x_DC_{layer}_rot_temp = ({Particle}_y_DC_{layer}*(TMath::Sin(Angle_rot))) + ({Particle}_x_DC_{layer}*(TMath::Cos(Angle_rot)));
    {Particle}_x_DC_{layer}_rot_temp = (TMath::Sin(-25/57.2958))*{Particle}_z_DC_{layer} + (TMath::Cos(-25/57.2958))*{Particle}_x_DC_{layer}_rot_temp;
    return {Particle}_x_DC_{layer}_rot_temp;
}}
        """)
        if(any(needed_col not in Data_Frame_Input.GetColumnNames()   for needed_col in [f"{Particle}_x_DC_{layer}_rot", f"{Particle}_x_DC_{layer}_rot"])):
            print(f"{color.Error}\nStill missing important variable(s) for the (new) fiducial cuts from Valerii (Cannot make cuts)\n{color.END}")
            # print(f"{color.BOLD}Variables available:{color.END}")
            # col_num = 1
            # for column_name in Data_Frame_Input.GetColumnNames():
            #     print(f"{col_num})\t{column_name}")
            #     col_num += 1
            # del col_num
            return Data_Frame_Input
        if(fidlevel not in ["None", "N/A"]):
            # DC Fiducial Cuts
            if(fidlevel == 'mid'):
                adjustment_layer1 = 0
                adjustment_layer2 = 0
                adjustment_layer3 = 0
            elif(fidlevel == 'loose'):
                adjustment_layer1 = 0.6*1
                adjustment_layer2 = 0.6*2
                adjustment_layer3 = 0.6*3
            elif(fidlevel == 'tight'):
                adjustment_layer1 = -0.6*1
                adjustment_layer2 = -0.6*2
                adjustment_layer3 = -0.6*3
            else:
                print(f"{color.Error}Error: Check fidlevel ({fidlevel})\n{color.END}")
                return Data_Frame_Input
            Cut_Code_txt = "".join(["""
    auto Cal_layer_Min =   -120;
    auto Cal_layer_Max =    120;
    """, f"""
    Cal_layer_Min  =   -0.50 * ({str(Particle)}_x_DC_{layer}_rot + 72  + {str(adjustment_layer1)});
    Cal_layer_Max  =    0.50 * ({str(Particle)}_x_DC_{layer}_rot + 72  + {str(adjustment_layer1)});
    """ if(layer in [6]) else f"""
    Cal_layer_Min  =  -0.505 * ({str(Particle)}_x_DC_{layer}_rot + 114 + {str(adjustment_layer2)});
    Cal_layer_Max  =   0.505 * ({str(Particle)}_x_DC_{layer}_rot + 114 + {str(adjustment_layer2)});
    """ if(layer in [18]) else f"""
    Cal_layer_Min  =  -0.495 * ({str(Particle)}_x_DC_{layer}_rot + 180 + {str(adjustment_layer3)});
    Cal_layer_Max  =   0.495 * ({str(Particle)}_x_DC_{layer}_rot + 180 + {str(adjustment_layer3)});
    """, f"""
    return (({str(Particle)}_y_DC_{layer}_rot > Cal_layer_Min) && ({str(Particle)}_y_DC_{layer}_rot < Cal_layer_Max));
    """])
            if(not Cut_Flag):
                # Applies Cut normally with the Filter() function
                Data_Frame_Input = Data_Frame_Input.Filter(Cut_Code_txt)
                if(show_cut_code):
                    print(f"Applied Cut:\n{color.BOLD}{Cut_Code_txt}{color.END}\n")
            else:
                # Creates a new column to flag the events to cut (rather than cut them right away)
                Data_Frame_Input = Data_Frame_Input.Define(f"Valerii_DC_Fiducial_Cuts_{str(Particle)}_DC_{layer}", Cut_Code_txt)
    return Data_Frame_Input
    
    
# New Fiducial Volume Cuts for the electron in the PCal
    # Up-to-date as of: 7/8/2024
def Valerii_Fiducial_PCal_Volume_Cuts(Data_Frame_Input, Cut_Flag=False, show_cut_code=False):
    # Checking Dataframe for correct columns
    if(any(needed_col not in Data_Frame_Input.GetColumnNames()for needed_col in ["V_PCal", "W_PCal", "U_PCal"])):
        print(f"{color.Error}\nMissing very important variable(s) for the (new) fiducial {color.UNDERLINE}volume{color.END}{color.Error} cuts from Valerii (Cannot make cuts)\n{color.END}")
        print(f"{color.BOLD}Variables available:{color.END}")
        col_num = 1
        for column_name in Data_Frame_Input.GetColumnNames():
            print(f"{col_num})\t{column_name}")
            col_num += 1
        del col_num
        return Data_Frame_Input
    elif(not Cut_Flag):
        # Applies Cut normally with the Filter() function
        Data_Frame_Input = Data_Frame_Input.Filter("return ((V_PCal > 19) && (W_PCal > 19) && (U_PCal < 395));")
        if(show_cut_code):
            print(f"\n{color.BOLD}Applied PCal Cuts: {color.UNDERLINE}((V_PCal > 19) && (W_PCal > 19) && (U_PCal < 395)){color.END}\n")
    else:
        # Creates a new column to flag the events to cut (rather than cut them right away)
        Data_Frame_Input = Data_Frame_Input.Define("Valerii_PCal_Fiducial_Cuts", "return ((V_PCal > 19) && (W_PCal > 19) && (U_PCal < 395));")
    return Data_Frame_Input


# Additional Sector-dependent Fiducial Cuts for the electron in the PCal
    # Up-to-date as of: 10/31/2024
def Sector_Fiducial_PCal_Cuts(Data_Frame_Input, Cut_Flag=False, show_cut_code=False):
    # Checking Dataframe for correct columns
    # PCal_Timothy_Cuts = "return ((esec != 1 && esec != 2 && esec != 3 && esec != 4 && esec != 6) || (esec == 1 && !((W_PCal >  74.2 && W_PCal <  79.6) || (W_PCal >  85.4 && W_PCal <  90.8) || (W_PCal > 213.0 && W_PCal < 218.4) || (W_PCal > 224.1 && W_PCal < 229.5))) || (esec == 2 && !(V_PCal > 102.0 && V_PCal < 113.0)) || (esec == 3 && !(V_PCal > 306.0 && V_PCal < 324.0)) || (esec == 4 && !(V_PCal > 235.0 && V_PCal < 240.0)) || (esec == 5) || (esec == 6 && !((W_PCal > 174.1 && W_PCal < 179.5) || (W_PCal > 185.2 && W_PCal < 190.6))));"
    # Removing the cut from sector 3:
    PCal_Timothy_Cuts = "return ((esec != 1 && esec != 2 && esec != 4 && esec != 6) || (esec == 1 && !((W_PCal >  74.2 && W_PCal <  79.6) || (W_PCal >  85.4 && W_PCal <  90.8) || (W_PCal > 213.0 && W_PCal < 218.4) || (W_PCal > 224.1 && W_PCal < 229.5))) || (esec == 2 && !(V_PCal > 102.0 && V_PCal < 113.0)) || (esec == 3) || (esec == 4 && !(V_PCal > 235.0 && V_PCal < 240.0)) || (esec == 5) || (esec == 6 && !((W_PCal > 174.1 && W_PCal < 179.5) || (W_PCal > 185.2 && W_PCal < 190.6))));"
    if(any(needed_col not in Data_Frame_Input.GetColumnNames()for needed_col in ["V_PCal", "W_PCal", "esec"])):
        print(f"{color.Error}\nMissing very important variable(s) for the (new) {color.UNDERLINE}Sector-dependent PCal{color.END}{color.Error} fiducial cuts (Inspired by Timothy - Cannot make cuts)\n{color.END}")
        print(f"{color.BOLD}Variables available:{color.END}")
        col_num = 1
        for column_name in Data_Frame_Input.GetColumnNames():
            print(f"{col_num})\t{column_name}")
            col_num += 1
        del col_num
        return Data_Frame_Input
    elif(not Cut_Flag):
        # Applies Cut normally with the Filter() function
        Data_Frame_Input = Data_Frame_Input.Filter(PCal_Timothy_Cuts)
        if(show_cut_code):
            print(f"{color.BOLD}Applied the following sector-dependent Fiducial Cuts for the electron in the PCal:{color.END}\nApplied Cut:\n{PCal_Timothy_Cuts}\n\n")
    else:
        # Creates a new column to flag the events to cut (rather than cut them right away)
        Data_Frame_Input = Data_Frame_Input.Define("Sector_PCal_Fiducial_Cuts", PCal_Timothy_Cuts)
    return Data_Frame_Input
    
    
from Pion_Test_Fiducial_Cuts_Defs import *
# Function for applying all the Fiducial Cuts above
def New_Fiducial_Cuts_Function(Data_Frame_In, Skip_Options="N/A", Cut_Flag=False, Show_Cut_Code=False):
    if("All" in Skip_Options):
        return Data_Frame_In
    Data_Frame_Out = Data_Frame_In
    Failed_Filter  = True
    if(not Cut_Flag):
        if(not any(my_cuts   in Skip_Options for my_cuts   in ["My_Fiducial", "My_Cuts", "sector", "esec",   "Electron", "All"])):
            # Applying my (electron) fiducial cuts
            # Data_Frame_Out = Data_Frame_Out.Filter("""is_point_in_polygon(ele_x_DC_6_rot,  ele_y_DC_6_rot,  Polygon_Layers["Layer_6__ele"])""")
            # Data_Frame_Out = Data_Frame_Out.Filter("""is_point_in_polygon(ele_x_DC_18_rot, ele_y_DC_18_rot, Polygon_Layers["Layer_18_ele"])""")
            # Data_Frame_Out = Data_Frame_Out.Filter("""is_point_in_polygon(ele_x_DC_36_rot, ele_y_DC_36_rot, Polygon_Layers["Layer_36_ele"])""")
            Data_Frame_Out = Apply_Test_Fiducial_Cuts(Data_Frame_In=Data_Frame_Out, List_of_Layers=["6", "18", "36"], List_of_Particles=["ele"], show_cut_code=Show_Cut_Code)
            Failed_Filter  = False
        if(not any(my_cuts   in Skip_Options for my_cuts   in ["My_Fiducial", "My_Cuts", "sector", "pipsec", "Pion",     "All"])):
            # Applying my (pion) fiducial cuts
            # Data_Frame_Out = Data_Frame_Out.Filter("""is_point_in_polygon(pip_x_DC_6_rot,  pip_y_DC_6_rot,  Polygon_Layers["Layer_6__pip"])""")
            # Data_Frame_Out = Data_Frame_Out.Filter("""is_point_in_polygon(pip_x_DC_18_rot, pip_y_DC_18_rot, Polygon_Layers["Layer_18_pip"])""")
            # Data_Frame_Out = Data_Frame_Out.Filter("""is_point_in_polygon(pip_x_DC_36_rot, pip_y_DC_36_rot, Polygon_Layers["Layer_36_pip"])""")
            Data_Frame_Out = Apply_Test_Fiducial_Cuts(Data_Frame_In=Data_Frame_Out, List_of_Layers=["6", "18", "36"], List_of_Particles=["pip"], show_cut_code=Show_Cut_Code)
            Failed_Filter  = False
    else:
        if(not any(my_cuts   in Skip_Options for my_cuts   in ["My_Fiducial", "My_Cuts", "sector", "esec",   "Electron", "All"])):
            # Applying my (electron) fiducial cuts
            # Data_Frame_Out = Data_Frame_Out.Define("My_ele_DC_Fiducial_Cuts", """(is_point_in_polygon(ele_x_DC_6_rot,  ele_y_DC_6_rot,  Polygon_Layers["Layer_6__ele"])) && (is_point_in_polygon(ele_x_DC_18_rot, ele_y_DC_18_rot, Polygon_Layers["Layer_18_ele"])) && (is_point_in_polygon(ele_x_DC_36_rot, ele_y_DC_36_rot, Polygon_Layers["Layer_36_ele"]))""")
            Data_Frame_Out = Apply_Test_Fiducial_Cuts(Data_Frame_In=Data_Frame_Out, List_of_Layers=["6", "18", "36"], List_of_Particles=["ele"], Define_Column=True, show_cut_code=Show_Cut_Code)
            Failed_Filter  = False
        if(not any(my_cuts   in Skip_Options for my_cuts   in ["My_Fiducial", "My_Cuts", "sector", "pipsec", "Pion",     "All"])):
            # Applying my (pion) fiducial cuts
            # Data_Frame_Out = Data_Frame_Out.Define("My_pip_DC_Fiducial_Cuts", """(is_point_in_polygon(pip_x_DC_6_rot,  pip_y_DC_6_rot,  Polygon_Layers["Layer_6__pip"])) && (is_point_in_polygon(pip_x_DC_18_rot, pip_y_DC_18_rot, Polygon_Layers["Layer_18_pip"])) && (is_point_in_polygon(pip_x_DC_36_rot, pip_y_DC_36_rot, Polygon_Layers["Layer_36_pip"]))""")
            Data_Frame_Out = Apply_Test_Fiducial_Cuts(Data_Frame_In=Data_Frame_Out, List_of_Layers=["6", "18", "36"], List_of_Particles=["pip"], Define_Column=True, show_cut_code=Show_Cut_Code)
            Failed_Filter  = False
    if(not any(DC_cuts   in Skip_Options for DC_cuts   in ["DC", "Sangbaek_and_Valerii_Fiducial_Cuts", "Sangbaek_and_Valerii", "Sangbaek", "Valerii", "DC_ele", "DC_el", "All"])):
        Data_Frame_Out = Sangbaek_and_Valerii_Fiducial_Cuts(Data_Frame_Input=Data_Frame_Out, fidlevel='mid', Particle="ele", Cut_Flag=Cut_Flag, show_cut_code=Show_Cut_Code)
        Failed_Filter  = False
    if(not any(DC_cuts   in Skip_Options for DC_cuts   in ["DC", "Sangbaek_and_Valerii_Fiducial_Cuts", "Sangbaek_and_Valerii", "Sangbaek", "Valerii", "DC_pip",          "All"])):
        Data_Frame_Out = Sangbaek_and_Valerii_Fiducial_Cuts(Data_Frame_Input=Data_Frame_Out, fidlevel='mid', Particle="pip", Cut_Flag=Cut_Flag, show_cut_code=Show_Cut_Code)
        Failed_Filter  = False
    if(not any(PCal_cuts in Skip_Options for PCal_cuts in ["PCal", "PCal_Volume", "Volume", "Valerii", "All"])):
        Data_Frame_Out = Valerii_Fiducial_PCal_Volume_Cuts(Data_Frame_Input=Data_Frame_Out, Cut_Flag=Cut_Flag, show_cut_code=Show_Cut_Code)
        Failed_Filter  = False
    if(not any(PCal_cuts in Skip_Options for PCal_cuts in ["PCal", "PCal_Sector", "Timothy", "All"])):
        Data_Frame_Out = Sector_Fiducial_PCal_Cuts(Data_Frame_Input=Data_Frame_Out, Cut_Flag=Cut_Flag, show_cut_code=Show_Cut_Code)
        Failed_Filter  = False
    if(Failed_Filter):
        print(f"{color.Error}\nPossible Error: New_Fiducial_Cuts_Function() did not apply any cuts...{color.END}\n\n")
        return Data_Frame_In
    return Data_Frame_Out



def PID_Histo_Label(Histogram):
    # Define the mapping and the histogram setup in Python
    pid_map = {-2212: (1,  "Anti-Proton"),
                -321: (2,  "Kaon (K^{-})"),
                -211: (3,  "#pi^{-} Pion"),
                  11: (4,  "Electron"),
                   0: (5,  "Unidentified"),
                 -11: (6,  "Positron"),
                 -13: (7,  "#mu^{+} Muon"),
                 211: (8,  "#pi^{+} Pion"),
                 321: (9,  "Kaon (K^{+})"),
                2212: (10, "Proton")}
    for pid, (idx, name) in pid_map.items():
        Histogram.GetZaxis().SetBinLabel(idx, name)
        Histogram.GetYaxis().SetBinLabel(idx, name)
    Histogram.GetZaxis().SetBinLabel(11, "Other")
    Histogram.GetYaxis().SetBinLabel(11, "Other")
    Histogram.GetZaxis().SetLabelSize(0.0375)
    Histogram.GetYaxis().SetLabelSize(0.0375)
    
    return Histogram