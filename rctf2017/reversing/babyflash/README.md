# baby flash
 
It’s CrossBridge-compiled swf file. I was new to reverse engineer this kind of binary, but I found that there’s “_main” routine, and “check” routine. All strings are in binaryData types. By searching and finding references by filename and classname, I was able to find the printed string’s usage (Try again, …).
 
The routine was simple: it does `strcmp(input, “RCTF{_Dyiin9__F1ash__1ike5_CPP}”)`, but the strcmp is biased.

`babyflash.py` is the ported and reversed version of strcmp in the binary.
