import requests
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime

# Set up the API endpoint and API key
endpoint = 'https://api.data.gov.in/catalog/6141ea17-a69d-4713-b600-0a43c8fd9a6c'
api_key = 'YOUR_API_KEY'

# Set the parameters for the API request
params = {
    'api-key': api_key,
    'format': 'json',
    'filters[state]': 'Gujarat',
    'limit': '1000'
}

# Send the API request and retrieve the response
response = requests.get(endpoint, params=params)

# Parse the response as JSON
data = response.json()

# Create a new PDF document
buffer = BytesIO()

# Define the table data
data_rows = data['records']
data_table = [
    ["No.", "Commodity", "Market", "District", "Min Price", "Max Price", "Modal Price"]
]

for i, row in enumerate(data_rows, start=1):
    data_table.append([i, row['commodity'], row['market'], row['district'], float(row['min_price'])/5, float(row['max_price'])/5, float(row['modal_price'])/5])

# Define the table style
style = TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey ),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
    ('TOPPADDING', (0, 0), (-1, 0), 10),
    ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
    ('BACKGROUND', (0, 1), (-1, -1), '#D0E9C6'),
    ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
    ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 1), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ('LEFTPADDING', (0, 0), (-1, -1), 2),
    ('RIGHTPADDING', (0, 0), (-1, -1), 2),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Header row text color
    ('BACKGROUND', (0, 0), (-1, 0), '#0c4f18'),  # Header row background color
    ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),  # Header row line below
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header row font
])

# Create the table object
table = Table(data_table)

# Apply the table style
table.setStyle(style)

# Add the header row to each page
table.repeatRows = 1
table.repeatRowValues = data_table[:1]

# Set up the PDF document
filename = "prices.pdf"
pdf = SimpleDocTemplate(
    buffer, pagesize=letter, topMargin=0.3*inch, bottomMargin=0.3*inch,
    leftMargin=0.1*inch, rightMargin=0.1*inch
)

# Define the styles
styles = getSampleStyleSheet()
special_style = styles['Heading1']
special_style.alignment = 1

# Build the header
header = Paragraph(f"Date: {datetime.now().strftime('%d-%m-%Y')}", special_style)
footer = Paragraph("Thank You",special_style)
# Build the PDF document
pdf.build([header, table,footer])

# Move to the beginning of the buffer
buffer.seek(0)

# Save the PDF to a file
with open(filename, 'wb') as file:
    file.write(buffer.getvalue())

print(f"PDF created and saved as '{filename}' at {datetime.now()}")
