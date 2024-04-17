# Transformer from Easting-Northing to Longitude-Longitude taken from:

# Author: WebScraping.com
# Year: 2012
# Accessed: 11/04/2024
# URL: https://webscraping.com/blog/Converting-UK-Easting-Northing-coordinates/


from pyproj import Proj, transform

v84 = Proj(proj="latlong",towgs84="0,0,0",ellps="WGS84")
v36 = Proj(proj="latlong", k=0.9996012717, ellps="airy",
towgs84="446.448,-125.157,542.060,0.1502,0.2470,0.8421,-20.4894")
vgrid = Proj(init="world:bng")

def ENtoLL84(easting, northing):
    vlon36, vlat36 = vgrid(easting, northing, inverse=True)
    return transform(v36, v84, vlon36, vlat36) # (longitude, latitude)