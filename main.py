from pathlib import Path 
from PIL import Image
import pytesseract
import csv
import helpers

directory = "./data"
files = Path(directory).glob("*.jpg")

data = []
fields = ["reference #", "transaction date", "amount-us", "amount-kh", "remark", "seller", "original amount", "from account"]

for file in files:
    img = Image.open(file)
    extracted_text = pytesseract.image_to_string(img, "eng+khm")
    lines = extracted_text.splitlines()

    # TODO: turn write to row to a function
    row = {}
    for idx, line in enumerate(lines):
        split = line.split(":")
        if idx == 0:
            currency = split[0][-3:-1].lower()
            if currency == "us":
                row["amount-us"] = split[0][1:-4]
                row["amount-kh"] = 0
            elif currency == "kh":
                row["amount-kh"] = split[0][1:-4]
                row["amount-us"] = 0
            continue

        field = split[0].lower()

        if field == "transaction date":
            date = helpers.string_to_date(split[1][1:-3]) # substr omiting hours and left space
            split[1] = date

        if len(split) > 1 and (field in fields):
            row[field] = split[1]
    data.append(row)

print(data)
with open('tests3.csv', 'w', newline='', encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()
    writer.writerows(data)



