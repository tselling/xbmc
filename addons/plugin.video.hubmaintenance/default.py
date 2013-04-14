import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os
import shutil
import subprocess
import urllib2,urllib
import re
import addon
import datetime
import time

USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
base='http://dl.dropbox.com/u/129714017/hubmaintenance/'
howto='http://dl.dropbox.com/u/129714017/XBMC%20HUB%20GUIDES/txts/howto.txt'
hubpath = xbmc.translatePath(os.path.join('special://home/addons', ''))
hubrepo=os.path.join(hubpath, 'repository.xbmchub')
mikey=os.path.join(hubpath, 'repository.Mikey1234')
ADDON=xbmcaddon.Addon(id='plugin.video.hubmaintenance')
boxbackupzip=ADDON.getSetting('boxbackupzip')+'.zip'
dropboxnumber=ADDON.getSetting('boxnumber')
boxuserdata='https://dl.dropbox.com/u/%s/%s'%(dropboxnumber,boxbackupzip)
linux_download=ADDON.getSetting('download_linux')
wallpaper_download=ADDON.getSetting('download_wallpaper')
hd_wallurl='http://www.hdwallpapers.in'
wallurl='http://wallpaperswide.com'
if ADDON.getSetting('visitor_ga')=='':
    from random import randint
    ADDON.setSetting('visitor_ga',str(randint(0, 0x7fffffff)))

VERSION = "4.8f"
PATH = "HUBMAINTENANCE"            
UATRACK="UA-35537758-1"   

if os.path.exists(mikey)==True: 
    for root, dirs, files in os.walk(mikey):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))
    os.rmdir(mikey)


def DownloaderClass(url,dest, useReq = False):
    dp = xbmcgui.DialogProgress()
    dp.create("XBMCHUB...Maintenance","Downloading & Copying File",'')

    if useReq:
        import urllib2
        req = urllib2.Request(url)
        req.add_header('Referer', 'http://wallpaperswide.com/')
        f       = open(dest, mode='wb')
        resp    = urllib2.urlopen(req)
        content = int(resp.headers['Content-Length'])
        size    = content / 100
        total   = 0
        while True:
            if dp.iscanceled(): 
                raise Exception("Canceled")                
                dp.close()

            chunk = resp.read(size)
            if not chunk:            
                f.close()
                break

            f.write(chunk)
            total += len(chunk)
            percent = min(100 * total / content, 100)
            dp.update(percent)       
    else:
        urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))
 
def _pbhook(numblocks, blocksize, filesize, url=None,dp=None):
    try:
        percent = min((numblocks*blocksize*100)/filesize, 100)
        dp.update(percent)
    except:
        percent = 100
        dp.update(percent)
    if dp.iscanceled(): 
        raise Exception("Canceled")
        dp.close()
    ############################################################        Remove Mikey        ###############################################################
try:  
    if os.path.exists(hubrepo)==False: 
        dialog = xbmcgui.Dialog()
        dialog.ok("XBMCHUB TEAM", "XBMCHUB Repo Is Going To Install Reboot To Take", "Effect   Brought To You By XBMCHUB.COM")
        print '############################################################        INSTALL XBMCHUB REPO        ###############################################################'
        url = 'http://xbmc-hub-repo.googlecode.com/svn/addons/repository.xbmchub/repository.xbmchub-1.0.1.zip'
        path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
        lib=os.path.join(path, 'repository.xbmchub-1.0.1.zip')
        DownloaderClass(url,lib)
        addonfolder = xbmc.translatePath(os.path.join('special://home/addons',''))
        time.sleep(2)
        xbmc.executebuiltin("XBMC.Extract(%s,%s)"%(lib,addonfolder))
except:
    pass        
    
    



def CATEGORIES():
        addDir("How To Video's",howto,13,base+'images/VideoGuides.jpg',base+'images/fanart/gettingstarted.jpg','Safely delete all cache from plugins')
        addDir('Maintenance','url',9,base+'images/maintenance.jpg',base+'images/fanart/beginners.jpg','Safely delete all cache from plugins')
        addDir('Fixes','url',10,base+'images/fixes.jpg',base+'images/fanart/advanced.jpg','XBMC Fixes')
        addDir('Tweaks','url',11,base+'images/tweaks.jpg',base+'images/fanart/expert.jpg','Adding Your Favourite Tweaks')
        addDir("Wallpaper Downloads",howto,48,base+'images/wallpapers.jpg',base+'images/fanart/gettingstarted.jpg','Safely delete all cache from plugins')
        addDir('Fusion Installer','url',18,base+'images/fusion.jpg',base+'images/fanart/expert.jpg','Fusion Installer')
        if os.path.exists(hubrepo)==False: 
            addDir('Install XBMCHUB Repo','url',21,base+'repoinstalls/xbmchubrepo/icon.png',base+'repoinstalls/xbmchubrepo/fanart.jpg','Install XBMCHUB Repo')
        addDir('Upload Your LogFile','url',15,base+'images/logger.png',base+'images/fanart/expert.jpg','Adding Your Favourite Tweaks')
        addDir('Install Si02 For Eden','http://dl.dropbox.com/u/129714017/hubmaintenance/info/skin.txt',16,base+'images/si02.png',base+'images/fanart/expert.jpg','Adding Your Favourite Tweaks')
        if xbmc.getCondVisibility('system.platform.android'):
            addDir('Anything Android','url',36,base+'images/recover.jpg',base+'images/fanart/expert.jpg','')
        if xbmc.getCondVisibility('system.platform.linux'):
            addDir('All Linux','url',38,base+'images/linux.jpg',base+'images/fanart/expert.jpg','Anything Linux')
        addDir('Need Help??','url',2000,base+'images/help.jpg',base+'images/fanart/expert.jpg','Fusion Installer')
        setView('movies', 'MAIN')
        
def alllinux(url):
        addDir('Flash Linux','http://www.pivosforums.com/viewtopic.php?f=11&t=941',33,base+'images/linux.jpg',base+'images/fanart/expert.jpg','Flash Your Box With Linux And Open Your World !!')
        addDir('Flash Toys4Me Linux','url',42,base+'images/linux.jpg',base+'images/fanart/expert.jpg','Flash Your Box With Linux And Open Your World !!')
        addDir('Enter Recovery/Upgrade','url',19,base+'images/linux.jpg',base+'images/fanart/expert.jpg','Fed up with holding that stupid upgrade button down just use this make sure your upgrade image is on card and plugged in')
        setView('movies', 'SUB')
def allandroid(url):
        addDir("Add GSH's PlayerCore.xml",'http://dl.dropbox.com/u/129714017/hubmaintenance/playercorefactory.xml',37,base+'images/recover.jpg',base+'images/fanart/expert.jpg','Change your playercorefactory hardware accelerated players to gsh xml')
        addDir('Flash Linux Linux','http://www.pivosforums.com/viewtopic.php?f=11&t=941',33,base+'images/recover.jpg',base+'images/fanart/expert.jpg','See If There Is A New Image For You')
        addDir('Flash Toys4Me','url',42,base+'images/linux.jpg',base+'images/fanart/expert.jpg','Flash Your Box With Linux And Open Your World !!')
        addDir('Enter Recovery/Upgrade','url',19,base+'images/recover.jpg',base+'images/fanart/expert.jpg','Fed up with holding that stupid upgrade button down just use this make sure your upgrade image is on card and plugged in')
        setView('movies', 'SUB')

