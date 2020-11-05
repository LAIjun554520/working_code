# -*- coding: utf-8 -*-


def user_agent(name="tdt_performance"):
    """
    Return a string representing the default user agent.

    :rtype: str
    """
    return '%s' % name


def authorization_headers(federation_token, content_type="application/json;charset=UTF-8"):
    """
    :rtype: headers conf
    """
    return {
        'User-Agent': user_agent(),
        'Accept-Encoding': ', '.join(('gzip', 'deflate')),
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Content-Type': content_type,
        'Authorization': "Bearer %s" % federation_token
    }


def default_headers(content_type="application/json;charset=UTF-8"):
    """
        :rtype: headers conf
        """
    return {
        'User-Agent': user_agent(),
        'Accept-Encoding': ', '.join(('gzip', 'deflate')),
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Content-Type': content_type
    }
