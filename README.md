## Update Record
    - 2019/6/12 
        finish spider module, now could get original data from bilibili
    - 2019/7/2
        refactoring almost everything
    - 2019/7/4
        perfect try and catch
        fix program not working bug for getting a not existed or deleted video info
    - 2019/7/5 
        add proxy function
    - 2019/7/6 
        add error logging module
    - 2019/7/8 
        bug fix and add MachineLearning Perceptron Module
    - 2019/7/9 
        perfect perceptron module and optimize code design 
    - 2019/7/10 
        fixed perceptron module bug, add failure statistics
    - 2019/7/13 
        formally support multiple processes 
    - 2019/7/16 
        configuration supported
    - 2019/7/17 
        add generator function for fakedata module
        add proxy_pool module, not ready for using
    - 2019/7/18
        Greatly adjust file structure
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
    flag in data processing. <br>
4.2019/7/8<br>
    Holy shit! I forgot to get video's points info! Fuck it. So I have to do it again now.
    To figure out how did the website calculate the video points from some indexes, assume it a 
    multiple linear regression model is a good choice. Perceptron is a
    a easy enough but nice classifier to solve linear problem.<br>
    Well, the spider now is steady after I used proxy module and add try-catch to almost every 
    procedure that may make errors.<br>
5.2019/7/9<br>
    A 8-element linear function could be fit with 1000 test data in no more than 20 iterations by
    perceptron. But it can't fit bilibili data. I think there are at least three possible reasons
    caused that:<br>
    1. they are nonlinear<br>
    2. some data need to clean<br>
    3. missing some features or too much features<br>
    Whatever, I choose to analyse the data first.<br>
6.2019/7/13<br>
    I finally choose to use *multiple processes* to accelerate spider procedure after days of 
    trying. At first I want to use *threads*, but threads is dead in python because of 
    GIL. Today I tried *coroutines*, but it will take many changes if I use it. And *multiple processes*
    is very easy to apply to my original program framework.<br>
    Through testing the whole bilibili ranking(about 1300 info), the spider result are below<br>
    - single process: about 14 minutes<br>
    - multiple processes: about 5 minutes<br>
    It improved at least a half compared with single process.<br>
7.2019/7/17<br>
    Nowadays, I'm doing some mathematic foundation for building a fully connected network with perceptron. It's easy on theory but hard on practice.<br>
    And today's later update has added a test module, *proxy pool module*. I borrowed from some others' proxy_pool. The biggest problem for this module is the spider efficiency is too low. *Multiple process*, *thread*, and *coroutines* are all need for better peroformance. Can't avoid using
    them.
    
    
    
    
        
        