def maintenance(url):
        addDir('Download All Repos','http://dl.dropbox.com/u/129714017/hubmaintenance/allrepos.zip',35,base+'repoinstalls/xbmchubrepo/icon.png',base+'repoinstalls/xbmchubrepo/fanart.jpg','Install All Popular Repos In One Click All Repos From Fusion')
        addDir('Remove Addons','plugin.',25,base+'images/recycle.png',base+'images/fanart/beginners.jpg','Safely Remove Unwanted plugins')
        addDir('Remove Repos','repository.',25,base+'images/recycle.png',base+'images/fanart/beginners.jpg','Safely Remove Unwanted Repositories')
        addDir('Remove Skins','skin.',25,base+'images/recycle.png',base+'images/fanart/beginners.jpg','Safely Remove Unwanted Skins')
        addDir('Delete My Cache','url',3,base+'images/maintenance.jpg',base+'images/fanart/beginners.jpg','Safely delete all cache from plugins')
        #addDir('Delete Stale Thumbnails','url',111,base+'images/maintenance.jpg',base+'images/fanart/beginners.jpg','Delete stale thumbnails and textures')
        addDir('Delete Packages','url',2,base+'images/maintenance.jpg',base+'images/fanart/advanced.jpg','Delete all you old zipped packages very safe but you wont be able to roll back')
        addDir('Delete Crash Logs','url',1,base+'images/maintenance.jpg',base+'images/fanart/advanced.jpg','Delete all your old crash logs')
        if xbmc.getCondVisibility('system.platform.ATV2')or xbmc.getCondVisibility('system.platform.windows') or xbmc.getCondVisibility('system.platform.osx') or xbmc.getCondVisibility('system.platform.android'):
            addDir('Update Lib File','url',12,base+'images/maintenance.jpg',base+'images/fanart/expert.jpg','Update you lib file for rtmp live streams')
        setView('movies', 'SUB')
        
def fixesdir(url):
        addDir('Hulu Fix',base+'fix/script.module.cryptopy.zip',39,base+'images/hulu.png',base+'images/fanart/advanced.jpg','Fix For Hulu')
        addDir('YouTube Fix',base+'',30,base+'images/fixes.jpg',base+'images/fanart/advanced.jpg','Fix For YouTube')
        addDir('ITV Player Fix',base+'',31,base+'fix/icon.png',base+'images/fanart/advanced.jpg','Get More Results From ITV With This Fix')
        addDir('1Channel Eden Fix',base+'fix/1channelfix.txt',4,base+'images/fixes.jpg',base+'images/fanart/advanced.jpg','Use This If you Get This Error in your Log \n"listitem.addContextMenuItems(cm, replaceItems=True)"')
        addDir('1Channel Reboot Fix',base+'fix/1channelfix.txt',20,base+'images/fixes.jpg',base+'images/fanart/advanced.jpg','Having problems with having to reboot xbmc to view next movie or tv show then this is your fix for that')
        addDir('1Channel Subtitles Fix',base+'fix/1channelfix.txt',27,base+'images/fixes.jpg',base+'images/fanart/advanced.jpg','Use This To Fix Subtitles Not Working')
        addDir('1Channel.db Issues Fix ','url',8,base+'images/fixes.jpg',base+'images/fanart/advanced.jpg','Only Use this if you Know that it is your 1Channel.db is malformed \n\nIF YOU GET THIS MESSAGE IN YOUR LOG \n plugin.video.1channel/default.py \n"DatabaseError: database disk image is malformed"\nThen use this fix')
        addDir('1Channel/Icefilms Meta_Cache Fix','url',7,base+'images/fixes.jpg',base+'images/fanart/advanced.jpg','Only Use this if you Know that it is your meta_cache video_cache.db is malformed \n\nIF YOU GET THIS MESSAGE IN YOUR LOG \nlib/metahandler/metahandlers.py \n"DatabaseError: database disk image is malformed"\n\n Then use this fix')
        addDir('Extend Captcha Times','url',24,base+'images/maintenance.jpg',base+'images/fanart/beginners.jpg','If you can never see the captchas for long enough please install this it will give you 5 seconds to read the captcha before the keyboard pops up')
        addDir('Fix Slow Gui Issues','url',28,base+'images/maintenance.jpg',base+'images/fanart/beginners.jpg','Fix Slow GUI (Not Necessarily Going To Work For All!!)')
        setView('movies', 'SUB')
        
def tweaksdir(url):
        addDir('Confluence 7 Icons (Frodo Only)','url',40,base+'images/tweaks.jpg',base+'images/fanart/expert.jpg','Add 7 Icons To Your Home Menu For Video')
        addDir('Add Tuxens Advanced XML',base+'tweaks/tuxen.xml',5,base+'images/tweaks.jpg',base+'images/fanart/expert.jpg','Add advanced xml to sort your buffering if you have issues')
        addDir('Add Mikey1234 Advanced XML',base+'tweaks/mikeys.xml',5,base+'images/tweaks.jpg',base+'images/fanart/expert.jpg','Add advanced xml to sort your buffering if you have issues')
        addDir('Add 0 Cache Advanced XML',base+'tweaks/0cache.xml',5,base+'images/tweaks.jpg',base+'images/fanart/expert.jpg','Add advanced xml to sort your buffering if you have issues')
        addDir('Check What XML You Are Using','url',29,base+'images/tweaks.jpg',base+'images/fanart/expert.jpg','Check what advancedsettings.xml your are using')
        addDir('Delete Advanced XML','url',14,base+'images/tweaks.jpg',base+'images/fanart/expert.jpg','Add advanced xml to sort your buffering if you have issues')
        if xbmc.getCondVisibility('system.platform.ATV2'):
            addDir('Add Skip Forward/Back 10 Mins',base+'tweaks/joystick.AppleRemote.xml',6,base+'images/tweaks.jpg',base+'images/fanart/expert.jpg','ATV2 must have so you can push up or down to skip 10 minutes back or forward')
        setView('movies', 'SUB')
        
def wallpaper_catergories():
        addDir("wallpaperswide.com",howto,44,base+'images/wallpaperwide.png',base+'images/fanart/gettingstarted.jpg','Safely delete all cache from plugins')
        addDir("hdwallpapers.in",howto,49,'http://www.hdwallpapers.in/templates/custom/images/logo.png',base+'images/fanart/gettingstarted.jpg','Safely delete all cache from plugins')
        
        
############################################################        STANDARD CACHE          ###############################################################  
  
