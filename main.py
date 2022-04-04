import requests, json, os, base64

cookie = os.environ["COOKIE"]
agentid = os.environ["AGENTID"]
secret = os.environ["SECRET"]
companyid = os.environ["COMPANYID"]

# wecom 函数
def send_to_wecom(text,wecom_cid,wecom_aid,wecom_secret,wecom_touid='@all'):
    get_token_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={wecom_cid}&corpsecret={wecom_secret}"
    response = requests.get(get_token_url).content
    access_token = json.loads(response).get('access_token')
    if access_token and len(access_token) > 0:
        send_msg_url = f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}'
        data = {
            "touser":wecom_touid,
            "agentid":wecom_aid,
            "msgtype":"text",
            "text":{
                "content":text
            },
            "duplicate_check_interval":600
        }
        response = requests.post(send_msg_url,data=json.dumps(data)).content
        return response
    else:
        return False

def send_to_wecom_image(base64_content,wecom_cid,wecom_aid,wecom_secret,wecom_touid='@all'):
    get_token_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={wecom_cid}&corpsecret={wecom_secret}"
    response = requests.get(get_token_url).content
    access_token = json.loads(response).get('access_token')
    if access_token and len(access_token) > 0:
        upload_url = f'https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={access_token}&type=image'
        upload_response = requests.post(upload_url, files={
            "picture": base64.b64decode(base64_content)
        }).json()
        if "media_id" in upload_response:
            media_id = upload_response['media_id']
        else:
            return False

        send_msg_url = f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}'
        data = {
            "touser":wecom_touid,
            "agentid":wecom_aid,
            "msgtype":"image",
            "image":{
                "media_id": media_id
            },
            "duplicate_check_interval":600
        }
        response = requests.post(send_msg_url,data=json.dumps(data)).content
        return response
    else:
        return False

def send_to_wecom_markdown(text,wecom_cid,wecom_aid,wecom_secret,wecom_touid='@all'):
    get_token_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={wecom_cid}&corpsecret={wecom_secret}"
    response = requests.get(get_token_url).content
    access_token = json.loads(response).get('access_token')
    if access_token and len(access_token) > 0:
        send_msg_url = f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}'
        data = {
            "touser":wecom_touid,
            "agentid":wecom_aid,
            "msgtype":"markdown",
            "markdown":{
                "content":text
            },
            "duplicate_check_interval":600
        }
        response = requests.post(send_msg_url,data=json.dumps(data)).content
        return response
    else:
        return False


def main():
    checkin_url= "https://glados.rocks/api/user/checkin"
    status_url= "https://glados.rocks/api/user/status"
    traffic_url= "https://glados.rocks/api/user/traffic"
    referer = 'https://glados.rocks/console/checkin'
    origin = "https://glados.rocks"
    useragent = "Mozilla/5.0 (X11; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0"
    payload={
        'token': 'glados_network'
    }
    checkin = requests.post(checkin_url,headers={'cookie': cookie ,'referer': referer,'origin':origin,'user-agent':useragent,'content-type':'application/json;charset=UTF-8'},data=json.dumps(payload))
    state =  requests.get(status_url,headers={'cookie': cookie ,'referer': referer,'origin':origin,'user-agent':useragent})
    traffic =  requests.get(traffic_url,headers={'cookie': cookie ,'referer': referer,'origin':origin,'user-agent':useragent})
    today = traffic.json()['data']['today']
    if 'message' in checkin.text:
        mess = checkin.json()['message']
        time = state.json()['data']['leftDays']
        time = time.split('.')[0]
        total = 200
        use = today/1024/1024/1024
        str = '[base] %s , you have %s days left. use: %.3f/%dGB(%.2f%%)' % (mess, time, use, total, use/total*100)
    else:
        str = "cookie 已经过期了"
    ret = send_to_wecom(str, companyid, agentid, secret)
    print(str, ret)

if __name__ == '__main__':
    main()
