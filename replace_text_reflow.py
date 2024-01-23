import fitz  # Import the PyMuPDF library

def replace_text_and_reflow(original_pdf_path, output_pdf_path, tag, replacement_text):
    """
    Replace a specified tag in a PDF with new text and reflow the text to fit the original layout.

    Args:
    original_pdf_path (str): The path to the original PDF file.
    output_pdf_path (str): The path where the modified PDF will be saved.
    tag (str): The text to be replaced in the PDF.
    replacement_text (str): The text that will replace the tag.

    Returns:
    None
    """

    # Open the original PDF
    doc = fitz.open(original_pdf_path)

    # Define a font and size for the replacement text
    font = 'helv'  # Helvetica font
    font_size = 11  # Font size

    # Iterate over each page in the document
    for page in doc:
        # Search for all instances of the tag on the page
        text_instances = page.search_for(tag)

        # Iterate over each found instance
        for inst in text_instances:
            # Remove the original tag by adding a redaction annotation
            page.add_redact_annot(inst, text=replacement_text, fill=(1, 1, 1))
            # Apply the redaction to remove the original text and add the new text
            page.apply_redactions()

            # Calculate the width of the replacement text
            text_width = fitz.get_text_length(replacement_text, font, font_size)
            # Create a new rectangle for the replacement text
            new_rect = fitz.Rect(inst[0], inst[1], inst[0] + text_width, inst[3])

            # Add the new text with the adjusted textbox size
            page.insert_textbox(new_rect, replacement_text, fontname=font, fontsize=font_size)

    # Save the modified document
    doc.save(output_pdf_path)

# Example usage
# replace_text_and_reflow("path/to/original.pdf", "path/to/output.pdf", "old text", "new text")
