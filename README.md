# kernel ftrace to NewRelic

A wrapper to send Linux kernel `ftrace` logs to NewRelic via the
NewRelic Python instrumentation.

This has some relation to the project:

    https://github.com/je-nunez/perf_record_to_NewRelic

but the issue is that the Linux kernel ftrace has different tracers possible
in `available_tracers` into `current_tracer`, and options: see:

    https://www.kernel.org/doc/Documentation/trace/ftrace.txt

so the best approach is not a wrapper as the wrapper in C in the above
mentioned link (`ftrace` would need much more options for its `events` to
enable, `set_events` masks, etc), but a consumer of standard-input which will
sends the measures it reads up to the New Relic collector, via the New Relic
Python instrumentation. So the general process in which this program is called
set-ups the ftrace environment under

    /sys/kernel/debug/tracing/....

does the tracing, and pipes the `ftrace` report to send to New Relic using
this program (possibly real-time measures from `trace_pipe` -but piping
directly from it, since different `ftrace` tracers have different output
formats, and from these formats, only some fields may be necessary to upload
to New Relic).

# WIP

This project is a *work in progress*. The implementation is *incomplete* and subject to change. The documentation can be inaccurate.


