import urllib.parse

encoded_uri = 'http%3A%2F%2F192.168.44.4%3A54003%2Fgithub_login%2Fauthorized'
decoded_uri = urllib.parse.unquote(encoded_uri)
print(decoded_uri)
