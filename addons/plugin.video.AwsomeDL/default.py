import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,base64,datetime,os,urlresolver
import settings
import time
from t0mm0.common.net import Net
net = Net()

ADDON = xbmcaddon.Addon(id='plugin.video.AwsomeDL')

def CATEGORIES():
        url1='http://www.awesomedl.com/'
        addDir('Search','Url',3,'https://dl.dropbox.com/u/94360623/My-Repo/AWImages/Search.png','')
        addDir('Recommend Top 10 TV Shows',url1,5,'https://dl.dropbox.com/u/94360623/My-Repo/AWImages/Recommend.png','')
        addDir('New Tv Shows','url',7,'','')
        req = urllib2.Request(url1)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        link1=link.replace("/search/label/Site News",'').replace("/search/label/Other",'')
        match=re.compile("<li><a href='/(search/label/).+?'>(.+?)<").findall(link1)
        for caturl, name in match:
                url=url1+caturl+name.replace(" ","%20")
                iconimage='https://dl.dropbox.com/u/94360623/My-Repo/AWImages/%s.png' % str(name).replace(" ","%20")
                addDir(name,url,1,iconimage,'')

def INDEX(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        link1=link.replace('"','')
        match=re.compile("entry-title'>\n<a href='(.+?)'>(.+?)</a>\n.+?\n.+?\n.+?\n.+?\n.+?\n.+?\n.+?\n.+?\n.+?src=(.+?)alt=><br>").findall(link1)
        for url, name, iconimage in match:
                print 'index=url===================='+(str(url))
                addDir(name,url,2,iconimage,'')
        #try:
        if len(match)>=19:
                match2=re.compile("<a class='blog-pager-older-link' href='(.+?)' id=").findall(link1)
                print 'match2======================='+(str(match2))
                url1= match2[0]
                iconimage=str(url)
                addDir('Next Page',url1,4,iconimage,'')
        setView('movies', 'media info 2')   

def VIDEOLINKS(url,name,iconimage):
        print"ef videolinks "+(url)
        req = urllib2.Request(str(url))
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link2=response.read()
        response.close()
        print(str(response))
        link=link2.replace('\n','')
        match=re.compile('<b><u>Watch Online:</b></u><br />(.+?)</p>').findall(link)
        r= match[0]
        match1=re.compile('<a href="http://adf.ly/(.+?)">Put(.+?)</a>').findall(r)
        print (match1)
        match2=re.compile('<a href="http://www.vidxden.com/(.+?)">Vidx(.+?)</a>').findall(r)
        match3=re.compile('<a href="http://q.gs/(.+?)">Put(.+?)</a>').findall(r)
        match4=re.compile('http://www.putlocker.com/file/(.+?)">Put(.+?)</a>').findall(r)
        match5=re.compile('http://www.uploadc.com/(.+?)">Uploa(.+?)</a>').findall(r)
        match6=re.compile('http://www.vidbux.com/(.+?)/.+?">Vidb(.+?)</a>').findall(r)
        match7=re.compile('http://www.nowvideo.eu/video/(.+?)">Now(.+?)</a>').findall(r)
        match8=re.compile('<a href="http://adf.ly/(.+?)">Put(.+?)</a>.+?href="http://adf.ly/(.+?)">NowV(.+?)</a>').findall(r)
        match9=re.compile('<a href="http://q.gs/(.+?)">Put(.+?)</a>.+?<a href="http://q.gs/(.+?)">NowV(.+?)</a>').findall(r)
        print '===================================   5  =====       '+str(match5)
        iconimage=str(iconimage)
        adfly='http://adf.ly/'
        qgs='http://q.gs/'
        try:
	        for file, name in match3:
	                name='Put'+str(name)
	                cleanfile=str(qgs)+str(file)
                        html = net.http_GET(cleanfile).content
	                matches = re.compile("var url = '(.*?)';").findall (html)
                        gourl=matches[0]
                        print 'THIS IS THE GO URL WE WANT==============================================     '+str(gourl)
	                time.sleep(5)
	                html1 = net.http_GET('https://adf.ly/'+gourl).content
	                link1 = html1.encode('ascii', 'ignore')
	                try:
                                reallink = re.compile('META HTTP-EQUIV="Refresh" CONTENT="0; URL=(.+?)">').findall (link1)
                                hosturl= reallink[0]
                                print 'THIS IS THE SOURCE WE WANT==============================================     '+str(hosturl)
                                media_url=urlresolver.resolve(hosturl)
                                url= str(media_url)
                                iconimage = 'https://dl.dropbox.com/u/94360623/My-Repo/AWimages/putlocker.jpg'
                                addLink(name,url,iconimage)
                        except:
                                pass
                        url= str(media_url)
                        iconimage = 'https://dl.dropbox.com/u/94360623/My-Repo/AWimages/putlocker.jpg'
	                addLink(name,url,iconimage)
        except:
                pass
        try:
	        for file, name in match1:
                        print 'MATCH1+MATCH1+MATCH1'
	                name='Put'+str(name)
	                cleanfile=str(adfly)+str(file)
	                print 'MATCH1 CLEAN==========+'+str(cleanfile)
                        html = net.http_GET(cleanfile).content
	                matches = re.compile("var url = '(.*?)';").findall (html)
                        gourl=matches[0]
                        print 'mM1THIS IS THE GO URL WE WANT==============================================     '+str(gourl)
	                time.sleep(5)
	                html1 = net.http_GET('https://adf.ly/'+gourl).content
	                link1 = html1.encode('ascii', 'ignore')
	                try:
		                reallink = re.compile('META HTTP-EQUIV="Refresh" CONTENT="0; URL=(.+?)">').findall (link1)
                                hosturl= reallink[0]
                                print 'THIS IS THE SOURCE WE WANT==============================================     '+str(hosturl)
                                media_url=urlresolver.resolve(hosturl)
                                url= str(media_url)
                                iconimage = 'https://dl.dropbox.com/u/94360623/My-Repo/AWimages/putlocker.jpg'
                                addLink(name,url,iconimage)
	                except:
		                pass
	                url= str(media_url)
                        iconimage = 'https://dl.dropbox.com/u/94360623/My-Repo/AWimages/putlocker.jpg'
	                addLink(name,url,iconimage)
        except:
                pass
        try:
	        for file, name in match4:
	                hosturl='http://www.putlocker.com/file/'+str(file)
	                name='Put'+str(name)
	                print'MATCH4========================================'+str(hosturl)
	                media_url=urlresolver.resolve(hosturl)
	                url= str(media_url)
	                iconimage = 'https://dl.dropbox.com/u/94360623/My-Repo/AWimages/putlocker.jpg'
	                addLink(name,url,iconimage)
        except:
                pass
        try:
	        for file, name in match2:
	                hosturl='http://www.vidxden.com/'+str(file)
	                name='Vidx'+str(name)
	                media_url=urlresolver.resolve(hosturl)
	                url= str(media_url)
	                iconimage = 'https://dl.dropbox.com/u/94360623/My-Repo/AWimages/vidxden.jpg'
	                addLink(name,url,iconimage)
        except:
                pass
        try:
	        for file, name in match5:
	                hosturl='http://www.uploadc.com/'+str(file)
	                name='Uploa'+str(name)
	                media_url=urlresolver.resolve(hosturl)
	                url= str(media_url)
	                iconimage = 'https://dl.dropbox.com/u/94360623/My-Repo/AWimages/uploadc.jpg'
	                #print 'MATCH5 UPLOADC ========================================='+(url)
	                #print 'HOSTURL ================================================'+(hosturl)
	                addLink(name,url,iconimage)
        except:
                pass
        try:
	        for file, name in match6:
	                hosturl='http://www.vidbux.com/'+str(file)
	                name='Vidb'+str(name)
	                media_url=urlresolver.resolve(hosturl)
	                url= str(media_url)
	                iconimage = 'https://dl.dropbox.com/u/94360623/My-Repo/AWimages/vidxden.jpg'
	                addLink(name,url,iconimage)
        except:
                pass
        try:
                for file, name in match7:
	                hosturl='http://www.nowvideo.eu/video/'+str(file)
	                print 'MATCH7============================'+str((hosturl))
	                name= 'Now'+str(name)
	                print 'NAME7=============================='+(name)
	                #media_url=urlresolver.resolve(hosturl)
	                #url= str(media_url)
	                #iconimage = 'https://dl.dropbox.com/u/94360623/My-Repo/AWimages/uploadc.jpg'
	                data = cache_page(str(hosturl))
	                file = get_match(data,'flashvars.file="([^"]+)"')
	                key = get_match(data,'flashvars.filekey="([^"]+)"')
	                codes = get_match(data,'flashvars.cid="([^"]+)"')
	                url = "http://www.nowvideo.eu/api/player.api.php?file="+file+"&user=undefined&codes="+codes+"&pass=undefined&key="+key.replace(".","%2E").replace("-","%2D")
	                data = cache_page(url)
	                location = get_match(data,'url=([^\&]+)&')
	                location = location + "?client=FLASH"
	                if not location:
                                location = 'CONTENTREMOVED'
                        print 'auth url is ' + str(location)
                        url=str(location)
                        iconimage='https://dl.dropbox.com/u/94360623/My-Repo/AWimages/NowVideo.png'
                        addLink(name,url,iconimage)
          
        except:
                pass
        try:
                for file1, name1, file, name in match8:
                        #print 'MATCH8 URL============================'+str(url)
                        name='NowV'+str(name)
                        cleanfile=str(adfly)+str(file)
                        print 'match8 cleanfile==================='+str(cleanfile)
                        html = net.http_GET(cleanfile).content
                        #print (html)
                        time.sleep(8)
                        matches = re.compile("var url = '(.*?)';").findall (html)
                        print (matches)
                        gourl=matches[0]
                        print 'THIS IS THE GO URL WE WANT==============================================     '+str(gourl)
                        url1='https://adf.ly'+str(gourl)
                        print 'THIS IS THE FULL ADFLY GOURL URL==================================================     '+str(url1)
                        html1 = net.http_GET(url1,{'Referer': str(url)}).content
                        
                        reallink = re.compile('META HTTP-EQUIV="Refresh" CONTENT="0; URL=(.+?)">').findall (html1)
                        hosturl=reallink[0]
                        print 'THIS IS THE RESOLVED URL WE WANT==============================================     '+str(hosturl)
                        time.sleep(5)
                        data = cache_page(str(hosturl))
                        file = get_match(data,'flashvars.file="([^"]+)"')
                        print (file)
                        key = get_match(data,'flashvars.filekey="([^"]+)"')
                        print (key)
                        codes = get_match(data,'flashvars.cid="([^"]+)"')
                        print (codes)
                        url = "http://www.nowvideo.eu/api/player.api.php?file="+file+"&user=undefined&codes="+codes+"&pass=undefined&key="+key.replace(".","%2E").replace("-","%2D")
                        data = cache_page(url)
                        location = get_match(data,'url=([^\&]+)&')
                        location = location + "?client=FLASH"
                        if not location:
                                location = 'CONTENTREMOVED'
                        print 'auth url is ' + str(location)
                        url=str(location)
                        iconimage='https://dl.dropbox.com/u/94360623/My-Repo/AWimages/NowVideo.png'
                        addLink(name,url,iconimage)
        except:
                pass
        try:
                for file1, name1, file, name in match9:
                        print 'MATCH9MATCH9MATC9=========='+str(match9)
                        name='NowV'+str(name)
                        cleanfile=str(qgs)+str(file)
                        html = net.http_GET(cleanfile).content
                        matches = re.compile("var url = '(.*?)';").findall (html)
                        gourl=matches[0]
                        print 'THIS IS THE GO URL WE WANT==============================================     '+str(gourl)
                        time.sleep(5)
                        html1 = net.http_GET('https://adf.ly/'+gourl).content
                        link1 = html1.encode('ascii', 'ignore')
                        reallink = re.compile('META HTTP-EQUIV="Refresh" CONTENT="0; URL=(.+?)">').findall (link1)
                        hosturl= reallink[0]
                        print 'THIS IS THE SOURCE WE WANT==============================================     '+str(hosturl)
                        time.sleep(5)
                        data = cache_page(str(hosturl))
                        file = get_match(data,'flashvars.file="([^"]+)"')
                        print (file)
                        key = get_match(data,'flashvars.filekey="([^"]+)"')
                        print (key)
                        codes = get_match(data,'flashvars.cid="([^"]+)"')
                        print (codes)
                        url = "http://www.nowvideo.eu/api/player.api.php?file="+file+"&user=undefined&codes="+codes+"&pass=undefined&key="+key.replace(".","%2E").replace("-","%2D")
                        data = cache_page(url)
                        location = get_match(data,'url=([^\&]+)&')
                        location = location + "?client=FLASH"
                        if not location:
                            location = 'CONTENTREMOVED'
                        print 'auth url is ' + str(location)
                        url=str(location)
                        iconimage='https://dl.dropbox.com/u/94360623/My-Repo/AWimages/NowVideo.png'
                        addLink(name,url,iconimage)
        except:
                pass
      
def cache_page(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        data=response.read()
        response.close()
        return data

def get_match(data, regex) :
        match = "";
        m = re.search(regex, data)
        if m != None :
                match = m.group(1)
                return match

def SEARCH(url):
        search_entered = ''
        keyboard = xbmc.Keyboard(search_entered, 'Search AwesomDL...XBMCHUB.COM')
        keyboard.doModal()
        if keyboard.isConfirmed():
                search_entered = keyboard.getText()#.replace(' ','+')# sometimes you need to replace spaces with + or %20#
        if search_entered == None or len(search_entered)<1:
                CATEGORIES()
        else:
                url = 'http://www.awesomedl.com/search?q=%s&x=0&y=0'%(search_entered).replace(' ','+')
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read().replace('\n','').replace('"','').replace('amp;','')
                response.close()
                match=re.compile("class='post-title entry-title'><a href='(.+?)'>(.+?)</a>.+?><img src=(.+?) alt=.+?<br><br>(.+?)<br>").findall(link)
                for url, name, iconim, desc in match:
                        addDir(name,url,2,iconim,desc)
                        #setView('movies', 'media info 2')
                match2=re.compile("<a class='blog-pager-older-link' href='(http://www.awesomedl.com/search.+?by-date=false)'").findall(link)
                print(match2)
                for url in match2:
                        iconimage=str(url)
                        addDir('Next Page',url,4,iconimage,'')

def SEARCHNEXTPAGE(url,iconimage):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        req.add_header('Referer', str(iconimage))
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        link1=link.replace('"','').replace('amp;','')
        match=re.compile("<a href='(.+?)'>(.+?)</a>\n</h3>\n<div class='post-header-line-1'></div>\n<div class='postmeta-primary'>\n<span class='meta_date'>.+?</span>\n.+?<span class='meta_comments'></span>\n</div>\n<div class='post-body entry-content'>\n<p>\n<div id='.+?'><img src=(.+?) alt=><br>\n<img src=.+?alt=><br>\n<br>\n(.+?)<br>").findall(link1)
        match1=re.compile("<a href='(.+?)'>(.+?)</a>\n</h3>\n<div class='post-header-line-1'></div>\n<div class='postmeta-primary'>\n<span class='meta_date'>.+?</span>\n.+?<span class='meta_comments'></span>\n</div>\n<div class='post-body entry-content'>\n<p>\n<div id='.+?'><img src=(.+?) alt=><br>\n<br>\n(.+?)<br>").findall(link1)
        try:
                for url,name, iconimage, description in match1:
                        addDir(name,url,2,iconimage,description)
        except:
                pass
        try:
                for url,name, iconimage, description in match:
                        addDir(name,url,2,iconimage,description)
        except:
                pass
        try:
                match2=re.compile("<a class='blog-pager-older-link' href='(.+?)' id=").findall(link1)
                match3=re.compile("<a class='blog-pager-newer-link' href='(.+?)' id=").findall(link1)
                url1= match2[0]
                iconimage= match3[0]
                addDir('Next Page',url1,1,iconimage,'')
                setView('movies', 'media info 2')
        except:
                pass

def Recommend10(url):
        req = urllib2.Request (url)
        print 'def recomend10======'+url
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        link1=link.replace('"','').replace('\n','')
        response.close()
        match1=re.compile("class='title'>Recommend Top 10 TV Shows</h2><div class='widget-content'>(.+?)</div>").findall(link1)
        match2 = re.compile('href=(.+?)>(.+?)-(.+?)</a>').findall(str(match1))
        for url1, number, name2 in match2:
                number=number.replace(' ','')
                dropbox='https://dl.dropbox.com/u/94360623/My-Repo/AWImages/'
                iconimage=dropbox+number+'.png'
                name=(number)+" - "+(name2)
                url=url1.replace(' ','%20')
                addDir(name,url,1,iconimage,'')
        match3=re.compile("<a class='blog-pager-older-link' href='(.+?)' id=").findall(link1)
        url1= match3[0]
        description=str(url)
        
def Recommend10NP(url,description):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        req.add_header('Referer', str(description))
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        link1=link.replace('"','').replace('amp;','').replace('\n','')
        match=re.compile("<a name='.+?<h3 class='post-title entry-title'>(.+?)alt=><br><br>.+?<br>").findall(link1)
        test=re.compile('a href=(.+?)>(.+?)<').findall(str(match))
        for url, name in test:
                print 'r10NP=================================='+str(url)
                addDir(name,url,2,'','')
        match2=re.compile("<a class='blog-pager-older-link' href='(.+?) title=").findall(str(link1))
        if str(match)==21:
                for url in match2:
                #print 'match2 url============================'+str(url)
                        description=str(url)
                        addDir('Next Page',url,6,'',description)

def NEWTVSHOWS(url,description):
        url = 'http://www.awesomedl.com'
        req = urllib2.Request (url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        link1=link.replace('"','')
        response.close()
        match=re.compile("<h2 class='title'>NEW TV SHOWS<(.+?)</div>", re.DOTALL).findall(str(link1))
        newshows=re.compile("href=(.+?)>(.+?)<").findall(str(match))
        for url, name in newshows:
                addDir(name,url,1,'','')
                                        
def setView(content, viewType):
         #set content type so library shows more views and info
        if content:
                xbmcplugin.setContent(int(sys.argv[1]), content)
        if ADDON.getSetting('auto-view') == 'true':
                xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )
                
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param




def addLink(name,url,iconimage):
        print 'DEF ADDLINK =========================='+(description)         
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok
        
        
def addDir(name,url,mode,iconimage,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description} )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
              
params=get_params()
url=None
name=None
mode=None
iconimage=None
description=None


try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:
        description=urllib.unquote_plus(params["description"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
       
elif mode==1:
        print ""+url
        INDEX(url)
        
elif mode==2:
        print ""+url
        VIDEOLINKS(url,name,iconimage)

elif mode==3:
        print ""+url
        SEARCH(url)
        
elif mode==4:
        print ""+url
        SEARCHNEXTPAGE(url,iconimage)

elif mode==5:
        print ""+url
        Recommend10(url)

elif mode==6:
        print ""+url
        Recommend10NP(url,description)

elif mode==7:
        print ""+url
        NEWTVSHOWS(url,description)
        

                
xbmcplugin.endOfDirectory(int(sys.argv[1]))
