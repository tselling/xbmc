# -*- coding: utf-8 -*-
#------------------------------------------------------------
# RadioReference.com
#------------------------------------------------------------
# Based on code from pelisalacarta
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item

DEBUG = config.get_setting("debug")
URL = "http://www.radioreference.com/apps/audio/"
IMAGES = os.path.join(config.get_runtime_path(),"resources")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[channel.py] mainlist")
    item.url = URL
    return countries(item)

def countries(item):
    logger.info("[channel.py] countries")
    itemlist = []

    # Descarga la home
    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,'<span style="[^"]+">Choose Country.</span[^<]+<select[^>]+>(.*?)</select>')
    logger.info("data="+str(data))

    patron = '<option value="([^"]+)">([^<]+)</option>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    if len(matches)==0:
        return []

    for code,title in matches:
        url="http://www.radioreference.com/apps/audio/?coid="+code
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"]")
        thumbnail = os.path.join(IMAGES,"flags",code+".png")
        itemlist.append( Item(action="states", title=title , url=url, thumbnail=thumbnail, viewmode=1 ) )
    
    return itemlist

def states(item):
    logger.info("[channel.py] states")
    itemlist = []

    # Descarga la home
    data = scrapertools.cache_page(item.url)
    
    # Search for states combo
    try:
        data2 = scrapertools.get_match(data,'<form method="GET" action="/apps/audio/"><select size="1" name="stid"(.*?)</selec')
        patron = '<option value="([^"]+)">([^<]+)</option>'
        matches = re.compile(patron,re.DOTALL).findall(data2)
        if DEBUG: scrapertools.printMatches(matches)
    
        for code,title in matches:
            url="http://www.radioreference.com/apps/audio/?stid="+code
            if (DEBUG): logger.info("title=["+title+"], url=["+url+"]")
            itemlist.append( Item(action="county", title=title , url=url) )
    except:
        pass

    if len(itemlist)>0:
        return itemlist

    # Search for states urls without repeating
    #<a href="/apps/audio/?stid=158">Australian Capital Territory</a>
    try:
        patron = '<a href="/apps/audio/\?stid\=(\d+)">([^<]+)</a>'
        matches = re.compile(patron,re.DOTALL).findall(data)
        if DEBUG: scrapertools.printMatches(matches)
        encontrados = set()

        for code,title in matches:
            if code not in encontrados:    
                url="http://www.radioreference.com/apps/audio/?stid="+code
                if (DEBUG): logger.info("title=["+title+"], url=["+url+"]")
                itemlist.append( Item(action="county", title=title , url=url) )
                encontrados.add(code)

    except:
        pass
    
    return itemlist

def county(item):
    logger.info("[channel.py] county")

    # Descarga la home
    data = scrapertools.cache_page(item.url)
    itemlist = parse_counties(data,'<option value="ctid,([^"]+)">([^<]+)</option>',"http://www.radioreference.com/apps/audio/?ctid=")
    if len(itemlist)>0:
        return itemlist

    itemlist = parse_counties(data,'<option value="mid,([^"]+)">([^<]+)</option>',"http://www.radioreference.com/apps/audio/?mid=")
    if len(itemlist)>0:
        return itemlist

    itemlist = parse_counties(data,'<a href="/apps/audio/\?ctid\=(\d+)">([^<]+)</a>',"http://www.radioreference.com/apps/audio/?ctid=")
    if len(itemlist)>0:
        return itemlist

    itemlist = parse_counties(data,'<a href="/apps/audio/\?mid\=(\d+)">([^<]+)</a>',"http://www.radioreference.com/apps/audio/?mid=")

    return itemlist

def parse_counties(data,patron,baseurl):
    itemlist=[]
    
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for code,title in matches:
        url=baseurl+code
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"]")
        itemlist.append( Item(action="feeds", title=title , url=url) )

    return itemlist

def feeds(item):
    logger.info("[channel.py] feeds")
    itemlist = []

    # Descarga la home
    data = scrapertools.cache_page(item.url)
    logger.info("data="+data)
    
    if "No feeds available for this" in data or "You have an error in your SQL syntax" in data:
        thumbnail = os.path.join(IMAGES,"images","Actions-application-exit-icon.png")
        itemlist.append( Item(action="play", title="No feeds available for this area." , thumbnail=thumbnail, url="", folder=False) )
    else:
        
        # Feed table
        data = scrapertools.get_match(data,'<table class="rrtable"(.*?)</table>')
        
        # Row pattern
        patron = '<td class="w1p">(.*?)</tr>'
        matches = re.compile(patron,re.DOTALL).findall(data)
        if DEBUG: scrapertools.printMatches(matches)
    
        for match in matches:
            try:
                code = scrapertools.get_match(match,'<a href="/apps/audio/.feedId\=(\d+)')
            except:
                code = ""
            try:
                title = scrapertools.get_match(match,'<a href="/apps/audio/.feedId\=\d+"><span[^>]+>([^<]+)</span></a>')
            except:
                title = ""
            try:
                subtitle = scrapertools.get_match(match,'<span class="rrfont">([^<]+)</span>')
            except:
                subtitle = ""
            try:
                feedtype = scrapertools.get_match(match,'<td class="c" nowrap>([^<]+)<.*?<td class="c" nowrap>[^<]+</td>.*?')
            except:
                feedtype = ""
            try:
                listeners = scrapertools.get_match(match,'<td class="c" nowrap>[^<]+<.*?<td class="c" nowrap>([^<]+)</td>.*?')
            except:
                listeners = ""
            try:
                #<b>Online</b></td>    </tr>
                status = scrapertools.get_match(match,'<b>([^<]+)</b></td>[^<]+</tr>')
            except:
                status = ""
                
            fulltitle = title.strip() + " (" + feedtype.strip() + ")" + "(" + listeners.strip() + " listeners)" + "(" + status.strip() + ")"
            url="http://www.radioreference.com/scripts/playlists/ep.php?feedId="+code
            thumbnail = os.path.join(IMAGES,"images","radio-icon.png")
            if (DEBUG): logger.info("title=["+title+"], url=["+url+"]")
            itemlist.append( Item(action="play", title=fulltitle , url=url, plot=subtitle, thumbnail=thumbnail, folder=False) )

    return itemlist

def play(item):
    itemlist = []

    if item.url!="":
        # Descarga la home
        data = scrapertools.cache_page(item.url)
        location = scrapertools.get_match(data,"<location>([^<]+)</location>")
        itemlist.append( Item(action="play", title=item.title , server="directo", url=location, fanart=os.path.join(config.get_runtime_path(),"fanart.jpg"), folder=False) )
    
    return itemlist

def test():
    mainlist_items = mainlist(Item())
    
    for mainlist_item in mainlist_items:
        if mainlist_item.title!="United States":
            f = open("salida.txt","a")
            f.write(mainlist_item.title+"\n")
            f.close()
            print_child_items("",mainlist_item)
        
def print_child_items(margen,item):
    exec "itemlist = "+item.action+"(item)"

    for item in itemlist:
        f = open("salida.txt","a")
        f.write(margen+"  "+item.title+"\n")
        f.close()
        if item.action!="play":
            print_child_items(margen+"  ",item)
