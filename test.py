from pypdf import PdfReader, PdfWriter

pdf_path = "backend\partnership\data\COVER+NOTE+Partnership_edited.pdf"

reader = PdfReader(pdf_path)
writer = PdfWriter()


page = reader.pages[0]
fields = reader.get_fields()

print(fields)

writer.append(reader)

writer.update_page_form_field_values(
    writer.pages[0],
    {
        "proposed_name_1": "Nana Brown".upper(),
        "proposed_name_2": "Kenkey".upper(),
        "tin_1": "236426281",
    },
    auto_regenerate=False,
)

with open("filled-out.pdf", "wb") as output_stream:
    writer.write(output_stream)
