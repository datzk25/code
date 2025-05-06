import discord
from discord.ext import commands
import threading
import time
import re
import requests
import os
import random

TOKEN = input("Token bot: ")
ADMIN_ID = int(input("ID admin: "))

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

allowed_users = set()
treo_threads = {}
treo_start_times = {}
messenger_instances = {}
nhay_threads = {}
nhay_start_times = {}
reo_threads = {}
reo_start_times = {}
chui_threads = {}
chui_start_times = {}
codelag_threads = {}
codelag_start_times = {}

UA_KIWI = [
    "Mozilla/5.0 (Linux; Android 11; RMX2185) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.140 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Redmi Note 11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.129 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel 6a) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.68 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; V2031) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.60 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; CPH2481) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.86 Mobile Safari/537.36"
]

UA_VIA = [
    "Mozilla/5.0 (Linux; Android 10; Redmi Note 8) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/108.0.0.0 Mobile Safari/537.36 Via/4.8.2",
    "Mozilla/5.0 (Linux; Android 11; V2109) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/112.0.5615.138 Mobile Safari/537.36 Via/4.9.0",
    "Mozilla/5.0 (Linux; Android 13; TECNO POVA 5) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/114.0.5735.134 Mobile Safari/537.36 Via/5.0.1",
    "Mozilla/5.0 (Linux; Android 12; Infinix X6710) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/115.0.5790.138 Mobile Safari/537.36 Via/5.2.0",
    "Mozilla/5.0 (Linux; Android 14; SM-A546E) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/122.0.6261.112 Mobile Safari/537.36 Via/5.3.1"
]

USER_AGENTS = UA_KIWI + UA_VIA

class Messenger:
    def __init__(self, cookie):
        self.cookie = cookie
        self.user_id = self.id_user()
        self.user_agent = random.choice(USER_AGENTS)
        self.fb_dtsg = None
        self.init_params()

    def id_user(self):
        try:
            c_user = re.search(r"c_user=(\d+)", self.cookie).group(1)
            return c_user
        except:
            raise Exception("Cookie không hợp lệ")

    def init_params(self):
        headers = {
            'Cookie': self.cookie,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,vi;q=0.8',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1'
        }

        try:
            response = requests.get('https://www.facebook.com', headers=headers)
            fb_dtsg_match = re.search(r'"token":"(.*?)"', response.text)

            if not fb_dtsg_match:
                response = requests.get('https://mbasic.facebook.com', headers=headers)
                fb_dtsg_match = re.search(r'name="fb_dtsg" value="(.*?)"', response.text)

                if not fb_dtsg_match:
                    response = requests.get('https://m.facebook.com', headers=headers)
                    fb_dtsg_match = re.search(r'name="fb_dtsg" value="(.*?)"', response.text)

            if fb_dtsg_match:
                self.fb_dtsg = fb_dtsg_match.group(1)
            else:
                raise Exception("Không thể lấy được fb_dtsg")

        except Exception as e:
            raise Exception(f"Lỗi khi khởi tạo tham số: {str(e)}")

    def gui_tn(self, recipient_id, message, max_retries=10):
        for attempt in range(max_retries):
            timestamp = int(time.time() * 1000)
            offline_threading_id = str(timestamp)
            message_id = str(timestamp)

            data = {
                'thread_fbid': recipient_id,
                'action_type': 'ma-type:user-generated-message',
                'body': message,
                'client': 'mercury',
                'author': f'fbid:{self.user_id}',
                'timestamp': timestamp,
                'source': 'source:chat:web',
                'offline_threading_id': offline_threading_id,
                'message_id': message_id,
                'ephemeral_ttl_mode': '',
                '__user': self.user_id,
                '__a': '1',
                '__req': '1b',
                '__rev': '1015919737',
                'fb_dtsg': self.fb_dtsg
            }

            headers = {
                'Cookie': self.cookie,
                'User-Agent': self.user_agent,
                'Accept': '*/*',
                'Accept-Language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Origin': 'https://www.facebook.com',
                'Referer': f'https://www.facebook.com/messages/t/{recipient_id}',
                'Host': 'www.facebook.com',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'empty'
            }

            try:
                response = requests.post(
                    'https://www.facebook.com/messaging/send/',
                    data=data,
                    headers=headers
                )
                if response.status_code != 200:
                    return {
                        'success': False,
                        'error': 'HTTP_ERROR',
                        'error_description': f'Status code: {response.status_code}'
                    }

                if 'for (;;);' in response.text:
                    clean_text = response.text.replace('for (;;);', '')
                    try:
                        result = json.loads(clean_text)
                        if 'error' in result:
                            return {
                                'success': False,
                                'error': result.get('error'),
                                'error_description': result.get('errorDescription', 'Unknown error')
                            }
                        return {
                            'success': True,
                            'message_id': message_id,
                            'timestamp': timestamp
                        }
                    except json.JSONDecodeError:
                        pass

                return {
                    'success': True,
                    'message_id': message_id,
                    'timestamp': timestamp
                }
            except Exception as e:
                return {
                    'success': False,
                    'error': 'REQUEST_ERROR',
                    'error_description': str(e)
                }

