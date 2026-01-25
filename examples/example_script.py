"""
Example script showing how to call the library-level conversion API.
"""

# from seamless_pdf import convert
# convert("file.docx")
# TODO: Add more example use cases.

from seamless_pdf import convert

# Convert the project README into a PDF for quick manual testing.
convert("README.md", output_path="testing.pdf")
