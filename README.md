# Scalable-data-refresh-system

Have a look at the Foursquare API, more specifically, the Venues search route at
https://developer.foursquare.com/docs/venues/search
Design a system that can receive locations (as a [latitude, longitude, accuracy] mobile GPS fix) that
represent a place that a user has visited and outputs information (that comes from the Foursquare API-call
above) about that place. Include a way to cache Foursquare results. Also include a way to refresh
Foursquare results as data retrieved from Foursquare can only be kept for a maximum of 30 days.
