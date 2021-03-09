lines="""
A = mem[8]
if (A == 4127179254) goto 0142 # 0104
if (A == 1933881070) goto 0126 # 0105
if (A == 4255576062) goto 0138 # 0106
if (A == 1670347938) goto 0118 # 0107
if (A == 2720551936) goto 0124 # 0108
if (A == 2307981054) goto 0136 # 0109
if (A == 2673307092) goto 0140 # 0110
if (A == 4139379682) goto 0122 # 0111
if (A == 4192373742) goto 0128 # 0112
if (A == 530288564) goto 0134 # 0113
if (A == 4025255646) goto 0144 # 0114
if (A == 3747612986) goto 0130 # 0115
if (A == 3098492862) goto 0120 # 0116
if (A == 2130820044) goto 0132 # 0117

A = mem[9] # 0118
if (A == 4056898606) goto 0170 else goto 0204 # 0119
A = mem[9] # 0120
if (A == 3064954302) goto 0154 else goto 0204 # 0121
A = mem[9] # 0122
if (A == 3602496994) goto 0148 else goto 0204 # 0123
A = mem[9] # 0124
if (A == 1627051272) goto 0160 else goto 0204 # 0125
A = mem[9] # 0126
if (A == 2002783966) goto 0162 else goto 0204 # 0127
A = mem[9] # 0128
if (A == 4088827598) goto 0158 else goto 0204 # 0129
A = mem[9] # 0130
if (A == 1340672294) goto 0168 else goto 0204 # 0131
A = mem[9] # 0132
if (A == 2115580844) goto 0146 else goto 0204 # 0133
A = mem[9] # 0134
if (A == 530288564) goto 0172 else goto 0204 # 0135
A = mem[9] # 0136
if (A == 3415533530) goto 0166 else goto 0204 # 0137
A = mem[9] # 0138
if (A == 3116543486) goto 0150 else goto 0204 # 0139
A = mem[9] # 0140
if (A == 251771212) goto 0156 else goto 0204 # 0141
A = mem[9] # 0142
if (A == 4126139894) goto 0164 else goto 0204 # 0143
A = mem[9] # 0144
if (A == 2813168974) goto 0152 else goto 0204 # 0145
A = mem[10] # 0146
if (A == 2130523044) goto 0194 else goto 0204 # 0147
A = mem[10] # 0148
if (A == 3606265306) goto 0186 else goto 0204 # 0149
A = mem[10] # 0150
if (A == 3151668710) goto 0190 else goto 0204 # 0151
A = mem[10] # 0152
if (A == 614968622) goto 0188 else goto 0204 # 0153
A = mem[10] # 0154
if (A == 3086875838) goto 0198 else goto 0204 # 0155
A = mem[10] # 0156
if (A == 251771212) goto 0174 else goto 0204 # 0157
A = mem[10] # 0158
if (A == 3015552726) goto 0178 else goto 0204 # 0159
A = mem[10] # 0160
if (A == 1627379644) goto 0196 else goto 0204 # 0161
A = mem[10] # 0162
if (A == 1601724370) goto 0176 else goto 0204 # 0163
A = mem[10] # 0164
if (A == 665780030) goto 0184 else goto 0204 # 0165
A = mem[10] # 0166
if (A == 3281895882) goto 0182 else goto 0204 # 0167
A = mem[10] # 0168
if (A == 1301225350) goto 0200 else goto 0204 # 0169
A = mem[10] # 0170
if (A == 2583645294) goto 0192 else goto 0204 # 0171
A = mem[10] # 0172
if (A == 3917315412) goto 0180 else goto 0204 # 0173
A = mem[11] # 0174
if (A == 2673307092) goto 0203 else goto 0204 # 0175
A = mem[11] # 0176
if (A == 1532821474) goto 0203 else goto 0204 # 0177
A = mem[11] # 0178
if (A == 3119098870) goto 0203 else goto 0204 # 0179
A = mem[11] # 0180
if (A == 3917315412) goto 0203 else goto 0204 # 0181
A = mem[11] # 0182
if (A == 2174343406) goto 0203 else goto 0204 # 0183
A = mem[11] # 0184
if (A == 666819390) goto 0203 else goto 0204 # 0185
A = mem[11] # 0186
if (A == 4143147994) goto 0203 else goto 0204 # 0187
A = mem[11] # 0188
if (A == 1827055294) goto 0203 else goto 0204 # 0189
A = mem[11] # 0190
if (A == 4290701286) goto 0203 else goto 0204 # 0191
A = mem[11] # 0192
if (A == 197094626) goto 0203 else goto 0204 # 0193
A = mem[11] # 0194
if (A == 2145762244) goto 0203 else goto 0204 # 0195
A = mem[11] # 0196
if (A == 2720880308) goto 0203 else goto 0204 # 0197
A = mem[11] # 0198
if (A == 3120414398) goto 0203 else goto 0204 # 0199
A = mem[11] # 0200
if (A == 3708166042) goto 0203 else goto 0204 # 0201
""".strip().split('\n')

mem = {}

for x in lines:
	if '#' in x:
		label = int(x.split('#')[1].strip())
	x = x.split('#')[0].strip()
	if x.startswith('A = '):
		prev = x[4:]
	elif x.startswith('if '):
		const = int(x.split(' == ')[1].split(')')[0])
		target = int(x.split('goto ')[1].split(' ')[0])
		label -= 1
		if label not in mem:
			assert prev == 'mem[8]', label
			mem[label] = []
		mem[target] = mem[label]
		mem[target].append((prev, (const)))
		if prev == 'mem[11]':
			print([x for name, x in mem[target]])
	elif x:
		print(x)
		exit()