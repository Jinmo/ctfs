import json
import struct

# I guessed the protocol.
obj = json.load(open('dump/download.json'))
f = None
known = {}
for item in obj:
	udp = item['_source']['layers'].get('data')
	if udp is None:
		continue
	data = udp['data.data']
	data = data.replace(':' ,'').decode('hex')
	src, dst, size, cmd, ack, seq = struct.unpack(">HHHHHH", data[:12])
	if size != 0:
		payload = data[14:size+12]
		if len(data) == size + 14:
			print 'good',
		if payload.startswith('\x01\x00'):
			name = payload.split('\x00')[1]
			print 'File!', name
			f = open('extracted/' + name, 'wb')
		elif payload.startswith('\x15\x00'):
			print 'Directory!', payload.split('\x00')[1]
		elif payload.startswith('\xff\x00'):
			filedata = payload[10:]
			# Some data were retransmissioned, breaking some printable strings.
			# I put this check and the string were recovered.
			if data in known:
				print '???', `data`
				continue
			known[data] = 1
			f.write(filedata)
			print 'Data!', `filedata`
		else:
			print src, dst, `payload`