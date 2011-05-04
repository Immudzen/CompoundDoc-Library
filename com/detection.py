from AccessControl import getSecurityManager

def gzip_enabled(REQUEST):
    "This function takes the REQUEST as an arguement and then returns True if gzip is enabled and false if it is not"
    return 'gzip' in REQUEST.environ.get('HTTP_ACCEPT_ENCODING', '')

def isClient():
    "return True if the current user has the role of Client else False"
    return isRole('Client')
    
def isManager():
    "return True if the current user has the role of Manager else False"
    return isRole('Manager')
    
def isAuthenticated():
    "return True if the current user has the role of Authenticated else False"
    return isRole('Authenticated')
    
def isRole(role):
    "return True if the current user has the role of [role] else False"
    return getSecurityManager().getUser().has_role([role])