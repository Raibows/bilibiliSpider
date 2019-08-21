<head> 
    <script defer src="https://use.fontawesome.com/releases/v5.0.13/js/all.js"></script> 
    <script defer src="https://use.fontawesome.com/releases/v5.0.13/js/v4-shims.js"></script> 
</head> 
<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.0.13/css/all.css">
<h1 id="title">📺RankSpider</h1>
<p align="center">
<a href="https://github.com/Raibows/bilibiliRankSpider/blob/master/LICENSE"><img alt="GitHub license" src="https://img.shields.io/github/license/Raibows/bilibiliRankSpider"></a>
<a href="https://github.com/Raibows/bilibiliRankSpider/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/Raibows/bilibiliRankSpider"></a>
<a href="https://github.com/Raibows/bilibiliRankSpider/network"><img alt="GitHub forks" src="https://img.shields.io/github/forks/Raibows/bilibiliRankSpider"></a>
<a href="https://github.com/Raibows/bilibiliRankSpider/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/Raibows/bilibiliRankSpider"></a>
<a href="https://www.codacy.com/app/Raibows/bilibiliRankSpider?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Raibows/bilibiliRankSpider&amp;utm_campaign=Badge_Grade"><img src="https://api.codacy.com/project/badge/Grade/51f521e5189748dbafd845f01b187817"/></a><br>
</p>
<p align="left">
A project for bilibiliRankSpider and free proxy pool. Spider used <I>requests</I> and <I>multiprocessing</I> some base packages for spider. ProxyPool used <I>Python Asyncio</I>. Hope this project could help you learn <I>Python Spider</I>.<br>
<b>This project is only for learning Python, commercial using is strictly prohibited. I will delete this project at once in case of infringement.</b><br>
Please star or fork my project if you like it 😁<br>
And welcome to propose an issue if you have bugs to feedback.
</p>

---

