if __name__ == '__main__':

    import requests
    string_url = r'http://127.0.0.1:5010/proxy/get_one/string'
    dict_url = r'http://127.0.0.1:5010/proxy/get_one/dict'
    feedback_url = r'http://127.0.0.1:5010/proxy/feedback'
    # res = requests.get(dict_url)
    feedback = {"http":"http://111.23.214.123:23"}
    post_info = {
        'proxy': feedback,
        'flag': 'increase',
    }
    res = requests.post(
        url=feedback_url,
        data=post_info
    )


    pass