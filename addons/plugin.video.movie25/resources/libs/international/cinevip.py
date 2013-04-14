#-*- coding: utf-8 -*-
import urllib,urllib2,re,cookielib,urlresolver,os,sys
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
from resources.libs import main

#Mash Up - by Mash2k3 2012.

addon_id = 'plugin.video.movie25'
selfAddon = xbmcaddon.Addon(id=addon_id)


def LISTINT3(url):
        urllist=['http://www.cinevip.org/','http://www.cinevip.org/page/2','http://www.cinevip.org/page/3','http://www.cinevip.org/page/4','http://www.cinevip.org/page/5','http://www.cinevip.org/page/6','http://www.cinevip.org/page/7','http://www.cinevip.org/page/8','http://www.cinevip.org/page/9','http://www.cinevip.org/page/10']
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Movie list is cached.')
        totalLinks = len(urllist)
        loadedLinks = 0
        remaining_display = 'Pages loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0,'[B]Loading....[/B]',remaining_display)
        for murl in urllist:
                link=main.OPENURL(murl)
                match=re.compile('<a class="entry-thumbnails-link" href="(.+?)"><img width=".+?" height=".+?" src="(.+?)" class=".+?" alt=".+? Genero:(.+?) Titulo:.+? Info:(.+?) Sinopsis:(.+?)" title="(.+?)" />').findall(link)
                for url,thumb,genre,lang,desc,name in match:
                        lang ='[COLOR red]'+lang+'[/COLOR]'
                        lang = lang.replace('Audio','').replace('Español','').replace('Subtitulos','[COLOR blue]Sub(ESP)[/COLOR]').replace('DVDRip','')
                        name=name.replace(') Online','').replace('Ver ','')
                        name=name+')'
                        main.addSport(name+' '+lang,url,67,thumb,desc,'',genre)
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Pages loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Loading....[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                        return False   
        dialogWait.close()
        del dialogWait
        main.GA("INT","Cinevip")


def LINKINT3(name,murl):
        sources = []
        main.GA("Cinevip","Watched")
        link=main.OPENURL(murl)
        ok=True
        match=re.compile('<span class=".+?">(.+?)</span></td>\n<td>(.+?)</td>\n<td>.+?</td>\n<td>.+?href=http://adf.ly/.+?/(.+?)>').findall(link)
        if len(match) == 0:
                match=re.compile('<span class=".+?">(.+?)</span></td>\n<td>(.+?)</td>\n<td>.+?</td>\n<td>.+?href="http://adf.ly/.+?/(.+?)"').findall(link)
        for host, lang, url in match:
                print url
                hosted_media = urlresolver.HostedMediaFile(url=url, title=host+' [COLOR red]'+lang+'[/COLOR]')
                sources.append(hosted_media)
        if (len(sources)==0):
                xbmc.executebuiltin("XBMC.Notification(Sorry!,Show doesn't have playable links,5000)")
      
        else:
                source = urlresolver.choose_source(sources)
                if source:
                        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Resolving Link,3000)")
                        stream_url = source.resolve()
                        if source.resolve()==False:
                                xbmc.executebuiltin("XBMC.Notification(Sorry!,Link Cannot Be Resolved,5000)")
                                return
                else:
                        stream_url = False
                        return
                listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png")
                listitem.setInfo('video', {'Title': name, 'Year': ''} )         
                xbmc.Player().play(stream_url, listitem)
                return ok
