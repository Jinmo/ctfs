data=open('matryoshka.jpg','rb').read()
open('flag.jpg','wb').write(data[data.rfind('\xff\xd8'):data.find('\xff\xd9')+2])