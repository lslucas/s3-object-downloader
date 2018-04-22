import boto
import os
from tkinter import *
from tkinter import scrolledtext
from boto.exception import S3ResponseError
from dotenv import load_dotenv

load_dotenv('.env')

cwd = os.getcwd()

# if local path doesn't exists, create it first
if not os.path.exists(os.getenv('DOWNLOAD_PATH')):
	print("creating download directory")
	os.mkdir(os.getenv('DOWNLOAD_PATH'))

# window
window = Tk()
window.title("Download Objects From S3")
window.geometry('630x330')

# connect to s3 bucket
conn  = boto.connect_s3(os.getenv('AWS_ACCESS_KEY_ID'), os.getenv('AWS_ACCESS_SECRET_KEY'))
bucket = conn.get_bucket(os.getenv('BUCKET_NAME'))

lbl = Label(window, text="Prefix:", padx=5, pady=5)
lbl.grid(column=0, row=0)

# get the order_number from the user
text = Entry(window, width=15)
text.grid(column=1, row=0, padx=5, pady=5)
text.focus()

output = scrolledtext.ScrolledText(window,width=85,height=20)
output.grid(column=0, row=1, columnspan=3)

# list all files from the bucket and download
def download():
    btn.configure(text="Downloading...")

    bucket_list = bucket.list(prefix=text.get())

    for l in bucket_list:
        file = str(l.key)
        s3_path = os.getenv('DOWNLOAD_PATH') + file
        output.insert(INSERT,"- downloading " + file + "\n")
        try:
            if not os.path.exists(s3_path):
                output.insert(INSERT,"- downloading " + file + "\n")
                l.get_contents_to_filename(s3_path)
            else:
                output.insert(INSERT,"- file exists " + file + "\n")
        except (OSError, S3ResponseError) as e:
            pass
            # check if the file has been downloaded locally  
            if not os.path.exists(s3_path):
                try:
                    os.makedirs(s3_path)
                except OSError as exc:
                    # let guard againts race conditions
                    import errno
                    if exc.errno != errno.EEXIST:
                        output.insert(INSERT,"- raise what? " + file + "\n")
                        raise

    btn.configure(text="Download")


btn = Button(window, text="Download", command=download)
btn.grid(column=2, row=0)

window.mainloop()