def deletecachefiles(url):
    GA("Maintenance","Delete Cache")
    print '############################################################       DELETING STANDARD CACHE             ###############################################################'
    xbmc_cache_path = os.path.join(xbmc.translatePath('special://home'), 'cache')
    if os.path.exists(xbmc_cache_path)==True:    
        for root, dirs, files in os.walk(xbmc_cache_path):
            file_count = 0
            file_count += len(files)
        
        # Count files and give option to delete
            if file_count > 0:
    
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete XBMC Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
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
        archive_cache_path =os.path.join('/private/var/cache/apt', 'archives')
        try:    
            for root, dirs, files in os.walk(archive_cache_path):
                file_count = 0
                file_count += len(files)
                
            # Count files and give option to delete
                if file_count > 0:
        
                    dialog = xbmcgui.Dialog()
                    if dialog.yesno("Delete 'Cydia Archived' Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                    
                        for f in files:
                            os.unlink(os.path.join(root, f))
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
    GA("Maintenance","Delete Packages")
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
        
        
############################################################        DELETING CRASH LOGS          ###############################################################    
        
def DeleteCrashLogs(url):  
    print '############################################################       DELETING CRASH LOGS             ###############################################################'
    dialog = xbmcgui.Dialog()
    if dialog.yesno("Delete Old Crash Logs", '', "Do you want to delete them?"):
        path=loglocation()
        import glob
        for infile in glob.glob(os.path.join(path, 'xbmc_crashlog*.*')):
             File=infile
             print infile
             os.remove(infile)
    dialog = xbmcgui.Dialog()
    dialog.ok("XBMCHUB TEAM", "Please Reboot XBMC To Take Effect !!", "Brought To You By XBMCHUB.COM")
    GA('Maintenance','Deleting Crash Logs')
            
            
            
############################################################        1CHANNEL FIX         ###############################################################    
                
def OneChannel(url):
    GA("Fixes","1Channel Eden Fix")
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
    
def advancexml(url,name):
    GA("Tweaks",name)
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
    
############################################################        CHECK ADVANCE XML          ###############################################################    
    
def checkadvancexml(url,name):
    print '############################################################       CHECK ADVANCE XML          ###############################################################'
    path = xbmc.translatePath(os.path.join('special://home/userdata',''))
    advance=os.path.join(path, 'advancedsettings.xml')
    try:
        a=open(advance).read()
        if re.search('34603008',a,re.IGNORECASE):
            name='MIKEYS'
        if re.search('size>0</cache',a,re.IGNORECASE):
            name='0'
        if re.search('<network> <curlclienttimeout>',a,re.IGNORECASE):
            name='TUXENS'
    except:
        name="NO ADVANCED"
    GA("Tweaks","Check XML:"+name)
    dialog = xbmcgui.Dialog()
    dialog.ok("XBMCHUB TEAM","[COLOR yellow]YOU HAVE[/COLOR] "+ name+"[COLOR yellow] SETTINGS SETUP[/COLOR]",'', "Brought To You By XBMCHUB.COM")
    
############################################################        DELETE ADVANCE XML          ###############################################################    
def deleteadvancexml(url):
    GA("Tweaks","Delete Advanced XML")
    print '############################################################       DELETING ADVANCE XML          ###############################################################'
    path = xbmc.translatePath(os.path.join('special://home/userdata',''))
    advance=os.path.join(path, 'advancedsettings.xml')
    os.remove(advance)
    dialog = xbmcgui.Dialog()
    dialog.ok("XBMCHUB TEAM", "       Thats It All Done Please Come Visit Again", "          Brought To You By XBMCHUB.COM")
    
############################################################        KEYMAPS          ###############################################################    
    
    
def joystick(url): 
    GA("Tweaks","Joystick")
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
    GA("Maintenance","Malformed META")
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
    GA("Maintenance","Corrupt 1Channel.db")
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
    
def loglocation(): 
    versionNumber = int(xbmc.getInfoLabel("System.BuildVersion" )[0:2])
    if versionNumber < 12:
        if xbmc.getCondVisibility('system.platform.osx'):
            if xbmc.getCondVisibility('system.platform.atv2'):
                log_path = '/var/mobile/Library/Preferences'
            else:
                log_path = os.path.join(os.path.expanduser('~'), 'Library/Logs')
        elif xbmc.getCondVisibility('system.platform.ios'):
            log_path = '/var/mobile/Library/Preferences'
        elif xbmc.getCondVisibility('system.platform.windows'):
            log_path = xbmc.translatePath('special://home')
            log = os.path.join(log_path, 'xbmc.log')
        elif xbmc.getCondVisibility('system.platform.linux'):
            log_path = xbmc.translatePath('special://home/temp')
        else:
            log_path = xbmc.translatePath('special://logpath')
    elif versionNumber > 11:
        log_path = xbmc.translatePath('special://logpath')
        log = os.path.join(log_path, 'xbmc.log')
    return log_path


    
def lib(url): 
    GA("Maintenance","Update Lib")
    print '############################################################        LYB          ###############################################################'
    log_path=loglocation()
    log = os.path.join(log_path, 'xbmc.log')
    logfile=open(log, 'r').read()
    if 'Windows' in logfile:
        match = re.compile('special://xbmc/ is mapped to: (.+?)\\XBMC').findall(logfile)
        path = xbmc.translatePath(os.path.join(match[0]+'XBMC\system\players\dvdplayer',''))
        lib=os.path.join(path, 'librtmp.dll')
        try:
            os.remove(lib)
        except:
            pass
        url = base+'lib/windows/librtmp.dll'
        DownloaderClass(url,lib)
        dialog = xbmcgui.Dialog()
        dialog.ok("XBMCHUB TEAM", "       Thats It All Done Please Come Visit Again", "          Brought To You By XBMCHUB.COM")
        
    if 'Darwin OSX' in logfile:
        try:    
            match = re.compile('special://frameworks/ is mapped to: (.+?)Frameworks').findall(logfile)
            path = xbmc.translatePath(os.path.join(match[0]+'Frameworks',''))
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
        
    if 'Darwin iOS' in logfile:
        try:    
            match = re.compile('special://frameworks/ is mapped to: (.+?)Frameworks').findall(logfile)
            path = xbmc.translatePath(os.path.join(match[0]+'Frameworks',''))
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
            
    if 'Android,' in logfile:
        try:    
            path = xbmc.translatePath(os.path.join('/data/data/org.xbmc.xbmc/lib',''))
            lib=os.path.join(path, 'librtmp.so')
            try:
                os.remove(lib)
            except:
                pass
            url = base+'lib/android/librtmp.so'
            DownloaderClass(url,lib)
            dialog = xbmcgui.Dialog()
            dialog.ok("XBMCHUB TEAM", "       Thats It All Done Please Come Visit Again", "          Brought To You By XBMCHUB.COM")
        except: 
            dialog = xbmcgui.Dialog()
            dialog.ok("XBMCHUB TEAM", "       CANT UPDATE YOUR LIB FILE SORRY!!!", "          Brought To You By XBMCHUB.COM")
            
    print '########################### LIB LOCATION ####################'
    print lib
    
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
    
     
def howtos(url,fanart):
        GA("Maintenance","How To Videos")
        link=OPEN_URL(url)
        match=re.compile('i="(.+?)" n="(.+?)" u="(.+?)" d="(.+?)"').findall(link)
        for icon, name, youtube , description in match:
                if icon=='none':
                    iconimage = 'http://i.ytimg.com/vi/%s/0.jpg' % youtube
                else:
                    iconimage=str(icon)
                print iconimage
                fanart=str(fanart)
                url = 'plugin://plugin.video.youtube/?path=root/video&action=play_video&videoid=%s' % youtube
                addLink(name,url,iconimage,description,fanart)        
                setView('movies', 'SUB') 
                
def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
     
def uploadlog(url): 
    GA("Maintenance","Upload Log")
    if ADDON.getSetting('email')=='':
        dialog = xbmcgui.Dialog()
        dialog.ok("XBMCHUB TEAM", "A New Window Will Now Open For You To In Put", "Your Email Address For The Logfile To Be Emailed To")
        ADDON.openSettings()
    addon.LogUploader()
    
############################################################        SKIN          ###############################################################    
    
def fastcoloreden(url,iconimage):    
        GA("Maintenance","Install Si02 Skin")
        link=OPEN_URL(url)
        match=re.compile('skinurl="(.+?)" name"(.+?)" icon="(.+?)"').findall(link)
        for url,name,iconimage in match:
            addDir(name,url,17,iconimage,'','Download'+str(name))
            
def downloadanything(url,name):     
    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
    lib=os.path.join(path, name)
    DownloaderClass(url,lib)
    addonfolder = xbmc.translatePath(os.path.join('special://home/addons',''))
    time.sleep(4)
    xbmc.executebuiltin("XBMC.Extract(%s,%s)"%(lib,addonfolder))
    dialog = xbmcgui.Dialog()
    if dialog.yesno("XBMCHUB TEAM", "Would You Like To Change Skin Now", "Window Will Change To Apperance Settings"):
        xbmc.executebuiltin("XBMC.ActivateWindow(appearancesettings)")
    
         ############################################################        FUSION INSTALLER           ###############################################################    
def FusionInstaller(url):
    GA("Maintenance","Fusion Installer")
    print '############################################################        FUSION INSTALLER          ###############################################################'
    path = os.path.join(xbmc.translatePath('special://home'),'userdata', 'sources.xml')

    if not os.path.exists(path):
        f = open(path, mode='w')
        f.write('<sources><files><source><name>FUSION</name><path pathversion="1">http://fusion.xbmchub.com</path></source></files></sources>')
        f.close()
        dialog = xbmcgui.Dialog()
        dialog.ok("XBMCHUB TEAM", "Reboot To Take Effect Then Come", "Back Here To Install Your Plugins")
        return
        
    f   = open(path, mode='r')
    str = f.read()
    f.close()
    if 'http://fusion.xbmchub.com' in str:
        dialog = xbmcgui.Dialog()
        if dialog.yesno("XBMCHUB TEAM", "Please Select Install From Zip Then ", "Select Fusion On The Right Hand Side"):
            xbmc.executebuiltin("XBMC.Container.Update(path,replace)")
            xbmc.executebuiltin("XBMC.ActivateWindow(AddonBrowser)")
    if not'http://fusion.xbmchub.com' in str:
        if '</files>' in str:
            str = str.replace('</files>','<source><name>FUSION</name><path pathversion="1">http://fusion.xbmchub.com</path></source></files>')
            dialog = xbmcgui.Dialog()
            dialog.ok("XBMCHUB TEAM", "Reboot To Take Effect Then Come", "Back Here To Install Your Plugins")
            f = open(path, mode='w')
            f.write(str)
            f.close()
        else:
            str = str.replace('</sources>','<files><source><name>FUSION</name><path pathversion="1">http://fusion.xbmchub.com</path></source></files></sources>')
            dialog = xbmcgui.Dialog()
            dialog.ok("XBMCHUB TEAM", "Reboot To Take Effect Then Come", "Back Here To Install Your Plugins")
            f = open(path, mode='w')
            f.write(str)
            f.close()
    
            
   
    
         ############################################################        1Channel REBOOT FIX           ###############################################################   
def onechannelreboot(url):
    GA("Fixes","1Channel REBOOT FIX")
    print '############################################################        1Channel REBOOT FIX        ###############################################################'
    path = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.1channel',''))
    lib=os.path.join(path, 'playback.py')
    os.remove(lib)
    url = base+'fix/playback.py'
    DownloaderClass(url,lib)
    dialog = xbmcgui.Dialog()
    dialog.ok("XBMCHUB TEAM", "       Thats It All Done Please Come Visit Again", "          Brought To You By XBMCHUB.COM")
    
         ############################################################        INSTALL XBMCHUB REPO           ###############################################################   
def xbmchubrepo(url):
    GA("Maintenance","Install HubRepo")
    print '############################################################        INSTALL XBMCHUB REPO        ###############################################################'
    url = 'http://xbmc-hub-repo.googlecode.com/svn/addons/repository.xbmchub/repository.xbmchub-1.0.1.zip'
    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
    lib=os.path.join(path, 'repository.xbmchub-1.0.1.zip')
    DownloaderClass(url,lib)
    addonfolder = xbmc.translatePath(os.path.join('special://home/addons',''))
    time.sleep(2)
    xbmc.executebuiltin("XBMC.Extract(%s,%s)"%(lib,addonfolder))

    ############################################################        Recovery        ###############################################################
def doRecovery(url):
    GA("None","Enter Recovery")
    print '############################################################        Android Recovery        ###############################################################'
    dialog = xbmcgui.Dialog()
    if dialog.yesno('XBMCHUB TEAM', "Are you sure you want to enter recovery mode?"):
       from subprocess import Popen, PIPE, STDOUT
       cmd = 'reboot recovery'
       Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT )    
       
    ############################################################        Remove Mikey        ###############################################################
