Geocoding Proxy Service README


These files should be in the same directory:

   latlon_fetch.py
   server_1.py
   settings.py

Starting the Server

   python server_1.py

       url is localhost:<PORT> , where the default PORT value is contained in settings.PORT

       the port number can also be specified via the commandline, such as

           python server_1.py -p8080


Running the Service

    The server only responds to GETs

    The server assumes that the input address follows the 'addr=' in the request url, so each of the following urls is accepted:

        http://localhost:8080/addr=16886+fenton+48219
	http://localhost:8080/a/b/c?addr=16886+fenton+48219

    A successful fetch of the latlon coordinates will return data in this format:

        {"data":[{"coordinates": {"Latitude": 42.41317220000001, "Longitude": -83.281988}}]}

    If the service can't find the address in the request url, it will return a 500 response.


Unittests

    python -m unittest latlon_fetch


Forcing the primary service (Google) fetch to fail

    LatLonFetch.fetch_with_backup() attempts to use Google's service first.
    If that fails, it will attempt to use Here's service.
    You can force the backup service to be used via

        LatLonFetch.force_error('GOOGLE')
