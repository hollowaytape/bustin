## Intro
* Text is at CLM:BIN:0x3180, plain SJIS.
* Accepts ASCII just fine.

## Game
* Can't find any of the dialogue in memory. 
	* At 0x1ac90, the pattern "01 21 02 22 03 23..." is a bunch of things fed to the a9 font table port. (outsb)
		* EBX holds the normal SJIS value of the character that gets printed. Where does that get set?
		* Why does it read from another big mess around 0x34360? Is this some kind of dictionary?
			* Anything LZ-ish happening here? There are ff fe, fd fe, 5e ff, etc. tags every now and then.
			* This appears to be some segment of SEN013R.MCV. (5efdfe022cd347 is at SEN013R.MCV:421)
			* When it reads from that place, some branches on that value:
				* (This is all around 079f:8615)
				* !IMPORTANT! First you xor the value with 0xff. So the 05 read becomes fa. (2d before became d2, which was encoded as 82df)
				* 00: Return immediately
				* < 16: 8668
					* xor ah, ah; xchg al, ah
						* 00-0f: 8676
							* (which just returns)
						* 10-16:
							* lodsb; xor al, ff; jmp 8676 (which returns)
				* 16-1f: 85ce
					* (see below)
				* 20-7f: 861f
					* Jump to more comparisons
						* 20-2f: 8643
							* sub al, 20; mov bx, 420e; jmp 865d (xor ah, ah; add bx, ax; mov al, es:[bx]; mov ah, 81; jmp 8676 (which returns))
								 * bx becomes 00-0f. ax becomes 81 __ :
								 	* 40 49 68 94 90 93 95 66 69 6a 96 7b 41 7c 44 5e
								 	* sp !  ”  #  $  %  &  ’  (  )  *  +  、  -  .  /
						* 30-39: (863d)
							* add al, 1f; mov ah, 82; jmp 8676 (which returns)
								* ax becomes 824f-8258 (numbers)
						* 3a-40: 864a
							* sub al, 3a; mov bx, 421e; jmp 865d
								* bx becomes 00-06. ax becomes 81 __ :
									* 46 47 83 81 84 48 97
									* :  ;  <  =  >  ?  @
						* 41-5a: (863d)
							* add al, 1f; mov ah, 82; jmp 8676 (which returns)
								* ax becomes 8260-8279 (fullwidth Latin capitals)
						* 5b-60: 8651
							* sub al, 5b; mov bx, 4225; jmp 865d
								* bx becomes 00-05. ax becomes 81 __ :
									* 6d 8f 6e 4f 51 65
									* [ ￥  ]  ^  _  ‘
						* 61-7a: 863d
							* ax becomes 8280-8299 (fullwidth Latin lowercase)
						* 7b-7f: 8658
							* sub al, 7b; mov bx, 422b; etc
								* ax becomes 81 __ :
									* 6f 62 70 60 40
									* {  ‖  }  ~  sp
				* 80-9f: 8618
					* mov ah, al; lodsb; xor al, ff; 
						* Normal SJIS, but 2nd byte is bit-flipped
				* a0-e0: 85ce
					* (see below)
				* e0-ef: 8618
					* (mov ah, al; lodsb; xor al, ff;)
						* Normal SJIS, but 2nd byte is bit-flipped
				* (16-1f, a0-e0, f0-ff):
					* mov ah, 82; push bx; xor bh, bh; mov bl, al;
						* bl == b0: 85f5
							* mov al, 5b; dec ah; return;
								* ax is 815b (ー)
						* bl <= 1f: 8603
							* sub bl, 16; mov al, es:[bx+427c]
								* bx is 00-09, ax is 82 __ :
								* ce d1 d4 d7 da cf d2 d5 d8 db
								* ば び  ぶ べ  ぼ ぱ ぴ  ぷ  ぺ ぽ (ba bi bu be bo, pa pi pu pe po)
						* bl >= f0: 85f9
							* sub bl, f0; mov al, es:[bx+426d]
								* bx is 00-0f, ax is 82 __ :
									* aa ac ae b0 b2 b4 b6 b8 ba bc be c0 c3 c5 c7 ce
									* が  ぎ ぐ げ  ご  ざ  じ ず  ぜ  ぞ だ  ぢ づ  で ど
						* bl >= a6: 860d
							* sub bl, a6; mov al, es:[bx+4236]
								* 9f a1 a3 a5 a7 e1 e3 e5 c1 00 a0 a2 a4 a6 a8 a9 ab ad af b1 b3 b5 b7 b9 bb bd bf c2 c4 c6 c8 c9 ca cb cc cd d0 d3 d6 d9 dc dd de df e0 e2 e4 e6 e7 e8 e9 ea eb ed f1...
								* ぁ ぃ ぅ ぇ ぉ ゃ ゅ ょ っ _ あ い う え お...
						* else (a0 <= bl <= a5): 
							* sub bl, a0; mov al, es:[bx+422f]
								* bx is 00-05, ax is 81 __ :
									* 40 42 75 76 41 45
									* sp 。   「 」  、  ・
								* This returns.

	* Flipped all the bits of SEN000A.MCV. Parwsing:
		* AVM 存 91-0f (oops, that's not a real SJIS value)

	* The results get stored at 0x1acb0 onward, which get put directly into VRAM.
	* Looking at the file SEN000A.SCV which gets loaded at 0x2f2e0:
		* b6, 09 (offset of beginning), c2 79 00 a8 a0 01 01 a4 a0 01 01 a4
		* Jumps to start reading c2.
			* Compare to a0, b0, b6, ba, bc, c2
			* If it's not any of those, jmp 8a57 -> 8a69 (misaligned place, weird)

	* ko no u su = 82 b1, 82 cc, 82 a4, 82 b7



* Replaced "miru" with "Look". Only wants to display the first ascii letter.

* TLDR: The bytes get transformed into various punctuation/numbers through a sort of GLodia TOS-type spec. The table is in either MPM.BIN or TBS.EXE.

0000 0100
0000 0010