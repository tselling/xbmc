# -*- coding: utf-8 -*-
#------------------------------------------------------------
# http://www.fastpasstv.ms/
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#------------------------------------------------------------

import os
import sys
import urlparse
import plugintools

import xbmcaddon
__settings__ = xbmcaddon.Addon(id="plugin.video.fastpasstv2")

# Entry point
def run():
    plugintools.log("fastpasstv.run")
    
    # Get params
    params = plugintools.get_params()
    
    if params.get("action") is None:
        main_list(params)
    else:
        action = params.get("action")
        exec action+"(params)"
    
    plugintools.close_item_list()

# Main menu
def main_list(params):
    plugintools.log("fastpasstv.main_list "+repr(params))

    # On first page, pagination parameters are fixed
    params["url"] = "http://www.fastpasstv.ms/channels/"

    THUMBNAIL_PATH = os.path.join( xbmc.translatePath( __settings__.getAddonInfo('Path') ) ,"art")
    
    plugintools.add_item( action="movies" , title="Movies" , plot="" , url="http://www.fastpasstv.ms/movies/" ,thumbnail=os.path.join(THUMBNAIL_PATH,"movie.png") , folder=True )
    plugintools.add_item( action="tvshows" , title="TV Shows" , plot="" , url="http://www.fastpasstv.ms/tv/" ,thumbnail=os.path.join(THUMBNAIL_PATH,"tv.png") , folder=True )
    plugintools.add_item( action="channel" , title="Documentaries" , plot="" , url="http://www.fastpasstv.ms/documentaries/" ,thumbnail=os.path.join(THUMBNAIL_PATH,"doc.png") , folder=True )
    plugintools.add_item( action="channel" , title="Cartoons" , plot="" , url="http://www.fastpasstv.ms/cartoons/" ,thumbnail=os.path.join(THUMBNAIL_PATH,"cartoon.png") , folder=True )

# Movie channel, four filter options
def movies(params):
    plugintools.log("fastpasstv.movies "+repr(params))

    plugintools.add_item( action="mostpopularmovies" , title="Most popular today" , plot="" , url="http://www.fastpasstv.ms/" ,thumbnail="" , folder=True )
    plugintools.add_item( action="featuredmovies" , title="Featured" , plot="" , url="http://www.fastpasstv.ms/" ,thumbnail="" , folder=True )
    plugintools.add_item( action="channel" , title="Alphabetic order" , plot="" , url=params.get("url") ,thumbnail="" , folder=True )
    plugintools.add_item( action="years" , title="Browse by year" , plot="" , url=params.get("url") ,thumbnail="" , folder=True )

# TV Shows channel, two filter options
def tvshows(params):
    plugintools.log("fastpasstv.tvshows "+repr(params))

    plugintools.add_item( action="mostpopulartvshows" , title="Most popular today" , plot="" , url="http://www.fastpasstv.ms/" ,thumbnail="" , folder=True )
    plugintools.add_item( action="channel" , title="Alphabetic order" , plot="" , url=params.get("url") ,thumbnail="" , folder=True )

# Most popular tv shows
def mostpopulartvshows(params):
    plugintools.log("fastpasstv.mostpopulartvshows "+repr(params))

    # Fetch page
    data = plugintools.read( params.get("url") )

    # Narrow search
    data = plugintools.find_single_match(data,'<h1 class="title">Most Popular TV Shows Today</h1>(.*?)</div>')
    
    # Extract items
    pattern = '<li><a title="[^"]+" href="([^"]+)[^>]+>([^<]+)</a></li>'
    matches = plugintools.find_multiple_matches(data,pattern)

    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle.strip()
        plot = ""
        thumbnail = ""
        url = urlparse.urljoin(params.get("url"),scrapedurl)

        # Appends a new item to the xbmc item list
        plugintools.add_item( action="mirrors" , title=title , plot=plot , url=url ,thumbnail=thumbnail , folder=True )

