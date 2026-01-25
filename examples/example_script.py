# from seamless_pdf import convert
# convert("file.docx")
# TODO: Add more examples "mock" usecase


from seamless_pdf import convert
from seamless_pdf.markdown_converter import convert_markdown_to_html

convert_markdown_to_html("README.md", output_path="testing.html")
