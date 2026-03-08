# PDF-Booklet
You can easily create a PDF booklet that can be turned into a book after printing using this tool.

Recommended to use the coptic stitch after printing on the _"Booklet"_ settings and to spiral bind after printing on the _"Split Page"_ settings, and thus you can **save 4 times the paper**.

## Dependancies
- PyPDF3
- Tkinter

## Screenshot
<img width="291" height="454" alt="image" src="https://github.com/user-attachments/assets/704c3c0a-1a58-4a58-bba6-cfc7bdbf6b48" />

## Getting Started

There are two algorithms to create a processed PDF for printing. They result in different kinds of books, so you can choose the way you want your book to be and set it with those settings.

| Split Page | Booklet |
| ---------- | ----------|
| <img width="350" height="250" alt="image" src="https://github.com/user-attachments/assets/74847989-4c10-41c1-a6f0-2d4b3eaca43a" /> | <img width="365" height="250" alt="image" src="https://github.com/user-attachments/assets/80c4619d-b4ab-4207-ab7a-c5398117feb7" /> |

### Procedure
- First, select the PDF that you want to make a book from.
- Select the algorithm according to your preference.
- If you want to trim the range of the PDF file, you can adjust the _"Start Page"_ and _"Page Count"_ from that start point accordingly.
- Hit _"Process"_. This will make you a PDF to print as a book.
- With the _“Split Page”_ setting, you need to cut the pages in half and stack the first half on the other before proceeding with the binding.
- With the _“Booklet”_ setting, the printed segments must be stacked in order before using the Coptic stitch technique to bind the book.

### Trick
If your home printer cannot print on both sides of the paper, check _“Inversely Sort Even Pages”_ before processing. First, print the even pages. Then reinsert the printed sheets into the printer and print the odd pages on the reverse side.

If your printer supports duplex printing, you can simply enable “Print on Both Sides” and print normally. In that case, there is no need to check _“Inversely Sort Even Pages.”_