# Most popular movies
def mostpopularmovies(params):
    plugintools.log("fastpasstv.mostpopularmovies "+repr(params))

    # Fetch page
    data = plugintools.read( params.get("url") )

    # Narrow search
    data = plugintools.find_single_match(data,'<h1 class="title">Most Popular Movies Today</h1>(.*?)</div>')
    
    # Extract items
    pattern = '<li><a title="[^"]+" href="([^"]+)[^>]+>([^<]+)</a></li>'
    matches = plugintools.find_multiple_matches(data,pattern)

    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle.strip()
        plot = ""
        thumbnail = ""
        url = urlparse.urljoin(params.get("url"),scrapedurl)

        # Appends a new item to the xbmc item list
        plugintools.add_item( action="mirrors" , title=title , plot=plot , url=url ,thumbnail=thumbnail , folder=True )

# Featured movies
def featuredmovies(params):
    plugintools.log("fastpasstv.featuredmovies "+repr(params))

    # Fetch page
    data = plugintools.read( params.get("url") )

    # Narrow search
    data = plugintools.find_single_match(data,'<h1 class="title">Featured Movies</h1>(.*?)</div>')
    
    # Extract items
    pattern = '<td><a href="([^"]+)"><img src="([^"]+)" alt="([^"]+)"'
    matches = plugintools.find_multiple_matches(data,pattern)

    for scrapedurl,scrapedthumbnail,scrapedtitle in matches:
        title = scrapedtitle.strip()
        plot = ""
        thumbnail = urlparse.urljoin(params.get("url"),scrapedthumbnail)
        url = urlparse.urljoin(params.get("url"),scrapedurl)

        # Appends a new item to the xbmc item list
        plugintools.add_item( action="mirrors" , title=title , plot=plot , url=url ,thumbnail=thumbnail , folder=True )

# Movie channel, years filter
def years(params):
    plugintools.log("fastpasstv.years "+repr(params))

    # Fetch page
    data = plugintools.read( params.get("url") )

    # Narrow search
    data = plugintools.find_single_match(data,'<ul class="pagination[^<]+<b>Browse by Year(.*?)</ul>')
    
    # Extract items
    pattern = '<li><a href="([^"]+)[^>]+>([^<]+)</a></li>'
    matches = plugintools.find_multiple_matches(data,pattern)

    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle.strip()
        plot = ""
        thumbnail = ""
        url = urlparse.urljoin(params.get("url"),scrapedurl)

        # Appends a new item to the xbmc item list
        plugintools.add_item( action="channel" , title=title , plot=plot , url=url ,thumbnail=thumbnail , folder=True )

# Single channel, alphabetic filter
def channel(params):
    plugintools.log("fastpasstv.channel "+repr(params))

    # Fetch page
    data = plugintools.read( params.get("url") )

    # Narrow search    
    narrow = plugintools.find_single_match(data,'<ul class="pagination"(.*?)</ul>')
    
    # Extract items
    pattern = '<li[^<]+<a href="([^"]+)">([^<]+)</a></li>'
    matches = plugintools.find_multiple_matches(narrow,pattern)

    # Movie letters have a different pattern
    if len(matches)==0:
        narrow = plugintools.find_single_match(data,'<ul class="pagination[^<]+<b>Browse by Year.*?</ul[^<]+<ul class="pagination"(.*?)</ul>')
        pattern = '<li[^<]+<a.*?href="([^"]+)[^>]+>([^<]+)</a></li>'
        matches = plugintools.find_multiple_matches(narrow,pattern)

    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle.strip()
        plot = ""
        thumbnail = ""
        thumbnail_for_item = os.path.join( xbmc.translatePath( __settings__.getAddonInfo('Path') ) ,"art/"+title+".png")
        if os.path.exists( thumbnail_for_item ):
            thumbnail = thumbnail_for_item
        url = urlparse.urljoin(params.get("url"),scrapedurl)

        # Appends a new item to the xbmc item list
        plugintools.add_item( action="video_list" , title=title , plot=plot , url=url ,thumbnail=thumbnail , folder=True )

