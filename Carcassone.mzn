include "globals.mzn";

/* Parameters */

int: TileNumber;
int: numOfRegularCards;
array[1..numOfRegularCards] of int: Cards;
int: numOfTypes;
enum oldTypes = {T,F,P,R};
enum Types = {FPTP,PFFF,PFFP,FFTF,FTTF,FTTT,PFTP,PPTF,PPFP,PPTP,PTTT,PPTT,FFFR,RRPP,RRTT,RPRT,RFRP,FFRR,FTFT,PFPF,RFRF,RPRP,RTRT,FFFF,TTTT,PPPP};

set of int: RegularCards = 1..numOfRegularCards;
set of int: TileN = 1..TileNumber;

array[RegularCards] of Types: Tiles;
array[RegularCards] of 1..4: RotationCount;
array[RegularCards, 1..4] of oldTypes: OldTiles;
%array[1..sum(RotationCount),1..4] of Types: RotationTable;


/* Decision variables */

array[1..7, 1..12] of var 1..84: Game;

array[TileN] of var Types: TileRotation;

array[TileN,1..4] of var oldTypes: TileRotation2;

array[RegularCards] of var 0..10: NumOfTypes;

%array[TileN] of var RegularCards: Map;

%array[1..TileNumber,1..numOfRegularCards] of var 0..1: Map;


/* Constraints */

constraint forall (i in RegularCards) (count(TileRotation,Tiles[i]) = Cards[i]);

constraint alldifferent(Game);

%constraint forall (i in RegularCards, j in TileN where Tiles[i] = TileRotation[j]) (Map[j] = i);

%constraint forall (i in TileN, j in RegularCards where Tiles[j] = TileRotation[i]) (Map[i,j] = 1);

constraint forall (i in TileN, j in RegularCards where Tiles[j] = TileRotation[i]) (TileRotation2[i,..] = OldTiles[j,..]);



%constraint forall (i in 1..12) (TileRotation2[Game[1,i],2] = F /\ TileRotation2[Game[7,i],4] = F); 

%constraint forall (i in 1..7) (TileRotation2[Game[i,1],1] = F /\ TileRotation2[Game[i,12],3] = F); 


%constraint forall (i in 1..7, j in 1..11) (TileRotation[Game[i,j],3] = TileRotation[Game[i,j+1],1]);

%constraint forall (i in 1..6, j in 1..12) (TileRotation[Game[i,j],4] = TileRotation[Game[i+1,j],2]);

%constraint forall (i in 1..TileNumber) (table(TileRotation[i,..],RotationTable));

%constraint forall (i in 24..26) (bin_packing(Cards[i],TileRotaion[..,

%constraint forall (i in 1..sum(RotationCount)) (count(TileRotation


%constraint forall (i in 1..numOfRegularCards, j in Types, k in 1..TileNumber) (count(Tiles[i,..],j) = count(TileRotation[k,..],j));

solve satisfy;

output[show(TileRotation)];


