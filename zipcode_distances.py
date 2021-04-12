from geopy import distance
from geopy.geocoders import Nominatim

SEARCH_ZIP_CODE_STR = '{zip_code}, France'
REF_ZIP_CODE = '75019'
NOMINATIM = Nominatim(user_agent='project_etienne')

def get_point(zip_code):
    _, point = NOMINATIM.geocode(SEARCH_ZIP_CODE_STR.format(zip_code=zip_code))
    return point

def distance_to_ref(zip_code):
    d = distance.distance(REF_POINT, get_point(zip_code))
    return d

def distances_to_ref(zip_codes):
    distances = [distance_to_ref(zip_code) for zip_code in zip_codes]
    return distances

REF_POINT = get_point(REF_ZIP_CODE)
