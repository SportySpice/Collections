class AddToCollectionVisual:
    def __init__(self, title, textSettings, icon, thumb):
        self._title = title
        self.textSettings = textSettings
        self.icon = icon
        self.thumb = thumb
        
        
    def title(self):
        return self.textSettings.apply(self._title)
    
    
    def images(self):
        return self.icon, self.thumb
    
    
    
    
    
    
#     def __init__(self, title, textSettings, channelWord, playlistword, kodiFolderWord,
#                  sourceWordTextSettings, icon, thumb):
#         self.title = title
#         self.textSettings = textSettings
#         
#         self.channelWord = channelWord
#         self.playlistword = playlistword
#         self.kodiFolderWord = kodiFolderWord
#         self.sourceWordTextSettings = sourceWordTextSettings
#         
#         self.icon = icon
#         self.thumb = thumb
#         
#         
#     def title(self, source):
#         title = self.textSettings.apply(self.title)
#         
#         if source.isYoutube()
#             if source.isChannel()
#                 sourceWord = self.channelWord
#             else:
#                 sourceWord = self.playlistword
#         else:
#             sourceWord = self.kodiFolderWord
#         
#         sourceWord = self.sourceWordTextSettings.apply(sourceWord) 
#             
#         title = title % sourceWord
#         return title
#         
#         
#     def images(self):
#         return self.icon, self.thumb