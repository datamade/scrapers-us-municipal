from unicodedata import normalize
from urllib.parse import urlencode
from datetime import datetime, date

import requests

from pupa.scrape import Event, Bill, VoteEvent

from .base import MiamiScraper, ToArabic


class MiamiEventScraper(MiamiScraper):

    BASE_URL = 'http://miamifl.iqm2.com/'
    EVENTSPAGE = 'http://miamifl.iqm2.com/Citizens/calendar.aspx'

    date_format = '%b %-d, %Y %H:%M %p'

    def session(self, action_date):
        localizer = pytz.timezone(self.TIMEZONE).localize

        if action_date < localize(datetime(2017, 11, 7)):
            return '2015'
        else:
            return '2017'

    def bill(self, bill_link, classification, event):

        bill_detail = self.lxmlize(detail_link)

        identifier = bill_detail.xpath('//div[@id="ContentPlaceholder1_lblResNum"]/text()')[0]
        history = bill_detail.xpath("//tr[contains(@class, 'HistorySection')]")
        first_action_date = history.xpath("td[@class='Date']/a/text()")[0]

        leg_session = self.session(self.toTime(first_action_date))

        bill = Bill(identifier=identifier,
                    legislative_session=leg_session,
                    title=subsection_title,
                    classification=classification,
                    from_organization={'name': 'Miami City Commission'})

        bill.add_source(detail_link, note='web')

        for vote in bill_detail.xpath("//table[contains(@class, 'MeetingHistory')]"):
            vote_dates = vote.xpath("//td[@class='Date']//a[contains(@id, 'lnkMeeting')]/text()")
            vote_records = vote.xpath("//table[@class='VoteRecord']")

            for vote_date, vote_record in zip(vote_dates, vote_records):

                result = vote_record.xpath("tr/td[contains(text(), 'RESULT')]/following-sibling::td/text()")[0]

                vote_event = VoteEvent(legislative_session=leg_session,
                                       motion_text='Adopt {}'.format(identifier),
                                       organization='Miami City Commission',
                                       start_date=self.toTime(vote_date),
                                       result=result,
                                       bill=bill)

                vote_event.add_source(detail_link)

                ayes = vote_record.xpath("tr/td[contains(text(), 'AYES')]/following-sibling::td/text()")
                nays = vote_record.xpath("tr/td[contains(text(), 'NAYS')]/following-sibling::td/text()")

                if ayes:
                    people = ayes[0].split(',')

                    for person in people:
                        vote_event.yes(person)

                if nays:
                    people = nays[0].split(',')

                    for person in people:
                        vote_event.no(person)

                event.add_vote_event(vote_event)

                yield vote_event

        event.add_bill(bill, note=classification)

        yield bill

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
            event_name = event_row.xpath("div/div[contains(@class, 'MainScreenText')]/text()")[0]
            event_detail_link = event_row.xpath("div/div/a[contains(@href, 'Detail_Meeting.aspx')]")[0]
            event_detail_url = event_detail_link.xpath('@href')[0]
            event_time = event_detail_link.xpath('text()')
            event_location = event_name.split(' - ')[1]

            documents = event_row.xpath("div/div[contains(@id, 'DownloadLinks')]/div/a")
            document_dict = {}
            for document in documents:
                document_type = document.xpath('text()')[0]
                if document_type != 'Video':
                    document_dict[document_type] = dict(note=document_type,
                                                        url=document.xpath('@href')[0],
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

            event_address = event_detail.xpath("//div[@class='MeetingAddress']/text()")[0]
            clean_address = normalize('NFKD', event_address)
            event_location = '{0} - {1}'.format(event_location, clean_address)

            event = Event(name=event_name,
                          start_date=event_time,
                          location_name=event_location)

            event.add_source(event_detail_url,
                             note='web')

            # Reconstruct agenda

            agenda_rows = event_detail.xpath("//table[@id='MeetingDetail']/tr")

            for index, row in enumerate(agenda_rows):
                if len(row.xpath('td')) == 2:
                    # This is the top level header
                    roman_numeral = row.xpath("td[@class='Num']//strong/text()")
                    if roman_numeral:
                        # Sometimes there are top headers that mark the end of an
                        # agenda item. Skip them
                        section_number = float(ToArabic(roman_numeral[0].strip().replace('.', '')).arabic)
                        section_title = row.xpath("td[@class='Title']//strong/text()")[0]

                        main_agenda_item = event.add_agenda_item(section_title)

                elif len(row.xpath('td')) == 3:
                    # These are the subitems under the headers Sometimes there
                    # are several versions of the same resolution under one
                    # agenda item. Only the first mention will have a subsection
                    # number

                    subsection_text = row.xpath("td[@class='Num']/text()")

                    if subsection_text:
                        subsection_text = subsection_text[0].strip().replace('.', '')
                        subsection_number = '{0}.{1}'.format(int(section_number), subsection_text)
                        subsection_title = row.xpath("td[@class='Title']//text()")[0]

                        event.add_agenda_item(subsection_title)

                        # Hmm ... need to add the bill to the event
                        if 'a resolution of' in subsection_title.lower():
                            detail_link = row.xpath("td[@class='Title']//a/@href")[0]
                            yield from self.bill(detail_link, 'resolution', event)

                        elif 'an ordinance of' in subsection_title.lower():
                            detail_link = row.xpath("td[@class='Title']//a/@href")[0]
                            yield from self.bill(detail_link, 'ordinance', event)
            yield event

    def scrape(self):
        pass
