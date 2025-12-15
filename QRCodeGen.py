import qrcode

# Create CLOAK_ON QR Code
qr_on = qrcode.QRCode(version=1, box_size=10, border=5)
qr_on.add_data('CLOAK_ON')
qr_on.make(fit=True)
img_on = qr_on.make_image(fill_color="black", back_color="white")
img_on.save('cloak_on.png')
print("✓ Created: cloak_on.png")

# Create CLOAK_OFF QR Code
qr_off = qrcode.QRCode(version=1, box_size=10, border=5)
qr_off.add_data('CLOAK_OFF')
qr_off.make(fit=True)
img_off = qr_off.make_image(fill_color="black", back_color="white")
img_off.save('cloak_off.png')
print("✓ Created: cloak_off.png")

# Create TOGGLE QR Code
qr_toggle = qrcode.QRCode(version=1, box_size=10, border=5)
qr_toggle.add_data('TOGGLE')
qr_toggle.make(fit=True)
img_toggle = qr_toggle.make_image(fill_color="black", back_color="white")
img_toggle.save('toggle.png')
print("✓ Created: toggle.png")

print("\n✅ All QR codes generated successfully!")
print("Files saved: cloak_on.png, cloak_off.png, toggle.png")
