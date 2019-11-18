
import base64
import os
import qrcode


# shortURL = base64.b64encode(os.urandom(5), b'ab').strip(b'=')

shortURL = 'aBmaO1k'
link = 'http://pacific-plateau-42582.herokuapp.com/rss/{}'.format(shortURL)
qr = qrcode.QRCode(version=1, box_size=10, border=4)
qr.add_data(link)
qr.make(fit=True)
img = qr.make_image(fill='black', back_color='RGB(52, 235, 222)')
name = '{}.png'.format(shortURL)
img.save('static/{}'.format(name))

print(name)
with open('static/{}'.format(name), "rb") as imageFile:
	# str = base64.b64encode(imageFile.read())
	str = base64.b64encode(imageFile.read())
	print(str)