def format_duration(seconds):
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    parts = []
    if d: parts.append(f"{d} ngày")
    if h: parts.append(f"{h} giờ")
    if m: parts.append(f"{m} phút")
    if s or not parts: parts.append(f"{s} giây")
    return " ".join(parts)

def start_spam(user_id, idbox, cookie, message, delay):
    try:
        messenger = Messenger(cookie)
    except Exception as e:
        return f"Lỗi cookie: {str(e)}"

    def loop_send():
        while (user_id, idbox) in treo_threads:
            success = messenger.gui_tn(idbox, message)
            print(f"Gửi Tin Nhắn {'Thành Công' if success else 'Thất Bại'}")
            time.sleep(delay)

    key = (user_id, idbox)
    thread = threading.Thread(target=loop_send)
    treo_threads[key] = thread
    treo_start_times[key] = time.time()
    messenger_instances[key] = messenger
    thread.start()
    return "Đã bắt đầu gửi tin nhắn."
    
def start_nhay(user_id, idbox, cookie, delay):
    if not os.path.exists("nhay.txt"):
        return "Không tìm thấy file nhay.txt."
    try:
        messenger = Messenger(cookie)
    except Exception as e:
        return f"Lỗi cookie: {str(e)}"

    with open("nhay.txt", "r", encoding="utf-8") as f:
        messages = [line.strip() for line in f if line.strip()]

    if not messages:
        return "File nhay.txt không có nội dung."

    def loop_nhay():
        index = 0
        while (user_id, idbox) in nhay_threads:
            message = messages[index % len(messages)]
            success = messenger.gui_tn(idbox, message)
            print(f"Gửi tin nhắn {'Thành công' if success else 'Thất bại'}")
            time.sleep(delay)
            index += 1

    key = (user_id, idbox)
    thread = threading.Thread(target=loop_nhay)
    nhay_threads[key] = thread
    nhay_start_times[key] = time.time()
    thread.start()
    return "Đã bắt đầu nhây."
    
def start_reo(user_id, name, cookie, delay):
    if not os.path.exists("reo.txt"):
        return "Không tìm thấy file reo.txt."
    try:
        messenger = Messenger(cookie)
    except Exception as e:
        return f"Lỗi cookie: {str(e)}"

    with open("reo.txt", "r", encoding="utf-8") as f:
        messages = [line.strip() for line in f if line.strip()]

    if not messages:
        return "File reo.txt không có nội dung."

    def loop_reo():
        index = 0
        while (user_id, name) in reo_threads:
            message = messages[index % len(messages)]
            success = messenger.gui_tn(name, message)
            print(f"Gửi tin nhắn {'Thành công' if success else 'Thất bại'}")
            time.sleep(delay)
            index += 1

    key = (user_id, name)
    thread = threading.Thread(target=loop_reo)
    reo_threads[key] = thread
    reo_start_times[key] = time.time()
    thread.start()
    return f"Đã bắt đầu reo cho {name}."
    
