# uwp
The program is UWP based program, which is combination of .NET assemblies I think, and I was enable to analyze the routine with dnSpy.
 
The routine was simple: user gives the number, and the program does decryption with fixed key(which is from the bundle’s FamilyName), and shows it to the user.
 
I wrote a decryption program for whole rows in database (flag.sqlite), and found that one of them is the flag. (it contains “ROIS”)
