import asyncio


def first():
    return "hi"


async def second():
    data  = first()
    print("Data from first function:", data)
    return data

# second()
asyncio.run(second())

import bcrypt

def get_hashed_password(password: str) -> str:
    # Encode password to bytes and truncate to 72 bytes limit
    pwd_bytes = password.encode('utf-8')
    if len(pwd_bytes) > 72:
        pwd_bytes = pwd_bytes[:72]
    
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')

print(get_hashed_password("mysecretpassword"))



# API call

import requests,time
from concurrent.futures import ThreadPoolExecutor, as_completed

url = "http://127.0.0.1:8000/v1/admin/get-user-list"
headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwiZXhwIjoxNzY5NTEwOTUxLCJ0eXBlIjoiYWNjZXNzIn0.qeVN3ZEink-ktSuzukWSVNsA7TgrPbRlJdnnDwqrXgQ"
}

def call_api(i):
    r = requests.get(url, headers=headers)
    return i, r.status_code

with ThreadPoolExecutor(max_workers=20) as executor:
    start= time.time()
    futures = [executor.submit(call_api, i) for i in range(1000)]
    for future in as_completed(futures):
        i, status = future.result()
        print(f"Request {i + 1}: status={status}")
    end = time.time()

    print(end-start)