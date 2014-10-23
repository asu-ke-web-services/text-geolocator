text-geolocator
===============

Fall 2014/Spring 2015 CS Capstone - Generating heatmaps from and searching for geolocation data from text documents

## Install Instructions
- Install docker. http://docker.com Follow the directions provided for the target system.
- Install Python. (If it hasn't been already)
- Install pip.
- Install fig with `sudo pip install -U fig`
- Clone the repo. `git clone https://github.com/gios-asu/text-geolocator.git`
- Start the docker containers and development environment. `sudo fig up -d`
- Verify that everything started up ok. `sudo fig ps`

## Useful Commands
- sudo fig build -> rebuilds docker instance from Dockerfile
- sudo fig run web python -> launches docker environment and python interactive shell
- sudo docker rm $(sudo docker ps -a -q) -> removes all stopped old docker containers
- sudo docker rmi $(sudo docker images -q --filter "dangling=true") -> removes all untagged docker images
- sudo fig run --rm web -> removes container after run

## Example 1 request and response

HTTP Request
```
POST /geocode
Content: "This article is about the Dinagat Islands, in the middle of some large region." 
```

RESPONSE (in [geojson](http://geojson.org/)):
```javascript
[{
  "type": "Feature",
  "properties": {
    "weight": 1.0,
    "name": "Dinagat Islands"
    },
  "geometry": {
    "type": "Point",
    "coordinates": [125.6, 10.1]
  }
}, {
    "type": "Feature",
    "properties": {
      "weight": 0.5,
      "name": "some large region"
      },
    "geometry": {
        "type": "Polygon",
        "coordinates": [[
            [-109.05, 41.00],
            [-102.06, 40.99],
            [-102.03, 36.99],
            [-109.04, 36.99],
            [-109.05, 41.00]
        ]]
    }
}]
```

## Example 2 request and response

This example should work during Semester 2 of the workload when a higher level of detail is added to the system, other than just cities, states, and countries.

HTTP Request
```
POST /geocode
Content: "During this study that we conducted on A Mountain, we found that the number of overall species has decreased significantly from 2010 to 2014." 
```

RESPONSE:
```javascript
[{
  "type": "Feature",
  "properties": {
    "weight": 0.5,
    "name": "Tempe Butte"
    },
  "geometry": {
    "type": "Point",
    "coordinates": [33.428372, -111.935905]
  }
},{
  "type": "Feature",
  "properties": {
    "weight": 0.5,
    "name": "Sentinel Peak"
    },
  "geometry": {
    "type": "Point",
    "coordinates": [32.210484, -110.992475]
  }
}]
```

## 