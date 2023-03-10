# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import csv
import getopt
import re
import sys
from datetime import datetime
import email.header

NEW_EMAIL_HEADER_REGEX = "From [\d\d]+@xxx [A-Z][a-z]{2} [A-Z][a-z]{2} \d{2} \d{2}:\d{2}:\d{2}"
DATE_REGEX = "Date: [A-Z][a-z,]{3} \d+ [A-Z][a-z]{2} \d{4} \d{2}:\d{2}:\d{2}"
valid_emails = []


class Email:

    def __init__(self):
        self.date = None
        self.sender = None
        self.receiver = "Undisclosed"
        self.subject = None

    def csv(self):
        return [str(self.date), self.sender, self.receiver, self.subject]


# https://stackoverflow.com/a/36716138
def decode_mime_words(s):
    return u''.join(
        word.decode(encoding or 'utf8') if isinstance(word, bytes) else word
        for word, encoding in email.header.decode_header(s))


def decoded(line, prefix):
    line = line.removeprefix(prefix).removesuffix("\n")
    if line.startswith("=?utf-8?Q?") or line.startswith("=?UTF-8?Q?"):
        line = decode_mime_words(u'' + line)
    line = line.replace("\"", "")
    return line


def date_decoded(date_string):  # date_string = Date: Tue, 1 Nov 2022 09:57:20 +0000 (GMT)?
    split_line = date_string.split(" ")
    if len(split_line) == 8:
        date_string = date_string.removesuffix(
            " " + split_line[7])  # date_string = Date: Tue, 1 Nov 2022 09:57:20 +0000
    date_string = date_string.removeprefix("Date: " + split_line[1] + " ").removesuffix(
        " " + split_line[6])  # date_string = 1 Nov 2022 09:57:20
    date = datetime.strptime(date_string, "%d %b %Y %X")  # https://www.w3schools.com/python/python_datetime.asp
    return date


def write_csv(out_list):
    with open(output_file, 'w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Sender", "Receiver", "Subject"])
        for out in out_list:
            writer.writerow(out.csv())


def email_decoder(line, email):
    line = line.replace("  ", " ")  # Just as some emails are formatted with double space for dates
    split_line = line.split(" ")

    if re.match(NEW_EMAIL_HEADER_REGEX, line):  # Checks if a new email is found
        if (email.date is not None) and email.date >= valid_date:  # Checks if the date is in the range required
            valid_emails.append(email)
        email = Email()

    if split_line[0] == "To:":
        email.receiver = decoded(line, "To: ")
    if split_line[0] == "From:":
        email.sender = decoded(line, "From: ")
    if re.match(DATE_REGEX, line):
        email.date = date_decoded(line)
    if split_line[0] == "Subject:":
        email.subject = decoded(line, "Subject: ")
    return email


def file_reader():
    try:
        with open(input_file, "r") as file:
            email = Email()
            for line in file:
                email = email_decoder(line, email)
        write_csv(valid_emails)
        print("Successfully created!")
    except FileNotFoundError:
        print("Input File not found")


def main(argv):
    global input_file
    global output_file
    global valid_date
    valid_date = datetime.strptime("6 Mar 2023 00:00:00", "%d %b %Y %X")
    output_file = "output.csv"
    opts, args = getopt.getopt(argv, "hi:o:d:", ["ifile=", "ofile=", "date="])
    for opt, arg in opts:
        if opt == '-h':
            print("email_to_csv.py -i <inputfile> -o <outputfile> -d <date:dd/mm/yyyy>")
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file = arg
        elif opt in ("-o", "--ofile"):
            output_file = arg
        elif opt in ("-d", "--date"):
            valid_date = datetime.strptime(arg, "%d/%m/%Y")
    print("Input file is", input_file)
    print("Output file is", output_file)
    print("Date is", valid_date)
    file_reader()


if __name__ == "__main__":
    main(sys.argv[1:])
