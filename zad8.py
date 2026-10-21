import requests
import argparse

class Brewery:
        def __init__(self, id, name, brewery_type, address_1, address_2, address_3, city, state, street, state_province, postal_code, country, phone, website_url, longitude, latitude):
            self.id = id
            self.name = name
            self.brewery_type = brewery_type
            self.address_1 = address_1
            self.address_2 = address_2
            self.address_3 = address_3
            self.city = city
            self.street = street
            self.state_province = state_province
            self.postal_code = postal_code
            self.country = country
            self.phone = phone
            self.website_url = website_url
            self.longitude = longitude
            self.latitude = latitude
            self.state = state

        def __str__(self) -> str:
            return (
                f"Browar: {self.name}\n"
                f"Typ: {self.brewery_type}\n"
                f"Adres: {self.address_1}, {self.address_2}, {self.address_3}\n"
                f"Miasto: {self.city}\n"
                f"Kod pocztowy: {self.postal_code}\n"
                f"Kraj: {self.country}\n"
                f"Telefon: {self.phone}\n"
                f"Strona internetowa: {self.website_url}\n"
                f"Długość geograficzna: {self.longitude}\n"
                f"Szerokość geograficzna: {self.latitude}\n"
                f"Stan: {self.state}\n"
                f"Ulica: {self.street}"
            )


parser = argparse.ArgumentParser(description="Pobiera browary z Open Brewery DB")
parser.add_argument("--city", type=str, help="miasto, do którego ograniczyć wyniki")
args = parser.parse_args()
 
params = {"per_page": 20}
if args.city:
    params["by_city"] = args.city
 
response = requests.get("https://api.openbrewerydb.org/v1/breweries", params=params)
data = response.json()
 
breweries = [Brewery(**item) for item in data]

for brewery in breweries:
    print(brewery)
    print()

    