def removemikey(url):
    print '############################################################        Remove Mikey       ###############################################################'
    for root, dirs, files in os.walk(url):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))
    os.rmdir(url)
    
    
        ############################################################       Restore Userdata       ###############################################################'
def restore(url):
        GA("Maintenance","Restore Userdata")
        print '############################################################       Restore Userdata       ###############################################################'
        path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
        zippath=os.path.join(path, boxbackupzip)
        DownloaderClass(url,zippath)
        userdata = xbmc.translatePath(os.path.join('special://profile/addon_data/',''))
        time.sleep(3)
        xbmc.executebuiltin("XBMC.Extract(%s,%s)"%(zippath,userdata))
        dialog = xbmcgui.Dialog()
        dialog.ok("XBMCHUB TEAM", "Thats It All Done", " Brought To You By XBMCHUB.COM")
        os.remove(zippath)
        if xbmc.getCondVisibility('system.platform.ATV2'):
            os.chmod(userdata, stat.S_IRWXO)        
        
         ############################################################        CAPTCHA FIX           ###############################################################   
def captcha(url):
    GA("Fixes","Add Captcha")
    print '############################################################        CAPTCHA FIX       ###############################################################'
    url = 'http://dl.dropbox.com/u/129714017/hubmaintenance/fix/vidxden.py'
    path = xbmc.translatePath(os.path.join('special://home/addons/script.module.urlresolver/lib/urlresolver/','plugins'))
    lib=os.path.join(path, 'vidxden.py')
    DownloaderClass(url,lib)
    url = 'http://dl.dropbox.com/u/129714017/hubmaintenance/fix/putlocker.py'
    path = xbmc.translatePath(os.path.join('special://home/addons/script.module.urlresolver/lib/urlresolver/','plugins'))
    lib=os.path.join(path, 'putlocker.py')
    DownloaderClass(url,lib)
    
    
    ############################################################       REMOVE ADDON             ###############################################################'
def findaddon(url,name):  
    GA("Maintenance",name)
    print '############################################################       REMOVE ADDON             ###############################################################'
    pluginpath = xbmc.translatePath(os.path.join('special://home/addons',''))
    import glob
    for file in glob.glob(os.path.join(pluginpath, url+'*')):
        name=str(file).replace(pluginpath,'').replace('plugin.','').replace('audio.','').replace('video.','').replace('skin.','').replace('repository.','')
        iconimage=(os.path.join(file,'icon.png'))
        fanart=(os.path.join(file,'fanart.jpg'))
        addDir(name,file,26,iconimage,fanart,'')
        setView('movies', 'SUB') 
         ############################################################        SUBTITLE FIX           ###############################################################   
def subtitle(url):
    GA("Fixes","Subtitle Fix")
    print '############################################################        SUBTITLE FIX       ###############################################################'
    url = 'http://dl.dropbox.com/u/129714017/hubmaintenance/fix/default.py'
    path = xbmc.translatePath(os.path.join('special://home/addons/','plugin.video.1channel'))
    lib=os.path.join(path, 'default.py')
    DownloaderClass(url,lib)
    url = 'http://dl.dropbox.com/u/129714017/hubmaintenance/fix/playback.py'
    path = xbmc.translatePath(os.path.join('special://home/addons/','plugin.video.1channel'))
    lib=os.path.join(path, 'playback.py')
    DownloaderClass(url,lib)
    dialog = xbmcgui.Dialog()
    dialog.ok("XBMCHUB TEAM", "Thats It All Done", " Brought To You By XBMCHUB.COM")
    
    
         ############################################################       SLOW GUI          ###############################################################    
def gui(url):
    GA("Fixes","Slow Gui")
    print '############################################################        SLOW GUI         ###############################################################'
    path = os.path.join(xbmc.translatePath('special://home'),'userdata', 'advancedsettings.xml')
    try:
        f   = open(path, mode='r')
        str = f.read()
        f.close()
        if '<algorithmdirtyregions>3</algorithmdirtyregions>' in str:
                str = str.replace('<algorithmdirtyregions>3</algorithmdirtyregions>','<algorithmdirtyregions>0</algorithmdirtyregions>')
                dialog = xbmcgui.Dialog()
                dialog.ok("XBMCHUB TEAM", 'You Had Dirty Regions Set To "3"', "All Fixed And Disabled")
                f = open(path, mode='w')
                f.write(str)
                f.close()
        else:
                dialog = xbmcgui.Dialog()
                dialog.ok("XBMCHUB TEAM", 'You Have Not Got Dirty Regions "3"', "So Sorry You Just Have A Slow Box")
                f = open(path, mode='w')
                f.write(str)
                f.close()
    except:
        dialog = xbmcgui.Dialog()
        dialog.ok("XBMCHUB TEAM", 'You Have Not Got Any Advanced Settings Anyway', "So Sorry You Just Have A Slow Box")
        
            
def select_build(): 
    dialog=xbmcgui.Dialog()
    version_select=['Frodo','Eden']
    select=['Frodo','Eden']
    return version_select[xbmcgui.Dialog().select('Please Choose Your Build', select)]
   
         ############################################################        YouTube Fix           ###############################################################   
def youtubefix(name):
    GA("Maintenance","YouTube Fix")
    print '############################################################        YouTube Fix       ###############################################################'
    version=select_build()
    url = base+'plugin.video.youtube-'+str(version)+'.zip'
    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
    lib=os.path.join(path, 'plugin.video.youtube.zip')
    youtube = xbmc.translatePath(os.path.join('special://home/addons','plugin.video.youtube'))
    for root, dirs, files in os.walk(youtube):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))
    os.rmdir(youtube)
    DownloaderClass(url,lib)
    addonfolder = xbmc.translatePath(os.path.join('special://home/addons',''))
    time.sleep(3)
    xbmc.executebuiltin("XBMC.Extract(%s,%s)"%(lib,addonfolder))
    dialog = xbmcgui.Dialog()
    dialog.ok("XBMCHUB TEAM", "YouTube Is Now Fixed !!", "Brought To You By XBMCHUB.COM")
    
