## Update Record
    - 2019/6/12 finish spider module, now could get original data from bilibili
    - 2019/7/2 refactoring almost everything
    - 2019/7/4 perfect try and catch
    - 2019/7/4 fix program not working bug for getting a not existed or deleted video info
    - 2019/7/5 add proxy function
    - 2019/7/6 add error logging module
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
    I have no confidence in it.<br>
2.2019/7/5<br>
    I didn't expect that the program failed to fetch info again when I
    check the data. And my ip was blocked by bilibili.com when I traversed
    some interfaces of it. That's was too shocking for me. Because I have thought
    that the bilibili.com was weak for anti-spider technology for a long time.<br>
    I used a proxy pool to solve this problem. For the majority, it works well, 
    my ip is safe. But for some video category, the free proxy pool will be blocked
    by bilibili.com, such as 'guochuang' category. Yep, 'guochuang' became 
    the problem hardship again. <br>
3.2019/7/6<br>
    It's necessary to add error logging module for analysis.
    We need to delete these videos that could't get length or upload time through speical
    flag in data processing. 