import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PyPDF3 import PdfFileWriter, PdfFileReader
from PyPDF3.pdf import PageObject
import webbrowser
import math
import os
from os import path
import sys

def browse_file():
    """Opens a file dialog and displays the selected file's path in a label."""
    global filename, path_label, start, count, input_pdf
    # Open the file dialog and get the selected file path
    filename = filedialog.askopenfilename(
        initialdir="/", # Sets the initial directory
        title="Select a File",
        filetypes=(
            ("PDF files", "*.pdf"), ("All files", "*.*")
        )
    )
    
    # Update the label with the selected file's path
    if filename:
        path_label.config(text=filename)
        input_pdf = PdfFileReader(open(filename, "rb"), strict=False)
        start.set("1")
        count.set(str(len(input_pdf.pages)))
        process_btn.config(state=tk.NORMAL)
        print(f"Selected file: {filename}") # You can use the filename string to open and process the file later

def save_file_dialog():
    process_btn.config(text="Working")
    # Define file types for the dialog
    files = [
        ('PDF Document', '*.pdf'),
        ('All Files', '*.*')
    ]
    
    # Open the save dialog and get a file object in write mode
    # 'defaultextension' ensures an extension is added if the user doesn't provide one
    file = filedialog.asksaveasfile(filetypes=files, defaultextension=files)
    
    # Check if a file was successfully opened (user didn't cancel)
    if file:
        process(location=file.name)
    else:
        print("Save operation cancelled.")
    process_btn.config(text="Process")

def radio_change():
    if rb.get() == 2:
        seg_entry.config(state=tk.NORMAL)
    else:
        seg_entry.config(state=tk.DISABLED)

def make_2_in_1(page1,page2):
    total_width = page1.mediaBox.upperRight[0] + page2.mediaBox.upperRight[0]
    total_height = max([page1.mediaBox.upperRight[1], page2.mediaBox.upperRight[1]])
    new_page = PageObject.createBlankPage(None, total_width, total_height)
    new_page.mergePage(page1)
    new_page.mergeTranslatedPage(page2, page1.mediaBox.upperRight[0], 0)
    return new_page

def process(location: str):
    global input_pdf,output_pdf
    if(rb.get() == 1):
        offset = int(start.get())-1
        output_pdf = PdfFileWriter()
        half = math.ceil(int(count.get())/2.0)
        for i in range(half):
            if(inverse_even.get() & i%2==1):
                page1 = input_pdf.getPage(offset+half - i)
                if((2*half - i) < int(count.get())):
                    page2 = input_pdf.pages[offset+2*half - i]
                else:
                    page2 = PageObject.createBlankPage(None,page1.mediaBox.upperRight[0],page1.mediaBox.upperRight[1])
            else:
                page1 = input_pdf.getPage(offset+i)
                if(half + i < int(count.get())):
                    page2 = input_pdf.pages[offset + half + i]
                else:
                    page2 = PageObject.createBlankPage(None,page1.mediaBox.upperRight[0],page1.mediaBox.upperRight[1])
            output_pdf.addPage(make_2_in_1(page1,page2))
        output_pdf.write(open(location, "wb"))
    else:
        for n in range(math.ceil(int(count.get())/4/seg.get())):
            if(seg.get()*(n+1)*4<int(count.get())):
                half = seg.get()*2
            else:
                half = math.ceil((int(count.get())-seg.get()*n*4)/2)
            output_pdf = PdfFileWriter()
            offset = seg.get()*4*n+int(start.get())-1
            for i in range(half):
                if(inverse_even.get() & i%2==1):
                    page1 = input_pdf.getPage(offset+half - i)
                    if(seg.get()*4*n+half + i - 1< int(count.get())):
                        page2 = input_pdf.pages[offset+half + i - 1]
                    else:
                        page2 = PageObject.createBlankPage(None,page1.mediaBox.upperRight[0],page1.mediaBox.upperRight[1])
                else:
                    page1 = input_pdf.getPage(offset+i)
                    if(seg.get()*4*n+2*half - i - 1< int(count.get())):
                        page2 = input_pdf.pages[offset+2*half - i - 1]
                    else:
                        page2 = PageObject.createBlankPage(None,page1.mediaBox.upperRight[0],page1.mediaBox.upperRight[1])
                output_pdf.addPage(make_2_in_1(page1,page2))
            output_pdf.write(open('{0}{1}.pdf'.format(os.path.splitext(location)[0],n), "wb"))

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Create the main window
root = tk.Tk()
root.title("PDF Booklet")
frame1 = ttk.Frame(root,padding=10)
frame1.pack()
tk.Button(frame1, text="Browse File", command=browse_file).grid(row=0,column=0)
path_label = tk.Label(frame1,text="Open a PDF file you want to process")
path_label.grid(row=0,column=1)

frame2 = ttk.Frame(root,padding=10)
frame2.pack(fill=tk.X)
ttk.Label(frame2,text="Algorithms").pack(anchor=tk.W)

frame3 = ttk.Frame()
frame3.pack()
rb = tk.IntVar()
tk.Radiobutton(frame3, text="Split Page", variable=rb, value=1, command=radio_change).grid(row=0,column=0,sticky=tk.W)
tk.Radiobutton(frame3, text="Booklet", variable=rb, value=2, command=radio_change).grid(row=1,column=0,sticky=tk.W)
rb.set(2)
frameSeg = tk.Frame(frame3)
frameSeg.grid(row=2,column=0,sticky=tk.W)
seg = tk.IntVar()
tk.Label(frameSeg,text="Segment Size").grid(row=0,column=0)
seg_entry = tk.Entry(frameSeg,textvariable=seg)
seg_entry.grid(row=0,column=1)
seg.set(5)

frame4 = ttk.Frame(root,padding=10)
frame4.pack(fill=tk.X)
ttk.Label(frame4,text="Page Setting").pack(anchor=tk.W)

frame5 = ttk.Frame(root,padding=10)
frame5.pack()
ttk.Label(frame5,text="Start Page").grid(row=0,column=0,sticky=tk.W)
ttk.Label(frame5,text="Page Count").grid(row=1,column=0,sticky=tk.W)
start = tk.StringVar()
count = tk.StringVar()
ttk.Entry(frame5,textvariable=start).grid(row=0,column=1)
ttk.Entry(frame5,textvariable=count).grid(row=1,column=1)
start.set("0")
count.set("0")

inverse_even = tk.BooleanVar()
ttk.Checkbutton(root,text="Inversely sort even pages",variable=inverse_even).pack(pady=10)

process_btn = ttk.Button(root,text="Process",state=tk.DISABLED, command=save_file_dialog)
process_btn.pack(pady=20)

def go_to_git():
    # The URL you want to open
    url = "https://github.com/rifat-hossain/PDF-Booklet"
    # Use the webbrowser module to open the URL in the default browser
    webbrowser.open_new(url)

photo = tk.PhotoImage(file = path.abspath(path.join(path.dirname(__file__), 'github.png')))
ttk.Button(root, image = photo, command=go_to_git).pack(anchor=tk.E,padx=5,pady=5)

# Run the Tkinter event loop
root.mainloop()