def itvfix(name):
    GA("Fixes","ITV Fix")
    print '############################################################        ITV FIX       ###############################################################'
    url = 'http://dl.dropbox.com/u/129714017/hubmaintenance/fix/plugin.video.itv.zip'
    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
    lib=os.path.join(path, 'plugin.video.itv.zip')
    DownloaderClass(url,lib)
    addonfolder = xbmc.translatePath(os.path.join('special://home/addons',''))
    time.sleep(2)
    xbmc.executebuiltin("XBMC.Extract(%s,%s)"%(lib,addonfolder))
    dialog = xbmcgui.Dialog()
    dialog.ok("XBMCHUB TEAM", "Please Reboot To Take", "Effect   Brought To You By XBMCHUB.COM")
        
def image_select():
    dialog = xbmcgui.Dialog()
    select=['M1','M3']
    image_select=['M1','M3']
    return select[xbmcgui.Dialog().select('Which Version ?', image_select)]
    
def image_select_url():
    dialog = xbmcgui.Dialog()
    url=['https://www.dropbox.com/sh/qfsqqow67m8hawp/izMaTF_I4f/m1','https://www.dropbox.com/sh/qfsqqow67m8hawp/xWXi4ONQjX/m3']
    image_select=['M1','M3']
    return url[xbmcgui.Dialog().select('Which Version ?', image_select)]

def getimgdropbox(url):
    link=OPEN_URL(url)
    match=re.compile('MB</div><a href="(.+?)"').findall(link)
    return match[0]
    
def toys4me_select_url():
    dialog = xbmcgui.Dialog()
    url=['http://d-h.st/users/toys4me/?fld_id=11798#files','http://d-h.st/users/toys4me/?fld_id=10436#files']
    image_select=['M1','M3']
    return url[xbmcgui.Dialog().select('Which Version ?', image_select)]
    
            
    
def toys4me(name,url,iconimage):
    url=toys4me_select_url()
    print url
    link=OPEN_URL(url)
    match=re.compile('<a href="(.+?)">(.+?).img</a>').findall(link)
    yourversion='[B][COLOR yellow]Your Version Build Date: %s[/B][/COLOR]'%(myversion())
    addDir(yourversion,'url',34,iconimage,'',name)
    for url,name in match:
        regex=re.compile('(.+?)-(.+?)-(.+?)(.+?)(.+?)(.+?)(.+?)(.+?)(.+?)(.+?)')
        match=regex.search(name)
        name='Date:%s%s/%s%s/%s%s%s%s - %s-%s'%(match.group(5),match.group(6),match.group(3),match.group(4),match.group(7),match.group(8),match.group(9),match.group(10),match.group(1).upper(),match.group(2).upper())
        url='http://d-h.st'+url
        addDir(name,url,43,iconimage,'','')  
        
def toys4medownload(name,url,iconimage):
    link=OPEN_URL(url)
    match=re.compile('action="(.+?)"').findall(link)
    path = xbmc.translatePath(os.path.join(linux_download,''))
    img=os.path.join(path, 'update.img')
    try:
        os.remove(img)
    except:
        pass
    DownloaderClass(match[0],img)
    time.sleep(3)
    if dialog.yesno("[B][COLOR red]WARNING !!![/B][/COLOR]", '[B]ARE YOU SURE YOU KNOW WHAT THIS DOES !?![/B]','', "[B][COLOR red]     THIS WILL FLASH TO THIS LINUX IMAGE !!![/B][/COLOR]"):
        GA("Check Linux","Flashing: Toys4me")
        doRecovery(url)       
          
        
        
    
def linux_image(name,url,iconimage):
        dialog = xbmcgui.Dialog()
        if dialog.yesno("What Is Your Box", 'Did you know that if you have an M1','box you can flash with official Pivos',"so what box do you have now ?",'OTHER','PIVOS'):
            if dialog.yesno("Which Build", '','Do You Want To Use Latest Nightly Builds',"",'NIGHTLIES','OFFICIAL'):
                yourversion='[B][COLOR yellow]Your Version Build Date: %s[/B][/COLOR]'%(myversion())
                addDir(yourversion,'url',34,iconimage,'',name)
                print '############################################################     LINUX IMAGE OFFICIAL      ###############################################################'
                GA("None","Check Linux")
                link=OPEN_URL(url)
                r='Firmware Release %s</span></span><br/><span style="font-weight: bold">Date: (.+?)</span>.+?Download from <a href="(.+?)"'%(image_select())
                uniques=[]
                match=re.compile(r).findall(link)
                for name,url in match:
                    if name not in uniques:
                        uniques.append(name)
                        regex=re.compile('(.+?)(.+?)/(.+?)(.+?)/(.+?)(.+?)')
                        match=regex.search(name)
                        name='%s%s/%s%s/20%s%s'%(match.group(3),match.group(4),match.group(1),match.group(2),match.group(5),match.group(6))
                        addDir('Date: '+name,url,34,iconimage,'','To Install This Image Please Go Ahead And Click on The One you Desire')       
                        setView('movies', 'default') 
            else:
                yourversion='[B][COLOR yellow]Your Version Build Date: %s[/B][/COLOR]'%(myversion())
                addDir(yourversion,'url',34,iconimage,'',name)
                print '############################################################     LINUX IMAGE NIGHTLIES      ###############################################################'
                url=image_select_url()
                print url
                link=OPEN_URL(url)
                if re.search('/m1',url,re.IGNORECASE):
                    v='m1'
                else:
                    v='m3'
                link=link.split(v+'/MD5SUM')[2]
                match=re.compile('<div class="filename"><a href="(.+?)update(.+?)img" target="_top" class="filename-link" onclick="" rel="nofollow"><span id="emsnippet-.+?"></span></a></div></div><div class="filesize-col"><span class="size">(.+?)</span></div><div class="modified-col"><span><span class="modified-time">(.+?)</span>').findall(link)
                for url,name,size,date in match:
                    url= url+'update'+name+'img'
                    name='update'+name+'img'+' ['+date+' '+size+']' 
                    url=getimgdropbox(url)
                    addDir(name,url,41,iconimage,'','To Install This Image Please Go Ahead And Click on The One you Desire')
        else:
            if dialog.yesno("What Is Your Box", '','',"",'M3','M1'):
                url='http://dl.dropbox.com/u/129714017/hubmaintenance/linuxflash/jynx_m1.zip'
                print '======= Jynx M1 ======='
                install_linux_image('Jynx M1',url,iconimage)
            else:
                if dialog.yesno("Which Image?", '','',"",'GEEKSQUAD','JYNX'):
                    url='http://dl.dropbox.com/u/129714017/hubmaintenance/linuxflash/jynx_m3.zip'
                    print '======= Jynx M3 ======='
                    install_linux_image('Jynx M3',url,iconimage)
                else:
                    url='http://dl.dropbox.com/u/129714017/hubmaintenance/linuxflash/Geeksquad8.m3.zip'
                    print '======= GEEKSQUAD M3 ======='
                    install_linux_image('GEEKSQUAD M3',url,iconimage)
                    
def install_linux_image_nightlies(name,url,iconimage):
    url = str(url)
    name = name.split(' [')[0]
    dialog = xbmcgui.Dialog()
    if linux_download == '':
        dialog = xbmcgui.Dialog()
        dialog.ok("XBMC TEAM", "You Need To Set Your Download Path", "A Window Will Now Open For You To Set","Its In Hub Settings")
        ADDON.openSettings()
    path = xbmc.translatePath(os.path.join(linux_download,''))
    img=os.path.join(path, 'update.img')
    try:
        os.remove(img)
    except:
        pass
    DownloaderClass(url,img)
    time.sleep(1)
    if dialog.yesno("[B][COLOR red]WARNING !!![/B][/COLOR]", '[B]ARE YOU SURE YOU KNOW WHAT THIS DOES !?![/B]','', "[B][COLOR red]     THIS WILL FLASH TO THIS LINUX IMAGE !!![/B][/COLOR]"):
        GA("Check Linux","Flashing: "+name)
        doRecovery(url)       
                    
                
