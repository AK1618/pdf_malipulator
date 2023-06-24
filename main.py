from tkinter import Tk, Label, Button, filedialog
from PyPDF2 import PdfMerger, PdfReader, PdfWriter

class PDFManipulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AK PDF Manipulator")
        self.root.geometry("800x600")

        # Customize the colors
        self.root.config(bg="lightgray")

        # Create labels
        self.label = Label(root, text="AK PDF Manipulator", font=("Arial", 18, "bold"), bg="lightgray")
        self.label.pack(pady=10)

        # Create buttons with custom colors
        self.merge_button = Button(root, text="Merge PDFs", command=self.merge_pdfs, bg="violet", fg="black")
        self.merge_button.pack(pady=5)

        self.encrypt_button = Button(root, text="Encrypt PDF", command=self.encrypt_pdf, bg="blue", fg="black")
        self.encrypt_button.pack(pady=5)

        self.decrypt_button = Button(root, text="Decrypt PDF", command=self.decrypt_pdf, bg="green", fg="black")
        self.decrypt_button.pack(pady=5)

        self.stamp_button = Button(root, text="Stamp PDF", command=self.stamp_pdf, bg="yellow", fg="black")
        self.stamp_button.pack(pady=5)

        self.watermark_button = Button(root, text="Watermark PDF", command=self.watermark_pdf, bg="orange", fg="black")
        self.watermark_button.pack(pady=5)

        self.compress_button = Button(root, text="Compress PDF", command=self.compress_pdf, bg="red", fg="black")
        self.compress_button.pack(pady=5)

    def merge_pdfs(self):
        file_paths = filedialog.askopenfilenames(title="Select PDF Files", filetypes=(("PDF files", "*.pdf"),))
        if file_paths:
            merger = PdfMerger()
            for file_path in file_paths:
                merger.append(file_path)
            output_path = filedialog.asksaveasfilename(title="Save Merged PDF", defaultextension=".pdf",filetypes=(("PDF file", "*.pdf"),))
            if output_path:
                merger.write(output_path)
                merger.close()
                print("PDFs merged successfully.")

    def encrypt_pdf(self):
        file_path = filedialog.askopenfilename(title="Select PDF File", filetypes=(("PDF file", "*.pdf"),))
        if file_path:
            password = input("Enter password for encryption: ")
            reader = PdfReader(file_path)
            writer = PdfWriter()
            for page in reader.pages:
                writer.add_page(page)
            writer.encrypt(password)
            output_path = filedialog.asksaveasfilename(title="Save Encrypted PDF", defaultextension=".pdf",filetypes=(("PDF file", "*.pdf"),))
            if output_path:
                with open(output_path, "wb") as f:
                    writer.write(f)
                print("PDF encrypted successfully.")

    def decrypt_pdf(self):
        file_path = filedialog.askopenfilename(title="Select PDF File", filetypes=(("PDF file", "*.pdf"),))
        if file_path:
            password = input("Enter password for decryption: ")
            reader = PdfReader(file_path)
            writer = PdfWriter()
            if reader.is_encrypted:
                reader.decrypt(password)
            for page in reader.pages:
                writer.add_page(page)
            output_path = filedialog.asksaveasfilename(title="Save Decrypted PDF", defaultextension=".pdf",filetypes=(("PDF file", "*.pdf"),))
            if output_path:
                with open(output_path, "wb") as f:
                    writer.write(f)
                print("PDF decrypted successfully.")

    def stamp_pdf(self):
        content_pdf_path = filedialog.askopenfilename(title="Select Content PDF", filetypes=(("PDF file", "*.pdf"),))
        stamp_pdf_path = filedialog.askopenfilename(title="Select Stamp PDF", filetypes=(("PDF file", "*.pdf"),))

        if content_pdf_path and stamp_pdf_path:
            output_path = filedialog.asksaveasfilename(title="Save Stamped PDF", defaultextension=".pdf",
                                                       filetypes=(("PDF file", "*.pdf"),))
            if output_path:
                reader = PdfReader(stamp_pdf_path)
                image_page = reader.pages[0]
                writer = PdfWriter()
                reader = PdfReader(content_pdf_path)
                for index, content_page in enumerate(reader.pages):
                    mediabox = content_page.mediabox
                    content_page.merge_page(image_page)
                    content_page.mediabox = mediabox
                    writer.add_page(content_page)
                with open(output_path, "wb") as fp:
                    writer.write(fp)
                print("PDF stamped successfully.")

    def watermark_pdf(self):
        content_pdf_path = filedialog.askopenfilename(title="Select Content PDF", filetypes=(("PDF file", "*.pdf"),))
        stamp_pdf_path = filedialog.askopenfilename(title="Select Stamp PDF", filetypes=(("PDF file", "*.pdf"),))

        if content_pdf_path and stamp_pdf_path:
            output_path = filedialog.asksaveasfilename(title="Save Watermarked PDF", defaultextension=".pdf",filetypes=(("PDF file", "*.pdf"),))
            if output_path:
                reader = PdfReader(content_pdf_path)
                writer = PdfWriter()
                for index, content_page in enumerate(reader.pages):
                    mediabox = content_page.mediabox
                    # Load the stamp PDF separately for each page
                    reader_stamp = PdfReader(stamp_pdf_path)
                    image_page = reader_stamp.pages[0]
                    image_page.merge_page(content_page)
                    image_page.mediabox = mediabox
                    writer.add_page(image_page)
                with open(output_path, "wb") as fp:
                    writer.write(fp)
                print("PDF watermarked successfully.")

    def compress_pdf(self):
        file_path = filedialog.askopenfilename(title="Select PDF File", filetypes=(("PDF file", "*.pdf"),))

        if file_path:
            output_path = filedialog.asksaveasfilename(title="Save Compressed PDF", defaultextension=".pdf",filetypes=(("PDF file", "*.pdf"),))
            if output_path:
                reader = PdfReader(file_path)
                writer = PdfWriter()
                for page in reader.pages:
                    page.compress_content_streams()
                    writer.add_page(page)
                with open(output_path, "wb") as f:
                    writer.write(f)
                print("PDF compressed successfully.")



root = Tk()
pdf_manipulator = PDFManipulatorGUI(root)
root.mainloop()
