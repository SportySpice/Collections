from visual.browse_for_sources import viewStyle, youtubeSearchVisual, youtubeSubscriptionsVisual, youtubeCategoriesVisual, kodiFoldersVisual 
from src.li.ItemList import ItemList
from src import router
from src.videosource.kodi import KodiFolder
from src.tools.addonSettings import string as st


#VIDEO_ROOT_PATH         =   'library://video/'
VIDEO_ADDONS_PATH       =   'addons://sources/video/'
VIDEO_LIBRARY_PATH      =   'videodb://'
VIDEO_FILES_PATH        =   'sources://video/'
VIDEO_PLAYLISTS_PATH    =   'special://videoplaylists/'

MUSIC_ADDONS_PATH       =   'addons://sources/audio/'
MUSIC_LIBRARY_PATH      =   'musicdb://'
#MUSIC_FILES_PATH       =    ???
MUSIC_PLAYLISTS_PATH    =   'special://musicplaylists/'

PROGRAM_ADDONS_PATH     =   'addons://sources/executable/'

PICTURE_ADDONS_PATH     =   'addons://sources/image/'
#PICTURE_LIBRARY_PATH    =   ???
#PICTURE_FILES_PATH      =   ???
#PICTURE_PLAYLISTS_PATH  =   ???


def browse():
    items = ItemList()
    
    items.addCustomFolder(router.searchYoutubeSelectUrl(),          youtubeSearchVisual)
    items.addCustomFolder(router.browseYoutubeSubscriptionsUrl(),   youtubeSubscriptionsVisual)
    items.addCustomFolder(router.browseYoutubeCategoriesUrl(),      youtubeCategoriesVisual)
    
    
    
    kodiFolders = (
        #path                    #title        #thumb
        #(VIDEO_ROOT_PATH,       st(710)        None,)
        (VIDEO_ADDONS_PATH,      st(711),       None),
        (VIDEO_LIBRARY_PATH,     st(712),       None),
        (VIDEO_FILES_PATH,       st(713),       None),
        (VIDEO_PLAYLISTS_PATH,   st(714),       None),
        
        (MUSIC_ADDONS_PATH,      st(720),       None),
        (MUSIC_LIBRARY_PATH,     st(721),       None),
        #(MUSIC_FILES_PATH,      st(722),       None),
        (MUSIC_PLAYLISTS_PATH,   st(723),       None),
        
        (PROGRAM_ADDONS_PATH,    st(730),       None),
        
        (PICTURE_ADDONS_PATH,    st(731),       None),
        #(PICTURE_FILES_PATH,    ??,            None)
    )
    
    for kodiFolder in kodiFolders:
        path, title, thumb = kodiFolder        
        kodiFolder = KodiFolder.fromPath(path, title, thumb)
        items.addKodiFolder(kodiFolder, kodiFoldersVisual, root=True)
        
    
#     if 'win' in sys.platform:
#         items.addCustomFolder(router.browseLocalStorageUrl(),           localStorageVisual)
    

    items.present(viewStyle)
    
    
    
