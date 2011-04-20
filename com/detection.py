from AccessControl import getSecurityManager

def gzip_enabled(REQUEST):
    "see if gzip works and return .gz or '' based on that"
    return 'gzip' in REQUEST.environ.get('HTTP_ACCEPT_ENCODING', '')

def isClient():
    return isRole('Client')
    
def isManager():
    return isRole('Manager')
    
def isAuthenticated():
    return isRole('Authenticated')
    
def isRole(role):
    return getSecurityManager().getUser().has_role([role])