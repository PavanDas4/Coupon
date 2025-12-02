import pandas as pd
import qrcode
from PIL import Image, ImageDraw, ImageFont
import os

csv_path = 'ticket.csv'  
df = pd.read_csv(csv_path, header=None) 

output_folder = 'ticket'
os.makedirs(output_folder, exist_ok=True)

qr_width = 210
qr_height = 210
qr_x_offset = 0  
qr_y_offset = 0  

for index, qr_data in enumerate(df.iloc[:, 0]):  
    
    qr = qrcode.QRCode(box_size=10, border=2)
    qr.add_data(str(qr_data))
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color="blue", back_color="white").convert("RGB")
    
    qr_image = qr_image.resize((qr_width, qr_height))
    
    draw = ImageDraw.Draw(qr_image)
    try:
        font = ImageFont.truetype("arial.ttf", 18)
    except:
        font = ImageFont.load_default()
    text = str(qr_data)
    
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = (qr_width - text_width) // 2
    text_y = -5
    
    draw.rectangle(
        [text_x - 5, text_y - 5, text_x + text_width + 5, text_y + text_height + 5],
        fill="white"
    )
    draw.text((text_x, text_y), text, fill="blue", font=font)
    
    ticket_path = 'Ticket.png'
    ticket = Image.open(ticket_path)

    # Get ticket and QR sizes
    ticket_width, ticket_height = ticket.size
    qr_width, qr_height = qr_image.size

    # Calculate QR position: place at top-left of white area (right side)
    # Assume white area starts at 2/3 of ticket width
    white_x = 485

    # Center QR vertically in white area
    white_height = ticket_height
    qr_y = (white_height - qr_height) // 2
    qr_x = white_x + 10  # 10px padding from left edge of white area

    # Paste QR code
    ticket.paste(qr_image, (qr_x, qr_y + 10))
    
    output_path = os.path.join(output_folder, f'{qr_data}.png')
    ticket.save(output_path)