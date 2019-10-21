from flask import Flask, request, jsonify

def checkAuthorization(headers):
    if 'X-Api-Key' in headers:
        auth = headers.get('X-Api-Key')
        if auth == 'QfatjqNAFBkAA40zON5z':
            return True
        else:
            return False 
    else:
        return False