def install_linux_image(name,url,iconimage):
    name = str(name).replace('Date: ','Pivos_').replace('/','_')
    dialog = xbmcgui.Dialog()
    if linux_download == '':
        dialog = xbmcgui.Dialog()
        dialog.ok("XBMC TEAM", "You Need To Set Your Download Path", "A Window Will Now Open For You To Set","Its In Hub Settings")
        ADDON.openSettings()
    path = xbmc.translatePath(os.path.join(linux_download,''))
    img=os.path.join(path, 'update.img')
    try:
        os.remove(img)
    except:
        pass
    lib=os.path.join(path, 'update.zip')
    DownloaderClass(url,lib)
    time.sleep(4)
    xbmc.executebuiltin("XBMC.Extract(%s,%s)"%(lib,path))
    try:
        os.remove(lib)
    except:
        pass
    if dialog.yesno("[B][COLOR red]WARNING !!![/B][/COLOR]", '[B]ARE YOU SURE YOU KNOW WHAT THIS DOES !?![/B]','', "[B][COLOR red]     THIS WILL FLASH TO THIS LINUX IMAGE !!![/B][/COLOR]"):
        GA("Check Linux","Flashing: "+name)
        doRecovery(url)       

    
    
def myversion():
   log_path = xbmc.translatePath('special://logpath')
   log = os.path.join(log_path, 'xbmc.log')
   logfile = open(log, 'r').read()
   match=re.compile('Starting XBMC \(.+? Git:(.+?)\)').findall(logfile)
   result=match[0]
   try:
       regex=re.compile('(.+?)(.+?)(.+?)(.+?)(.+?)(.+?)(.+?)(.+?)-.+?')
       match=regex.search(result)
       date='%s%s/%s%s/%s%s'%(match.group(7),match.group(8),match.group(5),match.group(6),match.group(3),match.group(4))
   except:
       date='Unknown'
   return date
   
############################################################        INSTALL ALL REPOS        ###############################################################
def allrepos(url):  
    GA("None","All Repo Install")
    print '############################################################        INSTALL ALL REPOS        ###############################################################'
    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
    lib=os.path.join(path, 'allrepos.zip')
    DownloaderClass(url,lib)
    addonfolder = xbmc.translatePath(os.path.join('special://home/addons',''))
    time.sleep(4)
    xbmc.executebuiltin("XBMC.Extract(%s,%s)"%(lib,addonfolder))
    dialog = xbmcgui.Dialog()
    dialog.ok("XBMCHUB TEAM", "Please Reboot To Take", "Effect   Brought To You By XBMCHUB.COM")
        
def removeanything(url):   
    dialog = xbmcgui.Dialog()
    if dialog.yesno("Remove", '', "Do you want to Remove"):
        for root, dirs, files in os.walk(url):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))
        os.rmdir(url)
        xbmc.executebuiltin('Container.Refresh')         
    
    
############################################################        PLAYERCORE          ###############################################################    
    
    
def playercore(url): 
    GA("Maintenance","PlayerCore")
    print '############################################################        PLAYERCORE          ###############################################################'
    path = xbmc.translatePath(os.path.join('special://home/userdata',''))
    playercore=os.path.join(path, 'playercorefactory.xml')
    try:
        os.remove(playercore)
        print '========= REMOVING    '+str(playercore)+'     =========================='
    except:
        pass
    link=OPEN_URL(url)
    a = open(playercore,"w") 
    a.write(link)
    a.close()
    print '========= WRITING NEW    '+str(playercore)+'     =========================='
    dialog = xbmcgui.Dialog()
    dialog.ok("XBMCHUB TEAM", "Please Enable Hardware Acceleration In Settings",'Please Reboot XBMC',"          Brought To You By XBMCHUB.COM")
    
    
############################################################        HULU FIX          ###############################################################    
def hulufix(url):  
    GA("None","Hulu")
    print '############################################################        HULU FIX        ###############################################################'
    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
    lib=os.path.join(path, 'script.module.cryptopy.zip')
    DownloaderClass(url,lib)
    addonfolder = xbmc.translatePath(os.path.join('special://home/addons',''))
    time.sleep(2)
    xbmc.executebuiltin("XBMC.Extract(%s,%s)"%(lib,addonfolder))
    dialog = xbmcgui.Dialog()
    dialog.ok("XBMCHUB TEAM", "Please Reboot To Take", "Effect   Brought To You By XBMCHUB.COM")
    
    
############################################################        ADD 7 ICONS          ###############################################################    
    
def add7icons(url): 
    dialog = xbmcgui.Dialog()
    print '############################################################        ADD 7 ICONS          ###############################################################'
    if dialog.yesno("XBMCHUB TEAM","" , "Add 7 Icons Or Restore To 5",'','Restore 5','Add 7'):
        GA("Maintenance","Add 7 Icons")
        url = base+'tweaks/confluence_7.zip'
        path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
        lib=os.path.join(path, 'confluence_7.zip')
        DownloaderClass(url,lib)
        time.sleep(3)
        addonfolder = xbmc.translatePath(os.path.join('special://home/addons',''))
        xbmc.executebuiltin("XBMC.Extract(%s,%s)"%(lib,addonfolder))
        ADDON.setSetting('add7','false')
        dialog = xbmcgui.Dialog()
        dialog.ok("XBMCHUB TEAM", "Please Reboot To Take", "Effect   Brought To You By XBMCHUB.COM")
    else:
        GA("Maintenance","Restore 5")
        confluence = xbmc.translatePath(os.path.join('special://home/addons','skin.confluence'))
        if ADDON.getSetting('add7')=='false':
            dialog = xbmcgui.Dialog()
            dialog.ok("XBMCHUB TEAM", "Run Me Again After Reboot To Completely Clean", "Brought To You By XBMCHUB.COM")
            ADDON.setSetting('add7','true')
        else:
            dialog = xbmcgui.Dialog()
            dialog.ok("XBMCHUB TEAM", "Great You Are Completely Clean Now", "Brought To You By XBMCHUB.COM")
            ADDON.setSetting('add7','false')
        for root, dirs, files in os.walk(confluence):
            try:
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))
            except:
                pass
        try:
            os.rmdir(confluence)
        except:
            pass
            
############################################################       WALLPAPER         ###############################################################    
def wallpaper(name,url,iconimage):
    link=OPEN_URL(wallurl)
    match=re.compile('<a href="(.+?)" title=".+?">(.+?)</a>  <small>(.+?)</small').findall(link)
    for url,name,amount in match:
            url=wallurl+url
            name= name+' '+amount
            addDir(name,url,45,iconimage,base+'images/fanart/gettingstarted.jpg','')
    

def wallpaper2(name,url,iconimage):
    link=OPEN_URL(url)
    match=re.compile('href="(.+?)" title=".+?"><p align="center">(.+?)</p>').findall(link)
    if not match:
            wallpaper3(name,url,iconimage)
    elif len(match)<2:
            addDir(name,url,46,iconimage,base+'images/fanart/gettingstarted.jpg','')
    else:
        for url,name in match:
            url=wallurl+url
            addDir(name,url,46,iconimage,base+'images/fanart/gettingstarted.jpg','')


def wallpaper3(name,url,iconimage):    
    link=OPEN_URL(url)
    match=re.compile('href="(.+?)" title=".+?">\n.+?img src="(.+?)" alt="(.+?) HD Wide').findall(link)
    for url,iconimage,name in match:
            url=wallurl+url
            addDir(name,url,47,iconimage,base+'images/fanart/gettingstarted.jpg','')
    if 'Next ' in link:
        try:
	        link=link.split('Previous<')[1]
	        link=link.split('>Next')[0]
	        match=re.compile('href="(.+?)"').findall(link)
	        pos=int(len(match))-1
	        url=wallurl+str(match[pos])
	        name= 'Next Page >>'
	        addDir(name,url,46,base+'images/nextpage.jpg',base+'images/fanart/gettingstarted.jpg','')
        except:
	        pass
    setView('movies', 'MAIN')