## Contents
- <a href="#title">Introduction</a>
- [Requirement](#requirement)
- [QuickStart](#quick-start)
- [Advanced Usage](#advanced-usage)
- [Overview](#function-overview)
- [Journal](#journal)
- [Update Record](#update-record)
- [WARNING](#warning)
---

## Requirement
| Item  |  Necessary | Statement  |
| ------------ | ------------ | ------------ |
| Linux or Windows  | <i class="fas fa-check"></i>  | Linux or Windows Supported  |
| Python Interpretor | <i class="fas fa-check"></i>  |  Make sure your Python version >=3.7 |
| Redis |  <i class="fas fa-times"></i> |  Only for ProxyPool, do not affect Spider |
|  Python Packages | <i class="fas fa-check"></i>  | Requirements List you could see in <a href="./requirements.txt">requirements.txt</a>  |
| Python Virtual Environment | <i class="fas fa-times"></i> | Not necessary but strongly suggested |

## Quick Start
1. Check your enviroment whether satisfy Requirment above.
1. Install
    clone this project to your local
    ```
    git clone https://github.com/Raibows/bilibiliRankSpider
    ```
    or <a href="https://github.com/Raibows/bilibiliRankSpider/archive/master.zip">Download</a> this project in Zip.
2. Create a new Python Virtual Environment
    ```
    virtualenv venv
    ```
    or use Conda.
3. Activate virtual environment(**virtualenv**)  
    Linux:
	```
    source ./venv/bin/activate
	```
    Windows:
	```
    . ./venv/Scripts/activate
	```
4. Install Necessary Packages
    ```
    pip3 install -r requirements.txt
    ```
5. **Make your own Configuration**  
    Create one .py file named Config in the root directory of this project. Make your configuration, for example like below
    ```
    class spider_config():
        current_path = None
        output_path = r'../data/bilibili_rank_data.csv'
        mas_proxy_flag = False
        tasks = [
            'all',
            'animation',
            'guochuang',
            'music',
            'dance',
            'game',
            'technology',
            'digital',
            'life',
            'guichu',
            'fashion',
            'entertainment',
            'movie'
        ]
        rank_type = 'origin' #or all
        multi_processor_flag = True
        mas_proxy_pool_ip = '127.0.0.1:5010'
        multi_processor_num = 2
        coroutine = True # can't change`
    ```
    I have updated my <a href="./Config.py">Config.py</a> as example. You could edit it as you like.
6. Run your Spider
    ```
    python3 run.py
    ```
## Advanced Usage
1. Select what info you want to get  
    Edit ``spider_config class`` in ``Config.py``  
    ``tasks`` attribute is **video types**, default is all types video  
    ``rank_type`` attribute is **rank types** with **origin** or **all** for you to choose, default is origin
1. Use *Multiprocessor* to accelerate spider  
    Edit ``spider_config class`` in ``Config.py``
    ```
    multi_processor_flag = True
    multi_processor_num = your cpu count
    ```
2. Use *ProxyPool* to avoid being banned  
    Here I strongly recommend <a href="https://github.com/jhao104/proxy_pool">proxy_pool</a>, more stable than my project's ProxyPool.
    - Edit ``spider_config class`` in ``Config.py`` first
        ```
        multi_processor_flag = True
        mas_proxy_pool_ip = your proxy_pool server get-proxy api address
        ```
    - Then install Redis for Linux or Windows and start Redis service
    - Lanuch <a href="https://github.com/jhao104/proxy_pool">proxy_pool</a> wait a few minutes
    - Run Spider
        ```
        python3 ./bilibiliSpider/run.py
        ```
    If you want to use **internal ProxyPool Module**, please read the below tips.
3. About **ToolBox Module**  
    ToolBox Module has a lot of useful functions for all modules in this project to use. It's necessary and fundamental for this project.
    - Change FakeHeaders Browser if you want, default is *Chrome*
    - Set your own logging_path
        ```
        logging_path = your own path
        ```
5. How to use **internal ProxyPool** ?  
    - install Redis first
    - Edit ``proxypool_config class`` in ``Config.py``
        ```
        class proxypool_config(repr_base_class):
            check_interval = 150 #seconds
            spider_interval = 300 #seconds
            print_interval = 15
            evaluate_interval = 30
            check_proxy_timeout = 10
            coroutines_semaphore = 10 #limit the number of coroutines

            database_type = 'Redis'
            database_host = 'localhost'
            database_port = '6379'
            database_password = None
            database_init_flushall = True
        ```
        Make sure your Redis Database related configurations is right. Other configurations you need to read **ProxyPool** Designs in [Overview](#function-overview).
    - Run ProxyPool
        ```
        python3 ./ProxyPool/run.py
        ``` 
    - You still need to read next tips after it runs successfully 
6. About **FlaskServer Module**  
    FlaskServer Module is for offering useful proxies from database. So just like access a website, get a useful proxy from a **special url**. And I have completed related functions in ``./bilibiliSpider/MasModule.py``that could let you get proxies and feedback to the proxies. Details are below:
    - ``mas_get_proxy_dict()``
        get a useful proxy from FlaskServer in dict format
    - ``mas_get_proxy_string()``
        get a useful proxy from FlaskServer in string format
    - ``mas_get_html(url)``
        There are 2 **different** ``mas_get_html()`` but have **the same name** functions in MasModule. If you use <a href="https://github.com/jhao104/proxy_pool">proxy_pool</a> recommended above, use the **first** ``mas_get_html()`` function and annotate the **second** ``mas_get_html()`` function.
        If you use **internal ProxyPool Module**, try the **second** ``mas_get_html()`` function.
7. Add a new api for **bilibiliSpider**  
    Edit ``bilibili_spider class`` in ``./bilibiliSpider/SpiderModule.py``, for example  
    1. add a new attribute to ``__init__()``
        ```
        self.api_xxxx = api's url
        ```
    2. add a new function to get raw info from new added api
        For example, to get one user's raw info
        ```
        def get_raw_user_info(self, mid):
            # param mid: users mid
            # return: dict, this users raw info
            url = self.api_user_info.format(mid)
            res = self.__get_html_requests(url)
            res_dict = res.json()
            return res_dict
        ```
    3. add related ``process_raw()`` to ``./bilibiliSpider/ProcessRawModule.py``

8. Add new free-proxy-website to **internal ProxyPool**  
    You need to master some *Python Async* and *Python aiohttp* to write a *async* function because **internal ProxyPool** used *Python Async**. Details could be seen in Python Official Documents.  
9. Project Structure  
    Next chapter **Function Overview** could help you a lot to know this project's design and structure.
        
## Function Overview
#### bilibiliSpider:
![avatar](https://github.com/Raibows/MarkdownPhotos/raw/master/bilibilivideohot/bilibilispider-Design1.png)
#### ProxyPool:
![avatar](https://github.com/Raibows/MarkdownPhotos/raw/master/bilibilivideohot/ProxyPool-Design1.png)

#### FlaskServer
![avatar](https://github.com/Raibows/MarkdownPhotos/raw/master/bilibilivideohot/FlaskServer-Design.png)

## Journal
1. 2019/7/4  
    Bugs and program exception occurred frequently when I update spider module to get additional video info through some other apis. And I gradually find the risk to get info directlyfrom a video page is so great. A big problem is you got aid of a video in the ranking list but this video has been deleted.Almost every functions that get info by a aid won't work well asexpected.  
    Another problem is 'guochuang' video partition has a lotof official videos. They have entirely different html page that willcause some functions collapse, like 'get_video_upload_time'.  
    Aim at the above two problems, I have tried to useunique flags and 'Try-Except' to avoid their happening. But will itfinally work? Somehow I have no confidence in it.
2. 2019/7/5  
    I didn't expect that the program failed to fetch infoagain when I check the data. And my ip was blocked by bilibili.comwhen I traversed some interfaces of it. That's was too shocking for me.Because I have thought that the bilibili.com was weak for anti-spidertechnology for a long time.  
    I used a proxy pool to solve this problem. For themajority, it works well, my ip is safe. But for some video category, the freeproxy pool will be blocked by bilibili.com, such as 'guochuang' category. Yep,'guochuang' became the problem hardship again.  
3. 2019/7/6  
    It's necessary to add error logging module for analysis.
    We need to delete these videos that could't get lengthor upload time through speical flag in data processing.
4. 2019/7/8  
    Holy shit! I forgot to get video's points info! Fuck it.So I have to do it again now. To figure out how did the website calculate the videopoints from some indexes, assume it a 
    multiple linear regression model is a good choice. Perceptron is a easy enough but nice classifier to solve linearproblem.  
    Well, the spider now is steady after I used proxy moduleand add try-catch to almost every procedure that may make errors.  
6. 2019/7/9  
    A 8-element linear function could be fit with 1000 testdata in no more than 20 iterations by perceptron. But it can't fit bilibili data. I thinkthere are at least three possible reasons caused that:
    * they are nonlinear
    * some data need to clean
    * missing some features or too much features

    Whatever, I choose to analyse the data first.
6. 2019/7/13  
    I finally choose to use *multiple processes* toaccelerate spider procedure after days of trying. At first I want to use *threads*, but threads isdead in python because of 
    GIL. Today I tried *coroutines*, but it will take manychanges if I use it. And *multiple processes* is very easy to apply to my original programframework.  
    Through testing the whole bilibili ranking(about 1300info), the spider result are below
    - single process: about 14 minutes
    - multiple processes: about 5 minutes

    It improved at least a half compared with singleprocess.
7. 2019/7/17  
    Nowadays, I'm doing some mathematic foundation for building a fully connected network with perceptron. It's easy on theory but hard on practice.  
    And today's later update has added a test module, *proxy pool module*. I borrowed from some others' proxy_pool. The biggest problem for this module is the spider efficiency is too low. *Multiple process*, *thread*, and *coroutines* are all need for better peroformance. Can't avoid using them.
8. 2019/7/22  
    Finally successfully used *coroutines* on proxy pool module! I just failed to apply it to bilibili spider module for many times a few days ago. *aiohttp*, *Python async* documentations help me a lot.  
    The proxy pool module used *multi thread*, *coroutins* up to now. I have to say the spider procedure is more than 10 times faster than before after using *coroutines*. The next few days, I will try *redis* and *Flask* to build my own proxy pool.  
9. 2019/8/9  
    Proxypool is all ready for using. It could fetch about 20 available HTTP proxies after one spider timer up to now.
    But with little regret, the *asyncio.semaphore* couldn't work normally when I try to implement semaphore to *proxy check* to control concurrency speed.  
    Now I just need to perfect *Flask Server* for the spider to use conveniently. And it will be a big work as I could see.  
10. 2019/8/17  
    Decided to remove MachineLearning module from this project. Focus on bilibili spider and Proxypool. The project is going to the end. If you have some advice or bugs feedback, please contact with me or propose an issue.   
## Update Record
1. 2019/6/12 
    * finish spider module, now could get original data from bilibili
2. 2019/7/2
    * refactoring almost everything
3. 2019/7/4
    * perfect try and catch
    * fix program not working bug for getting a not existed or deleted video info
4. 2019/7/5 
    * add proxy function
5. 2019/7/6 
    * add error logging module
6. 2019/7/8 
    * bug fix and add MachineLearning Perceptron Module
7. 2019/7/9 
    * perfect perceptron module and optimize code design 
8. 2019/7/10 
    * fixed perceptron module bug, add failure statistics
9. 2019/7/13 
    * formally support multiple processes 
10. 2019/7/16 
    * configuration supported
11. 2019/7/17 
    * add generator function for fakedata module
    * add proxy_pool module, not ready for using
12. 2019/7/18
    * Greatly adjust file structure
13. 2019/7/19
    * Changed the way of generating error data, more scientific
14. 2019/7/21
    * Try to use coroutines for proxy pool module(not avaliable now)
15. 2019/7/22
    * Apply coroutines to proxy pool module succeesully
16. 2019/7/23
    * Add redis module
    * Redis Module bugs fix, improve stability
17. 2019/7/24
    * Add Flask Server module for connecting with proxypool database
18. 2019/7/25
    * Add lots of interfaces for proxypool(pool module, database module)
19. 2019/7/26
    * Cancel the coroutines for fetching (kuaidaili.com) proxies
  (because of its anti spider strategy)
20. 2019/7/28
    * Perfect flask server api, get_one api, feedback api
21. 2019/8/2
    * Add GradientDescent module(.ipynb for jupyter Notebook)
22. 2019/8/3
    * Perceptron bias calculate bug fixed
23. 2019/8/8
    * Proxy class equal bug fixed
24. 2019/8/9
    * ProxyPool evaluate rule bug fixed
    * ProxyPool ready for using steadily
25. 2019/8/17
    * Perfect mas_module for using proxy_pool   
    * Delete MachineLearning module
26. 2019/8/19
    * add user guidance
27. 2019/8/21
    * update ``Config.py`` and perfect ``README.md``
    
## WARNING   
<b>This project is only for learning Python, commercial using is strictly prohibited. I will delete this project at once in case of infringement.</b>        
        
