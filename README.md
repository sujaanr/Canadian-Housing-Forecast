# canadian housing cost estimator

## introduction

this project aims to predict the current value of unlisted properties in the greater toronto region using a sophisticated multilayer perceptron model that considers over 30 variables. the ultimate goal is to integrate this model into a web application, possibly developed with python-flask and react, allowing users to input an address or postal code and receive an estimated property value instantly.

## data

the dataset encompasses over 14,000 property listings extracted via a puppeteer web scraper from zolo.com. additional geolocational data were obtained through latlong.net, with the scraper simulating human interactions to retrieve longitude and latitude details. this comprehensive dataset is stored in a mysql database for efficient access and manipulation.

### features

the machine learning model incorporates a diverse set of features to ensure accurate predictions, including but not limited to:

- **location:** the geographical area of the property.
- **property type:** the category of property (e.g., detached, condo, etc.).
- **nearby amenities:** proximity to essential services such as schools and grocery stores.
- **school rankings:** the quality of educational institutions in the vicinity.

## conclusion

this project represents a significant step towards automating property valuation in the toronto area, potentially revolutionizing how property values are assessed and providing valuable insights to homeowners, buyers, and real estate professionals alike.