def wallpaper_download(name,url,iconimage):  
    GA('Wallpaper','Download '+name)
    link=OPEN_URL(url)
    if ADDON.getSetting('download_wallpaper')=='':
        dialog = xbmcgui.Dialog()
        dialog.ok("XBMCHUB TEAM", "A New Window Will Now Open For You To In Put", "Download Path")
        ADDON.openSettings()
    size='1920x1080'
    r='<a target="_self" href="(.+?)" title=".+?">%s</a>'%(size)
    match=re.compile(r).findall(link)
    url= wallurl+match[0] 
    path = xbmc.translatePath(os.path.join(ADDON.getSetting('download_wallpaper'),''))
    img=os.path.join(path, name+'.jpg')
    try:
        DownloaderClass(url,img, True)    
    except Exception as e:
        try:
            os.remove(img)
        except:
            pass
        if str(e) == "Canceled":
            #you will end up here only if the user cancelled the download 
            pass
    
def hd_wallpaper(name,url,iconimage):
    link=OPEN_URL(hd_wallurl)
    match=re.compile('li style="padding-left:0px;"><a  href="(.+?)">(.+?)</a>').findall(link)
    for url,name in match:    
            url=hd_wallurl+url
            name= name
            addDir(name,url,50,iconimage,base+'images/fanart/gettingstarted.jpg','')
    

def hd_wallpaper2(name,url,iconimage):
    url=url.replace('pageSub','page')
    print'######################## '+url
    link=OPEN_URL(url)
    split=link.split('class="rss-image"')[1]
    match=re.compile('href="(.+?)"><p>(.+?)</p><em>.+?</em><img src="(.+?)"').findall(split)
    for url,name,iconimage in match:
        url=hd_wallurl+'/wallpapers/'+iconimage.replace('/thumbs/','').replace('-t1','-1920x1080')
        addDir(name,url,51,hd_wallurl+iconimage,base+'images/fanart/gettingstarted.jpg','')
    if 'Next ' in link:
        try:
	        if '/pageSub/' in link:
	            link=link.split('Previous<')[2]
	        else:
	            link=link.split('Previous<')[1]
	        link=link.split('>Next')[0]
	        match=re.compile('href="(.+?)"').findall(link)
	        pos=int(len(match))-1
	        url=hd_wallurl+str(match[pos])
	        name= 'Next Page >>'
	        addDir(name,url,50,base+'images/nextpage.jpg',base+'images/fanart/gettingstarted.jpg','')
        except:
	        pass
    setView('movies', 'MAIN')

def hd_wallpaper_download(name,url,iconimage):   
    GA('Wallpaper','Download '+name)
    link=OPEN_URL(url)
    if ADDON.getSetting('download_wallpaper')=='':
        dialog = xbmcgui.Dialog()
        dialog.ok("XBMCHUB TEAM", "A New Window Will Now Open For You To In Put", "Download Path")
        ADDON.openSettings()
    print '==================================    '+url
    path = xbmc.translatePath(os.path.join(ADDON.getSetting('download_wallpaper'),''))
    img=os.path.join(path, name+'.jpg')
    print '==================================    '+img
    DownloaderClass(url,img)
    
    
def parseDate(dateString):
    try:
        return datetime.datetime.fromtimestamp(time.mktime(time.strptime(dateString.encode('utf-8', 'replace'), "%Y-%m-%d %H:%M:%S")))
    except:
        return datetime.datetime.today() - datetime.timedelta(days = 1) #force update


def checkGA():

    secsInHour = 60 * 60
    threshold  = 2 * secsInHour

    now   = datetime.datetime.today()
    prev  = parseDate(ADDON.getSetting('ga_time'))
    delta = now - prev
    nDays = delta.days
    nSecs = delta.seconds

    doUpdate = (nDays > 0) or (nSecs > threshold)
    if not doUpdate:
        return

    ADDON.setSetting('ga_time', str(now).split('.')[0])
    APP_LAUNCH()    
    
                    
def send_request_to_google_analytics(utm_url):
    ua='Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
    import urllib2
    try:
        req = urllib2.Request(utm_url, None,
                                    {'User-Agent':ua}
                                     )
        response = urllib2.urlopen(req).read()
    except:
        print ("GA fail: %s" % utm_url)         
    return response
       
def GA(group,name):
        try:
            try:
                from hashlib import md5
            except:
                from md5 import md5
            from random import randint
            import time
            from urllib import unquote, quote
            from os import environ
            from hashlib import sha1
            VISITOR = ADDON.getSetting('visitor_ga')
            utm_gif_location = "http://www.google-analytics.com/__utm.gif"
            if not group=="None":
                    utm_track = utm_gif_location + "?" + \
                            "utmwv=" + VERSION + \
                            "&utmn=" + str(randint(0, 0x7fffffff)) + \
                            "&utmt=" + "event" + \
                            "&utme="+ quote("5("+PATH+"*"+group+"*"+name+")")+\
                            "&utmp=" + quote(PATH) + \
                            "&utmac=" + UATRACK + \
                            "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR,VISITOR,"2"])
                    try:
                        print "============================ POSTING TRACK EVENT ============================"
                        send_request_to_google_analytics(utm_track)
                    except:
                        print "============================  CANNOT POST TRACK EVENT ============================" 
            if name=="None":
                    utm_url = utm_gif_location + "?" + \
                            "utmwv=" + VERSION + \
                            "&utmn=" + str(randint(0, 0x7fffffff)) + \
                            "&utmp=" + quote(PATH) + \
                            "&utmac=" + UATRACK + \
                            "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR, VISITOR,"2"])
            else:
                if group=="None":
                       utm_url = utm_gif_location + "?" + \
                                "utmwv=" + VERSION + \
                                "&utmn=" + str(randint(0, 0x7fffffff)) + \
                                "&utmp=" + quote(PATH+"/"+name) + \
                                "&utmac=" + UATRACK + \
                                "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR, VISITOR,"2"])
                else:
                       utm_url = utm_gif_location + "?" + \
                                "utmwv=" + VERSION + \
                                "&utmn=" + str(randint(0, 0x7fffffff)) + \
                                "&utmp=" + quote(PATH+"/"+group+"/"+name) + \
                                "&utmac=" + UATRACK + \
                                "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR, VISITOR,"2"])
                                
            print "============================ POSTING ANALYTICS ============================"
            send_request_to_google_analytics(utm_url)
            
        except:
            print "================  CANNOT POST TO ANALYTICS  ================" 
            
            
def APP_LAUNCH():
        versionNumber = int(xbmc.getInfoLabel("System.BuildVersion" )[0:2])
        if versionNumber < 12:
            if xbmc.getCondVisibility('system.platform.osx'):
                if xbmc.getCondVisibility('system.platform.atv2'):
                    log_path = '/var/mobile/Library/Preferences'
                else:
                    log_path = os.path.join(os.path.expanduser('~'), 'Library/Logs')
            elif xbmc.getCondVisibility('system.platform.ios'):
                log_path = '/var/mobile/Library/Preferences'
            elif xbmc.getCondVisibility('system.platform.windows'):
                log_path = xbmc.translatePath('special://home')
                log = os.path.join(log_path, 'xbmc.log')
                logfile = open(log, 'r').read()
            elif xbmc.getCondVisibility('system.platform.linux'):
                log_path = xbmc.translatePath('special://home/temp')
            else:
                log_path = xbmc.translatePath('special://logpath')
            log = os.path.join(log_path, 'xbmc.log')
            logfile = open(log, 'r').read()
            match=re.compile('Starting XBMC \((.+?) Git:.+?Platform: (.+?)\. Built.+?').findall(logfile)
        elif versionNumber > 11:
            print '======================= more than ===================='
            log_path = xbmc.translatePath('special://logpath')
            log = os.path.join(log_path, 'xbmc.log')
            logfile = open(log, 'r').read()
            match=re.compile('Starting XBMC \((.+?) Git:.+?Platform: (.+?)\. Built.+?').findall(logfile)
        else:
            logfile='Starting XBMC (Unknown Git:.+?Platform: Unknown. Built.+?'
            match=re.compile('Starting XBMC \((.+?) Git:.+?Platform: (.+?)\. Built.+?').findall(logfile)
        print '==========================   '+PATH+' '+VERSION+'  =========================='
        try:
            from hashlib import md5
        except:
            from md5 import md5
        from random import randint
        import time
        from urllib import unquote, quote
        from os import environ
        from hashlib import sha1
        import platform
        VISITOR = ADDON.getSetting('visitor_ga')
        for build, PLATFORM in match:
            if re.search('12',build[0:2],re.IGNORECASE): 
                build="Frodo" 
            if re.search('11',build[0:2],re.IGNORECASE): 
                build="Eden" 
            if re.search('13',build[0:2],re.IGNORECASE): 
                build="Gotham" 
            print build
            print PLATFORM
            utm_gif_location = "http://www.google-analytics.com/__utm.gif"
            utm_track = utm_gif_location + "?" + \
                    "utmwv=" + VERSION + \
                    "&utmn=" + str(randint(0, 0x7fffffff)) + \
                    "&utmt=" + "event" + \
                    "&utme="+ quote("5(APP LAUNCH*"+build+"*"+PLATFORM+")")+\
                    "&utmp=" + quote(PATH) + \
                    "&utmac=" + UATRACK + \
                    "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR,VISITOR,"2"])
            try:
                print "============================ POSTING APP LAUNCH TRACK EVENT ============================"
                send_request_to_google_analytics(utm_track)
            except:
                print "============================  CANNOT POST APP LAUNCH TRACK EVENT ============================" 
                
