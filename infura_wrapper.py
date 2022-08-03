import requests

# Infura project info
projectId = "2CkE2yXUbaem6DrlmwaUQwhXK0k"
projectSecret = "0dc8f97c874fcd8694effaa043332d76"
endpoint = "https://ipfs.infura.io:5001"


def infura_wrapper(metadata):
    files = {
        'file': metadata
    }
    response = requests.post(endpoint + '/api/v0/add', files=files, auth=(projectId, projectSecret))
    hash = response.text.split(",")[1].split(":")[1].replace('"', '')
    return hash
