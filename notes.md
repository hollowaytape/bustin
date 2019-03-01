## Intro
* Text is at CLM.BIN:0x3180, plain SJIS.
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

* Halfwidth text in gameplay mode:
	* Load an 85 instead of 82 when it handles the fullwidth ascii.
		* TBS.EXE:e4e1: set to 85 (font table hack)
		* TBS.EXE:e41e: set to 02 (cursor hack)

* Replaced "miru" with "Look". Only wants to display the first ascii letter.

* TLDR: The bytes get transformed into various punctuation/numbers through a sort of GLodia TOS-type spec. The table is in either MPM.BIN or TBS.EXE.

0000 0100
0000 0010

* MEnu text hack
* 079f:d71c:

starting at mov ah, al, put this instead:
08c074f63c2072193c80720b3c9f76193ce0730be981ffb4829090eb099090
or al, al
jz d717
cmp al, 20
jb d73e
cmp al, 80
jb d734
cmp al, 9f
jbe d746
cmp al, e0
jnb d73c
jmp d6b5
mov ah, 82
nop
nop
jmp d743
nop
nop

Weird unexpected result? It gets outputted as halfwidth rather than fake fullwidth. Yay!

NEW: This code is also used to display MSGS text. So it gets output as fullwidth.
	What happens if I change it to 85?
		Fine in menus.
	But the offset is wrong. Need a way to add 0x1f-0x20 if it's displaying a MSG, and not if otherwise.
		Theory: BL == 80 when doing normal text, BL == bb when displaying a MSG
		ac 08c0 74f6 3c20 7219 b485 90 90 80fbbb 7515 0414 eb11
		lodsb
		or al, al
		jz d717
		cmp al, 20
		jb d73e
		mov ah, 85
		nop
		nop
		cmp bl, bb
		jnz d743
		add al, 1f
		(mroe conditions as needed)
		jmp d743

Menu text is TBS.EXE:11030
THat asm code is at TBS.EXE:e51d.


## CLX
* Beginning seems to have a big table of offsets. Since OPEN.CLX is a huge file, it is probably many images packed into one
	* First thing is offset, second thing is length. (2a 02 00 00 eb 00 00 00 = seg at offset 22a is 3a long, next begins at 315)

## GRP
* My immediate impression is that this might just be a bitmap-type thing. Lots of repeated FF FF FF's, no attempt at compressing repeated things, etc


## Pointers
* SO there's definitely a pointer to the first bit of text in SEN013R, and then the one after the room gets displayed.
	* First string, which is "5a 5a 5a 5a 5e fd fc": ESI value is 0xed
	* This loads only a part of SEN013R into that part in memory, from 0x421 to the end
	* Important values: 0x421, 0x00ed
		* Maybe these pointers are in the code in TBS.EXE? Check this out
* The next text that is displayed is actually from MSGS.001, at 0x3f37. (or MSGS.013, at 0xf4.)
	* And then the next text after she sits up is back at the next string in SEN013R. (0xd5e uncompressed, 0x281 compressed) (or maybe 0x280?)
		* 0x11a2 in TBS.EXE?
		* Doesn't appear to be any instances of 280 or 281...
* Alright. That next text's pointer value is 0x6a2 (0x281 + 0x421. So just take the compressed location, ignore the weird ESI value/0x421 fuckery) which is found at SEN013R.SCV:0x19e8.
	* 0e05 is also a value with a 16 prefix.
	* find_pointers.py should look for all things preceded by a016. (and maybe followed by a4)