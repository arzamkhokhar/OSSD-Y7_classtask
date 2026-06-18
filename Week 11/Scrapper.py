import requests
from bs4 import BeautifulSoup
import csv

# Take manufacturer name from user
car = input("Enter manufacturer name: ")

# Headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://google.com"
}

# Website URL
url = f'https://www.pakwheels.com/new-cars/pricelist/{car}'

# Send request
response = requests.get(url, headers=headers)

# Function to save data into CSV file
def save_to_csv(data, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # CSV headings
        writer.writerow(["Car Name", "Price"])

        # Write data rows
        writer.writerows(data)

# Check if page opened successfully
if response.status_code == 200:

    soup = BeautifulSoup(response.text, 'html.parser')

    tables = soup.find_all('table')

    # Empty list to store data
    car_data = []

    # Loop through tables
    for table in tables:

        rows = table.find_all('tr')

        for row in rows:

            cols = row.find_all('td')

            if len(cols) >= 2:

                name = cols[0].get_text(strip=True)
                price = cols[1].get_text(strip=True)

                print(f"Car Name: {name} - Price: {price}")

                # Save into list
                car_data.append([name, price])

    # Save data into CSV file
    save_to_csv(car_data, "cars.csv")

    print("Data saved to cars.csv")

else:
    print("Page not available!")