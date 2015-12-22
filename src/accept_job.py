#!/usr/bin/env pythonf
from __future__ import print_function 
from gnip_historical.gnip_historical_cmd import GnipHistoricalCmd

class AcceptJob(GnipHistoricalCmd):
    def __call__(self):
        if self.userUrl is None:
            print("Please provide a job URL. Use accept_job.py -h for more information.")
        else:
            print("RESULT:")
            print(str(self.gnipHistorical.acceptJob(self.userUrl)))
            
AcceptJob()()