def start_chui(user_id, idbox, cookie, delay):
    if not os.path.exists("chui.txt"):
        return "Không tìm thấy file chui.txt."
    try:
        messenger = Messenger(cookie)
    except Exception as e:
        return f"Lỗi cookie: {str(e)}"

    with open("chui.txt", "r", encoding="utf-8") as f:
        messages = [line.strip() for line in f if line.strip()]

    if not messages:
        return "File chui.txt không có nội dung."

    def loop_chui():
        index = 0
        while (user_id, idbox) in chui_threads:
            message = messages[index % len(messages)]
            success = messenger.gui_tn(idbox, message)
            print(f"Gửi tin nhắn {'Thành công' if success else 'Thất bại'}")
            time.sleep(delay)
            index += 1

    key = (user_id, idbox)
    thread = threading.Thread(target=loop_chui)
    chui_threads[key] = thread
    chui_start_times[key] = time.time()
    thread.start()
    return "Đã bắt đầu gửi tin nhắn."       
    
def start_codelag(user_id, idbox, cookie, delay):
    if not os.path.exists("codelag.txt"):
        return "Không tìm thấy file codelag.txt."
    try:
        messenger = Messenger(cookie)
    except Exception as e:
        return f"Lỗi cookie: {str(e)}"

    with open("codelag.txt", "r", encoding="utf-8") as f:
        messages = [line.strip() for line in f if line.strip()]

    if not messages:
        return "File codelag.txt không có nội dung."

    def loop_codelag():
        index = 0
        while (user_id, idbox) in codelag_threads:
            message = messages[index % len(messages)]
            success = messenger.gui_tn(idbox, message)
            print(f"Gửi tin nhắn {'Thành công' if success else 'Thất bại'}")
            time.sleep(delay)
            index += 1

    key = (user_id, idbox)
    thread = threading.Thread(target=loop_codelag)
    codelag_threads[key] = thread
    codelag_start_times[key] = time.time()
    thread.start()
    return "Đã bắt đầu spam code lag."               

@bot.command()
async def set(ctx):
    if ctx.author.id not in allowed_users and ctx.author.id != ADMIN_ID:
        return await ctx.send("Bạn chưa thuê bot ?")
    if not ctx.message.attachments:
        return await ctx.send("Vui lòng đính kèm file .txt.")
    attachment = ctx.message.attachments[0]
    if not attachment.filename.endswith(".txt"):
        return await ctx.send("Chỉ chấp nhận file .txt.")
    path = f"{ctx.author.id}_{attachment.filename}"
    await attachment.save(path)
    await ctx.send(f"Đã lưu file thành công dưới tên: `{path}`.")

@bot.command()
async def treo(ctx, idbox: str, cookie: str, filename: str, delay: int):
    if ctx.author.id not in allowed_users and ctx.author.id != ADMIN_ID:
        return await ctx.send("Bạn chưa thuê bot ?")
    filepath = f"{ctx.author.id}_{filename}"
    if not os.path.exists(filepath):
        return await ctx.send("Không tìm thấy file đã set.")
    with open(filepath, "r", encoding="utf-8") as f:
        message = f.read()
    result = start_spam(ctx.author.id, idbox, cookie, message, delay)
    await ctx.send(result)

@bot.command()
async def stoptreo(ctx, idbox: str):
    removed = False
    keys_to_remove = [(uid, ib) for (uid, ib) in treo_threads if uid == ctx.author.id and ib == idbox]
    for key in keys_to_remove:
        treo_threads.pop(key)
        treo_start_times.pop(key)
        messenger_instances.pop(key)
        removed = True
    if removed:
        await ctx.send(f"Đã dừng các tab treo với idbox {idbox}.")
    else:
        await ctx.send("Không có tab treo nào.")

