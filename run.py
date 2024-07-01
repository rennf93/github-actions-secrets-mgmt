from base64 import b64encode
import json
from nacl import encoding, public
import requests
import sys
import os
import logging
from typing import Dict, Any


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



def retrieve_input(env: str) -> str:
    """
    Retrieve an input from the environment.
    """
    value = os.getenv(env)
    if value is None:
        logging.error(f"{env} is a required input and must be set.")
        sys.exit(1)
    return value



def generate_authentication_headers(access_token: str) -> Dict[str, str]:
    """
    Generate authentication headers for GitHub API.
    """
    return {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {access_token}",
    }



def retrieve_public_key_details(
    base_url: str,
    access_token: str
) -> Dict[str, Any]:
    """
    Retrieve public key details from GitHub Actions Secrets.
    """
    try:
        response = requests.get(
            f"{base_url}/public-key",
            headers=generate_authentication_headers(access_token)
        )
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Failed to retrieve public key: {e}")
        sys.exit(1)
    return response.json()



def encrypt_secret(
    key: str,
    coding: str,
    secret_plain: str
) -> str:
    """
    Encrypt a secret using the public key.
    """
    try:
        public_key = public.PublicKey(key.encode(coding), encoding.Base64Encoder())
        sealed_box = public.SealedBox(public_key)
        encrypted = sealed_box.encrypt(secret_plain.encode(coding))
        return b64encode(encrypted).decode(coding)
    except Exception as e:
        logging.error(f"Failed to encrypt secret: {e}")
        sys.exit(1)



def save_secret(
    base_url: str,
    access_token: str,
    key_id: str,
    secret_name: str,
    secret: str
) -> None:
    """
    Save a secret to GitHub Actions Secrets.
    """
    try:
        response = requests.put(
            f"{base_url}/{secret_name}",
            headers=generate_authentication_headers(access_token),
            data=json.dumps({
                "encrypted_value": secret,
                "key_id": key_id,
            })
        )
        logging.info(f"Save secret response status code: {response.status_code}")
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Error saving secret: {e}")
        sys.exit(1)



if __name__ == "__main__":
    logging.info('Extracting input ...')
    owner = retrieve_input('OWNER')
    repository = retrieve_input('REPOSITORY')
    access_token = retrieve_input('ACCESS_TOKEN')
    secret_name = retrieve_input('SECRET_NAME')
    secret_value = os.getenv('SECRET_VALUE', '')

    base_url = f"https://api.github.com/repos/{owner}/{repository}/actions/secrets"
    coding = "utf-8"

    logging.info(f"Retrieving public key for {owner}/{repository} ...")
    key = retrieve_public_key_details(base_url, access_token)

    logging.info("Encrypting secret value ...")
    secret = encrypt_secret(key['key'], coding, secret_value)

    logging.info(f"Saving secret value in GitHub action secret {secret_name} ...")
    save_secret(base_url, access_token, key['key_id'], secret_name, secret)
    logging.info("Secret saved successfully!")