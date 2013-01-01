import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os
import shutil
import subprocess
import urllib2,urllib
import re
import addon
USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
base='https://dl.dropbox.com/u/129714017/hubmaintenance/'
howto='https://dl.dropbox.com/u/24282292/XBMC%20HUB%20GUIDES/txts/advanced.txt'


ADDON=xbmcaddon.Addon(id='plugin.video.hubmaintenance')


def CATEGORIES():
        addDir('Upload Your LogFile','url',15,base+'images/logger.png',base+'images/fanart/expert.jpg','Adding Your Favourite Tweaks')
        addDir("How To Video's",howto,13,base+'images/VideoGuides.jpg',base+'images/fanart/gettingstarted.jpg','Safely delete all cache from plugins')
        addDir('Maintenance','url',9,base+'images/maintenance.jpg',base+'images/fanart/beginners.jpg','Safely delete all cache from plugins')
        addDir('Fixes','url',10,base+'images/fixes.jpg',base+'images/fanart/advanced.jpg','XBMC Fixes')
        addDir('Tweaks','url',11,base+'images/tweaks.jpg',base+'images/fanart/expert.jpg','Adding Your Favourite Tweaks')
        if xbmc.getCondVisibility('system.platform.ATV2'):
            addDir('Install Si02 For Eden','http://dl.dropbox.com/u/129714017/hubmaintenance/info/skin.txt',16,base+'images/si02.png',base+'images/fanart/expert.jpg','Adding Your Favourite Tweaks')
        setView('movies', 'MAIN')


def maintenance(url):
        addDir('Delete My Cache','url',3,base+'images/maintenance.jpg',base+'images/fanart/beginners.jpg','Safely delete all cache from plugins')
        addDir('Delete Thumbnails','url',1,base+'images/maintenance.jpg',base+'images/fanart/beginners.jpg','Delete all your thumbnails you will need to reboot XBMC and rebuild your libraries')
        addDir('Delete Packages','url',2,base+'images/maintenance.jpg',base+'images/fanart/advanced.jpg','Delete all you old zipped packages very safe but you wont be able to roll back')
        addDir('Update Lib File','url',12,base+'images/maintenance.jpg',base+'images/fanart/expert.jpg','Update you lib file for rtmp live streams')
        setView('movies', 'SUB')
        
def fixesdir(url):
        addDir('1Channel Eden Fix',base+'fix/1channelfix.txt',4,base+'images/fixes.jpg',base+'images/fanart/advanced.jpg','Fix 1channel issue Eden')
        addDir('1Channel.db Issues Fix ','url',8,base+'images/fixes.jpg',base+'images/fanart/advanced.jpg','Only Use this if you Know that it is your 1Channel.db is malformed \n\nIF YOU GET THIS MESSAGE IN YOUR LOG \n plugin.video.1channel/default.py \n"DatabaseError: database disk image is malformed"\nThen use this fix')
        addDir('1Channel/Icefilms Meta_Cache Fix','url',7,base+'images/fixes.jpg',base+'images/fanart/advanced.jpg','Only Use this if you Know that it is your meta_cache video_cache.db is malformed \n\nIF YOU GET THIS MESSAGE IN YOUR LOG \nlib/metahandler/metahandlers.py \n"DatabaseError: database disk image is malformed"\n\n Then use this fix')
        setView('movies', 'SUB')
        
def tweaksdir(url):
        addDir('Add Tuxens Advanced XML',base+'tweaks/tuxen.xml',5,base+'images/tweaks.jpg',base+'images/fanart/expert.jpg','Add advanced xml to sort your buffering if you have issues')
        addDir('Add Mikey1234 Advanced XML',base+'tweaks/mikeys.xml',5,base+'images/tweaks.jpg',base+'images/fanart/expert.jpg','Add advanced xml to sort your buffering if you have issues')
        addDir('Add 0 Cache Advanced XML',base+'tweaks/0cache.xml',5,base+'images/tweaks.jpg',base+'images/fanart/expert.jpg','Add advanced xml to sort your buffering if you have issues')
        addDir('Delete Advanced XML','url',14,base+'images/tweaks.jpg',base+'images/fanart/expert.jpg','Add advanced xml to sort your buffering if you have issues')
        if xbmc.getCondVisibility('system.platform.ATV2'):
            addDir('Add Skip Forward/Back 10 Mins',base+'tweaks/joystick.AppleRemote.xml',6,base+'images/tweaks.jpg',base+'images/fanart/expert.jpg','ATV2 must have so you can push up or down to skip 10 minutes back or forward')
        setView('movies', 'SUB')
        

