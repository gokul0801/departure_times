import logging

logging.basicConfig(level    = logging.DEBUG,
                    format   ='%(asctime)s %(levelname)s %(message)s',
                    filename = ('rtt.log'),
                    filemode = 'a')

def error(*args, **kwargs):
    caller = logging.getLogger().findCaller()
    args_list = list(args)
    args_list[0] = "%s in %s():%s %s" % ( caller[0], caller[2], caller[1], args[0])
    logging.error(*tuple(args_list), **kwargs)

def warning(*args, **kwargs):
    caller = logging.getLogger().findCaller()
    args_list = list(args)
    args_list[0] = "%s in %s():%s %s" % ( caller[0], caller[2], caller[1], args[0])
    logging.warning(*tuple(args_list), **kwargs)

def debug(*args, **kwargs):
    caller = logging.getLogger().findCaller()
    args_list = list(args)
    args_list[0] = "%s in %s():%s %s" % ( caller[0], caller[2], caller[1], args[0])
    logging.debug(*tuple(args_list), **kwargs)