# Video list
def video_list(params):
    plugintools.log("fastpasstv.video_list "+repr(params))

    # Extract index from url
    url = params.get("url")

    if "#" in url:
        index = plugintools.find_single_match(url,'\#(.*?)$')
        plugintools.log("fastpasstv.video_list index="+index)
    
        url = plugintools.find_single_match(url,'(.*?)\#')
        plugintools.log("fastpasstv.video_list url="+url)
    else:
        index = ""

    # Fetch video list from page
    data = plugintools.read( url )

    # Narrow search to the selected letter (if present)
    if index!="":
        data = plugintools.find_single_match(data,'<h3 id="'+index+'">(.*?)</ul>')
        plugintools.log("data="+data)

    # Extract items
    pattern  = '<li[^<]+<a.*?href="([^"]+)">([^<]+)<span class="epnum">([^<]+)'
    matches = plugintools.find_multiple_matches(data,pattern)
    
    for scrapedurl,scrapedtitle,episodes in matches:
        title = scrapedtitle.strip()+" ("+episodes+")"
        plot = ""
        thumbnail = ""
        url = urlparse.urljoin(params.get("url"),scrapedurl)

        # Appends a new item to the xbmc item list
        if "/tv/" in url:
            plugintools.add_item( action="seasons" , title=title , plot=plot , url=url ,thumbnail=thumbnail , folder=True )
        else:
            plugintools.add_item( action="mirrors" , title=title , plot=plot , url=url ,thumbnail=thumbnail , folder=True )

# Seasons list
def seasons(params):
    plugintools.log("fastpasstv.seasons "+repr(params))

    # Extract index from url
    url = params.get("url")

    # Fetch video list from page
    data = plugintools.read( url )

    # Extract items
    pattern  = '<h3>(Season[^<]+)</h3><ul'
    matches = plugintools.find_multiple_matches(data,pattern)
    
    for scrapedtitle in matches:
        title = scrapedtitle.strip()
        plot = ""
        thumbnail = ""
        url = params.get("url")

        # Appends a new item to the xbmc item list
        plugintools.add_item( action="episodes" , title=title , plot=plot , url=url ,thumbnail=thumbnail , folder=True )

# Episodes list
def episodes(params):
    plugintools.log("fastpasstv.episodes "+repr(params))

    # Extract index from url
    url = params.get("url")

    # Fetch video list from page
    data = plugintools.read( url )
    season = plugintools.find_single_match(data,'<h3>'+params.get("title")+'</h3><ul(.*?)</ul>')
    plugintools.log("season="+season)
    if season=="":
        season = plugintools.find_single_match(data,'<h3>'+params.get("title")+'</h3><ul(.*?)</div>')
        plugintools.log("season="+season)

    # Extract items
    pattern  = '<li class="episode"><a href="([^"]+)">([^<]+)</a></li>'
    matches = plugintools.find_multiple_matches(season,pattern)
    
    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle.strip()
        plot = ""
        thumbnail = ""
        url = urlparse.urljoin(params.get("url"),scrapedurl)

        # Appends a new item to the xbmc item list
        plugintools.add_item( action="mirrors" , title=title , plot=plot , url=url ,thumbnail=thumbnail , folder=True )

#
def mirrors(params):
    plugintools.log("fastpasstv.mirrors "+repr(params))

    # Fetch video page and search for the media url
    data = plugintools.read( params.get("url") )
    pattern  = '<tr[^<]+<td[^<]+<b>([^<]+)</b></td>[^<]+<td class="siteparts"[^<]+<a class="link" href="([^"]+)[^>]+>Watch This Video'
    matches = plugintools.find_multiple_matches(data,pattern)
    
    for scrapedtitle,scrapedurl in matches:
        title = scrapedtitle.strip()
        plot = ""
        thumbnail = ""
        url = urlparse.urljoin(params.get("url"),scrapedurl)

        # Appends a new item to the xbmc item list
        if not "idxden" in title and not "idbux" in title and not "idbull" in title and not "veehd" in title.lower():
            plugintools.add_item( action="play" , title=title , plot=plot , url=url ,thumbnail=thumbnail , folder=False )

