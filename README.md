## Update Record
    - 2019/6/12 finish spider module, now could get original data from bilibili
    - 2019/7/2 refactoring almost everything
    - 2019/7/4 perfect try and catch
    - 2019/7/4 fix program not working bug for getting a not existed or deleted video info
   
## Journal
1.2019/7/4<br>
Bug and program exception occurred frequently when I update
spider module to get additional video info through some other
api. And I gradually find the risk to get info directly from 
a video page is so great. A big problem is you got aid of a video
in the ranking list but this video has been deleted. Almost every 
functions that get info by a aid won't work well as expected.<br>
Another problem is 'guochuang' video partition has a lot of official 
videos. They have entirely different html page that will cause some 
functions collapse, like 'get_video_upload_time'. <br>
Aim at the above two problems, I have tried to use unique flags and
'Try-Except' to avoid their happening. But will it finally work? Somehow
I have no confidence in it.
