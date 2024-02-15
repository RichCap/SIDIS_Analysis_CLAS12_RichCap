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
    // (Total of 39 Q2-y bins including migration bins)
z_pT_Bin_Borders[1][1][0] = 0.2; z_pT_Bin_Borders[1][1][1] = 0.16; z_pT_Bin_Borders[1][1][2] = 0.2; z_pT_Bin_Borders[1][1][3] = 0.05;
Phi_h_Bin_Values[1][1][0] =  24; Phi_h_Bin_Values[1][1][1] = 0; Phi_h_Bin_Values[1][1][2] = 0;
z_pT_Bin_Borders[1][2][0] = 0.2; z_pT_Bin_Borders[1][2][1] = 0.16; z_pT_Bin_Borders[1][2][2] = 0.3; z_pT_Bin_Borders[1][2][3] = 0.2;
Phi_h_Bin_Values[1][2][0] =  24; Phi_h_Bin_Values[1][2][1] = 24; Phi_h_Bin_Values[1][2][2] = 24;
z_pT_Bin_Borders[1][3][0] = 0.2; z_pT_Bin_Borders[1][3][1] = 0.16; z_pT_Bin_Borders[1][3][2] = 0.4; z_pT_Bin_Borders[1][3][3] = 0.3;
Phi_h_Bin_Values[1][3][0] =  24; Phi_h_Bin_Values[1][3][1] = 48; Phi_h_Bin_Values[1][3][2] = 48;
z_pT_Bin_Borders[1][4][0] = 0.2; z_pT_Bin_Borders[1][4][1] = 0.16; z_pT_Bin_Borders[1][4][2] = 0.5; z_pT_Bin_Borders[1][4][3] = 0.4;
Phi_h_Bin_Values[1][4][0] =  24; Phi_h_Bin_Values[1][4][1] = 72; Phi_h_Bin_Values[1][4][2] = 72;
z_pT_Bin_Borders[1][5][0] = 0.2; z_pT_Bin_Borders[1][5][1] = 0.16; z_pT_Bin_Borders[1][5][2] = 0.6; z_pT_Bin_Borders[1][5][3] = 0.5;
Phi_h_Bin_Values[1][5][0] =  1; Phi_h_Bin_Values[1][5][1] = 96; Phi_h_Bin_Values[1][5][2] = 96;
z_pT_Bin_Borders[1][6][0] = 0.2; z_pT_Bin_Borders[1][6][1] = 0.16; z_pT_Bin_Borders[1][6][2] = 0.75; z_pT_Bin_Borders[1][6][3] = 0.6;
Phi_h_Bin_Values[1][6][0] =  1; Phi_h_Bin_Values[1][6][1] = 97; Phi_h_Bin_Values[1][6][2] = 97;
z_pT_Bin_Borders[1][7][0] = 0.2; z_pT_Bin_Borders[1][7][1] = 0.16; z_pT_Bin_Borders[1][7][2] = 1.0; z_pT_Bin_Borders[1][7][3] = 0.75;
Phi_h_Bin_Values[1][7][0] =  1; Phi_h_Bin_Values[1][7][1] = 98; Phi_h_Bin_Values[1][7][2] = 98;
z_pT_Bin_Borders[1][8][0] = 0.24; z_pT_Bin_Borders[1][8][1] = 0.2; z_pT_Bin_Borders[1][8][2] = 0.2; z_pT_Bin_Borders[1][8][3] = 0.05;
Phi_h_Bin_Values[1][8][0] =  24; Phi_h_Bin_Values[1][8][1] = 99; Phi_h_Bin_Values[1][8][2] = 99;
z_pT_Bin_Borders[1][9][0] = 0.24; z_pT_Bin_Borders[1][9][1] = 0.2; z_pT_Bin_Borders[1][9][2] = 0.3; z_pT_Bin_Borders[1][9][3] = 0.2;
Phi_h_Bin_Values[1][9][0] =  24; Phi_h_Bin_Values[1][9][1] = 123; Phi_h_Bin_Values[1][9][2] = 123;
z_pT_Bin_Borders[1][10][0] = 0.24; z_pT_Bin_Borders[1][10][1] = 0.2; z_pT_Bin_Borders[1][10][2] = 0.4; z_pT_Bin_Borders[1][10][3] = 0.3;
Phi_h_Bin_Values[1][10][0] =  24; Phi_h_Bin_Values[1][10][1] = 147; Phi_h_Bin_Values[1][10][2] = 147;
z_pT_Bin_Borders[1][11][0] = 0.24; z_pT_Bin_Borders[1][11][1] = 0.2; z_pT_Bin_Borders[1][11][2] = 0.5; z_pT_Bin_Borders[1][11][3] = 0.4;
Phi_h_Bin_Values[1][11][0] =  24; Phi_h_Bin_Values[1][11][1] = 171; Phi_h_Bin_Values[1][11][2] = 171;
z_pT_Bin_Borders[1][12][0] = 0.24; z_pT_Bin_Borders[1][12][1] = 0.2; z_pT_Bin_Borders[1][12][2] = 0.6; z_pT_Bin_Borders[1][12][3] = 0.5;
Phi_h_Bin_Values[1][12][0] =  24; Phi_h_Bin_Values[1][12][1] = 195; Phi_h_Bin_Values[1][12][2] = 195;
z_pT_Bin_Borders[1][13][0] = 0.24; z_pT_Bin_Borders[1][13][1] = 0.2; z_pT_Bin_Borders[1][13][2] = 0.75; z_pT_Bin_Borders[1][13][3] = 0.6;
Phi_h_Bin_Values[1][13][0] =  1; Phi_h_Bin_Values[1][13][1] = 219; Phi_h_Bin_Values[1][13][2] = 219;
z_pT_Bin_Borders[1][14][0] = 0.24; z_pT_Bin_Borders[1][14][1] = 0.2; z_pT_Bin_Borders[1][14][2] = 1.0; z_pT_Bin_Borders[1][14][3] = 0.75;
Phi_h_Bin_Values[1][14][0] =  1; Phi_h_Bin_Values[1][14][1] = 220; Phi_h_Bin_Values[1][14][2] = 220;
z_pT_Bin_Borders[1][15][0] = 0.31; z_pT_Bin_Borders[1][15][1] = 0.24; z_pT_Bin_Borders[1][15][2] = 0.2; z_pT_Bin_Borders[1][15][3] = 0.05;
Phi_h_Bin_Values[1][15][0] =  24; Phi_h_Bin_Values[1][15][1] = 221; Phi_h_Bin_Values[1][15][2] = 221;
z_pT_Bin_Borders[1][16][0] = 0.31; z_pT_Bin_Borders[1][16][1] = 0.24; z_pT_Bin_Borders[1][16][2] = 0.3; z_pT_Bin_Borders[1][16][3] = 0.2;
Phi_h_Bin_Values[1][16][0] =  24; Phi_h_Bin_Values[1][16][1] = 245; Phi_h_Bin_Values[1][16][2] = 245;
z_pT_Bin_Borders[1][17][0] = 0.31; z_pT_Bin_Borders[1][17][1] = 0.24; z_pT_Bin_Borders[1][17][2] = 0.4; z_pT_Bin_Borders[1][17][3] = 0.3;
Phi_h_Bin_Values[1][17][0] =  24; Phi_h_Bin_Values[1][17][1] = 269; Phi_h_Bin_Values[1][17][2] = 269;
z_pT_Bin_Borders[1][18][0] = 0.31; z_pT_Bin_Borders[1][18][1] = 0.24; z_pT_Bin_Borders[1][18][2] = 0.5; z_pT_Bin_Borders[1][18][3] = 0.4;
Phi_h_Bin_Values[1][18][0] =  24; Phi_h_Bin_Values[1][18][1] = 293; Phi_h_Bin_Values[1][18][2] = 293;
z_pT_Bin_Borders[1][19][0] = 0.31; z_pT_Bin_Borders[1][19][1] = 0.24; z_pT_Bin_Borders[1][19][2] = 0.6; z_pT_Bin_Borders[1][19][3] = 0.5;
Phi_h_Bin_Values[1][19][0] =  24; Phi_h_Bin_Values[1][19][1] = 317; Phi_h_Bin_Values[1][19][2] = 317;
z_pT_Bin_Borders[1][20][0] = 0.31; z_pT_Bin_Borders[1][20][1] = 0.24; z_pT_Bin_Borders[1][20][2] = 0.75; z_pT_Bin_Borders[1][20][3] = 0.6;
Phi_h_Bin_Values[1][20][0] =  24; Phi_h_Bin_Values[1][20][1] = 341; Phi_h_Bin_Values[1][20][2] = 341;
z_pT_Bin_Borders[1][21][0] = 0.31; z_pT_Bin_Borders[1][21][1] = 0.24; z_pT_Bin_Borders[1][21][2] = 1.0; z_pT_Bin_Borders[1][21][3] = 0.75;
Phi_h_Bin_Values[1][21][0] =  1; Phi_h_Bin_Values[1][21][1] = 365; Phi_h_Bin_Values[1][21][2] = 365;
z_pT_Bin_Borders[1][22][0] = 0.41; z_pT_Bin_Borders[1][22][1] = 0.31; z_pT_Bin_Borders[1][22][2] = 0.2; z_pT_Bin_Borders[1][22][3] = 0.05;
Phi_h_Bin_Values[1][22][0] =  24; Phi_h_Bin_Values[1][22][1] = 366; Phi_h_Bin_Values[1][22][2] = 366;
z_pT_Bin_Borders[1][23][0] = 0.41; z_pT_Bin_Borders[1][23][1] = 0.31; z_pT_Bin_Borders[1][23][2] = 0.3; z_pT_Bin_Borders[1][23][3] = 0.2;
Phi_h_Bin_Values[1][23][0] =  24; Phi_h_Bin_Values[1][23][1] = 390; Phi_h_Bin_Values[1][23][2] = 390;
z_pT_Bin_Borders[1][24][0] = 0.41; z_pT_Bin_Borders[1][24][1] = 0.31; z_pT_Bin_Borders[1][24][2] = 0.4; z_pT_Bin_Borders[1][24][3] = 0.3;
Phi_h_Bin_Values[1][24][0] =  24; Phi_h_Bin_Values[1][24][1] = 414; Phi_h_Bin_Values[1][24][2] = 414;
z_pT_Bin_Borders[1][25][0] = 0.41; z_pT_Bin_Borders[1][25][1] = 0.31; z_pT_Bin_Borders[1][25][2] = 0.5; z_pT_Bin_Borders[1][25][3] = 0.4;
Phi_h_Bin_Values[1][25][0] =  24; Phi_h_Bin_Values[1][25][1] = 438; Phi_h_Bin_Values[1][25][2] = 438;
z_pT_Bin_Borders[1][26][0] = 0.41; z_pT_Bin_Borders[1][26][1] = 0.31; z_pT_Bin_Borders[1][26][2] = 0.6; z_pT_Bin_Borders[1][26][3] = 0.5;
Phi_h_Bin_Values[1][26][0] =  24; Phi_h_Bin_Values[1][26][1] = 462; Phi_h_Bin_Values[1][26][2] = 462;
z_pT_Bin_Borders[1][27][0] = 0.41; z_pT_Bin_Borders[1][27][1] = 0.31; z_pT_Bin_Borders[1][27][2] = 0.75; z_pT_Bin_Borders[1][27][3] = 0.6;
Phi_h_Bin_Values[1][27][0] =  24; Phi_h_Bin_Values[1][27][1] = 486; Phi_h_Bin_Values[1][27][2] = 486;
z_pT_Bin_Borders[1][28][0] = 0.41; z_pT_Bin_Borders[1][28][1] = 0.31; z_pT_Bin_Borders[1][28][2] = 1.0; z_pT_Bin_Borders[1][28][3] = 0.75;
Phi_h_Bin_Values[1][28][0] =  24; Phi_h_Bin_Values[1][28][1] = 510; Phi_h_Bin_Values[1][28][2] = 510;
z_pT_Bin_Borders[1][29][0] = 0.7; z_pT_Bin_Borders[1][29][1] = 0.41; z_pT_Bin_Borders[1][29][2] = 0.2; z_pT_Bin_Borders[1][29][3] = 0.05;
Phi_h_Bin_Values[1][29][0] =  24; Phi_h_Bin_Values[1][29][1] = 534; Phi_h_Bin_Values[1][29][2] = 534;
z_pT_Bin_Borders[1][30][0] = 0.7; z_pT_Bin_Borders[1][30][1] = 0.41; z_pT_Bin_Borders[1][30][2] = 0.3; z_pT_Bin_Borders[1][30][3] = 0.2;
Phi_h_Bin_Values[1][30][0] =  24; Phi_h_Bin_Values[1][30][1] = 558; Phi_h_Bin_Values[1][30][2] = 558;
z_pT_Bin_Borders[1][31][0] = 0.7; z_pT_Bin_Borders[1][31][1] = 0.41; z_pT_Bin_Borders[1][31][2] = 0.4; z_pT_Bin_Borders[1][31][3] = 0.3;
Phi_h_Bin_Values[1][31][0] =  24; Phi_h_Bin_Values[1][31][1] = 582; Phi_h_Bin_Values[1][31][2] = 582;
z_pT_Bin_Borders[1][32][0] = 0.7; z_pT_Bin_Borders[1][32][1] = 0.41; z_pT_Bin_Borders[1][32][2] = 0.5; z_pT_Bin_Borders[1][32][3] = 0.4;
Phi_h_Bin_Values[1][32][0] =  24; Phi_h_Bin_Values[1][32][1] = 606; Phi_h_Bin_Values[1][32][2] = 606;
z_pT_Bin_Borders[1][33][0] = 0.7; z_pT_Bin_Borders[1][33][1] = 0.41; z_pT_Bin_Borders[1][33][2] = 0.6; z_pT_Bin_Borders[1][33][3] = 0.5;
Phi_h_Bin_Values[1][33][0] =  24; Phi_h_Bin_Values[1][33][1] = 630; Phi_h_Bin_Values[1][33][2] = 630;
z_pT_Bin_Borders[1][34][0] = 0.7; z_pT_Bin_Borders[1][34][1] = 0.41; z_pT_Bin_Borders[1][34][2] = 0.75; z_pT_Bin_Borders[1][34][3] = 0.6;
Phi_h_Bin_Values[1][34][0] =  24; Phi_h_Bin_Values[1][34][1] = 654; Phi_h_Bin_Values[1][34][2] = 654;
z_pT_Bin_Borders[1][35][0] = 0.7; z_pT_Bin_Borders[1][35][1] = 0.41; z_pT_Bin_Borders[1][35][2] = 1.0; z_pT_Bin_Borders[1][35][3] = 0.75;
Phi_h_Bin_Values[1][35][0] =  24; Phi_h_Bin_Values[1][35][1] = 678; Phi_h_Bin_Values[1][35][2] = 678;
z_pT_Bin_Borders[1][36][0] = 0.16; z_pT_Bin_Borders[1][36][1] = 0; z_pT_Bin_Borders[1][36][2] = 0.05; z_pT_Bin_Borders[1][36][3] = 0;
Phi_h_Bin_Values[1][36][0] =  1; Phi_h_Bin_Values[1][36][1] = 702; Phi_h_Bin_Values[1][36][2] = 702;
z_pT_Bin_Borders[1][37][0] = 0.16; z_pT_Bin_Borders[1][37][1] = 0; z_pT_Bin_Borders[1][37][2] = 0.05; z_pT_Bin_Borders[1][37][3] = 0.2;
Phi_h_Bin_Values[1][37][0] =  1; Phi_h_Bin_Values[1][37][1] = 703; Phi_h_Bin_Values[1][37][2] = 703;
z_pT_Bin_Borders[1][38][0] = 0.16; z_pT_Bin_Borders[1][38][1] = 0; z_pT_Bin_Borders[1][38][2] = 0.2; z_pT_Bin_Borders[1][38][3] = 0.3;
Phi_h_Bin_Values[1][38][0] =  1; Phi_h_Bin_Values[1][38][1] = 704; Phi_h_Bin_Values[1][38][2] = 704;
z_pT_Bin_Borders[1][39][0] = 0.16; z_pT_Bin_Borders[1][39][1] = 0; z_pT_Bin_Borders[1][39][2] = 0.3; z_pT_Bin_Borders[1][39][3] = 0.4;
Phi_h_Bin_Values[1][39][0] =  1; Phi_h_Bin_Values[1][39][1] = 705; Phi_h_Bin_Values[1][39][2] = 705;
z_pT_Bin_Borders[1][40][0] = 0.16; z_pT_Bin_Borders[1][40][1] = 0; z_pT_Bin_Borders[1][40][2] = 0.4; z_pT_Bin_Borders[1][40][3] = 0.5;
Phi_h_Bin_Values[1][40][0] =  1; Phi_h_Bin_Values[1][40][1] = 706; Phi_h_Bin_Values[1][40][2] = 706;
z_pT_Bin_Borders[1][41][0] = 0.16; z_pT_Bin_Borders[1][41][1] = 0; z_pT_Bin_Borders[1][41][2] = 0.5; z_pT_Bin_Borders[1][41][3] = 0.6;
Phi_h_Bin_Values[1][41][0] =  1; Phi_h_Bin_Values[1][41][1] = 707; Phi_h_Bin_Values[1][41][2] = 707;
z_pT_Bin_Borders[1][42][0] = 0.16; z_pT_Bin_Borders[1][42][1] = 0; z_pT_Bin_Borders[1][42][2] = 0.6; z_pT_Bin_Borders[1][42][3] = 0.75;
Phi_h_Bin_Values[1][42][0] =  1; Phi_h_Bin_Values[1][42][1] = 708; Phi_h_Bin_Values[1][42][2] = 708;
z_pT_Bin_Borders[1][43][0] = 0.16; z_pT_Bin_Borders[1][43][1] = 0; z_pT_Bin_Borders[1][43][2] = 0.75; z_pT_Bin_Borders[1][43][3] = 1.0;
Phi_h_Bin_Values[1][43][0] =  1; Phi_h_Bin_Values[1][43][1] = 709; Phi_h_Bin_Values[1][43][2] = 709;
z_pT_Bin_Borders[1][44][0] = 0.16; z_pT_Bin_Borders[1][44][1] = 0; z_pT_Bin_Borders[1][44][2] = 10; z_pT_Bin_Borders[1][44][3] = 1.0;
Phi_h_Bin_Values[1][44][0] =  1; Phi_h_Bin_Values[1][44][1] = 710; Phi_h_Bin_Values[1][44][2] = 710;
z_pT_Bin_Borders[1][45][0] = 0.16; z_pT_Bin_Borders[1][45][1] = 0.2; z_pT_Bin_Borders[1][45][2] = 0.05; z_pT_Bin_Borders[1][45][3] = 0;
Phi_h_Bin_Values[1][45][0] =  1; Phi_h_Bin_Values[1][45][1] = 711; Phi_h_Bin_Values[1][45][2] = 711;
z_pT_Bin_Borders[1][46][0] = 0.16; z_pT_Bin_Borders[1][46][1] = 0.2; z_pT_Bin_Borders[1][46][2] = 10; z_pT_Bin_Borders[1][46][3] = 1.0;
Phi_h_Bin_Values[1][46][0] =  1; Phi_h_Bin_Values[1][46][1] = 712; Phi_h_Bin_Values[1][46][2] = 712;
z_pT_Bin_Borders[1][47][0] = 0.2; z_pT_Bin_Borders[1][47][1] = 0.24; z_pT_Bin_Borders[1][47][2] = 0.05; z_pT_Bin_Borders[1][47][3] = 0;
Phi_h_Bin_Values[1][47][0] =  1; Phi_h_Bin_Values[1][47][1] = 713; Phi_h_Bin_Values[1][47][2] = 713;
z_pT_Bin_Borders[1][48][0] = 0.2; z_pT_Bin_Borders[1][48][1] = 0.24; z_pT_Bin_Borders[1][48][2] = 10; z_pT_Bin_Borders[1][48][3] = 1.0;
Phi_h_Bin_Values[1][48][0] =  1; Phi_h_Bin_Values[1][48][1] = 714; Phi_h_Bin_Values[1][48][2] = 714;
z_pT_Bin_Borders[1][49][0] = 0.24; z_pT_Bin_Borders[1][49][1] = 0.31; z_pT_Bin_Borders[1][49][2] = 0.05; z_pT_Bin_Borders[1][49][3] = 0;
Phi_h_Bin_Values[1][49][0] =  1; Phi_h_Bin_Values[1][49][1] = 715; Phi_h_Bin_Values[1][49][2] = 715;
z_pT_Bin_Borders[1][50][0] = 0.24; z_pT_Bin_Borders[1][50][1] = 0.31; z_pT_Bin_Borders[1][50][2] = 10; z_pT_Bin_Borders[1][50][3] = 1.0;
Phi_h_Bin_Values[1][50][0] =  1; Phi_h_Bin_Values[1][50][1] = 716; Phi_h_Bin_Values[1][50][2] = 716;
z_pT_Bin_Borders[1][51][0] = 0.31; z_pT_Bin_Borders[1][51][1] = 0.41; z_pT_Bin_Borders[1][51][2] = 0.05; z_pT_Bin_Borders[1][51][3] = 0;
Phi_h_Bin_Values[1][51][0] =  1; Phi_h_Bin_Values[1][51][1] = 717; Phi_h_Bin_Values[1][51][2] = 717;
z_pT_Bin_Borders[1][52][0] = 0.31; z_pT_Bin_Borders[1][52][1] = 0.41; z_pT_Bin_Borders[1][52][2] = 10; z_pT_Bin_Borders[1][52][3] = 1.0;
Phi_h_Bin_Values[1][52][0] =  1; Phi_h_Bin_Values[1][52][1] = 718; Phi_h_Bin_Values[1][52][2] = 718;
z_pT_Bin_Borders[1][53][0] = 0.41; z_pT_Bin_Borders[1][53][1] = 0.7; z_pT_Bin_Borders[1][53][2] = 0.05; z_pT_Bin_Borders[1][53][3] = 0;
Phi_h_Bin_Values[1][53][0] =  1; Phi_h_Bin_Values[1][53][1] = 719; Phi_h_Bin_Values[1][53][2] = 719;
z_pT_Bin_Borders[1][54][0] = 0.41; z_pT_Bin_Borders[1][54][1] = 0.7; z_pT_Bin_Borders[1][54][2] = 10; z_pT_Bin_Borders[1][54][3] = 1.0;
Phi_h_Bin_Values[1][54][0] =  1; Phi_h_Bin_Values[1][54][1] = 720; Phi_h_Bin_Values[1][54][2] = 720;
z_pT_Bin_Borders[1][55][0] = 10; z_pT_Bin_Borders[1][55][1] = 0.7; z_pT_Bin_Borders[1][55][2] = 0; z_pT_Bin_Borders[1][55][3] = 0.05;
Phi_h_Bin_Values[1][55][0] =  1; Phi_h_Bin_Values[1][55][1] = 721; Phi_h_Bin_Values[1][55][2] = 721;
z_pT_Bin_Borders[1][56][0] = 10; z_pT_Bin_Borders[1][56][1] = 0.7; z_pT_Bin_Borders[1][56][2] = 0.05; z_pT_Bin_Borders[1][56][3] = 0.2;
Phi_h_Bin_Values[1][56][0] =  1; Phi_h_Bin_Values[1][56][1] = 722; Phi_h_Bin_Values[1][56][2] = 722;
z_pT_Bin_Borders[1][57][0] = 10; z_pT_Bin_Borders[1][57][1] = 0.7; z_pT_Bin_Borders[1][57][2] = 0.2; z_pT_Bin_Borders[1][57][3] = 0.3;
Phi_h_Bin_Values[1][57][0] =  1; Phi_h_Bin_Values[1][57][1] = 723; Phi_h_Bin_Values[1][57][2] = 723;
z_pT_Bin_Borders[1][58][0] = 10; z_pT_Bin_Borders[1][58][1] = 0.7; z_pT_Bin_Borders[1][58][2] = 0.3; z_pT_Bin_Borders[1][58][3] = 0.4;
Phi_h_Bin_Values[1][58][0] =  1; Phi_h_Bin_Values[1][58][1] = 724; Phi_h_Bin_Values[1][58][2] = 724;
z_pT_Bin_Borders[1][59][0] = 10; z_pT_Bin_Borders[1][59][1] = 0.7; z_pT_Bin_Borders[1][59][2] = 0.4; z_pT_Bin_Borders[1][59][3] = 0.5;
Phi_h_Bin_Values[1][59][0] =  1; Phi_h_Bin_Values[1][59][1] = 725; Phi_h_Bin_Values[1][59][2] = 725;
z_pT_Bin_Borders[1][60][0] = 10; z_pT_Bin_Borders[1][60][1] = 0.7; z_pT_Bin_Borders[1][60][2] = 0.5; z_pT_Bin_Borders[1][60][3] = 0.6;
Phi_h_Bin_Values[1][60][0] =  1; Phi_h_Bin_Values[1][60][1] = 726; Phi_h_Bin_Values[1][60][2] = 726;
z_pT_Bin_Borders[1][61][0] = 10; z_pT_Bin_Borders[1][61][1] = 0.7; z_pT_Bin_Borders[1][61][2] = 0.6; z_pT_Bin_Borders[1][61][3] = 0.75;
Phi_h_Bin_Values[1][61][0] =  1; Phi_h_Bin_Values[1][61][1] = 727; Phi_h_Bin_Values[1][61][2] = 727;
z_pT_Bin_Borders[1][62][0] = 10; z_pT_Bin_Borders[1][62][1] = 0.7; z_pT_Bin_Borders[1][62][2] = 0.75; z_pT_Bin_Borders[1][62][3] = 1.0;
Phi_h_Bin_Values[1][62][0] =  1; Phi_h_Bin_Values[1][62][1] = 728; Phi_h_Bin_Values[1][62][2] = 728;
z_pT_Bin_Borders[1][63][0] = 10; z_pT_Bin_Borders[1][63][1] = 0.7; z_pT_Bin_Borders[1][63][2] = 10; z_pT_Bin_Borders[1][63][3] = 1.0;
Phi_h_Bin_Values[1][63][0] =  1; Phi_h_Bin_Values[1][63][1] = 729; Phi_h_Bin_Values[1][63][2] = 729;
z_pT_Bin_Borders[2][1][0] = 0.23; z_pT_Bin_Borders[2][1][1] = 0.19; z_pT_Bin_Borders[2][1][2] = 0.25; z_pT_Bin_Borders[2][1][3] = 0.05;
Phi_h_Bin_Values[2][1][0] =  24; Phi_h_Bin_Values[2][1][1] = 0; Phi_h_Bin_Values[2][1][2] = 730;
z_pT_Bin_Borders[2][2][0] = 0.23; z_pT_Bin_Borders[2][2][1] = 0.19; z_pT_Bin_Borders[2][2][2] = 0.35; z_pT_Bin_Borders[2][2][3] = 0.25;
Phi_h_Bin_Values[2][2][0] =  24; Phi_h_Bin_Values[2][2][1] = 24; Phi_h_Bin_Values[2][2][2] = 754;
z_pT_Bin_Borders[2][3][0] = 0.23; z_pT_Bin_Borders[2][3][1] = 0.19; z_pT_Bin_Borders[2][3][2] = 0.45; z_pT_Bin_Borders[2][3][3] = 0.35;
Phi_h_Bin_Values[2][3][0] =  24; Phi_h_Bin_Values[2][3][1] = 48; Phi_h_Bin_Values[2][3][2] = 778;
z_pT_Bin_Borders[2][4][0] = 0.23; z_pT_Bin_Borders[2][4][1] = 0.19; z_pT_Bin_Borders[2][4][2] = 0.54; z_pT_Bin_Borders[2][4][3] = 0.45;
Phi_h_Bin_Values[2][4][0] =  24; Phi_h_Bin_Values[2][4][1] = 72; Phi_h_Bin_Values[2][4][2] = 802;
z_pT_Bin_Borders[2][5][0] = 0.23; z_pT_Bin_Borders[2][5][1] = 0.19; z_pT_Bin_Borders[2][5][2] = 0.67; z_pT_Bin_Borders[2][5][3] = 0.54;
Phi_h_Bin_Values[2][5][0] =  1; Phi_h_Bin_Values[2][5][1] = 96; Phi_h_Bin_Values[2][5][2] = 826;
z_pT_Bin_Borders[2][6][0] = 0.23; z_pT_Bin_Borders[2][6][1] = 0.19; z_pT_Bin_Borders[2][6][2] = 0.93; z_pT_Bin_Borders[2][6][3] = 0.67;
Phi_h_Bin_Values[2][6][0] =  1; Phi_h_Bin_Values[2][6][1] = 97; Phi_h_Bin_Values[2][6][2] = 827;
z_pT_Bin_Borders[2][7][0] = 0.26; z_pT_Bin_Borders[2][7][1] = 0.23; z_pT_Bin_Borders[2][7][2] = 0.25; z_pT_Bin_Borders[2][7][3] = 0.05;
Phi_h_Bin_Values[2][7][0] =  24; Phi_h_Bin_Values[2][7][1] = 98; Phi_h_Bin_Values[2][7][2] = 828;
z_pT_Bin_Borders[2][8][0] = 0.26; z_pT_Bin_Borders[2][8][1] = 0.23; z_pT_Bin_Borders[2][8][2] = 0.35; z_pT_Bin_Borders[2][8][3] = 0.25;
Phi_h_Bin_Values[2][8][0] =  24; Phi_h_Bin_Values[2][8][1] = 122; Phi_h_Bin_Values[2][8][2] = 852;
z_pT_Bin_Borders[2][9][0] = 0.26; z_pT_Bin_Borders[2][9][1] = 0.23; z_pT_Bin_Borders[2][9][2] = 0.45; z_pT_Bin_Borders[2][9][3] = 0.35;
Phi_h_Bin_Values[2][9][0] =  24; Phi_h_Bin_Values[2][9][1] = 146; Phi_h_Bin_Values[2][9][2] = 876;
z_pT_Bin_Borders[2][10][0] = 0.26; z_pT_Bin_Borders[2][10][1] = 0.23; z_pT_Bin_Borders[2][10][2] = 0.54; z_pT_Bin_Borders[2][10][3] = 0.45;
Phi_h_Bin_Values[2][10][0] =  24; Phi_h_Bin_Values[2][10][1] = 170; Phi_h_Bin_Values[2][10][2] = 900;
z_pT_Bin_Borders[2][11][0] = 0.26; z_pT_Bin_Borders[2][11][1] = 0.23; z_pT_Bin_Borders[2][11][2] = 0.67; z_pT_Bin_Borders[2][11][3] = 0.54;
Phi_h_Bin_Values[2][11][0] =  24; Phi_h_Bin_Values[2][11][1] = 194; Phi_h_Bin_Values[2][11][2] = 924;
z_pT_Bin_Borders[2][12][0] = 0.26; z_pT_Bin_Borders[2][12][1] = 0.23; z_pT_Bin_Borders[2][12][2] = 0.93; z_pT_Bin_Borders[2][12][3] = 0.67;
Phi_h_Bin_Values[2][12][0] =  1; Phi_h_Bin_Values[2][12][1] = 218; Phi_h_Bin_Values[2][12][2] = 948;
z_pT_Bin_Borders[2][13][0] = 0.31; z_pT_Bin_Borders[2][13][1] = 0.26; z_pT_Bin_Borders[2][13][2] = 0.25; z_pT_Bin_Borders[2][13][3] = 0.05;
Phi_h_Bin_Values[2][13][0] =  24; Phi_h_Bin_Values[2][13][1] = 219; Phi_h_Bin_Values[2][13][2] = 949;
z_pT_Bin_Borders[2][14][0] = 0.31; z_pT_Bin_Borders[2][14][1] = 0.26; z_pT_Bin_Borders[2][14][2] = 0.35; z_pT_Bin_Borders[2][14][3] = 0.25;
Phi_h_Bin_Values[2][14][0] =  24; Phi_h_Bin_Values[2][14][1] = 243; Phi_h_Bin_Values[2][14][2] = 973;
z_pT_Bin_Borders[2][15][0] = 0.31; z_pT_Bin_Borders[2][15][1] = 0.26; z_pT_Bin_Borders[2][15][2] = 0.45; z_pT_Bin_Borders[2][15][3] = 0.35;
Phi_h_Bin_Values[2][15][0] =  24; Phi_h_Bin_Values[2][15][1] = 267; Phi_h_Bin_Values[2][15][2] = 997;
z_pT_Bin_Borders[2][16][0] = 0.31; z_pT_Bin_Borders[2][16][1] = 0.26; z_pT_Bin_Borders[2][16][2] = 0.54; z_pT_Bin_Borders[2][16][3] = 0.45;
Phi_h_Bin_Values[2][16][0] =  24; Phi_h_Bin_Values[2][16][1] = 291; Phi_h_Bin_Values[2][16][2] = 1021;
z_pT_Bin_Borders[2][17][0] = 0.31; z_pT_Bin_Borders[2][17][1] = 0.26; z_pT_Bin_Borders[2][17][2] = 0.67; z_pT_Bin_Borders[2][17][3] = 0.54;
Phi_h_Bin_Values[2][17][0] =  24; Phi_h_Bin_Values[2][17][1] = 315; Phi_h_Bin_Values[2][17][2] = 1045;
z_pT_Bin_Borders[2][18][0] = 0.31; z_pT_Bin_Borders[2][18][1] = 0.26; z_pT_Bin_Borders[2][18][2] = 0.93; z_pT_Bin_Borders[2][18][3] = 0.67;
Phi_h_Bin_Values[2][18][0] =  1; Phi_h_Bin_Values[2][18][1] = 339; Phi_h_Bin_Values[2][18][2] = 1069;
z_pT_Bin_Borders[2][19][0] = 0.38; z_pT_Bin_Borders[2][19][1] = 0.31; z_pT_Bin_Borders[2][19][2] = 0.25; z_pT_Bin_Borders[2][19][3] = 0.05;
Phi_h_Bin_Values[2][19][0] =  24; Phi_h_Bin_Values[2][19][1] = 340; Phi_h_Bin_Values[2][19][2] = 1070;
z_pT_Bin_Borders[2][20][0] = 0.38; z_pT_Bin_Borders[2][20][1] = 0.31; z_pT_Bin_Borders[2][20][2] = 0.35; z_pT_Bin_Borders[2][20][3] = 0.25;
Phi_h_Bin_Values[2][20][0] =  24; Phi_h_Bin_Values[2][20][1] = 364; Phi_h_Bin_Values[2][20][2] = 1094;
z_pT_Bin_Borders[2][21][0] = 0.38; z_pT_Bin_Borders[2][21][1] = 0.31; z_pT_Bin_Borders[2][21][2] = 0.45; z_pT_Bin_Borders[2][21][3] = 0.35;
Phi_h_Bin_Values[2][21][0] =  24; Phi_h_Bin_Values[2][21][1] = 388; Phi_h_Bin_Values[2][21][2] = 1118;
z_pT_Bin_Borders[2][22][0] = 0.38; z_pT_Bin_Borders[2][22][1] = 0.31; z_pT_Bin_Borders[2][22][2] = 0.54; z_pT_Bin_Borders[2][22][3] = 0.45;
Phi_h_Bin_Values[2][22][0] =  24; Phi_h_Bin_Values[2][22][1] = 412; Phi_h_Bin_Values[2][22][2] = 1142;
z_pT_Bin_Borders[2][23][0] = 0.38; z_pT_Bin_Borders[2][23][1] = 0.31; z_pT_Bin_Borders[2][23][2] = 0.67; z_pT_Bin_Borders[2][23][3] = 0.54;
Phi_h_Bin_Values[2][23][0] =  24; Phi_h_Bin_Values[2][23][1] = 436; Phi_h_Bin_Values[2][23][2] = 1166;
z_pT_Bin_Borders[2][24][0] = 0.38; z_pT_Bin_Borders[2][24][1] = 0.31; z_pT_Bin_Borders[2][24][2] = 0.93; z_pT_Bin_Borders[2][24][3] = 0.67;
Phi_h_Bin_Values[2][24][0] =  24; Phi_h_Bin_Values[2][24][1] = 460; Phi_h_Bin_Values[2][24][2] = 1190;
z_pT_Bin_Borders[2][25][0] = 0.5; z_pT_Bin_Borders[2][25][1] = 0.38; z_pT_Bin_Borders[2][25][2] = 0.25; z_pT_Bin_Borders[2][25][3] = 0.05;
Phi_h_Bin_Values[2][25][0] =  24; Phi_h_Bin_Values[2][25][1] = 484; Phi_h_Bin_Values[2][25][2] = 1214;
z_pT_Bin_Borders[2][26][0] = 0.5; z_pT_Bin_Borders[2][26][1] = 0.38; z_pT_Bin_Borders[2][26][2] = 0.35; z_pT_Bin_Borders[2][26][3] = 0.25;
Phi_h_Bin_Values[2][26][0] =  24; Phi_h_Bin_Values[2][26][1] = 508; Phi_h_Bin_Values[2][26][2] = 1238;
z_pT_Bin_Borders[2][27][0] = 0.5; z_pT_Bin_Borders[2][27][1] = 0.38; z_pT_Bin_Borders[2][27][2] = 0.45; z_pT_Bin_Borders[2][27][3] = 0.35;
Phi_h_Bin_Values[2][27][0] =  24; Phi_h_Bin_Values[2][27][1] = 532; Phi_h_Bin_Values[2][27][2] = 1262;
z_pT_Bin_Borders[2][28][0] = 0.5; z_pT_Bin_Borders[2][28][1] = 0.38; z_pT_Bin_Borders[2][28][2] = 0.54; z_pT_Bin_Borders[2][28][3] = 0.45;
Phi_h_Bin_Values[2][28][0] =  24; Phi_h_Bin_Values[2][28][1] = 556; Phi_h_Bin_Values[2][28][2] = 1286;
z_pT_Bin_Borders[2][29][0] = 0.5; z_pT_Bin_Borders[2][29][1] = 0.38; z_pT_Bin_Borders[2][29][2] = 0.67; z_pT_Bin_Borders[2][29][3] = 0.54;
Phi_h_Bin_Values[2][29][0] =  24; Phi_h_Bin_Values[2][29][1] = 580; Phi_h_Bin_Values[2][29][2] = 1310;
z_pT_Bin_Borders[2][30][0] = 0.5; z_pT_Bin_Borders[2][30][1] = 0.38; z_pT_Bin_Borders[2][30][2] = 0.93; z_pT_Bin_Borders[2][30][3] = 0.67;
Phi_h_Bin_Values[2][30][0] =  24; Phi_h_Bin_Values[2][30][1] = 604; Phi_h_Bin_Values[2][30][2] = 1334;
z_pT_Bin_Borders[2][31][0] = 0.75; z_pT_Bin_Borders[2][31][1] = 0.5; z_pT_Bin_Borders[2][31][2] = 0.25; z_pT_Bin_Borders[2][31][3] = 0.05;
Phi_h_Bin_Values[2][31][0] =  24; Phi_h_Bin_Values[2][31][1] = 628; Phi_h_Bin_Values[2][31][2] = 1358;
z_pT_Bin_Borders[2][32][0] = 0.75; z_pT_Bin_Borders[2][32][1] = 0.5; z_pT_Bin_Borders[2][32][2] = 0.35; z_pT_Bin_Borders[2][32][3] = 0.25;
Phi_h_Bin_Values[2][32][0] =  24; Phi_h_Bin_Values[2][32][1] = 652; Phi_h_Bin_Values[2][32][2] = 1382;
z_pT_Bin_Borders[2][33][0] = 0.75; z_pT_Bin_Borders[2][33][1] = 0.5; z_pT_Bin_Borders[2][33][2] = 0.45; z_pT_Bin_Borders[2][33][3] = 0.35;
Phi_h_Bin_Values[2][33][0] =  24; Phi_h_Bin_Values[2][33][1] = 676; Phi_h_Bin_Values[2][33][2] = 1406;
z_pT_Bin_Borders[2][34][0] = 0.75; z_pT_Bin_Borders[2][34][1] = 0.5; z_pT_Bin_Borders[2][34][2] = 0.54; z_pT_Bin_Borders[2][34][3] = 0.45;
Phi_h_Bin_Values[2][34][0] =  24; Phi_h_Bin_Values[2][34][1] = 700; Phi_h_Bin_Values[2][34][2] = 1430;
z_pT_Bin_Borders[2][35][0] = 0.75; z_pT_Bin_Borders[2][35][1] = 0.5; z_pT_Bin_Borders[2][35][2] = 0.67; z_pT_Bin_Borders[2][35][3] = 0.54;
Phi_h_Bin_Values[2][35][0] =  24; Phi_h_Bin_Values[2][35][1] = 724; Phi_h_Bin_Values[2][35][2] = 1454;
z_pT_Bin_Borders[2][36][0] = 0.75; z_pT_Bin_Borders[2][36][1] = 0.5; z_pT_Bin_Borders[2][36][2] = 0.93; z_pT_Bin_Borders[2][36][3] = 0.67;
Phi_h_Bin_Values[2][36][0] =  1; Phi_h_Bin_Values[2][36][1] = 748; Phi_h_Bin_Values[2][36][2] = 1478;
z_pT_Bin_Borders[2][37][0] = 0.19; z_pT_Bin_Borders[2][37][1] = 0; z_pT_Bin_Borders[2][37][2] = 0.05; z_pT_Bin_Borders[2][37][3] = 0;
Phi_h_Bin_Values[2][37][0] =  1; Phi_h_Bin_Values[2][37][1] = 749; Phi_h_Bin_Values[2][37][2] = 1479;
z_pT_Bin_Borders[2][38][0] = 0.19; z_pT_Bin_Borders[2][38][1] = 0; z_pT_Bin_Borders[2][38][2] = 0.05; z_pT_Bin_Borders[2][38][3] = 0.25;
Phi_h_Bin_Values[2][38][0] =  1; Phi_h_Bin_Values[2][38][1] = 750; Phi_h_Bin_Values[2][38][2] = 1480;
z_pT_Bin_Borders[2][39][0] = 0.19; z_pT_Bin_Borders[2][39][1] = 0; z_pT_Bin_Borders[2][39][2] = 0.25; z_pT_Bin_Borders[2][39][3] = 0.35;
Phi_h_Bin_Values[2][39][0] =  1; Phi_h_Bin_Values[2][39][1] = 751; Phi_h_Bin_Values[2][39][2] = 1481;
z_pT_Bin_Borders[2][40][0] = 0.19; z_pT_Bin_Borders[2][40][1] = 0; z_pT_Bin_Borders[2][40][2] = 0.35; z_pT_Bin_Borders[2][40][3] = 0.45;
Phi_h_Bin_Values[2][40][0] =  1; Phi_h_Bin_Values[2][40][1] = 752; Phi_h_Bin_Values[2][40][2] = 1482;
z_pT_Bin_Borders[2][41][0] = 0.19; z_pT_Bin_Borders[2][41][1] = 0; z_pT_Bin_Borders[2][41][2] = 0.45; z_pT_Bin_Borders[2][41][3] = 0.54;
Phi_h_Bin_Values[2][41][0] =  1; Phi_h_Bin_Values[2][41][1] = 753; Phi_h_Bin_Values[2][41][2] = 1483;
z_pT_Bin_Borders[2][42][0] = 0.19; z_pT_Bin_Borders[2][42][1] = 0; z_pT_Bin_Borders[2][42][2] = 0.54; z_pT_Bin_Borders[2][42][3] = 0.67;
Phi_h_Bin_Values[2][42][0] =  1; Phi_h_Bin_Values[2][42][1] = 754; Phi_h_Bin_Values[2][42][2] = 1484;
z_pT_Bin_Borders[2][43][0] = 0.19; z_pT_Bin_Borders[2][43][1] = 0; z_pT_Bin_Borders[2][43][2] = 0.67; z_pT_Bin_Borders[2][43][3] = 0.93;
Phi_h_Bin_Values[2][43][0] =  1; Phi_h_Bin_Values[2][43][1] = 755; Phi_h_Bin_Values[2][43][2] = 1485;
z_pT_Bin_Borders[2][44][0] = 0.19; z_pT_Bin_Borders[2][44][1] = 0; z_pT_Bin_Borders[2][44][2] = 10; z_pT_Bin_Borders[2][44][3] = 0.93;
Phi_h_Bin_Values[2][44][0] =  1; Phi_h_Bin_Values[2][44][1] = 756; Phi_h_Bin_Values[2][44][2] = 1486;
z_pT_Bin_Borders[2][45][0] = 0.19; z_pT_Bin_Borders[2][45][1] = 0.23; z_pT_Bin_Borders[2][45][2] = 0.05; z_pT_Bin_Borders[2][45][3] = 0;
Phi_h_Bin_Values[2][45][0] =  1; Phi_h_Bin_Values[2][45][1] = 757; Phi_h_Bin_Values[2][45][2] = 1487;
z_pT_Bin_Borders[2][46][0] = 0.19; z_pT_Bin_Borders[2][46][1] = 0.23; z_pT_Bin_Borders[2][46][2] = 10; z_pT_Bin_Borders[2][46][3] = 0.93;
Phi_h_Bin_Values[2][46][0] =  1; Phi_h_Bin_Values[2][46][1] = 758; Phi_h_Bin_Values[2][46][2] = 1488;
z_pT_Bin_Borders[2][47][0] = 0.23; z_pT_Bin_Borders[2][47][1] = 0.26; z_pT_Bin_Borders[2][47][2] = 0.05; z_pT_Bin_Borders[2][47][3] = 0;
Phi_h_Bin_Values[2][47][0] =  1; Phi_h_Bin_Values[2][47][1] = 759; Phi_h_Bin_Values[2][47][2] = 1489;
z_pT_Bin_Borders[2][48][0] = 0.23; z_pT_Bin_Borders[2][48][1] = 0.26; z_pT_Bin_Borders[2][48][2] = 10; z_pT_Bin_Borders[2][48][3] = 0.93;
Phi_h_Bin_Values[2][48][0] =  1; Phi_h_Bin_Values[2][48][1] = 760; Phi_h_Bin_Values[2][48][2] = 1490;
z_pT_Bin_Borders[2][49][0] = 0.26; z_pT_Bin_Borders[2][49][1] = 0.31; z_pT_Bin_Borders[2][49][2] = 0.05; z_pT_Bin_Borders[2][49][3] = 0;
Phi_h_Bin_Values[2][49][0] =  1; Phi_h_Bin_Values[2][49][1] = 761; Phi_h_Bin_Values[2][49][2] = 1491;
z_pT_Bin_Borders[2][50][0] = 0.26; z_pT_Bin_Borders[2][50][1] = 0.31; z_pT_Bin_Borders[2][50][2] = 10; z_pT_Bin_Borders[2][50][3] = 0.93;
Phi_h_Bin_Values[2][50][0] =  1; Phi_h_Bin_Values[2][50][1] = 762; Phi_h_Bin_Values[2][50][2] = 1492;
z_pT_Bin_Borders[2][51][0] = 0.31; z_pT_Bin_Borders[2][51][1] = 0.38; z_pT_Bin_Borders[2][51][2] = 0.05; z_pT_Bin_Borders[2][51][3] = 0;
Phi_h_Bin_Values[2][51][0] =  1; Phi_h_Bin_Values[2][51][1] = 763; Phi_h_Bin_Values[2][51][2] = 1493;
z_pT_Bin_Borders[2][52][0] = 0.31; z_pT_Bin_Borders[2][52][1] = 0.38; z_pT_Bin_Borders[2][52][2] = 10; z_pT_Bin_Borders[2][52][3] = 0.93;
Phi_h_Bin_Values[2][52][0] =  1; Phi_h_Bin_Values[2][52][1] = 764; Phi_h_Bin_Values[2][52][2] = 1494;
z_pT_Bin_Borders[2][53][0] = 0.38; z_pT_Bin_Borders[2][53][1] = 0.5; z_pT_Bin_Borders[2][53][2] = 0.05; z_pT_Bin_Borders[2][53][3] = 0;
Phi_h_Bin_Values[2][53][0] =  1; Phi_h_Bin_Values[2][53][1] = 765; Phi_h_Bin_Values[2][53][2] = 1495;
z_pT_Bin_Borders[2][54][0] = 0.38; z_pT_Bin_Borders[2][54][1] = 0.5; z_pT_Bin_Borders[2][54][2] = 10; z_pT_Bin_Borders[2][54][3] = 0.93;
Phi_h_Bin_Values[2][54][0] =  1; Phi_h_Bin_Values[2][54][1] = 766; Phi_h_Bin_Values[2][54][2] = 1496;
z_pT_Bin_Borders[2][55][0] = 0.5; z_pT_Bin_Borders[2][55][1] = 0.75; z_pT_Bin_Borders[2][55][2] = 0.05; z_pT_Bin_Borders[2][55][3] = 0;
Phi_h_Bin_Values[2][55][0] =  1; Phi_h_Bin_Values[2][55][1] = 767; Phi_h_Bin_Values[2][55][2] = 1497;
z_pT_Bin_Borders[2][56][0] = 0.5; z_pT_Bin_Borders[2][56][1] = 0.75; z_pT_Bin_Borders[2][56][2] = 10; z_pT_Bin_Borders[2][56][3] = 0.93;
Phi_h_Bin_Values[2][56][0] =  1; Phi_h_Bin_Values[2][56][1] = 768; Phi_h_Bin_Values[2][56][2] = 1498;
z_pT_Bin_Borders[2][57][0] = 10; z_pT_Bin_Borders[2][57][1] = 0.75; z_pT_Bin_Borders[2][57][2] = 0; z_pT_Bin_Borders[2][57][3] = 0.05;
Phi_h_Bin_Values[2][57][0] =  1; Phi_h_Bin_Values[2][57][1] = 769; Phi_h_Bin_Values[2][57][2] = 1499;
z_pT_Bin_Borders[2][58][0] = 10; z_pT_Bin_Borders[2][58][1] = 0.75; z_pT_Bin_Borders[2][58][2] = 0.05; z_pT_Bin_Borders[2][58][3] = 0.25;
Phi_h_Bin_Values[2][58][0] =  1; Phi_h_Bin_Values[2][58][1] = 770; Phi_h_Bin_Values[2][58][2] = 1500;
z_pT_Bin_Borders[2][59][0] = 10; z_pT_Bin_Borders[2][59][1] = 0.75; z_pT_Bin_Borders[2][59][2] = 0.25; z_pT_Bin_Borders[2][59][3] = 0.35;
Phi_h_Bin_Values[2][59][0] =  1; Phi_h_Bin_Values[2][59][1] = 771; Phi_h_Bin_Values[2][59][2] = 1501;
z_pT_Bin_Borders[2][60][0] = 10; z_pT_Bin_Borders[2][60][1] = 0.75; z_pT_Bin_Borders[2][60][2] = 0.35; z_pT_Bin_Borders[2][60][3] = 0.45;
Phi_h_Bin_Values[2][60][0] =  1; Phi_h_Bin_Values[2][60][1] = 772; Phi_h_Bin_Values[2][60][2] = 1502;
z_pT_Bin_Borders[2][61][0] = 10; z_pT_Bin_Borders[2][61][1] = 0.75; z_pT_Bin_Borders[2][61][2] = 0.45; z_pT_Bin_Borders[2][61][3] = 0.54;
Phi_h_Bin_Values[2][61][0] =  1; Phi_h_Bin_Values[2][61][1] = 773; Phi_h_Bin_Values[2][61][2] = 1503;
z_pT_Bin_Borders[2][62][0] = 10; z_pT_Bin_Borders[2][62][1] = 0.75; z_pT_Bin_Borders[2][62][2] = 0.54; z_pT_Bin_Borders[2][62][3] = 0.67;
Phi_h_Bin_Values[2][62][0] =  1; Phi_h_Bin_Values[2][62][1] = 774; Phi_h_Bin_Values[2][62][2] = 1504;
z_pT_Bin_Borders[2][63][0] = 10; z_pT_Bin_Borders[2][63][1] = 0.75; z_pT_Bin_Borders[2][63][2] = 0.67; z_pT_Bin_Borders[2][63][3] = 0.93;
Phi_h_Bin_Values[2][63][0] =  1; Phi_h_Bin_Values[2][63][1] = 775; Phi_h_Bin_Values[2][63][2] = 1505;
z_pT_Bin_Borders[2][64][0] = 10; z_pT_Bin_Borders[2][64][1] = 0.75; z_pT_Bin_Borders[2][64][2] = 10; z_pT_Bin_Borders[2][64][3] = 0.93;
Phi_h_Bin_Values[2][64][0] =  1; Phi_h_Bin_Values[2][64][1] = 776; Phi_h_Bin_Values[2][64][2] = 1506;
z_pT_Bin_Borders[3][1][0] = 0.28; z_pT_Bin_Borders[3][1][1] = 0.22; z_pT_Bin_Borders[3][1][2] = 0.2; z_pT_Bin_Borders[3][1][3] = 0.05;
Phi_h_Bin_Values[3][1][0] =  24; Phi_h_Bin_Values[3][1][1] = 0; Phi_h_Bin_Values[3][1][2] = 1507;
z_pT_Bin_Borders[3][2][0] = 0.28; z_pT_Bin_Borders[3][2][1] = 0.22; z_pT_Bin_Borders[3][2][2] = 0.3; z_pT_Bin_Borders[3][2][3] = 0.2;
Phi_h_Bin_Values[3][2][0] =  24; Phi_h_Bin_Values[3][2][1] = 24; Phi_h_Bin_Values[3][2][2] = 1531;
z_pT_Bin_Borders[3][3][0] = 0.28; z_pT_Bin_Borders[3][3][1] = 0.22; z_pT_Bin_Borders[3][3][2] = 0.4; z_pT_Bin_Borders[3][3][3] = 0.3;
Phi_h_Bin_Values[3][3][0] =  24; Phi_h_Bin_Values[3][3][1] = 48; Phi_h_Bin_Values[3][3][2] = 1555;
z_pT_Bin_Borders[3][4][0] = 0.28; z_pT_Bin_Borders[3][4][1] = 0.22; z_pT_Bin_Borders[3][4][2] = 0.5; z_pT_Bin_Borders[3][4][3] = 0.4;
Phi_h_Bin_Values[3][4][0] =  24; Phi_h_Bin_Values[3][4][1] = 72; Phi_h_Bin_Values[3][4][2] = 1579;
z_pT_Bin_Borders[3][5][0] = 0.28; z_pT_Bin_Borders[3][5][1] = 0.22; z_pT_Bin_Borders[3][5][2] = 0.6; z_pT_Bin_Borders[3][5][3] = 0.5;
Phi_h_Bin_Values[3][5][0] =  24; Phi_h_Bin_Values[3][5][1] = 96; Phi_h_Bin_Values[3][5][2] = 1603;
z_pT_Bin_Borders[3][6][0] = 0.28; z_pT_Bin_Borders[3][6][1] = 0.22; z_pT_Bin_Borders[3][6][2] = 0.75; z_pT_Bin_Borders[3][6][3] = 0.6;
Phi_h_Bin_Values[3][6][0] =  1; Phi_h_Bin_Values[3][6][1] = 120; Phi_h_Bin_Values[3][6][2] = 1627;
z_pT_Bin_Borders[3][7][0] = 0.35; z_pT_Bin_Borders[3][7][1] = 0.28; z_pT_Bin_Borders[3][7][2] = 0.2; z_pT_Bin_Borders[3][7][3] = 0.05;
Phi_h_Bin_Values[3][7][0] =  24; Phi_h_Bin_Values[3][7][1] = 121; Phi_h_Bin_Values[3][7][2] = 1628;
z_pT_Bin_Borders[3][8][0] = 0.35; z_pT_Bin_Borders[3][8][1] = 0.28; z_pT_Bin_Borders[3][8][2] = 0.3; z_pT_Bin_Borders[3][8][3] = 0.2;
Phi_h_Bin_Values[3][8][0] =  24; Phi_h_Bin_Values[3][8][1] = 145; Phi_h_Bin_Values[3][8][2] = 1652;
z_pT_Bin_Borders[3][9][0] = 0.35; z_pT_Bin_Borders[3][9][1] = 0.28; z_pT_Bin_Borders[3][9][2] = 0.4; z_pT_Bin_Borders[3][9][3] = 0.3;
Phi_h_Bin_Values[3][9][0] =  24; Phi_h_Bin_Values[3][9][1] = 169; Phi_h_Bin_Values[3][9][2] = 1676;
z_pT_Bin_Borders[3][10][0] = 0.35; z_pT_Bin_Borders[3][10][1] = 0.28; z_pT_Bin_Borders[3][10][2] = 0.5; z_pT_Bin_Borders[3][10][3] = 0.4;
Phi_h_Bin_Values[3][10][0] =  24; Phi_h_Bin_Values[3][10][1] = 193; Phi_h_Bin_Values[3][10][2] = 1700;
z_pT_Bin_Borders[3][11][0] = 0.35; z_pT_Bin_Borders[3][11][1] = 0.28; z_pT_Bin_Borders[3][11][2] = 0.6; z_pT_Bin_Borders[3][11][3] = 0.5;
Phi_h_Bin_Values[3][11][0] =  24; Phi_h_Bin_Values[3][11][1] = 217; Phi_h_Bin_Values[3][11][2] = 1724;
z_pT_Bin_Borders[3][12][0] = 0.35; z_pT_Bin_Borders[3][12][1] = 0.28; z_pT_Bin_Borders[3][12][2] = 0.75; z_pT_Bin_Borders[3][12][3] = 0.6;
Phi_h_Bin_Values[3][12][0] =  24; Phi_h_Bin_Values[3][12][1] = 241; Phi_h_Bin_Values[3][12][2] = 1748;
z_pT_Bin_Borders[3][13][0] = 0.45; z_pT_Bin_Borders[3][13][1] = 0.35; z_pT_Bin_Borders[3][13][2] = 0.2; z_pT_Bin_Borders[3][13][3] = 0.05;
Phi_h_Bin_Values[3][13][0] =  24; Phi_h_Bin_Values[3][13][1] = 265; Phi_h_Bin_Values[3][13][2] = 1772;
z_pT_Bin_Borders[3][14][0] = 0.45; z_pT_Bin_Borders[3][14][1] = 0.35; z_pT_Bin_Borders[3][14][2] = 0.3; z_pT_Bin_Borders[3][14][3] = 0.2;
Phi_h_Bin_Values[3][14][0] =  24; Phi_h_Bin_Values[3][14][1] = 289; Phi_h_Bin_Values[3][14][2] = 1796;
z_pT_Bin_Borders[3][15][0] = 0.45; z_pT_Bin_Borders[3][15][1] = 0.35; z_pT_Bin_Borders[3][15][2] = 0.4; z_pT_Bin_Borders[3][15][3] = 0.3;
Phi_h_Bin_Values[3][15][0] =  24; Phi_h_Bin_Values[3][15][1] = 313; Phi_h_Bin_Values[3][15][2] = 1820;
z_pT_Bin_Borders[3][16][0] = 0.45; z_pT_Bin_Borders[3][16][1] = 0.35; z_pT_Bin_Borders[3][16][2] = 0.5; z_pT_Bin_Borders[3][16][3] = 0.4;
Phi_h_Bin_Values[3][16][0] =  24; Phi_h_Bin_Values[3][16][1] = 337; Phi_h_Bin_Values[3][16][2] = 1844;
z_pT_Bin_Borders[3][17][0] = 0.45; z_pT_Bin_Borders[3][17][1] = 0.35; z_pT_Bin_Borders[3][17][2] = 0.6; z_pT_Bin_Borders[3][17][3] = 0.5;
Phi_h_Bin_Values[3][17][0] =  24; Phi_h_Bin_Values[3][17][1] = 361; Phi_h_Bin_Values[3][17][2] = 1868;
z_pT_Bin_Borders[3][18][0] = 0.45; z_pT_Bin_Borders[3][18][1] = 0.35; z_pT_Bin_Borders[3][18][2] = 0.75; z_pT_Bin_Borders[3][18][3] = 0.6;
Phi_h_Bin_Values[3][18][0] =  24; Phi_h_Bin_Values[3][18][1] = 385; Phi_h_Bin_Values[3][18][2] = 1892;
z_pT_Bin_Borders[3][19][0] = 0.7; z_pT_Bin_Borders[3][19][1] = 0.45; z_pT_Bin_Borders[3][19][2] = 0.2; z_pT_Bin_Borders[3][19][3] = 0.05;
Phi_h_Bin_Values[3][19][0] =  24; Phi_h_Bin_Values[3][19][1] = 409; Phi_h_Bin_Values[3][19][2] = 1916;
z_pT_Bin_Borders[3][20][0] = 0.7; z_pT_Bin_Borders[3][20][1] = 0.45; z_pT_Bin_Borders[3][20][2] = 0.3; z_pT_Bin_Borders[3][20][3] = 0.2;
Phi_h_Bin_Values[3][20][0] =  24; Phi_h_Bin_Values[3][20][1] = 433; Phi_h_Bin_Values[3][20][2] = 1940;
z_pT_Bin_Borders[3][21][0] = 0.7; z_pT_Bin_Borders[3][21][1] = 0.45; z_pT_Bin_Borders[3][21][2] = 0.4; z_pT_Bin_Borders[3][21][3] = 0.3;
Phi_h_Bin_Values[3][21][0] =  24; Phi_h_Bin_Values[3][21][1] = 457; Phi_h_Bin_Values[3][21][2] = 1964;
z_pT_Bin_Borders[3][22][0] = 0.7; z_pT_Bin_Borders[3][22][1] = 0.45; z_pT_Bin_Borders[3][22][2] = 0.5; z_pT_Bin_Borders[3][22][3] = 0.4;
Phi_h_Bin_Values[3][22][0] =  24; Phi_h_Bin_Values[3][22][1] = 481; Phi_h_Bin_Values[3][22][2] = 1988;
z_pT_Bin_Borders[3][23][0] = 0.7; z_pT_Bin_Borders[3][23][1] = 0.45; z_pT_Bin_Borders[3][23][2] = 0.6; z_pT_Bin_Borders[3][23][3] = 0.5;
Phi_h_Bin_Values[3][23][0] =  24; Phi_h_Bin_Values[3][23][1] = 505; Phi_h_Bin_Values[3][23][2] = 2012;
z_pT_Bin_Borders[3][24][0] = 0.7; z_pT_Bin_Borders[3][24][1] = 0.45; z_pT_Bin_Borders[3][24][2] = 0.75; z_pT_Bin_Borders[3][24][3] = 0.6;
Phi_h_Bin_Values[3][24][0] =  1; Phi_h_Bin_Values[3][24][1] = 529; Phi_h_Bin_Values[3][24][2] = 2036;
z_pT_Bin_Borders[3][25][0] = 0.22; z_pT_Bin_Borders[3][25][1] = 0; z_pT_Bin_Borders[3][25][2] = 0.05; z_pT_Bin_Borders[3][25][3] = 0;
Phi_h_Bin_Values[3][25][0] =  1; Phi_h_Bin_Values[3][25][1] = 530; Phi_h_Bin_Values[3][25][2] = 2037;
z_pT_Bin_Borders[3][26][0] = 0.22; z_pT_Bin_Borders[3][26][1] = 0; z_pT_Bin_Borders[3][26][2] = 0.05; z_pT_Bin_Borders[3][26][3] = 0.2;
Phi_h_Bin_Values[3][26][0] =  1; Phi_h_Bin_Values[3][26][1] = 531; Phi_h_Bin_Values[3][26][2] = 2038;
z_pT_Bin_Borders[3][27][0] = 0.22; z_pT_Bin_Borders[3][27][1] = 0; z_pT_Bin_Borders[3][27][2] = 0.2; z_pT_Bin_Borders[3][27][3] = 0.3;
Phi_h_Bin_Values[3][27][0] =  1; Phi_h_Bin_Values[3][27][1] = 532; Phi_h_Bin_Values[3][27][2] = 2039;
z_pT_Bin_Borders[3][28][0] = 0.22; z_pT_Bin_Borders[3][28][1] = 0; z_pT_Bin_Borders[3][28][2] = 0.3; z_pT_Bin_Borders[3][28][3] = 0.4;
Phi_h_Bin_Values[3][28][0] =  1; Phi_h_Bin_Values[3][28][1] = 533; Phi_h_Bin_Values[3][28][2] = 2040;
z_pT_Bin_Borders[3][29][0] = 0.22; z_pT_Bin_Borders[3][29][1] = 0; z_pT_Bin_Borders[3][29][2] = 0.4; z_pT_Bin_Borders[3][29][3] = 0.5;
Phi_h_Bin_Values[3][29][0] =  1; Phi_h_Bin_Values[3][29][1] = 534; Phi_h_Bin_Values[3][29][2] = 2041;
z_pT_Bin_Borders[3][30][0] = 0.22; z_pT_Bin_Borders[3][30][1] = 0; z_pT_Bin_Borders[3][30][2] = 0.5; z_pT_Bin_Borders[3][30][3] = 0.6;
Phi_h_Bin_Values[3][30][0] =  1; Phi_h_Bin_Values[3][30][1] = 535; Phi_h_Bin_Values[3][30][2] = 2042;
z_pT_Bin_Borders[3][31][0] = 0.22; z_pT_Bin_Borders[3][31][1] = 0; z_pT_Bin_Borders[3][31][2] = 0.6; z_pT_Bin_Borders[3][31][3] = 0.75;
Phi_h_Bin_Values[3][31][0] =  1; Phi_h_Bin_Values[3][31][1] = 536; Phi_h_Bin_Values[3][31][2] = 2043;
z_pT_Bin_Borders[3][32][0] = 0.22; z_pT_Bin_Borders[3][32][1] = 0; z_pT_Bin_Borders[3][32][2] = 10; z_pT_Bin_Borders[3][32][3] = 0.75;
Phi_h_Bin_Values[3][32][0] =  1; Phi_h_Bin_Values[3][32][1] = 537; Phi_h_Bin_Values[3][32][2] = 2044;
z_pT_Bin_Borders[3][33][0] = 0.22; z_pT_Bin_Borders[3][33][1] = 0.28; z_pT_Bin_Borders[3][33][2] = 0.05; z_pT_Bin_Borders[3][33][3] = 0;
Phi_h_Bin_Values[3][33][0] =  1; Phi_h_Bin_Values[3][33][1] = 538; Phi_h_Bin_Values[3][33][2] = 2045;
z_pT_Bin_Borders[3][34][0] = 0.22; z_pT_Bin_Borders[3][34][1] = 0.28; z_pT_Bin_Borders[3][34][2] = 10; z_pT_Bin_Borders[3][34][3] = 0.75;
Phi_h_Bin_Values[3][34][0] =  1; Phi_h_Bin_Values[3][34][1] = 539; Phi_h_Bin_Values[3][34][2] = 2046;
z_pT_Bin_Borders[3][35][0] = 0.28; z_pT_Bin_Borders[3][35][1] = 0.35; z_pT_Bin_Borders[3][35][2] = 0.05; z_pT_Bin_Borders[3][35][3] = 0;
Phi_h_Bin_Values[3][35][0] =  1; Phi_h_Bin_Values[3][35][1] = 540; Phi_h_Bin_Values[3][35][2] = 2047;
z_pT_Bin_Borders[3][36][0] = 0.28; z_pT_Bin_Borders[3][36][1] = 0.35; z_pT_Bin_Borders[3][36][2] = 10; z_pT_Bin_Borders[3][36][3] = 0.75;
Phi_h_Bin_Values[3][36][0] =  1; Phi_h_Bin_Values[3][36][1] = 541; Phi_h_Bin_Values[3][36][2] = 2048;
z_pT_Bin_Borders[3][37][0] = 0.35; z_pT_Bin_Borders[3][37][1] = 0.45; z_pT_Bin_Borders[3][37][2] = 0.05; z_pT_Bin_Borders[3][37][3] = 0;
Phi_h_Bin_Values[3][37][0] =  1; Phi_h_Bin_Values[3][37][1] = 542; Phi_h_Bin_Values[3][37][2] = 2049;
z_pT_Bin_Borders[3][38][0] = 0.35; z_pT_Bin_Borders[3][38][1] = 0.45; z_pT_Bin_Borders[3][38][2] = 10; z_pT_Bin_Borders[3][38][3] = 0.75;
Phi_h_Bin_Values[3][38][0] =  1; Phi_h_Bin_Values[3][38][1] = 543; Phi_h_Bin_Values[3][38][2] = 2050;
z_pT_Bin_Borders[3][39][0] = 0.45; z_pT_Bin_Borders[3][39][1] = 0.7; z_pT_Bin_Borders[3][39][2] = 0.05; z_pT_Bin_Borders[3][39][3] = 0;
Phi_h_Bin_Values[3][39][0] =  1; Phi_h_Bin_Values[3][39][1] = 544; Phi_h_Bin_Values[3][39][2] = 2051;
z_pT_Bin_Borders[3][40][0] = 0.45; z_pT_Bin_Borders[3][40][1] = 0.7; z_pT_Bin_Borders[3][40][2] = 10; z_pT_Bin_Borders[3][40][3] = 0.75;
Phi_h_Bin_Values[3][40][0] =  1; Phi_h_Bin_Values[3][40][1] = 545; Phi_h_Bin_Values[3][40][2] = 2052;
z_pT_Bin_Borders[3][41][0] = 10; z_pT_Bin_Borders[3][41][1] = 0.7; z_pT_Bin_Borders[3][41][2] = 0; z_pT_Bin_Borders[3][41][3] = 0.05;
Phi_h_Bin_Values[3][41][0] =  1; Phi_h_Bin_Values[3][41][1] = 546; Phi_h_Bin_Values[3][41][2] = 2053;
z_pT_Bin_Borders[3][42][0] = 10; z_pT_Bin_Borders[3][42][1] = 0.7; z_pT_Bin_Borders[3][42][2] = 0.05; z_pT_Bin_Borders[3][42][3] = 0.2;
Phi_h_Bin_Values[3][42][0] =  1; Phi_h_Bin_Values[3][42][1] = 547; Phi_h_Bin_Values[3][42][2] = 2054;
z_pT_Bin_Borders[3][43][0] = 10; z_pT_Bin_Borders[3][43][1] = 0.7; z_pT_Bin_Borders[3][43][2] = 0.2; z_pT_Bin_Borders[3][43][3] = 0.3;
Phi_h_Bin_Values[3][43][0] =  1; Phi_h_Bin_Values[3][43][1] = 548; Phi_h_Bin_Values[3][43][2] = 2055;
z_pT_Bin_Borders[3][44][0] = 10; z_pT_Bin_Borders[3][44][1] = 0.7; z_pT_Bin_Borders[3][44][2] = 0.3; z_pT_Bin_Borders[3][44][3] = 0.4;
Phi_h_Bin_Values[3][44][0] =  1; Phi_h_Bin_Values[3][44][1] = 549; Phi_h_Bin_Values[3][44][2] = 2056;
z_pT_Bin_Borders[3][45][0] = 10; z_pT_Bin_Borders[3][45][1] = 0.7; z_pT_Bin_Borders[3][45][2] = 0.4; z_pT_Bin_Borders[3][45][3] = 0.5;
Phi_h_Bin_Values[3][45][0] =  1; Phi_h_Bin_Values[3][45][1] = 550; Phi_h_Bin_Values[3][45][2] = 2057;
z_pT_Bin_Borders[3][46][0] = 10; z_pT_Bin_Borders[3][46][1] = 0.7; z_pT_Bin_Borders[3][46][2] = 0.5; z_pT_Bin_Borders[3][46][3] = 0.6;
Phi_h_Bin_Values[3][46][0] =  1; Phi_h_Bin_Values[3][46][1] = 551; Phi_h_Bin_Values[3][46][2] = 2058;
z_pT_Bin_Borders[3][47][0] = 10; z_pT_Bin_Borders[3][47][1] = 0.7; z_pT_Bin_Borders[3][47][2] = 0.6; z_pT_Bin_Borders[3][47][3] = 0.75;
Phi_h_Bin_Values[3][47][0] =  1; Phi_h_Bin_Values[3][47][1] = 552; Phi_h_Bin_Values[3][47][2] = 2059;
z_pT_Bin_Borders[3][48][0] = 10; z_pT_Bin_Borders[3][48][1] = 0.7; z_pT_Bin_Borders[3][48][2] = 10; z_pT_Bin_Borders[3][48][3] = 0.75;
Phi_h_Bin_Values[3][48][0] =  1; Phi_h_Bin_Values[3][48][1] = 553; Phi_h_Bin_Values[3][48][2] = 2060;
z_pT_Bin_Borders[4][1][0] = 0.34; z_pT_Bin_Borders[4][1][1] = 0.26; z_pT_Bin_Borders[4][1][2] = 0.2; z_pT_Bin_Borders[4][1][3] = 0.05;
Phi_h_Bin_Values[4][1][0] =  24; Phi_h_Bin_Values[4][1][1] = 0; Phi_h_Bin_Values[4][1][2] = 2061;
z_pT_Bin_Borders[4][2][0] = 0.34; z_pT_Bin_Borders[4][2][1] = 0.26; z_pT_Bin_Borders[4][2][2] = 0.29; z_pT_Bin_Borders[4][2][3] = 0.2;
Phi_h_Bin_Values[4][2][0] =  24; Phi_h_Bin_Values[4][2][1] = 24; Phi_h_Bin_Values[4][2][2] = 2085;
z_pT_Bin_Borders[4][3][0] = 0.34; z_pT_Bin_Borders[4][3][1] = 0.26; z_pT_Bin_Borders[4][3][2] = 0.38; z_pT_Bin_Borders[4][3][3] = 0.29;
Phi_h_Bin_Values[4][3][0] =  24; Phi_h_Bin_Values[4][3][1] = 48; Phi_h_Bin_Values[4][3][2] = 2109;
z_pT_Bin_Borders[4][4][0] = 0.34; z_pT_Bin_Borders[4][4][1] = 0.26; z_pT_Bin_Borders[4][4][2] = 0.48; z_pT_Bin_Borders[4][4][3] = 0.38;
Phi_h_Bin_Values[4][4][0] =  24; Phi_h_Bin_Values[4][4][1] = 72; Phi_h_Bin_Values[4][4][2] = 2133;
z_pT_Bin_Borders[4][5][0] = 0.34; z_pT_Bin_Borders[4][5][1] = 0.26; z_pT_Bin_Borders[4][5][2] = 0.61; z_pT_Bin_Borders[4][5][3] = 0.48;
Phi_h_Bin_Values[4][5][0] =  24; Phi_h_Bin_Values[4][5][1] = 96; Phi_h_Bin_Values[4][5][2] = 2157;
z_pT_Bin_Borders[4][6][0] = 0.38; z_pT_Bin_Borders[4][6][1] = 0.34; z_pT_Bin_Borders[4][6][2] = 0.2; z_pT_Bin_Borders[4][6][3] = 0.05;
Phi_h_Bin_Values[4][6][0] =  24; Phi_h_Bin_Values[4][6][1] = 120; Phi_h_Bin_Values[4][6][2] = 2181;
z_pT_Bin_Borders[4][7][0] = 0.38; z_pT_Bin_Borders[4][7][1] = 0.34; z_pT_Bin_Borders[4][7][2] = 0.29; z_pT_Bin_Borders[4][7][3] = 0.2;
Phi_h_Bin_Values[4][7][0] =  24; Phi_h_Bin_Values[4][7][1] = 144; Phi_h_Bin_Values[4][7][2] = 2205;
z_pT_Bin_Borders[4][8][0] = 0.38; z_pT_Bin_Borders[4][8][1] = 0.34; z_pT_Bin_Borders[4][8][2] = 0.38; z_pT_Bin_Borders[4][8][3] = 0.29;
Phi_h_Bin_Values[4][8][0] =  24; Phi_h_Bin_Values[4][8][1] = 168; Phi_h_Bin_Values[4][8][2] = 2229;
z_pT_Bin_Borders[4][9][0] = 0.38; z_pT_Bin_Borders[4][9][1] = 0.34; z_pT_Bin_Borders[4][9][2] = 0.48; z_pT_Bin_Borders[4][9][3] = 0.38;
Phi_h_Bin_Values[4][9][0] =  24; Phi_h_Bin_Values[4][9][1] = 192; Phi_h_Bin_Values[4][9][2] = 2253;
z_pT_Bin_Borders[4][10][0] = 0.38; z_pT_Bin_Borders[4][10][1] = 0.34; z_pT_Bin_Borders[4][10][2] = 0.61; z_pT_Bin_Borders[4][10][3] = 0.48;
Phi_h_Bin_Values[4][10][0] =  24; Phi_h_Bin_Values[4][10][1] = 216; Phi_h_Bin_Values[4][10][2] = 2277;
z_pT_Bin_Borders[4][11][0] = 0.43; z_pT_Bin_Borders[4][11][1] = 0.38; z_pT_Bin_Borders[4][11][2] = 0.2; z_pT_Bin_Borders[4][11][3] = 0.05;
Phi_h_Bin_Values[4][11][0] =  24; Phi_h_Bin_Values[4][11][1] = 240; Phi_h_Bin_Values[4][11][2] = 2301;
z_pT_Bin_Borders[4][12][0] = 0.43; z_pT_Bin_Borders[4][12][1] = 0.38; z_pT_Bin_Borders[4][12][2] = 0.29; z_pT_Bin_Borders[4][12][3] = 0.2;
Phi_h_Bin_Values[4][12][0] =  24; Phi_h_Bin_Values[4][12][1] = 264; Phi_h_Bin_Values[4][12][2] = 2325;
z_pT_Bin_Borders[4][13][0] = 0.43; z_pT_Bin_Borders[4][13][1] = 0.38; z_pT_Bin_Borders[4][13][2] = 0.38; z_pT_Bin_Borders[4][13][3] = 0.29;
Phi_h_Bin_Values[4][13][0] =  24; Phi_h_Bin_Values[4][13][1] = 288; Phi_h_Bin_Values[4][13][2] = 2349;
z_pT_Bin_Borders[4][14][0] = 0.43; z_pT_Bin_Borders[4][14][1] = 0.38; z_pT_Bin_Borders[4][14][2] = 0.48; z_pT_Bin_Borders[4][14][3] = 0.38;
Phi_h_Bin_Values[4][14][0] =  24; Phi_h_Bin_Values[4][14][1] = 312; Phi_h_Bin_Values[4][14][2] = 2373;
z_pT_Bin_Borders[4][15][0] = 0.43; z_pT_Bin_Borders[4][15][1] = 0.38; z_pT_Bin_Borders[4][15][2] = 0.61; z_pT_Bin_Borders[4][15][3] = 0.48;
Phi_h_Bin_Values[4][15][0] =  24; Phi_h_Bin_Values[4][15][1] = 336; Phi_h_Bin_Values[4][15][2] = 2397;
z_pT_Bin_Borders[4][16][0] = 0.5; z_pT_Bin_Borders[4][16][1] = 0.43; z_pT_Bin_Borders[4][16][2] = 0.2; z_pT_Bin_Borders[4][16][3] = 0.05;
Phi_h_Bin_Values[4][16][0] =  24; Phi_h_Bin_Values[4][16][1] = 360; Phi_h_Bin_Values[4][16][2] = 2421;
z_pT_Bin_Borders[4][17][0] = 0.5; z_pT_Bin_Borders[4][17][1] = 0.43; z_pT_Bin_Borders[4][17][2] = 0.29; z_pT_Bin_Borders[4][17][3] = 0.2;
Phi_h_Bin_Values[4][17][0] =  24; Phi_h_Bin_Values[4][17][1] = 384; Phi_h_Bin_Values[4][17][2] = 2445;
z_pT_Bin_Borders[4][18][0] = 0.5; z_pT_Bin_Borders[4][18][1] = 0.43; z_pT_Bin_Borders[4][18][2] = 0.38; z_pT_Bin_Borders[4][18][3] = 0.29;
Phi_h_Bin_Values[4][18][0] =  24; Phi_h_Bin_Values[4][18][1] = 408; Phi_h_Bin_Values[4][18][2] = 2469;
z_pT_Bin_Borders[4][19][0] = 0.5; z_pT_Bin_Borders[4][19][1] = 0.43; z_pT_Bin_Borders[4][19][2] = 0.48; z_pT_Bin_Borders[4][19][3] = 0.38;
Phi_h_Bin_Values[4][19][0] =  24; Phi_h_Bin_Values[4][19][1] = 432; Phi_h_Bin_Values[4][19][2] = 2493;
z_pT_Bin_Borders[4][20][0] = 0.5; z_pT_Bin_Borders[4][20][1] = 0.43; z_pT_Bin_Borders[4][20][2] = 0.61; z_pT_Bin_Borders[4][20][3] = 0.48;
Phi_h_Bin_Values[4][20][0] =  24; Phi_h_Bin_Values[4][20][1] = 456; Phi_h_Bin_Values[4][20][2] = 2517;
z_pT_Bin_Borders[4][21][0] = 0.6; z_pT_Bin_Borders[4][21][1] = 0.5; z_pT_Bin_Borders[4][21][2] = 0.2; z_pT_Bin_Borders[4][21][3] = 0.05;
Phi_h_Bin_Values[4][21][0] =  24; Phi_h_Bin_Values[4][21][1] = 480; Phi_h_Bin_Values[4][21][2] = 2541;
z_pT_Bin_Borders[4][22][0] = 0.6; z_pT_Bin_Borders[4][22][1] = 0.5; z_pT_Bin_Borders[4][22][2] = 0.29; z_pT_Bin_Borders[4][22][3] = 0.2;
Phi_h_Bin_Values[4][22][0] =  24; Phi_h_Bin_Values[4][22][1] = 504; Phi_h_Bin_Values[4][22][2] = 2565;
z_pT_Bin_Borders[4][23][0] = 0.6; z_pT_Bin_Borders[4][23][1] = 0.5; z_pT_Bin_Borders[4][23][2] = 0.38; z_pT_Bin_Borders[4][23][3] = 0.29;
Phi_h_Bin_Values[4][23][0] =  24; Phi_h_Bin_Values[4][23][1] = 528; Phi_h_Bin_Values[4][23][2] = 2589;
z_pT_Bin_Borders[4][24][0] = 0.6; z_pT_Bin_Borders[4][24][1] = 0.5; z_pT_Bin_Borders[4][24][2] = 0.48; z_pT_Bin_Borders[4][24][3] = 0.38;
Phi_h_Bin_Values[4][24][0] =  24; Phi_h_Bin_Values[4][24][1] = 552; Phi_h_Bin_Values[4][24][2] = 2613;
z_pT_Bin_Borders[4][25][0] = 0.6; z_pT_Bin_Borders[4][25][1] = 0.5; z_pT_Bin_Borders[4][25][2] = 0.61; z_pT_Bin_Borders[4][25][3] = 0.48;
Phi_h_Bin_Values[4][25][0] =  1; Phi_h_Bin_Values[4][25][1] = 576; Phi_h_Bin_Values[4][25][2] = 2637;
z_pT_Bin_Borders[4][26][0] = 0.26; z_pT_Bin_Borders[4][26][1] = 0; z_pT_Bin_Borders[4][26][2] = 0.05; z_pT_Bin_Borders[4][26][3] = 0;
Phi_h_Bin_Values[4][26][0] =  1; Phi_h_Bin_Values[4][26][1] = 577; Phi_h_Bin_Values[4][26][2] = 2638;
z_pT_Bin_Borders[4][27][0] = 0.26; z_pT_Bin_Borders[4][27][1] = 0; z_pT_Bin_Borders[4][27][2] = 0.05; z_pT_Bin_Borders[4][27][3] = 0.2;
Phi_h_Bin_Values[4][27][0] =  1; Phi_h_Bin_Values[4][27][1] = 578; Phi_h_Bin_Values[4][27][2] = 2639;
z_pT_Bin_Borders[4][28][0] = 0.26; z_pT_Bin_Borders[4][28][1] = 0; z_pT_Bin_Borders[4][28][2] = 0.2; z_pT_Bin_Borders[4][28][3] = 0.29;
Phi_h_Bin_Values[4][28][0] =  1; Phi_h_Bin_Values[4][28][1] = 579; Phi_h_Bin_Values[4][28][2] = 2640;
z_pT_Bin_Borders[4][29][0] = 0.26; z_pT_Bin_Borders[4][29][1] = 0; z_pT_Bin_Borders[4][29][2] = 0.29; z_pT_Bin_Borders[4][29][3] = 0.38;
Phi_h_Bin_Values[4][29][0] =  1; Phi_h_Bin_Values[4][29][1] = 580; Phi_h_Bin_Values[4][29][2] = 2641;
z_pT_Bin_Borders[4][30][0] = 0.26; z_pT_Bin_Borders[4][30][1] = 0; z_pT_Bin_Borders[4][30][2] = 0.38; z_pT_Bin_Borders[4][30][3] = 0.48;
Phi_h_Bin_Values[4][30][0] =  1; Phi_h_Bin_Values[4][30][1] = 581; Phi_h_Bin_Values[4][30][2] = 2642;
z_pT_Bin_Borders[4][31][0] = 0.26; z_pT_Bin_Borders[4][31][1] = 0; z_pT_Bin_Borders[4][31][2] = 0.48; z_pT_Bin_Borders[4][31][3] = 0.61;
Phi_h_Bin_Values[4][31][0] =  1; Phi_h_Bin_Values[4][31][1] = 582; Phi_h_Bin_Values[4][31][2] = 2643;
z_pT_Bin_Borders[4][32][0] = 0.26; z_pT_Bin_Borders[4][32][1] = 0; z_pT_Bin_Borders[4][32][2] = 10; z_pT_Bin_Borders[4][32][3] = 0.61;
Phi_h_Bin_Values[4][32][0] =  1; Phi_h_Bin_Values[4][32][1] = 583; Phi_h_Bin_Values[4][32][2] = 2644;
z_pT_Bin_Borders[4][33][0] = 0.26; z_pT_Bin_Borders[4][33][1] = 0.34; z_pT_Bin_Borders[4][33][2] = 0.05; z_pT_Bin_Borders[4][33][3] = 0;
Phi_h_Bin_Values[4][33][0] =  1; Phi_h_Bin_Values[4][33][1] = 584; Phi_h_Bin_Values[4][33][2] = 2645;
z_pT_Bin_Borders[4][34][0] = 0.26; z_pT_Bin_Borders[4][34][1] = 0.34; z_pT_Bin_Borders[4][34][2] = 10; z_pT_Bin_Borders[4][34][3] = 0.61;
Phi_h_Bin_Values[4][34][0] =  1; Phi_h_Bin_Values[4][34][1] = 585; Phi_h_Bin_Values[4][34][2] = 2646;
z_pT_Bin_Borders[4][35][0] = 0.34; z_pT_Bin_Borders[4][35][1] = 0.38; z_pT_Bin_Borders[4][35][2] = 0.05; z_pT_Bin_Borders[4][35][3] = 0;
Phi_h_Bin_Values[4][35][0] =  1; Phi_h_Bin_Values[4][35][1] = 586; Phi_h_Bin_Values[4][35][2] = 2647;
z_pT_Bin_Borders[4][36][0] = 0.34; z_pT_Bin_Borders[4][36][1] = 0.38; z_pT_Bin_Borders[4][36][2] = 10; z_pT_Bin_Borders[4][36][3] = 0.61;
Phi_h_Bin_Values[4][36][0] =  1; Phi_h_Bin_Values[4][36][1] = 587; Phi_h_Bin_Values[4][36][2] = 2648;
z_pT_Bin_Borders[4][37][0] = 0.38; z_pT_Bin_Borders[4][37][1] = 0.43; z_pT_Bin_Borders[4][37][2] = 0.05; z_pT_Bin_Borders[4][37][3] = 0;
Phi_h_Bin_Values[4][37][0] =  1; Phi_h_Bin_Values[4][37][1] = 588; Phi_h_Bin_Values[4][37][2] = 2649;
z_pT_Bin_Borders[4][38][0] = 0.38; z_pT_Bin_Borders[4][38][1] = 0.43; z_pT_Bin_Borders[4][38][2] = 10; z_pT_Bin_Borders[4][38][3] = 0.61;
Phi_h_Bin_Values[4][38][0] =  1; Phi_h_Bin_Values[4][38][1] = 589; Phi_h_Bin_Values[4][38][2] = 2650;
z_pT_Bin_Borders[4][39][0] = 0.43; z_pT_Bin_Borders[4][39][1] = 0.5; z_pT_Bin_Borders[4][39][2] = 0.05; z_pT_Bin_Borders[4][39][3] = 0;
Phi_h_Bin_Values[4][39][0] =  1; Phi_h_Bin_Values[4][39][1] = 590; Phi_h_Bin_Values[4][39][2] = 2651;
z_pT_Bin_Borders[4][40][0] = 0.43; z_pT_Bin_Borders[4][40][1] = 0.5; z_pT_Bin_Borders[4][40][2] = 10; z_pT_Bin_Borders[4][40][3] = 0.61;
Phi_h_Bin_Values[4][40][0] =  1; Phi_h_Bin_Values[4][40][1] = 591; Phi_h_Bin_Values[4][40][2] = 2652;
z_pT_Bin_Borders[4][41][0] = 0.5; z_pT_Bin_Borders[4][41][1] = 0.6; z_pT_Bin_Borders[4][41][2] = 0.05; z_pT_Bin_Borders[4][41][3] = 0;
Phi_h_Bin_Values[4][41][0] =  1; Phi_h_Bin_Values[4][41][1] = 592; Phi_h_Bin_Values[4][41][2] = 2653;
z_pT_Bin_Borders[4][42][0] = 0.5; z_pT_Bin_Borders[4][42][1] = 0.6; z_pT_Bin_Borders[4][42][2] = 10; z_pT_Bin_Borders[4][42][3] = 0.61;
Phi_h_Bin_Values[4][42][0] =  1; Phi_h_Bin_Values[4][42][1] = 593; Phi_h_Bin_Values[4][42][2] = 2654;
z_pT_Bin_Borders[4][43][0] = 10; z_pT_Bin_Borders[4][43][1] = 0.6; z_pT_Bin_Borders[4][43][2] = 0; z_pT_Bin_Borders[4][43][3] = 0.05;
Phi_h_Bin_Values[4][43][0] =  1; Phi_h_Bin_Values[4][43][1] = 594; Phi_h_Bin_Values[4][43][2] = 2655;
z_pT_Bin_Borders[4][44][0] = 10; z_pT_Bin_Borders[4][44][1] = 0.6; z_pT_Bin_Borders[4][44][2] = 0.05; z_pT_Bin_Borders[4][44][3] = 0.2;
Phi_h_Bin_Values[4][44][0] =  1; Phi_h_Bin_Values[4][44][1] = 595; Phi_h_Bin_Values[4][44][2] = 2656;
z_pT_Bin_Borders[4][45][0] = 10; z_pT_Bin_Borders[4][45][1] = 0.6; z_pT_Bin_Borders[4][45][2] = 0.2; z_pT_Bin_Borders[4][45][3] = 0.29;
Phi_h_Bin_Values[4][45][0] =  1; Phi_h_Bin_Values[4][45][1] = 596; Phi_h_Bin_Values[4][45][2] = 2657;
z_pT_Bin_Borders[4][46][0] = 10; z_pT_Bin_Borders[4][46][1] = 0.6; z_pT_Bin_Borders[4][46][2] = 0.29; z_pT_Bin_Borders[4][46][3] = 0.38;
Phi_h_Bin_Values[4][46][0] =  1; Phi_h_Bin_Values[4][46][1] = 597; Phi_h_Bin_Values[4][46][2] = 2658;
z_pT_Bin_Borders[4][47][0] = 10; z_pT_Bin_Borders[4][47][1] = 0.6; z_pT_Bin_Borders[4][47][2] = 0.38; z_pT_Bin_Borders[4][47][3] = 0.48;
Phi_h_Bin_Values[4][47][0] =  1; Phi_h_Bin_Values[4][47][1] = 598; Phi_h_Bin_Values[4][47][2] = 2659;
z_pT_Bin_Borders[4][48][0] = 10; z_pT_Bin_Borders[4][48][1] = 0.6; z_pT_Bin_Borders[4][48][2] = 0.48; z_pT_Bin_Borders[4][48][3] = 0.61;
Phi_h_Bin_Values[4][48][0] =  1; Phi_h_Bin_Values[4][48][1] = 599; Phi_h_Bin_Values[4][48][2] = 2660;
z_pT_Bin_Borders[4][49][0] = 10; z_pT_Bin_Borders[4][49][1] = 0.6; z_pT_Bin_Borders[4][49][2] = 10; z_pT_Bin_Borders[4][49][3] = 0.61;
Phi_h_Bin_Values[4][49][0] =  1; Phi_h_Bin_Values[4][49][1] = 600; Phi_h_Bin_Values[4][49][2] = 2661;
z_pT_Bin_Borders[5][1][0] = 0.2; z_pT_Bin_Borders[5][1][1] = 0.16; z_pT_Bin_Borders[5][1][2] = 0.22; z_pT_Bin_Borders[5][1][3] = 0.05;
Phi_h_Bin_Values[5][1][0] =  24; Phi_h_Bin_Values[5][1][1] = 0; Phi_h_Bin_Values[5][1][2] = 2662;
z_pT_Bin_Borders[5][2][0] = 0.2; z_pT_Bin_Borders[5][2][1] = 0.16; z_pT_Bin_Borders[5][2][2] = 0.32; z_pT_Bin_Borders[5][2][3] = 0.22;
Phi_h_Bin_Values[5][2][0] =  24; Phi_h_Bin_Values[5][2][1] = 24; Phi_h_Bin_Values[5][2][2] = 2686;
z_pT_Bin_Borders[5][3][0] = 0.2; z_pT_Bin_Borders[5][3][1] = 0.16; z_pT_Bin_Borders[5][3][2] = 0.41; z_pT_Bin_Borders[5][3][3] = 0.32;
Phi_h_Bin_Values[5][3][0] =  24; Phi_h_Bin_Values[5][3][1] = 48; Phi_h_Bin_Values[5][3][2] = 2710;
z_pT_Bin_Borders[5][4][0] = 0.2; z_pT_Bin_Borders[5][4][1] = 0.16; z_pT_Bin_Borders[5][4][2] = 0.51; z_pT_Bin_Borders[5][4][3] = 0.41;
Phi_h_Bin_Values[5][4][0] =  24; Phi_h_Bin_Values[5][4][1] = 72; Phi_h_Bin_Values[5][4][2] = 2734;
z_pT_Bin_Borders[5][5][0] = 0.2; z_pT_Bin_Borders[5][5][1] = 0.16; z_pT_Bin_Borders[5][5][2] = 0.65; z_pT_Bin_Borders[5][5][3] = 0.51;
Phi_h_Bin_Values[5][5][0] =  1; Phi_h_Bin_Values[5][5][1] = 96; Phi_h_Bin_Values[5][5][2] = 2758;
z_pT_Bin_Borders[5][6][0] = 0.2; z_pT_Bin_Borders[5][6][1] = 0.16; z_pT_Bin_Borders[5][6][2] = 0.98; z_pT_Bin_Borders[5][6][3] = 0.65;
Phi_h_Bin_Values[5][6][0] =  1; Phi_h_Bin_Values[5][6][1] = 97; Phi_h_Bin_Values[5][6][2] = 2759;
z_pT_Bin_Borders[5][7][0] = 0.24; z_pT_Bin_Borders[5][7][1] = 0.2; z_pT_Bin_Borders[5][7][2] = 0.22; z_pT_Bin_Borders[5][7][3] = 0.05;
Phi_h_Bin_Values[5][7][0] =  24; Phi_h_Bin_Values[5][7][1] = 98; Phi_h_Bin_Values[5][7][2] = 2760;
z_pT_Bin_Borders[5][8][0] = 0.24; z_pT_Bin_Borders[5][8][1] = 0.2; z_pT_Bin_Borders[5][8][2] = 0.32; z_pT_Bin_Borders[5][8][3] = 0.22;
Phi_h_Bin_Values[5][8][0] =  24; Phi_h_Bin_Values[5][8][1] = 122; Phi_h_Bin_Values[5][8][2] = 2784;
z_pT_Bin_Borders[5][9][0] = 0.24; z_pT_Bin_Borders[5][9][1] = 0.2; z_pT_Bin_Borders[5][9][2] = 0.41; z_pT_Bin_Borders[5][9][3] = 0.32;
Phi_h_Bin_Values[5][9][0] =  24; Phi_h_Bin_Values[5][9][1] = 146; Phi_h_Bin_Values[5][9][2] = 2808;
z_pT_Bin_Borders[5][10][0] = 0.24; z_pT_Bin_Borders[5][10][1] = 0.2; z_pT_Bin_Borders[5][10][2] = 0.51; z_pT_Bin_Borders[5][10][3] = 0.41;
Phi_h_Bin_Values[5][10][0] =  24; Phi_h_Bin_Values[5][10][1] = 170; Phi_h_Bin_Values[5][10][2] = 2832;
z_pT_Bin_Borders[5][11][0] = 0.24; z_pT_Bin_Borders[5][11][1] = 0.2; z_pT_Bin_Borders[5][11][2] = 0.65; z_pT_Bin_Borders[5][11][3] = 0.51;
Phi_h_Bin_Values[5][11][0] =  24; Phi_h_Bin_Values[5][11][1] = 194; Phi_h_Bin_Values[5][11][2] = 2856;
z_pT_Bin_Borders[5][12][0] = 0.24; z_pT_Bin_Borders[5][12][1] = 0.2; z_pT_Bin_Borders[5][12][2] = 0.98; z_pT_Bin_Borders[5][12][3] = 0.65;
Phi_h_Bin_Values[5][12][0] =  1; Phi_h_Bin_Values[5][12][1] = 218; Phi_h_Bin_Values[5][12][2] = 2880;
z_pT_Bin_Borders[5][13][0] = 0.3; z_pT_Bin_Borders[5][13][1] = 0.24; z_pT_Bin_Borders[5][13][2] = 0.22; z_pT_Bin_Borders[5][13][3] = 0.05;
Phi_h_Bin_Values[5][13][0] =  24; Phi_h_Bin_Values[5][13][1] = 219; Phi_h_Bin_Values[5][13][2] = 2881;
z_pT_Bin_Borders[5][14][0] = 0.3; z_pT_Bin_Borders[5][14][1] = 0.24; z_pT_Bin_Borders[5][14][2] = 0.32; z_pT_Bin_Borders[5][14][3] = 0.22;
Phi_h_Bin_Values[5][14][0] =  24; Phi_h_Bin_Values[5][14][1] = 243; Phi_h_Bin_Values[5][14][2] = 2905;
z_pT_Bin_Borders[5][15][0] = 0.3; z_pT_Bin_Borders[5][15][1] = 0.24; z_pT_Bin_Borders[5][15][2] = 0.41; z_pT_Bin_Borders[5][15][3] = 0.32;
Phi_h_Bin_Values[5][15][0] =  24; Phi_h_Bin_Values[5][15][1] = 267; Phi_h_Bin_Values[5][15][2] = 2929;
z_pT_Bin_Borders[5][16][0] = 0.3; z_pT_Bin_Borders[5][16][1] = 0.24; z_pT_Bin_Borders[5][16][2] = 0.51; z_pT_Bin_Borders[5][16][3] = 0.41;
Phi_h_Bin_Values[5][16][0] =  24; Phi_h_Bin_Values[5][16][1] = 291; Phi_h_Bin_Values[5][16][2] = 2953;
z_pT_Bin_Borders[5][17][0] = 0.3; z_pT_Bin_Borders[5][17][1] = 0.24; z_pT_Bin_Borders[5][17][2] = 0.65; z_pT_Bin_Borders[5][17][3] = 0.51;
Phi_h_Bin_Values[5][17][0] =  24; Phi_h_Bin_Values[5][17][1] = 315; Phi_h_Bin_Values[5][17][2] = 2977;
z_pT_Bin_Borders[5][18][0] = 0.3; z_pT_Bin_Borders[5][18][1] = 0.24; z_pT_Bin_Borders[5][18][2] = 0.98; z_pT_Bin_Borders[5][18][3] = 0.65;
Phi_h_Bin_Values[5][18][0] =  1; Phi_h_Bin_Values[5][18][1] = 339; Phi_h_Bin_Values[5][18][2] = 3001;
z_pT_Bin_Borders[5][19][0] = 0.38; z_pT_Bin_Borders[5][19][1] = 0.3; z_pT_Bin_Borders[5][19][2] = 0.22; z_pT_Bin_Borders[5][19][3] = 0.05;
Phi_h_Bin_Values[5][19][0] =  24; Phi_h_Bin_Values[5][19][1] = 340; Phi_h_Bin_Values[5][19][2] = 3002;
z_pT_Bin_Borders[5][20][0] = 0.38; z_pT_Bin_Borders[5][20][1] = 0.3; z_pT_Bin_Borders[5][20][2] = 0.32; z_pT_Bin_Borders[5][20][3] = 0.22;
Phi_h_Bin_Values[5][20][0] =  24; Phi_h_Bin_Values[5][20][1] = 364; Phi_h_Bin_Values[5][20][2] = 3026;
z_pT_Bin_Borders[5][21][0] = 0.38; z_pT_Bin_Borders[5][21][1] = 0.3; z_pT_Bin_Borders[5][21][2] = 0.41; z_pT_Bin_Borders[5][21][3] = 0.32;
Phi_h_Bin_Values[5][21][0] =  24; Phi_h_Bin_Values[5][21][1] = 388; Phi_h_Bin_Values[5][21][2] = 3050;
z_pT_Bin_Borders[5][22][0] = 0.38; z_pT_Bin_Borders[5][22][1] = 0.3; z_pT_Bin_Borders[5][22][2] = 0.51; z_pT_Bin_Borders[5][22][3] = 0.41;
Phi_h_Bin_Values[5][22][0] =  24; Phi_h_Bin_Values[5][22][1] = 412; Phi_h_Bin_Values[5][22][2] = 3074;
z_pT_Bin_Borders[5][23][0] = 0.38; z_pT_Bin_Borders[5][23][1] = 0.3; z_pT_Bin_Borders[5][23][2] = 0.65; z_pT_Bin_Borders[5][23][3] = 0.51;
Phi_h_Bin_Values[5][23][0] =  24; Phi_h_Bin_Values[5][23][1] = 436; Phi_h_Bin_Values[5][23][2] = 3098;
z_pT_Bin_Borders[5][24][0] = 0.38; z_pT_Bin_Borders[5][24][1] = 0.3; z_pT_Bin_Borders[5][24][2] = 0.98; z_pT_Bin_Borders[5][24][3] = 0.65;
Phi_h_Bin_Values[5][24][0] =  24; Phi_h_Bin_Values[5][24][1] = 460; Phi_h_Bin_Values[5][24][2] = 3122;
z_pT_Bin_Borders[5][25][0] = 0.49; z_pT_Bin_Borders[5][25][1] = 0.38; z_pT_Bin_Borders[5][25][2] = 0.22; z_pT_Bin_Borders[5][25][3] = 0.05;
Phi_h_Bin_Values[5][25][0] =  24; Phi_h_Bin_Values[5][25][1] = 484; Phi_h_Bin_Values[5][25][2] = 3146;
z_pT_Bin_Borders[5][26][0] = 0.49; z_pT_Bin_Borders[5][26][1] = 0.38; z_pT_Bin_Borders[5][26][2] = 0.32; z_pT_Bin_Borders[5][26][3] = 0.22;
Phi_h_Bin_Values[5][26][0] =  24; Phi_h_Bin_Values[5][26][1] = 508; Phi_h_Bin_Values[5][26][2] = 3170;
z_pT_Bin_Borders[5][27][0] = 0.49; z_pT_Bin_Borders[5][27][1] = 0.38; z_pT_Bin_Borders[5][27][2] = 0.41; z_pT_Bin_Borders[5][27][3] = 0.32;
Phi_h_Bin_Values[5][27][0] =  24; Phi_h_Bin_Values[5][27][1] = 532; Phi_h_Bin_Values[5][27][2] = 3194;
z_pT_Bin_Borders[5][28][0] = 0.49; z_pT_Bin_Borders[5][28][1] = 0.38; z_pT_Bin_Borders[5][28][2] = 0.51; z_pT_Bin_Borders[5][28][3] = 0.41;
Phi_h_Bin_Values[5][28][0] =  24; Phi_h_Bin_Values[5][28][1] = 556; Phi_h_Bin_Values[5][28][2] = 3218;
z_pT_Bin_Borders[5][29][0] = 0.49; z_pT_Bin_Borders[5][29][1] = 0.38; z_pT_Bin_Borders[5][29][2] = 0.65; z_pT_Bin_Borders[5][29][3] = 0.51;
Phi_h_Bin_Values[5][29][0] =  24; Phi_h_Bin_Values[5][29][1] = 580; Phi_h_Bin_Values[5][29][2] = 3242;
z_pT_Bin_Borders[5][30][0] = 0.49; z_pT_Bin_Borders[5][30][1] = 0.38; z_pT_Bin_Borders[5][30][2] = 0.98; z_pT_Bin_Borders[5][30][3] = 0.65;
Phi_h_Bin_Values[5][30][0] =  24; Phi_h_Bin_Values[5][30][1] = 604; Phi_h_Bin_Values[5][30][2] = 3266;
z_pT_Bin_Borders[5][31][0] = 0.72; z_pT_Bin_Borders[5][31][1] = 0.49; z_pT_Bin_Borders[5][31][2] = 0.22; z_pT_Bin_Borders[5][31][3] = 0.05;
Phi_h_Bin_Values[5][31][0] =  24; Phi_h_Bin_Values[5][31][1] = 628; Phi_h_Bin_Values[5][31][2] = 3290;
z_pT_Bin_Borders[5][32][0] = 0.72; z_pT_Bin_Borders[5][32][1] = 0.49; z_pT_Bin_Borders[5][32][2] = 0.32; z_pT_Bin_Borders[5][32][3] = 0.22;
Phi_h_Bin_Values[5][32][0] =  24; Phi_h_Bin_Values[5][32][1] = 652; Phi_h_Bin_Values[5][32][2] = 3314;
z_pT_Bin_Borders[5][33][0] = 0.72; z_pT_Bin_Borders[5][33][1] = 0.49; z_pT_Bin_Borders[5][33][2] = 0.41; z_pT_Bin_Borders[5][33][3] = 0.32;
Phi_h_Bin_Values[5][33][0] =  24; Phi_h_Bin_Values[5][33][1] = 676; Phi_h_Bin_Values[5][33][2] = 3338;
z_pT_Bin_Borders[5][34][0] = 0.72; z_pT_Bin_Borders[5][34][1] = 0.49; z_pT_Bin_Borders[5][34][2] = 0.51; z_pT_Bin_Borders[5][34][3] = 0.41;
Phi_h_Bin_Values[5][34][0] =  24; Phi_h_Bin_Values[5][34][1] = 700; Phi_h_Bin_Values[5][34][2] = 3362;
z_pT_Bin_Borders[5][35][0] = 0.72; z_pT_Bin_Borders[5][35][1] = 0.49; z_pT_Bin_Borders[5][35][2] = 0.65; z_pT_Bin_Borders[5][35][3] = 0.51;
Phi_h_Bin_Values[5][35][0] =  24; Phi_h_Bin_Values[5][35][1] = 724; Phi_h_Bin_Values[5][35][2] = 3386;
z_pT_Bin_Borders[5][36][0] = 0.72; z_pT_Bin_Borders[5][36][1] = 0.49; z_pT_Bin_Borders[5][36][2] = 0.98; z_pT_Bin_Borders[5][36][3] = 0.65;
Phi_h_Bin_Values[5][36][0] =  24; Phi_h_Bin_Values[5][36][1] = 748; Phi_h_Bin_Values[5][36][2] = 3410;
z_pT_Bin_Borders[5][37][0] = 0.16; z_pT_Bin_Borders[5][37][1] = 0; z_pT_Bin_Borders[5][37][2] = 0.05; z_pT_Bin_Borders[5][37][3] = 0;
Phi_h_Bin_Values[5][37][0] =  1; Phi_h_Bin_Values[5][37][1] = 772; Phi_h_Bin_Values[5][37][2] = 3434;
z_pT_Bin_Borders[5][38][0] = 0.16; z_pT_Bin_Borders[5][38][1] = 0; z_pT_Bin_Borders[5][38][2] = 0.05; z_pT_Bin_Borders[5][38][3] = 0.22;
Phi_h_Bin_Values[5][38][0] =  1; Phi_h_Bin_Values[5][38][1] = 773; Phi_h_Bin_Values[5][38][2] = 3435;
z_pT_Bin_Borders[5][39][0] = 0.16; z_pT_Bin_Borders[5][39][1] = 0; z_pT_Bin_Borders[5][39][2] = 0.22; z_pT_Bin_Borders[5][39][3] = 0.32;
Phi_h_Bin_Values[5][39][0] =  1; Phi_h_Bin_Values[5][39][1] = 774; Phi_h_Bin_Values[5][39][2] = 3436;
z_pT_Bin_Borders[5][40][0] = 0.16; z_pT_Bin_Borders[5][40][1] = 0; z_pT_Bin_Borders[5][40][2] = 0.32; z_pT_Bin_Borders[5][40][3] = 0.41;
Phi_h_Bin_Values[5][40][0] =  1; Phi_h_Bin_Values[5][40][1] = 775; Phi_h_Bin_Values[5][40][2] = 3437;
z_pT_Bin_Borders[5][41][0] = 0.16; z_pT_Bin_Borders[5][41][1] = 0; z_pT_Bin_Borders[5][41][2] = 0.41; z_pT_Bin_Borders[5][41][3] = 0.51;
Phi_h_Bin_Values[5][41][0] =  1; Phi_h_Bin_Values[5][41][1] = 776; Phi_h_Bin_Values[5][41][2] = 3438;
z_pT_Bin_Borders[5][42][0] = 0.16; z_pT_Bin_Borders[5][42][1] = 0; z_pT_Bin_Borders[5][42][2] = 0.51; z_pT_Bin_Borders[5][42][3] = 0.65;
Phi_h_Bin_Values[5][42][0] =  1; Phi_h_Bin_Values[5][42][1] = 777; Phi_h_Bin_Values[5][42][2] = 3439;
z_pT_Bin_Borders[5][43][0] = 0.16; z_pT_Bin_Borders[5][43][1] = 0; z_pT_Bin_Borders[5][43][2] = 0.65; z_pT_Bin_Borders[5][43][3] = 0.98;
Phi_h_Bin_Values[5][43][0] =  1; Phi_h_Bin_Values[5][43][1] = 778; Phi_h_Bin_Values[5][43][2] = 3440;
z_pT_Bin_Borders[5][44][0] = 0.16; z_pT_Bin_Borders[5][44][1] = 0; z_pT_Bin_Borders[5][44][2] = 10; z_pT_Bin_Borders[5][44][3] = 0.98;
Phi_h_Bin_Values[5][44][0] =  1; Phi_h_Bin_Values[5][44][1] = 779; Phi_h_Bin_Values[5][44][2] = 3441;
z_pT_Bin_Borders[5][45][0] = 0.16; z_pT_Bin_Borders[5][45][1] = 0.2; z_pT_Bin_Borders[5][45][2] = 0.05; z_pT_Bin_Borders[5][45][3] = 0;
Phi_h_Bin_Values[5][45][0] =  1; Phi_h_Bin_Values[5][45][1] = 780; Phi_h_Bin_Values[5][45][2] = 3442;
z_pT_Bin_Borders[5][46][0] = 0.16; z_pT_Bin_Borders[5][46][1] = 0.2; z_pT_Bin_Borders[5][46][2] = 10; z_pT_Bin_Borders[5][46][3] = 0.98;
Phi_h_Bin_Values[5][46][0] =  1; Phi_h_Bin_Values[5][46][1] = 781; Phi_h_Bin_Values[5][46][2] = 3443;
z_pT_Bin_Borders[5][47][0] = 0.2; z_pT_Bin_Borders[5][47][1] = 0.24; z_pT_Bin_Borders[5][47][2] = 0.05; z_pT_Bin_Borders[5][47][3] = 0;
Phi_h_Bin_Values[5][47][0] =  1; Phi_h_Bin_Values[5][47][1] = 782; Phi_h_Bin_Values[5][47][2] = 3444;
z_pT_Bin_Borders[5][48][0] = 0.2; z_pT_Bin_Borders[5][48][1] = 0.24; z_pT_Bin_Borders[5][48][2] = 10; z_pT_Bin_Borders[5][48][3] = 0.98;
Phi_h_Bin_Values[5][48][0] =  1; Phi_h_Bin_Values[5][48][1] = 783; Phi_h_Bin_Values[5][48][2] = 3445;
z_pT_Bin_Borders[5][49][0] = 0.24; z_pT_Bin_Borders[5][49][1] = 0.3; z_pT_Bin_Borders[5][49][2] = 0.05; z_pT_Bin_Borders[5][49][3] = 0;
Phi_h_Bin_Values[5][49][0] =  1; Phi_h_Bin_Values[5][49][1] = 784; Phi_h_Bin_Values[5][49][2] = 3446;
z_pT_Bin_Borders[5][50][0] = 0.24; z_pT_Bin_Borders[5][50][1] = 0.3; z_pT_Bin_Borders[5][50][2] = 10; z_pT_Bin_Borders[5][50][3] = 0.98;
Phi_h_Bin_Values[5][50][0] =  1; Phi_h_Bin_Values[5][50][1] = 785; Phi_h_Bin_Values[5][50][2] = 3447;
z_pT_Bin_Borders[5][51][0] = 0.3; z_pT_Bin_Borders[5][51][1] = 0.38; z_pT_Bin_Borders[5][51][2] = 0.05; z_pT_Bin_Borders[5][51][3] = 0;
Phi_h_Bin_Values[5][51][0] =  1; Phi_h_Bin_Values[5][51][1] = 786; Phi_h_Bin_Values[5][51][2] = 3448;
z_pT_Bin_Borders[5][52][0] = 0.3; z_pT_Bin_Borders[5][52][1] = 0.38; z_pT_Bin_Borders[5][52][2] = 10; z_pT_Bin_Borders[5][52][3] = 0.98;
Phi_h_Bin_Values[5][52][0] =  1; Phi_h_Bin_Values[5][52][1] = 787; Phi_h_Bin_Values[5][52][2] = 3449;
z_pT_Bin_Borders[5][53][0] = 0.38; z_pT_Bin_Borders[5][53][1] = 0.49; z_pT_Bin_Borders[5][53][2] = 0.05; z_pT_Bin_Borders[5][53][3] = 0;
Phi_h_Bin_Values[5][53][0] =  1; Phi_h_Bin_Values[5][53][1] = 788; Phi_h_Bin_Values[5][53][2] = 3450;
z_pT_Bin_Borders[5][54][0] = 0.38; z_pT_Bin_Borders[5][54][1] = 0.49; z_pT_Bin_Borders[5][54][2] = 10; z_pT_Bin_Borders[5][54][3] = 0.98;
Phi_h_Bin_Values[5][54][0] =  1; Phi_h_Bin_Values[5][54][1] = 789; Phi_h_Bin_Values[5][54][2] = 3451;
z_pT_Bin_Borders[5][55][0] = 0.49; z_pT_Bin_Borders[5][55][1] = 0.72; z_pT_Bin_Borders[5][55][2] = 0.05; z_pT_Bin_Borders[5][55][3] = 0;
Phi_h_Bin_Values[5][55][0] =  1; Phi_h_Bin_Values[5][55][1] = 790; Phi_h_Bin_Values[5][55][2] = 3452;
z_pT_Bin_Borders[5][56][0] = 0.49; z_pT_Bin_Borders[5][56][1] = 0.72; z_pT_Bin_Borders[5][56][2] = 10; z_pT_Bin_Borders[5][56][3] = 0.98;
Phi_h_Bin_Values[5][56][0] =  1; Phi_h_Bin_Values[5][56][1] = 791; Phi_h_Bin_Values[5][56][2] = 3453;
z_pT_Bin_Borders[5][57][0] = 10; z_pT_Bin_Borders[5][57][1] = 0.72; z_pT_Bin_Borders[5][57][2] = 0; z_pT_Bin_Borders[5][57][3] = 0.05;
Phi_h_Bin_Values[5][57][0] =  1; Phi_h_Bin_Values[5][57][1] = 792; Phi_h_Bin_Values[5][57][2] = 3454;
z_pT_Bin_Borders[5][58][0] = 10; z_pT_Bin_Borders[5][58][1] = 0.72; z_pT_Bin_Borders[5][58][2] = 0.05; z_pT_Bin_Borders[5][58][3] = 0.22;
Phi_h_Bin_Values[5][58][0] =  1; Phi_h_Bin_Values[5][58][1] = 793; Phi_h_Bin_Values[5][58][2] = 3455;
z_pT_Bin_Borders[5][59][0] = 10; z_pT_Bin_Borders[5][59][1] = 0.72; z_pT_Bin_Borders[5][59][2] = 0.22; z_pT_Bin_Borders[5][59][3] = 0.32;
Phi_h_Bin_Values[5][59][0] =  1; Phi_h_Bin_Values[5][59][1] = 794; Phi_h_Bin_Values[5][59][2] = 3456;
z_pT_Bin_Borders[5][60][0] = 10; z_pT_Bin_Borders[5][60][1] = 0.72; z_pT_Bin_Borders[5][60][2] = 0.32; z_pT_Bin_Borders[5][60][3] = 0.41;
Phi_h_Bin_Values[5][60][0] =  1; Phi_h_Bin_Values[5][60][1] = 795; Phi_h_Bin_Values[5][60][2] = 3457;
z_pT_Bin_Borders[5][61][0] = 10; z_pT_Bin_Borders[5][61][1] = 0.72; z_pT_Bin_Borders[5][61][2] = 0.41; z_pT_Bin_Borders[5][61][3] = 0.51;
Phi_h_Bin_Values[5][61][0] =  1; Phi_h_Bin_Values[5][61][1] = 796; Phi_h_Bin_Values[5][61][2] = 3458;
z_pT_Bin_Borders[5][62][0] = 10; z_pT_Bin_Borders[5][62][1] = 0.72; z_pT_Bin_Borders[5][62][2] = 0.51; z_pT_Bin_Borders[5][62][3] = 0.65;
Phi_h_Bin_Values[5][62][0] =  1; Phi_h_Bin_Values[5][62][1] = 797; Phi_h_Bin_Values[5][62][2] = 3459;
z_pT_Bin_Borders[5][63][0] = 10; z_pT_Bin_Borders[5][63][1] = 0.72; z_pT_Bin_Borders[5][63][2] = 0.65; z_pT_Bin_Borders[5][63][3] = 0.98;
Phi_h_Bin_Values[5][63][0] =  1; Phi_h_Bin_Values[5][63][1] = 798; Phi_h_Bin_Values[5][63][2] = 3460;
z_pT_Bin_Borders[5][64][0] = 10; z_pT_Bin_Borders[5][64][1] = 0.72; z_pT_Bin_Borders[5][64][2] = 10; z_pT_Bin_Borders[5][64][3] = 0.98;
Phi_h_Bin_Values[5][64][0] =  1; Phi_h_Bin_Values[5][64][1] = 799; Phi_h_Bin_Values[5][64][2] = 3461;
z_pT_Bin_Borders[6][1][0] = 0.23; z_pT_Bin_Borders[6][1][1] = 0.18; z_pT_Bin_Borders[6][1][2] = 0.22; z_pT_Bin_Borders[6][1][3] = 0.05;
Phi_h_Bin_Values[6][1][0] =  24; Phi_h_Bin_Values[6][1][1] = 0; Phi_h_Bin_Values[6][1][2] = 3462;
z_pT_Bin_Borders[6][2][0] = 0.23; z_pT_Bin_Borders[6][2][1] = 0.18; z_pT_Bin_Borders[6][2][2] = 0.32; z_pT_Bin_Borders[6][2][3] = 0.22;
Phi_h_Bin_Values[6][2][0] =  24; Phi_h_Bin_Values[6][2][1] = 24; Phi_h_Bin_Values[6][2][2] = 3486;
z_pT_Bin_Borders[6][3][0] = 0.23; z_pT_Bin_Borders[6][3][1] = 0.18; z_pT_Bin_Borders[6][3][2] = 0.41; z_pT_Bin_Borders[6][3][3] = 0.32;
Phi_h_Bin_Values[6][3][0] =  24; Phi_h_Bin_Values[6][3][1] = 48; Phi_h_Bin_Values[6][3][2] = 3510;
z_pT_Bin_Borders[6][4][0] = 0.23; z_pT_Bin_Borders[6][4][1] = 0.18; z_pT_Bin_Borders[6][4][2] = 0.51; z_pT_Bin_Borders[6][4][3] = 0.41;
Phi_h_Bin_Values[6][4][0] =  24; Phi_h_Bin_Values[6][4][1] = 72; Phi_h_Bin_Values[6][4][2] = 3534;
z_pT_Bin_Borders[6][5][0] = 0.23; z_pT_Bin_Borders[6][5][1] = 0.18; z_pT_Bin_Borders[6][5][2] = 0.65; z_pT_Bin_Borders[6][5][3] = 0.51;
Phi_h_Bin_Values[6][5][0] =  1; Phi_h_Bin_Values[6][5][1] = 96; Phi_h_Bin_Values[6][5][2] = 3558;
z_pT_Bin_Borders[6][6][0] = 0.23; z_pT_Bin_Borders[6][6][1] = 0.18; z_pT_Bin_Borders[6][6][2] = 1.05; z_pT_Bin_Borders[6][6][3] = 0.65;
Phi_h_Bin_Values[6][6][0] =  1; Phi_h_Bin_Values[6][6][1] = 97; Phi_h_Bin_Values[6][6][2] = 3559;
z_pT_Bin_Borders[6][7][0] = 0.28; z_pT_Bin_Borders[6][7][1] = 0.23; z_pT_Bin_Borders[6][7][2] = 0.22; z_pT_Bin_Borders[6][7][3] = 0.05;
Phi_h_Bin_Values[6][7][0] =  24; Phi_h_Bin_Values[6][7][1] = 98; Phi_h_Bin_Values[6][7][2] = 3560;
z_pT_Bin_Borders[6][8][0] = 0.28; z_pT_Bin_Borders[6][8][1] = 0.23; z_pT_Bin_Borders[6][8][2] = 0.32; z_pT_Bin_Borders[6][8][3] = 0.22;
Phi_h_Bin_Values[6][8][0] =  24; Phi_h_Bin_Values[6][8][1] = 122; Phi_h_Bin_Values[6][8][2] = 3584;
z_pT_Bin_Borders[6][9][0] = 0.28; z_pT_Bin_Borders[6][9][1] = 0.23; z_pT_Bin_Borders[6][9][2] = 0.41; z_pT_Bin_Borders[6][9][3] = 0.32;
Phi_h_Bin_Values[6][9][0] =  24; Phi_h_Bin_Values[6][9][1] = 146; Phi_h_Bin_Values[6][9][2] = 3608;
z_pT_Bin_Borders[6][10][0] = 0.28; z_pT_Bin_Borders[6][10][1] = 0.23; z_pT_Bin_Borders[6][10][2] = 0.51; z_pT_Bin_Borders[6][10][3] = 0.41;
Phi_h_Bin_Values[6][10][0] =  24; Phi_h_Bin_Values[6][10][1] = 170; Phi_h_Bin_Values[6][10][2] = 3632;
z_pT_Bin_Borders[6][11][0] = 0.28; z_pT_Bin_Borders[6][11][1] = 0.23; z_pT_Bin_Borders[6][11][2] = 0.65; z_pT_Bin_Borders[6][11][3] = 0.51;
Phi_h_Bin_Values[6][11][0] =  24; Phi_h_Bin_Values[6][11][1] = 194; Phi_h_Bin_Values[6][11][2] = 3656;
z_pT_Bin_Borders[6][12][0] = 0.28; z_pT_Bin_Borders[6][12][1] = 0.23; z_pT_Bin_Borders[6][12][2] = 1.05; z_pT_Bin_Borders[6][12][3] = 0.65;
Phi_h_Bin_Values[6][12][0] =  1; Phi_h_Bin_Values[6][12][1] = 218; Phi_h_Bin_Values[6][12][2] = 3680;
z_pT_Bin_Borders[6][13][0] = 0.35; z_pT_Bin_Borders[6][13][1] = 0.28; z_pT_Bin_Borders[6][13][2] = 0.22; z_pT_Bin_Borders[6][13][3] = 0.05;
Phi_h_Bin_Values[6][13][0] =  24; Phi_h_Bin_Values[6][13][1] = 219; Phi_h_Bin_Values[6][13][2] = 3681;
z_pT_Bin_Borders[6][14][0] = 0.35; z_pT_Bin_Borders[6][14][1] = 0.28; z_pT_Bin_Borders[6][14][2] = 0.32; z_pT_Bin_Borders[6][14][3] = 0.22;
Phi_h_Bin_Values[6][14][0] =  24; Phi_h_Bin_Values[6][14][1] = 243; Phi_h_Bin_Values[6][14][2] = 3705;
z_pT_Bin_Borders[6][15][0] = 0.35; z_pT_Bin_Borders[6][15][1] = 0.28; z_pT_Bin_Borders[6][15][2] = 0.41; z_pT_Bin_Borders[6][15][3] = 0.32;
Phi_h_Bin_Values[6][15][0] =  24; Phi_h_Bin_Values[6][15][1] = 267; Phi_h_Bin_Values[6][15][2] = 3729;
z_pT_Bin_Borders[6][16][0] = 0.35; z_pT_Bin_Borders[6][16][1] = 0.28; z_pT_Bin_Borders[6][16][2] = 0.51; z_pT_Bin_Borders[6][16][3] = 0.41;
Phi_h_Bin_Values[6][16][0] =  24; Phi_h_Bin_Values[6][16][1] = 291; Phi_h_Bin_Values[6][16][2] = 3753;
z_pT_Bin_Borders[6][17][0] = 0.35; z_pT_Bin_Borders[6][17][1] = 0.28; z_pT_Bin_Borders[6][17][2] = 0.65; z_pT_Bin_Borders[6][17][3] = 0.51;
Phi_h_Bin_Values[6][17][0] =  24; Phi_h_Bin_Values[6][17][1] = 315; Phi_h_Bin_Values[6][17][2] = 3777;
z_pT_Bin_Borders[6][18][0] = 0.35; z_pT_Bin_Borders[6][18][1] = 0.28; z_pT_Bin_Borders[6][18][2] = 1.05; z_pT_Bin_Borders[6][18][3] = 0.65;
Phi_h_Bin_Values[6][18][0] =  1; Phi_h_Bin_Values[6][18][1] = 339; Phi_h_Bin_Values[6][18][2] = 3801;
z_pT_Bin_Borders[6][19][0] = 0.45; z_pT_Bin_Borders[6][19][1] = 0.35; z_pT_Bin_Borders[6][19][2] = 0.22; z_pT_Bin_Borders[6][19][3] = 0.05;
Phi_h_Bin_Values[6][19][0] =  24; Phi_h_Bin_Values[6][19][1] = 340; Phi_h_Bin_Values[6][19][2] = 3802;
z_pT_Bin_Borders[6][20][0] = 0.45; z_pT_Bin_Borders[6][20][1] = 0.35; z_pT_Bin_Borders[6][20][2] = 0.32; z_pT_Bin_Borders[6][20][3] = 0.22;
Phi_h_Bin_Values[6][20][0] =  24; Phi_h_Bin_Values[6][20][1] = 364; Phi_h_Bin_Values[6][20][2] = 3826;
z_pT_Bin_Borders[6][21][0] = 0.45; z_pT_Bin_Borders[6][21][1] = 0.35; z_pT_Bin_Borders[6][21][2] = 0.41; z_pT_Bin_Borders[6][21][3] = 0.32;
Phi_h_Bin_Values[6][21][0] =  24; Phi_h_Bin_Values[6][21][1] = 388; Phi_h_Bin_Values[6][21][2] = 3850;
z_pT_Bin_Borders[6][22][0] = 0.45; z_pT_Bin_Borders[6][22][1] = 0.35; z_pT_Bin_Borders[6][22][2] = 0.51; z_pT_Bin_Borders[6][22][3] = 0.41;
Phi_h_Bin_Values[6][22][0] =  24; Phi_h_Bin_Values[6][22][1] = 412; Phi_h_Bin_Values[6][22][2] = 3874;
z_pT_Bin_Borders[6][23][0] = 0.45; z_pT_Bin_Borders[6][23][1] = 0.35; z_pT_Bin_Borders[6][23][2] = 0.65; z_pT_Bin_Borders[6][23][3] = 0.51;
Phi_h_Bin_Values[6][23][0] =  24; Phi_h_Bin_Values[6][23][1] = 436; Phi_h_Bin_Values[6][23][2] = 3898;
z_pT_Bin_Borders[6][24][0] = 0.45; z_pT_Bin_Borders[6][24][1] = 0.35; z_pT_Bin_Borders[6][24][2] = 1.05; z_pT_Bin_Borders[6][24][3] = 0.65;
Phi_h_Bin_Values[6][24][0] =  24; Phi_h_Bin_Values[6][24][1] = 460; Phi_h_Bin_Values[6][24][2] = 3922;
z_pT_Bin_Borders[6][25][0] = 0.75; z_pT_Bin_Borders[6][25][1] = 0.45; z_pT_Bin_Borders[6][25][2] = 0.22; z_pT_Bin_Borders[6][25][3] = 0.05;
Phi_h_Bin_Values[6][25][0] =  24; Phi_h_Bin_Values[6][25][1] = 484; Phi_h_Bin_Values[6][25][2] = 3946;
z_pT_Bin_Borders[6][26][0] = 0.75; z_pT_Bin_Borders[6][26][1] = 0.45; z_pT_Bin_Borders[6][26][2] = 0.32; z_pT_Bin_Borders[6][26][3] = 0.22;
Phi_h_Bin_Values[6][26][0] =  24; Phi_h_Bin_Values[6][26][1] = 508; Phi_h_Bin_Values[6][26][2] = 3970;
z_pT_Bin_Borders[6][27][0] = 0.75; z_pT_Bin_Borders[6][27][1] = 0.45; z_pT_Bin_Borders[6][27][2] = 0.41; z_pT_Bin_Borders[6][27][3] = 0.32;
Phi_h_Bin_Values[6][27][0] =  24; Phi_h_Bin_Values[6][27][1] = 532; Phi_h_Bin_Values[6][27][2] = 3994;
z_pT_Bin_Borders[6][28][0] = 0.75; z_pT_Bin_Borders[6][28][1] = 0.45; z_pT_Bin_Borders[6][28][2] = 0.51; z_pT_Bin_Borders[6][28][3] = 0.41;
Phi_h_Bin_Values[6][28][0] =  24; Phi_h_Bin_Values[6][28][1] = 556; Phi_h_Bin_Values[6][28][2] = 4018;
z_pT_Bin_Borders[6][29][0] = 0.75; z_pT_Bin_Borders[6][29][1] = 0.45; z_pT_Bin_Borders[6][29][2] = 0.65; z_pT_Bin_Borders[6][29][3] = 0.51;
Phi_h_Bin_Values[6][29][0] =  24; Phi_h_Bin_Values[6][29][1] = 580; Phi_h_Bin_Values[6][29][2] = 4042;
z_pT_Bin_Borders[6][30][0] = 0.75; z_pT_Bin_Borders[6][30][1] = 0.45; z_pT_Bin_Borders[6][30][2] = 1.05; z_pT_Bin_Borders[6][30][3] = 0.65;
Phi_h_Bin_Values[6][30][0] =  1; Phi_h_Bin_Values[6][30][1] = 604; Phi_h_Bin_Values[6][30][2] = 4066;
z_pT_Bin_Borders[6][31][0] = 0.18; z_pT_Bin_Borders[6][31][1] = 0; z_pT_Bin_Borders[6][31][2] = 0.05; z_pT_Bin_Borders[6][31][3] = 0;
Phi_h_Bin_Values[6][31][0] =  1; Phi_h_Bin_Values[6][31][1] = 605; Phi_h_Bin_Values[6][31][2] = 4067;
z_pT_Bin_Borders[6][32][0] = 0.18; z_pT_Bin_Borders[6][32][1] = 0; z_pT_Bin_Borders[6][32][2] = 0.05; z_pT_Bin_Borders[6][32][3] = 0.22;
Phi_h_Bin_Values[6][32][0] =  1; Phi_h_Bin_Values[6][32][1] = 606; Phi_h_Bin_Values[6][32][2] = 4068;
z_pT_Bin_Borders[6][33][0] = 0.18; z_pT_Bin_Borders[6][33][1] = 0; z_pT_Bin_Borders[6][33][2] = 0.22; z_pT_Bin_Borders[6][33][3] = 0.32;
Phi_h_Bin_Values[6][33][0] =  1; Phi_h_Bin_Values[6][33][1] = 607; Phi_h_Bin_Values[6][33][2] = 4069;
z_pT_Bin_Borders[6][34][0] = 0.18; z_pT_Bin_Borders[6][34][1] = 0; z_pT_Bin_Borders[6][34][2] = 0.32; z_pT_Bin_Borders[6][34][3] = 0.41;
Phi_h_Bin_Values[6][34][0] =  1; Phi_h_Bin_Values[6][34][1] = 608; Phi_h_Bin_Values[6][34][2] = 4070;
z_pT_Bin_Borders[6][35][0] = 0.18; z_pT_Bin_Borders[6][35][1] = 0; z_pT_Bin_Borders[6][35][2] = 0.41; z_pT_Bin_Borders[6][35][3] = 0.51;
Phi_h_Bin_Values[6][35][0] =  1; Phi_h_Bin_Values[6][35][1] = 609; Phi_h_Bin_Values[6][35][2] = 4071;
z_pT_Bin_Borders[6][36][0] = 0.18; z_pT_Bin_Borders[6][36][1] = 0; z_pT_Bin_Borders[6][36][2] = 0.51; z_pT_Bin_Borders[6][36][3] = 0.65;
Phi_h_Bin_Values[6][36][0] =  1; Phi_h_Bin_Values[6][36][1] = 610; Phi_h_Bin_Values[6][36][2] = 4072;
z_pT_Bin_Borders[6][37][0] = 0.18; z_pT_Bin_Borders[6][37][1] = 0; z_pT_Bin_Borders[6][37][2] = 0.65; z_pT_Bin_Borders[6][37][3] = 1.05;
Phi_h_Bin_Values[6][37][0] =  1; Phi_h_Bin_Values[6][37][1] = 611; Phi_h_Bin_Values[6][37][2] = 4073;
z_pT_Bin_Borders[6][38][0] = 0.18; z_pT_Bin_Borders[6][38][1] = 0; z_pT_Bin_Borders[6][38][2] = 10; z_pT_Bin_Borders[6][38][3] = 1.05;
Phi_h_Bin_Values[6][38][0] =  1; Phi_h_Bin_Values[6][38][1] = 612; Phi_h_Bin_Values[6][38][2] = 4074;
z_pT_Bin_Borders[6][39][0] = 0.18; z_pT_Bin_Borders[6][39][1] = 0.23; z_pT_Bin_Borders[6][39][2] = 0.05; z_pT_Bin_Borders[6][39][3] = 0;
Phi_h_Bin_Values[6][39][0] =  1; Phi_h_Bin_Values[6][39][1] = 613; Phi_h_Bin_Values[6][39][2] = 4075;
z_pT_Bin_Borders[6][40][0] = 0.18; z_pT_Bin_Borders[6][40][1] = 0.23; z_pT_Bin_Borders[6][40][2] = 10; z_pT_Bin_Borders[6][40][3] = 1.05;
Phi_h_Bin_Values[6][40][0] =  1; Phi_h_Bin_Values[6][40][1] = 614; Phi_h_Bin_Values[6][40][2] = 4076;
z_pT_Bin_Borders[6][41][0] = 0.23; z_pT_Bin_Borders[6][41][1] = 0.28; z_pT_Bin_Borders[6][41][2] = 0.05; z_pT_Bin_Borders[6][41][3] = 0;
Phi_h_Bin_Values[6][41][0] =  1; Phi_h_Bin_Values[6][41][1] = 615; Phi_h_Bin_Values[6][41][2] = 4077;
z_pT_Bin_Borders[6][42][0] = 0.23; z_pT_Bin_Borders[6][42][1] = 0.28; z_pT_Bin_Borders[6][42][2] = 10; z_pT_Bin_Borders[6][42][3] = 1.05;
Phi_h_Bin_Values[6][42][0] =  1; Phi_h_Bin_Values[6][42][1] = 616; Phi_h_Bin_Values[6][42][2] = 4078;
z_pT_Bin_Borders[6][43][0] = 0.28; z_pT_Bin_Borders[6][43][1] = 0.35; z_pT_Bin_Borders[6][43][2] = 0.05; z_pT_Bin_Borders[6][43][3] = 0;
Phi_h_Bin_Values[6][43][0] =  1; Phi_h_Bin_Values[6][43][1] = 617; Phi_h_Bin_Values[6][43][2] = 4079;
z_pT_Bin_Borders[6][44][0] = 0.28; z_pT_Bin_Borders[6][44][1] = 0.35; z_pT_Bin_Borders[6][44][2] = 10; z_pT_Bin_Borders[6][44][3] = 1.05;
Phi_h_Bin_Values[6][44][0] =  1; Phi_h_Bin_Values[6][44][1] = 618; Phi_h_Bin_Values[6][44][2] = 4080;
z_pT_Bin_Borders[6][45][0] = 0.35; z_pT_Bin_Borders[6][45][1] = 0.45; z_pT_Bin_Borders[6][45][2] = 0.05; z_pT_Bin_Borders[6][45][3] = 0;
Phi_h_Bin_Values[6][45][0] =  1; Phi_h_Bin_Values[6][45][1] = 619; Phi_h_Bin_Values[6][45][2] = 4081;
z_pT_Bin_Borders[6][46][0] = 0.35; z_pT_Bin_Borders[6][46][1] = 0.45; z_pT_Bin_Borders[6][46][2] = 10; z_pT_Bin_Borders[6][46][3] = 1.05;
Phi_h_Bin_Values[6][46][0] =  1; Phi_h_Bin_Values[6][46][1] = 620; Phi_h_Bin_Values[6][46][2] = 4082;
z_pT_Bin_Borders[6][47][0] = 0.45; z_pT_Bin_Borders[6][47][1] = 0.75; z_pT_Bin_Borders[6][47][2] = 0.05; z_pT_Bin_Borders[6][47][3] = 0;
Phi_h_Bin_Values[6][47][0] =  1; Phi_h_Bin_Values[6][47][1] = 621; Phi_h_Bin_Values[6][47][2] = 4083;
z_pT_Bin_Borders[6][48][0] = 0.45; z_pT_Bin_Borders[6][48][1] = 0.75; z_pT_Bin_Borders[6][48][2] = 10; z_pT_Bin_Borders[6][48][3] = 1.05;
Phi_h_Bin_Values[6][48][0] =  1; Phi_h_Bin_Values[6][48][1] = 622; Phi_h_Bin_Values[6][48][2] = 4084;
z_pT_Bin_Borders[6][49][0] = 10; z_pT_Bin_Borders[6][49][1] = 0.75; z_pT_Bin_Borders[6][49][2] = 0; z_pT_Bin_Borders[6][49][3] = 0.05;
Phi_h_Bin_Values[6][49][0] =  1; Phi_h_Bin_Values[6][49][1] = 623; Phi_h_Bin_Values[6][49][2] = 4085;
z_pT_Bin_Borders[6][50][0] = 10; z_pT_Bin_Borders[6][50][1] = 0.75; z_pT_Bin_Borders[6][50][2] = 0.05; z_pT_Bin_Borders[6][50][3] = 0.22;
Phi_h_Bin_Values[6][50][0] =  1; Phi_h_Bin_Values[6][50][1] = 624; Phi_h_Bin_Values[6][50][2] = 4086;
z_pT_Bin_Borders[6][51][0] = 10; z_pT_Bin_Borders[6][51][1] = 0.75; z_pT_Bin_Borders[6][51][2] = 0.22; z_pT_Bin_Borders[6][51][3] = 0.32;
Phi_h_Bin_Values[6][51][0] =  1; Phi_h_Bin_Values[6][51][1] = 625; Phi_h_Bin_Values[6][51][2] = 4087;
z_pT_Bin_Borders[6][52][0] = 10; z_pT_Bin_Borders[6][52][1] = 0.75; z_pT_Bin_Borders[6][52][2] = 0.32; z_pT_Bin_Borders[6][52][3] = 0.41;
Phi_h_Bin_Values[6][52][0] =  1; Phi_h_Bin_Values[6][52][1] = 626; Phi_h_Bin_Values[6][52][2] = 4088;
z_pT_Bin_Borders[6][53][0] = 10; z_pT_Bin_Borders[6][53][1] = 0.75; z_pT_Bin_Borders[6][53][2] = 0.41; z_pT_Bin_Borders[6][53][3] = 0.51;
Phi_h_Bin_Values[6][53][0] =  1; Phi_h_Bin_Values[6][53][1] = 627; Phi_h_Bin_Values[6][53][2] = 4089;
z_pT_Bin_Borders[6][54][0] = 10; z_pT_Bin_Borders[6][54][1] = 0.75; z_pT_Bin_Borders[6][54][2] = 0.51; z_pT_Bin_Borders[6][54][3] = 0.65;
Phi_h_Bin_Values[6][54][0] =  1; Phi_h_Bin_Values[6][54][1] = 628; Phi_h_Bin_Values[6][54][2] = 4090;
z_pT_Bin_Borders[6][55][0] = 10; z_pT_Bin_Borders[6][55][1] = 0.75; z_pT_Bin_Borders[6][55][2] = 0.65; z_pT_Bin_Borders[6][55][3] = 1.05;
Phi_h_Bin_Values[6][55][0] =  1; Phi_h_Bin_Values[6][55][1] = 629; Phi_h_Bin_Values[6][55][2] = 4091;
z_pT_Bin_Borders[6][56][0] = 10; z_pT_Bin_Borders[6][56][1] = 0.75; z_pT_Bin_Borders[6][56][2] = 10; z_pT_Bin_Borders[6][56][3] = 1.05;
Phi_h_Bin_Values[6][56][0] =  1; Phi_h_Bin_Values[6][56][1] = 630; Phi_h_Bin_Values[6][56][2] = 4092;
z_pT_Bin_Borders[7][1][0] = 0.28; z_pT_Bin_Borders[7][1][1] = 0.22; z_pT_Bin_Borders[7][1][2] = 0.2; z_pT_Bin_Borders[7][1][3] = 0.05;
Phi_h_Bin_Values[7][1][0] =  24; Phi_h_Bin_Values[7][1][1] = 0; Phi_h_Bin_Values[7][1][2] = 4093;
z_pT_Bin_Borders[7][2][0] = 0.28; z_pT_Bin_Borders[7][2][1] = 0.22; z_pT_Bin_Borders[7][2][2] = 0.29; z_pT_Bin_Borders[7][2][3] = 0.2;
Phi_h_Bin_Values[7][2][0] =  24; Phi_h_Bin_Values[7][2][1] = 24; Phi_h_Bin_Values[7][2][2] = 4117;
z_pT_Bin_Borders[7][3][0] = 0.28; z_pT_Bin_Borders[7][3][1] = 0.22; z_pT_Bin_Borders[7][3][2] = 0.38; z_pT_Bin_Borders[7][3][3] = 0.29;
Phi_h_Bin_Values[7][3][0] =  24; Phi_h_Bin_Values[7][3][1] = 48; Phi_h_Bin_Values[7][3][2] = 4141;
z_pT_Bin_Borders[7][4][0] = 0.28; z_pT_Bin_Borders[7][4][1] = 0.22; z_pT_Bin_Borders[7][4][2] = 0.48; z_pT_Bin_Borders[7][4][3] = 0.38;
Phi_h_Bin_Values[7][4][0] =  24; Phi_h_Bin_Values[7][4][1] = 72; Phi_h_Bin_Values[7][4][2] = 4165;
z_pT_Bin_Borders[7][5][0] = 0.28; z_pT_Bin_Borders[7][5][1] = 0.22; z_pT_Bin_Borders[7][5][2] = 0.6; z_pT_Bin_Borders[7][5][3] = 0.48;
Phi_h_Bin_Values[7][5][0] =  24; Phi_h_Bin_Values[7][5][1] = 96; Phi_h_Bin_Values[7][5][2] = 4189;
z_pT_Bin_Borders[7][6][0] = 0.28; z_pT_Bin_Borders[7][6][1] = 0.22; z_pT_Bin_Borders[7][6][2] = 0.83; z_pT_Bin_Borders[7][6][3] = 0.6;
Phi_h_Bin_Values[7][6][0] =  1; Phi_h_Bin_Values[7][6][1] = 120; Phi_h_Bin_Values[7][6][2] = 4213;
z_pT_Bin_Borders[7][7][0] = 0.33; z_pT_Bin_Borders[7][7][1] = 0.28; z_pT_Bin_Borders[7][7][2] = 0.2; z_pT_Bin_Borders[7][7][3] = 0.05;
Phi_h_Bin_Values[7][7][0] =  24; Phi_h_Bin_Values[7][7][1] = 121; Phi_h_Bin_Values[7][7][2] = 4214;
z_pT_Bin_Borders[7][8][0] = 0.33; z_pT_Bin_Borders[7][8][1] = 0.28; z_pT_Bin_Borders[7][8][2] = 0.29; z_pT_Bin_Borders[7][8][3] = 0.2;
Phi_h_Bin_Values[7][8][0] =  24; Phi_h_Bin_Values[7][8][1] = 145; Phi_h_Bin_Values[7][8][2] = 4238;
z_pT_Bin_Borders[7][9][0] = 0.33; z_pT_Bin_Borders[7][9][1] = 0.28; z_pT_Bin_Borders[7][9][2] = 0.38; z_pT_Bin_Borders[7][9][3] = 0.29;
Phi_h_Bin_Values[7][9][0] =  24; Phi_h_Bin_Values[7][9][1] = 169; Phi_h_Bin_Values[7][9][2] = 4262;
z_pT_Bin_Borders[7][10][0] = 0.33; z_pT_Bin_Borders[7][10][1] = 0.28; z_pT_Bin_Borders[7][10][2] = 0.48; z_pT_Bin_Borders[7][10][3] = 0.38;
Phi_h_Bin_Values[7][10][0] =  24; Phi_h_Bin_Values[7][10][1] = 193; Phi_h_Bin_Values[7][10][2] = 4286;
z_pT_Bin_Borders[7][11][0] = 0.33; z_pT_Bin_Borders[7][11][1] = 0.28; z_pT_Bin_Borders[7][11][2] = 0.6; z_pT_Bin_Borders[7][11][3] = 0.48;
Phi_h_Bin_Values[7][11][0] =  24; Phi_h_Bin_Values[7][11][1] = 217; Phi_h_Bin_Values[7][11][2] = 4310;
z_pT_Bin_Borders[7][12][0] = 0.33; z_pT_Bin_Borders[7][12][1] = 0.28; z_pT_Bin_Borders[7][12][2] = 0.83; z_pT_Bin_Borders[7][12][3] = 0.6;
Phi_h_Bin_Values[7][12][0] =  1; Phi_h_Bin_Values[7][12][1] = 241; Phi_h_Bin_Values[7][12][2] = 4334;
z_pT_Bin_Borders[7][13][0] = 0.4; z_pT_Bin_Borders[7][13][1] = 0.33; z_pT_Bin_Borders[7][13][2] = 0.2; z_pT_Bin_Borders[7][13][3] = 0.05;
Phi_h_Bin_Values[7][13][0] =  24; Phi_h_Bin_Values[7][13][1] = 242; Phi_h_Bin_Values[7][13][2] = 4335;
z_pT_Bin_Borders[7][14][0] = 0.4; z_pT_Bin_Borders[7][14][1] = 0.33; z_pT_Bin_Borders[7][14][2] = 0.29; z_pT_Bin_Borders[7][14][3] = 0.2;
Phi_h_Bin_Values[7][14][0] =  24; Phi_h_Bin_Values[7][14][1] = 266; Phi_h_Bin_Values[7][14][2] = 4359;
z_pT_Bin_Borders[7][15][0] = 0.4; z_pT_Bin_Borders[7][15][1] = 0.33; z_pT_Bin_Borders[7][15][2] = 0.38; z_pT_Bin_Borders[7][15][3] = 0.29;
Phi_h_Bin_Values[7][15][0] =  24; Phi_h_Bin_Values[7][15][1] = 290; Phi_h_Bin_Values[7][15][2] = 4383;
z_pT_Bin_Borders[7][16][0] = 0.4; z_pT_Bin_Borders[7][16][1] = 0.33; z_pT_Bin_Borders[7][16][2] = 0.48; z_pT_Bin_Borders[7][16][3] = 0.38;
Phi_h_Bin_Values[7][16][0] =  24; Phi_h_Bin_Values[7][16][1] = 314; Phi_h_Bin_Values[7][16][2] = 4407;
z_pT_Bin_Borders[7][17][0] = 0.4; z_pT_Bin_Borders[7][17][1] = 0.33; z_pT_Bin_Borders[7][17][2] = 0.6; z_pT_Bin_Borders[7][17][3] = 0.48;
Phi_h_Bin_Values[7][17][0] =  24; Phi_h_Bin_Values[7][17][1] = 338; Phi_h_Bin_Values[7][17][2] = 4431;
z_pT_Bin_Borders[7][18][0] = 0.4; z_pT_Bin_Borders[7][18][1] = 0.33; z_pT_Bin_Borders[7][18][2] = 0.83; z_pT_Bin_Borders[7][18][3] = 0.6;
Phi_h_Bin_Values[7][18][0] =  24; Phi_h_Bin_Values[7][18][1] = 362; Phi_h_Bin_Values[7][18][2] = 4455;
z_pT_Bin_Borders[7][19][0] = 0.51; z_pT_Bin_Borders[7][19][1] = 0.4; z_pT_Bin_Borders[7][19][2] = 0.2; z_pT_Bin_Borders[7][19][3] = 0.05;
Phi_h_Bin_Values[7][19][0] =  24; Phi_h_Bin_Values[7][19][1] = 386; Phi_h_Bin_Values[7][19][2] = 4479;
z_pT_Bin_Borders[7][20][0] = 0.51; z_pT_Bin_Borders[7][20][1] = 0.4; z_pT_Bin_Borders[7][20][2] = 0.29; z_pT_Bin_Borders[7][20][3] = 0.2;
Phi_h_Bin_Values[7][20][0] =  24; Phi_h_Bin_Values[7][20][1] = 410; Phi_h_Bin_Values[7][20][2] = 4503;
z_pT_Bin_Borders[7][21][0] = 0.51; z_pT_Bin_Borders[7][21][1] = 0.4; z_pT_Bin_Borders[7][21][2] = 0.38; z_pT_Bin_Borders[7][21][3] = 0.29;
Phi_h_Bin_Values[7][21][0] =  24; Phi_h_Bin_Values[7][21][1] = 434; Phi_h_Bin_Values[7][21][2] = 4527;
z_pT_Bin_Borders[7][22][0] = 0.51; z_pT_Bin_Borders[7][22][1] = 0.4; z_pT_Bin_Borders[7][22][2] = 0.48; z_pT_Bin_Borders[7][22][3] = 0.38;
Phi_h_Bin_Values[7][22][0] =  24; Phi_h_Bin_Values[7][22][1] = 458; Phi_h_Bin_Values[7][22][2] = 4551;
z_pT_Bin_Borders[7][23][0] = 0.51; z_pT_Bin_Borders[7][23][1] = 0.4; z_pT_Bin_Borders[7][23][2] = 0.6; z_pT_Bin_Borders[7][23][3] = 0.48;
Phi_h_Bin_Values[7][23][0] =  24; Phi_h_Bin_Values[7][23][1] = 482; Phi_h_Bin_Values[7][23][2] = 4575;
z_pT_Bin_Borders[7][24][0] = 0.51; z_pT_Bin_Borders[7][24][1] = 0.4; z_pT_Bin_Borders[7][24][2] = 0.83; z_pT_Bin_Borders[7][24][3] = 0.6;
Phi_h_Bin_Values[7][24][0] =  24; Phi_h_Bin_Values[7][24][1] = 506; Phi_h_Bin_Values[7][24][2] = 4599;
z_pT_Bin_Borders[7][25][0] = 0.7; z_pT_Bin_Borders[7][25][1] = 0.51; z_pT_Bin_Borders[7][25][2] = 0.2; z_pT_Bin_Borders[7][25][3] = 0.05;
Phi_h_Bin_Values[7][25][0] =  24; Phi_h_Bin_Values[7][25][1] = 530; Phi_h_Bin_Values[7][25][2] = 4623;
z_pT_Bin_Borders[7][26][0] = 0.7; z_pT_Bin_Borders[7][26][1] = 0.51; z_pT_Bin_Borders[7][26][2] = 0.29; z_pT_Bin_Borders[7][26][3] = 0.2;
Phi_h_Bin_Values[7][26][0] =  24; Phi_h_Bin_Values[7][26][1] = 554; Phi_h_Bin_Values[7][26][2] = 4647;
z_pT_Bin_Borders[7][27][0] = 0.7; z_pT_Bin_Borders[7][27][1] = 0.51; z_pT_Bin_Borders[7][27][2] = 0.38; z_pT_Bin_Borders[7][27][3] = 0.29;
Phi_h_Bin_Values[7][27][0] =  24; Phi_h_Bin_Values[7][27][1] = 578; Phi_h_Bin_Values[7][27][2] = 4671;
z_pT_Bin_Borders[7][28][0] = 0.7; z_pT_Bin_Borders[7][28][1] = 0.51; z_pT_Bin_Borders[7][28][2] = 0.48; z_pT_Bin_Borders[7][28][3] = 0.38;
Phi_h_Bin_Values[7][28][0] =  24; Phi_h_Bin_Values[7][28][1] = 602; Phi_h_Bin_Values[7][28][2] = 4695;
z_pT_Bin_Borders[7][29][0] = 0.7; z_pT_Bin_Borders[7][29][1] = 0.51; z_pT_Bin_Borders[7][29][2] = 0.6; z_pT_Bin_Borders[7][29][3] = 0.48;
Phi_h_Bin_Values[7][29][0] =  1; Phi_h_Bin_Values[7][29][1] = 626; Phi_h_Bin_Values[7][29][2] = 4719;
z_pT_Bin_Borders[7][30][0] = 0.7; z_pT_Bin_Borders[7][30][1] = 0.51; z_pT_Bin_Borders[7][30][2] = 0.83; z_pT_Bin_Borders[7][30][3] = 0.6;
Phi_h_Bin_Values[7][30][0] =  1; Phi_h_Bin_Values[7][30][1] = 627; Phi_h_Bin_Values[7][30][2] = 4720;
z_pT_Bin_Borders[7][31][0] = 0.22; z_pT_Bin_Borders[7][31][1] = 0; z_pT_Bin_Borders[7][31][2] = 0.05; z_pT_Bin_Borders[7][31][3] = 0;
Phi_h_Bin_Values[7][31][0] =  1; Phi_h_Bin_Values[7][31][1] = 628; Phi_h_Bin_Values[7][31][2] = 4721;
z_pT_Bin_Borders[7][32][0] = 0.22; z_pT_Bin_Borders[7][32][1] = 0; z_pT_Bin_Borders[7][32][2] = 0.05; z_pT_Bin_Borders[7][32][3] = 0.2;
Phi_h_Bin_Values[7][32][0] =  1; Phi_h_Bin_Values[7][32][1] = 629; Phi_h_Bin_Values[7][32][2] = 4722;
z_pT_Bin_Borders[7][33][0] = 0.22; z_pT_Bin_Borders[7][33][1] = 0; z_pT_Bin_Borders[7][33][2] = 0.2; z_pT_Bin_Borders[7][33][3] = 0.29;
Phi_h_Bin_Values[7][33][0] =  1; Phi_h_Bin_Values[7][33][1] = 630; Phi_h_Bin_Values[7][33][2] = 4723;
z_pT_Bin_Borders[7][34][0] = 0.22; z_pT_Bin_Borders[7][34][1] = 0; z_pT_Bin_Borders[7][34][2] = 0.29; z_pT_Bin_Borders[7][34][3] = 0.38;
Phi_h_Bin_Values[7][34][0] =  1; Phi_h_Bin_Values[7][34][1] = 631; Phi_h_Bin_Values[7][34][2] = 4724;
z_pT_Bin_Borders[7][35][0] = 0.22; z_pT_Bin_Borders[7][35][1] = 0; z_pT_Bin_Borders[7][35][2] = 0.38; z_pT_Bin_Borders[7][35][3] = 0.48;
Phi_h_Bin_Values[7][35][0] =  1; Phi_h_Bin_Values[7][35][1] = 632; Phi_h_Bin_Values[7][35][2] = 4725;
z_pT_Bin_Borders[7][36][0] = 0.22; z_pT_Bin_Borders[7][36][1] = 0; z_pT_Bin_Borders[7][36][2] = 0.48; z_pT_Bin_Borders[7][36][3] = 0.6;
Phi_h_Bin_Values[7][36][0] =  1; Phi_h_Bin_Values[7][36][1] = 633; Phi_h_Bin_Values[7][36][2] = 4726;
z_pT_Bin_Borders[7][37][0] = 0.22; z_pT_Bin_Borders[7][37][1] = 0; z_pT_Bin_Borders[7][37][2] = 0.6; z_pT_Bin_Borders[7][37][3] = 0.83;
Phi_h_Bin_Values[7][37][0] =  1; Phi_h_Bin_Values[7][37][1] = 634; Phi_h_Bin_Values[7][37][2] = 4727;
z_pT_Bin_Borders[7][38][0] = 0.22; z_pT_Bin_Borders[7][38][1] = 0; z_pT_Bin_Borders[7][38][2] = 10; z_pT_Bin_Borders[7][38][3] = 0.83;
Phi_h_Bin_Values[7][38][0] =  1; Phi_h_Bin_Values[7][38][1] = 635; Phi_h_Bin_Values[7][38][2] = 4728;
z_pT_Bin_Borders[7][39][0] = 0.22; z_pT_Bin_Borders[7][39][1] = 0.28; z_pT_Bin_Borders[7][39][2] = 0.05; z_pT_Bin_Borders[7][39][3] = 0;
Phi_h_Bin_Values[7][39][0] =  1; Phi_h_Bin_Values[7][39][1] = 636; Phi_h_Bin_Values[7][39][2] = 4729;
z_pT_Bin_Borders[7][40][0] = 0.22; z_pT_Bin_Borders[7][40][1] = 0.28; z_pT_Bin_Borders[7][40][2] = 10; z_pT_Bin_Borders[7][40][3] = 0.83;
Phi_h_Bin_Values[7][40][0] =  1; Phi_h_Bin_Values[7][40][1] = 637; Phi_h_Bin_Values[7][40][2] = 4730;
z_pT_Bin_Borders[7][41][0] = 0.28; z_pT_Bin_Borders[7][41][1] = 0.33; z_pT_Bin_Borders[7][41][2] = 0.05; z_pT_Bin_Borders[7][41][3] = 0;
Phi_h_Bin_Values[7][41][0] =  1; Phi_h_Bin_Values[7][41][1] = 638; Phi_h_Bin_Values[7][41][2] = 4731;
z_pT_Bin_Borders[7][42][0] = 0.28; z_pT_Bin_Borders[7][42][1] = 0.33; z_pT_Bin_Borders[7][42][2] = 10; z_pT_Bin_Borders[7][42][3] = 0.83;
Phi_h_Bin_Values[7][42][0] =  1; Phi_h_Bin_Values[7][42][1] = 639; Phi_h_Bin_Values[7][42][2] = 4732;
z_pT_Bin_Borders[7][43][0] = 0.33; z_pT_Bin_Borders[7][43][1] = 0.4; z_pT_Bin_Borders[7][43][2] = 0.05; z_pT_Bin_Borders[7][43][3] = 0;
Phi_h_Bin_Values[7][43][0] =  1; Phi_h_Bin_Values[7][43][1] = 640; Phi_h_Bin_Values[7][43][2] = 4733;
z_pT_Bin_Borders[7][44][0] = 0.33; z_pT_Bin_Borders[7][44][1] = 0.4; z_pT_Bin_Borders[7][44][2] = 10; z_pT_Bin_Borders[7][44][3] = 0.83;
Phi_h_Bin_Values[7][44][0] =  1; Phi_h_Bin_Values[7][44][1] = 641; Phi_h_Bin_Values[7][44][2] = 4734;
z_pT_Bin_Borders[7][45][0] = 0.4; z_pT_Bin_Borders[7][45][1] = 0.51; z_pT_Bin_Borders[7][45][2] = 0.05; z_pT_Bin_Borders[7][45][3] = 0;
Phi_h_Bin_Values[7][45][0] =  1; Phi_h_Bin_Values[7][45][1] = 642; Phi_h_Bin_Values[7][45][2] = 4735;
z_pT_Bin_Borders[7][46][0] = 0.4; z_pT_Bin_Borders[7][46][1] = 0.51; z_pT_Bin_Borders[7][46][2] = 10; z_pT_Bin_Borders[7][46][3] = 0.83;
Phi_h_Bin_Values[7][46][0] =  1; Phi_h_Bin_Values[7][46][1] = 643; Phi_h_Bin_Values[7][46][2] = 4736;
z_pT_Bin_Borders[7][47][0] = 0.51; z_pT_Bin_Borders[7][47][1] = 0.7; z_pT_Bin_Borders[7][47][2] = 0.05; z_pT_Bin_Borders[7][47][3] = 0;
Phi_h_Bin_Values[7][47][0] =  1; Phi_h_Bin_Values[7][47][1] = 644; Phi_h_Bin_Values[7][47][2] = 4737;
z_pT_Bin_Borders[7][48][0] = 0.51; z_pT_Bin_Borders[7][48][1] = 0.7; z_pT_Bin_Borders[7][48][2] = 10; z_pT_Bin_Borders[7][48][3] = 0.83;
Phi_h_Bin_Values[7][48][0] =  1; Phi_h_Bin_Values[7][48][1] = 645; Phi_h_Bin_Values[7][48][2] = 4738;
z_pT_Bin_Borders[7][49][0] = 10; z_pT_Bin_Borders[7][49][1] = 0.7; z_pT_Bin_Borders[7][49][2] = 0; z_pT_Bin_Borders[7][49][3] = 0.05;
Phi_h_Bin_Values[7][49][0] =  1; Phi_h_Bin_Values[7][49][1] = 646; Phi_h_Bin_Values[7][49][2] = 4739;
z_pT_Bin_Borders[7][50][0] = 10; z_pT_Bin_Borders[7][50][1] = 0.7; z_pT_Bin_Borders[7][50][2] = 0.05; z_pT_Bin_Borders[7][50][3] = 0.2;
Phi_h_Bin_Values[7][50][0] =  1; Phi_h_Bin_Values[7][50][1] = 647; Phi_h_Bin_Values[7][50][2] = 4740;
z_pT_Bin_Borders[7][51][0] = 10; z_pT_Bin_Borders[7][51][1] = 0.7; z_pT_Bin_Borders[7][51][2] = 0.2; z_pT_Bin_Borders[7][51][3] = 0.29;
Phi_h_Bin_Values[7][51][0] =  1; Phi_h_Bin_Values[7][51][1] = 648; Phi_h_Bin_Values[7][51][2] = 4741;
z_pT_Bin_Borders[7][52][0] = 10; z_pT_Bin_Borders[7][52][1] = 0.7; z_pT_Bin_Borders[7][52][2] = 0.29; z_pT_Bin_Borders[7][52][3] = 0.38;
Phi_h_Bin_Values[7][52][0] =  1; Phi_h_Bin_Values[7][52][1] = 649; Phi_h_Bin_Values[7][52][2] = 4742;
z_pT_Bin_Borders[7][53][0] = 10; z_pT_Bin_Borders[7][53][1] = 0.7; z_pT_Bin_Borders[7][53][2] = 0.38; z_pT_Bin_Borders[7][53][3] = 0.48;
Phi_h_Bin_Values[7][53][0] =  1; Phi_h_Bin_Values[7][53][1] = 650; Phi_h_Bin_Values[7][53][2] = 4743;
z_pT_Bin_Borders[7][54][0] = 10; z_pT_Bin_Borders[7][54][1] = 0.7; z_pT_Bin_Borders[7][54][2] = 0.48; z_pT_Bin_Borders[7][54][3] = 0.6;
Phi_h_Bin_Values[7][54][0] =  1; Phi_h_Bin_Values[7][54][1] = 651; Phi_h_Bin_Values[7][54][2] = 4744;
z_pT_Bin_Borders[7][55][0] = 10; z_pT_Bin_Borders[7][55][1] = 0.7; z_pT_Bin_Borders[7][55][2] = 0.6; z_pT_Bin_Borders[7][55][3] = 0.83;
Phi_h_Bin_Values[7][55][0] =  1; Phi_h_Bin_Values[7][55][1] = 652; Phi_h_Bin_Values[7][55][2] = 4745;
z_pT_Bin_Borders[7][56][0] = 10; z_pT_Bin_Borders[7][56][1] = 0.7; z_pT_Bin_Borders[7][56][2] = 10; z_pT_Bin_Borders[7][56][3] = 0.83;
Phi_h_Bin_Values[7][56][0] =  1; Phi_h_Bin_Values[7][56][1] = 653; Phi_h_Bin_Values[7][56][2] = 4746;
z_pT_Bin_Borders[8][1][0] = 0.32; z_pT_Bin_Borders[8][1][1] = 0.27; z_pT_Bin_Borders[8][1][2] = 0.21; z_pT_Bin_Borders[8][1][3] = 0.05;
Phi_h_Bin_Values[8][1][0] =  24; Phi_h_Bin_Values[8][1][1] = 0; Phi_h_Bin_Values[8][1][2] = 4747;
z_pT_Bin_Borders[8][2][0] = 0.32; z_pT_Bin_Borders[8][2][1] = 0.27; z_pT_Bin_Borders[8][2][2] = 0.31; z_pT_Bin_Borders[8][2][3] = 0.21;
Phi_h_Bin_Values[8][2][0] =  24; Phi_h_Bin_Values[8][2][1] = 24; Phi_h_Bin_Values[8][2][2] = 4771;
z_pT_Bin_Borders[8][3][0] = 0.32; z_pT_Bin_Borders[8][3][1] = 0.27; z_pT_Bin_Borders[8][3][2] = 0.4; z_pT_Bin_Borders[8][3][3] = 0.31;
Phi_h_Bin_Values[8][3][0] =  24; Phi_h_Bin_Values[8][3][1] = 48; Phi_h_Bin_Values[8][3][2] = 4795;
z_pT_Bin_Borders[8][4][0] = 0.32; z_pT_Bin_Borders[8][4][1] = 0.27; z_pT_Bin_Borders[8][4][2] = 0.5; z_pT_Bin_Borders[8][4][3] = 0.4;
Phi_h_Bin_Values[8][4][0] =  24; Phi_h_Bin_Values[8][4][1] = 72; Phi_h_Bin_Values[8][4][2] = 4819;
z_pT_Bin_Borders[8][5][0] = 0.36; z_pT_Bin_Borders[8][5][1] = 0.32; z_pT_Bin_Borders[8][5][2] = 0.21; z_pT_Bin_Borders[8][5][3] = 0.05;
Phi_h_Bin_Values[8][5][0] =  24; Phi_h_Bin_Values[8][5][1] = 96; Phi_h_Bin_Values[8][5][2] = 4843;
z_pT_Bin_Borders[8][6][0] = 0.36; z_pT_Bin_Borders[8][6][1] = 0.32; z_pT_Bin_Borders[8][6][2] = 0.31; z_pT_Bin_Borders[8][6][3] = 0.21;
Phi_h_Bin_Values[8][6][0] =  24; Phi_h_Bin_Values[8][6][1] = 120; Phi_h_Bin_Values[8][6][2] = 4867;
z_pT_Bin_Borders[8][7][0] = 0.36; z_pT_Bin_Borders[8][7][1] = 0.32; z_pT_Bin_Borders[8][7][2] = 0.4; z_pT_Bin_Borders[8][7][3] = 0.31;
Phi_h_Bin_Values[8][7][0] =  24; Phi_h_Bin_Values[8][7][1] = 144; Phi_h_Bin_Values[8][7][2] = 4891;
z_pT_Bin_Borders[8][8][0] = 0.36; z_pT_Bin_Borders[8][8][1] = 0.32; z_pT_Bin_Borders[8][8][2] = 0.5; z_pT_Bin_Borders[8][8][3] = 0.4;
Phi_h_Bin_Values[8][8][0] =  24; Phi_h_Bin_Values[8][8][1] = 168; Phi_h_Bin_Values[8][8][2] = 4915;
z_pT_Bin_Borders[8][9][0] = 0.4; z_pT_Bin_Borders[8][9][1] = 0.36; z_pT_Bin_Borders[8][9][2] = 0.21; z_pT_Bin_Borders[8][9][3] = 0.05;
Phi_h_Bin_Values[8][9][0] =  24; Phi_h_Bin_Values[8][9][1] = 192; Phi_h_Bin_Values[8][9][2] = 4939;
z_pT_Bin_Borders[8][10][0] = 0.4; z_pT_Bin_Borders[8][10][1] = 0.36; z_pT_Bin_Borders[8][10][2] = 0.31; z_pT_Bin_Borders[8][10][3] = 0.21;
Phi_h_Bin_Values[8][10][0] =  24; Phi_h_Bin_Values[8][10][1] = 216; Phi_h_Bin_Values[8][10][2] = 4963;
z_pT_Bin_Borders[8][11][0] = 0.4; z_pT_Bin_Borders[8][11][1] = 0.36; z_pT_Bin_Borders[8][11][2] = 0.4; z_pT_Bin_Borders[8][11][3] = 0.31;
Phi_h_Bin_Values[8][11][0] =  24; Phi_h_Bin_Values[8][11][1] = 240; Phi_h_Bin_Values[8][11][2] = 4987;
z_pT_Bin_Borders[8][12][0] = 0.4; z_pT_Bin_Borders[8][12][1] = 0.36; z_pT_Bin_Borders[8][12][2] = 0.5; z_pT_Bin_Borders[8][12][3] = 0.4;
Phi_h_Bin_Values[8][12][0] =  24; Phi_h_Bin_Values[8][12][1] = 264; Phi_h_Bin_Values[8][12][2] = 5011;
z_pT_Bin_Borders[8][13][0] = 0.45; z_pT_Bin_Borders[8][13][1] = 0.4; z_pT_Bin_Borders[8][13][2] = 0.21; z_pT_Bin_Borders[8][13][3] = 0.05;
Phi_h_Bin_Values[8][13][0] =  24; Phi_h_Bin_Values[8][13][1] = 288; Phi_h_Bin_Values[8][13][2] = 5035;
z_pT_Bin_Borders[8][14][0] = 0.45; z_pT_Bin_Borders[8][14][1] = 0.4; z_pT_Bin_Borders[8][14][2] = 0.31; z_pT_Bin_Borders[8][14][3] = 0.21;
Phi_h_Bin_Values[8][14][0] =  24; Phi_h_Bin_Values[8][14][1] = 312; Phi_h_Bin_Values[8][14][2] = 5059;
z_pT_Bin_Borders[8][15][0] = 0.45; z_pT_Bin_Borders[8][15][1] = 0.4; z_pT_Bin_Borders[8][15][2] = 0.4; z_pT_Bin_Borders[8][15][3] = 0.31;
Phi_h_Bin_Values[8][15][0] =  24; Phi_h_Bin_Values[8][15][1] = 336; Phi_h_Bin_Values[8][15][2] = 5083;
z_pT_Bin_Borders[8][16][0] = 0.45; z_pT_Bin_Borders[8][16][1] = 0.4; z_pT_Bin_Borders[8][16][2] = 0.5; z_pT_Bin_Borders[8][16][3] = 0.4;
Phi_h_Bin_Values[8][16][0] =  24; Phi_h_Bin_Values[8][16][1] = 360; Phi_h_Bin_Values[8][16][2] = 5107;
z_pT_Bin_Borders[8][17][0] = 0.5; z_pT_Bin_Borders[8][17][1] = 0.45; z_pT_Bin_Borders[8][17][2] = 0.21; z_pT_Bin_Borders[8][17][3] = 0.05;
Phi_h_Bin_Values[8][17][0] =  24; Phi_h_Bin_Values[8][17][1] = 384; Phi_h_Bin_Values[8][17][2] = 5131;
z_pT_Bin_Borders[8][18][0] = 0.5; z_pT_Bin_Borders[8][18][1] = 0.45; z_pT_Bin_Borders[8][18][2] = 0.31; z_pT_Bin_Borders[8][18][3] = 0.21;
Phi_h_Bin_Values[8][18][0] =  24; Phi_h_Bin_Values[8][18][1] = 408; Phi_h_Bin_Values[8][18][2] = 5155;
z_pT_Bin_Borders[8][19][0] = 0.5; z_pT_Bin_Borders[8][19][1] = 0.45; z_pT_Bin_Borders[8][19][2] = 0.4; z_pT_Bin_Borders[8][19][3] = 0.31;
Phi_h_Bin_Values[8][19][0] =  24; Phi_h_Bin_Values[8][19][1] = 432; Phi_h_Bin_Values[8][19][2] = 5179;
z_pT_Bin_Borders[8][20][0] = 0.5; z_pT_Bin_Borders[8][20][1] = 0.45; z_pT_Bin_Borders[8][20][2] = 0.5; z_pT_Bin_Borders[8][20][3] = 0.4;
Phi_h_Bin_Values[8][20][0] =  24; Phi_h_Bin_Values[8][20][1] = 456; Phi_h_Bin_Values[8][20][2] = 5203;
z_pT_Bin_Borders[8][21][0] = 0.6; z_pT_Bin_Borders[8][21][1] = 0.5; z_pT_Bin_Borders[8][21][2] = 0.21; z_pT_Bin_Borders[8][21][3] = 0.05;
Phi_h_Bin_Values[8][21][0] =  24; Phi_h_Bin_Values[8][21][1] = 480; Phi_h_Bin_Values[8][21][2] = 5227;
z_pT_Bin_Borders[8][22][0] = 0.6; z_pT_Bin_Borders[8][22][1] = 0.5; z_pT_Bin_Borders[8][22][2] = 0.31; z_pT_Bin_Borders[8][22][3] = 0.21;
Phi_h_Bin_Values[8][22][0] =  24; Phi_h_Bin_Values[8][22][1] = 504; Phi_h_Bin_Values[8][22][2] = 5251;
z_pT_Bin_Borders[8][23][0] = 0.6; z_pT_Bin_Borders[8][23][1] = 0.5; z_pT_Bin_Borders[8][23][2] = 0.4; z_pT_Bin_Borders[8][23][3] = 0.31;
Phi_h_Bin_Values[8][23][0] =  1; Phi_h_Bin_Values[8][23][1] = 528; Phi_h_Bin_Values[8][23][2] = 5275;
z_pT_Bin_Borders[8][24][0] = 0.6; z_pT_Bin_Borders[8][24][1] = 0.5; z_pT_Bin_Borders[8][24][2] = 0.5; z_pT_Bin_Borders[8][24][3] = 0.4;
Phi_h_Bin_Values[8][24][0] =  1; Phi_h_Bin_Values[8][24][1] = 529; Phi_h_Bin_Values[8][24][2] = 5276;
z_pT_Bin_Borders[8][25][0] = 0.27; z_pT_Bin_Borders[8][25][1] = 0; z_pT_Bin_Borders[8][25][2] = 0.05; z_pT_Bin_Borders[8][25][3] = 0;
Phi_h_Bin_Values[8][25][0] =  1; Phi_h_Bin_Values[8][25][1] = 530; Phi_h_Bin_Values[8][25][2] = 5277;
z_pT_Bin_Borders[8][26][0] = 0.27; z_pT_Bin_Borders[8][26][1] = 0; z_pT_Bin_Borders[8][26][2] = 0.05; z_pT_Bin_Borders[8][26][3] = 0.21;
Phi_h_Bin_Values[8][26][0] =  1; Phi_h_Bin_Values[8][26][1] = 531; Phi_h_Bin_Values[8][26][2] = 5278;
z_pT_Bin_Borders[8][27][0] = 0.27; z_pT_Bin_Borders[8][27][1] = 0; z_pT_Bin_Borders[8][27][2] = 0.21; z_pT_Bin_Borders[8][27][3] = 0.31;
Phi_h_Bin_Values[8][27][0] =  1; Phi_h_Bin_Values[8][27][1] = 532; Phi_h_Bin_Values[8][27][2] = 5279;
z_pT_Bin_Borders[8][28][0] = 0.27; z_pT_Bin_Borders[8][28][1] = 0; z_pT_Bin_Borders[8][28][2] = 0.31; z_pT_Bin_Borders[8][28][3] = 0.4;
Phi_h_Bin_Values[8][28][0] =  1; Phi_h_Bin_Values[8][28][1] = 533; Phi_h_Bin_Values[8][28][2] = 5280;
z_pT_Bin_Borders[8][29][0] = 0.27; z_pT_Bin_Borders[8][29][1] = 0; z_pT_Bin_Borders[8][29][2] = 0.4; z_pT_Bin_Borders[8][29][3] = 0.5;
Phi_h_Bin_Values[8][29][0] =  1; Phi_h_Bin_Values[8][29][1] = 534; Phi_h_Bin_Values[8][29][2] = 5281;
z_pT_Bin_Borders[8][30][0] = 0.27; z_pT_Bin_Borders[8][30][1] = 0; z_pT_Bin_Borders[8][30][2] = 10; z_pT_Bin_Borders[8][30][3] = 0.5;
Phi_h_Bin_Values[8][30][0] =  1; Phi_h_Bin_Values[8][30][1] = 535; Phi_h_Bin_Values[8][30][2] = 5282;
z_pT_Bin_Borders[8][31][0] = 0.27; z_pT_Bin_Borders[8][31][1] = 0.32; z_pT_Bin_Borders[8][31][2] = 0.05; z_pT_Bin_Borders[8][31][3] = 0;
Phi_h_Bin_Values[8][31][0] =  1; Phi_h_Bin_Values[8][31][1] = 536; Phi_h_Bin_Values[8][31][2] = 5283;
z_pT_Bin_Borders[8][32][0] = 0.27; z_pT_Bin_Borders[8][32][1] = 0.32; z_pT_Bin_Borders[8][32][2] = 10; z_pT_Bin_Borders[8][32][3] = 0.5;
Phi_h_Bin_Values[8][32][0] =  1; Phi_h_Bin_Values[8][32][1] = 537; Phi_h_Bin_Values[8][32][2] = 5284;
z_pT_Bin_Borders[8][33][0] = 0.32; z_pT_Bin_Borders[8][33][1] = 0.36; z_pT_Bin_Borders[8][33][2] = 0.05; z_pT_Bin_Borders[8][33][3] = 0;
Phi_h_Bin_Values[8][33][0] =  1; Phi_h_Bin_Values[8][33][1] = 538; Phi_h_Bin_Values[8][33][2] = 5285;
z_pT_Bin_Borders[8][34][0] = 0.32; z_pT_Bin_Borders[8][34][1] = 0.36; z_pT_Bin_Borders[8][34][2] = 10; z_pT_Bin_Borders[8][34][3] = 0.5;
Phi_h_Bin_Values[8][34][0] =  1; Phi_h_Bin_Values[8][34][1] = 539; Phi_h_Bin_Values[8][34][2] = 5286;
z_pT_Bin_Borders[8][35][0] = 0.36; z_pT_Bin_Borders[8][35][1] = 0.4; z_pT_Bin_Borders[8][35][2] = 0.05; z_pT_Bin_Borders[8][35][3] = 0;
Phi_h_Bin_Values[8][35][0] =  1; Phi_h_Bin_Values[8][35][1] = 540; Phi_h_Bin_Values[8][35][2] = 5287;
z_pT_Bin_Borders[8][36][0] = 0.36; z_pT_Bin_Borders[8][36][1] = 0.4; z_pT_Bin_Borders[8][36][2] = 10; z_pT_Bin_Borders[8][36][3] = 0.5;
Phi_h_Bin_Values[8][36][0] =  1; Phi_h_Bin_Values[8][36][1] = 541; Phi_h_Bin_Values[8][36][2] = 5288;
z_pT_Bin_Borders[8][37][0] = 0.4; z_pT_Bin_Borders[8][37][1] = 0.45; z_pT_Bin_Borders[8][37][2] = 0.05; z_pT_Bin_Borders[8][37][3] = 0;
Phi_h_Bin_Values[8][37][0] =  1; Phi_h_Bin_Values[8][37][1] = 542; Phi_h_Bin_Values[8][37][2] = 5289;
z_pT_Bin_Borders[8][38][0] = 0.4; z_pT_Bin_Borders[8][38][1] = 0.45; z_pT_Bin_Borders[8][38][2] = 10; z_pT_Bin_Borders[8][38][3] = 0.5;
Phi_h_Bin_Values[8][38][0] =  1; Phi_h_Bin_Values[8][38][1] = 543; Phi_h_Bin_Values[8][38][2] = 5290;
z_pT_Bin_Borders[8][39][0] = 0.45; z_pT_Bin_Borders[8][39][1] = 0.5; z_pT_Bin_Borders[8][39][2] = 0.05; z_pT_Bin_Borders[8][39][3] = 0;
Phi_h_Bin_Values[8][39][0] =  1; Phi_h_Bin_Values[8][39][1] = 544; Phi_h_Bin_Values[8][39][2] = 5291;
z_pT_Bin_Borders[8][40][0] = 0.45; z_pT_Bin_Borders[8][40][1] = 0.5; z_pT_Bin_Borders[8][40][2] = 10; z_pT_Bin_Borders[8][40][3] = 0.5;
Phi_h_Bin_Values[8][40][0] =  1; Phi_h_Bin_Values[8][40][1] = 545; Phi_h_Bin_Values[8][40][2] = 5292;
z_pT_Bin_Borders[8][41][0] = 0.5; z_pT_Bin_Borders[8][41][1] = 0.6; z_pT_Bin_Borders[8][41][2] = 0.05; z_pT_Bin_Borders[8][41][3] = 0;
Phi_h_Bin_Values[8][41][0] =  1; Phi_h_Bin_Values[8][41][1] = 546; Phi_h_Bin_Values[8][41][2] = 5293;
z_pT_Bin_Borders[8][42][0] = 0.5; z_pT_Bin_Borders[8][42][1] = 0.6; z_pT_Bin_Borders[8][42][2] = 10; z_pT_Bin_Borders[8][42][3] = 0.5;
Phi_h_Bin_Values[8][42][0] =  1; Phi_h_Bin_Values[8][42][1] = 547; Phi_h_Bin_Values[8][42][2] = 5294;
z_pT_Bin_Borders[8][43][0] = 10; z_pT_Bin_Borders[8][43][1] = 0.6; z_pT_Bin_Borders[8][43][2] = 0; z_pT_Bin_Borders[8][43][3] = 0.05;
Phi_h_Bin_Values[8][43][0] =  1; Phi_h_Bin_Values[8][43][1] = 548; Phi_h_Bin_Values[8][43][2] = 5295;
z_pT_Bin_Borders[8][44][0] = 10; z_pT_Bin_Borders[8][44][1] = 0.6; z_pT_Bin_Borders[8][44][2] = 0.05; z_pT_Bin_Borders[8][44][3] = 0.21;
Phi_h_Bin_Values[8][44][0] =  1; Phi_h_Bin_Values[8][44][1] = 549; Phi_h_Bin_Values[8][44][2] = 5296;
z_pT_Bin_Borders[8][45][0] = 10; z_pT_Bin_Borders[8][45][1] = 0.6; z_pT_Bin_Borders[8][45][2] = 0.21; z_pT_Bin_Borders[8][45][3] = 0.31;
Phi_h_Bin_Values[8][45][0] =  1; Phi_h_Bin_Values[8][45][1] = 550; Phi_h_Bin_Values[8][45][2] = 5297;
z_pT_Bin_Borders[8][46][0] = 10; z_pT_Bin_Borders[8][46][1] = 0.6; z_pT_Bin_Borders[8][46][2] = 0.31; z_pT_Bin_Borders[8][46][3] = 0.4;
Phi_h_Bin_Values[8][46][0] =  1; Phi_h_Bin_Values[8][46][1] = 551; Phi_h_Bin_Values[8][46][2] = 5298;
z_pT_Bin_Borders[8][47][0] = 10; z_pT_Bin_Borders[8][47][1] = 0.6; z_pT_Bin_Borders[8][47][2] = 0.4; z_pT_Bin_Borders[8][47][3] = 0.5;
Phi_h_Bin_Values[8][47][0] =  1; Phi_h_Bin_Values[8][47][1] = 552; Phi_h_Bin_Values[8][47][2] = 5299;
z_pT_Bin_Borders[8][48][0] = 10; z_pT_Bin_Borders[8][48][1] = 0.6; z_pT_Bin_Borders[8][48][2] = 10; z_pT_Bin_Borders[8][48][3] = 0.5;
Phi_h_Bin_Values[8][48][0] =  1; Phi_h_Bin_Values[8][48][1] = 553; Phi_h_Bin_Values[8][48][2] = 5300;
z_pT_Bin_Borders[9][1][0] = 0.2; z_pT_Bin_Borders[9][1][1] = 0.16; z_pT_Bin_Borders[9][1][2] = 0.22; z_pT_Bin_Borders[9][1][3] = 0.05;
Phi_h_Bin_Values[9][1][0] =  24; Phi_h_Bin_Values[9][1][1] = 0; Phi_h_Bin_Values[9][1][2] = 5301;
z_pT_Bin_Borders[9][2][0] = 0.2; z_pT_Bin_Borders[9][2][1] = 0.16; z_pT_Bin_Borders[9][2][2] = 0.3; z_pT_Bin_Borders[9][2][3] = 0.22;
Phi_h_Bin_Values[9][2][0] =  24; Phi_h_Bin_Values[9][2][1] = 24; Phi_h_Bin_Values[9][2][2] = 5325;
z_pT_Bin_Borders[9][3][0] = 0.2; z_pT_Bin_Borders[9][3][1] = 0.16; z_pT_Bin_Borders[9][3][2] = 0.38; z_pT_Bin_Borders[9][3][3] = 0.3;
Phi_h_Bin_Values[9][3][0] =  24; Phi_h_Bin_Values[9][3][1] = 48; Phi_h_Bin_Values[9][3][2] = 5349;
z_pT_Bin_Borders[9][4][0] = 0.2; z_pT_Bin_Borders[9][4][1] = 0.16; z_pT_Bin_Borders[9][4][2] = 0.46; z_pT_Bin_Borders[9][4][3] = 0.38;
Phi_h_Bin_Values[9][4][0] =  24; Phi_h_Bin_Values[9][4][1] = 72; Phi_h_Bin_Values[9][4][2] = 5373;
z_pT_Bin_Borders[9][5][0] = 0.2; z_pT_Bin_Borders[9][5][1] = 0.16; z_pT_Bin_Borders[9][5][2] = 0.58; z_pT_Bin_Borders[9][5][3] = 0.46;
Phi_h_Bin_Values[9][5][0] =  24; Phi_h_Bin_Values[9][5][1] = 96; Phi_h_Bin_Values[9][5][2] = 5397;
z_pT_Bin_Borders[9][6][0] = 0.2; z_pT_Bin_Borders[9][6][1] = 0.16; z_pT_Bin_Borders[9][6][2] = 0.74; z_pT_Bin_Borders[9][6][3] = 0.58;
Phi_h_Bin_Values[9][6][0] =  1; Phi_h_Bin_Values[9][6][1] = 120; Phi_h_Bin_Values[9][6][2] = 5421;
z_pT_Bin_Borders[9][7][0] = 0.2; z_pT_Bin_Borders[9][7][1] = 0.16; z_pT_Bin_Borders[9][7][2] = 0.95; z_pT_Bin_Borders[9][7][3] = 0.74;
Phi_h_Bin_Values[9][7][0] =  1; Phi_h_Bin_Values[9][7][1] = 121; Phi_h_Bin_Values[9][7][2] = 5422;
z_pT_Bin_Borders[9][8][0] = 0.24; z_pT_Bin_Borders[9][8][1] = 0.2; z_pT_Bin_Borders[9][8][2] = 0.22; z_pT_Bin_Borders[9][8][3] = 0.05;
Phi_h_Bin_Values[9][8][0] =  24; Phi_h_Bin_Values[9][8][1] = 122; Phi_h_Bin_Values[9][8][2] = 5423;
z_pT_Bin_Borders[9][9][0] = 0.24; z_pT_Bin_Borders[9][9][1] = 0.2; z_pT_Bin_Borders[9][9][2] = 0.3; z_pT_Bin_Borders[9][9][3] = 0.22;
Phi_h_Bin_Values[9][9][0] =  24; Phi_h_Bin_Values[9][9][1] = 146; Phi_h_Bin_Values[9][9][2] = 5447;
z_pT_Bin_Borders[9][10][0] = 0.24; z_pT_Bin_Borders[9][10][1] = 0.2; z_pT_Bin_Borders[9][10][2] = 0.38; z_pT_Bin_Borders[9][10][3] = 0.3;
Phi_h_Bin_Values[9][10][0] =  24; Phi_h_Bin_Values[9][10][1] = 170; Phi_h_Bin_Values[9][10][2] = 5471;
z_pT_Bin_Borders[9][11][0] = 0.24; z_pT_Bin_Borders[9][11][1] = 0.2; z_pT_Bin_Borders[9][11][2] = 0.46; z_pT_Bin_Borders[9][11][3] = 0.38;
Phi_h_Bin_Values[9][11][0] =  24; Phi_h_Bin_Values[9][11][1] = 194; Phi_h_Bin_Values[9][11][2] = 5495;
z_pT_Bin_Borders[9][12][0] = 0.24; z_pT_Bin_Borders[9][12][1] = 0.2; z_pT_Bin_Borders[9][12][2] = 0.58; z_pT_Bin_Borders[9][12][3] = 0.46;
Phi_h_Bin_Values[9][12][0] =  24; Phi_h_Bin_Values[9][12][1] = 218; Phi_h_Bin_Values[9][12][2] = 5519;
z_pT_Bin_Borders[9][13][0] = 0.24; z_pT_Bin_Borders[9][13][1] = 0.2; z_pT_Bin_Borders[9][13][2] = 0.74; z_pT_Bin_Borders[9][13][3] = 0.58;
Phi_h_Bin_Values[9][13][0] =  1; Phi_h_Bin_Values[9][13][1] = 242; Phi_h_Bin_Values[9][13][2] = 5543;
z_pT_Bin_Borders[9][14][0] = 0.24; z_pT_Bin_Borders[9][14][1] = 0.2; z_pT_Bin_Borders[9][14][2] = 0.95; z_pT_Bin_Borders[9][14][3] = 0.74;
Phi_h_Bin_Values[9][14][0] =  1; Phi_h_Bin_Values[9][14][1] = 243; Phi_h_Bin_Values[9][14][2] = 5544;
z_pT_Bin_Borders[9][15][0] = 0.3; z_pT_Bin_Borders[9][15][1] = 0.24; z_pT_Bin_Borders[9][15][2] = 0.22; z_pT_Bin_Borders[9][15][3] = 0.05;
Phi_h_Bin_Values[9][15][0] =  24; Phi_h_Bin_Values[9][15][1] = 244; Phi_h_Bin_Values[9][15][2] = 5545;
z_pT_Bin_Borders[9][16][0] = 0.3; z_pT_Bin_Borders[9][16][1] = 0.24; z_pT_Bin_Borders[9][16][2] = 0.3; z_pT_Bin_Borders[9][16][3] = 0.22;
Phi_h_Bin_Values[9][16][0] =  24; Phi_h_Bin_Values[9][16][1] = 268; Phi_h_Bin_Values[9][16][2] = 5569;
z_pT_Bin_Borders[9][17][0] = 0.3; z_pT_Bin_Borders[9][17][1] = 0.24; z_pT_Bin_Borders[9][17][2] = 0.38; z_pT_Bin_Borders[9][17][3] = 0.3;
Phi_h_Bin_Values[9][17][0] =  24; Phi_h_Bin_Values[9][17][1] = 292; Phi_h_Bin_Values[9][17][2] = 5593;
z_pT_Bin_Borders[9][18][0] = 0.3; z_pT_Bin_Borders[9][18][1] = 0.24; z_pT_Bin_Borders[9][18][2] = 0.46; z_pT_Bin_Borders[9][18][3] = 0.38;
Phi_h_Bin_Values[9][18][0] =  24; Phi_h_Bin_Values[9][18][1] = 316; Phi_h_Bin_Values[9][18][2] = 5617;
z_pT_Bin_Borders[9][19][0] = 0.3; z_pT_Bin_Borders[9][19][1] = 0.24; z_pT_Bin_Borders[9][19][2] = 0.58; z_pT_Bin_Borders[9][19][3] = 0.46;
Phi_h_Bin_Values[9][19][0] =  24; Phi_h_Bin_Values[9][19][1] = 340; Phi_h_Bin_Values[9][19][2] = 5641;
z_pT_Bin_Borders[9][20][0] = 0.3; z_pT_Bin_Borders[9][20][1] = 0.24; z_pT_Bin_Borders[9][20][2] = 0.74; z_pT_Bin_Borders[9][20][3] = 0.58;
Phi_h_Bin_Values[9][20][0] =  24; Phi_h_Bin_Values[9][20][1] = 364; Phi_h_Bin_Values[9][20][2] = 5665;
z_pT_Bin_Borders[9][21][0] = 0.3; z_pT_Bin_Borders[9][21][1] = 0.24; z_pT_Bin_Borders[9][21][2] = 0.95; z_pT_Bin_Borders[9][21][3] = 0.74;
Phi_h_Bin_Values[9][21][0] =  1; Phi_h_Bin_Values[9][21][1] = 388; Phi_h_Bin_Values[9][21][2] = 5689;
z_pT_Bin_Borders[9][22][0] = 0.42; z_pT_Bin_Borders[9][22][1] = 0.3; z_pT_Bin_Borders[9][22][2] = 0.22; z_pT_Bin_Borders[9][22][3] = 0.05;
Phi_h_Bin_Values[9][22][0] =  24; Phi_h_Bin_Values[9][22][1] = 389; Phi_h_Bin_Values[9][22][2] = 5690;
z_pT_Bin_Borders[9][23][0] = 0.42; z_pT_Bin_Borders[9][23][1] = 0.3; z_pT_Bin_Borders[9][23][2] = 0.3; z_pT_Bin_Borders[9][23][3] = 0.22;
Phi_h_Bin_Values[9][23][0] =  24; Phi_h_Bin_Values[9][23][1] = 413; Phi_h_Bin_Values[9][23][2] = 5714;
z_pT_Bin_Borders[9][24][0] = 0.42; z_pT_Bin_Borders[9][24][1] = 0.3; z_pT_Bin_Borders[9][24][2] = 0.38; z_pT_Bin_Borders[9][24][3] = 0.3;
Phi_h_Bin_Values[9][24][0] =  24; Phi_h_Bin_Values[9][24][1] = 437; Phi_h_Bin_Values[9][24][2] = 5738;
z_pT_Bin_Borders[9][25][0] = 0.42; z_pT_Bin_Borders[9][25][1] = 0.3; z_pT_Bin_Borders[9][25][2] = 0.46; z_pT_Bin_Borders[9][25][3] = 0.38;
Phi_h_Bin_Values[9][25][0] =  24; Phi_h_Bin_Values[9][25][1] = 461; Phi_h_Bin_Values[9][25][2] = 5762;
z_pT_Bin_Borders[9][26][0] = 0.42; z_pT_Bin_Borders[9][26][1] = 0.3; z_pT_Bin_Borders[9][26][2] = 0.58; z_pT_Bin_Borders[9][26][3] = 0.46;
Phi_h_Bin_Values[9][26][0] =  24; Phi_h_Bin_Values[9][26][1] = 485; Phi_h_Bin_Values[9][26][2] = 5786;
z_pT_Bin_Borders[9][27][0] = 0.42; z_pT_Bin_Borders[9][27][1] = 0.3; z_pT_Bin_Borders[9][27][2] = 0.74; z_pT_Bin_Borders[9][27][3] = 0.58;
Phi_h_Bin_Values[9][27][0] =  24; Phi_h_Bin_Values[9][27][1] = 509; Phi_h_Bin_Values[9][27][2] = 5810;
z_pT_Bin_Borders[9][28][0] = 0.42; z_pT_Bin_Borders[9][28][1] = 0.3; z_pT_Bin_Borders[9][28][2] = 0.95; z_pT_Bin_Borders[9][28][3] = 0.74;
Phi_h_Bin_Values[9][28][0] =  24; Phi_h_Bin_Values[9][28][1] = 533; Phi_h_Bin_Values[9][28][2] = 5834;
z_pT_Bin_Borders[9][29][0] = 0.7; z_pT_Bin_Borders[9][29][1] = 0.42; z_pT_Bin_Borders[9][29][2] = 0.22; z_pT_Bin_Borders[9][29][3] = 0.05;
Phi_h_Bin_Values[9][29][0] =  24; Phi_h_Bin_Values[9][29][1] = 557; Phi_h_Bin_Values[9][29][2] = 5858;
z_pT_Bin_Borders[9][30][0] = 0.7; z_pT_Bin_Borders[9][30][1] = 0.42; z_pT_Bin_Borders[9][30][2] = 0.3; z_pT_Bin_Borders[9][30][3] = 0.22;
Phi_h_Bin_Values[9][30][0] =  24; Phi_h_Bin_Values[9][30][1] = 581; Phi_h_Bin_Values[9][30][2] = 5882;
z_pT_Bin_Borders[9][31][0] = 0.7; z_pT_Bin_Borders[9][31][1] = 0.42; z_pT_Bin_Borders[9][31][2] = 0.38; z_pT_Bin_Borders[9][31][3] = 0.3;
Phi_h_Bin_Values[9][31][0] =  24; Phi_h_Bin_Values[9][31][1] = 605; Phi_h_Bin_Values[9][31][2] = 5906;
z_pT_Bin_Borders[9][32][0] = 0.7; z_pT_Bin_Borders[9][32][1] = 0.42; z_pT_Bin_Borders[9][32][2] = 0.46; z_pT_Bin_Borders[9][32][3] = 0.38;
Phi_h_Bin_Values[9][32][0] =  24; Phi_h_Bin_Values[9][32][1] = 629; Phi_h_Bin_Values[9][32][2] = 5930;
z_pT_Bin_Borders[9][33][0] = 0.7; z_pT_Bin_Borders[9][33][1] = 0.42; z_pT_Bin_Borders[9][33][2] = 0.58; z_pT_Bin_Borders[9][33][3] = 0.46;
Phi_h_Bin_Values[9][33][0] =  24; Phi_h_Bin_Values[9][33][1] = 653; Phi_h_Bin_Values[9][33][2] = 5954;
z_pT_Bin_Borders[9][34][0] = 0.7; z_pT_Bin_Borders[9][34][1] = 0.42; z_pT_Bin_Borders[9][34][2] = 0.74; z_pT_Bin_Borders[9][34][3] = 0.58;
Phi_h_Bin_Values[9][34][0] =  24; Phi_h_Bin_Values[9][34][1] = 677; Phi_h_Bin_Values[9][34][2] = 5978;
z_pT_Bin_Borders[9][35][0] = 0.7; z_pT_Bin_Borders[9][35][1] = 0.42; z_pT_Bin_Borders[9][35][2] = 0.95; z_pT_Bin_Borders[9][35][3] = 0.74;
Phi_h_Bin_Values[9][35][0] =  24; Phi_h_Bin_Values[9][35][1] = 701; Phi_h_Bin_Values[9][35][2] = 6002;
z_pT_Bin_Borders[9][36][0] = 0.16; z_pT_Bin_Borders[9][36][1] = 0; z_pT_Bin_Borders[9][36][2] = 0.05; z_pT_Bin_Borders[9][36][3] = 0;
Phi_h_Bin_Values[9][36][0] =  1; Phi_h_Bin_Values[9][36][1] = 725; Phi_h_Bin_Values[9][36][2] = 6026;
z_pT_Bin_Borders[9][37][0] = 0.16; z_pT_Bin_Borders[9][37][1] = 0; z_pT_Bin_Borders[9][37][2] = 0.05; z_pT_Bin_Borders[9][37][3] = 0.22;
Phi_h_Bin_Values[9][37][0] =  1; Phi_h_Bin_Values[9][37][1] = 726; Phi_h_Bin_Values[9][37][2] = 6027;
z_pT_Bin_Borders[9][38][0] = 0.16; z_pT_Bin_Borders[9][38][1] = 0; z_pT_Bin_Borders[9][38][2] = 0.22; z_pT_Bin_Borders[9][38][3] = 0.3;
Phi_h_Bin_Values[9][38][0] =  1; Phi_h_Bin_Values[9][38][1] = 727; Phi_h_Bin_Values[9][38][2] = 6028;
z_pT_Bin_Borders[9][39][0] = 0.16; z_pT_Bin_Borders[9][39][1] = 0; z_pT_Bin_Borders[9][39][2] = 0.3; z_pT_Bin_Borders[9][39][3] = 0.38;
Phi_h_Bin_Values[9][39][0] =  1; Phi_h_Bin_Values[9][39][1] = 728; Phi_h_Bin_Values[9][39][2] = 6029;
z_pT_Bin_Borders[9][40][0] = 0.16; z_pT_Bin_Borders[9][40][1] = 0; z_pT_Bin_Borders[9][40][2] = 0.38; z_pT_Bin_Borders[9][40][3] = 0.46;
Phi_h_Bin_Values[9][40][0] =  1; Phi_h_Bin_Values[9][40][1] = 729; Phi_h_Bin_Values[9][40][2] = 6030;
z_pT_Bin_Borders[9][41][0] = 0.16; z_pT_Bin_Borders[9][41][1] = 0; z_pT_Bin_Borders[9][41][2] = 0.46; z_pT_Bin_Borders[9][41][3] = 0.58;
Phi_h_Bin_Values[9][41][0] =  1; Phi_h_Bin_Values[9][41][1] = 730; Phi_h_Bin_Values[9][41][2] = 6031;
z_pT_Bin_Borders[9][42][0] = 0.16; z_pT_Bin_Borders[9][42][1] = 0; z_pT_Bin_Borders[9][42][2] = 0.58; z_pT_Bin_Borders[9][42][3] = 0.74;
Phi_h_Bin_Values[9][42][0] =  1; Phi_h_Bin_Values[9][42][1] = 731; Phi_h_Bin_Values[9][42][2] = 6032;
z_pT_Bin_Borders[9][43][0] = 0.16; z_pT_Bin_Borders[9][43][1] = 0; z_pT_Bin_Borders[9][43][2] = 0.74; z_pT_Bin_Borders[9][43][3] = 0.95;
Phi_h_Bin_Values[9][43][0] =  1; Phi_h_Bin_Values[9][43][1] = 732; Phi_h_Bin_Values[9][43][2] = 6033;
z_pT_Bin_Borders[9][44][0] = 0.16; z_pT_Bin_Borders[9][44][1] = 0; z_pT_Bin_Borders[9][44][2] = 10; z_pT_Bin_Borders[9][44][3] = 0.95;
Phi_h_Bin_Values[9][44][0] =  1; Phi_h_Bin_Values[9][44][1] = 733; Phi_h_Bin_Values[9][44][2] = 6034;
z_pT_Bin_Borders[9][45][0] = 0.16; z_pT_Bin_Borders[9][45][1] = 0.2; z_pT_Bin_Borders[9][45][2] = 0.05; z_pT_Bin_Borders[9][45][3] = 0;
Phi_h_Bin_Values[9][45][0] =  1; Phi_h_Bin_Values[9][45][1] = 734; Phi_h_Bin_Values[9][45][2] = 6035;
z_pT_Bin_Borders[9][46][0] = 0.16; z_pT_Bin_Borders[9][46][1] = 0.2; z_pT_Bin_Borders[9][46][2] = 10; z_pT_Bin_Borders[9][46][3] = 0.95;
Phi_h_Bin_Values[9][46][0] =  1; Phi_h_Bin_Values[9][46][1] = 735; Phi_h_Bin_Values[9][46][2] = 6036;
z_pT_Bin_Borders[9][47][0] = 0.2; z_pT_Bin_Borders[9][47][1] = 0.24; z_pT_Bin_Borders[9][47][2] = 0.05; z_pT_Bin_Borders[9][47][3] = 0;
Phi_h_Bin_Values[9][47][0] =  1; Phi_h_Bin_Values[9][47][1] = 736; Phi_h_Bin_Values[9][47][2] = 6037;
z_pT_Bin_Borders[9][48][0] = 0.2; z_pT_Bin_Borders[9][48][1] = 0.24; z_pT_Bin_Borders[9][48][2] = 10; z_pT_Bin_Borders[9][48][3] = 0.95;
Phi_h_Bin_Values[9][48][0] =  1; Phi_h_Bin_Values[9][48][1] = 737; Phi_h_Bin_Values[9][48][2] = 6038;
z_pT_Bin_Borders[9][49][0] = 0.24; z_pT_Bin_Borders[9][49][1] = 0.3; z_pT_Bin_Borders[9][49][2] = 0.05; z_pT_Bin_Borders[9][49][3] = 0;
Phi_h_Bin_Values[9][49][0] =  1; Phi_h_Bin_Values[9][49][1] = 738; Phi_h_Bin_Values[9][49][2] = 6039;
z_pT_Bin_Borders[9][50][0] = 0.24; z_pT_Bin_Borders[9][50][1] = 0.3; z_pT_Bin_Borders[9][50][2] = 10; z_pT_Bin_Borders[9][50][3] = 0.95;
Phi_h_Bin_Values[9][50][0] =  1; Phi_h_Bin_Values[9][50][1] = 739; Phi_h_Bin_Values[9][50][2] = 6040;
z_pT_Bin_Borders[9][51][0] = 0.3; z_pT_Bin_Borders[9][51][1] = 0.42; z_pT_Bin_Borders[9][51][2] = 0.05; z_pT_Bin_Borders[9][51][3] = 0;
Phi_h_Bin_Values[9][51][0] =  1; Phi_h_Bin_Values[9][51][1] = 740; Phi_h_Bin_Values[9][51][2] = 6041;
z_pT_Bin_Borders[9][52][0] = 0.3; z_pT_Bin_Borders[9][52][1] = 0.42; z_pT_Bin_Borders[9][52][2] = 10; z_pT_Bin_Borders[9][52][3] = 0.95;
Phi_h_Bin_Values[9][52][0] =  1; Phi_h_Bin_Values[9][52][1] = 741; Phi_h_Bin_Values[9][52][2] = 6042;
z_pT_Bin_Borders[9][53][0] = 0.42; z_pT_Bin_Borders[9][53][1] = 0.7; z_pT_Bin_Borders[9][53][2] = 0.05; z_pT_Bin_Borders[9][53][3] = 0;
Phi_h_Bin_Values[9][53][0] =  1; Phi_h_Bin_Values[9][53][1] = 742; Phi_h_Bin_Values[9][53][2] = 6043;
z_pT_Bin_Borders[9][54][0] = 0.42; z_pT_Bin_Borders[9][54][1] = 0.7; z_pT_Bin_Borders[9][54][2] = 10; z_pT_Bin_Borders[9][54][3] = 0.95;
Phi_h_Bin_Values[9][54][0] =  1; Phi_h_Bin_Values[9][54][1] = 743; Phi_h_Bin_Values[9][54][2] = 6044;
z_pT_Bin_Borders[9][55][0] = 10; z_pT_Bin_Borders[9][55][1] = 0.7; z_pT_Bin_Borders[9][55][2] = 0; z_pT_Bin_Borders[9][55][3] = 0.05;
Phi_h_Bin_Values[9][55][0] =  1; Phi_h_Bin_Values[9][55][1] = 744; Phi_h_Bin_Values[9][55][2] = 6045;
z_pT_Bin_Borders[9][56][0] = 10; z_pT_Bin_Borders[9][56][1] = 0.7; z_pT_Bin_Borders[9][56][2] = 0.05; z_pT_Bin_Borders[9][56][3] = 0.22;
Phi_h_Bin_Values[9][56][0] =  1; Phi_h_Bin_Values[9][56][1] = 745; Phi_h_Bin_Values[9][56][2] = 6046;
z_pT_Bin_Borders[9][57][0] = 10; z_pT_Bin_Borders[9][57][1] = 0.7; z_pT_Bin_Borders[9][57][2] = 0.22; z_pT_Bin_Borders[9][57][3] = 0.3;
Phi_h_Bin_Values[9][57][0] =  1; Phi_h_Bin_Values[9][57][1] = 746; Phi_h_Bin_Values[9][57][2] = 6047;
z_pT_Bin_Borders[9][58][0] = 10; z_pT_Bin_Borders[9][58][1] = 0.7; z_pT_Bin_Borders[9][58][2] = 0.3; z_pT_Bin_Borders[9][58][3] = 0.38;
Phi_h_Bin_Values[9][58][0] =  1; Phi_h_Bin_Values[9][58][1] = 747; Phi_h_Bin_Values[9][58][2] = 6048;
z_pT_Bin_Borders[9][59][0] = 10; z_pT_Bin_Borders[9][59][1] = 0.7; z_pT_Bin_Borders[9][59][2] = 0.38; z_pT_Bin_Borders[9][59][3] = 0.46;
Phi_h_Bin_Values[9][59][0] =  1; Phi_h_Bin_Values[9][59][1] = 748; Phi_h_Bin_Values[9][59][2] = 6049;
z_pT_Bin_Borders[9][60][0] = 10; z_pT_Bin_Borders[9][60][1] = 0.7; z_pT_Bin_Borders[9][60][2] = 0.46; z_pT_Bin_Borders[9][60][3] = 0.58;
Phi_h_Bin_Values[9][60][0] =  1; Phi_h_Bin_Values[9][60][1] = 749; Phi_h_Bin_Values[9][60][2] = 6050;
z_pT_Bin_Borders[9][61][0] = 10; z_pT_Bin_Borders[9][61][1] = 0.7; z_pT_Bin_Borders[9][61][2] = 0.58; z_pT_Bin_Borders[9][61][3] = 0.74;
Phi_h_Bin_Values[9][61][0] =  1; Phi_h_Bin_Values[9][61][1] = 750; Phi_h_Bin_Values[9][61][2] = 6051;
z_pT_Bin_Borders[9][62][0] = 10; z_pT_Bin_Borders[9][62][1] = 0.7; z_pT_Bin_Borders[9][62][2] = 0.74; z_pT_Bin_Borders[9][62][3] = 0.95;
Phi_h_Bin_Values[9][62][0] =  1; Phi_h_Bin_Values[9][62][1] = 751; Phi_h_Bin_Values[9][62][2] = 6052;
z_pT_Bin_Borders[9][63][0] = 10; z_pT_Bin_Borders[9][63][1] = 0.7; z_pT_Bin_Borders[9][63][2] = 10; z_pT_Bin_Borders[9][63][3] = 0.95;
Phi_h_Bin_Values[9][63][0] =  1; Phi_h_Bin_Values[9][63][1] = 752; Phi_h_Bin_Values[9][63][2] = 6053;
z_pT_Bin_Borders[10][1][0] = 0.23; z_pT_Bin_Borders[10][1][1] = 0.19; z_pT_Bin_Borders[10][1][2] = 0.21; z_pT_Bin_Borders[10][1][3] = 0.05;
Phi_h_Bin_Values[10][1][0] =  24; Phi_h_Bin_Values[10][1][1] = 0; Phi_h_Bin_Values[10][1][2] = 6054;
z_pT_Bin_Borders[10][2][0] = 0.23; z_pT_Bin_Borders[10][2][1] = 0.19; z_pT_Bin_Borders[10][2][2] = 0.31; z_pT_Bin_Borders[10][2][3] = 0.21;
Phi_h_Bin_Values[10][2][0] =  24; Phi_h_Bin_Values[10][2][1] = 24; Phi_h_Bin_Values[10][2][2] = 6078;
z_pT_Bin_Borders[10][3][0] = 0.23; z_pT_Bin_Borders[10][3][1] = 0.19; z_pT_Bin_Borders[10][3][2] = 0.4; z_pT_Bin_Borders[10][3][3] = 0.31;
Phi_h_Bin_Values[10][3][0] =  24; Phi_h_Bin_Values[10][3][1] = 48; Phi_h_Bin_Values[10][3][2] = 6102;
z_pT_Bin_Borders[10][4][0] = 0.23; z_pT_Bin_Borders[10][4][1] = 0.19; z_pT_Bin_Borders[10][4][2] = 0.5; z_pT_Bin_Borders[10][4][3] = 0.4;
Phi_h_Bin_Values[10][4][0] =  24; Phi_h_Bin_Values[10][4][1] = 72; Phi_h_Bin_Values[10][4][2] = 6126;
z_pT_Bin_Borders[10][5][0] = 0.23; z_pT_Bin_Borders[10][5][1] = 0.19; z_pT_Bin_Borders[10][5][2] = 0.64; z_pT_Bin_Borders[10][5][3] = 0.5;
Phi_h_Bin_Values[10][5][0] =  1; Phi_h_Bin_Values[10][5][1] = 96; Phi_h_Bin_Values[10][5][2] = 6150;
z_pT_Bin_Borders[10][6][0] = 0.23; z_pT_Bin_Borders[10][6][1] = 0.19; z_pT_Bin_Borders[10][6][2] = 0.9; z_pT_Bin_Borders[10][6][3] = 0.64;
Phi_h_Bin_Values[10][6][0] =  1; Phi_h_Bin_Values[10][6][1] = 97; Phi_h_Bin_Values[10][6][2] = 6151;
z_pT_Bin_Borders[10][7][0] = 0.26; z_pT_Bin_Borders[10][7][1] = 0.23; z_pT_Bin_Borders[10][7][2] = 0.21; z_pT_Bin_Borders[10][7][3] = 0.05;
Phi_h_Bin_Values[10][7][0] =  24; Phi_h_Bin_Values[10][7][1] = 98; Phi_h_Bin_Values[10][7][2] = 6152;
z_pT_Bin_Borders[10][8][0] = 0.26; z_pT_Bin_Borders[10][8][1] = 0.23; z_pT_Bin_Borders[10][8][2] = 0.31; z_pT_Bin_Borders[10][8][3] = 0.21;
Phi_h_Bin_Values[10][8][0] =  24; Phi_h_Bin_Values[10][8][1] = 122; Phi_h_Bin_Values[10][8][2] = 6176;
z_pT_Bin_Borders[10][9][0] = 0.26; z_pT_Bin_Borders[10][9][1] = 0.23; z_pT_Bin_Borders[10][9][2] = 0.4; z_pT_Bin_Borders[10][9][3] = 0.31;
Phi_h_Bin_Values[10][9][0] =  24; Phi_h_Bin_Values[10][9][1] = 146; Phi_h_Bin_Values[10][9][2] = 6200;
z_pT_Bin_Borders[10][10][0] = 0.26; z_pT_Bin_Borders[10][10][1] = 0.23; z_pT_Bin_Borders[10][10][2] = 0.5; z_pT_Bin_Borders[10][10][3] = 0.4;
Phi_h_Bin_Values[10][10][0] =  24; Phi_h_Bin_Values[10][10][1] = 170; Phi_h_Bin_Values[10][10][2] = 6224;
z_pT_Bin_Borders[10][11][0] = 0.26; z_pT_Bin_Borders[10][11][1] = 0.23; z_pT_Bin_Borders[10][11][2] = 0.64; z_pT_Bin_Borders[10][11][3] = 0.5;
Phi_h_Bin_Values[10][11][0] =  24; Phi_h_Bin_Values[10][11][1] = 194; Phi_h_Bin_Values[10][11][2] = 6248;
z_pT_Bin_Borders[10][12][0] = 0.26; z_pT_Bin_Borders[10][12][1] = 0.23; z_pT_Bin_Borders[10][12][2] = 0.9; z_pT_Bin_Borders[10][12][3] = 0.64;
Phi_h_Bin_Values[10][12][0] =  1; Phi_h_Bin_Values[10][12][1] = 218; Phi_h_Bin_Values[10][12][2] = 6272;
z_pT_Bin_Borders[10][13][0] = 0.32; z_pT_Bin_Borders[10][13][1] = 0.26; z_pT_Bin_Borders[10][13][2] = 0.21; z_pT_Bin_Borders[10][13][3] = 0.05;
Phi_h_Bin_Values[10][13][0] =  24; Phi_h_Bin_Values[10][13][1] = 219; Phi_h_Bin_Values[10][13][2] = 6273;
z_pT_Bin_Borders[10][14][0] = 0.32; z_pT_Bin_Borders[10][14][1] = 0.26; z_pT_Bin_Borders[10][14][2] = 0.31; z_pT_Bin_Borders[10][14][3] = 0.21;
Phi_h_Bin_Values[10][14][0] =  24; Phi_h_Bin_Values[10][14][1] = 243; Phi_h_Bin_Values[10][14][2] = 6297;
z_pT_Bin_Borders[10][15][0] = 0.32; z_pT_Bin_Borders[10][15][1] = 0.26; z_pT_Bin_Borders[10][15][2] = 0.4; z_pT_Bin_Borders[10][15][3] = 0.31;
Phi_h_Bin_Values[10][15][0] =  24; Phi_h_Bin_Values[10][15][1] = 267; Phi_h_Bin_Values[10][15][2] = 6321;
z_pT_Bin_Borders[10][16][0] = 0.32; z_pT_Bin_Borders[10][16][1] = 0.26; z_pT_Bin_Borders[10][16][2] = 0.5; z_pT_Bin_Borders[10][16][3] = 0.4;
Phi_h_Bin_Values[10][16][0] =  24; Phi_h_Bin_Values[10][16][1] = 291; Phi_h_Bin_Values[10][16][2] = 6345;
z_pT_Bin_Borders[10][17][0] = 0.32; z_pT_Bin_Borders[10][17][1] = 0.26; z_pT_Bin_Borders[10][17][2] = 0.64; z_pT_Bin_Borders[10][17][3] = 0.5;
Phi_h_Bin_Values[10][17][0] =  24; Phi_h_Bin_Values[10][17][1] = 315; Phi_h_Bin_Values[10][17][2] = 6369;
z_pT_Bin_Borders[10][18][0] = 0.32; z_pT_Bin_Borders[10][18][1] = 0.26; z_pT_Bin_Borders[10][18][2] = 0.9; z_pT_Bin_Borders[10][18][3] = 0.64;
Phi_h_Bin_Values[10][18][0] =  1; Phi_h_Bin_Values[10][18][1] = 339; Phi_h_Bin_Values[10][18][2] = 6393;
z_pT_Bin_Borders[10][19][0] = 0.4; z_pT_Bin_Borders[10][19][1] = 0.32; z_pT_Bin_Borders[10][19][2] = 0.21; z_pT_Bin_Borders[10][19][3] = 0.05;
Phi_h_Bin_Values[10][19][0] =  24; Phi_h_Bin_Values[10][19][1] = 340; Phi_h_Bin_Values[10][19][2] = 6394;
z_pT_Bin_Borders[10][20][0] = 0.4; z_pT_Bin_Borders[10][20][1] = 0.32; z_pT_Bin_Borders[10][20][2] = 0.31; z_pT_Bin_Borders[10][20][3] = 0.21;
Phi_h_Bin_Values[10][20][0] =  24; Phi_h_Bin_Values[10][20][1] = 364; Phi_h_Bin_Values[10][20][2] = 6418;
z_pT_Bin_Borders[10][21][0] = 0.4; z_pT_Bin_Borders[10][21][1] = 0.32; z_pT_Bin_Borders[10][21][2] = 0.4; z_pT_Bin_Borders[10][21][3] = 0.31;
Phi_h_Bin_Values[10][21][0] =  24; Phi_h_Bin_Values[10][21][1] = 388; Phi_h_Bin_Values[10][21][2] = 6442;
z_pT_Bin_Borders[10][22][0] = 0.4; z_pT_Bin_Borders[10][22][1] = 0.32; z_pT_Bin_Borders[10][22][2] = 0.5; z_pT_Bin_Borders[10][22][3] = 0.4;
Phi_h_Bin_Values[10][22][0] =  24; Phi_h_Bin_Values[10][22][1] = 412; Phi_h_Bin_Values[10][22][2] = 6466;
z_pT_Bin_Borders[10][23][0] = 0.4; z_pT_Bin_Borders[10][23][1] = 0.32; z_pT_Bin_Borders[10][23][2] = 0.64; z_pT_Bin_Borders[10][23][3] = 0.5;
Phi_h_Bin_Values[10][23][0] =  24; Phi_h_Bin_Values[10][23][1] = 436; Phi_h_Bin_Values[10][23][2] = 6490;
z_pT_Bin_Borders[10][24][0] = 0.4; z_pT_Bin_Borders[10][24][1] = 0.32; z_pT_Bin_Borders[10][24][2] = 0.9; z_pT_Bin_Borders[10][24][3] = 0.64;
Phi_h_Bin_Values[10][24][0] =  24; Phi_h_Bin_Values[10][24][1] = 460; Phi_h_Bin_Values[10][24][2] = 6514;
z_pT_Bin_Borders[10][25][0] = 0.5; z_pT_Bin_Borders[10][25][1] = 0.4; z_pT_Bin_Borders[10][25][2] = 0.21; z_pT_Bin_Borders[10][25][3] = 0.05;
Phi_h_Bin_Values[10][25][0] =  24; Phi_h_Bin_Values[10][25][1] = 484; Phi_h_Bin_Values[10][25][2] = 6538;
z_pT_Bin_Borders[10][26][0] = 0.5; z_pT_Bin_Borders[10][26][1] = 0.4; z_pT_Bin_Borders[10][26][2] = 0.31; z_pT_Bin_Borders[10][26][3] = 0.21;
Phi_h_Bin_Values[10][26][0] =  24; Phi_h_Bin_Values[10][26][1] = 508; Phi_h_Bin_Values[10][26][2] = 6562;
z_pT_Bin_Borders[10][27][0] = 0.5; z_pT_Bin_Borders[10][27][1] = 0.4; z_pT_Bin_Borders[10][27][2] = 0.4; z_pT_Bin_Borders[10][27][3] = 0.31;
Phi_h_Bin_Values[10][27][0] =  24; Phi_h_Bin_Values[10][27][1] = 532; Phi_h_Bin_Values[10][27][2] = 6586;
z_pT_Bin_Borders[10][28][0] = 0.5; z_pT_Bin_Borders[10][28][1] = 0.4; z_pT_Bin_Borders[10][28][2] = 0.5; z_pT_Bin_Borders[10][28][3] = 0.4;
Phi_h_Bin_Values[10][28][0] =  24; Phi_h_Bin_Values[10][28][1] = 556; Phi_h_Bin_Values[10][28][2] = 6610;
z_pT_Bin_Borders[10][29][0] = 0.5; z_pT_Bin_Borders[10][29][1] = 0.4; z_pT_Bin_Borders[10][29][2] = 0.64; z_pT_Bin_Borders[10][29][3] = 0.5;
Phi_h_Bin_Values[10][29][0] =  24; Phi_h_Bin_Values[10][29][1] = 580; Phi_h_Bin_Values[10][29][2] = 6634;
z_pT_Bin_Borders[10][30][0] = 0.5; z_pT_Bin_Borders[10][30][1] = 0.4; z_pT_Bin_Borders[10][30][2] = 0.9; z_pT_Bin_Borders[10][30][3] = 0.64;
Phi_h_Bin_Values[10][30][0] =  24; Phi_h_Bin_Values[10][30][1] = 604; Phi_h_Bin_Values[10][30][2] = 6658;
z_pT_Bin_Borders[10][31][0] = 0.72; z_pT_Bin_Borders[10][31][1] = 0.5; z_pT_Bin_Borders[10][31][2] = 0.21; z_pT_Bin_Borders[10][31][3] = 0.05;
Phi_h_Bin_Values[10][31][0] =  24; Phi_h_Bin_Values[10][31][1] = 628; Phi_h_Bin_Values[10][31][2] = 6682;
z_pT_Bin_Borders[10][32][0] = 0.72; z_pT_Bin_Borders[10][32][1] = 0.5; z_pT_Bin_Borders[10][32][2] = 0.31; z_pT_Bin_Borders[10][32][3] = 0.21;
Phi_h_Bin_Values[10][32][0] =  24; Phi_h_Bin_Values[10][32][1] = 652; Phi_h_Bin_Values[10][32][2] = 6706;
z_pT_Bin_Borders[10][33][0] = 0.72; z_pT_Bin_Borders[10][33][1] = 0.5; z_pT_Bin_Borders[10][33][2] = 0.4; z_pT_Bin_Borders[10][33][3] = 0.31;
Phi_h_Bin_Values[10][33][0] =  24; Phi_h_Bin_Values[10][33][1] = 676; Phi_h_Bin_Values[10][33][2] = 6730;
z_pT_Bin_Borders[10][34][0] = 0.72; z_pT_Bin_Borders[10][34][1] = 0.5; z_pT_Bin_Borders[10][34][2] = 0.5; z_pT_Bin_Borders[10][34][3] = 0.4;
Phi_h_Bin_Values[10][34][0] =  24; Phi_h_Bin_Values[10][34][1] = 700; Phi_h_Bin_Values[10][34][2] = 6754;
z_pT_Bin_Borders[10][35][0] = 0.72; z_pT_Bin_Borders[10][35][1] = 0.5; z_pT_Bin_Borders[10][35][2] = 0.64; z_pT_Bin_Borders[10][35][3] = 0.5;
Phi_h_Bin_Values[10][35][0] =  24; Phi_h_Bin_Values[10][35][1] = 724; Phi_h_Bin_Values[10][35][2] = 6778;
z_pT_Bin_Borders[10][36][0] = 0.72; z_pT_Bin_Borders[10][36][1] = 0.5; z_pT_Bin_Borders[10][36][2] = 0.9; z_pT_Bin_Borders[10][36][3] = 0.64;
Phi_h_Bin_Values[10][36][0] =  1; Phi_h_Bin_Values[10][36][1] = 748; Phi_h_Bin_Values[10][36][2] = 6802;
z_pT_Bin_Borders[10][37][0] = 0.19; z_pT_Bin_Borders[10][37][1] = 0; z_pT_Bin_Borders[10][37][2] = 0.05; z_pT_Bin_Borders[10][37][3] = 0;
Phi_h_Bin_Values[10][37][0] =  1; Phi_h_Bin_Values[10][37][1] = 749; Phi_h_Bin_Values[10][37][2] = 6803;
z_pT_Bin_Borders[10][38][0] = 0.19; z_pT_Bin_Borders[10][38][1] = 0; z_pT_Bin_Borders[10][38][2] = 0.05; z_pT_Bin_Borders[10][38][3] = 0.21;
Phi_h_Bin_Values[10][38][0] =  1; Phi_h_Bin_Values[10][38][1] = 750; Phi_h_Bin_Values[10][38][2] = 6804;
z_pT_Bin_Borders[10][39][0] = 0.19; z_pT_Bin_Borders[10][39][1] = 0; z_pT_Bin_Borders[10][39][2] = 0.21; z_pT_Bin_Borders[10][39][3] = 0.31;
Phi_h_Bin_Values[10][39][0] =  1; Phi_h_Bin_Values[10][39][1] = 751; Phi_h_Bin_Values[10][39][2] = 6805;
z_pT_Bin_Borders[10][40][0] = 0.19; z_pT_Bin_Borders[10][40][1] = 0; z_pT_Bin_Borders[10][40][2] = 0.31; z_pT_Bin_Borders[10][40][3] = 0.4;
Phi_h_Bin_Values[10][40][0] =  1; Phi_h_Bin_Values[10][40][1] = 752; Phi_h_Bin_Values[10][40][2] = 6806;
z_pT_Bin_Borders[10][41][0] = 0.19; z_pT_Bin_Borders[10][41][1] = 0; z_pT_Bin_Borders[10][41][2] = 0.4; z_pT_Bin_Borders[10][41][3] = 0.5;
Phi_h_Bin_Values[10][41][0] =  1; Phi_h_Bin_Values[10][41][1] = 753; Phi_h_Bin_Values[10][41][2] = 6807;
z_pT_Bin_Borders[10][42][0] = 0.19; z_pT_Bin_Borders[10][42][1] = 0; z_pT_Bin_Borders[10][42][2] = 0.5; z_pT_Bin_Borders[10][42][3] = 0.64;
Phi_h_Bin_Values[10][42][0] =  1; Phi_h_Bin_Values[10][42][1] = 754; Phi_h_Bin_Values[10][42][2] = 6808;
z_pT_Bin_Borders[10][43][0] = 0.19; z_pT_Bin_Borders[10][43][1] = 0; z_pT_Bin_Borders[10][43][2] = 0.64; z_pT_Bin_Borders[10][43][3] = 0.9;
Phi_h_Bin_Values[10][43][0] =  1; Phi_h_Bin_Values[10][43][1] = 755; Phi_h_Bin_Values[10][43][2] = 6809;
z_pT_Bin_Borders[10][44][0] = 0.19; z_pT_Bin_Borders[10][44][1] = 0; z_pT_Bin_Borders[10][44][2] = 10; z_pT_Bin_Borders[10][44][3] = 0.9;
Phi_h_Bin_Values[10][44][0] =  1; Phi_h_Bin_Values[10][44][1] = 756; Phi_h_Bin_Values[10][44][2] = 6810;
z_pT_Bin_Borders[10][45][0] = 0.19; z_pT_Bin_Borders[10][45][1] = 0.23; z_pT_Bin_Borders[10][45][2] = 0.05; z_pT_Bin_Borders[10][45][3] = 0;
Phi_h_Bin_Values[10][45][0] =  1; Phi_h_Bin_Values[10][45][1] = 757; Phi_h_Bin_Values[10][45][2] = 6811;
z_pT_Bin_Borders[10][46][0] = 0.19; z_pT_Bin_Borders[10][46][1] = 0.23; z_pT_Bin_Borders[10][46][2] = 10; z_pT_Bin_Borders[10][46][3] = 0.9;
Phi_h_Bin_Values[10][46][0] =  1; Phi_h_Bin_Values[10][46][1] = 758; Phi_h_Bin_Values[10][46][2] = 6812;
z_pT_Bin_Borders[10][47][0] = 0.23; z_pT_Bin_Borders[10][47][1] = 0.26; z_pT_Bin_Borders[10][47][2] = 0.05; z_pT_Bin_Borders[10][47][3] = 0;
Phi_h_Bin_Values[10][47][0] =  1; Phi_h_Bin_Values[10][47][1] = 759; Phi_h_Bin_Values[10][47][2] = 6813;
z_pT_Bin_Borders[10][48][0] = 0.23; z_pT_Bin_Borders[10][48][1] = 0.26; z_pT_Bin_Borders[10][48][2] = 10; z_pT_Bin_Borders[10][48][3] = 0.9;
Phi_h_Bin_Values[10][48][0] =  1; Phi_h_Bin_Values[10][48][1] = 760; Phi_h_Bin_Values[10][48][2] = 6814;
z_pT_Bin_Borders[10][49][0] = 0.26; z_pT_Bin_Borders[10][49][1] = 0.32; z_pT_Bin_Borders[10][49][2] = 0.05; z_pT_Bin_Borders[10][49][3] = 0;
Phi_h_Bin_Values[10][49][0] =  1; Phi_h_Bin_Values[10][49][1] = 761; Phi_h_Bin_Values[10][49][2] = 6815;
z_pT_Bin_Borders[10][50][0] = 0.26; z_pT_Bin_Borders[10][50][1] = 0.32; z_pT_Bin_Borders[10][50][2] = 10; z_pT_Bin_Borders[10][50][3] = 0.9;
Phi_h_Bin_Values[10][50][0] =  1; Phi_h_Bin_Values[10][50][1] = 762; Phi_h_Bin_Values[10][50][2] = 6816;
z_pT_Bin_Borders[10][51][0] = 0.32; z_pT_Bin_Borders[10][51][1] = 0.4; z_pT_Bin_Borders[10][51][2] = 0.05; z_pT_Bin_Borders[10][51][3] = 0;
Phi_h_Bin_Values[10][51][0] =  1; Phi_h_Bin_Values[10][51][1] = 763; Phi_h_Bin_Values[10][51][2] = 6817;
z_pT_Bin_Borders[10][52][0] = 0.32; z_pT_Bin_Borders[10][52][1] = 0.4; z_pT_Bin_Borders[10][52][2] = 10; z_pT_Bin_Borders[10][52][3] = 0.9;
Phi_h_Bin_Values[10][52][0] =  1; Phi_h_Bin_Values[10][52][1] = 764; Phi_h_Bin_Values[10][52][2] = 6818;
z_pT_Bin_Borders[10][53][0] = 0.4; z_pT_Bin_Borders[10][53][1] = 0.5; z_pT_Bin_Borders[10][53][2] = 0.05; z_pT_Bin_Borders[10][53][3] = 0;
Phi_h_Bin_Values[10][53][0] =  1; Phi_h_Bin_Values[10][53][1] = 765; Phi_h_Bin_Values[10][53][2] = 6819;
z_pT_Bin_Borders[10][54][0] = 0.4; z_pT_Bin_Borders[10][54][1] = 0.5; z_pT_Bin_Borders[10][54][2] = 10; z_pT_Bin_Borders[10][54][3] = 0.9;
Phi_h_Bin_Values[10][54][0] =  1; Phi_h_Bin_Values[10][54][1] = 766; Phi_h_Bin_Values[10][54][2] = 6820;
z_pT_Bin_Borders[10][55][0] = 0.5; z_pT_Bin_Borders[10][55][1] = 0.72; z_pT_Bin_Borders[10][55][2] = 0.05; z_pT_Bin_Borders[10][55][3] = 0;
Phi_h_Bin_Values[10][55][0] =  1; Phi_h_Bin_Values[10][55][1] = 767; Phi_h_Bin_Values[10][55][2] = 6821;
z_pT_Bin_Borders[10][56][0] = 0.5; z_pT_Bin_Borders[10][56][1] = 0.72; z_pT_Bin_Borders[10][56][2] = 10; z_pT_Bin_Borders[10][56][3] = 0.9;
Phi_h_Bin_Values[10][56][0] =  1; Phi_h_Bin_Values[10][56][1] = 768; Phi_h_Bin_Values[10][56][2] = 6822;
z_pT_Bin_Borders[10][57][0] = 10; z_pT_Bin_Borders[10][57][1] = 0.72; z_pT_Bin_Borders[10][57][2] = 0; z_pT_Bin_Borders[10][57][3] = 0.05;
Phi_h_Bin_Values[10][57][0] =  1; Phi_h_Bin_Values[10][57][1] = 769; Phi_h_Bin_Values[10][57][2] = 6823;
z_pT_Bin_Borders[10][58][0] = 10; z_pT_Bin_Borders[10][58][1] = 0.72; z_pT_Bin_Borders[10][58][2] = 0.05; z_pT_Bin_Borders[10][58][3] = 0.21;
Phi_h_Bin_Values[10][58][0] =  1; Phi_h_Bin_Values[10][58][1] = 770; Phi_h_Bin_Values[10][58][2] = 6824;
z_pT_Bin_Borders[10][59][0] = 10; z_pT_Bin_Borders[10][59][1] = 0.72; z_pT_Bin_Borders[10][59][2] = 0.21; z_pT_Bin_Borders[10][59][3] = 0.31;
Phi_h_Bin_Values[10][59][0] =  1; Phi_h_Bin_Values[10][59][1] = 771; Phi_h_Bin_Values[10][59][2] = 6825;
z_pT_Bin_Borders[10][60][0] = 10; z_pT_Bin_Borders[10][60][1] = 0.72; z_pT_Bin_Borders[10][60][2] = 0.31; z_pT_Bin_Borders[10][60][3] = 0.4;
Phi_h_Bin_Values[10][60][0] =  1; Phi_h_Bin_Values[10][60][1] = 772; Phi_h_Bin_Values[10][60][2] = 6826;
z_pT_Bin_Borders[10][61][0] = 10; z_pT_Bin_Borders[10][61][1] = 0.72; z_pT_Bin_Borders[10][61][2] = 0.4; z_pT_Bin_Borders[10][61][3] = 0.5;
Phi_h_Bin_Values[10][61][0] =  1; Phi_h_Bin_Values[10][61][1] = 773; Phi_h_Bin_Values[10][61][2] = 6827;
z_pT_Bin_Borders[10][62][0] = 10; z_pT_Bin_Borders[10][62][1] = 0.72; z_pT_Bin_Borders[10][62][2] = 0.5; z_pT_Bin_Borders[10][62][3] = 0.64;
Phi_h_Bin_Values[10][62][0] =  1; Phi_h_Bin_Values[10][62][1] = 774; Phi_h_Bin_Values[10][62][2] = 6828;
z_pT_Bin_Borders[10][63][0] = 10; z_pT_Bin_Borders[10][63][1] = 0.72; z_pT_Bin_Borders[10][63][2] = 0.64; z_pT_Bin_Borders[10][63][3] = 0.9;
Phi_h_Bin_Values[10][63][0] =  1; Phi_h_Bin_Values[10][63][1] = 775; Phi_h_Bin_Values[10][63][2] = 6829;
z_pT_Bin_Borders[10][64][0] = 10; z_pT_Bin_Borders[10][64][1] = 0.72; z_pT_Bin_Borders[10][64][2] = 10; z_pT_Bin_Borders[10][64][3] = 0.9;
Phi_h_Bin_Values[10][64][0] =  1; Phi_h_Bin_Values[10][64][1] = 776; Phi_h_Bin_Values[10][64][2] = 6830;
z_pT_Bin_Borders[11][1][0] = 0.27; z_pT_Bin_Borders[11][1][1] = 0.22; z_pT_Bin_Borders[11][1][2] = 0.2; z_pT_Bin_Borders[11][1][3] = 0.05;
Phi_h_Bin_Values[11][1][0] =  24; Phi_h_Bin_Values[11][1][1] = 0; Phi_h_Bin_Values[11][1][2] = 6831;
z_pT_Bin_Borders[11][2][0] = 0.27; z_pT_Bin_Borders[11][2][1] = 0.22; z_pT_Bin_Borders[11][2][2] = 0.3; z_pT_Bin_Borders[11][2][3] = 0.2;
Phi_h_Bin_Values[11][2][0] =  24; Phi_h_Bin_Values[11][2][1] = 24; Phi_h_Bin_Values[11][2][2] = 6855;
z_pT_Bin_Borders[11][3][0] = 0.27; z_pT_Bin_Borders[11][3][1] = 0.22; z_pT_Bin_Borders[11][3][2] = 0.4; z_pT_Bin_Borders[11][3][3] = 0.3;
Phi_h_Bin_Values[11][3][0] =  24; Phi_h_Bin_Values[11][3][1] = 48; Phi_h_Bin_Values[11][3][2] = 6879;
z_pT_Bin_Borders[11][4][0] = 0.27; z_pT_Bin_Borders[11][4][1] = 0.22; z_pT_Bin_Borders[11][4][2] = 0.54; z_pT_Bin_Borders[11][4][3] = 0.4;
Phi_h_Bin_Values[11][4][0] =  24; Phi_h_Bin_Values[11][4][1] = 72; Phi_h_Bin_Values[11][4][2] = 6903;
z_pT_Bin_Borders[11][5][0] = 0.27; z_pT_Bin_Borders[11][5][1] = 0.22; z_pT_Bin_Borders[11][5][2] = 0.69; z_pT_Bin_Borders[11][5][3] = 0.54;
Phi_h_Bin_Values[11][5][0] =  1; Phi_h_Bin_Values[11][5][1] = 96; Phi_h_Bin_Values[11][5][2] = 6927;
z_pT_Bin_Borders[11][6][0] = 0.32; z_pT_Bin_Borders[11][6][1] = 0.27; z_pT_Bin_Borders[11][6][2] = 0.2; z_pT_Bin_Borders[11][6][3] = 0.05;
Phi_h_Bin_Values[11][6][0] =  24; Phi_h_Bin_Values[11][6][1] = 97; Phi_h_Bin_Values[11][6][2] = 6928;
z_pT_Bin_Borders[11][7][0] = 0.32; z_pT_Bin_Borders[11][7][1] = 0.27; z_pT_Bin_Borders[11][7][2] = 0.3; z_pT_Bin_Borders[11][7][3] = 0.2;
Phi_h_Bin_Values[11][7][0] =  24; Phi_h_Bin_Values[11][7][1] = 121; Phi_h_Bin_Values[11][7][2] = 6952;
z_pT_Bin_Borders[11][8][0] = 0.32; z_pT_Bin_Borders[11][8][1] = 0.27; z_pT_Bin_Borders[11][8][2] = 0.4; z_pT_Bin_Borders[11][8][3] = 0.3;
Phi_h_Bin_Values[11][8][0] =  24; Phi_h_Bin_Values[11][8][1] = 145; Phi_h_Bin_Values[11][8][2] = 6976;
z_pT_Bin_Borders[11][9][0] = 0.32; z_pT_Bin_Borders[11][9][1] = 0.27; z_pT_Bin_Borders[11][9][2] = 0.54; z_pT_Bin_Borders[11][9][3] = 0.4;
Phi_h_Bin_Values[11][9][0] =  24; Phi_h_Bin_Values[11][9][1] = 169; Phi_h_Bin_Values[11][9][2] = 7000;
z_pT_Bin_Borders[11][10][0] = 0.32; z_pT_Bin_Borders[11][10][1] = 0.27; z_pT_Bin_Borders[11][10][2] = 0.69; z_pT_Bin_Borders[11][10][3] = 0.54;
Phi_h_Bin_Values[11][10][0] =  24; Phi_h_Bin_Values[11][10][1] = 193; Phi_h_Bin_Values[11][10][2] = 7024;
z_pT_Bin_Borders[11][11][0] = 0.4; z_pT_Bin_Borders[11][11][1] = 0.32; z_pT_Bin_Borders[11][11][2] = 0.2; z_pT_Bin_Borders[11][11][3] = 0.05;
Phi_h_Bin_Values[11][11][0] =  24; Phi_h_Bin_Values[11][11][1] = 217; Phi_h_Bin_Values[11][11][2] = 7048;
z_pT_Bin_Borders[11][12][0] = 0.4; z_pT_Bin_Borders[11][12][1] = 0.32; z_pT_Bin_Borders[11][12][2] = 0.3; z_pT_Bin_Borders[11][12][3] = 0.2;
Phi_h_Bin_Values[11][12][0] =  24; Phi_h_Bin_Values[11][12][1] = 241; Phi_h_Bin_Values[11][12][2] = 7072;
z_pT_Bin_Borders[11][13][0] = 0.4; z_pT_Bin_Borders[11][13][1] = 0.32; z_pT_Bin_Borders[11][13][2] = 0.4; z_pT_Bin_Borders[11][13][3] = 0.3;
Phi_h_Bin_Values[11][13][0] =  24; Phi_h_Bin_Values[11][13][1] = 265; Phi_h_Bin_Values[11][13][2] = 7096;
z_pT_Bin_Borders[11][14][0] = 0.4; z_pT_Bin_Borders[11][14][1] = 0.32; z_pT_Bin_Borders[11][14][2] = 0.54; z_pT_Bin_Borders[11][14][3] = 0.4;
Phi_h_Bin_Values[11][14][0] =  24; Phi_h_Bin_Values[11][14][1] = 289; Phi_h_Bin_Values[11][14][2] = 7120;
z_pT_Bin_Borders[11][15][0] = 0.4; z_pT_Bin_Borders[11][15][1] = 0.32; z_pT_Bin_Borders[11][15][2] = 0.69; z_pT_Bin_Borders[11][15][3] = 0.54;
Phi_h_Bin_Values[11][15][0] =  24; Phi_h_Bin_Values[11][15][1] = 313; Phi_h_Bin_Values[11][15][2] = 7144;
z_pT_Bin_Borders[11][16][0] = 0.53; z_pT_Bin_Borders[11][16][1] = 0.4; z_pT_Bin_Borders[11][16][2] = 0.2; z_pT_Bin_Borders[11][16][3] = 0.05;
Phi_h_Bin_Values[11][16][0] =  24; Phi_h_Bin_Values[11][16][1] = 337; Phi_h_Bin_Values[11][16][2] = 7168;
z_pT_Bin_Borders[11][17][0] = 0.53; z_pT_Bin_Borders[11][17][1] = 0.4; z_pT_Bin_Borders[11][17][2] = 0.3; z_pT_Bin_Borders[11][17][3] = 0.2;
Phi_h_Bin_Values[11][17][0] =  24; Phi_h_Bin_Values[11][17][1] = 361; Phi_h_Bin_Values[11][17][2] = 7192;
z_pT_Bin_Borders[11][18][0] = 0.53; z_pT_Bin_Borders[11][18][1] = 0.4; z_pT_Bin_Borders[11][18][2] = 0.4; z_pT_Bin_Borders[11][18][3] = 0.3;
Phi_h_Bin_Values[11][18][0] =  24; Phi_h_Bin_Values[11][18][1] = 385; Phi_h_Bin_Values[11][18][2] = 7216;
z_pT_Bin_Borders[11][19][0] = 0.53; z_pT_Bin_Borders[11][19][1] = 0.4; z_pT_Bin_Borders[11][19][2] = 0.54; z_pT_Bin_Borders[11][19][3] = 0.4;
Phi_h_Bin_Values[11][19][0] =  24; Phi_h_Bin_Values[11][19][1] = 409; Phi_h_Bin_Values[11][19][2] = 7240;
z_pT_Bin_Borders[11][20][0] = 0.53; z_pT_Bin_Borders[11][20][1] = 0.4; z_pT_Bin_Borders[11][20][2] = 0.69; z_pT_Bin_Borders[11][20][3] = 0.54;
Phi_h_Bin_Values[11][20][0] =  24; Phi_h_Bin_Values[11][20][1] = 433; Phi_h_Bin_Values[11][20][2] = 7264;
z_pT_Bin_Borders[11][21][0] = 0.69; z_pT_Bin_Borders[11][21][1] = 0.53; z_pT_Bin_Borders[11][21][2] = 0.2; z_pT_Bin_Borders[11][21][3] = 0.05;
Phi_h_Bin_Values[11][21][0] =  24; Phi_h_Bin_Values[11][21][1] = 457; Phi_h_Bin_Values[11][21][2] = 7288;
z_pT_Bin_Borders[11][22][0] = 0.69; z_pT_Bin_Borders[11][22][1] = 0.53; z_pT_Bin_Borders[11][22][2] = 0.3; z_pT_Bin_Borders[11][22][3] = 0.2;
Phi_h_Bin_Values[11][22][0] =  24; Phi_h_Bin_Values[11][22][1] = 481; Phi_h_Bin_Values[11][22][2] = 7312;
z_pT_Bin_Borders[11][23][0] = 0.69; z_pT_Bin_Borders[11][23][1] = 0.53; z_pT_Bin_Borders[11][23][2] = 0.4; z_pT_Bin_Borders[11][23][3] = 0.3;
Phi_h_Bin_Values[11][23][0] =  1; Phi_h_Bin_Values[11][23][1] = 505; Phi_h_Bin_Values[11][23][2] = 7336;
z_pT_Bin_Borders[11][24][0] = 0.69; z_pT_Bin_Borders[11][24][1] = 0.53; z_pT_Bin_Borders[11][24][2] = 0.54; z_pT_Bin_Borders[11][24][3] = 0.4;
Phi_h_Bin_Values[11][24][0] =  1; Phi_h_Bin_Values[11][24][1] = 506; Phi_h_Bin_Values[11][24][2] = 7337;
z_pT_Bin_Borders[11][25][0] = 0.69; z_pT_Bin_Borders[11][25][1] = 0.53; z_pT_Bin_Borders[11][25][2] = 0.69; z_pT_Bin_Borders[11][25][3] = 0.54;
Phi_h_Bin_Values[11][25][0] =  1; Phi_h_Bin_Values[11][25][1] = 507; Phi_h_Bin_Values[11][25][2] = 7338;
z_pT_Bin_Borders[11][26][0] = 0.22; z_pT_Bin_Borders[11][26][1] = 0; z_pT_Bin_Borders[11][26][2] = 0.05; z_pT_Bin_Borders[11][26][3] = 0;
Phi_h_Bin_Values[11][26][0] =  1; Phi_h_Bin_Values[11][26][1] = 508; Phi_h_Bin_Values[11][26][2] = 7339;
z_pT_Bin_Borders[11][27][0] = 0.22; z_pT_Bin_Borders[11][27][1] = 0; z_pT_Bin_Borders[11][27][2] = 0.05; z_pT_Bin_Borders[11][27][3] = 0.2;
Phi_h_Bin_Values[11][27][0] =  1; Phi_h_Bin_Values[11][27][1] = 509; Phi_h_Bin_Values[11][27][2] = 7340;
z_pT_Bin_Borders[11][28][0] = 0.22; z_pT_Bin_Borders[11][28][1] = 0; z_pT_Bin_Borders[11][28][2] = 0.2; z_pT_Bin_Borders[11][28][3] = 0.3;
Phi_h_Bin_Values[11][28][0] =  1; Phi_h_Bin_Values[11][28][1] = 510; Phi_h_Bin_Values[11][28][2] = 7341;
z_pT_Bin_Borders[11][29][0] = 0.22; z_pT_Bin_Borders[11][29][1] = 0; z_pT_Bin_Borders[11][29][2] = 0.3; z_pT_Bin_Borders[11][29][3] = 0.4;
Phi_h_Bin_Values[11][29][0] =  1; Phi_h_Bin_Values[11][29][1] = 511; Phi_h_Bin_Values[11][29][2] = 7342;
z_pT_Bin_Borders[11][30][0] = 0.22; z_pT_Bin_Borders[11][30][1] = 0; z_pT_Bin_Borders[11][30][2] = 0.4; z_pT_Bin_Borders[11][30][3] = 0.54;
Phi_h_Bin_Values[11][30][0] =  1; Phi_h_Bin_Values[11][30][1] = 512; Phi_h_Bin_Values[11][30][2] = 7343;
z_pT_Bin_Borders[11][31][0] = 0.22; z_pT_Bin_Borders[11][31][1] = 0; z_pT_Bin_Borders[11][31][2] = 0.54; z_pT_Bin_Borders[11][31][3] = 0.69;
Phi_h_Bin_Values[11][31][0] =  1; Phi_h_Bin_Values[11][31][1] = 513; Phi_h_Bin_Values[11][31][2] = 7344;
z_pT_Bin_Borders[11][32][0] = 0.22; z_pT_Bin_Borders[11][32][1] = 0; z_pT_Bin_Borders[11][32][2] = 10; z_pT_Bin_Borders[11][32][3] = 0.69;
Phi_h_Bin_Values[11][32][0] =  1; Phi_h_Bin_Values[11][32][1] = 514; Phi_h_Bin_Values[11][32][2] = 7345;
z_pT_Bin_Borders[11][33][0] = 0.22; z_pT_Bin_Borders[11][33][1] = 0.27; z_pT_Bin_Borders[11][33][2] = 0.05; z_pT_Bin_Borders[11][33][3] = 0;
Phi_h_Bin_Values[11][33][0] =  1; Phi_h_Bin_Values[11][33][1] = 515; Phi_h_Bin_Values[11][33][2] = 7346;
z_pT_Bin_Borders[11][34][0] = 0.22; z_pT_Bin_Borders[11][34][1] = 0.27; z_pT_Bin_Borders[11][34][2] = 10; z_pT_Bin_Borders[11][34][3] = 0.69;
Phi_h_Bin_Values[11][34][0] =  1; Phi_h_Bin_Values[11][34][1] = 516; Phi_h_Bin_Values[11][34][2] = 7347;
z_pT_Bin_Borders[11][35][0] = 0.27; z_pT_Bin_Borders[11][35][1] = 0.32; z_pT_Bin_Borders[11][35][2] = 0.05; z_pT_Bin_Borders[11][35][3] = 0;
Phi_h_Bin_Values[11][35][0] =  1; Phi_h_Bin_Values[11][35][1] = 517; Phi_h_Bin_Values[11][35][2] = 7348;
z_pT_Bin_Borders[11][36][0] = 0.27; z_pT_Bin_Borders[11][36][1] = 0.32; z_pT_Bin_Borders[11][36][2] = 10; z_pT_Bin_Borders[11][36][3] = 0.69;
Phi_h_Bin_Values[11][36][0] =  1; Phi_h_Bin_Values[11][36][1] = 518; Phi_h_Bin_Values[11][36][2] = 7349;
z_pT_Bin_Borders[11][37][0] = 0.32; z_pT_Bin_Borders[11][37][1] = 0.4; z_pT_Bin_Borders[11][37][2] = 0.05; z_pT_Bin_Borders[11][37][3] = 0;
Phi_h_Bin_Values[11][37][0] =  1; Phi_h_Bin_Values[11][37][1] = 519; Phi_h_Bin_Values[11][37][2] = 7350;
z_pT_Bin_Borders[11][38][0] = 0.32; z_pT_Bin_Borders[11][38][1] = 0.4; z_pT_Bin_Borders[11][38][2] = 10; z_pT_Bin_Borders[11][38][3] = 0.69;
Phi_h_Bin_Values[11][38][0] =  1; Phi_h_Bin_Values[11][38][1] = 520; Phi_h_Bin_Values[11][38][2] = 7351;
z_pT_Bin_Borders[11][39][0] = 0.4; z_pT_Bin_Borders[11][39][1] = 0.53; z_pT_Bin_Borders[11][39][2] = 0.05; z_pT_Bin_Borders[11][39][3] = 0;
Phi_h_Bin_Values[11][39][0] =  1; Phi_h_Bin_Values[11][39][1] = 521; Phi_h_Bin_Values[11][39][2] = 7352;
z_pT_Bin_Borders[11][40][0] = 0.4; z_pT_Bin_Borders[11][40][1] = 0.53; z_pT_Bin_Borders[11][40][2] = 10; z_pT_Bin_Borders[11][40][3] = 0.69;
Phi_h_Bin_Values[11][40][0] =  1; Phi_h_Bin_Values[11][40][1] = 522; Phi_h_Bin_Values[11][40][2] = 7353;
z_pT_Bin_Borders[11][41][0] = 0.53; z_pT_Bin_Borders[11][41][1] = 0.69; z_pT_Bin_Borders[11][41][2] = 0.05; z_pT_Bin_Borders[11][41][3] = 0;
Phi_h_Bin_Values[11][41][0] =  1; Phi_h_Bin_Values[11][41][1] = 523; Phi_h_Bin_Values[11][41][2] = 7354;
z_pT_Bin_Borders[11][42][0] = 0.53; z_pT_Bin_Borders[11][42][1] = 0.69; z_pT_Bin_Borders[11][42][2] = 10; z_pT_Bin_Borders[11][42][3] = 0.69;
Phi_h_Bin_Values[11][42][0] =  1; Phi_h_Bin_Values[11][42][1] = 524; Phi_h_Bin_Values[11][42][2] = 7355;
z_pT_Bin_Borders[11][43][0] = 10; z_pT_Bin_Borders[11][43][1] = 0.69; z_pT_Bin_Borders[11][43][2] = 0; z_pT_Bin_Borders[11][43][3] = 0.05;
Phi_h_Bin_Values[11][43][0] =  1; Phi_h_Bin_Values[11][43][1] = 525; Phi_h_Bin_Values[11][43][2] = 7356;
z_pT_Bin_Borders[11][44][0] = 10; z_pT_Bin_Borders[11][44][1] = 0.69; z_pT_Bin_Borders[11][44][2] = 0.05; z_pT_Bin_Borders[11][44][3] = 0.2;
Phi_h_Bin_Values[11][44][0] =  1; Phi_h_Bin_Values[11][44][1] = 526; Phi_h_Bin_Values[11][44][2] = 7357;
z_pT_Bin_Borders[11][45][0] = 10; z_pT_Bin_Borders[11][45][1] = 0.69; z_pT_Bin_Borders[11][45][2] = 0.2; z_pT_Bin_Borders[11][45][3] = 0.3;
Phi_h_Bin_Values[11][45][0] =  1; Phi_h_Bin_Values[11][45][1] = 527; Phi_h_Bin_Values[11][45][2] = 7358;
z_pT_Bin_Borders[11][46][0] = 10; z_pT_Bin_Borders[11][46][1] = 0.69; z_pT_Bin_Borders[11][46][2] = 0.3; z_pT_Bin_Borders[11][46][3] = 0.4;
Phi_h_Bin_Values[11][46][0] =  1; Phi_h_Bin_Values[11][46][1] = 528; Phi_h_Bin_Values[11][46][2] = 7359;
z_pT_Bin_Borders[11][47][0] = 10; z_pT_Bin_Borders[11][47][1] = 0.69; z_pT_Bin_Borders[11][47][2] = 0.4; z_pT_Bin_Borders[11][47][3] = 0.54;
Phi_h_Bin_Values[11][47][0] =  1; Phi_h_Bin_Values[11][47][1] = 529; Phi_h_Bin_Values[11][47][2] = 7360;
z_pT_Bin_Borders[11][48][0] = 10; z_pT_Bin_Borders[11][48][1] = 0.69; z_pT_Bin_Borders[11][48][2] = 0.54; z_pT_Bin_Borders[11][48][3] = 0.69;
Phi_h_Bin_Values[11][48][0] =  1; Phi_h_Bin_Values[11][48][1] = 530; Phi_h_Bin_Values[11][48][2] = 7361;
z_pT_Bin_Borders[11][49][0] = 10; z_pT_Bin_Borders[11][49][1] = 0.69; z_pT_Bin_Borders[11][49][2] = 10; z_pT_Bin_Borders[11][49][3] = 0.69;
Phi_h_Bin_Values[11][49][0] =  1; Phi_h_Bin_Values[11][49][1] = 531; Phi_h_Bin_Values[11][49][2] = 7362;
z_pT_Bin_Borders[12][1][0] = 0.31; z_pT_Bin_Borders[12][1][1] = 0.27; z_pT_Bin_Borders[12][1][2] = 0.22; z_pT_Bin_Borders[12][1][3] = 0.05;
Phi_h_Bin_Values[12][1][0] =  24; Phi_h_Bin_Values[12][1][1] = 0; Phi_h_Bin_Values[12][1][2] = 7363;
z_pT_Bin_Borders[12][2][0] = 0.31; z_pT_Bin_Borders[12][2][1] = 0.27; z_pT_Bin_Borders[12][2][2] = 0.32; z_pT_Bin_Borders[12][2][3] = 0.22;
Phi_h_Bin_Values[12][2][0] =  24; Phi_h_Bin_Values[12][2][1] = 24; Phi_h_Bin_Values[12][2][2] = 7387;
z_pT_Bin_Borders[12][3][0] = 0.31; z_pT_Bin_Borders[12][3][1] = 0.27; z_pT_Bin_Borders[12][3][2] = 0.41; z_pT_Bin_Borders[12][3][3] = 0.32;
Phi_h_Bin_Values[12][3][0] =  24; Phi_h_Bin_Values[12][3][1] = 48; Phi_h_Bin_Values[12][3][2] = 7411;
z_pT_Bin_Borders[12][4][0] = 0.35; z_pT_Bin_Borders[12][4][1] = 0.31; z_pT_Bin_Borders[12][4][2] = 0.22; z_pT_Bin_Borders[12][4][3] = 0.05;
Phi_h_Bin_Values[12][4][0] =  24; Phi_h_Bin_Values[12][4][1] = 72; Phi_h_Bin_Values[12][4][2] = 7435;
z_pT_Bin_Borders[12][5][0] = 0.35; z_pT_Bin_Borders[12][5][1] = 0.31; z_pT_Bin_Borders[12][5][2] = 0.32; z_pT_Bin_Borders[12][5][3] = 0.22;
Phi_h_Bin_Values[12][5][0] =  24; Phi_h_Bin_Values[12][5][1] = 96; Phi_h_Bin_Values[12][5][2] = 7459;
z_pT_Bin_Borders[12][6][0] = 0.35; z_pT_Bin_Borders[12][6][1] = 0.31; z_pT_Bin_Borders[12][6][2] = 0.41; z_pT_Bin_Borders[12][6][3] = 0.32;
Phi_h_Bin_Values[12][6][0] =  24; Phi_h_Bin_Values[12][6][1] = 120; Phi_h_Bin_Values[12][6][2] = 7483;
z_pT_Bin_Borders[12][7][0] = 0.4; z_pT_Bin_Borders[12][7][1] = 0.35; z_pT_Bin_Borders[12][7][2] = 0.22; z_pT_Bin_Borders[12][7][3] = 0.05;
Phi_h_Bin_Values[12][7][0] =  24; Phi_h_Bin_Values[12][7][1] = 144; Phi_h_Bin_Values[12][7][2] = 7507;
z_pT_Bin_Borders[12][8][0] = 0.4; z_pT_Bin_Borders[12][8][1] = 0.35; z_pT_Bin_Borders[12][8][2] = 0.32; z_pT_Bin_Borders[12][8][3] = 0.22;
Phi_h_Bin_Values[12][8][0] =  24; Phi_h_Bin_Values[12][8][1] = 168; Phi_h_Bin_Values[12][8][2] = 7531;
z_pT_Bin_Borders[12][9][0] = 0.4; z_pT_Bin_Borders[12][9][1] = 0.35; z_pT_Bin_Borders[12][9][2] = 0.41; z_pT_Bin_Borders[12][9][3] = 0.32;
Phi_h_Bin_Values[12][9][0] =  24; Phi_h_Bin_Values[12][9][1] = 192; Phi_h_Bin_Values[12][9][2] = 7555;
z_pT_Bin_Borders[12][10][0] = 0.5; z_pT_Bin_Borders[12][10][1] = 0.4; z_pT_Bin_Borders[12][10][2] = 0.22; z_pT_Bin_Borders[12][10][3] = 0.05;
Phi_h_Bin_Values[12][10][0] =  24; Phi_h_Bin_Values[12][10][1] = 216; Phi_h_Bin_Values[12][10][2] = 7579;
z_pT_Bin_Borders[12][11][0] = 0.5; z_pT_Bin_Borders[12][11][1] = 0.4; z_pT_Bin_Borders[12][11][2] = 0.32; z_pT_Bin_Borders[12][11][3] = 0.22;
Phi_h_Bin_Values[12][11][0] =  1; Phi_h_Bin_Values[12][11][1] = 240; Phi_h_Bin_Values[12][11][2] = 7603;
z_pT_Bin_Borders[12][12][0] = 0.5; z_pT_Bin_Borders[12][12][1] = 0.4; z_pT_Bin_Borders[12][12][2] = 0.41; z_pT_Bin_Borders[12][12][3] = 0.32;
Phi_h_Bin_Values[12][12][0] =  1; Phi_h_Bin_Values[12][12][1] = 241; Phi_h_Bin_Values[12][12][2] = 7604;
z_pT_Bin_Borders[12][13][0] = 0.27; z_pT_Bin_Borders[12][13][1] = 0; z_pT_Bin_Borders[12][13][2] = 0.05; z_pT_Bin_Borders[12][13][3] = 0;
Phi_h_Bin_Values[12][13][0] =  1; Phi_h_Bin_Values[12][13][1] = 242; Phi_h_Bin_Values[12][13][2] = 7605;
z_pT_Bin_Borders[12][14][0] = 0.27; z_pT_Bin_Borders[12][14][1] = 0; z_pT_Bin_Borders[12][14][2] = 0.05; z_pT_Bin_Borders[12][14][3] = 0.22;
Phi_h_Bin_Values[12][14][0] =  1; Phi_h_Bin_Values[12][14][1] = 243; Phi_h_Bin_Values[12][14][2] = 7606;
z_pT_Bin_Borders[12][15][0] = 0.27; z_pT_Bin_Borders[12][15][1] = 0; z_pT_Bin_Borders[12][15][2] = 0.22; z_pT_Bin_Borders[12][15][3] = 0.32;
Phi_h_Bin_Values[12][15][0] =  1; Phi_h_Bin_Values[12][15][1] = 244; Phi_h_Bin_Values[12][15][2] = 7607;
z_pT_Bin_Borders[12][16][0] = 0.27; z_pT_Bin_Borders[12][16][1] = 0; z_pT_Bin_Borders[12][16][2] = 0.32; z_pT_Bin_Borders[12][16][3] = 0.41;
Phi_h_Bin_Values[12][16][0] =  1; Phi_h_Bin_Values[12][16][1] = 245; Phi_h_Bin_Values[12][16][2] = 7608;
z_pT_Bin_Borders[12][17][0] = 0.27; z_pT_Bin_Borders[12][17][1] = 0; z_pT_Bin_Borders[12][17][2] = 10; z_pT_Bin_Borders[12][17][3] = 0.41;
Phi_h_Bin_Values[12][17][0] =  1; Phi_h_Bin_Values[12][17][1] = 246; Phi_h_Bin_Values[12][17][2] = 7609;
z_pT_Bin_Borders[12][18][0] = 0.27; z_pT_Bin_Borders[12][18][1] = 0.31; z_pT_Bin_Borders[12][18][2] = 0.05; z_pT_Bin_Borders[12][18][3] = 0;
Phi_h_Bin_Values[12][18][0] =  1; Phi_h_Bin_Values[12][18][1] = 247; Phi_h_Bin_Values[12][18][2] = 7610;
z_pT_Bin_Borders[12][19][0] = 0.27; z_pT_Bin_Borders[12][19][1] = 0.31; z_pT_Bin_Borders[12][19][2] = 10; z_pT_Bin_Borders[12][19][3] = 0.41;
Phi_h_Bin_Values[12][19][0] =  1; Phi_h_Bin_Values[12][19][1] = 248; Phi_h_Bin_Values[12][19][2] = 7611;
z_pT_Bin_Borders[12][20][0] = 0.31; z_pT_Bin_Borders[12][20][1] = 0.35; z_pT_Bin_Borders[12][20][2] = 0.05; z_pT_Bin_Borders[12][20][3] = 0;
Phi_h_Bin_Values[12][20][0] =  1; Phi_h_Bin_Values[12][20][1] = 249; Phi_h_Bin_Values[12][20][2] = 7612;
z_pT_Bin_Borders[12][21][0] = 0.31; z_pT_Bin_Borders[12][21][1] = 0.35; z_pT_Bin_Borders[12][21][2] = 10; z_pT_Bin_Borders[12][21][3] = 0.41;
Phi_h_Bin_Values[12][21][0] =  1; Phi_h_Bin_Values[12][21][1] = 250; Phi_h_Bin_Values[12][21][2] = 7613;
z_pT_Bin_Borders[12][22][0] = 0.35; z_pT_Bin_Borders[12][22][1] = 0.4; z_pT_Bin_Borders[12][22][2] = 0.05; z_pT_Bin_Borders[12][22][3] = 0;
Phi_h_Bin_Values[12][22][0] =  1; Phi_h_Bin_Values[12][22][1] = 251; Phi_h_Bin_Values[12][22][2] = 7614;
z_pT_Bin_Borders[12][23][0] = 0.35; z_pT_Bin_Borders[12][23][1] = 0.4; z_pT_Bin_Borders[12][23][2] = 10; z_pT_Bin_Borders[12][23][3] = 0.41;
Phi_h_Bin_Values[12][23][0] =  1; Phi_h_Bin_Values[12][23][1] = 252; Phi_h_Bin_Values[12][23][2] = 7615;
z_pT_Bin_Borders[12][24][0] = 0.4; z_pT_Bin_Borders[12][24][1] = 0.5; z_pT_Bin_Borders[12][24][2] = 0.05; z_pT_Bin_Borders[12][24][3] = 0;
Phi_h_Bin_Values[12][24][0] =  1; Phi_h_Bin_Values[12][24][1] = 253; Phi_h_Bin_Values[12][24][2] = 7616;
z_pT_Bin_Borders[12][25][0] = 0.4; z_pT_Bin_Borders[12][25][1] = 0.5; z_pT_Bin_Borders[12][25][2] = 10; z_pT_Bin_Borders[12][25][3] = 0.41;
Phi_h_Bin_Values[12][25][0] =  1; Phi_h_Bin_Values[12][25][1] = 254; Phi_h_Bin_Values[12][25][2] = 7617;
z_pT_Bin_Borders[12][26][0] = 10; z_pT_Bin_Borders[12][26][1] = 0.5; z_pT_Bin_Borders[12][26][2] = 0; z_pT_Bin_Borders[12][26][3] = 0.05;
Phi_h_Bin_Values[12][26][0] =  1; Phi_h_Bin_Values[12][26][1] = 255; Phi_h_Bin_Values[12][26][2] = 7618;
z_pT_Bin_Borders[12][27][0] = 10; z_pT_Bin_Borders[12][27][1] = 0.5; z_pT_Bin_Borders[12][27][2] = 0.05; z_pT_Bin_Borders[12][27][3] = 0.22;
Phi_h_Bin_Values[12][27][0] =  1; Phi_h_Bin_Values[12][27][1] = 256; Phi_h_Bin_Values[12][27][2] = 7619;
z_pT_Bin_Borders[12][28][0] = 10; z_pT_Bin_Borders[12][28][1] = 0.5; z_pT_Bin_Borders[12][28][2] = 0.22; z_pT_Bin_Borders[12][28][3] = 0.32;
Phi_h_Bin_Values[12][28][0] =  1; Phi_h_Bin_Values[12][28][1] = 257; Phi_h_Bin_Values[12][28][2] = 7620;
z_pT_Bin_Borders[12][29][0] = 10; z_pT_Bin_Borders[12][29][1] = 0.5; z_pT_Bin_Borders[12][29][2] = 0.32; z_pT_Bin_Borders[12][29][3] = 0.41;
Phi_h_Bin_Values[12][29][0] =  1; Phi_h_Bin_Values[12][29][1] = 258; Phi_h_Bin_Values[12][29][2] = 7621;
z_pT_Bin_Borders[12][30][0] = 10; z_pT_Bin_Borders[12][30][1] = 0.5; z_pT_Bin_Borders[12][30][2] = 10; z_pT_Bin_Borders[12][30][3] = 0.41;
Phi_h_Bin_Values[12][30][0] =  1; Phi_h_Bin_Values[12][30][1] = 259; Phi_h_Bin_Values[12][30][2] = 7622;
z_pT_Bin_Borders[13][1][0] = 0.2; z_pT_Bin_Borders[13][1][1] = 0.16; z_pT_Bin_Borders[13][1][2] = 0.22; z_pT_Bin_Borders[13][1][3] = 0.05;
Phi_h_Bin_Values[13][1][0] =  24; Phi_h_Bin_Values[13][1][1] = 0; Phi_h_Bin_Values[13][1][2] = 7623;
z_pT_Bin_Borders[13][2][0] = 0.2; z_pT_Bin_Borders[13][2][1] = 0.16; z_pT_Bin_Borders[13][2][2] = 0.35; z_pT_Bin_Borders[13][2][3] = 0.22;
Phi_h_Bin_Values[13][2][0] =  24; Phi_h_Bin_Values[13][2][1] = 24; Phi_h_Bin_Values[13][2][2] = 7647;
z_pT_Bin_Borders[13][3][0] = 0.2; z_pT_Bin_Borders[13][3][1] = 0.16; z_pT_Bin_Borders[13][3][2] = 0.45; z_pT_Bin_Borders[13][3][3] = 0.35;
Phi_h_Bin_Values[13][3][0] =  24; Phi_h_Bin_Values[13][3][1] = 48; Phi_h_Bin_Values[13][3][2] = 7671;
z_pT_Bin_Borders[13][4][0] = 0.2; z_pT_Bin_Borders[13][4][1] = 0.16; z_pT_Bin_Borders[13][4][2] = 0.6; z_pT_Bin_Borders[13][4][3] = 0.45;
Phi_h_Bin_Values[13][4][0] =  1; Phi_h_Bin_Values[13][4][1] = 72; Phi_h_Bin_Values[13][4][2] = 7695;
z_pT_Bin_Borders[13][5][0] = 0.2; z_pT_Bin_Borders[13][5][1] = 0.16; z_pT_Bin_Borders[13][5][2] = 0.9; z_pT_Bin_Borders[13][5][3] = 0.6;
Phi_h_Bin_Values[13][5][0] =  1; Phi_h_Bin_Values[13][5][1] = 73; Phi_h_Bin_Values[13][5][2] = 7696;
z_pT_Bin_Borders[13][6][0] = 0.24; z_pT_Bin_Borders[13][6][1] = 0.2; z_pT_Bin_Borders[13][6][2] = 0.22; z_pT_Bin_Borders[13][6][3] = 0.05;
Phi_h_Bin_Values[13][6][0] =  24; Phi_h_Bin_Values[13][6][1] = 74; Phi_h_Bin_Values[13][6][2] = 7697;
z_pT_Bin_Borders[13][7][0] = 0.24; z_pT_Bin_Borders[13][7][1] = 0.2; z_pT_Bin_Borders[13][7][2] = 0.35; z_pT_Bin_Borders[13][7][3] = 0.22;
Phi_h_Bin_Values[13][7][0] =  24; Phi_h_Bin_Values[13][7][1] = 98; Phi_h_Bin_Values[13][7][2] = 7721;
z_pT_Bin_Borders[13][8][0] = 0.24; z_pT_Bin_Borders[13][8][1] = 0.2; z_pT_Bin_Borders[13][8][2] = 0.45; z_pT_Bin_Borders[13][8][3] = 0.35;
Phi_h_Bin_Values[13][8][0] =  24; Phi_h_Bin_Values[13][8][1] = 122; Phi_h_Bin_Values[13][8][2] = 7745;
z_pT_Bin_Borders[13][9][0] = 0.24; z_pT_Bin_Borders[13][9][1] = 0.2; z_pT_Bin_Borders[13][9][2] = 0.6; z_pT_Bin_Borders[13][9][3] = 0.45;
Phi_h_Bin_Values[13][9][0] =  24; Phi_h_Bin_Values[13][9][1] = 146; Phi_h_Bin_Values[13][9][2] = 7769;
z_pT_Bin_Borders[13][10][0] = 0.24; z_pT_Bin_Borders[13][10][1] = 0.2; z_pT_Bin_Borders[13][10][2] = 0.9; z_pT_Bin_Borders[13][10][3] = 0.6;
Phi_h_Bin_Values[13][10][0] =  1; Phi_h_Bin_Values[13][10][1] = 170; Phi_h_Bin_Values[13][10][2] = 7793;
z_pT_Bin_Borders[13][11][0] = 0.29; z_pT_Bin_Borders[13][11][1] = 0.24; z_pT_Bin_Borders[13][11][2] = 0.22; z_pT_Bin_Borders[13][11][3] = 0.05;
Phi_h_Bin_Values[13][11][0] =  24; Phi_h_Bin_Values[13][11][1] = 171; Phi_h_Bin_Values[13][11][2] = 7794;
z_pT_Bin_Borders[13][12][0] = 0.29; z_pT_Bin_Borders[13][12][1] = 0.24; z_pT_Bin_Borders[13][12][2] = 0.35; z_pT_Bin_Borders[13][12][3] = 0.22;
Phi_h_Bin_Values[13][12][0] =  24; Phi_h_Bin_Values[13][12][1] = 195; Phi_h_Bin_Values[13][12][2] = 7818;
z_pT_Bin_Borders[13][13][0] = 0.29; z_pT_Bin_Borders[13][13][1] = 0.24; z_pT_Bin_Borders[13][13][2] = 0.45; z_pT_Bin_Borders[13][13][3] = 0.35;
Phi_h_Bin_Values[13][13][0] =  24; Phi_h_Bin_Values[13][13][1] = 219; Phi_h_Bin_Values[13][13][2] = 7842;
z_pT_Bin_Borders[13][14][0] = 0.29; z_pT_Bin_Borders[13][14][1] = 0.24; z_pT_Bin_Borders[13][14][2] = 0.6; z_pT_Bin_Borders[13][14][3] = 0.45;
Phi_h_Bin_Values[13][14][0] =  24; Phi_h_Bin_Values[13][14][1] = 243; Phi_h_Bin_Values[13][14][2] = 7866;
z_pT_Bin_Borders[13][15][0] = 0.29; z_pT_Bin_Borders[13][15][1] = 0.24; z_pT_Bin_Borders[13][15][2] = 0.9; z_pT_Bin_Borders[13][15][3] = 0.6;
Phi_h_Bin_Values[13][15][0] =  1; Phi_h_Bin_Values[13][15][1] = 267; Phi_h_Bin_Values[13][15][2] = 7890;
z_pT_Bin_Borders[13][16][0] = 0.36; z_pT_Bin_Borders[13][16][1] = 0.29; z_pT_Bin_Borders[13][16][2] = 0.22; z_pT_Bin_Borders[13][16][3] = 0.05;
Phi_h_Bin_Values[13][16][0] =  24; Phi_h_Bin_Values[13][16][1] = 268; Phi_h_Bin_Values[13][16][2] = 7891;
z_pT_Bin_Borders[13][17][0] = 0.36; z_pT_Bin_Borders[13][17][1] = 0.29; z_pT_Bin_Borders[13][17][2] = 0.35; z_pT_Bin_Borders[13][17][3] = 0.22;
Phi_h_Bin_Values[13][17][0] =  24; Phi_h_Bin_Values[13][17][1] = 292; Phi_h_Bin_Values[13][17][2] = 7915;
z_pT_Bin_Borders[13][18][0] = 0.36; z_pT_Bin_Borders[13][18][1] = 0.29; z_pT_Bin_Borders[13][18][2] = 0.45; z_pT_Bin_Borders[13][18][3] = 0.35;
Phi_h_Bin_Values[13][18][0] =  24; Phi_h_Bin_Values[13][18][1] = 316; Phi_h_Bin_Values[13][18][2] = 7939;
z_pT_Bin_Borders[13][19][0] = 0.36; z_pT_Bin_Borders[13][19][1] = 0.29; z_pT_Bin_Borders[13][19][2] = 0.6; z_pT_Bin_Borders[13][19][3] = 0.45;
Phi_h_Bin_Values[13][19][0] =  24; Phi_h_Bin_Values[13][19][1] = 340; Phi_h_Bin_Values[13][19][2] = 7963;
z_pT_Bin_Borders[13][20][0] = 0.36; z_pT_Bin_Borders[13][20][1] = 0.29; z_pT_Bin_Borders[13][20][2] = 0.9; z_pT_Bin_Borders[13][20][3] = 0.6;
Phi_h_Bin_Values[13][20][0] =  24; Phi_h_Bin_Values[13][20][1] = 364; Phi_h_Bin_Values[13][20][2] = 7987;
z_pT_Bin_Borders[13][21][0] = 0.51; z_pT_Bin_Borders[13][21][1] = 0.36; z_pT_Bin_Borders[13][21][2] = 0.22; z_pT_Bin_Borders[13][21][3] = 0.05;
Phi_h_Bin_Values[13][21][0] =  24; Phi_h_Bin_Values[13][21][1] = 388; Phi_h_Bin_Values[13][21][2] = 8011;
z_pT_Bin_Borders[13][22][0] = 0.51; z_pT_Bin_Borders[13][22][1] = 0.36; z_pT_Bin_Borders[13][22][2] = 0.35; z_pT_Bin_Borders[13][22][3] = 0.22;
Phi_h_Bin_Values[13][22][0] =  24; Phi_h_Bin_Values[13][22][1] = 412; Phi_h_Bin_Values[13][22][2] = 8035;
z_pT_Bin_Borders[13][23][0] = 0.51; z_pT_Bin_Borders[13][23][1] = 0.36; z_pT_Bin_Borders[13][23][2] = 0.45; z_pT_Bin_Borders[13][23][3] = 0.35;
Phi_h_Bin_Values[13][23][0] =  24; Phi_h_Bin_Values[13][23][1] = 436; Phi_h_Bin_Values[13][23][2] = 8059;
z_pT_Bin_Borders[13][24][0] = 0.51; z_pT_Bin_Borders[13][24][1] = 0.36; z_pT_Bin_Borders[13][24][2] = 0.6; z_pT_Bin_Borders[13][24][3] = 0.45;
Phi_h_Bin_Values[13][24][0] =  24; Phi_h_Bin_Values[13][24][1] = 460; Phi_h_Bin_Values[13][24][2] = 8083;
z_pT_Bin_Borders[13][25][0] = 0.51; z_pT_Bin_Borders[13][25][1] = 0.36; z_pT_Bin_Borders[13][25][2] = 0.9; z_pT_Bin_Borders[13][25][3] = 0.6;
Phi_h_Bin_Values[13][25][0] =  24; Phi_h_Bin_Values[13][25][1] = 484; Phi_h_Bin_Values[13][25][2] = 8107;
z_pT_Bin_Borders[13][26][0] = 0.72; z_pT_Bin_Borders[13][26][1] = 0.51; z_pT_Bin_Borders[13][26][2] = 0.22; z_pT_Bin_Borders[13][26][3] = 0.05;
Phi_h_Bin_Values[13][26][0] =  24; Phi_h_Bin_Values[13][26][1] = 508; Phi_h_Bin_Values[13][26][2] = 8131;
z_pT_Bin_Borders[13][27][0] = 0.72; z_pT_Bin_Borders[13][27][1] = 0.51; z_pT_Bin_Borders[13][27][2] = 0.35; z_pT_Bin_Borders[13][27][3] = 0.22;
Phi_h_Bin_Values[13][27][0] =  24; Phi_h_Bin_Values[13][27][1] = 532; Phi_h_Bin_Values[13][27][2] = 8155;
z_pT_Bin_Borders[13][28][0] = 0.72; z_pT_Bin_Borders[13][28][1] = 0.51; z_pT_Bin_Borders[13][28][2] = 0.45; z_pT_Bin_Borders[13][28][3] = 0.35;
Phi_h_Bin_Values[13][28][0] =  24; Phi_h_Bin_Values[13][28][1] = 556; Phi_h_Bin_Values[13][28][2] = 8179;
z_pT_Bin_Borders[13][29][0] = 0.72; z_pT_Bin_Borders[13][29][1] = 0.51; z_pT_Bin_Borders[13][29][2] = 0.6; z_pT_Bin_Borders[13][29][3] = 0.45;
Phi_h_Bin_Values[13][29][0] =  24; Phi_h_Bin_Values[13][29][1] = 580; Phi_h_Bin_Values[13][29][2] = 8203;
z_pT_Bin_Borders[13][30][0] = 0.72; z_pT_Bin_Borders[13][30][1] = 0.51; z_pT_Bin_Borders[13][30][2] = 0.9; z_pT_Bin_Borders[13][30][3] = 0.6;
Phi_h_Bin_Values[13][30][0] =  1; Phi_h_Bin_Values[13][30][1] = 604; Phi_h_Bin_Values[13][30][2] = 8227;
z_pT_Bin_Borders[13][31][0] = 0.16; z_pT_Bin_Borders[13][31][1] = 0; z_pT_Bin_Borders[13][31][2] = 0.05; z_pT_Bin_Borders[13][31][3] = 0;
Phi_h_Bin_Values[13][31][0] =  1; Phi_h_Bin_Values[13][31][1] = 605; Phi_h_Bin_Values[13][31][2] = 8228;
z_pT_Bin_Borders[13][32][0] = 0.16; z_pT_Bin_Borders[13][32][1] = 0; z_pT_Bin_Borders[13][32][2] = 0.05; z_pT_Bin_Borders[13][32][3] = 0.22;
Phi_h_Bin_Values[13][32][0] =  1; Phi_h_Bin_Values[13][32][1] = 606; Phi_h_Bin_Values[13][32][2] = 8229;
z_pT_Bin_Borders[13][33][0] = 0.16; z_pT_Bin_Borders[13][33][1] = 0; z_pT_Bin_Borders[13][33][2] = 0.22; z_pT_Bin_Borders[13][33][3] = 0.35;
Phi_h_Bin_Values[13][33][0] =  1; Phi_h_Bin_Values[13][33][1] = 607; Phi_h_Bin_Values[13][33][2] = 8230;
z_pT_Bin_Borders[13][34][0] = 0.16; z_pT_Bin_Borders[13][34][1] = 0; z_pT_Bin_Borders[13][34][2] = 0.35; z_pT_Bin_Borders[13][34][3] = 0.45;
Phi_h_Bin_Values[13][34][0] =  1; Phi_h_Bin_Values[13][34][1] = 608; Phi_h_Bin_Values[13][34][2] = 8231;
z_pT_Bin_Borders[13][35][0] = 0.16; z_pT_Bin_Borders[13][35][1] = 0; z_pT_Bin_Borders[13][35][2] = 0.45; z_pT_Bin_Borders[13][35][3] = 0.6;
Phi_h_Bin_Values[13][35][0] =  1; Phi_h_Bin_Values[13][35][1] = 609; Phi_h_Bin_Values[13][35][2] = 8232;
z_pT_Bin_Borders[13][36][0] = 0.16; z_pT_Bin_Borders[13][36][1] = 0; z_pT_Bin_Borders[13][36][2] = 0.6; z_pT_Bin_Borders[13][36][3] = 0.9;
Phi_h_Bin_Values[13][36][0] =  1; Phi_h_Bin_Values[13][36][1] = 610; Phi_h_Bin_Values[13][36][2] = 8233;
z_pT_Bin_Borders[13][37][0] = 0.16; z_pT_Bin_Borders[13][37][1] = 0; z_pT_Bin_Borders[13][37][2] = 10; z_pT_Bin_Borders[13][37][3] = 0.9;
Phi_h_Bin_Values[13][37][0] =  1; Phi_h_Bin_Values[13][37][1] = 611; Phi_h_Bin_Values[13][37][2] = 8234;
z_pT_Bin_Borders[13][38][0] = 0.16; z_pT_Bin_Borders[13][38][1] = 0.2; z_pT_Bin_Borders[13][38][2] = 0.05; z_pT_Bin_Borders[13][38][3] = 0;
Phi_h_Bin_Values[13][38][0] =  1; Phi_h_Bin_Values[13][38][1] = 612; Phi_h_Bin_Values[13][38][2] = 8235;
z_pT_Bin_Borders[13][39][0] = 0.16; z_pT_Bin_Borders[13][39][1] = 0.2; z_pT_Bin_Borders[13][39][2] = 10; z_pT_Bin_Borders[13][39][3] = 0.9;
Phi_h_Bin_Values[13][39][0] =  1; Phi_h_Bin_Values[13][39][1] = 613; Phi_h_Bin_Values[13][39][2] = 8236;
z_pT_Bin_Borders[13][40][0] = 0.2; z_pT_Bin_Borders[13][40][1] = 0.24; z_pT_Bin_Borders[13][40][2] = 0.05; z_pT_Bin_Borders[13][40][3] = 0;
Phi_h_Bin_Values[13][40][0] =  1; Phi_h_Bin_Values[13][40][1] = 614; Phi_h_Bin_Values[13][40][2] = 8237;
z_pT_Bin_Borders[13][41][0] = 0.2; z_pT_Bin_Borders[13][41][1] = 0.24; z_pT_Bin_Borders[13][41][2] = 10; z_pT_Bin_Borders[13][41][3] = 0.9;
Phi_h_Bin_Values[13][41][0] =  1; Phi_h_Bin_Values[13][41][1] = 615; Phi_h_Bin_Values[13][41][2] = 8238;
z_pT_Bin_Borders[13][42][0] = 0.24; z_pT_Bin_Borders[13][42][1] = 0.29; z_pT_Bin_Borders[13][42][2] = 0.05; z_pT_Bin_Borders[13][42][3] = 0;
Phi_h_Bin_Values[13][42][0] =  1; Phi_h_Bin_Values[13][42][1] = 616; Phi_h_Bin_Values[13][42][2] = 8239;
z_pT_Bin_Borders[13][43][0] = 0.24; z_pT_Bin_Borders[13][43][1] = 0.29; z_pT_Bin_Borders[13][43][2] = 10; z_pT_Bin_Borders[13][43][3] = 0.9;
Phi_h_Bin_Values[13][43][0] =  1; Phi_h_Bin_Values[13][43][1] = 617; Phi_h_Bin_Values[13][43][2] = 8240;
z_pT_Bin_Borders[13][44][0] = 0.29; z_pT_Bin_Borders[13][44][1] = 0.36; z_pT_Bin_Borders[13][44][2] = 0.05; z_pT_Bin_Borders[13][44][3] = 0;
Phi_h_Bin_Values[13][44][0] =  1; Phi_h_Bin_Values[13][44][1] = 618; Phi_h_Bin_Values[13][44][2] = 8241;
z_pT_Bin_Borders[13][45][0] = 0.29; z_pT_Bin_Borders[13][45][1] = 0.36; z_pT_Bin_Borders[13][45][2] = 10; z_pT_Bin_Borders[13][45][3] = 0.9;
Phi_h_Bin_Values[13][45][0] =  1; Phi_h_Bin_Values[13][45][1] = 619; Phi_h_Bin_Values[13][45][2] = 8242;
z_pT_Bin_Borders[13][46][0] = 0.36; z_pT_Bin_Borders[13][46][1] = 0.51; z_pT_Bin_Borders[13][46][2] = 0.05; z_pT_Bin_Borders[13][46][3] = 0;
Phi_h_Bin_Values[13][46][0] =  1; Phi_h_Bin_Values[13][46][1] = 620; Phi_h_Bin_Values[13][46][2] = 8243;
z_pT_Bin_Borders[13][47][0] = 0.36; z_pT_Bin_Borders[13][47][1] = 0.51; z_pT_Bin_Borders[13][47][2] = 10; z_pT_Bin_Borders[13][47][3] = 0.9;
Phi_h_Bin_Values[13][47][0] =  1; Phi_h_Bin_Values[13][47][1] = 621; Phi_h_Bin_Values[13][47][2] = 8244;
z_pT_Bin_Borders[13][48][0] = 0.51; z_pT_Bin_Borders[13][48][1] = 0.72; z_pT_Bin_Borders[13][48][2] = 0.05; z_pT_Bin_Borders[13][48][3] = 0;
Phi_h_Bin_Values[13][48][0] =  1; Phi_h_Bin_Values[13][48][1] = 622; Phi_h_Bin_Values[13][48][2] = 8245;
z_pT_Bin_Borders[13][49][0] = 0.51; z_pT_Bin_Borders[13][49][1] = 0.72; z_pT_Bin_Borders[13][49][2] = 10; z_pT_Bin_Borders[13][49][3] = 0.9;
Phi_h_Bin_Values[13][49][0] =  1; Phi_h_Bin_Values[13][49][1] = 623; Phi_h_Bin_Values[13][49][2] = 8246;
z_pT_Bin_Borders[13][50][0] = 10; z_pT_Bin_Borders[13][50][1] = 0.72; z_pT_Bin_Borders[13][50][2] = 0; z_pT_Bin_Borders[13][50][3] = 0.05;
Phi_h_Bin_Values[13][50][0] =  1; Phi_h_Bin_Values[13][50][1] = 624; Phi_h_Bin_Values[13][50][2] = 8247;
z_pT_Bin_Borders[13][51][0] = 10; z_pT_Bin_Borders[13][51][1] = 0.72; z_pT_Bin_Borders[13][51][2] = 0.05; z_pT_Bin_Borders[13][51][3] = 0.22;
Phi_h_Bin_Values[13][51][0] =  1; Phi_h_Bin_Values[13][51][1] = 625; Phi_h_Bin_Values[13][51][2] = 8248;
z_pT_Bin_Borders[13][52][0] = 10; z_pT_Bin_Borders[13][52][1] = 0.72; z_pT_Bin_Borders[13][52][2] = 0.22; z_pT_Bin_Borders[13][52][3] = 0.35;
Phi_h_Bin_Values[13][52][0] =  1; Phi_h_Bin_Values[13][52][1] = 626; Phi_h_Bin_Values[13][52][2] = 8249;
z_pT_Bin_Borders[13][53][0] = 10; z_pT_Bin_Borders[13][53][1] = 0.72; z_pT_Bin_Borders[13][53][2] = 0.35; z_pT_Bin_Borders[13][53][3] = 0.45;
Phi_h_Bin_Values[13][53][0] =  1; Phi_h_Bin_Values[13][53][1] = 627; Phi_h_Bin_Values[13][53][2] = 8250;
z_pT_Bin_Borders[13][54][0] = 10; z_pT_Bin_Borders[13][54][1] = 0.72; z_pT_Bin_Borders[13][54][2] = 0.45; z_pT_Bin_Borders[13][54][3] = 0.6;
Phi_h_Bin_Values[13][54][0] =  1; Phi_h_Bin_Values[13][54][1] = 628; Phi_h_Bin_Values[13][54][2] = 8251;
z_pT_Bin_Borders[13][55][0] = 10; z_pT_Bin_Borders[13][55][1] = 0.72; z_pT_Bin_Borders[13][55][2] = 0.6; z_pT_Bin_Borders[13][55][3] = 0.9;
Phi_h_Bin_Values[13][55][0] =  1; Phi_h_Bin_Values[13][55][1] = 629; Phi_h_Bin_Values[13][55][2] = 8252;
z_pT_Bin_Borders[13][56][0] = 10; z_pT_Bin_Borders[13][56][1] = 0.72; z_pT_Bin_Borders[13][56][2] = 10; z_pT_Bin_Borders[13][56][3] = 0.9;
Phi_h_Bin_Values[13][56][0] =  1; Phi_h_Bin_Values[13][56][1] = 630; Phi_h_Bin_Values[13][56][2] = 8253;
z_pT_Bin_Borders[14][1][0] = 0.23; z_pT_Bin_Borders[14][1][1] = 0.19; z_pT_Bin_Borders[14][1][2] = 0.2; z_pT_Bin_Borders[14][1][3] = 0.05;
Phi_h_Bin_Values[14][1][0] =  24; Phi_h_Bin_Values[14][1][1] = 0; Phi_h_Bin_Values[14][1][2] = 8254;
z_pT_Bin_Borders[14][2][0] = 0.23; z_pT_Bin_Borders[14][2][1] = 0.19; z_pT_Bin_Borders[14][2][2] = 0.3; z_pT_Bin_Borders[14][2][3] = 0.2;
Phi_h_Bin_Values[14][2][0] =  24; Phi_h_Bin_Values[14][2][1] = 24; Phi_h_Bin_Values[14][2][2] = 8278;
z_pT_Bin_Borders[14][3][0] = 0.23; z_pT_Bin_Borders[14][3][1] = 0.19; z_pT_Bin_Borders[14][3][2] = 0.4; z_pT_Bin_Borders[14][3][3] = 0.3;
Phi_h_Bin_Values[14][3][0] =  24; Phi_h_Bin_Values[14][3][1] = 48; Phi_h_Bin_Values[14][3][2] = 8302;
z_pT_Bin_Borders[14][4][0] = 0.23; z_pT_Bin_Borders[14][4][1] = 0.19; z_pT_Bin_Borders[14][4][2] = 0.5; z_pT_Bin_Borders[14][4][3] = 0.4;
Phi_h_Bin_Values[14][4][0] =  24; Phi_h_Bin_Values[14][4][1] = 72; Phi_h_Bin_Values[14][4][2] = 8326;
z_pT_Bin_Borders[14][5][0] = 0.23; z_pT_Bin_Borders[14][5][1] = 0.19; z_pT_Bin_Borders[14][5][2] = 0.65; z_pT_Bin_Borders[14][5][3] = 0.5;
Phi_h_Bin_Values[14][5][0] =  1; Phi_h_Bin_Values[14][5][1] = 96; Phi_h_Bin_Values[14][5][2] = 8350;
z_pT_Bin_Borders[14][6][0] = 0.23; z_pT_Bin_Borders[14][6][1] = 0.19; z_pT_Bin_Borders[14][6][2] = 0.8; z_pT_Bin_Borders[14][6][3] = 0.65;
Phi_h_Bin_Values[14][6][0] =  1; Phi_h_Bin_Values[14][6][1] = 97; Phi_h_Bin_Values[14][6][2] = 8351;
z_pT_Bin_Borders[14][7][0] = 0.27; z_pT_Bin_Borders[14][7][1] = 0.23; z_pT_Bin_Borders[14][7][2] = 0.2; z_pT_Bin_Borders[14][7][3] = 0.05;
Phi_h_Bin_Values[14][7][0] =  24; Phi_h_Bin_Values[14][7][1] = 98; Phi_h_Bin_Values[14][7][2] = 8352;
z_pT_Bin_Borders[14][8][0] = 0.27; z_pT_Bin_Borders[14][8][1] = 0.23; z_pT_Bin_Borders[14][8][2] = 0.3; z_pT_Bin_Borders[14][8][3] = 0.2;
Phi_h_Bin_Values[14][8][0] =  24; Phi_h_Bin_Values[14][8][1] = 122; Phi_h_Bin_Values[14][8][2] = 8376;
z_pT_Bin_Borders[14][9][0] = 0.27; z_pT_Bin_Borders[14][9][1] = 0.23; z_pT_Bin_Borders[14][9][2] = 0.4; z_pT_Bin_Borders[14][9][3] = 0.3;
Phi_h_Bin_Values[14][9][0] =  24; Phi_h_Bin_Values[14][9][1] = 146; Phi_h_Bin_Values[14][9][2] = 8400;
z_pT_Bin_Borders[14][10][0] = 0.27; z_pT_Bin_Borders[14][10][1] = 0.23; z_pT_Bin_Borders[14][10][2] = 0.5; z_pT_Bin_Borders[14][10][3] = 0.4;
Phi_h_Bin_Values[14][10][0] =  24; Phi_h_Bin_Values[14][10][1] = 170; Phi_h_Bin_Values[14][10][2] = 8424;
z_pT_Bin_Borders[14][11][0] = 0.27; z_pT_Bin_Borders[14][11][1] = 0.23; z_pT_Bin_Borders[14][11][2] = 0.65; z_pT_Bin_Borders[14][11][3] = 0.5;
Phi_h_Bin_Values[14][11][0] =  24; Phi_h_Bin_Values[14][11][1] = 194; Phi_h_Bin_Values[14][11][2] = 8448;
z_pT_Bin_Borders[14][12][0] = 0.27; z_pT_Bin_Borders[14][12][1] = 0.23; z_pT_Bin_Borders[14][12][2] = 0.8; z_pT_Bin_Borders[14][12][3] = 0.65;
Phi_h_Bin_Values[14][12][0] =  1; Phi_h_Bin_Values[14][12][1] = 218; Phi_h_Bin_Values[14][12][2] = 8472;
z_pT_Bin_Borders[14][13][0] = 0.32; z_pT_Bin_Borders[14][13][1] = 0.27; z_pT_Bin_Borders[14][13][2] = 0.2; z_pT_Bin_Borders[14][13][3] = 0.05;
Phi_h_Bin_Values[14][13][0] =  24; Phi_h_Bin_Values[14][13][1] = 219; Phi_h_Bin_Values[14][13][2] = 8473;
z_pT_Bin_Borders[14][14][0] = 0.32; z_pT_Bin_Borders[14][14][1] = 0.27; z_pT_Bin_Borders[14][14][2] = 0.3; z_pT_Bin_Borders[14][14][3] = 0.2;
Phi_h_Bin_Values[14][14][0] =  24; Phi_h_Bin_Values[14][14][1] = 243; Phi_h_Bin_Values[14][14][2] = 8497;
z_pT_Bin_Borders[14][15][0] = 0.32; z_pT_Bin_Borders[14][15][1] = 0.27; z_pT_Bin_Borders[14][15][2] = 0.4; z_pT_Bin_Borders[14][15][3] = 0.3;
Phi_h_Bin_Values[14][15][0] =  24; Phi_h_Bin_Values[14][15][1] = 267; Phi_h_Bin_Values[14][15][2] = 8521;
z_pT_Bin_Borders[14][16][0] = 0.32; z_pT_Bin_Borders[14][16][1] = 0.27; z_pT_Bin_Borders[14][16][2] = 0.5; z_pT_Bin_Borders[14][16][3] = 0.4;
Phi_h_Bin_Values[14][16][0] =  24; Phi_h_Bin_Values[14][16][1] = 291; Phi_h_Bin_Values[14][16][2] = 8545;
z_pT_Bin_Borders[14][17][0] = 0.32; z_pT_Bin_Borders[14][17][1] = 0.27; z_pT_Bin_Borders[14][17][2] = 0.65; z_pT_Bin_Borders[14][17][3] = 0.5;
Phi_h_Bin_Values[14][17][0] =  24; Phi_h_Bin_Values[14][17][1] = 315; Phi_h_Bin_Values[14][17][2] = 8569;
z_pT_Bin_Borders[14][18][0] = 0.32; z_pT_Bin_Borders[14][18][1] = 0.27; z_pT_Bin_Borders[14][18][2] = 0.8; z_pT_Bin_Borders[14][18][3] = 0.65;
Phi_h_Bin_Values[14][18][0] =  1; Phi_h_Bin_Values[14][18][1] = 339; Phi_h_Bin_Values[14][18][2] = 8593;
z_pT_Bin_Borders[14][19][0] = 0.4; z_pT_Bin_Borders[14][19][1] = 0.32; z_pT_Bin_Borders[14][19][2] = 0.2; z_pT_Bin_Borders[14][19][3] = 0.05;
Phi_h_Bin_Values[14][19][0] =  24; Phi_h_Bin_Values[14][19][1] = 340; Phi_h_Bin_Values[14][19][2] = 8594;
z_pT_Bin_Borders[14][20][0] = 0.4; z_pT_Bin_Borders[14][20][1] = 0.32; z_pT_Bin_Borders[14][20][2] = 0.3; z_pT_Bin_Borders[14][20][3] = 0.2;
Phi_h_Bin_Values[14][20][0] =  24; Phi_h_Bin_Values[14][20][1] = 364; Phi_h_Bin_Values[14][20][2] = 8618;
z_pT_Bin_Borders[14][21][0] = 0.4; z_pT_Bin_Borders[14][21][1] = 0.32; z_pT_Bin_Borders[14][21][2] = 0.4; z_pT_Bin_Borders[14][21][3] = 0.3;
Phi_h_Bin_Values[14][21][0] =  24; Phi_h_Bin_Values[14][21][1] = 388; Phi_h_Bin_Values[14][21][2] = 8642;
z_pT_Bin_Borders[14][22][0] = 0.4; z_pT_Bin_Borders[14][22][1] = 0.32; z_pT_Bin_Borders[14][22][2] = 0.5; z_pT_Bin_Borders[14][22][3] = 0.4;
Phi_h_Bin_Values[14][22][0] =  24; Phi_h_Bin_Values[14][22][1] = 412; Phi_h_Bin_Values[14][22][2] = 8666;
z_pT_Bin_Borders[14][23][0] = 0.4; z_pT_Bin_Borders[14][23][1] = 0.32; z_pT_Bin_Borders[14][23][2] = 0.65; z_pT_Bin_Borders[14][23][3] = 0.5;
Phi_h_Bin_Values[14][23][0] =  24; Phi_h_Bin_Values[14][23][1] = 436; Phi_h_Bin_Values[14][23][2] = 8690;
z_pT_Bin_Borders[14][24][0] = 0.4; z_pT_Bin_Borders[14][24][1] = 0.32; z_pT_Bin_Borders[14][24][2] = 0.8; z_pT_Bin_Borders[14][24][3] = 0.65;
Phi_h_Bin_Values[14][24][0] =  1; Phi_h_Bin_Values[14][24][1] = 460; Phi_h_Bin_Values[14][24][2] = 8714;
z_pT_Bin_Borders[14][25][0] = 0.53; z_pT_Bin_Borders[14][25][1] = 0.4; z_pT_Bin_Borders[14][25][2] = 0.2; z_pT_Bin_Borders[14][25][3] = 0.05;
Phi_h_Bin_Values[14][25][0] =  24; Phi_h_Bin_Values[14][25][1] = 461; Phi_h_Bin_Values[14][25][2] = 8715;
z_pT_Bin_Borders[14][26][0] = 0.53; z_pT_Bin_Borders[14][26][1] = 0.4; z_pT_Bin_Borders[14][26][2] = 0.3; z_pT_Bin_Borders[14][26][3] = 0.2;
Phi_h_Bin_Values[14][26][0] =  24; Phi_h_Bin_Values[14][26][1] = 485; Phi_h_Bin_Values[14][26][2] = 8739;
z_pT_Bin_Borders[14][27][0] = 0.53; z_pT_Bin_Borders[14][27][1] = 0.4; z_pT_Bin_Borders[14][27][2] = 0.4; z_pT_Bin_Borders[14][27][3] = 0.3;
Phi_h_Bin_Values[14][27][0] =  24; Phi_h_Bin_Values[14][27][1] = 509; Phi_h_Bin_Values[14][27][2] = 8763;
z_pT_Bin_Borders[14][28][0] = 0.53; z_pT_Bin_Borders[14][28][1] = 0.4; z_pT_Bin_Borders[14][28][2] = 0.5; z_pT_Bin_Borders[14][28][3] = 0.4;
Phi_h_Bin_Values[14][28][0] =  24; Phi_h_Bin_Values[14][28][1] = 533; Phi_h_Bin_Values[14][28][2] = 8787;
z_pT_Bin_Borders[14][29][0] = 0.53; z_pT_Bin_Borders[14][29][1] = 0.4; z_pT_Bin_Borders[14][29][2] = 0.65; z_pT_Bin_Borders[14][29][3] = 0.5;
Phi_h_Bin_Values[14][29][0] =  24; Phi_h_Bin_Values[14][29][1] = 557; Phi_h_Bin_Values[14][29][2] = 8811;
z_pT_Bin_Borders[14][30][0] = 0.53; z_pT_Bin_Borders[14][30][1] = 0.4; z_pT_Bin_Borders[14][30][2] = 0.8; z_pT_Bin_Borders[14][30][3] = 0.65;
Phi_h_Bin_Values[14][30][0] =  1; Phi_h_Bin_Values[14][30][1] = 581; Phi_h_Bin_Values[14][30][2] = 8835;
z_pT_Bin_Borders[14][31][0] = 0.69; z_pT_Bin_Borders[14][31][1] = 0.53; z_pT_Bin_Borders[14][31][2] = 0.2; z_pT_Bin_Borders[14][31][3] = 0.05;
Phi_h_Bin_Values[14][31][0] =  24; Phi_h_Bin_Values[14][31][1] = 582; Phi_h_Bin_Values[14][31][2] = 8836;
z_pT_Bin_Borders[14][32][0] = 0.69; z_pT_Bin_Borders[14][32][1] = 0.53; z_pT_Bin_Borders[14][32][2] = 0.3; z_pT_Bin_Borders[14][32][3] = 0.2;
Phi_h_Bin_Values[14][32][0] =  24; Phi_h_Bin_Values[14][32][1] = 606; Phi_h_Bin_Values[14][32][2] = 8860;
z_pT_Bin_Borders[14][33][0] = 0.69; z_pT_Bin_Borders[14][33][1] = 0.53; z_pT_Bin_Borders[14][33][2] = 0.4; z_pT_Bin_Borders[14][33][3] = 0.3;
Phi_h_Bin_Values[14][33][0] =  24; Phi_h_Bin_Values[14][33][1] = 630; Phi_h_Bin_Values[14][33][2] = 8884;
z_pT_Bin_Borders[14][34][0] = 0.69; z_pT_Bin_Borders[14][34][1] = 0.53; z_pT_Bin_Borders[14][34][2] = 0.5; z_pT_Bin_Borders[14][34][3] = 0.4;
Phi_h_Bin_Values[14][34][0] =  1; Phi_h_Bin_Values[14][34][1] = 654; Phi_h_Bin_Values[14][34][2] = 8908;
z_pT_Bin_Borders[14][35][0] = 0.69; z_pT_Bin_Borders[14][35][1] = 0.53; z_pT_Bin_Borders[14][35][2] = 0.65; z_pT_Bin_Borders[14][35][3] = 0.5;
Phi_h_Bin_Values[14][35][0] =  1; Phi_h_Bin_Values[14][35][1] = 655; Phi_h_Bin_Values[14][35][2] = 8909;
z_pT_Bin_Borders[14][36][0] = 0.69; z_pT_Bin_Borders[14][36][1] = 0.53; z_pT_Bin_Borders[14][36][2] = 0.8; z_pT_Bin_Borders[14][36][3] = 0.65;
Phi_h_Bin_Values[14][36][0] =  1; Phi_h_Bin_Values[14][36][1] = 656; Phi_h_Bin_Values[14][36][2] = 8910;
z_pT_Bin_Borders[14][37][0] = 0.19; z_pT_Bin_Borders[14][37][1] = 0; z_pT_Bin_Borders[14][37][2] = 0.05; z_pT_Bin_Borders[14][37][3] = 0;
Phi_h_Bin_Values[14][37][0] =  1; Phi_h_Bin_Values[14][37][1] = 657; Phi_h_Bin_Values[14][37][2] = 8911;
z_pT_Bin_Borders[14][38][0] = 0.19; z_pT_Bin_Borders[14][38][1] = 0; z_pT_Bin_Borders[14][38][2] = 0.05; z_pT_Bin_Borders[14][38][3] = 0.2;
Phi_h_Bin_Values[14][38][0] =  1; Phi_h_Bin_Values[14][38][1] = 658; Phi_h_Bin_Values[14][38][2] = 8912;
z_pT_Bin_Borders[14][39][0] = 0.19; z_pT_Bin_Borders[14][39][1] = 0; z_pT_Bin_Borders[14][39][2] = 0.2; z_pT_Bin_Borders[14][39][3] = 0.3;
Phi_h_Bin_Values[14][39][0] =  1; Phi_h_Bin_Values[14][39][1] = 659; Phi_h_Bin_Values[14][39][2] = 8913;
z_pT_Bin_Borders[14][40][0] = 0.19; z_pT_Bin_Borders[14][40][1] = 0; z_pT_Bin_Borders[14][40][2] = 0.3; z_pT_Bin_Borders[14][40][3] = 0.4;
Phi_h_Bin_Values[14][40][0] =  1; Phi_h_Bin_Values[14][40][1] = 660; Phi_h_Bin_Values[14][40][2] = 8914;
z_pT_Bin_Borders[14][41][0] = 0.19; z_pT_Bin_Borders[14][41][1] = 0; z_pT_Bin_Borders[14][41][2] = 0.4; z_pT_Bin_Borders[14][41][3] = 0.5;
Phi_h_Bin_Values[14][41][0] =  1; Phi_h_Bin_Values[14][41][1] = 661; Phi_h_Bin_Values[14][41][2] = 8915;
z_pT_Bin_Borders[14][42][0] = 0.19; z_pT_Bin_Borders[14][42][1] = 0; z_pT_Bin_Borders[14][42][2] = 0.5; z_pT_Bin_Borders[14][42][3] = 0.65;
Phi_h_Bin_Values[14][42][0] =  1; Phi_h_Bin_Values[14][42][1] = 662; Phi_h_Bin_Values[14][42][2] = 8916;
z_pT_Bin_Borders[14][43][0] = 0.19; z_pT_Bin_Borders[14][43][1] = 0; z_pT_Bin_Borders[14][43][2] = 0.65; z_pT_Bin_Borders[14][43][3] = 0.8;
Phi_h_Bin_Values[14][43][0] =  1; Phi_h_Bin_Values[14][43][1] = 663; Phi_h_Bin_Values[14][43][2] = 8917;
z_pT_Bin_Borders[14][44][0] = 0.19; z_pT_Bin_Borders[14][44][1] = 0; z_pT_Bin_Borders[14][44][2] = 10; z_pT_Bin_Borders[14][44][3] = 0.8;
Phi_h_Bin_Values[14][44][0] =  1; Phi_h_Bin_Values[14][44][1] = 664; Phi_h_Bin_Values[14][44][2] = 8918;
z_pT_Bin_Borders[14][45][0] = 0.19; z_pT_Bin_Borders[14][45][1] = 0.23; z_pT_Bin_Borders[14][45][2] = 0.05; z_pT_Bin_Borders[14][45][3] = 0;
Phi_h_Bin_Values[14][45][0] =  1; Phi_h_Bin_Values[14][45][1] = 665; Phi_h_Bin_Values[14][45][2] = 8919;
z_pT_Bin_Borders[14][46][0] = 0.19; z_pT_Bin_Borders[14][46][1] = 0.23; z_pT_Bin_Borders[14][46][2] = 10; z_pT_Bin_Borders[14][46][3] = 0.8;
Phi_h_Bin_Values[14][46][0] =  1; Phi_h_Bin_Values[14][46][1] = 666; Phi_h_Bin_Values[14][46][2] = 8920;
z_pT_Bin_Borders[14][47][0] = 0.23; z_pT_Bin_Borders[14][47][1] = 0.27; z_pT_Bin_Borders[14][47][2] = 0.05; z_pT_Bin_Borders[14][47][3] = 0;
Phi_h_Bin_Values[14][47][0] =  1; Phi_h_Bin_Values[14][47][1] = 667; Phi_h_Bin_Values[14][47][2] = 8921;
z_pT_Bin_Borders[14][48][0] = 0.23; z_pT_Bin_Borders[14][48][1] = 0.27; z_pT_Bin_Borders[14][48][2] = 10; z_pT_Bin_Borders[14][48][3] = 0.8;
Phi_h_Bin_Values[14][48][0] =  1; Phi_h_Bin_Values[14][48][1] = 668; Phi_h_Bin_Values[14][48][2] = 8922;
z_pT_Bin_Borders[14][49][0] = 0.27; z_pT_Bin_Borders[14][49][1] = 0.32; z_pT_Bin_Borders[14][49][2] = 0.05; z_pT_Bin_Borders[14][49][3] = 0;
Phi_h_Bin_Values[14][49][0] =  1; Phi_h_Bin_Values[14][49][1] = 669; Phi_h_Bin_Values[14][49][2] = 8923;
z_pT_Bin_Borders[14][50][0] = 0.27; z_pT_Bin_Borders[14][50][1] = 0.32; z_pT_Bin_Borders[14][50][2] = 10; z_pT_Bin_Borders[14][50][3] = 0.8;
Phi_h_Bin_Values[14][50][0] =  1; Phi_h_Bin_Values[14][50][1] = 670; Phi_h_Bin_Values[14][50][2] = 8924;
z_pT_Bin_Borders[14][51][0] = 0.32; z_pT_Bin_Borders[14][51][1] = 0.4; z_pT_Bin_Borders[14][51][2] = 0.05; z_pT_Bin_Borders[14][51][3] = 0;
Phi_h_Bin_Values[14][51][0] =  1; Phi_h_Bin_Values[14][51][1] = 671; Phi_h_Bin_Values[14][51][2] = 8925;
z_pT_Bin_Borders[14][52][0] = 0.32; z_pT_Bin_Borders[14][52][1] = 0.4; z_pT_Bin_Borders[14][52][2] = 10; z_pT_Bin_Borders[14][52][3] = 0.8;
Phi_h_Bin_Values[14][52][0] =  1; Phi_h_Bin_Values[14][52][1] = 672; Phi_h_Bin_Values[14][52][2] = 8926;
z_pT_Bin_Borders[14][53][0] = 0.4; z_pT_Bin_Borders[14][53][1] = 0.53; z_pT_Bin_Borders[14][53][2] = 0.05; z_pT_Bin_Borders[14][53][3] = 0;
Phi_h_Bin_Values[14][53][0] =  1; Phi_h_Bin_Values[14][53][1] = 673; Phi_h_Bin_Values[14][53][2] = 8927;
z_pT_Bin_Borders[14][54][0] = 0.4; z_pT_Bin_Borders[14][54][1] = 0.53; z_pT_Bin_Borders[14][54][2] = 10; z_pT_Bin_Borders[14][54][3] = 0.8;
Phi_h_Bin_Values[14][54][0] =  1; Phi_h_Bin_Values[14][54][1] = 674; Phi_h_Bin_Values[14][54][2] = 8928;
z_pT_Bin_Borders[14][55][0] = 0.53; z_pT_Bin_Borders[14][55][1] = 0.69; z_pT_Bin_Borders[14][55][2] = 0.05; z_pT_Bin_Borders[14][55][3] = 0;
Phi_h_Bin_Values[14][55][0] =  1; Phi_h_Bin_Values[14][55][1] = 675; Phi_h_Bin_Values[14][55][2] = 8929;
z_pT_Bin_Borders[14][56][0] = 0.53; z_pT_Bin_Borders[14][56][1] = 0.69; z_pT_Bin_Borders[14][56][2] = 10; z_pT_Bin_Borders[14][56][3] = 0.8;
Phi_h_Bin_Values[14][56][0] =  1; Phi_h_Bin_Values[14][56][1] = 676; Phi_h_Bin_Values[14][56][2] = 8930;
z_pT_Bin_Borders[14][57][0] = 10; z_pT_Bin_Borders[14][57][1] = 0.69; z_pT_Bin_Borders[14][57][2] = 0; z_pT_Bin_Borders[14][57][3] = 0.05;
Phi_h_Bin_Values[14][57][0] =  1; Phi_h_Bin_Values[14][57][1] = 677; Phi_h_Bin_Values[14][57][2] = 8931;
z_pT_Bin_Borders[14][58][0] = 10; z_pT_Bin_Borders[14][58][1] = 0.69; z_pT_Bin_Borders[14][58][2] = 0.05; z_pT_Bin_Borders[14][58][3] = 0.2;
Phi_h_Bin_Values[14][58][0] =  1; Phi_h_Bin_Values[14][58][1] = 678; Phi_h_Bin_Values[14][58][2] = 8932;
z_pT_Bin_Borders[14][59][0] = 10; z_pT_Bin_Borders[14][59][1] = 0.69; z_pT_Bin_Borders[14][59][2] = 0.2; z_pT_Bin_Borders[14][59][3] = 0.3;
Phi_h_Bin_Values[14][59][0] =  1; Phi_h_Bin_Values[14][59][1] = 679; Phi_h_Bin_Values[14][59][2] = 8933;
z_pT_Bin_Borders[14][60][0] = 10; z_pT_Bin_Borders[14][60][1] = 0.69; z_pT_Bin_Borders[14][60][2] = 0.3; z_pT_Bin_Borders[14][60][3] = 0.4;
Phi_h_Bin_Values[14][60][0] =  1; Phi_h_Bin_Values[14][60][1] = 680; Phi_h_Bin_Values[14][60][2] = 8934;
z_pT_Bin_Borders[14][61][0] = 10; z_pT_Bin_Borders[14][61][1] = 0.69; z_pT_Bin_Borders[14][61][2] = 0.4; z_pT_Bin_Borders[14][61][3] = 0.5;
Phi_h_Bin_Values[14][61][0] =  1; Phi_h_Bin_Values[14][61][1] = 681; Phi_h_Bin_Values[14][61][2] = 8935;
z_pT_Bin_Borders[14][62][0] = 10; z_pT_Bin_Borders[14][62][1] = 0.69; z_pT_Bin_Borders[14][62][2] = 0.5; z_pT_Bin_Borders[14][62][3] = 0.65;
Phi_h_Bin_Values[14][62][0] =  1; Phi_h_Bin_Values[14][62][1] = 682; Phi_h_Bin_Values[14][62][2] = 8936;
z_pT_Bin_Borders[14][63][0] = 10; z_pT_Bin_Borders[14][63][1] = 0.69; z_pT_Bin_Borders[14][63][2] = 0.65; z_pT_Bin_Borders[14][63][3] = 0.8;
Phi_h_Bin_Values[14][63][0] =  1; Phi_h_Bin_Values[14][63][1] = 683; Phi_h_Bin_Values[14][63][2] = 8937;
z_pT_Bin_Borders[14][64][0] = 10; z_pT_Bin_Borders[14][64][1] = 0.69; z_pT_Bin_Borders[14][64][2] = 10; z_pT_Bin_Borders[14][64][3] = 0.8;
Phi_h_Bin_Values[14][64][0] =  1; Phi_h_Bin_Values[14][64][1] = 684; Phi_h_Bin_Values[14][64][2] = 8938;
z_pT_Bin_Borders[15][1][0] = 0.28; z_pT_Bin_Borders[15][1][1] = 0.22; z_pT_Bin_Borders[15][1][2] = 0.23; z_pT_Bin_Borders[15][1][3] = 0.05;
Phi_h_Bin_Values[15][1][0] =  24; Phi_h_Bin_Values[15][1][1] = 0; Phi_h_Bin_Values[15][1][2] = 8939;
z_pT_Bin_Borders[15][2][0] = 0.28; z_pT_Bin_Borders[15][2][1] = 0.22; z_pT_Bin_Borders[15][2][2] = 0.33; z_pT_Bin_Borders[15][2][3] = 0.23;
Phi_h_Bin_Values[15][2][0] =  24; Phi_h_Bin_Values[15][2][1] = 24; Phi_h_Bin_Values[15][2][2] = 8963;
z_pT_Bin_Borders[15][3][0] = 0.28; z_pT_Bin_Borders[15][3][1] = 0.22; z_pT_Bin_Borders[15][3][2] = 0.47; z_pT_Bin_Borders[15][3][3] = 0.33;
Phi_h_Bin_Values[15][3][0] =  24; Phi_h_Bin_Values[15][3][1] = 48; Phi_h_Bin_Values[15][3][2] = 8987;
z_pT_Bin_Borders[15][4][0] = 0.33; z_pT_Bin_Borders[15][4][1] = 0.28; z_pT_Bin_Borders[15][4][2] = 0.23; z_pT_Bin_Borders[15][4][3] = 0.05;
Phi_h_Bin_Values[15][4][0] =  24; Phi_h_Bin_Values[15][4][1] = 72; Phi_h_Bin_Values[15][4][2] = 9011;
z_pT_Bin_Borders[15][5][0] = 0.33; z_pT_Bin_Borders[15][5][1] = 0.28; z_pT_Bin_Borders[15][5][2] = 0.33; z_pT_Bin_Borders[15][5][3] = 0.23;
Phi_h_Bin_Values[15][5][0] =  24; Phi_h_Bin_Values[15][5][1] = 96; Phi_h_Bin_Values[15][5][2] = 9035;
z_pT_Bin_Borders[15][6][0] = 0.33; z_pT_Bin_Borders[15][6][1] = 0.28; z_pT_Bin_Borders[15][6][2] = 0.47; z_pT_Bin_Borders[15][6][3] = 0.33;
Phi_h_Bin_Values[15][6][0] =  24; Phi_h_Bin_Values[15][6][1] = 120; Phi_h_Bin_Values[15][6][2] = 9059;
z_pT_Bin_Borders[15][7][0] = 0.4; z_pT_Bin_Borders[15][7][1] = 0.33; z_pT_Bin_Borders[15][7][2] = 0.23; z_pT_Bin_Borders[15][7][3] = 0.05;
Phi_h_Bin_Values[15][7][0] =  24; Phi_h_Bin_Values[15][7][1] = 144; Phi_h_Bin_Values[15][7][2] = 9083;
z_pT_Bin_Borders[15][8][0] = 0.4; z_pT_Bin_Borders[15][8][1] = 0.33; z_pT_Bin_Borders[15][8][2] = 0.33; z_pT_Bin_Borders[15][8][3] = 0.23;
Phi_h_Bin_Values[15][8][0] =  24; Phi_h_Bin_Values[15][8][1] = 168; Phi_h_Bin_Values[15][8][2] = 9107;
z_pT_Bin_Borders[15][9][0] = 0.4; z_pT_Bin_Borders[15][9][1] = 0.33; z_pT_Bin_Borders[15][9][2] = 0.47; z_pT_Bin_Borders[15][9][3] = 0.33;
Phi_h_Bin_Values[15][9][0] =  24; Phi_h_Bin_Values[15][9][1] = 192; Phi_h_Bin_Values[15][9][2] = 9131;
z_pT_Bin_Borders[15][10][0] = 0.51; z_pT_Bin_Borders[15][10][1] = 0.4; z_pT_Bin_Borders[15][10][2] = 0.23; z_pT_Bin_Borders[15][10][3] = 0.05;
Phi_h_Bin_Values[15][10][0] =  24; Phi_h_Bin_Values[15][10][1] = 216; Phi_h_Bin_Values[15][10][2] = 9155;
z_pT_Bin_Borders[15][11][0] = 0.51; z_pT_Bin_Borders[15][11][1] = 0.4; z_pT_Bin_Borders[15][11][2] = 0.33; z_pT_Bin_Borders[15][11][3] = 0.23;
Phi_h_Bin_Values[15][11][0] =  24; Phi_h_Bin_Values[15][11][1] = 240; Phi_h_Bin_Values[15][11][2] = 9179;
z_pT_Bin_Borders[15][12][0] = 0.51; z_pT_Bin_Borders[15][12][1] = 0.4; z_pT_Bin_Borders[15][12][2] = 0.47; z_pT_Bin_Borders[15][12][3] = 0.33;
Phi_h_Bin_Values[15][12][0] =  1; Phi_h_Bin_Values[15][12][1] = 264; Phi_h_Bin_Values[15][12][2] = 9203;
z_pT_Bin_Borders[15][13][0] = 0.22; z_pT_Bin_Borders[15][13][1] = 0; z_pT_Bin_Borders[15][13][2] = 0.05; z_pT_Bin_Borders[15][13][3] = 0;
Phi_h_Bin_Values[15][13][0] =  1; Phi_h_Bin_Values[15][13][1] = 265; Phi_h_Bin_Values[15][13][2] = 9204;
z_pT_Bin_Borders[15][14][0] = 0.22; z_pT_Bin_Borders[15][14][1] = 0; z_pT_Bin_Borders[15][14][2] = 0.05; z_pT_Bin_Borders[15][14][3] = 0.23;
Phi_h_Bin_Values[15][14][0] =  1; Phi_h_Bin_Values[15][14][1] = 266; Phi_h_Bin_Values[15][14][2] = 9205;
z_pT_Bin_Borders[15][15][0] = 0.22; z_pT_Bin_Borders[15][15][1] = 0; z_pT_Bin_Borders[15][15][2] = 0.23; z_pT_Bin_Borders[15][15][3] = 0.33;
Phi_h_Bin_Values[15][15][0] =  1; Phi_h_Bin_Values[15][15][1] = 267; Phi_h_Bin_Values[15][15][2] = 9206;
z_pT_Bin_Borders[15][16][0] = 0.22; z_pT_Bin_Borders[15][16][1] = 0; z_pT_Bin_Borders[15][16][2] = 0.33; z_pT_Bin_Borders[15][16][3] = 0.47;
Phi_h_Bin_Values[15][16][0] =  1; Phi_h_Bin_Values[15][16][1] = 268; Phi_h_Bin_Values[15][16][2] = 9207;
z_pT_Bin_Borders[15][17][0] = 0.22; z_pT_Bin_Borders[15][17][1] = 0; z_pT_Bin_Borders[15][17][2] = 10; z_pT_Bin_Borders[15][17][3] = 0.47;
Phi_h_Bin_Values[15][17][0] =  1; Phi_h_Bin_Values[15][17][1] = 269; Phi_h_Bin_Values[15][17][2] = 9208;
z_pT_Bin_Borders[15][18][0] = 0.22; z_pT_Bin_Borders[15][18][1] = 0.28; z_pT_Bin_Borders[15][18][2] = 0.05; z_pT_Bin_Borders[15][18][3] = 0;
Phi_h_Bin_Values[15][18][0] =  1; Phi_h_Bin_Values[15][18][1] = 270; Phi_h_Bin_Values[15][18][2] = 9209;
z_pT_Bin_Borders[15][19][0] = 0.22; z_pT_Bin_Borders[15][19][1] = 0.28; z_pT_Bin_Borders[15][19][2] = 10; z_pT_Bin_Borders[15][19][3] = 0.47;
Phi_h_Bin_Values[15][19][0] =  1; Phi_h_Bin_Values[15][19][1] = 271; Phi_h_Bin_Values[15][19][2] = 9210;
z_pT_Bin_Borders[15][20][0] = 0.28; z_pT_Bin_Borders[15][20][1] = 0.33; z_pT_Bin_Borders[15][20][2] = 0.05; z_pT_Bin_Borders[15][20][3] = 0;
Phi_h_Bin_Values[15][20][0] =  1; Phi_h_Bin_Values[15][20][1] = 272; Phi_h_Bin_Values[15][20][2] = 9211;
z_pT_Bin_Borders[15][21][0] = 0.28; z_pT_Bin_Borders[15][21][1] = 0.33; z_pT_Bin_Borders[15][21][2] = 10; z_pT_Bin_Borders[15][21][3] = 0.47;
Phi_h_Bin_Values[15][21][0] =  1; Phi_h_Bin_Values[15][21][1] = 273; Phi_h_Bin_Values[15][21][2] = 9212;
z_pT_Bin_Borders[15][22][0] = 0.33; z_pT_Bin_Borders[15][22][1] = 0.4; z_pT_Bin_Borders[15][22][2] = 0.05; z_pT_Bin_Borders[15][22][3] = 0;
Phi_h_Bin_Values[15][22][0] =  1; Phi_h_Bin_Values[15][22][1] = 274; Phi_h_Bin_Values[15][22][2] = 9213;
z_pT_Bin_Borders[15][23][0] = 0.33; z_pT_Bin_Borders[15][23][1] = 0.4; z_pT_Bin_Borders[15][23][2] = 10; z_pT_Bin_Borders[15][23][3] = 0.47;
Phi_h_Bin_Values[15][23][0] =  1; Phi_h_Bin_Values[15][23][1] = 275; Phi_h_Bin_Values[15][23][2] = 9214;
z_pT_Bin_Borders[15][24][0] = 0.4; z_pT_Bin_Borders[15][24][1] = 0.51; z_pT_Bin_Borders[15][24][2] = 0.05; z_pT_Bin_Borders[15][24][3] = 0;
Phi_h_Bin_Values[15][24][0] =  1; Phi_h_Bin_Values[15][24][1] = 276; Phi_h_Bin_Values[15][24][2] = 9215;
z_pT_Bin_Borders[15][25][0] = 0.4; z_pT_Bin_Borders[15][25][1] = 0.51; z_pT_Bin_Borders[15][25][2] = 10; z_pT_Bin_Borders[15][25][3] = 0.47;
Phi_h_Bin_Values[15][25][0] =  1; Phi_h_Bin_Values[15][25][1] = 277; Phi_h_Bin_Values[15][25][2] = 9216;
z_pT_Bin_Borders[15][26][0] = 10; z_pT_Bin_Borders[15][26][1] = 0.51; z_pT_Bin_Borders[15][26][2] = 0; z_pT_Bin_Borders[15][26][3] = 0.05;
Phi_h_Bin_Values[15][26][0] =  1; Phi_h_Bin_Values[15][26][1] = 278; Phi_h_Bin_Values[15][26][2] = 9217;
z_pT_Bin_Borders[15][27][0] = 10; z_pT_Bin_Borders[15][27][1] = 0.51; z_pT_Bin_Borders[15][27][2] = 0.05; z_pT_Bin_Borders[15][27][3] = 0.23;
Phi_h_Bin_Values[15][27][0] =  1; Phi_h_Bin_Values[15][27][1] = 279; Phi_h_Bin_Values[15][27][2] = 9218;
z_pT_Bin_Borders[15][28][0] = 10; z_pT_Bin_Borders[15][28][1] = 0.51; z_pT_Bin_Borders[15][28][2] = 0.23; z_pT_Bin_Borders[15][28][3] = 0.33;
Phi_h_Bin_Values[15][28][0] =  1; Phi_h_Bin_Values[15][28][1] = 280; Phi_h_Bin_Values[15][28][2] = 9219;
z_pT_Bin_Borders[15][29][0] = 10; z_pT_Bin_Borders[15][29][1] = 0.51; z_pT_Bin_Borders[15][29][2] = 0.33; z_pT_Bin_Borders[15][29][3] = 0.47;
Phi_h_Bin_Values[15][29][0] =  1; Phi_h_Bin_Values[15][29][1] = 281; Phi_h_Bin_Values[15][29][2] = 9220;
z_pT_Bin_Borders[15][30][0] = 10; z_pT_Bin_Borders[15][30][1] = 0.51; z_pT_Bin_Borders[15][30][2] = 10; z_pT_Bin_Borders[15][30][3] = 0.47;
Phi_h_Bin_Values[15][30][0] =  1; Phi_h_Bin_Values[15][30][1] = 282; Phi_h_Bin_Values[15][30][2] = 9221;
z_pT_Bin_Borders[16][1][0] = 0.2; z_pT_Bin_Borders[16][1][1] = 0.16; z_pT_Bin_Borders[16][1][2] = 0.22; z_pT_Bin_Borders[16][1][3] = 0.05;
Phi_h_Bin_Values[16][1][0] =  24; Phi_h_Bin_Values[16][1][1] = 0; Phi_h_Bin_Values[16][1][2] = 9222;
z_pT_Bin_Borders[16][2][0] = 0.2; z_pT_Bin_Borders[16][2][1] = 0.16; z_pT_Bin_Borders[16][2][2] = 0.31; z_pT_Bin_Borders[16][2][3] = 0.22;
Phi_h_Bin_Values[16][2][0] =  24; Phi_h_Bin_Values[16][2][1] = 24; Phi_h_Bin_Values[16][2][2] = 9246;
z_pT_Bin_Borders[16][3][0] = 0.2; z_pT_Bin_Borders[16][3][1] = 0.16; z_pT_Bin_Borders[16][3][2] = 0.44; z_pT_Bin_Borders[16][3][3] = 0.31;
Phi_h_Bin_Values[16][3][0] =  24; Phi_h_Bin_Values[16][3][1] = 48; Phi_h_Bin_Values[16][3][2] = 9270;
z_pT_Bin_Borders[16][4][0] = 0.2; z_pT_Bin_Borders[16][4][1] = 0.16; z_pT_Bin_Borders[16][4][2] = 0.7; z_pT_Bin_Borders[16][4][3] = 0.44;
Phi_h_Bin_Values[16][4][0] =  1; Phi_h_Bin_Values[16][4][1] = 72; Phi_h_Bin_Values[16][4][2] = 9294;
z_pT_Bin_Borders[16][5][0] = 0.24; z_pT_Bin_Borders[16][5][1] = 0.2; z_pT_Bin_Borders[16][5][2] = 0.22; z_pT_Bin_Borders[16][5][3] = 0.05;
Phi_h_Bin_Values[16][5][0] =  24; Phi_h_Bin_Values[16][5][1] = 73; Phi_h_Bin_Values[16][5][2] = 9295;
z_pT_Bin_Borders[16][6][0] = 0.24; z_pT_Bin_Borders[16][6][1] = 0.2; z_pT_Bin_Borders[16][6][2] = 0.31; z_pT_Bin_Borders[16][6][3] = 0.22;
Phi_h_Bin_Values[16][6][0] =  24; Phi_h_Bin_Values[16][6][1] = 97; Phi_h_Bin_Values[16][6][2] = 9319;
z_pT_Bin_Borders[16][7][0] = 0.24; z_pT_Bin_Borders[16][7][1] = 0.2; z_pT_Bin_Borders[16][7][2] = 0.44; z_pT_Bin_Borders[16][7][3] = 0.31;
Phi_h_Bin_Values[16][7][0] =  24; Phi_h_Bin_Values[16][7][1] = 121; Phi_h_Bin_Values[16][7][2] = 9343;
z_pT_Bin_Borders[16][8][0] = 0.24; z_pT_Bin_Borders[16][8][1] = 0.2; z_pT_Bin_Borders[16][8][2] = 0.7; z_pT_Bin_Borders[16][8][3] = 0.44;
Phi_h_Bin_Values[16][8][0] =  1; Phi_h_Bin_Values[16][8][1] = 145; Phi_h_Bin_Values[16][8][2] = 9367;
z_pT_Bin_Borders[16][9][0] = 0.29; z_pT_Bin_Borders[16][9][1] = 0.24; z_pT_Bin_Borders[16][9][2] = 0.22; z_pT_Bin_Borders[16][9][3] = 0.05;
Phi_h_Bin_Values[16][9][0] =  24; Phi_h_Bin_Values[16][9][1] = 146; Phi_h_Bin_Values[16][9][2] = 9368;
z_pT_Bin_Borders[16][10][0] = 0.29; z_pT_Bin_Borders[16][10][1] = 0.24; z_pT_Bin_Borders[16][10][2] = 0.31; z_pT_Bin_Borders[16][10][3] = 0.22;
Phi_h_Bin_Values[16][10][0] =  24; Phi_h_Bin_Values[16][10][1] = 170; Phi_h_Bin_Values[16][10][2] = 9392;
z_pT_Bin_Borders[16][11][0] = 0.29; z_pT_Bin_Borders[16][11][1] = 0.24; z_pT_Bin_Borders[16][11][2] = 0.44; z_pT_Bin_Borders[16][11][3] = 0.31;
Phi_h_Bin_Values[16][11][0] =  24; Phi_h_Bin_Values[16][11][1] = 194; Phi_h_Bin_Values[16][11][2] = 9416;
z_pT_Bin_Borders[16][12][0] = 0.29; z_pT_Bin_Borders[16][12][1] = 0.24; z_pT_Bin_Borders[16][12][2] = 0.7; z_pT_Bin_Borders[16][12][3] = 0.44;
Phi_h_Bin_Values[16][12][0] =  24; Phi_h_Bin_Values[16][12][1] = 218; Phi_h_Bin_Values[16][12][2] = 9440;
z_pT_Bin_Borders[16][13][0] = 0.36; z_pT_Bin_Borders[16][13][1] = 0.29; z_pT_Bin_Borders[16][13][2] = 0.22; z_pT_Bin_Borders[16][13][3] = 0.05;
Phi_h_Bin_Values[16][13][0] =  24; Phi_h_Bin_Values[16][13][1] = 242; Phi_h_Bin_Values[16][13][2] = 9464;
z_pT_Bin_Borders[16][14][0] = 0.36; z_pT_Bin_Borders[16][14][1] = 0.29; z_pT_Bin_Borders[16][14][2] = 0.31; z_pT_Bin_Borders[16][14][3] = 0.22;
Phi_h_Bin_Values[16][14][0] =  24; Phi_h_Bin_Values[16][14][1] = 266; Phi_h_Bin_Values[16][14][2] = 9488;
z_pT_Bin_Borders[16][15][0] = 0.36; z_pT_Bin_Borders[16][15][1] = 0.29; z_pT_Bin_Borders[16][15][2] = 0.44; z_pT_Bin_Borders[16][15][3] = 0.31;
Phi_h_Bin_Values[16][15][0] =  24; Phi_h_Bin_Values[16][15][1] = 290; Phi_h_Bin_Values[16][15][2] = 9512;
z_pT_Bin_Borders[16][16][0] = 0.36; z_pT_Bin_Borders[16][16][1] = 0.29; z_pT_Bin_Borders[16][16][2] = 0.7; z_pT_Bin_Borders[16][16][3] = 0.44;
Phi_h_Bin_Values[16][16][0] =  24; Phi_h_Bin_Values[16][16][1] = 314; Phi_h_Bin_Values[16][16][2] = 9536;
z_pT_Bin_Borders[16][17][0] = 0.45; z_pT_Bin_Borders[16][17][1] = 0.36; z_pT_Bin_Borders[16][17][2] = 0.22; z_pT_Bin_Borders[16][17][3] = 0.05;
Phi_h_Bin_Values[16][17][0] =  24; Phi_h_Bin_Values[16][17][1] = 338; Phi_h_Bin_Values[16][17][2] = 9560;
z_pT_Bin_Borders[16][18][0] = 0.45; z_pT_Bin_Borders[16][18][1] = 0.36; z_pT_Bin_Borders[16][18][2] = 0.31; z_pT_Bin_Borders[16][18][3] = 0.22;
Phi_h_Bin_Values[16][18][0] =  24; Phi_h_Bin_Values[16][18][1] = 362; Phi_h_Bin_Values[16][18][2] = 9584;
z_pT_Bin_Borders[16][19][0] = 0.45; z_pT_Bin_Borders[16][19][1] = 0.36; z_pT_Bin_Borders[16][19][2] = 0.44; z_pT_Bin_Borders[16][19][3] = 0.31;
Phi_h_Bin_Values[16][19][0] =  24; Phi_h_Bin_Values[16][19][1] = 386; Phi_h_Bin_Values[16][19][2] = 9608;
z_pT_Bin_Borders[16][20][0] = 0.45; z_pT_Bin_Borders[16][20][1] = 0.36; z_pT_Bin_Borders[16][20][2] = 0.7; z_pT_Bin_Borders[16][20][3] = 0.44;
Phi_h_Bin_Values[16][20][0] =  24; Phi_h_Bin_Values[16][20][1] = 410; Phi_h_Bin_Values[16][20][2] = 9632;
z_pT_Bin_Borders[16][21][0] = 0.62; z_pT_Bin_Borders[16][21][1] = 0.45; z_pT_Bin_Borders[16][21][2] = 0.22; z_pT_Bin_Borders[16][21][3] = 0.05;
Phi_h_Bin_Values[16][21][0] =  24; Phi_h_Bin_Values[16][21][1] = 434; Phi_h_Bin_Values[16][21][2] = 9656;
z_pT_Bin_Borders[16][22][0] = 0.62; z_pT_Bin_Borders[16][22][1] = 0.45; z_pT_Bin_Borders[16][22][2] = 0.31; z_pT_Bin_Borders[16][22][3] = 0.22;
Phi_h_Bin_Values[16][22][0] =  24; Phi_h_Bin_Values[16][22][1] = 458; Phi_h_Bin_Values[16][22][2] = 9680;
z_pT_Bin_Borders[16][23][0] = 0.62; z_pT_Bin_Borders[16][23][1] = 0.45; z_pT_Bin_Borders[16][23][2] = 0.44; z_pT_Bin_Borders[16][23][3] = 0.31;
Phi_h_Bin_Values[16][23][0] =  24; Phi_h_Bin_Values[16][23][1] = 482; Phi_h_Bin_Values[16][23][2] = 9704;
z_pT_Bin_Borders[16][24][0] = 0.62; z_pT_Bin_Borders[16][24][1] = 0.45; z_pT_Bin_Borders[16][24][2] = 0.7; z_pT_Bin_Borders[16][24][3] = 0.44;
Phi_h_Bin_Values[16][24][0] =  1; Phi_h_Bin_Values[16][24][1] = 506; Phi_h_Bin_Values[16][24][2] = 9728;
z_pT_Bin_Borders[16][25][0] = 0.16; z_pT_Bin_Borders[16][25][1] = 0; z_pT_Bin_Borders[16][25][2] = 0.05; z_pT_Bin_Borders[16][25][3] = 0;
Phi_h_Bin_Values[16][25][0] =  1; Phi_h_Bin_Values[16][25][1] = 507; Phi_h_Bin_Values[16][25][2] = 9729;
z_pT_Bin_Borders[16][26][0] = 0.16; z_pT_Bin_Borders[16][26][1] = 0; z_pT_Bin_Borders[16][26][2] = 0.05; z_pT_Bin_Borders[16][26][3] = 0.22;
Phi_h_Bin_Values[16][26][0] =  1; Phi_h_Bin_Values[16][26][1] = 508; Phi_h_Bin_Values[16][26][2] = 9730;
z_pT_Bin_Borders[16][27][0] = 0.16; z_pT_Bin_Borders[16][27][1] = 0; z_pT_Bin_Borders[16][27][2] = 0.22; z_pT_Bin_Borders[16][27][3] = 0.31;
Phi_h_Bin_Values[16][27][0] =  1; Phi_h_Bin_Values[16][27][1] = 509; Phi_h_Bin_Values[16][27][2] = 9731;
z_pT_Bin_Borders[16][28][0] = 0.16; z_pT_Bin_Borders[16][28][1] = 0; z_pT_Bin_Borders[16][28][2] = 0.31; z_pT_Bin_Borders[16][28][3] = 0.44;
Phi_h_Bin_Values[16][28][0] =  1; Phi_h_Bin_Values[16][28][1] = 510; Phi_h_Bin_Values[16][28][2] = 9732;
z_pT_Bin_Borders[16][29][0] = 0.16; z_pT_Bin_Borders[16][29][1] = 0; z_pT_Bin_Borders[16][29][2] = 0.44; z_pT_Bin_Borders[16][29][3] = 0.7;
Phi_h_Bin_Values[16][29][0] =  1; Phi_h_Bin_Values[16][29][1] = 511; Phi_h_Bin_Values[16][29][2] = 9733;
z_pT_Bin_Borders[16][30][0] = 0.16; z_pT_Bin_Borders[16][30][1] = 0; z_pT_Bin_Borders[16][30][2] = 10; z_pT_Bin_Borders[16][30][3] = 0.7;
Phi_h_Bin_Values[16][30][0] =  1; Phi_h_Bin_Values[16][30][1] = 512; Phi_h_Bin_Values[16][30][2] = 9734;
z_pT_Bin_Borders[16][31][0] = 0.16; z_pT_Bin_Borders[16][31][1] = 0.2; z_pT_Bin_Borders[16][31][2] = 0.05; z_pT_Bin_Borders[16][31][3] = 0;
Phi_h_Bin_Values[16][31][0] =  1; Phi_h_Bin_Values[16][31][1] = 513; Phi_h_Bin_Values[16][31][2] = 9735;
z_pT_Bin_Borders[16][32][0] = 0.16; z_pT_Bin_Borders[16][32][1] = 0.2; z_pT_Bin_Borders[16][32][2] = 10; z_pT_Bin_Borders[16][32][3] = 0.7;
Phi_h_Bin_Values[16][32][0] =  1; Phi_h_Bin_Values[16][32][1] = 514; Phi_h_Bin_Values[16][32][2] = 9736;
z_pT_Bin_Borders[16][33][0] = 0.2; z_pT_Bin_Borders[16][33][1] = 0.24; z_pT_Bin_Borders[16][33][2] = 0.05; z_pT_Bin_Borders[16][33][3] = 0;
Phi_h_Bin_Values[16][33][0] =  1; Phi_h_Bin_Values[16][33][1] = 515; Phi_h_Bin_Values[16][33][2] = 9737;
z_pT_Bin_Borders[16][34][0] = 0.2; z_pT_Bin_Borders[16][34][1] = 0.24; z_pT_Bin_Borders[16][34][2] = 10; z_pT_Bin_Borders[16][34][3] = 0.7;
Phi_h_Bin_Values[16][34][0] =  1; Phi_h_Bin_Values[16][34][1] = 516; Phi_h_Bin_Values[16][34][2] = 9738;
z_pT_Bin_Borders[16][35][0] = 0.24; z_pT_Bin_Borders[16][35][1] = 0.29; z_pT_Bin_Borders[16][35][2] = 0.05; z_pT_Bin_Borders[16][35][3] = 0;
Phi_h_Bin_Values[16][35][0] =  1; Phi_h_Bin_Values[16][35][1] = 517; Phi_h_Bin_Values[16][35][2] = 9739;
z_pT_Bin_Borders[16][36][0] = 0.24; z_pT_Bin_Borders[16][36][1] = 0.29; z_pT_Bin_Borders[16][36][2] = 10; z_pT_Bin_Borders[16][36][3] = 0.7;
Phi_h_Bin_Values[16][36][0] =  1; Phi_h_Bin_Values[16][36][1] = 518; Phi_h_Bin_Values[16][36][2] = 9740;
z_pT_Bin_Borders[16][37][0] = 0.29; z_pT_Bin_Borders[16][37][1] = 0.36; z_pT_Bin_Borders[16][37][2] = 0.05; z_pT_Bin_Borders[16][37][3] = 0;
Phi_h_Bin_Values[16][37][0] =  1; Phi_h_Bin_Values[16][37][1] = 519; Phi_h_Bin_Values[16][37][2] = 9741;
z_pT_Bin_Borders[16][38][0] = 0.29; z_pT_Bin_Borders[16][38][1] = 0.36; z_pT_Bin_Borders[16][38][2] = 10; z_pT_Bin_Borders[16][38][3] = 0.7;
Phi_h_Bin_Values[16][38][0] =  1; Phi_h_Bin_Values[16][38][1] = 520; Phi_h_Bin_Values[16][38][2] = 9742;
z_pT_Bin_Borders[16][39][0] = 0.36; z_pT_Bin_Borders[16][39][1] = 0.45; z_pT_Bin_Borders[16][39][2] = 0.05; z_pT_Bin_Borders[16][39][3] = 0;
Phi_h_Bin_Values[16][39][0] =  1; Phi_h_Bin_Values[16][39][1] = 521; Phi_h_Bin_Values[16][39][2] = 9743;
z_pT_Bin_Borders[16][40][0] = 0.36; z_pT_Bin_Borders[16][40][1] = 0.45; z_pT_Bin_Borders[16][40][2] = 10; z_pT_Bin_Borders[16][40][3] = 0.7;
Phi_h_Bin_Values[16][40][0] =  1; Phi_h_Bin_Values[16][40][1] = 522; Phi_h_Bin_Values[16][40][2] = 9744;
z_pT_Bin_Borders[16][41][0] = 0.45; z_pT_Bin_Borders[16][41][1] = 0.62; z_pT_Bin_Borders[16][41][2] = 0.05; z_pT_Bin_Borders[16][41][3] = 0;
Phi_h_Bin_Values[16][41][0] =  1; Phi_h_Bin_Values[16][41][1] = 523; Phi_h_Bin_Values[16][41][2] = 9745;
z_pT_Bin_Borders[16][42][0] = 0.45; z_pT_Bin_Borders[16][42][1] = 0.62; z_pT_Bin_Borders[16][42][2] = 10; z_pT_Bin_Borders[16][42][3] = 0.7;
Phi_h_Bin_Values[16][42][0] =  1; Phi_h_Bin_Values[16][42][1] = 524; Phi_h_Bin_Values[16][42][2] = 9746;
z_pT_Bin_Borders[16][43][0] = 10; z_pT_Bin_Borders[16][43][1] = 0.62; z_pT_Bin_Borders[16][43][2] = 0; z_pT_Bin_Borders[16][43][3] = 0.05;
Phi_h_Bin_Values[16][43][0] =  1; Phi_h_Bin_Values[16][43][1] = 525; Phi_h_Bin_Values[16][43][2] = 9747;
z_pT_Bin_Borders[16][44][0] = 10; z_pT_Bin_Borders[16][44][1] = 0.62; z_pT_Bin_Borders[16][44][2] = 0.05; z_pT_Bin_Borders[16][44][3] = 0.22;
Phi_h_Bin_Values[16][44][0] =  1; Phi_h_Bin_Values[16][44][1] = 526; Phi_h_Bin_Values[16][44][2] = 9748;
z_pT_Bin_Borders[16][45][0] = 10; z_pT_Bin_Borders[16][45][1] = 0.62; z_pT_Bin_Borders[16][45][2] = 0.22; z_pT_Bin_Borders[16][45][3] = 0.31;
Phi_h_Bin_Values[16][45][0] =  1; Phi_h_Bin_Values[16][45][1] = 527; Phi_h_Bin_Values[16][45][2] = 9749;
z_pT_Bin_Borders[16][46][0] = 10; z_pT_Bin_Borders[16][46][1] = 0.62; z_pT_Bin_Borders[16][46][2] = 0.31; z_pT_Bin_Borders[16][46][3] = 0.44;
Phi_h_Bin_Values[16][46][0] =  1; Phi_h_Bin_Values[16][46][1] = 528; Phi_h_Bin_Values[16][46][2] = 9750;
z_pT_Bin_Borders[16][47][0] = 10; z_pT_Bin_Borders[16][47][1] = 0.62; z_pT_Bin_Borders[16][47][2] = 0.44; z_pT_Bin_Borders[16][47][3] = 0.7;
Phi_h_Bin_Values[16][47][0] =  1; Phi_h_Bin_Values[16][47][1] = 529; Phi_h_Bin_Values[16][47][2] = 9751;
z_pT_Bin_Borders[16][48][0] = 10; z_pT_Bin_Borders[16][48][1] = 0.62; z_pT_Bin_Borders[16][48][2] = 10; z_pT_Bin_Borders[16][48][3] = 0.7;
Phi_h_Bin_Values[16][48][0] =  1; Phi_h_Bin_Values[16][48][1] = 530; Phi_h_Bin_Values[16][48][2] = 9752;
z_pT_Bin_Borders[17][1][0] = 0.23; z_pT_Bin_Borders[17][1][1] = 0.19; z_pT_Bin_Borders[17][1][2] = 0.19; z_pT_Bin_Borders[17][1][3] = 0.05;
Phi_h_Bin_Values[17][1][0] =  24; Phi_h_Bin_Values[17][1][1] = 0; Phi_h_Bin_Values[17][1][2] = 9753;
z_pT_Bin_Borders[17][2][0] = 0.23; z_pT_Bin_Borders[17][2][1] = 0.19; z_pT_Bin_Borders[17][2][2] = 0.28; z_pT_Bin_Borders[17][2][3] = 0.19;
Phi_h_Bin_Values[17][2][0] =  24; Phi_h_Bin_Values[17][2][1] = 24; Phi_h_Bin_Values[17][2][2] = 9777;
z_pT_Bin_Borders[17][3][0] = 0.23; z_pT_Bin_Borders[17][3][1] = 0.19; z_pT_Bin_Borders[17][3][2] = 0.37; z_pT_Bin_Borders[17][3][3] = 0.28;
Phi_h_Bin_Values[17][3][0] =  24; Phi_h_Bin_Values[17][3][1] = 48; Phi_h_Bin_Values[17][3][2] = 9801;
z_pT_Bin_Borders[17][4][0] = 0.29; z_pT_Bin_Borders[17][4][1] = 0.23; z_pT_Bin_Borders[17][4][2] = 0.19; z_pT_Bin_Borders[17][4][3] = 0.05;
Phi_h_Bin_Values[17][4][0] =  24; Phi_h_Bin_Values[17][4][1] = 72; Phi_h_Bin_Values[17][4][2] = 9825;
z_pT_Bin_Borders[17][5][0] = 0.29; z_pT_Bin_Borders[17][5][1] = 0.23; z_pT_Bin_Borders[17][5][2] = 0.28; z_pT_Bin_Borders[17][5][3] = 0.19;
Phi_h_Bin_Values[17][5][0] =  24; Phi_h_Bin_Values[17][5][1] = 96; Phi_h_Bin_Values[17][5][2] = 9849;
z_pT_Bin_Borders[17][6][0] = 0.29; z_pT_Bin_Borders[17][6][1] = 0.23; z_pT_Bin_Borders[17][6][2] = 0.37; z_pT_Bin_Borders[17][6][3] = 0.28;
Phi_h_Bin_Values[17][6][0] =  24; Phi_h_Bin_Values[17][6][1] = 120; Phi_h_Bin_Values[17][6][2] = 9873;
z_pT_Bin_Borders[17][7][0] = 0.35; z_pT_Bin_Borders[17][7][1] = 0.29; z_pT_Bin_Borders[17][7][2] = 0.19; z_pT_Bin_Borders[17][7][3] = 0.05;
Phi_h_Bin_Values[17][7][0] =  24; Phi_h_Bin_Values[17][7][1] = 144; Phi_h_Bin_Values[17][7][2] = 9897;
z_pT_Bin_Borders[17][8][0] = 0.35; z_pT_Bin_Borders[17][8][1] = 0.29; z_pT_Bin_Borders[17][8][2] = 0.28; z_pT_Bin_Borders[17][8][3] = 0.19;
Phi_h_Bin_Values[17][8][0] =  24; Phi_h_Bin_Values[17][8][1] = 168; Phi_h_Bin_Values[17][8][2] = 9921;
z_pT_Bin_Borders[17][9][0] = 0.35; z_pT_Bin_Borders[17][9][1] = 0.29; z_pT_Bin_Borders[17][9][2] = 0.37; z_pT_Bin_Borders[17][9][3] = 0.28;
Phi_h_Bin_Values[17][9][0] =  24; Phi_h_Bin_Values[17][9][1] = 192; Phi_h_Bin_Values[17][9][2] = 9945;
z_pT_Bin_Borders[17][10][0] = 0.45; z_pT_Bin_Borders[17][10][1] = 0.35; z_pT_Bin_Borders[17][10][2] = 0.19; z_pT_Bin_Borders[17][10][3] = 0.05;
Phi_h_Bin_Values[17][10][0] =  24; Phi_h_Bin_Values[17][10][1] = 216; Phi_h_Bin_Values[17][10][2] = 9969;
z_pT_Bin_Borders[17][11][0] = 0.45; z_pT_Bin_Borders[17][11][1] = 0.35; z_pT_Bin_Borders[17][11][2] = 0.28; z_pT_Bin_Borders[17][11][3] = 0.19;
Phi_h_Bin_Values[17][11][0] =  1; Phi_h_Bin_Values[17][11][1] = 240; Phi_h_Bin_Values[17][11][2] = 9993;
z_pT_Bin_Borders[17][12][0] = 0.45; z_pT_Bin_Borders[17][12][1] = 0.35; z_pT_Bin_Borders[17][12][2] = 0.37; z_pT_Bin_Borders[17][12][3] = 0.28;
Phi_h_Bin_Values[17][12][0] =  1; Phi_h_Bin_Values[17][12][1] = 241; Phi_h_Bin_Values[17][12][2] = 9994;
z_pT_Bin_Borders[17][13][0] = 0.19; z_pT_Bin_Borders[17][13][1] = 0; z_pT_Bin_Borders[17][13][2] = 0.05; z_pT_Bin_Borders[17][13][3] = 0;
Phi_h_Bin_Values[17][13][0] =  1; Phi_h_Bin_Values[17][13][1] = 242; Phi_h_Bin_Values[17][13][2] = 9995;
z_pT_Bin_Borders[17][14][0] = 0.19; z_pT_Bin_Borders[17][14][1] = 0; z_pT_Bin_Borders[17][14][2] = 0.05; z_pT_Bin_Borders[17][14][3] = 0.19;
Phi_h_Bin_Values[17][14][0] =  1; Phi_h_Bin_Values[17][14][1] = 243; Phi_h_Bin_Values[17][14][2] = 9996;
z_pT_Bin_Borders[17][15][0] = 0.19; z_pT_Bin_Borders[17][15][1] = 0; z_pT_Bin_Borders[17][15][2] = 0.19; z_pT_Bin_Borders[17][15][3] = 0.28;
Phi_h_Bin_Values[17][15][0] =  1; Phi_h_Bin_Values[17][15][1] = 244; Phi_h_Bin_Values[17][15][2] = 9997;
z_pT_Bin_Borders[17][16][0] = 0.19; z_pT_Bin_Borders[17][16][1] = 0; z_pT_Bin_Borders[17][16][2] = 0.28; z_pT_Bin_Borders[17][16][3] = 0.37;
Phi_h_Bin_Values[17][16][0] =  1; Phi_h_Bin_Values[17][16][1] = 245; Phi_h_Bin_Values[17][16][2] = 9998;
z_pT_Bin_Borders[17][17][0] = 0.19; z_pT_Bin_Borders[17][17][1] = 0; z_pT_Bin_Borders[17][17][2] = 10; z_pT_Bin_Borders[17][17][3] = 0.37;
Phi_h_Bin_Values[17][17][0] =  1; Phi_h_Bin_Values[17][17][1] = 246; Phi_h_Bin_Values[17][17][2] = 9999;
z_pT_Bin_Borders[17][18][0] = 0.19; z_pT_Bin_Borders[17][18][1] = 0.23; z_pT_Bin_Borders[17][18][2] = 0.05; z_pT_Bin_Borders[17][18][3] = 0;
Phi_h_Bin_Values[17][18][0] =  1; Phi_h_Bin_Values[17][18][1] = 247; Phi_h_Bin_Values[17][18][2] = 10000;
z_pT_Bin_Borders[17][19][0] = 0.19; z_pT_Bin_Borders[17][19][1] = 0.23; z_pT_Bin_Borders[17][19][2] = 10; z_pT_Bin_Borders[17][19][3] = 0.37;
Phi_h_Bin_Values[17][19][0] =  1; Phi_h_Bin_Values[17][19][1] = 248; Phi_h_Bin_Values[17][19][2] = 10001;
z_pT_Bin_Borders[17][20][0] = 0.23; z_pT_Bin_Borders[17][20][1] = 0.29; z_pT_Bin_Borders[17][20][2] = 0.05; z_pT_Bin_Borders[17][20][3] = 0;
Phi_h_Bin_Values[17][20][0] =  1; Phi_h_Bin_Values[17][20][1] = 249; Phi_h_Bin_Values[17][20][2] = 10002;
z_pT_Bin_Borders[17][21][0] = 0.23; z_pT_Bin_Borders[17][21][1] = 0.29; z_pT_Bin_Borders[17][21][2] = 10; z_pT_Bin_Borders[17][21][3] = 0.37;
Phi_h_Bin_Values[17][21][0] =  1; Phi_h_Bin_Values[17][21][1] = 250; Phi_h_Bin_Values[17][21][2] = 10003;
z_pT_Bin_Borders[17][22][0] = 0.29; z_pT_Bin_Borders[17][22][1] = 0.35; z_pT_Bin_Borders[17][22][2] = 0.05; z_pT_Bin_Borders[17][22][3] = 0;
Phi_h_Bin_Values[17][22][0] =  1; Phi_h_Bin_Values[17][22][1] = 251; Phi_h_Bin_Values[17][22][2] = 10004;
z_pT_Bin_Borders[17][23][0] = 0.29; z_pT_Bin_Borders[17][23][1] = 0.35; z_pT_Bin_Borders[17][23][2] = 10; z_pT_Bin_Borders[17][23][3] = 0.37;
Phi_h_Bin_Values[17][23][0] =  1; Phi_h_Bin_Values[17][23][1] = 252; Phi_h_Bin_Values[17][23][2] = 10005;
z_pT_Bin_Borders[17][24][0] = 0.35; z_pT_Bin_Borders[17][24][1] = 0.45; z_pT_Bin_Borders[17][24][2] = 0.05; z_pT_Bin_Borders[17][24][3] = 0;
Phi_h_Bin_Values[17][24][0] =  1; Phi_h_Bin_Values[17][24][1] = 253; Phi_h_Bin_Values[17][24][2] = 10006;
z_pT_Bin_Borders[17][25][0] = 0.35; z_pT_Bin_Borders[17][25][1] = 0.45; z_pT_Bin_Borders[17][25][2] = 10; z_pT_Bin_Borders[17][25][3] = 0.37;
Phi_h_Bin_Values[17][25][0] =  1; Phi_h_Bin_Values[17][25][1] = 254; Phi_h_Bin_Values[17][25][2] = 10007;
z_pT_Bin_Borders[17][26][0] = 10; z_pT_Bin_Borders[17][26][1] = 0.45; z_pT_Bin_Borders[17][26][2] = 0; z_pT_Bin_Borders[17][26][3] = 0.05;
Phi_h_Bin_Values[17][26][0] =  1; Phi_h_Bin_Values[17][26][1] = 255; Phi_h_Bin_Values[17][26][2] = 10008;
z_pT_Bin_Borders[17][27][0] = 10; z_pT_Bin_Borders[17][27][1] = 0.45; z_pT_Bin_Borders[17][27][2] = 0.05; z_pT_Bin_Borders[17][27][3] = 0.19;
Phi_h_Bin_Values[17][27][0] =  1; Phi_h_Bin_Values[17][27][1] = 256; Phi_h_Bin_Values[17][27][2] = 10009;
z_pT_Bin_Borders[17][28][0] = 10; z_pT_Bin_Borders[17][28][1] = 0.45; z_pT_Bin_Borders[17][28][2] = 0.19; z_pT_Bin_Borders[17][28][3] = 0.28;
Phi_h_Bin_Values[17][28][0] =  1; Phi_h_Bin_Values[17][28][1] = 257; Phi_h_Bin_Values[17][28][2] = 10010;
z_pT_Bin_Borders[17][29][0] = 10; z_pT_Bin_Borders[17][29][1] = 0.45; z_pT_Bin_Borders[17][29][2] = 0.28; z_pT_Bin_Borders[17][29][3] = 0.37;
Phi_h_Bin_Values[17][29][0] =  1; Phi_h_Bin_Values[17][29][1] = 258; Phi_h_Bin_Values[17][29][2] = 10011;
z_pT_Bin_Borders[17][30][0] = 10; z_pT_Bin_Borders[17][30][1] = 0.45; z_pT_Bin_Borders[17][30][2] = 10; z_pT_Bin_Borders[17][30][3] = 0.37;
Phi_h_Bin_Values[17][30][0] =  1; Phi_h_Bin_Values[17][30][1] = 259; Phi_h_Bin_Values[17][30][2] = 10012;
Phi_h_Bin_Values[18][1][0] = 1; Phi_h_Bin_Values[18][1][1] = 1; Phi_h_Bin_Values[18][1][2] = 10013;
Phi_h_Bin_Values[19][1][0] = 1; Phi_h_Bin_Values[19][1][1] = 1; Phi_h_Bin_Values[19][1][2] = 10014;
Phi_h_Bin_Values[20][1][0] = 1; Phi_h_Bin_Values[20][1][1] = 1; Phi_h_Bin_Values[20][1][2] = 10015;
Phi_h_Bin_Values[21][1][0] = 1; Phi_h_Bin_Values[21][1][1] = 1; Phi_h_Bin_Values[21][1][2] = 10016;
Phi_h_Bin_Values[22][1][0] = 1; Phi_h_Bin_Values[22][1][1] = 1; Phi_h_Bin_Values[22][1][2] = 10017;
Phi_h_Bin_Values[23][1][0] = 1; Phi_h_Bin_Values[23][1][1] = 1; Phi_h_Bin_Values[23][1][2] = 10018;
Phi_h_Bin_Values[24][1][0] = 1; Phi_h_Bin_Values[24][1][1] = 1; Phi_h_Bin_Values[24][1][2] = 10019;
Phi_h_Bin_Values[25][1][0] = 1; Phi_h_Bin_Values[25][1][1] = 1; Phi_h_Bin_Values[25][1][2] = 10020;
Phi_h_Bin_Values[26][1][0] = 1; Phi_h_Bin_Values[26][1][1] = 1; Phi_h_Bin_Values[26][1][2] = 10021;
Phi_h_Bin_Values[27][1][0] = 1; Phi_h_Bin_Values[27][1][1] = 1; Phi_h_Bin_Values[27][1][2] = 10022;
Phi_h_Bin_Values[28][1][0] = 1; Phi_h_Bin_Values[28][1][1] = 1; Phi_h_Bin_Values[28][1][2] = 10023;
Phi_h_Bin_Values[29][1][0] = 1; Phi_h_Bin_Values[29][1][1] = 1; Phi_h_Bin_Values[29][1][2] = 10024;
Phi_h_Bin_Values[30][1][0] = 1; Phi_h_Bin_Values[30][1][1] = 1; Phi_h_Bin_Values[30][1][2] = 10025;
Phi_h_Bin_Values[31][1][0] = 1; Phi_h_Bin_Values[31][1][1] = 1; Phi_h_Bin_Values[31][1][2] = 10026;
Phi_h_Bin_Values[32][1][0] = 1; Phi_h_Bin_Values[32][1][1] = 1; Phi_h_Bin_Values[32][1][2] = 10027;
Phi_h_Bin_Values[33][1][0] = 1; Phi_h_Bin_Values[33][1][1] = 1; Phi_h_Bin_Values[33][1][2] = 10028;
Phi_h_Bin_Values[34][1][0] = 1; Phi_h_Bin_Values[34][1][1] = 1; Phi_h_Bin_Values[34][1][2] = 10029;
Phi_h_Bin_Values[35][1][0] = 1; Phi_h_Bin_Values[35][1][1] = 1; Phi_h_Bin_Values[35][1][2] = 10030;
Phi_h_Bin_Values[36][1][0] = 1; Phi_h_Bin_Values[36][1][1] = 1; Phi_h_Bin_Values[36][1][2] = 10031;
Phi_h_Bin_Values[37][1][0] = 1; Phi_h_Bin_Values[37][1][1] = 1; Phi_h_Bin_Values[37][1][2] = 10032;
Phi_h_Bin_Values[38][1][0] = 1; Phi_h_Bin_Values[38][1][1] = 1; Phi_h_Bin_Values[38][1][2] = 10033;
Phi_h_Bin_Values[39][1][0] = 1; Phi_h_Bin_Values[39][1][1] = 1; Phi_h_Bin_Values[39][1][2] = 10034;
auto Find_z_pT_Bin = [&](int Q2_y_Bin_Num_Value, double Z_Value, double PT_Value){
    int z_pT_Bin_Max = 1;
    if(Q2_y_Bin_Num_Value == 1){z_pT_Bin_Max = 63;}
    if(Q2_y_Bin_Num_Value == 2){z_pT_Bin_Max = 64;}
    if(Q2_y_Bin_Num_Value == 3){z_pT_Bin_Max = 48;}
    if(Q2_y_Bin_Num_Value == 4){z_pT_Bin_Max = 49;}
    if(Q2_y_Bin_Num_Value == 5){z_pT_Bin_Max = 64;}
    if(Q2_y_Bin_Num_Value == 6){z_pT_Bin_Max = 56;}
    if(Q2_y_Bin_Num_Value == 7){z_pT_Bin_Max = 56;}
    if(Q2_y_Bin_Num_Value == 8){z_pT_Bin_Max = 48;}
    if(Q2_y_Bin_Num_Value == 9){z_pT_Bin_Max = 63;}
    if(Q2_y_Bin_Num_Value == 10){z_pT_Bin_Max = 64;}
    if(Q2_y_Bin_Num_Value == 11){z_pT_Bin_Max = 49;}
    if(Q2_y_Bin_Num_Value == 12){z_pT_Bin_Max = 30;}
    if(Q2_y_Bin_Num_Value == 13){z_pT_Bin_Max = 56;}
    if(Q2_y_Bin_Num_Value == 14){z_pT_Bin_Max = 64;}
    if(Q2_y_Bin_Num_Value == 15){z_pT_Bin_Max = 30;}
    if(Q2_y_Bin_Num_Value == 16){z_pT_Bin_Max = 48;}
    if(Q2_y_Bin_Num_Value == 17){z_pT_Bin_Max = 30;}
    if(Q2_y_Bin_Num_Value < 1 || Q2_y_Bin_Num_Value > 17){return 1;}
    float z_max  = 0;
    float z_min  = 0;
    float pT_max = 0;
    float pT_min = 0;
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
    if(Num_PHI_BINS <= 1){return Num_PHI_BINS;}
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