def play(params):
    plugintools.log("fastpasstv.play "+repr(params))

    # Fetch video page and search for the media url
    data = plugintools.read( params.get("url") )

    import xbmc
    xbmc.executebuiltin((u'XBMC.Notification("Connecting", "Connecting with fastpasstv", 100)'))
    
    video_id = plugintools.find_single_match(data,'<input type="hidden" value="([^"]+)" id="video_id" />')
    plugintools.log("fastpasstv.play video_id="+video_id)
    video_host = plugintools.find_single_match(data,'<input type="hidden" value="([^"]+)" id="video_host" />')
    plugintools.log("fastpasstv.play video_host="+video_host)
    
    if video_id!="":
        page_url = build_server_url(video_id,video_host)
        plugintools.log("fastpasstv.play page_url="+page_url)
    else:
        redirect = plugintools.find_single_match(data,'<a href="(/redirect/[^"]+)">')
        if redirect!="":
            plugintools.log("fastpasstv.play redirect")
            redirect = urlparse.urljoin( params.get("url") , redirect )
            from core import scrapertools
            page_url = scrapertools.get_header_from_response(redirect,header_to_get="location")
            plugintools.log("fastpasstv.play page_url="+page_url)
            
            if "180upload" in page_url:
                video_host="one80upload"
            elif "flashx.tv" in page_url:
                video_host="flashx"
            elif "vidbull" in page_url:
                video_host="vidbull"
            elif "allmyvideos" in page_url:
                video_host="allmyvideos"
            elif "videobam" in page_url:
                video_host="videobam"
            elif "veehd" in page_url:
                video_host="veehd"
            elif "veoh" in page_url:
                video_host="veoh"
            
        else:
            return

    try:
        exec "from servers import "+video_host+" as server_module"
    except:
        if video_host=="":
            video_host="that hoster"
        import xbmcgui
        advertencia = xbmcgui.Dialog()
        resultado = advertencia.ok( "Unsupported hoster","Videos from "+video_host+" not supported yet")
        return

    import xbmc
    xbmc.executebuiltin((u'XBMC.Notification("Connecting", "Connecting with %s", 100)' % (video_host,)))

    try:
        video_urls = server_module.get_video_url(page_url)
        
        if len(video_urls)>0:
            mediaurl = video_urls[0][1]
            plugintools.log("fastpasstv.play mediaurl="+mediaurl)
        
            #plugintools.play_resolved_url( mediaurl )
            import xbmc,xbmcgui
            try:
                xlistitem = xbmcgui.ListItem( params.get("title"), iconImage="DefaultVideo.png", path=mediaurl)
            except:
                xlistitem = xbmcgui.ListItem( params.get("title"), iconImage="DefaultVideo.png", )
            xlistitem.setInfo( "video", { "Title": params.get("title") } )

            import xbmc
            xbmc.executebuiltin((u'XBMC.Notification("Connecting", "Launching video player", 100)'))

            playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
            playlist.clear()
            playlist.add( mediaurl, xlistitem )
        
            player_type = xbmc.PLAYER_CORE_AUTO
            xbmcPlayer = xbmc.Player( player_type )
            xbmcPlayer.play(playlist)
        else:
            import xbmcgui
            advertencia = xbmcgui.Dialog()
            resultado = advertencia.ok( "Media URL not found","The URL for this video cannot be found","or video has been removed")
    except:
        import xbmc
        xbmc.executebuiltin((u'XBMC.Notification("Connecting", "Connection ERROR", 100)'))
        
        import traceback,sys
        from pprint import pprint
        exc_type, exc_value, exc_tb = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_tb)
        for line in lines:
            line_splits = line.split("\n")
            for line_split in line_splits:
                plugintools.log(line_split)

        import xbmcgui
        advertencia = xbmcgui.Dialog()
        resultado = advertencia.ok( "Error found","An error occurred while trying to play video","Please try other server")

