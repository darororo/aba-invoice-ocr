# Store data from images of ABA invoice to csv

A script I wrote to help me extract data from ABA invoices. :DD

The extraction is not perfect. Double checking is still required.

main.py

```python
def main():
    directory = "YOUR/IMAGES/DIRECTORY"
```

You may set the directory variable to the folder where your images are stored.

# Running the script

## Prerequisite

- Make sure you have tesseract installed on your pc. https://tesseract-ocr.github.io

- Open the project in your terminal and install the python dependencies

  by running `pip install -r requirements.txt`. Using a virtual environment is recommended.

## Run the script

- Inside the project folder, enter `python main.py` in your terminal.
- a file `out.csv` will be created inside the folder.
