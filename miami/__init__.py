from pupa.scrape import Jurisdiction

from .bills import MiamiBillScraper
from .events import MiamiEventScraper
from .people import MiamiPersonScraper


class Miami(Jurisdiction):
    division_id = 'ocd-division/country:us/state:fl/place:miami'
    classification='government'
    name = 'Miami City Government'
    url = 'http://http://miamifl.iqm2.com/'

    scrapers = {
        'bills': MiamiBillScraper,
        'events': MiamiEventScraper,
        'people': MiamiPersonScraper,
    }
