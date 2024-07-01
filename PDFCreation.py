# This script is to automate PDF creation for GeoComm customers that request PDFs

import arcpy
import os

# Set the map document and parameters
aprx = arcpy.mp.ArcGISProject("CURRENT")
layout_name = arcpy.GetParameterAsText(0)
title_text = arcpy.GetParameterAsText(1)
floor_text = arcpy.GetParameterAsText(2)
address_text = arcpy.GetParameterAsText(3)
creationDate_text = arcpy.GetParameterAsText(4)
output_pdf = arcpy.GetParameterAsText(5)

# Access the layout
layout = aprx.listLayouts(layout_name)[0]

# Modify layout elements
for text_element in layout.listElements('TEXT_ELEMENT'):
    if text_element.name == 'Title':
        text_element.text = title_text
        text_element.elementPositionX = 4.2741
        text_element.elementPositionY = 10.3447
    elif text_element.name == 'Floor Number':
        text_element.text = floor_text
        text_element.elementPositionX = 2.9725
        text_element.elementPositionY = 10.0933
    elif text_element.name == 'Address':
        text_element.text = address_text
        text_element.elementPositionX = 2.9725
        text_element.elementPositionY = 9.9256 
    elif text_element.name == 'PDF Creation Date':
        text_element.text = (f'PDF Creation Date:' + " " + creationDate_text)
        text_element.elementPositionX = 2.9725
        text_element.elementPositionY = 9.758



# Export the layout to PDF
layout.exportToPDF(output_pdf)


if not arcpy.Exists(output_pdf):
    arcpy.AddMessage(f'PDF file created at: {output_pdf}')
else:
    arcpy.AddWarning(f'Failed to create PDF at: {output_pdf}')