def build_server_url(vid,vhost):

    url=""
    if vhost == "nolinks":
        url=""
    
    elif vhost == "youtube":
        url="http://www.youtube.com/v/" + vid
    elif vhost == "videozer":
        url="http://www.videozer.com/embed/" + vid
    elif vhost == "stagevu":
        url="http://stagevu.com/embed?width=640&height=480&background=000&uid=" + vid
    elif vhost  == "movshare":
        url="http://www.movshare.net/embed/" + vid
    elif vhost  == "vidbux":
        url="http://www.vidbux.com/embed-" + vid + "-width-640-height-480.html"
    elif vhost  == "videoweed":
        url="http://embed.videoweed.com/embed.php?v=" + vid + "&width=640&height=480"
    elif vhost  == "putlocker":
        url="http://www.putlocker.com/embed/" + vid
    elif vhost  == "loombo":
        url="http://loombo.com/embed-" + vid + "-640x480.html"
    elif vhost  == "divxden" or vhost == "vidxden":
        url="http://www.vidxden.com/embed-" + vid + ".html"
    elif vhost  == "novamov":
        url="http://www.novamov.com/embed.php?v=" + vid
    elif vhost  == "youku":
        url="http://player.youku.com/player.php/sid/' + vid + '=/v.swf"
    elif vhost  == "smotri":
        url="http://pics.smotri.com/scrubber_custom8.swf?file=" + vid + "&bufferTime=3&autoStart=false&str_lang=rus&xmlsource=http%3A%2F%2Fpics%2Esmotri%2Ecom%2Fcskins%2Fblue%2Fskin%5Fcolor%2Exml&xmldatasource=http%3A%2F%2Fpics%2Esmotri%2Ecom%2Fcskins%2Fblue%2Fskin%5Fng%2Exml"
    elif vhost  == "movreel":
        url="http://movreel.com/embed/" + vid
    elif vhost  == "royalvids":
        url="http://www.royalvids.eu/e.php?id=" + vid + "&width=650&height=418"
    elif vhost  == "zalaa":
        url="http://www.zalaa.com/embed-" + vid + ".html"
    elif vhost  == "divxcabin":
        url="http://www.divxcabin.com/embed-" + vid + ".html"
    elif vhost  == "divxstage":
        url="http://embed.divxstage.eu/embed.php?v=" + vid + "&width=600&height=400"
    elif vhost  == "uploadc":
        url="http://www.uploadc.com/embed-"+ vid +".html"
    elif vhost  == "sockshare":
        url="http://www.sockshare.com/embed/"+ vid
    elif vhost  == "gorillavid":
        url="http://gorillavid.in/player/player.swf"
    elif vhost  == "ovfile":
        url="http://ovfile.com/embed-"+ vid +"-650x481.html"
    elif vhost  == "filebox":
        url="http://filebox.com/embed-"+ vid +"-650x481.html"
    elif vhost  == "veevr":
        url="http://veevr.com/embed/"+ vid
    elif vhost  == "muchshare":
        url="http://muchshare.net/embed-"+ vid +".html"
    elif vhost  == "ufliq":
        url="http://www.ufliq.com/embed-"+ vid +".html"
    elif vhost == "xvidstage":
        url="http://xvidstage.com/embed-"+ vid +".html"
    elif vhost == "nowvideo":
        url="http://embed.nowvideo.eu/embed.php?v="+ vid +"&width=600&height=480"
    elif vhost == "vreer":
        url="http://vreer.com/embed-"+ vid +"-650x325.html"
    elif vhost == "vidhog":
        url="http://www.vidhog.com/embed-"+ vid +".html"
    elif vhost == "nosvideo":
        url="http://nosvideo.com/embed/"+ vid +"/640x360"
    elif vhost == "mooshare":
        url="http://mooshare.biz/embed-"+ vid +"-640x360.html"
    elif vhost == "hostingbulk":
        url="http://hostingbulk.com/embed-"+ vid +"-640x360.html"
    elif vhost == "xvidstream":
        url="http://xvidstream.net/embed-"+ vid +".html"
    elif vhost == "divxbase":
        url="http://www.divxbase.com/embed-"+ vid +"-640x360.html"
    elif vhost == "watchfreeinhd":
        url="http://www.watchfreeinhd.com/embed/"+ vid

    return url

run()