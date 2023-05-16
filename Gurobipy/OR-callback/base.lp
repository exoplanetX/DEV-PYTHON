\ Model Master Problem
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  1000 slack[0] + 1000 slack[1] + 1000 slack[2] + 1000 slack[3]
   + 1000 slack[4] + 1000 slack[5] + 1000 slack[6] + 1000 slack[7]
   + 1000 slack[8] + 1000 slack[9] + 1000 slack[10] + 1000 slack[11]
   + 1000 slack[12] + 1000 slack[13] + 1000 slack[14] + 1000 slack[15]
   + 1000 slack[16] + 1000 slack[17] + 1000 slack[18] + 1000 slack[19]
   + 1000 slack[20] + 1000 slack[21] + 1000 slack[22] + 1000 slack[23]
   + 1000 slack[24] + 1000 slack[25] + 1000 slack[26] + 1000 slack[27]
   + 1000 slack[28] + 1000 slack[29] + 1000 slack[30] + 1000 slack[31]
   + 1000 slack[32] + 1000 slack[33] + 1000 slack[34] + 1000 slack[35]
   + 1000 slack[36] + 1000 slack[37] + 1000 slack[38] + 1000 slack[39]
   + 1000 slack[40] + 1000 slack[41] + 1000 slack[42] + 1000 slack[43]
   + 1000 slack[44] + 1000 slack[45] + 1000 slack[46] + 1000 slack[47]
   + 1000 slack[48] + 1000 slack[49] + C50 + C51 + C52 + C53 + C54 + C55
   + C56 + C57 + C58 + C59 + C60 + C61 + C62 + C63 + C64 + C65 + C66 + C67
   + C68 + C69 + C70 + C71 + C72 + C73 + C74 + C75 + C76 + C77 + C78 + C79
   + C80 + C81 + C82 + C83 + C84 + C85 + C86 + C87 + C88 + C89 + C90 + C91
   + C92 + C93 + C94 + C95 + C96 + C97 + C98 + C99
Subject To
 R0: slack[0] + 3 C50 >= 102
 R1: slack[1] + 5 C51 >= 36
 R2: slack[2] + 27 C52 >= 176
 R3: slack[3] + 4 C53 >= 32
 R4: slack[4] + 5 C54 >= 159
 R5: slack[5] + 4 C55 >= 118
 R6: slack[6] + 21 C56 >= 156
 R7: slack[7] + 16 C57 >= 92
 R8: slack[8] + 3 C58 >= 165
 R9: slack[9] + 13 C59 >= 30
 R10: slack[10] + 3 C60 >= 5
 R11: slack[11] + 3 C61 >= 44
 R12: slack[12] + 4 C62 >= 175
 R13: slack[13] + 4 C63 >= 190
 R14: slack[14] + 3 C64 >= 144
 R15: slack[15] + 3 C65 >= 21
 R16: slack[16] + 9 C66 >= 98
 R17: slack[17] + 3 C67 >= 123
 R18: slack[18] + 10 C68 >= 153
 R19: slack[19] + 75 C69 >= 39
 R20: slack[20] + 10 C50 + 7 C51 + 2 C52 + 6 C53 + 5 C54 + 2 C55 + C56
   + C57 + 11 C58 + 13 C60 + 10 C61 + 8 C62 + 10 C63 + 14 C64 + 2 C65
   + 4 C66 + 9 C67 + 3 C68 + 75 C70 + 13 C71 + 6 C73 + 5 C75 + 7 C76
   + 4 C77 + 3 C78 + 5 C79 + 8 C83 + 17 C84 + 13 C85 + 7 C86 + 10 C88
   + 9 C89 + 12 C90 + C91 + 2 C92 + C93 + 5 C95 + 9 C96 + 3 C97 + 10 C98
   + 3 C99 >= 32
 R21: slack[21] + 3 C71 >= 30
 R22: slack[22] + 14 C72 >= 102
 R23: slack[23] + 4 C73 >= 83
 R24: slack[24] + 8 C74 >= 83
 R25: slack[25] + 12 C75 >= 66
 R26: slack[26] + 3 C76 >= 9
 R27: slack[27] + 12 C77 >= 131
 R28: slack[28] + 6 C78 >= 196
 R29: slack[29] + 4 C79 >= 47
 R30: slack[30] + 12 C80 >= 90
 R31: slack[31] + 10 C81 >= 39
 R32: slack[32] + 39 C82 >= 167
 R33: slack[33] + 7 C83 >= 151
 R34: slack[34] + 3 C84 >= 38
 R35: slack[35] + 3 C85 >= 125
 R36: slack[36] + 7 C86 >= 8
 R37: slack[37] + 4 C87 >= 144
 R38: slack[38] + 3 C88 >= 176
 R39: slack[39] + 4 C89 >= 141
 R40: slack[40] + 5 C90 >= 51
 R41: slack[41] + 6 C91 >= 11
 R42: slack[42] + 26 C92 >= 154
 R43: slack[43] + 11 C93 >= 168
 R44: slack[44] + 53 C94 >= 161
 R45: slack[45] + 7 C95 >= 16
 R46: slack[46] + 6 C96 >= 130
 R47: slack[47] + 12 C97 >= 58
 R48: slack[48] + 3 C98 >= 153
 R49: slack[49] + 4 C99 >= 41
Bounds
End
