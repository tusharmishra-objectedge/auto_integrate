import requests

url = "https://651313e18e505cebc2e98c43.mockapi.io"

try:
    getStudents = url + "/students"

    print(f"getStudents: {getStudents}")

    response = requests.get(getStudents)

    if response.status_code == 200:
        print("GET students: OK")
        data = response.json()
        # print(data)

        if len(data) > 0:
            for key, value in data[0].items():
                data_type = type(value).__name__
                print(f"{key}: ({data_type})")
    else:
        print("MockAPI GET: ERROR ", response.status_code)

except Exception as e:
    print(f"Error: {e}")
