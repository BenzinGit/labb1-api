import requests
import sys

def get_token(url):
    try:
        r = requests.post(f"{url}/api/token", timeout=5)
        status_code = r.status_code

        # If status code != 201, write out error
        if (status_code != 201):
            print("Status code " + str(status_code)+ ": "+  r.json().get("error", "Unknown error"))
            return None

        data = r.json()
        token = data.get("token")
        return token
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return None
    except ValueError:
        print("Response was not JSON:")
        print(r.text)
        return None


def verify_token(url, token):
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        }

        r = requests.post(f"{url}/api/verify", headers=headers, timeout=5)
        status_code = r.status_code

        # If status code != 200, write out error
        if (status_code != 200):
            print("Status code " + str(status_code)+ ": "+  r.json().get("error", "Unknown error"))
            return None
        
        # If status code is 200, get the secret
        data = r.json()
        secret = data.get("secret")
        return secret
    
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return None
    except ValueError:
        print("Response was not JSON:")
        print(r.text)
        return None
    


def get_flag(url, token, secret):
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        }
        payload = {"secret": secret}

        r = requests.post(f"{url}/api/flag", headers=headers, json=payload, timeout=5)
        status_code = r.status_code

        # If status code != 200, write out error
        if (status_code != 200):
            print("Status code: " + str(status_code)+ " "+  r.json().get("error", "Unknown error"))
            return None
        
        # If status code is 200, get the secret
        data = r.json()
        flag = data.get("flag")
        return flag

    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return None
    except ValueError:
        print("Response was not JSON:")
        print(r.text)
        return None
    




def main ():
    base_url = "http://10.3.10.104:3000"
   
    # Step 1
    token = get_token(base_url)
    if (token is None):
        print("Could not recieve token, closing program")
        sys.exit(1)

    # Step 2
    secret = verify_token(base_url, token)
    if (secret is None):
        print("Could not verify token and receive secret, closing program")
        sys.exit(1)

    # Step 3
    flag = get_flag(base_url, token, secret)
    if (flag is None):
        print("Could not recieve flag, closing program")
        sys.exit(1)

    print(flag)
    

if __name__ == "__main__":
    main()

