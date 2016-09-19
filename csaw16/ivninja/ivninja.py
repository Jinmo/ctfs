import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont

import math

im = Image.open('sample.png')
font = ImageFont.truetype("arial.ttf", 32)
draw = ImageDraw.Draw(im)

pi = 3.141592653589793

def get_exp_xy(i, color):
	width, height = im.size
	levelValue = (foundLevel + 1) * 2
	angle1 = (scalars[i] - scalars[0]) * 180 / (scalars[levelValue] - scalars[0]) * pi / 180
	cos = math.cos(angle1)
	sin = math.sin(angle1)
	_v1 = v1 = 475.0 - sin * 304 + 0
	v1 = int(v1)
	m = (width / 2.0) - cos * (width / 2.0 - 71)
	v2 = 5.0 + m
	v2 = int(v2)
	# print hex(v2), hex(v1)
	# print hex((v1 * width + v2) * 4)
	im.putpixel((v2, v1), color)
	for j in range(8):
		angle2 = (j + 1) * 45.0 * pi / 180.0
		cos = math.cos(angle2)
		sin = math.sin(angle2)
		v1 = sin * 5 + _v1
		v1 = int(v1)
		v2 = cos * 5 + m
		v2 = int(v2)
		# print ':', hex(v2), hex(v1)
		im.putpixel((v2, v1), color)

# struct
# defense 0
# stamina 8
# name 16
# v1 24
# v2 32
# v3 40

