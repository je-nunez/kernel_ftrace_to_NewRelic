#!/bin/env python

"""
Script to pipe measures up to the New Relic collector.

It expects its input to be of the form:

<metric_name> <metric_value> ...

where each pair is separated by spaces and consists of:

   <metric_name>: a string with a valid New Relic metric name
   <metric_value>: a float

Several pairs can be given in the same line (separated by spaces), or in
multiple input lines (but a pair can not be split into consecutive lines,
otherwise the first line is ignored as not having an even number of tokens).
"""

import sys
import fileinput
import newrelic.config
import newrelic.api.application
import newrelic.api.transaction

# In a future version of this script new features will added,
# like to send strings via:
#
#    add_custom_parameters()
#
# to add custom parameters, but instead in this first version
# we use only 'newrelic.api.application.record_custom_metrics()'
# to relay the custom metrics to New Relic.


def relay_info_to_new_relic(newr_app):
    """ Relays the fileinput.input() to the New Relic collector

        Parameters:
           newr_app: a newrelic.api.application.Application object

        Return Value:
           not applicable

        It creates a New Relic transaction on that application,
        and relays the custom metrics from fileinput.input() to
        New Relic.
    """

    newr_trans = newrelic.api.transaction.Transaction(newr_app, True)
    newr_trans.set_transaction_name("ftrace", "Pipe")
    newr_trans.background_task = True
    newr_trans.suppress_apdex = True
    newr_trans.capture_params = False
    newr_trans.autorum_disabled = True
    newr_trans.suppress_transaction_trace = True
    newr_trans.enabled = True

    for line in fileinput.input():
        simpler_line = line.strip()

        if not simpler_line:
            # empty input line: ignore it
            continue

        fields = simpler_line.split()

        if fields[0][0] == '#':
            # a comment
            continue

        if len(fields) % 2 == 0:
            # assume it is a sequence of Key Value to send to New Relic
            newrelic_metrics_dict = {}
            while fields:
                metric_name = fields.pop(0).strip()
                metric_value = fields.pop(0).strip()
                newrelic_metrics_dict[metric_name] = float(metric_value)

            newr_trans.record_custom_metrics(newrelic_metrics_dict.iteritems())
            continue

        sys.stderr.write("WARNING: Ignoring line '%s'\nIt doesn't have an "
                         "even number of fields in the format "
                         "'key numeric-value...' to relay to New Relic.\n" %
                         line.rstrip())

    # stop recording
    newr_trans.stop_recording()



def main():
    """Main function"""

    # debug_level = "DEBUG"
    debug_level = "INFO"
    app_name = "ftrace_to_NewRelic"
    newrelic.config.initialize(log_file="/tmp/ftrace_newrelic_log.log",
                               log_level=debug_level)
    newrelic_app = newrelic.api.application.application_instance(app_name)
    settings = newrelic_app.global_settings
    settings.enabled = True
    newrelic_app.activate()

    relay_info_to_new_relic(newrelic_app)



if __name__ == '__main__':
    main()

