import requests

from loguru import logger
from API.api_message import at_user
from API.api_iirose import APIIirose  # 大部分接口都在这里
from globals.globals import GlobalVal  # 一些全局变量 now_room_id 是机器人当前所在的房间标识，websocket是ws链接，请勿更改其他参数防止出bug，也不要去监听ws，websockets库只允许一个接收流
from API.api_get_config import get_master_id  # 用于获取配置文件中主人的唯一标识
from API.decorator.command import on_command, MessageType  # 注册指令装饰器和消息类型Enmu

API = APIIirose()  # 吧class定义到变量就不会要求输入self了（虽然我都带了装饰器没有要self的 直接用APIIirose也不是不可以 习惯了

api = "https://api.xingzhige.com/API/anime/?type="

@on_command('>番剧 ', True, command_type=[MessageType.room_chat, MessageType.private_chat])  # substring可输入布朗类型也可以是列表，用于取左侧的消息，第二个参数为数字类，框架会取这个数字的左侧，如果发送的消息=左侧这几个数字的消息就会执行此函数，函数需要有两个参数，第二个参数会返回去除指令的消息
async def animesearch(Message, text):
    para = text.split(" ")
    newline = "\n"
    if len(para) == 1:
        num = 1
        anime = []
        animelist = requests.post(f'{api}3&msg={para[0]}').json()
        for i in animelist["data"]:
            anime.append(f'番剧编号：{num}\n番剧名称：{i["name"]}\n[{i["image"]}#e]\n番剧状态：{i["ji"]}\n年份：{i["year"]}')
            num+=1
        await API.send_msg(Message, 
                        f'以下是搜索结果：\n'
                        f'{newline+newline.join(anime)}\n'
                        f'使用“>番剧 {text} 番剧编号”命令获取详情')
    elif len(para) == 2:
        animeinfo = requests.post(f'{api}3&msg={para[0]}&n={para[1]}').json()
        await API.send_msg(Message,
                           f'以下是番剧{animeinfo["data"]["name"]}的详情\n'
                           f'番剧名称：{animeinfo["data"]["name"]}\n'
                           f'[{animeinfo["data"]["image"]}#e]\n'
                           f'番剧简介：{animeinfo["data"]["desc"]}\n'
                           f'番剧标签：{animeinfo["data"]["class"]}\n'
                           f'番剧集数：{len(animeinfo["data"]["playlist"])}集\n'
                           f'使用“>番剧 {para[0]} {para[1] } 集数”点播番剧\n'
                           f'使用“>发送 {para[0]} {para[1] } 集数”以视频方式发送')
    elif len(para) == 3:
        animedata = requests.post(f'{api}3&msg={para[0]}&n={para[1]}&nn={para[2]}').json()
        await API.play_media(media_type=False,
                             media_url=animedata["data"]["play_url"],
                             media_name=animedata["data"]["name"],
                             media_auther=animedata["data"]["play_num"])

@on_command('>发送 ', True, command_type=[MessageType.room_chat, MessageType.private_chat])
async def animefile(Message, text):
    para = text.split(" ")
    newline = "\n"
    if len(para) == 1:
        num = 1
        anime = []
        animelist = requests.post(f'{api}1&msg={para[0]}').json()
        for i in animelist["data"]:
            anime.append(f'番剧编号：{num}\n番剧名称：{i["name"]}\n[{i["image"]}#e]\n番剧状态：{i["ji"]}\n年份：{i["year"]}')
            num+=1
        await API.send_msg(Message, 
                        f'以下是搜索结果：\n'
                        f'{newline+newline.join(anime)}\n'
                        f'使用“>番剧 {text} 番剧编号”命令获取详情')
    elif len(para) == 2:
        animeinfo = requests.post(f'{api}1&msg={para[0]}&n={para[1]}').json()
        await API.send_msg(Message,
                           f'以下是番剧{animeinfo["data"]["name"]}的详情\n'
                           f'番剧名称：{animeinfo["data"]["name"]}\n'
                           f'[{animeinfo["data"]["image"]}#e]\n'
                           f'番剧简介：{animeinfo["data"]["desc"]}\n'
                           f'番剧标签：{animeinfo["data"]["class"]}\n'
                           f'番剧集数：{len(animeinfo["data"]["playlist"])}集\n'
                           f'使用“>发送 {para[0]} {para[1] } 集数”以视频方式发送')

    para = text.split(" ")
    if len(para) == 3:
        animedata = requests.post(f'{api}1&msg={para[0]}&n={para[1]}&nn={para[2]}').json()
        await API.send_msg(Message, 
                           f'{at_user(Message.user_name)}，这是您点播的番剧'
                           f'{animedata["data"]["play_url"]}#.mp4')

