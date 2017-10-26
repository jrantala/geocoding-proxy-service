import urllib
import urllib2
import json
import settings
import unittest

debug = False

API_KEY_GOOGLE = settings.API_KEY_GOOGLE #'AIzaSyDLGnd26jaP7-cFWwCD_MpTpE1B6LyLXRc'
APP_ID_HERE = settings.APP_ID_HERE # 'RTL6uLe7Xa4lfI5vwk4K'
APP_CODE_HERE = settings.APP_CODE_HERE #'JxmA-W33RD2kTKc3kACFqw'

class LatLonFetch(object):
    def __init__(self):
        self.force_an_error = None

    def choose_provider(self, provider='GOOGLE'):
        self.provider = provider

    def force_error(self, provider):
        self.force_an_error = provider
    
    def fetch_with_backup(self, addr):
        self.choose_provider('GOOGLE')
        print 'fetching from Google'
        try:
            return self.fetch(addr)
        except:
            self.choose_provider('HERE')
            print 'fetching from Here'
            return self.fetch(addr)

    def fetch(self, addr):

        if self.force_an_error == self.provider:
            raise 'an exception' #  !!!

        esc_addr = urllib.quote(addr)
        if debug:
            print addr, esc_addr

        if self.provider == 'GOOGLE':
            # url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + esc_addr + '&key=' + API_KEY_GOOGLE
            url = settings.GOOGLE_GEOCODE_URL % (esc_addr, API_KEY_GOOGLE)
        elif self.provider == 'HERE':
            # url = 'https://geocoder.cit.api.here.com/6.2/geocode.json?app_id=' + APP_ID_HERE + '&app_code=' + APP_CODE_HERE + '&searchtext=' + esc_addr
            url = settings.HERE_GEOCODE_URL % (APP_ID_HERE, APP_CODE_HERE, esc_addr)
        
        reply = urllib2.urlopen(url)
        if debug: print reply
        contents = reply.read()
        if debug: print contents
        json_contents = json.loads(contents)
        if debug: 
            print '---------------'
            print json_contents

        if self.provider == 'GOOGLE':
            # parse google reply
            part = json_contents["results"][0]["geometry"]["location"]
            part["Latitude"] = part['lat']
            part["Longitude"] = part['lng']
            del part['lat']
            del part['lng']

            # print part
            return part

        elif self.provider == 'HERE':
            # print 'here goes here'
            part = json_contents["Response"]["View"][0]["Result"][0]["Location"]["DisplayPosition"]
            # print part
            return part

def main():
    llf = LatLonFetch()
    # llf.choose_provider('HERE')
    # llf.choose_provider('GOOGLE')

    # addr = '16886 blsh, fooroit, MI'
    addr = '1530 siskiyou dr 94598'

    llf.force_error('GOOGLE')
    llf.force_error(None)
    llf.force_error('HERE')

    llf.fetch_with_backup(addr)

if __name__ == '__main__':
    main()

# ---- unittests -------

# from command line: python -m unittest latlon_fetch

class TestLatLonFetch(unittest.TestCase):

    def test_google(self):
        llf = LatLonFetch()
        llf.choose_provider('GOOGLE')
        addr = '16887 fenton 48219'
        coordinates = llf.fetch(addr)
        print '---------\n%s\n-----------------' % coordinates

        self.assertIn('42.41', str(coordinates))
        self.assertIn('-83.28', str(coordinates))

    def test_here(self):
        llf = LatLonFetch()
        llf.choose_provider('HERE')
        addr = '16887 fenton 48219'
        coordinates = llf.fetch(addr)
        print '---------\n%s\n-----------------' % coordinates

        self.assertIn('42.41', str(coordinates))
        self.assertIn('-83.28', str(coordinates))

