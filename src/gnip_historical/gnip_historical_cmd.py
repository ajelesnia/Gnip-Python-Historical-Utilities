#!/usr/bin/env python
import configparser
from optparse import OptionParser
from gnip_historical.gnip_historical_main import GnipHistorical 


DEFAULT_FILE_NAME='./.gnip'

class GnipHistoricalCmd(object):
    def __init__(self, jobPar=None):
        self.config = configparser.ConfigParser()
        self.config.read(DEFAULT_FILE_NAME)

        un = self.config.get('creds', 'un')
        pwd = self.config.get('creds', 'pwd')
        endURL = self.config.get('endpoint', 'url')
        self.prevurl = self.config.get('tmp','prevUrl')

        parser = OptionParser()
        parser.add_option("-u", "--url", dest="url", default=None,
                    help="Job url.")
        parser.add_option("-l", "--prev-url", action="store_true", dest="prevUrl", default=False,
                    help="Use previous Job URL (only from this configuration file.).")
        parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False,
                    help="Detailed output.")

         # This is for other jobs to add in their parameters
        self.setOptions(parser)

        # Set Options
        (self.options, self.optArgs) = parser.parse_args()

        # Update prevUrl in the config
        self.updateURLConfig()

        # Set up a connection to GNIP
        self.gnipHistorical = GnipHistorical(un, pwd, endURL, jobPar)
        
    def setOptions(self, parser):
        # e.g. parser.add_option("-l", "--prev-url", action="store_true", dest="prevUrl", default=False,
        #            help="Use the prev Job URL.")
        pass

    def updateURLConfig(self, url = None):
        if self.options.prevUrl:
            self.userUrl = self.prevurl
        elif self.options.url is not None:
            self.userUrl = self.options.url
        elif url is not None:
            self.userUrl = url
        else:
            self.userUrl = None

        # If UserURL is not specified through -u flag
        # then just use '' since configparser.set cannot accept None
        try:
          self.config.set('tmp','prevUrl', self.userUrl)
        except:
          self.config.set('tmp','prevUrl', '')

        with open(DEFAULT_FILE_NAME, 'w') as self.configfile:
            self.config.write(self.configfile)

