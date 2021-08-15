# Flask Distance Measure Blueprint
A Flask Blueprint to calculate from two adress

[![Github](http://i.imgur.com/9I6NRUm.png) Github](https://github.com/aw09)<br>
[![Linkedin](https://i.stack.imgur.com/gVE0j.png) LinkedIn](https://www.linkedin.com/in/agungw9/) <br>
[Demo](http://34.101.133.218:5000/)

# Table of Content
- [Installation](#installation)
  - [Using Virtual Env](#using-virtual-env)
  - [Using Docker](#using-docker)
- [Documentation](#documentation)
  - [Geopy](#geopy)
  - [Yandex](#yandex)
    - [Example Result](#example-result)
- [Testing & Logging](#testing--logging)

# Installation

Clone the repository
```bash
    git clone https://github.com/aw09/Distance-Measure-Blueprint.git 
```


## Using Virtual Env

Tools needed :
 * Python >= 3.8
 * Virtualenv

Make and activate virtualenv
```bash
  virtualenv .
  ./Scripts/activate # Windows
  source bin/activate # Linux
```
Install the required libraries
```
    pip install -r requirements.txt
```
Run program
```
    flask run
```
Check on
```
    localhost:5000
```
## Using Docker
Tools needed :
 * Docker

I have created Dockerfile and created bash file to build docker image and run it, just make that file executable using
```bash
    chmod +x run_docker.sh
```
Then run that file
```
    ./run_docker.sh
```
Check running container
```
    docker ps
```
Check on
```
    ipserver:5000
```

# Documentation
This blueprint using geopy library and Yandex API.
## Geopy
| Routes | Function|
| :---: | :---: |
| /geopy/(address) | Calculate distance address with **Moscow Ring Road** |
|  /geopy/(address1)/(address2) | Calculate between two address |

## Yandex
| Routes | Function|
| :---: | :---: |
| /yandex/(address) | Calculate distance address with **Moscow Ring Road** |
|  /yandex/(address1)/(address2) | Calculate between two address |
| /yandex/(address) | Calculate distance address with **Moscow Ring Road** in miles|
|  /yandex/miles/(address1)/(address2) | Calculate between two address in miles |

### Example Result
 - Inside Moscow Ring Road
```json
{
    "data": {
        "address1": "Moscow Ring Road",
        "address2": "Ramenki District",
        "coordinate1": [55.766557, 37.623429],
        "coordinate2": [55.708034, 37.515775],
        "distance": 0,
        "info": "Ramenki District is inside MKAD, distance: 0",
        "unit": "km"
    },
    "message": "Success",
    "status": 200
}
```
 - Outside Moscow Ring Road
```json
{
  "data": {
    "address1": "Moscow Ring Road",
    "address2": "Jakarta",
    "coordinate1": [55.766557, 37.623429],
    "coordinate2": [-6.175391, 106.826261],
    "distance": 9310.475301508663,
    "info": "",
    "unit": "km"
  },
  "message": "Success",
  "status": 200
}
```
 - Two Address
```json
{
  "data": {
    "address1": "Jakarta",
    "address2": "Bandung",
    "coordinate1": [-6.175391, 106.826261],
    "coordinate2": [-6.94851, 107.653735],
    "distance": 125.5209569666838,
    "info": "",
    "unit": "km"
  },
  "message": "Success",
  "status": 200
}

```

# Testing & Logging
For testing use 
```
  pytest
```

All logs can be found in
  ***record.log***
