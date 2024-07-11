# This script is to automate PDF creation for GeoComm customers that request PDFs for arcgis 2.9

import arcpy
import os


# Set the project
aprx = arcpy.mp.ArcGISProject("CURRENT")


# Set the parameters
layout_file = arcpy.GetParameterAsText(0)
title_text = arcpy.GetParameterAsText(1)
floor_text = arcpy.GetParameterAsText(2)
address_text = arcpy.GetParameterAsText(3)
creationDate_text = arcpy.GetParameterAsText(4)
planType_text = arcpy.GetParameterAsText(5)
output_pdf = arcpy.GetParameterAsText(6)

distance_past_floorPlan = 50
distance_past_sitePlan = 5


try:
    # Access the layout
    layout = arcpy.mp.ConvertLayoutFileToLayout(layout_file)

    # Modify layout elements
    for text_element in layout.listElements('TEXT_ELEMENT'):
        if text_element.name == 'Title':
            text_element.text = title_text
            text_element.font = "Tahoma"
            text_element.fontSize = 20
            text_element.fontStyle = "Regular"
            # Center horizontally
            text_element.elementPositionX = 4.25 - (text_element.elementWidth / 2.0)
            text_element.elementPositionY = 10.5625
        elif text_element.name == 'Floor Number':
            text_element.text = floor_text
            text_element.font = "Tahoma"
            text_element.fontSize = 10
            text_element.fontStyle = "Regular"
            text_element.elementPositionX = 2.9725
            text_element.elementPositionY = 10.2522
        elif text_element.name == 'Address':
            text_element.text = address_text
            text_element.font = "Tahoma"
            text_element.fontSize = 10
            text_element.fontStyle = "Regular"
            text_element.elementPositionX = 2.9725
            text_element.elementPositionY = 10.0721 
        elif text_element.name == 'PDF Creation Date':
            text_element.text = (f'PDF Creation Date:' + " " + creationDate_text)
            text_element.font = "Tahoma"
            text_element.fontSize = 10
            text_element.elementPositionX = 2.9725
            text_element.elementPositionY = 9.9044
        elif text_element.name == 'Coordinates':
            text_element.elementPositionX = 8.0368
            text_element.elementPositionY = 0.8772
    
    # Map view for Floor Plan
    if planType_text == "Floor Plan":

        with arcpy.da.SearchCursor('levels', ['SHAPE@']) as cursor:
            for row in cursor:
                feature_geometry = row[0].extent

        # Calculate the new extent based on the feature's extent and distance past
        # Expand the feature's extent by adding the distance_past to its width and height
        new_extent = arcpy.Extent(
            feature_geometry.XMin - distance_past_floorPlan,
            feature_geometry.YMin - distance_past_floorPlan,
            feature_geometry.XMax + distance_past_floorPlan,
            feature_geometry.YMax + distance_past_floorPlan
        )


        # Set new extent for map frame
        for map_frame in layout.listElements('MAPFRAME_ELEMENT'):
            map_frame.camera.setExtent(new_extent)

    # Map view for Site Plan
    elif planType_text == "Site Plan":

        grid_layers = arcpy.ListFeatureClasses('*grid*')
        if not grid_layers:
            arcpy.AddError("No layers containing 'grid' found in the workspace.")

        # Use the first found grid layer
        grid_layer = grid_layers[0]
        
        # Find the extent of the grid layer
        desc = arcpy.Describe(grid_layer)
        feature_extent = desc.extent

        # Calculate the new extent based on the grid layer's extent and distance past
        new_extent = arcpy.Extent(
            feature_extent.XMin - distance_past_sitePlan,
            feature_extent.YMin - distance_past_sitePlan,
            feature_extent.XMax + distance_past_sitePlan,
            feature_extent.YMax + distance_past_sitePlan
        )
            
        # Set new extent for map frame
        for map_frame in layout.listElements('MAPFRAME_ELEMENT'):
            map_frame.camera.setExtent(new_extent)

    # Ensure output_pdf path is a valid PDF file path
    if not output_pdf.lower().endswith('.pdf'):
        output_pdf += '.pdf'
        
    # Delete existing PDF if exists
    if os.path.exists(output_pdf):
        os.remove(output_pdf)
        arcpy.AddMessage(f"Deleted existing file: {output_pdf}")

    # Export layout to PDF
    layout.exportToPDF(output_pdf)
    arcpy.AddMessage(f'PDF file created at: {output_pdf}')

except Exception as e:
    arcpy.AddError(f'Error occurred: {str(e)}')
