# Workflow for critics

Critics must be aware of the limitations of Claude's vision capabilities:
* Accuracy: Claude may hallucinate or make mistakes when interpreting low-quality, rotated, or very small images under 200 pixels.
* Spatial reasoning: Claude's spatial reasoning abilities are limited. It may struggle with tasks requiring precise localization or layouts, like reading an analog clock face or describing exact positions of chess pieces.
* Counting: Claude can give approximate counts of objects in an image but may not always be precisely accurate, especially with large numbers of small objects.

Sending images to the claude API is costly. Before doing so ask yourself:
* Do I really need to send this image to Claude for inspection, or can I maybe make a tool to get the insight I need? **IF SO: MAKE THE TOOL**
* Does the information that I seek to extract from the image allow for me to send it at a lower resolution? **IF SO: DOWNSCALE THE IMAGE**
* Avoid sending high resolution images to claude unless absolutely necessary
