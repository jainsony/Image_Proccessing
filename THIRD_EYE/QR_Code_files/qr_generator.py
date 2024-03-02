import qrcode

img1 = qrcode.make('Hi abcdefghi jk lmno pqrsuvwxyz   zz aa bb cc  dd')
img2 = qrcode.make('test_qr_2')
img3 = qrcode.make('test_qr_3')
img4 = qrcode.make('test_qr_4')

print(type(img1))
print(img1.size)
# <class 'qrcode.image.pil.PilImage'>
# (290, 290)

img1.save('test_qr_1.png')
img2.save('test_qr_2.png')
img3.save('test_qr_3.png')
img4.save('test_qr_4.png')