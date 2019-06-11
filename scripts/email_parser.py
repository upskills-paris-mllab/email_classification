
import re
import email
import os


file = os.path.join("C:", os.sep, "Users", "AurélienBAELDE", "Documents", "email_classification", "114_")

with open(file) as fp:
    # Create a text/plain message
    msg = email.message_from_file(fp)

body = msg._payload

#Remove the original message from the body

clean_body = body[0:body.find("-----Original Message-----")]



