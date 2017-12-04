from pupa.scrape import Jurisdiction, Organization

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

    def get_organizations(self):
        commission = Organization('Miami City Commission',
                                  classification='legislature')

        for district in range(1, 6):
            commission.add_post('Commissioner District {}'.format(district),
                                role='Commissioner',
                                division_id='ocd-division/country:us/state:fl/place:miami/council_district:{}'.format(district))

        yield commission

        mayor = Organization('Mayor', classification='executive')

        yield mayor
