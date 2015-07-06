# 
# from src.li.visual.TextSettings import TextSettings
# 
# #Location = enum(OFF=False, LEFT=1, MIDDLE=2, RIGHT=3)
# 
# #CountType = enum (VIEWS=1, SUBSCRIBERS=2, VIDEOS=3, NEW_VIDEOS=4)
# 
# 
# class CountTextSettings(TextSettings):
#     def __init__(self, color, bold, italic, location, show=True):
#         self.super = super(CountTextSettings, self)
#         
#         self.super.__init__(color, bold, italic, show)                
#         self.location = location        
#         
#         
#         
#         
#         
#     #overrides original method        
#     def apply(self, text):
#         if not self.show:
#             return ''
#         
#         text = '%s' % self.super.apply(text)        
#         if self.location == Location.LEFT_ALIGNED:
#             pass
#         else:
#             text = '(%s)' % text
#             
#         
#         return text
#     
#     
#     
#     
#   
# 
# 
# 
# 
# 
#     
#     
#     
# def fromOther(countTS):
#     c = countTS
#     return CountTextSettings(c.color, c.bold, c.italic, c.location, c.show)