scalars = [0.09399999678134918, 0.13513743078430837, 0.16639786958694458, 0.1926509144568865, 0.21573247015476227, 0.23657265502662245, 0.2557200491428375, 0.273530381100769, 0.29024988412857056, 0.30605738133577315, 0.3210875988006592, 0.3354450322950772, 0.3492126762866974, 0.3624577487787902, 0.37523558735847473, 0.38759241108516856, 0.39956727623939514, 0.4111935495172506, 0.42250001430511475, 0.4329264134104144, 0.443107545375824, 0.4530599538719859, 0.4627983868122101, 0.47233607778670494, 0.48168495297431946, 0.49085581025900893, 0.49985843896865845, 0.5087017569439922, 0.517393946647644, 0.5259425087713293, 0.5343543291091919, 0.5426357622303539, 0.5507926940917969, 0.5588305994380878, 0.5667545199394226, 0.5745691480392641, 0.5822789072990417, 0.5898879119772721, 0.5974000096321106, 0.6048236575020739, 0.6121572852134705, 0.6194041105660502, 0.6265671253204346, 0.6336491816227439, 0.6406529545783997, 0.647580963301656, 0.6544356346130371, 0.661219263506722, 0.667934000492096, 0.6745818992908182, 0.6811649203300476, 0.6876849058877712, 0.6941436529159546, 0.7005428932779783, 0.7068842053413391, 0.7131691023333414, 0.719399094581604, 0.7255756169725988, 0.7317000031471252, 0.7347410111373763, 0.7377694845199585, 0.7407855745973265, 0.7437894344329834, 0.7467812087024829, 0.7497610449790955, 0.7527291053058215, 0.7556855082511902, 0.7586303665196846, 0.7615638375282288, 0.7644860652552267, 0.7673971652984619, 0.7702972739715901, 0.7731865048408508, 0.776064945942412, 0.7789327502250671, 0.781790064808426, 0.7846369743347168, 0.787473583646825, 0.7903000116348267, 0.7931164]
defenses = [126L, 158L, 200L, 108L, 140L, 182L, 142L, 176L, 222L, 66L, 86L, 144L, 64L, 82L, 130L, 90L, 90L, 122L, 166L, 86L, 150L, 78L, 146L, 112L, 166L, 108L, 154L, 114L, 172L, 104L, 136L, 190L, 94L, 128L, 170L, 124L, 178L, 118L, 194L, 54L, 108L, 90L, 164L, 130L, 158L, 190L, 120L, 170L, 118L, 154L, 86L, 140L, 94L, 146L, 112L, 176L, 96L, 150L, 110L, 180L, 98L, 132L, 202L, 76L, 112L, 152L, 96L, 144L, 180L, 78L, 110L, 152L, 136L, 196L, 118L, 156L, 198L, 138L, 170L, 110L, 198L, 138L, 180L, 132L, 96L, 150L, 138L, 192L, 110L, 188L, 112L, 196L, 82L, 118L, 156L, 186L, 140L, 196L, 110L, 168L, 124L, 174L, 132L, 164L, 150L, 202L, 172L, 204L, 160L, 142L, 198L, 116L, 160L, 60L, 152L, 178L, 100L, 150L, 126L, 160L, 128L, 192L, 196L, 180L, 134L, 160L, 158L, 186L, 184L, 84L, 196L, 190L, 110L, 128L, 168L, 168L, 174L, 174L, 178L, 178L, 158L, 160L, 202L, 142L, 190L, 162L, 180L, 242L, 194L, 194L, 110L, 152L, 212L, 202L, 220L, 210L]
attacks = [126L, 156L, 198L, 128L, 160L, 212L, 112L, 144L, 186L, 62L, 56L, 144L, 68L, 62L, 144L, 94L, 94L, 126L, 170L, 92L, 146L, 102L, 168L, 112L, 166L, 124L, 200L, 90L, 150L, 100L, 132L, 184L, 110L, 142L, 204L, 116L, 178L, 106L, 176L, 98L, 168L, 88L, 164L, 134L, 162L, 202L, 122L, 162L, 108L, 172L, 108L, 148L, 104L, 156L, 132L, 194L, 122L, 178L, 156L, 230L, 108L, 132L, 180L, 110L, 150L, 186L, 118L, 154L, 198L, 158L, 190L, 222L, 106L, 170L, 106L, 142L, 176L, 168L, 200L, 110L, 184L, 128L, 186L, 138L, 126L, 182L, 104L, 156L, 124L, 180L, 120L, 196L, 136L, 172L, 204L, 90L, 104L, 162L, 116L, 178L, 102L, 150L, 110L, 232L, 102L, 140L, 148L, 138L, 126L, 136L, 190L, 110L, 166L, 40L, 164L, 142L, 122L, 176L, 112L, 172L, 130L, 194L, 154L, 176L, 172L, 198L, 214L, 184L, 148L, 42L, 192L, 186L, 110L, 114L, 186L, 186L, 192L, 192L, 238L, 238L, 156L, 132L, 180L, 148L, 190L, 182L, 180L, 198L, 232L, 242L, 128L, 170L, 250L, 284L, 220L, 200L]
staminas = [90L, 120L, 160L, 78L, 116L, 156L, 88L, 118L, 158L, 90L, 100L, 120L, 80L, 90L, 130L, 80L, 80L, 126L, 166L, 60L, 110L, 80L, 130L, 70L, 120L, 70L, 120L, 100L, 150L, 110L, 140L, 180L, 92L, 122L, 162L, 140L, 190L, 76L, 146L, 230L, 280L, 80L, 150L, 90L, 120L, 150L, 70L, 120L, 120L, 140L, 20L, 70L, 80L, 130L, 100L, 160L, 80L, 130L, 110L, 180L, 80L, 130L, 180L, 50L, 80L, 110L, 140L, 160L, 180L, 100L, 130L, 160L, 80L, 160L, 80L, 110L, 160L, 100L, 130L, 180L, 190L, 50L, 100L, 104L, 70L, 120L, 130L, 180L, 160L, 210L, 60L, 100L, 60L, 90L, 120L, 70L, 120L, 170L, 60L, 110L, 80L, 120L, 120L, 190L, 100L, 120L, 100L, 100L, 180L, 80L, 130L, 160L, 210L, 500L, 130L, 210L, 60L, 110L, 90L, 160L, 60L, 120L, 80L, 140L, 130L, 130L, 130L, 130L, 150L, 40L, 190L, 260L, 96L, 110L, 260L, 260L, 130L, 130L, 130L, 130L, 130L, 70L, 140L, 60L, 120L, 160L, 320L, 180L, 180L, 180L, 82L, 122L, 182L, 212L, 200L, 194L]
names = ['Bulbasaur', 'Ivysaur', 'Venusaur', 'Charmander', 'Charmeleon', 'Charizard', 'Squirtle', 'Wartortle', 'Blastoise', 'Caterpie', 'Metapod', 'Butterfree', 'Weedle', 'Kakuna', 'Beedrill', 'Pidgey', 'Candy', 'Pidgeotto', 'Pidgeot', 'Rattata', 'Raticate', 'Spearow', 'Fearow', 'Ekans', 'Arbok', 'Pikachu', 'Raichu', 'Sandshrew', 'Sandslash', 'Nidoran?', 'Nidorina', 'Nidoqueen', 'Nidoranf', 'Nidorino', 'Nidoking', 'Clefairy', 'Clefable', 'Vulpix', 'Ninetales', 'Jigglypuff', 'Wigglytuff', 'Zubat', 'Golbat', 'Oddish', 'Gloom', 'Vileplume', 'Paras', 'Parasect', 'Venonat', 'Venomoth', 'Diglett', 'Dugtrio', 'Meowth', 'Persian', 'Psyduck', 'Golduck', 'Mankey', 'Primeape', 'Growlithe', 'Arcanine', 'Poliwag', 'Poliwhirl', 'Poliwrath', 'Abra', 'Kadabra', 'Alakazam', 'Machop', 'Machoke', 'Machamp', 'Bellsprout', 'Weepinbell', 'Victreebel', 'Tentacool', 'Tentacruel', 'Geodude', 'Graveler', 'Golem', 'Ponyta', 'Rapidash', 'Slowpoke', 'Slowbro', 'Magnemite', 'Magneton', "Farfetch'd", 'Doduo', 'Dodrio', 'Seel', 'Dewgong', 'Grimer', 'Muk', 'Shellder', 'Cloyster', 'Gastly', 'Haunter', 'Gengar', 'Onix', 'Drowzee', 'Hypno', 'Krabby', 'Kingler', 'Voltorb', 'Electrode', 'Exeggcute', 'Exeggutor', 'Cubone', 'Marowak', 'Hitmonlee', 'Hitmonchan', 'Lickitung', 'Koffing', 'Weezing', 'Rhyhorn', 'Rhydon', 'Chansey', 'Tangela', 'Kangaskhan', 'Horsea', 'Seadra', 'Goldeen', 'Seaking', 'Staryu', 'Starmie', 'Mr. Mime', 'Scyther', 'Jynx', 'Electabuzz', 'Magmar', 'Pinsir', 'Tauros', 'Magikarp', 'Gyarados', 'Lapras', 'Ditto', 'Eevee', 'Vaporeon', 'Rainer', 'Jolteon', 'Sparky', 'Flareon', 'Pyro', 'Porygon', 'Omanyte', 'Omastar', 'Kabuto', 'Kabutops', 'Aerodactyl', 'Snorlax', 'Articuno', 'Zapdos', 'Moltres', 'Dratini', 'Dragonair', 'Dragonite', 'Mewtwo', 'Mew', 'Bininja']

