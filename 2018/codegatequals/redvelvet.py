from z3 import *
#----- (0000000000400986) ----------------------------------------------------

ss = Solver()

def iif(*x):
	ss.add(Not(Or(*x)))
def func1(a1, a2):

  iif  ( a1 * 2 * (a2 ^ a1) - a2 != 10858 )
    
  iif  ( a1 <= 85 , a1 > 95 , a2 <= 96 , a2 > 111 )
    
  

#----- (0000000000400A04) ----------------------------------------------------
def func2(a1, a2):

  iif  ( a1 % a2 != 7 )
    
  iif  ( a2 <= 90 )
    
  

#----- (0000000000400A53) ----------------------------------------------------
def func3(a1, a2):

  iif  ( a1 / a2 + (a2 ^ a1) != 21 , a1 > 99 , a2 > 119 )
    
  

#----- (0000000000400AAB) ----------------------------------------------------
def func4(a1, a2):

  v2 = (a2 ^ a1 ^ a2);
  iif( (v2 % a2) + a1 != 137 , a1 <= 115 , a2 > 99 , a2 != 95 )
  

#----- (0000000000400B0D) ----------------------------------------------------
def func5(a1, a2):

  iif  ( ((a2 + a1) ^ (a1 ^ a2 ^ a1)) != 225 , a1 <= 90 , a2 > 89 )
  

#----- (0000000000400B68) ----------------------------------------------------
def func6(a1, a2, a3):

  iif  ( a1 > a2 )
    
  iif  ( a2 > a3 )
    
  iif  ( a1 <= 85 , a2 <= 110 , a3 <= 115 , ((a2 + a3) ^ (a1 + a2)) != 44 , (a2 + a3) % a1 + a2 != 161 )
    
  

#----- (0000000000400C11) ----------------------------------------------------
def func7(a1, a2, a3):

  iif  ( a1 < a2 )
    
  iif  ( a2 < a3 )
    
  iif  ( a1 > 119 , a2 <= 90 , a3 > 89 , ((a1 + a3) ^ (a2 + a3)) != 122 , (a1 + a3) % a2 + a3 != 101 )
    
  

#----- (0000000000400CB7) ----------------------------------------------------
def func8(a1, a2, a3):

  iif  ( a1 > a2 )
    
  iif  ( a2 > a3 )
    
  iif  ( a3 > 114 , (a1 + a2) / a3 * a2 != 97 , (a3 ^ (a1 - a2)) * a2 != -10088 , a3 > 114 )
    
  

#----- (0000000000400D5D) ----------------------------------------------------
def func9(a1, a2, a3):

  iif  ( a1 != a2 )
    
  iif  ( a2 < a3 )
    
  iif  ( a3 > 99 , a3 + a1 * (a3 - a2) - a1 != -1443 )
    
  

#----- (0000000000400DE2) ----------------------------------------------------
def func10(a1, a2, a3):

  iif  ( a1 < a2 )
    
  iif  ( a2 < a3 )
    
  iif  ( a2 * (a1 + a3 + 1) - a3 != 15514 , a2 <= 90 , a2 > 99 )
    
  

#----- (0000000000400E6A) ----------------------------------------------------
def func11(a1, a2, a3):

  iif  ( a2 < a1 )
    
  iif  ( a1 < a3 )
    
  iif  ( a2 <= 100 , a2 > 104 , a1 + (a2 ^ (a2 - a3)) - a3 != 70 , (a2 + a3) / a1 + a1 != 68 )
    
  

#----- (0000000000400F13) ----------------------------------------------------
def func12(a1, a2, a3):

  iif  ( a1 < a2 )
    
  iif  ( a2 < a3 )
    
  iif  ( a2 > 59 , a3 > 44 , a1 + (a2 ^ (a3 + a2)) - a3 != 111 , (a2 ^ (a2 - a3)) + a2 != 101 )
    
  

#----- (0000000000400FB9) ----------------------------------------------------
def func13(a1, a2, a3):

  iif  ( a1 > a2 )
    
  iif  ( a2 > a3 )
    
  iif  ( a1 <= 40 , a2 <= 90 , a3 > 109 , a3 + (a2 ^ (a3 + a1)) - a1 != 269 , (a3 ^ (a2 - a1)) + a2 != 185 )
    
  

#----- (000000000040106B) ----------------------------------------------------
def func14(a1, a2, a3):

  iif  ( a1 < a3 )
    
  iif  ( a2 < a3 )
    
  iif  ( a2 > 99 , a3 <= 90 , a1 + (a2 ^ (a2 + a1)) - a3 != 185 )
    
  

#----- (00000000004010F5) ----------------------------------------------------
def func15(a1, a2, a3):

  iif  ( a2 < a3 )
    
  iif  ( a2 < a1 )
    
  iif  ( a3 <= 95 , a2 > 109 , ((a2 - a1) * a2 ^ a3) - a1 != 1214 , ((a3 - a2) * a3 ^ a1) + a2 != -1034 )
    
  
s = [BitVec('x[%d]' % i, 32) for i in range(26)]

func1(s[0], s[1]);
func2(s[1], s[2]);
func3(s[2], s[3]);
func4(s[3], s[4]);
func5(s[4], s[5]);
func6(s[5], s[6], s[7]);
func7(s[7], s[8], s[9]);
func8(s[9], s[10], s[11]);
func9(s[11], s[12], s[13]);
func10(s[13], s[14], s[15]);
func11(s[15], s[16], s[17]);
func12(s[17], s[18], s[19]);
func13(s[19], s[20], s[21]);
func14(s[21], s[22], s[23]);
func15(s[23], s[24], s[25]);

for x in s:
	ss.add(x & 0xff == x)

print ss.check()
print bytearray([ss.model()[s[i]].as_long() for i in range(26)])
while True:
	l = Or(*[ss.model()[s[i]] != s[i] for i in range(26)])
	ss.add(l)
	if ss.check() == unsat:
		break
	print bytearray([ss.model()[s[i]].as_long() for i in range(26)])
exit()