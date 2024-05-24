# Install Courier SDK: pip install trycourier
from trycourier import Courier

client = Courier(auth_token="pk_prod_3Q175NE07Q4NBRKTCVQ9XZY7KVWM")

def sendmail(name,email,username,password):

    resp = client.send_message(
    message={
        "to": {
        "email": email,
        },
        "template": "DYA4GWYM6VMTF4JEX1RTW5VS3NRQ",
        "data": {
        "recipientName": name,
        'username' : username,
        'password' : password
        },
    }
    )

    return resp['requestId']