@bot.command()
async def tabtreo(ctx):
    msg = "**Danh Sách Tab treo:**\n\n"
    count = 0
    for (uid, ib), start in treo_start_times.items():
        if uid == ctx.author.id:
            uptime = format_duration(time.time() - start)
            msg += f"**{ib}:** {uptime}\n"
            count += 1
    if count == 0:
        msg = "Bạn không có tab treo nào đang chạy."
    await ctx.send(msg)

@bot.command()
async def add(ctx, iduser: int):
    if ctx.author.id != ADMIN_ID:
        return await ctx.send("Chỉ admin được dùng lệnh này.")
    allowed_users.add(iduser)
    await ctx.send(f"Đã thêm {iduser} vào danh sách sử dụng bot.")

@bot.command()
async def xoa(ctx, iduser: int):
    if ctx.author.id != ADMIN_ID:
        return await ctx.send("Chỉ admin được dùng lệnh này.")
    allowed_users.discard(iduser)
    await ctx.send(f"Đã xóa {iduser} khỏi danh sách sử dụng bot.")
    
@bot.command()
async def nhay(ctx, idbox: str, cookie: str, delay: int):
    if ctx.author.id not in allowed_users and ctx.author.id != ADMIN_ID:
        return await ctx.send("Bạn chưa thuê bot ?")
    result = start_nhay(ctx.author.id, idbox, cookie, delay)
    await ctx.send(result)    

@bot.command()
async def stopnhay(ctx, idbox: str):
    key = (ctx.author.id, idbox)
    if key in nhay_threads:
        nhay_threads.pop(key)
        nhay_start_times.pop(key)
        await ctx.send(f"Đã dừng nhây vào {idbox}.")
    else:
        await ctx.send("Không có tab nhây nào đang chạy.")

@bot.command()
async def tabnhay(ctx):
    msg = "**Danh Sách Tab nhây:**\n\n"
    count = 0
    for (uid, ib), start in nhay_start_times.items():
        if uid == ctx.author.id:
            uptime = format_duration(time.time() - start)
            msg += f"**{ib}:** {uptime}\n"
            count += 1
    if count == 0:
        msg = "Bạn không có tab nhây nào đang chạy."
    await ctx.send(msg) 
    
@bot.command()
async def reo(ctx, idbox: str, cookie: str, delay: int):
    if ctx.author.id not in allowed_users and ctx.author.id != ADMIN_ID:
        return await ctx.send("Bạn chưa thuê bot ?")
    result = start_reo(ctx.author.id, idbox, cookie, delay)
    await ctx.send(result)    

@bot.command()
async def stopreo(ctx, idbox: str):
    key = (ctx.author.id, idbox)
    if key in reo_threads:
        reo_threads.pop(key)
        reo_start_times.pop(key)
        await ctx.send(f"Đã dừng nhây vào {idbox}.")
    else:
        await ctx.send("Không có tab nhây nào đang chạy.")

@bot.command()
async def tabreo(ctx):
    msg = "**Danh Sách Tab nhây:**\n\n"
    count = 0
    for (uid, ib), start in reo_start_times.items():
        if uid == ctx.author.id:
            uptime = format_duration(time.time() - start)
            msg += f"**{ib}:** {uptime}\n"
            count += 1
    if count == 0:
        msg = "Bạn không có tab nhây nào đang chạy."
    await ctx.send(msg) 
   
@bot.command()
async def chui(ctx, idbox: str, cookie: str, delay: int):
    if ctx.author.id not in allowed_users and ctx.author.id != ADMIN_ID:
        return await ctx.send("Bạn chưa thuê bot ?")
    result = start_chui(ctx.author.id, idbox, cookie, delay)
    await ctx.send(result)
    
@bot.command()
async def stopchui(ctx, idbox: str):
    key = (ctx.author.id, idbox)
    if key in chui_threads:
        chui_threads.pop(key)
        chui_start_times.pop(key)
        await ctx.send(f"Đã dừng gửi tin nhắn vào {idbox}.")
    else:
        await ctx.send("Không có tab nào đang chạy.")
 
