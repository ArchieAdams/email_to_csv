# email_to_csv
Basic project that takes a Google Takeout email file and output it as a csv file

This is not perfect and the receiver will needed editting but should still help


To get you emails downloaded 
1. Go to: https://takeout.google.com/?pli=1


| ![Image](https://imgur.com/UjFiobC.png) |
|:--:| 
| *Make sure you unselect it all.* |

2. Scroll down and select mail

| ![Image](https://imgur.com/AO48yQF.png) |
|:--:| 
| *Feel free to edit the all mail included but default is fine.* |

3. Scroll to the bottom and click next steps

| ![Image](https://imgur.com/YHe0UlE.png) |
|:--:| 
| *Transfer to where ever I went with drive an it worked fine, the reset is up to you.* |

4. Click "Create Export" (This bit takes a while)

5. Download the file when complete and file the file in Mail called "All mail Including Spam and Trash.mbox"

6. Run the email_to_csv.py

# Commands

email_to_csv.py -i \<inputfile\> -o \<outputfile\> -d \<date\>

date in the format dd/mm/yyyy

outputfile is output.csv by default

date is the 6th March by default

  
