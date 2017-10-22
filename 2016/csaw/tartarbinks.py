from hashlib import md5

flag = 'F5D1,4D6B,ED6A,08A6,38DD,F7FA,609E,EBC4,E55F,E6D1,7C89,ED5B,0871,1A69,5D58,72DE,224B,3AA6,0845,7DD6,58FB,E9CC,0A2D,76B8,ED60,251A,1F6B,32CC,E78D,12FA,201A,E889,2D25,922A,4BC5,F5FF,F8E5,C79B,3A77,4BDB,EA11,5941,58BD,3A95,F5C9,A225,AD40,F8BD,095D,70B6,458C,E7A9,EA68,252F,094B,5E41,0969,6015,5ED5,F6E5,59B9,7CAF,66DF,265B,7837,57B4,7CAF,AED9,F707,6A3C,F8E5,F509,7C8B,0915,2235,336F,33E9,2D14,7C91,5804,83E5,E78D,F4EA,0874,ED6B,4B35,E839,57B4,E77C,EA68,2525,AD41,ED6F,3A4A,4BCC,6015,F440,0858,3AA6,7809,671D,0874,EA77,63AF,2E91,5845,F6C4,086D,7795,3939,57B4,7C89,82DC,32ED,B994,C7AF,9135,0E65,1B66,ED5B,3235,6577,5A80,3AD3,E776,1EE5,AD41,ED59,864C,70B4,3876,ED67,64D6,F8E5,F505,EAD9,7C9C,32ED,B994,B4EF,0C6C,F665,F5F5,9047,521A,E99E,EA68,252F,9D09,76B7,E776,1ED0,095D,0D4D,5D5A,087B,2005,1526,7E76,85AD,78B9,E8B6,782C,251C,32ED,7F68,EBE3,EA41,57FD,ED59,846D,7A05,B994,BB78,ED6A,08A6,38DD,3B5D,7E45,E839,738C,E9CC,0A2D,764A,609E,E8B6,EA68,2524,E6BB,7C9C,639F,3A95,0895,F40F,8328,EA69,7EE5,F8BD,7F7D,0D6D,70B6,458C,E8B6,EA68,251C,6065,B35F,C789,5845,7F7D,6D89,4C6E,A20E,60B5,7E45,ED59,F707,69EF,922A,4BC5,F6EF,8635,F4B9,57B4,7CF8,ED60,2510,095D,20AF,3545,F40F,8328,EA41,58A4,225D,7E7C,4BDB,F8BD,082C,EAE7,5D57,5D50,0914,E7C7,8624,7CF8,ED60,2511,7C8E,7159,8416,7EF9,E7E5,774A,3895,1EC9,7C90,09B9,58BD,5FF5,E99E,EA68,250A,224C,EA3D,73F5,7C89,53A6,3190,3B5D,1526,7DD5,666A,0919,225F,CDEF,79E1,7E7B,7E6B,082C,A277,E885,E8BB,E775,5FF7,EA68,251B,7FDF,589D,7A05,779A,8A5A,7C91,5D5C,32ED,F628,2195,F49A,0C77,EAE1,59B9,58BD,E570,E99E,EA3D,73F9,13AD,2BF5,225D,7F7D,70B6,4A9C,337A,1EC9,4D05,7E75,2578,ED59,38E5,1ECA,A210,3B5D,779A,8A6F,C790,2518,4B41,7C89,5D49,4D05,152D,73C5,79F9,4BED,913C,37C9,5D4D,53C8,0941,7C97,5D5B,346A,82D8,5F36,801F,C800,'.split(',')[:-1]
flag = [int(x, 16) for x in flag]
flag = [(x % 40, (x // 40) % 40, (x // 40 // 40) % 40) for x in flag]
flag = reduce(lambda x, y: list(x) + list(y)[::-1], flag, [])

table = [0, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 32, 10, 0, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 40, 33, 64, 35, 44, 46, 63, 47, 42, 41, 60, 62, 0, 0]

shift = False
r = ''
for c in flag:
	if shift == True:
		r += chr(table[39 + c])
		shift = False
		continue
	if c == 39:
		shift = True
		continue
	elif c == 37:
		r += ' '
	else:
		r += chr(table[c])

r = r.strip('\x00')
# r = 'Milos Raonic (born 1990) is a Canadian professional tennis player. He reached a career-high world No. 4 singles ranking in May 2015, as ranked by the Association of Tennis Professionals (ATP). His career highlights include a Grand Slam final at the 2016 Wimbledon Championships and two Grand Slam semifinals at the 2014 Wimbledon Championships and 2016 Australian Open. He was the 2011 ATP Newcomer of the Year, and has been ranked continuously inside the top 20 since August 2012. Raonic is the first player born in the 1990s to win an ATP title, to be ranked in the top 10, and to qualify for the ATP World Tour Finals. He has eight ATP singles titles, all won on hard courts. He is frequently described as having one of the best serves among his contemporaries. Statistically, he is among the strongest servers in the Open Era, winning 91p of service games to rank third all-time. Aided by his serve, he plays an all-court style with an emphasis on short points.'

print `r`
print md5(r).hexdigest()