class HUB( xbmcgui.WindowXMLDialog ): # The call MUST be below the xbmcplugin.endOfDirectory(int(sys.argv[1])) or the dialog box will be visible over the pop-up.
    def __init__( self, *args, **kwargs ):
        self.shut = kwargs['close_time'] 
        xbmc.executebuiltin( "Skin.Reset(AnimeWindowXMLDialogClose)" )
        xbmc.executebuiltin( "Skin.SetBool(AnimeWindowXMLDialogClose)" )
                                       
    def onInit( self ):
        xbmc.Player().play('%s/resources/skins/DefaultSkin/media/xbmchub.mp3'%ADDON.getAddonInfo('path'))# Music.
        while self.shut > 0:
            xbmc.sleep(1000)
            self.shut -= 1
        xbmc.Player().stop()
        self._close_dialog()
                
    def onFocus( self, controlID ): pass
    
    def onClick( self, controlID ): 
        if controlID==12:
            xbmc.Player().stop()
            self._close_dialog()

    def onAction( self, action ):
        if action in [ 5, 6, 7, 9, 10, 92, 117 ] or action.getButtonCode() in [ 275, 257, 261 ]:
            xbmc.Player().stop()
            self._close_dialog()

    def _close_dialog( self ):
        xbmc.executebuiltin( "Skin.Reset(AnimeWindowXMLDialogClose)" )
        time.sleep( .4 )
        self.close()

             
def pop():# Added Close_time for window auto-close length.....
    if xbmc.getCondVisibility('system.platform.ios'):
        if not xbmc.getCondVisibility('system.platform.atv'):
            popup = HUB('hub1.xml',ADDON.getAddonInfo('path'),'DefaultSkin',close_time=34,logo_path='%s/resources/skins/DefaultSkin/media/Logo/'%ADDON.getAddonInfo('path'))
    elif xbmc.getCondVisibility('system.platform.android'):
        popup = HUB('hub1.xml',ADDON.getAddonInfo('path'),'DefaultSkin',close_time=34,logo_path='%s/resources/skins/DefaultSkin/media/Logo/'%ADDON.getAddonInfo('path'))
    else:
        popup = HUB('hub.xml',ADDON.getAddonInfo('path'),'DefaultSkin',close_time=34,logo_path='%s/resources/skins/DefaultSkin/media/Logo/'%ADDON.getAddonInfo('path'))
    
    popup.doModal()
    del popup
                
def checkdate(dateString):
    try:
        return datetime.datetime.fromtimestamp(time.mktime(time.strptime(dateString.encode('utf-8', 'replace'), "%Y-%m-%d %H:%M:%S")))
    except:
        return datetime.datetime.today() - datetime.timedelta(days = 1000) #force update


def check_popup():

    threshold  = 120

    now   = datetime.datetime.today()
    prev  = checkdate(ADDON.getSetting('pop_time'))
    delta = now - prev
    nDays = delta.days

    doUpdate = (nDays > threshold)
    if not doUpdate:
        return

    ADDON.setSetting('pop_time', str(now).split('.')[0])
    pop()
     
checkGA()

def addDir(name,url,mode,iconimage,fanart,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        if (mode==13) or (mode==9) or (mode==10)or (mode==11)or (mode==36)or (mode==38)or (mode==14)or (mode==5)or (mode==6)or (mode==16)or (mode==25)or (mode==33)or (mode==34)or (mode==44)or (mode==45)or (mode==46)or (mode==42)or (mode==48)or (mode==49)or (mode==50) or (mode ==None):
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
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
        
        
print str(PATH)+': '+str(VERSION)
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)


def setView(content, viewType):
    # set content type so library shows more views and info
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if ADDON.getSetting('auto-view')=='true':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )
        
        
if mode==None or url==None or len(url)<1:
        CATEGORIES()
       
elif mode==1:
        DeleteCrashLogs(url)
        
elif mode==2:
        DeletePackages(url)

elif mode==3:
        deletecachefiles(url)
        
elif mode==4:
        OneChannel(url)
        
elif mode==5:
        advancexml(url,name)
        
elif mode==6:
        joystick(url)
        
elif mode==7:
        print ""+url +iconimage
        malformed(url)
        
elif mode==8:
        onechanneldb(url)
        
elif mode==9:
        maintenance(url)
        
elif mode==10:
        fixesdir(url)
        
elif mode==11:
        tweaksdir(url)
        
elif mode==12:
        lib(url)
        
elif mode==13:
        howtos(url,fanart)
        
elif mode==14:
        deleteadvancexml(url)
        
elif mode==15:
        uploadlog(url)
        
elif mode==16:
        fastcoloreden(url,iconimage)
        
elif mode==17:
        downloadanything(url,name)
        
elif mode==18:
        FusionInstaller(url)
                
elif mode==19:
        doRecovery(url)
        
elif mode==20:
        onechannelreboot(url)
        
elif mode==21:
        xbmchubrepo(url)
        
elif mode==22:
        removemikey(url)
        
elif mode==23:
        restore(url)
elif mode==24:
        captcha(url)
elif mode==25:
        findaddon(url,name)
elif mode==26:
        removeanything(url)
elif mode==27:
        subtitle(url)
elif mode==28:
        gui(url)
elif mode==29:
        checkadvancexml(url,name)
elif mode==30:
        youtubefix(name)
elif mode==31:
        itvfix(name)
elif mode==33:
        linux_image(name,url,iconimage)
elif mode==34:
        install_linux_image(name,url,iconimage)
elif mode==35:
        allrepos(url)
elif mode==36:
        allandroid(url)
        
elif mode==37:
        playercore(url)
        
elif mode==38:
        alllinux(url)
        
elif mode==39:
        hulufix(url)
elif mode==40:
        add7icons(url)
elif mode==41:
        install_linux_image_nightlies(name,url,iconimage)
elif mode==42:
        toys4me(name,url,iconimage)
elif mode==43:
        toys4medownload(name,url,iconimage)
        
elif mode==44:
        wallpaper(name,url,iconimage)
        
elif mode==45:
        wallpaper2(name,url,iconimage)
elif mode==46:
        wallpaper3(name,url,iconimage)
elif mode==47:
        wallpaper_download(name,url,iconimage)
elif mode==48:
        wallpaper_catergories()
        
elif mode==49:
        hd_wallpaper(name,url,iconimage)
elif mode==50:
        hd_wallpaper2(name,url,iconimage)
elif mode==51:
        hd_wallpaper_download(name,url,iconimage)
        
elif mode==2000:
        pop()
        GA('None','Need Help')

elif mode==111:
        import maintenance
        maintenance.doMaintenance(1)
        GA("Maintenance","Delete Thumbnails")
        dialog = xbmcgui.Dialog()
        dialog.ok("XBMCHUB TEAM", "All Done Thank You", "Brought To You By XBMCHUB.COM")

xbmcplugin.endOfDirectory(int(sys.argv[1]))
check_popup()