def DownloaderClass(url,dest):
    dp = xbmcgui.DialogProgress()
    dp.create("XBMCHUB...Maintenance","Downloading & Copying File",'')
    urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))
 
def _pbhook(numblocks, blocksize, filesize, url=None,dp=None):
    try:
        percent = min((numblocks*blocksize*100)/filesize, 100)
        print percent
        dp.update(percent)
    except:
        percent = 100
        dp.update(percent)
    if dp.iscanceled(): 
        print "DOWNLOAD CANCELLED" # need to get this part working
        dp.close()
############################################################        STANDARD CACHE          ###############################################################  
  
def deletecachefiles(url):
    print '############################################################       DELETING STANDARD CACHE             ###############################################################'
    if xbmc.getCondVisibility('system.platform.ATV2'):
        atv2_cache_a = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')
        
        for root, dirs, files in os.walk(atv2_cache_a):
            file_count = 0
            file_count += len(files)
        
            if file_count > 0:

                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete ATV2 Cache Files", str(file_count) + " files found in 'Other'", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
        atv2_cache_b = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')
        
        for root, dirs, files in os.walk(atv2_cache_b):
            file_count = 0
            file_count += len(files)
        
            if file_count > 0:

                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete ATV2 Cache Files", str(file_count) + " files found in 'LocalAndRental'", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
              # Set path to Cydia Archives cache files
        archive_cache_path = '/var/cache/apt/archives/'
        try:    
            for root, dirs, files in os.walk(archive_cache_path):
                file_count = 0
                file_count += len(files)
                
            # Count files and give option to delete
                if file_count > 0:
        
                    dialog = xbmcgui.Dialog()
                    if dialog.yesno("Delete 'Archived' Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                    
                        cmd = ["su", "alpine", "apt-get clean"]
                        subprocess.call(cmd)
        except: 
            dialog = xbmcgui.Dialog()
            dialog.ok("XBMCHUB TEAM", "Cant Delete Please SSH Into ATV2 And Run", "apt-get autoclean   Brought To You By XBMCHUB.COM")
                              

    # Set path to What th Furk cache files
    wtf_cache_path = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.whatthefurk/cache'), '')
    if os.path.exists(wtf_cache_path)==True:    
        for root, dirs, files in os.walk(wtf_cache_path):
            file_count = 0
            file_count += len(files)
        
        # Count files and give option to delete
            if file_count > 0:
    
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete WTF Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
                
                # Set path to 4oD cache files
    channel4_cache_path= os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.4od/cache'), '')
    if os.path.exists(channel4_cache_path)==True:    
        for root, dirs, files in os.walk(channel4_cache_path):
            file_count = 0
            file_count += len(files)
        
        # Count files and give option to delete
            if file_count > 0:
    
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete 4oD Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
                
                # Set path to BBC iPlayer cache files
    iplayer_cache_path= os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.iplayer/iplayer_http_cache'), '')
    if os.path.exists(iplayer_cache_path)==True:    
        for root, dirs, files in os.walk(iplayer_cache_path):
            file_count = 0
            file_count += len(files)
        
        # Count files and give option to delete
            if file_count > 0:
    
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete BBC iPlayer Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
                
                
                # Set path to Simple Downloader cache files
    downloader_cache_path = os.path.join(xbmc.translatePath('special://profile/addon_data/script.module.simple.downloader'), '')
    if os.path.exists(downloader_cache_path)==True:    
        for root, dirs, files in os.walk(downloader_cache_path):
            file_count = 0
            file_count += len(files)
        
        # Count files and give option to delete
            if file_count > 0:
    
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete Simple Downloader Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
                
                # Set path to ITV cache files
    itv_cache_path = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.itv/Images'), '')
    if os.path.exists(itv_cache_path)==True:    
        for root, dirs, files in os.walk(itv_cache_path):
            file_count = 0
            file_count += len(files)
        
        # Count files and give option to delete
            if file_count > 0:
    
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete ITV Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
    dialog = xbmcgui.Dialog()
    dialog.ok("XBMCHUB TEAM", "       Thats It All Done Please Come Visit Again", "          Brought To You By XBMCHUB.COM")
    
    
############################################################        PACKAGES          ###############################################################    
          
def DeletePackages(url):
    print '############################################################       DELETING PACKAGES             ###############################################################'
    packages_cache_path = xbmc.translatePath(os.path.join('special://home/addons/packages', ''))
    try:    
        for root, dirs, files in os.walk(packages_cache_path):
            file_count = 0
            file_count += len(files)
            
        # Count files and give option to delete
            if file_count > 0:
    
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete Package Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                            
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                    dialog = xbmcgui.Dialog()
                    dialog.ok("XBMCHUB TEAM", "       Thats It All Done Please Come Visit Again", "          Brought To You By XBMCHUB.COM")
    except: 
        dialog = xbmcgui.Dialog()
        dialog.ok("XBMCHUB TEAM", "Bloody Packages Wont Delete Can Some Developer", "Sort It!!    Brought To You By XBMCHUB.COM")
        
        
############################################################        THUMBNAILS          ###############################################################    
        
def DeleteThumbnails(url):    
    print '############################################################       DELETING THUMBNAILS             ###############################################################'
    thumbnail_cache_path = xbmc.translatePath(os.path.join('special://home/userdata/Thumbnails',''))
    textures_cache_path = xbmc.translatePath(os.path.join('special://home/userdata/Database',''))
    if os.path.exists(thumbnail_cache_path)==True:    
        dialog = xbmcgui.Dialog()
        if dialog.yesno("Delete Thumbnails Cache Files", '', "Do you want to delete them?"):
            shutil.rmtree(thumbnail_cache_path)
            Textures=GetFile(textures_cache_path)
            Shrink(Textures)
            print '================AMMENDING=====    '+str(Textures)+'    ====================================='

            dialog = xbmcgui.Dialog()
            dialog.ok("XBMCHUB TEAM", "Please Reboot XBMC To Take Effect !!", "Brought To You By XBMCHUB.COM")
            
            
############################################################        1CHANNEL FIX         ###############################################################    
                
def OneChannel(url):
    dialog = xbmcgui.Dialog()
    if dialog.yesno("[B][COLOR red]WARNING !!![/B][/COLOR]", '[B]ARE YOU SURE YOU KNOW WHAT THIS DOES !?![/B]','', "[B][COLOR red]     AS YOU CANNOT GO BACK !!![/B][/COLOR]"):
        print '############################################################       1CHANNEL EDEN FIX           ###############################################################'
        path = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.1channel', ''))
        onechannel=os.path.join(path, 'default.py')
        os.remove(onechannel)
        print '========= REMOVING  '+str(onechannel)+'    =========================='
        link=OPEN_URL(url)
        a = open(onechannel,"w") 
        a.write(link)
        a.close()
        print '========= WRITING NEW  '+str(onechannel)+'=========================='
        dialog = xbmcgui.Dialog()
        dialog.ok("XBMCHUB TEAM", "       Thats It All Done Please Come Visit Again", "          Brought To You By XBMCHUB.COM")
        
    
############################################################        ADVANCE XML          ###############################################################    
    
def advancexml(url):
    print '############################################################       ADVANCE XML          ###############################################################'
    path = xbmc.translatePath(os.path.join('special://home/userdata',''))
    advance=os.path.join(path, 'advancedsettings.xml')
    try:
        os.remove(advance)
        print '========= REMOVING    '+str(advance)+'    ====================================='
    except:
        pass
    link=OPEN_URL(url)
    a = open(advance,"w") 
    a.write(link)
    a.close()
    print '========= WRITING NEW    '+str(advance)+'    =========================='
    dialog = xbmcgui.Dialog()
    dialog.ok("XBMCHUB TEAM", "       Thats It All Done Please Come Visit Again", "          Brought To You By XBMCHUB.COM")
    
############################################################        DELETE ADVANCE XML          ###############################################################    
def deleteadvancexml(url):
    print '############################################################       DELETING ADVANCE XML          ###############################################################'
    path = xbmc.translatePath(os.path.join('special://home/userdata',''))
    advance=os.path.join(path, 'advancedsettings.xml')
    os.remove(advance)
    dialog = xbmcgui.Dialog()
    dialog.ok("XBMCHUB TEAM", "       Thats It All Done Please Come Visit Again", "          Brought To You By XBMCHUB.COM")
    
############################################################        KEYMAPS          ###############################################################    
    
    
def joystick(url): 
    print '############################################################        KEYMAPS          ###############################################################'
    path = xbmc.translatePath(os.path.join('special://home/userdata/keymaps',''))
    joystick=os.path.join(path, 'joystick.AppleRemote.xml')
    try:
        os.remove(joystick)
        print '========= REMOVING    '+str(joystick)+'     =========================='
    except:
        pass
    link=OPEN_URL(url)
    a = open(joystick,"w") 
    a.write(link)
    a.close()
    print '========= WRITING NEW    '+str(joystick)+'     =========================='
    dialog = xbmcgui.Dialog()
    dialog.ok("XBMCHUB TEAM", "       Thats It All Done Please Come Visit Again", "          Brought To You By XBMCHUB.COM")
    
    
############################################################        CORRUPT META          ###############################################################    
    
def malformed(url):
    dialog = xbmcgui.Dialog()
    if dialog.yesno("[B][COLOR red]WARNING !!![/B][/COLOR]", '[B]ARE YOU SURE YOU KNOW WHAT THIS DOES !?![/B]','', "[B][COLOR red]     AS YOU CANNOT GO BACK !!![/B][/COLOR]"):
        print '############################################################        CORRUPT META          ###############################################################'
        path = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/script.module.metahandler/meta_cache',''))
        meta=os.path.join(path, 'video_cache.db')
        try:
            os.remove(meta)
            print '========= REMOVING  '+str(meta)+'     =========================='
        except:
            dialog = xbmcgui.Dialog()
            dialog.ok("XBMCHUB TEAM", "       CANT DELETE!!!!", "          Brought To You By XBMCHUB.COM")
        print '========= WRITING NEW   '+str(meta)+'     =========================='
        dialog = xbmcgui.Dialog()
        dialog.ok("XBMCHUB TEAM", "           REBOOT XBMC !!!!", "          Brought To You By XBMCHUB.COM")
        
############################################################        1CHANNEL.DB CORRUPT         ###############################################################    
    
def onechanneldb(url): 
    dialog = xbmcgui.Dialog()
    if dialog.yesno("[B][COLOR red]WARNING !!![/B][/COLOR]", '[B]ARE YOU SURE YOU KNOW WHAT THIS DOES !?![/B]','', "[B][COLOR red]     AS YOU CANNOT GO BACK !!![/B][/COLOR]"):
        print '############################################################        1CHANNEL.DB CORRUPT          ###############################################################'
        path = xbmc.translatePath(os.path.join('special://home/userdata/Database',''))
        onechanneldb=os.path.join(path, 'onechannelcache.db')
        try:
            os.remove(onechanneldb)
            print '========= REMOVING   '+str(onechanneldb)+'     =========================='
        except:
            dialog = xbmcgui.Dialog()
            dialog.ok("XBMCHUB TEAM", "       CANT DELETE!!!!", "          Brought To You By XBMCHUB.COM")
        print '========= WRITING NEW   '+str(onechanneldb)+'     =========================='
        dialog = xbmcgui.Dialog()
        dialog.ok("XBMCHUB TEAM", "           REBOOT XBMC !!!!", "          Brought To You By XBMCHUB.COM")
    
    
############################################################        LYB          ###############################################################    
    
    
def lib(url): 
    print '############################################################        LYB          ###############################################################'
    if xbmc.getCondVisibility("system.platform.windows"):
        path = xbmc.translatePath(os.path.join('C:\Program Files (x86)\XBMC\system\players\dvdplayer',''))
        lib=os.path.join(path, 'librtmp.dll')
        try:
            os.remove(lib)
        except:
            pass
        url = base+'lib/windows/librtmp.dll'
        DownloaderClass(url,lib)
        dialog = xbmcgui.Dialog()
        dialog.ok("XBMCHUB TEAM", "       Thats It All Done Please Come Visit Again", "          Brought To You By XBMCHUB.COM")
        
    if xbmc.getCondVisibility("system.platform.osx"):
        try:    
            path = xbmc.translatePath(os.path.join('/Applications/XBMC.app/Contents/Frameworks',''))
            lib=os.path.join(path, 'librtmp.0.dylib')
            try:
                os.remove(lib)
            except:
                pass
            url = base+'lib/mac/librtmp.0.dylib'
            DownloaderClass(url,lib)
            dialog = xbmcgui.Dialog()
            dialog.ok("XBMCHUB TEAM", "       Thats It All Done Please Come Visit Again", "          Brought To You By XBMCHUB.COM")
        except: 
            dialog = xbmcgui.Dialog()
            dialog.ok("XBMCHUB TEAM", "       CANT UPDATE YOUR LIB FILE SORRY!!!", "          Brought To You By XBMCHUB.COM")
        
    if xbmc.getCondVisibility("system.platform.ATV2"):
        try:    
            path = xbmc.translatePath(os.path.join('/private/var/stash/Applications/XBMC.frappliance/Frameworks',''))
            lib=os.path.join(path, 'librtmp.0.dylib')
            try:
                os.remove(lib)
            except:
                pass
            url = base+'lib/atv/librtmp.0.dylib'
            DownloaderClass(url,lib)
            dialog = xbmcgui.Dialog()
            dialog.ok("XBMCHUB TEAM", "       Thats It All Done Please Come Visit Again", "          Brought To You By XBMCHUB.COM")
        except: 
            dialog = xbmcgui.Dialog()
            dialog.ok("XBMCHUB TEAM", "       CANT UPDATE YOUR LIB FILE SORRY!!!", "          Brought To You By XBMCHUB.COM")
    
def Shrink(db):
    from sqlite3 import dbapi2 as sqlite3
    try:
        db   = xbmc.translatePath(db)
        conn = sqlite3.connect(db, timeout = 10, detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread = False)
        c    = conn.cursor()

        c.execute("DELETE FROM texture WHERE id > 0")       
        c.execute("VACUUM")       

        conn.commit()
        c.close()
    except:
        dialog = xbmcgui.Dialog()
        dialog.ok("XBMCHUB TEAM", "Sorry There Was A Problem Please Manually ", "Delete Textures.db")
        
    
def GetFile(filepath):
     import glob
     path = filepath
     for infile in glob.glob(os.path.join(path, 'Textures*.*')):
         File=infile
         print infile
     return File
    
     
def Youtube(url,fanart):
        link=OPEN_URL(url)
        link1=str(link).replace('\n','').replace('\r','').replace('\t','')
        match=re.compile('"i=(.+?) n=(.+?) u=(.+?) d=(.+?)"').findall(link1)
        for icon, name, youtube , description in match:
                if icon=='none':
                    iconimage = 'http://i.ytimg.com/vi/%s/0.jpg' % youtube
                else:
                    iconimage=str(icon)
                print iconimage
                fanart=str(fanart)
                url = 'plugin://plugin.video.youtube/?path=root/video&action=play_video&videoid=%s' % youtube
                addLink(name,url,iconimage,description,fanart)        
                setView('movies', 'videos') 
                
def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
     
def uploadlog(url):     
    addon.LogUploader()
    
    
    
def fastcoloreden(url,iconimage):     
        link=OPEN_URL(url)
        match=re.compile('skinurl="(.+?)" name"(.+?)" icon="(.+?)"').findall(link)
        for url,name,iconimage in match:
            addDir(name,url,17,iconimage,'','Download'+str(name))
            
def downloadanything(url,name):     
    path = xbmc.translatePath(os.path.join('/private/var/mobile',''))
    lib=os.path.join(path, name)
    DownloaderClass(url,lib)
    dialog = xbmcgui.Dialog()
    dialog.ok("XBMCHUB TEAM", "A New Window Will Now Open For You To ", "Install From Zip")
    xbmc.executebuiltin("XBMC.ActivateWindow(AddonBrowser)")

            
def addDir(name,url,mode,iconimage,fanart,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
def addLink(name,url,iconimage,description,fanart):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty("IsPlayable","true")
        liz.setProperty("Fanart_Image",fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
        return ok 
        
        
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
        
                      
params=get_params()
url=None
name=None
mode=None
iconimage=None
fanart=None
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
        mode=int(params["mode"])
except:
        pass
try:        
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass
                
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)


def setView(content, viewType):
    # set content type so library shows more views and info
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if ADDON.getSetting('auto-view') == 'true':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )
        
        
if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
       
elif mode==1:
        print ""+url
        DeleteThumbnails(url)
        
elif mode==2:
        print ""+url
        DeletePackages(url)

elif mode==3:
        print ""+url
        deletecachefiles(url)
        
elif mode==4:
        print ""+url +iconimage
        OneChannel(url)
        
elif mode==5:
        print ""+url +iconimage
        advancexml(url)
        
elif mode==6:
        print ""+url +iconimage
        joystick(url)
        
elif mode==7:
        print ""+url +iconimage
        malformed(url)
        
elif mode==8:
        print ""+url +iconimage
        onechanneldb(url)
        
elif mode==9:
        print ""+url +iconimage
        maintenance(url)
        
elif mode==10:
        print ""+url +iconimage
        fixesdir(url)
        
elif mode==11:
        print ""+url +iconimage
        tweaksdir(url)
        
elif mode==12:
        print ""+url +iconimage
        lib(url)
        
elif mode==13:
        print ""+url +iconimage
        Youtube(url,fanart)
        
elif mode==14:
        print ""+url +iconimage
        deleteadvancexml(url)
        
elif mode==15:
        print ""+url +iconimage
        uploadlog(url)
        
elif mode==16:
        print ""+url +iconimage
        fastcoloreden(url,iconimage)
        
elif mode==17:
        print ""+url +iconimage
        downloadanything(url,name)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