hp = 96
attack = 13
defense = 3
stamina = 7
sqrt = lambda x: pow(x, 0.5)
r16 = range(16)
for name, b_attack, b_defense, b_stamina in zip(names, attacks, defenses, staminas):
	if name not in ['Starmie', 'Bininja']:
		continue
	for exp, CPScalar in enumerate(scalars):
		found = []
		for attack in r16:
			for defense in r16:
				for stamina in r16:
					getCP = lambda attack, defense, stamina: (b_attack + attack) * sqrt(b_defense + defense) * sqrt(b_stamina + stamina) * (CPScalar**2) / 10
					CP = getCP(attack, defense, stamina)
			#			if name == 'Dragonite':
			#				print name, b_attack, CP
					CP = max(10, CP)
					CalculatedHP = (stamina + b_stamina) * CPScalar
					CalculatedHP = int(CalculatedHP)
					Perfection = CPScalar
					if int(CP) == 1337:
						found += [(attack, defense, stamina, CP)]
						if attack != 13 or defense != 3 or stamina != 7:
							continue
						print name, attack, defense, stamina, CalculatedHP, exp, CP, CPScalar
						print found
						print getCP(0, 0, 1)
						foundName = name
						foundLevel = exp / 2

						print sqrt(0x86)
						print (0x90*sqrt(0x82)*sqrt(0x86))*(CPScalar)**2/10
						draw.rectangle((303, 85, 466, 145), fill=0xFF000000)
						draw.rectangle((335, 707, 392, 735), fill=0xFFFFFFFF)
						draw.rectangle((405, 708, 464, 736), fill=0xFFFFFFFF)
						draw.rectangle((249, 599, 496, 657), fill=0xFFFFFFFF)
						draw.text((304, 90), str(int(CP)), fill=0xFFFFFFFF, font=font)
						draw.text((336, 707), str(CalculatedHP), fill=0xFF000000, font=font)
						draw.text((405, 708), str(CalculatedHP), fill=0xFF000000, font=font)
						draw.text((249, 599), foundName, fill=0xFF000000, font=font)

						for i in range(exp):
							# print 'yo', exp
							get_exp_xy(i, (0, 0, 0, 255))

						for i in range(50):
							for j in range(50):
								im.putpixel((i, j), (0xff, 0xff, 0xff, 0xff))

						get_exp_xy(exp, (255, 255, 255, 255))

						for i in range(exp + 1, foundLevel * 2 + 2):
							get_exp_xy(i, (0, 0, 0, 255))

						im.save('result.png')

						print 'trainer level', foundLevel