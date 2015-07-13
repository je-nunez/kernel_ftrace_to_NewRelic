# kernel ftrace to NewRelic

A pipe to send Linux kernel `ftrace` logs to NewRelic via the
NewRelic Python instrumentation.

This has some relation to the project:

    https://github.com/je-nunez/perf_record_to_NewRelic

but the issue is that the Linux kernel ftrace has different tracers possible
in `available_tracers` into `current_tracer`  (plus much many more options
for its `events` to enable, `set_events` masks, etc): see:

    https://www.kernel.org/doc/Documentation/trace/ftrace.txt

so the best approach is not a wrapper as the wrapper in C in the above
mentioned link, but a consumer of standard-input which will sends the measures
it reads up to the New Relic collector, via the New Relic Python
instrumentation. So the general process in which this program is called
set-ups the ftrace environment under

    /sys/kernel/debug/tracing/....

does the tracing, and pipes the `ftrace` report to send to New Relic using
this program (possibly real-time measures from `trace_pipe` -but piping
directly from it, since different `ftrace` tracers have different output
formats, and from these formats, only some fields may be necessary to upload
to New Relic).

# WIP

This project is a *work in progress*. The implementation is *incomplete* and subject to change. The documentation can be inaccurate.

# Required libraries:

The New Relic library for Python is necessary:

     sudo pip install newrelic

# How to call this program

How to call this program:

     export NEW_RELIC_LICENSE_KEY=<new_relic_license_key>
 
     <ftrace-pipe...> | ./relay_to_newrelic_collector.py

or
     export NEW_RELIC_CONFIG_FILE='<path-to>/newrelic.ini'
     export NEW_RELIC_ENVIRONMENT='production'
 
     <ftrace-pipe...> | ./relay_to_newrelic_collector.py

where, in the second case, such `<path-to>/newrelic.ini` has the New Relic
License Key and settings for the agent in this environment.

The script expects its input to be of the form:

    <metric_name> <metric_value> ...

where each pair is separated by spaces and consists of:

   <metric_name>: a string with a valid New Relic metric name
   <metric_value>: a float

Several pairs can be given in the same line (separated by spaces), or in
multiple input lines (but a pair can not be split into consecutive lines,
otherwise the first line is ignored as not having an even number of tokens).

