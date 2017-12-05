from unicodedata import normalize
from urllib.parse import urlencode
from datetime import datetime, date

import requests

from pupa.scrape import Event

from .base import MiamiScraper, ToArabic


class MiamiEventScraper(MiamiScraper):

    BASE_URL = 'http://miamifl.iqm2.com/'
    EVENTSPAGE = 'http://miamifl.iqm2.com/Citizens/calendar.aspx'

    def events(self, since=None):
        params = {
            'From': '10/1/2016',
            'To': '12/31/9999',
            'DepartmentID': 1000,
        }

        if since:
            params['From'] = datetime.strptime(since, '%m/%d/%Y').date()

        event_page_url = '{base}?{query}'.format(base=self.EVENTSPAGE,
                                                 query=urlencode(params))

        events_page = self.lxmlize(event_page_url)

        for event_row in events_page.xpath("//div[contains(@class, 'MeetingRow')]"):
            event_name = event_row.xpath("div/div[contains(@class, 'MainScreenText')]/text()")[0].text
            event_detail_link = event_row.xpath("div/div/a[contains(@href, 'Detail_Meeting.aspx')]")[0].text
            event_detail_url = event_detail_link.xpath('@href')[0].text
            event_time = event_detail_link.xpath('text()').text
            event_location = event_name.split(' - ')[1]

            documents = event_row.xpath("div/div[contains(@id, 'DownloadLinks')]/div/a")
            document_dict = {}
            for document in documents:
                document_type = document.xpath('text()')[0].text
                if document_type != 'Video':
                    document_dict[document_type] = dict(note=document_type,
                                                        url=document.xpath('@href')[0].text,
                                                        media_type='application/pdf')
                else:
                    event_id = event_detail_url.rsplit('ID=', 1)[-1]
                    video_url = 'http://miamifl.iqm2.com/Citizens/SplitView.aspx?Mode=Video&MeetingID={}&Format=Minutes'.format(event_id)
                    document_dict['Video'] = dict(note='Video',
                                                  url=video_url,
                                                  type='recording',
                                                  media_type='text/html')

            # Get better location, agenda, and roll call
            event_detail = self.lxmlize(event_detail_url)

            event_address = event_detail.xpath("//div[@class='MeetingAddress']/text()")[0].text
            clean_address = normalize('NFKD', event_address)
            event_location = '{0} - {1}'.format(event_location, clean_address)

            event = Event(name=event_name,
                          start_date=event_time,
                          location_name=event_location)

            # Reconstruct agenda

            agenda_rows = event_detail.xpath("//table[@id='MeetingDetail']/tr")

            for index, row in enumerate(agenda_rows):
                if len(row.xpath('td')) == 2:
                    # This is the top level header
                    roman_numeral = row.xpath("td[@class='Num']/strong/text()")
                    if roman_numeral:
                        # Sometimes there are top headers that mark the end of an
                        # agenda item. Skip them
                        section_number = float(ToArabic(roman_numeral[0]).arabic)
                elif len(row.xpath('td')) == 3:
                    # These are the subitems under the headers
                    print(row)
                elif len(row.xpath('td')) == 4:
                    # These are the attachments
                    print(row)

    def scrape(self):
        pass
