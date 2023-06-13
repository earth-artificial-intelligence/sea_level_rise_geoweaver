import earthaccess
from pprint import pprint

auth = earthaccess.login(strategy="netrc", persist=True)

# We'll get 4 collections that match with our keywords
collections = earthaccess.collection_query().keyword("SEA SURFACE HEIGHT").cloud_hosted(True).get(4)

# Let's print 2 collections
for collection in collections[0:2]:
    # pprint(collection.summary())
    print(pprint(collection.summary()), collection.abstract(), "\n", collection["umm"]["DOI"], "\n\n")
    

granules = earthaccess.granule_query().short_name("SEA_SURFACE_HEIGHT_ALT_GRIDS_L4_2SATS_5DAY_6THDEG_V_JPL2205").temporal("2017-01","2018-01").get()
print(len(granules))

# the collection is cloud hosted, but we can access it out of AWS with the regular HTTPS URL
granules[0].data_links(access="external")
granules[0].data_links(access="direct")
