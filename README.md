municipal-scrapers
==================

[![Build Status](https://travis-ci.org/datamade/scrapers-us-municipal.svg?branch=v0.0.32)](https://travis-ci.org/datamade/scrapers-us-municipal)

DataMade's source for municipal scrapers feeding [ocd.datamade.us](https://ocd-api-documentation.readthedocs.io/en/latest/).

See [the upstream README](https://github.com/opencivicdata/scrapers-us-municipal) for instructions on local installation and development of the scrapers.

## Development

### Making changes to this fork

Changes should only be made to this fork if they are related to deployment, configuration or task scheduling. All changes to scraper functionality should be made [upstream in `opencivicdata/scrapers-us-municipal`](https://github.com/opencivicdata/scrapers-us-municipal).

As such, we want changes in this repo to all be rebased off `opencivicdata/scrapers-us-municipal`.

First, set up your upstream branch.

```bash
git remote add upstream https://github.com/opencivicdata/scrapers-us-municipal.git
```

Then pull from origin of this fork.

```bash
git pull origin master
```

Next, rebase your changes onto upstream master.


```bash
git pull upstream master
```

```bash
git push origin master
```

### Deploying changes

This repo uses Travis for continuous integration and deployment. To trigger a production deployment, create and push a tag matching the regular expression at the top of [`.travis.yml`](.travis.yml).

## Logging

### Handling unresolved bills

For LA Metro, we have alerting set up to notify us if pupa is not able to resolve a board report associated with an agenda item. This is an important diagnostic tool to help us track down why some board reports are not getting scraped.

Some board reports are not getting scraped because they have not been made public and will not be made public. When LA Metro tells us that they will not make a board report public, we should "ignore" that alert in Sentry. Also add a comment that you were directed by LA Metro that this board report will not be made public.

We take this approach instead of editing the scraper to ignore certain bills because it's possible that LA Metro may decide to change their mind about what to make public sometime in the future.
