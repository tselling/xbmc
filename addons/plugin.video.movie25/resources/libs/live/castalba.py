import urllib,urllib2,re,cookielib
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
from resources.libs import main

#Mash Up - by Mash2k3 2012.

addon_id = 'plugin.video.movie25'
selfAddon = xbmcaddon.Addon(id=addon_id)

def CastalbaList(murl):
        try:
            urllist=['http://castalba.tv/channels/p=1','http://castalba.tv/channels/p=2']
        except:
            urllist=['http://castalba.tv/channels/p=1','http://castalba.tv/channels/p=2']
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until channel list is loaded.')
        totalLinks = len(urllist)
        loadedLinks = 0
        remaining_display = 'Pages loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0,'[B]Loading.....[/B]',remaining_display)
        for durl in urllist:
                link=main.OPENURL(durl)
                link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
                match=re.compile('<a href=".+?"><img src="..([^<]+)" alt="" />                                <span class=".+?">.+?</span>                                </a>                            <a href=".+?" class=".+?"><img src=".+?" alt="" /></a>                            </div>                        <div class=".+?"></div>                        <h4><a class=".+?"  href="..(.+?)">(.+?)</a></h4><p class=".+?" >In: <a href=".+?" class=".+?">(.+?)</a></p>').findall(link)
                for thumb,url,name,section in match:
                    if name != 'Playboy TV':
                        main.addPlay(name+'   [COLOR red]'+section+'[/COLOR]','http://castalba.tv'+url,123,'http://castalba.tv'+thumb)
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Pages loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Loading.....[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                        return False   
        dialogWait.close()
        del dialogWait
        main.GA("Castalba","List")

def CastalbaLink(mname,murl):
        main.GA("Castalba","Watched")
        link=main.OPENURL(murl)
        ok=True
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('<script type="text/javascript"> id="(.+?)"; ew="(.+?)"; eh="(.+?)";</script>').findall(link)
        for fid,wid,hei in match:
            pageUrl='http://castalba.tv/embed.php?cid='+fid+'&wh='+wid+'&ht='+hei
        link2=main.OPENURL(pageUrl)
        rtmp=re.compile("'streamer\': \'(.+?)\',").findall(link2)
        swfUrl=re.compile('flashplayer\': "(.+?)"').findall(link2)
        playPath=re.compile("'file\': \'(.+?)\',\r\n\r\n\t\t\t\'streamer\'").findall(link2)
        stream_url= rtmp[0] + ' playpath=' + playPath[0] + ' swfUrl=' + swfUrl[0] + ' live=true timeout=15 swfVfy=true pageUrl=' + pageUrl
        listitem = xbmcgui.ListItem(mname)
        playlist.add(stream_url,listitem)
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(playlist)
        return ok
