from pathlib import Path 
from PIL import Image
import pytesseract
import csv
import helpers

def get_row(file: Path, fields: list):
    img = Image.open(file)
    extracted_text = pytesseract.image_to_string(img, "eng+khm", config="--psm 4")
    lines = extracted_text.splitlines()
    row = {}
    try:
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
                try:
                    time = split[1] + ":" + split[2]
                    time = time[-8:]
                    row["time"] = time
                    
                    date = helpers.string_to_date(split[1][1:-3]) # substr omiting hours and left space
                    split[1] = date
                except:
                    raise StopIteration

            if len(split) > 1 and (field in fields):
                row[field] = split[1]
    except StopIteration:
        print("Error parsing date")
        print("Skipping: " + file.name)
        raise Exception("error while scanning row")
    return row

def main(): 
    directory = "YOUR/IMAGES/DIRECTORY"
    files = Path(directory).glob("*.jpg")

    fields = ["reference #", "transaction date", "time",  "remark", "amount-us", "amount-kh", "seller", "original amount", "from account"]

    data = []
    for file in files:
        print("File: " + file.name)
        try:
            row = get_row(file, fields)
        except Exception as e:
            print(e)
            try:
                with open(directory + "/errors.txt", "a", newline="", encoding="utf-8") as errLog:
                    message = file.name + ": " + str(e)
                    errLog.write(message + "\n")
            except Exception as e:
                print(e)
        else: 
            data.append(row)

    print(data)
    with open(directory + "/out.csv", 'w', newline='', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)
       
if __name__ == "__main__":
    main()



