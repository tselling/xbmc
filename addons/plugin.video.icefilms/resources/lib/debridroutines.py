import urllib, urllib2
import re, os, cookielib

class RealDebrid:

    def __init__(self, cookie_file, username, password):
        self.cookie_file = cookie_file
        self.username = username
        self.password = password
        


    def GetURL(self, url):

        print 'DebridRoutines - Requesting URL: %s' % url
        if self.cookie_file is not None and os.path.exists(self.cookie_file):
            cj = cookielib.LWPCookieJar()
            cj.load(self.cookie_file)
            req = urllib2.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')   
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            response = opener.open(req)

            #check if we might have been redirected (megapremium Direct Downloads...)
            finalurl = response.geturl()

            #if we weren't redirected, return the page source
            if finalurl is url:
                link=response.read()
                response.close()
                return link

            #if we have been redirected, return the redirect url
            elif finalurl is not url:               
                return finalurl    


    def Resolve(self, url):
        print 'DebridRoutines - Resolving url: %s' % url
        url = 'http://real-debrid.com/ajax/deb.php?lang=en&sl=1&link=%s' % url
        source = self.GetURL(url)
        print 'DebridRoutines - Returned Source: %s' % source
        download_details = {}
        download_details['download_link'] = ''
        download_details['message'] = ''
        if source == '<span id="generation-error">Your file is unavailable on the hoster.</span>':
            download_details['message'] = 'The file is unavailable on the hoster'
            return download_details
        elif re.search('This hoster is not included in our free offer', source):
            download_details['message'] = 'This hoster is not included in our free offer'
            return download_details
        elif re.search('<span id="generation-error">No server is available for this hoster.</span>', source):
            download_details['message'] = 'No server is available for this hoster'
            return download_details
        else:
            link = re.search('ok"><a href="(.+?)"', source).group(1)
            print 'DebridRoutines - Resolved Link: %s' % link
            download_details['download_link'] = link
            return download_details


    def valid_host(self, host):
        url = 'http://real-debrid.com/lib/api/hosters.php'
        allhosts = self.GetURL(url)
        if host in allhosts:
            return True
        else:
            return False


    def  checkLogin(self):
        url = 'http://real-debrid.com/lib/api/account.php'
        source = self.GetURL(url)
        if source is not None and re.search('expiration', source):
            return False
        else:
            return True


    def Login(self):    
        if self.checkLogin():
            cj = cookielib.LWPCookieJar()
            login_data = urllib.urlencode({'user' : self.username, 'pass' : self.password})
            url = 'https://real-debrid.com/ajax/login.php?' + login_data
            req = urllib2.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
            cj = cookielib.LWPCookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

            #do the login and get the response
            response = opener.open(req)
            source = response.read()
            response.close()
            cj.save(self.cookie_file)
            print source
            if re.search('OK', source):
                return True
            else:
                return False
        else:
            return True
