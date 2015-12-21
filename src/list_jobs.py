#!/usr/bin/env python
from __future__ import print_function 
from gnip_historical.gnip_historical_cmd import GnipHistoricalCmd

import datetime


class ListJobs(GnipHistoricalCmd):

    def setOptions(self, parser):
        parser.add_option("-d", "--since-date", dest="sinceDateString", default=None, 
                help="Only list jobs after date, (default 2012-01-01T00:00:00)")
        parser.add_option("-s", "--status", dest="statusString", default=None,
            help="Only list jobs with a specific status (options: open, quoted, accepted, rejected, running, or delivered)")
        parser.add_option("-o", "--output_data_file", dest="path_to_file", default='./data_files.txt',
            help="Full path to file name of where the data file names will be stored. Default ./data_files.txt")

    # available statuses: rejected, accepted, running, quoted
    def output(self, status):
        ''' Creates output for every job listed if not specified 
        and if there is no accepted result, then data files will be written to file specified '''

        if self.options.statusString is not None and status.status != self.options.statusString:
            return  
        else:
            if self.options.verbose:
                status = self.gnipHistorical.getJobStatus(status.jobURL)
                print(str(status))
                if status.result is not None:
                    print("Writing files to {} for {}...".format(self.options.path_to_file, status.title))
                    status.result.write(self.options.path_to_file)
            else:
                print("#"*25)
                print("TITLE:    {}".format(status.title))
                print("STATUS:   {}".format(status.status))
                print("PROGRESS: {}%".format(status.percentComplete))
                print("JOB URL:  {}".format(status.jobURL))
                if self.options.prevUrl or self.options.url is not None:
                    if status.result is not None:
                        print()
                        print(str(status.quote))
                        print(str(status.result))
                        print("Writing files to {} for {}...".format(self.options.path_to_file, status.title))
                        status.result.write(self.options.path_to_file)
                elif status.status.lower().startswith("delivered"):
                    print('Data files available, use "-v, -u or -l" flag to download files list.')

    def __call__(self):
        if self.userUrl is None:
            for status in self.gnipHistorical.listJobs():
                if self.options.sinceDateString is not None:
                    if datetime.datetime.strptime(self.options.sinceDateString, DATEFMT[:17]) <= status.requestedAt:
                        self.output(status)
                else:
                    self.output(status)
        else:
            status = self.gnipHistorical.getJobStatus(self.userUrl)
            self.output(status)


ListJobs()()               
