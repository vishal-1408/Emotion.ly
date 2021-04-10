import base64
import schedule


# Customer ID
customer_key = "5f2e45e4693e4a8d814d54220003a68b"
# Customer secret
customer_secret = "d55abefc622348c5bce8384a6d5556ab"

# Concatenate customer key and customer secret and use base64 to encode the concatenated string
credentials = customer_key + ":" + customer_secret
# Encode with base64
base64_credentials = base64.b64encode(credentials.encode("utf8"))
# credential = base64_credentials.decode("utf8")
# print(credential)


def printing():
    print("hello")

job = schedule.every(5).seconds.do(printing)
print(job)