@bot.command()
async def tabchui(ctx):
    msg = "**Danh Sách Tab:**\n\n"
    count = 0
    for (uid, ib), start in chui_start_times.items():
        if uid == ctx.author.id:
            uptime = format_duration(time.time() - start)
            msg += f"**{ib}:** {uptime}\n"
            count += 1
    if count == 0:
        msg = "Bạn không có tab nào đang chạy."
    await ctx.send(msg)
    
@bot.command()
async def codelag(ctx, idbox: str, cookie: str, delay: int):
    if ctx.author.id not in allowed_users and ctx.author.id != ADMIN_ID:
        return await ctx.send("Bạn chưa thuê bot ?")
    result = start_codelag(ctx.author.id, idbox, cookie, delay)
    await ctx.send(result)
             
@bot.command()
async def stopcodelag(ctx, idbox: str):
    key = (ctx.author.id, idbox)
    if key in codelag_threads:
        codelag_threads.pop(key)
        codelag_start_times.pop(key)
        await ctx.send(f"Đã dừng spam code lag vào {idbox}.")
    else:
        await ctx.send("Không có tab code lag nào đang chạy.")
        
@bot.command()
async def tabcodelag(ctx):
    msg = "**Danh Sách Tab code lag:**\n\n"
    count = 0
    for (uid, ib), start in codelag_start_times.items():
        if uid == ctx.author.id:
            uptime = format_duration(time.time() - start)
            msg += f"**{ib}:** {uptime}\n"
            count += 1
    if count == 0:
        msg = "Bạn không có tab code lag nào đang chạy."
    await ctx.send(msg)
    
@bot.command()
async def menu(ctx):
    await ctx.send(
        "╔═━━━｡ﾟ☆: *.☽ .* :☆ﾟ.━━━═╗ \n"
        "  『 🌸 ADMIN BY : Nguyễn Tiến Đạt 🌸 』 \n"
        "╚═━━━ﾟ☆: *.☽ .* :☆ﾟ.━━━═╝ \n\n"
        "✨ **All Lệnh Siêu Đáng Yêu** ✨ \n\n"
        "📂 **/set** \n"
        "↳ Gửi file TXT siêu xinh để chuẩn bị spam.\n\n"
        "⏳ **/treo `idbox \"cookie\" file.txt delay`**\n"
        "↳ Treo tin nhắn 24/7, mượt mà không lag!\n"
        "❌ **/stoptreo `idbox`**\n"
        "📋 **/tabtreo** — Xem tab treo siêu lung linh.\n\n""💃 **/nhay `idbox \"cookie\" delay`**\n"
        "↳ Nhây cực kỳ dễ thương, nhẹ nhàng nhưng đầy uy lực! \n"
        "❌ **/stopnhay `idbox`**  \n"
        "📋 **/tabnhay** — Tab nhây cực kỳ vui.  \n\n"
        "⚡ **/chui `idbox \"cookie\" delay`**  \n"
        "↳ Chửi đổng siêu “chanh sả”, vừa hài vừa toxic.  \n"
        "❌ **/stopchui `idbox`**  \n"
        "📋 **/tabchui** — Tab chửi gây viral.  \n\n"
        "💥 **/codelag `idbox \"cookie\" delay`**  \n"
        "↳ Thả code lag nhẹ nhàng mà vẫn “rung chuyển” cả hệ thống.  \n"
        "❌ **/stopcodelag `idbox`**  \n"
        "📋 **/tabcodelag** — Tab gây lú mạnh mẽ.  \n\n"
        "✨ **/add `iduser`**  \n"
        "↳ Tuyển admin siêu dễ thương.  \n"
        "❌ **/xoa `iduser`**  \n"
        "↳ Tạm biệt admin không hợp vibe.  \n"
        "📜 **/menu**  \n"
        "↳ Xem lại menu cực kỳ dễ thương này!\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🌸 **Admin dễ cưng**: Tiến Đạt\n"
        "🇻🇳 **FB**: Tiến Đạt ( Real)\n"
        "📱 **Zalo**: 0395988143\n"
        "━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "╰─═☆*･゜ﾟ･*✧･゜ﾟ･*☆═─╯"
    )

bot.run(TOKEN)