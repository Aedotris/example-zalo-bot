import re
from zlapi import ZaloAPI, ZaloAPIException
from zlapi.models import *
from datetime import datetime

class Client(ZaloAPI):
    def __init__(self, api_key, secret_key, imei, session_cookies):
        super().__init__(api_key, secret_key, imei=imei, session_cookies=session_cookies)

    def onMessage(self, mid, author_id, message, message_object, thread_id, thread_type):
        print(f"Received message: {message} from {author_id} in thread {thread_id}, type {thread_type}, {message_object}")

        if not isinstance(message, str):
            print(f"Unexpected message type: {type(message)}")
            return

        if message.startswith(".info"):
            msg_error = f"🔴 Something went wrong\n| Không thể lấy thông tin tài khoản Zalo!"
            
            style_error = MultiMsgStyle([
                MessageStyle(offset=0, length=23, style="font", size="12", auto_format=False),
                MessageStyle(offset=2, length=21, style="color", color="#f38ba8", auto_format=False),
                MessageStyle(offset=24, length=1, style="color", color="#585b70", auto_format=False),
                MessageStyle(offset=24, length=1, style="bold", auto_format=False),
                MessageStyle(offset=25, length=len(msg_error.encode()), style="font", size="13", auto_format=False),
                MessageStyle(offset=25, length=len(msg_error.encode()), style="color", color="#cdd6f4", auto_format=False)
            ])
            
            try:
                if message_object.mentions:
                    user_id = message_object.mentions[0]['uid']
                elif message[5:].strip().isnumeric():
                    user_id = message[5:].strip()
                elif message.strip() == ".info":
                    user_id = author_id
                else:
                    self.send(Message(text=msg_error, style=style_error), thread_id, thread_type)
                    return
                
                msg = ""
                multistyle = []
                try:
                    info = self.fetchUserInfo(user_id)
                    info = info.unchanged_profiles or info.changed_profiles
                    if info is self._undefined:
                        self.send(Message(text=msg_error, style=style_error), thread_id, thread_type)
                        return

                    info = info[str(user_id)]
                    userId = info.userId or "Undefined"
                    msg += f"• User ID: {userId}\n"
                    
                    offset = self.count(msg, "•")[0]
                    length = len(msg.rsplit("• ")[-1:][0].strip())
                    length2 = len(msg.split("• User ID: ")[1].strip())
                    multistyle.append(MessageStyle(offset=offset, length=1, style="color", color="#74c7ec", auto_format=False))
                    multistyle.append(MessageStyle(offset=offset + 2, length=length, style="font", size="13", auto_format=False))
                    multistyle.append(MessageStyle(offset=offset + 2, length=length, style="color", color="#cdd6f4", auto_format=False))
                    multistyle.append(MessageStyle(offset=offset + 11, length=length2, style="color", color="#a6adc8", auto_format=False))
                    
                    userName = info.zaloName[:30] + "..." if len(info.zaloName) > 30 else info.zaloName
                    userName = self.remove_special_chars(userName)
                    msg += f"• User Name: {userName}\n"
                    
                    offset = self.count(msg, "•")[1]
                    length = len(msg.rsplit("• ")[-1:][0].strip())
                    length2 = len(msg.split("• User Name: ")[1].strip())
                    multistyle.append(MessageStyle(offset=offset, length=1, style="color", color="#74c7ec", auto_format=False))
                    multistyle.append(MessageStyle(offset=offset + 2, length=length, style="font", size="13", auto_format=False))
                    multistyle.append(MessageStyle(offset=offset + 2, length=length, style="color", color="#cdd6f4", auto_format=False))
                    multistyle.append(MessageStyle(offset=offset + 13, length=length2, style="color", color="#a6adc8", auto_format=False))
                    
                    gender = "Male" if info.gender == 0 else "Female" if info.gender == 1 else "Undefined"
                    msg += f"• Gender: {gender}\n"
                    
                    offset = self.count(msg, "•")[2]
                    length = len(msg.rsplit("• ")[-1:][0].strip())
                    length2 = len(msg.split("• Gender: ")[1].strip())
                    multistyle.append(MessageStyle(offset=offset, length=1, style="color", color="#74c7ec", auto_format=False))
                    multistyle.append(MessageStyle(offset=offset + 2, length=length, style="font", size="13", auto_format=False))
                    multistyle.append(MessageStyle(offset=offset + 2, length=length, style="color", color="#cdd6f4", auto_format=False))
                    multistyle.append(MessageStyle(offset=offset + 10, length=length2, style="color", color="#a6adc8", auto_format=False))
                    
                    status = self.remove_special_chars(info.status) or "Default"
                    msg += f"• Bio: {status}\n" 
                    
                    offset = self.count(msg, "•")[3]
                    length = len(msg.rsplit("• ")[-1:][0].strip())
                    length2 = len(msg.split("• Bio: ")[1].strip())
                    multistyle.append(MessageStyle(offset=offset, length=1, style="color", color="#74c7ec", auto_format=False))
                    multistyle.append(MessageStyle(offset=offset + 2, length=length, style="font", size="13", auto_format=False))
                    multistyle.append(MessageStyle(offset=offset + 2, length=length, style="color", color="#cdd6f4", auto_format=False))
                    multistyle.append(MessageStyle(offset=offset + 7, length=length2, style="color", color="#a6adc8", auto_format=False))
                    
                    business = info.bizPkg.label
                    business = "Yes" if business else "No"
                    msg += f"• Business: {business}\n" 
                    
                    offset = self.count(msg, "•")[4]
                    length = len(msg.rsplit("• ")[-1:][0].strip())
                    length2 = len(msg.split("• Business: ")[1].strip())
                    multistyle.append(MessageStyle(offset=offset, length=1, style="color", color="#74c7ec", auto_format=False))
                    multistyle.append(MessageStyle(offset=offset + 2, length=length, style="font", size="13", auto_format=False))
                    multistyle.append(MessageStyle(offset=offset + 2, length=length, style="color", color="#cdd6f4", auto_format=False))
                    multistyle.append(MessageStyle(offset=offset + 12, length=length2, style="color", color="#a6adc8", auto_format=False))
                    
                    dob = info.dob or info.sdob or "Hidden"
                    if isinstance(dob, int):
                        dob = datetime.fromtimestamp(dob).strftime("%d/%m/%Y")
                    msg += f"• Date Of Birth: {dob}\n" 
                    
                    offset = self.count(msg, "•")[5]
                    length = len(msg.rsplit("• ")[-1:][0].strip())
                    length2 = len(msg.split("• Date Of Birth: ")[1].strip())
                    multistyle.append(MessageStyle(offset=offset, length=1, style="color", color="#74c7ec", auto_format=False))
                    multistyle.append(MessageStyle(offset=offset + 2, length=length, style="font", size="13", auto_format=False))
                    multistyle.append(MessageStyle(offset=offset + 2, length=length, style="color", color="#cdd6f4", auto_format=False))
                    multistyle.append(MessageStyle(offset=offset + 17, length=length2, style="color", color="#a6adc8", auto_format=False))
                    
                    phoneNumber = info.phoneNumber or "Hidden"
                    msg += f"• Phone Number: {phoneNumber}\n" 
                    
                    offset = self.count(msg, "•")[6]
                    length = len(msg.rsplit("• ")[-1:][0].strip())
                    length2 = len(msg.split("• Phone Number: ")[1].strip())
                    multistyle.append(MessageStyle(offset=offset, length=1, style="color", color="#74c7ec", auto_format=False))
                    multistyle.append(MessageStyle(offset=offset + 2, length=length, style="font", size="13", auto_format=False))
                    multistyle.append(MessageStyle(offset=offset + 2, length=length, style="color", color="#cdd6f4", auto_format=False))
                    multistyle.append(MessageStyle(offset=offset + 10, length=length2, style="color", color="#a6adc8", auto_format=False))
                    
                    # Adding Last Action Time
                    lastAction = info.lastActionTime
                    if isinstance(lastAction, int):
                        lastAction = lastAction / 1000
                        timeAction = datetime.fromtimestamp(lastAction)
                        lastAction = timeAction.strftime("%H:%M %d/%m/%Y")
                    else:
                        lastAction = "Undefined"
                    msg += f"• Last Action At: {lastAction}\n" 
                    
                    offset = self.count(msg, "•")[7]
                    length = len(msg.rsplit("• ")[-1:][0].strip())
                    length2 = len(msg.split("• Last Action At: ")[1].strip())
                    multistyle.append(MessageStyle(offset=offset, length=1, style="color", color="#74c7ec", auto_format=False))
                    multistyle.append(MessageStyle(offset=offset + 2, length=length, style="font", size="13", auto_format=False))
                    multistyle.append(MessageStyle(offset=offset + 2, length=length, style="color", color="#cdd6f4", auto_format=False))
                    multistyle.append(MessageStyle(offset=offset + 18, length=length2, style="color", color="#a6adc8", auto_format=False))
                    
                    # Adding Created Time
                    createTime = info.createdTs
                    if isinstance(createTime, int):
                        createTime = datetime.fromtimestamp(createTime).strftime("%H:%M %d/%m/%Y")
                    else:
                        createTime = "Undefined"
                    msg += f"• Created Time: {createTime}\n" 
                    
                    offset = self.count(msg, "•")[8]
                    length = len(msg.rsplit("• ")[-1:][0].strip())
                    length2 = len(msg.split("• Created Time: ")[1].strip())
                    multistyle.append(MessageStyle(offset=offset, length=1, style="color", color="#74c7ec", auto_format=False))
                    multistyle.append(MessageStyle(offset=offset + 2, length=length, style="font", size="13", auto_format=False))
                    multistyle.append(MessageStyle(offset=offset + 2, length=length, style="color", color="#cdd6f4", auto_format=False))
                    multistyle.append(MessageStyle(offset=offset + 16, length=length2, style="color", color="#a6adc8", auto_format=False))
                    
                    msg_to_send = Message(text=msg, style=MultiMsgStyle(multistyle))
                    self.replyMessage(msg_to_send, message_object, thread_id, thread_type)
                except ZaloAPIException as e:
                    print(f"Error fetching user info: {e}")
                    self.send(Message(text=msg_error, style=style_error), thread_id, thread_type)
            except Exception as e:
                print(f"Error: {e}")
                self.send(Message(text=msg_error, style=style_error), thread_id, thread_type)

    def remove_special_chars(self, string):
        return re.sub(r'[^a-zA-Z0-9-\sàáãạảăắằẳẵặâấầẩẫậèéẹẻẽêềếểễệìíịỉĩòóõọỏôốồổỗộơớờởỡợùúũụủưứừửữựỳýỵỷỹÀÁÃẠẢĂẮẰẲẴẶÂẤẦẨẪẬÈÉẸẺẼÊỀẾỂỄỆÌÍỊỈĨÒÓÕỌỎÔỐỒỔỖỘƠỚỜỞỠỢÙÚŨỤỦƯỨỪỬỮỰỲÝỴỶỸ]', '', string)

    def count(self, string: str, word: str) -> list:
        indices = []
        start = 0
        while True:
            idx = string.find(word, start)
            
            if idx == -1:
                break
            
            indices.append(idx)
            start = idx + 1
        
        return indices


imei = ""
session_cookies = {

}
client = Client('api_key', 'secret_key', imei=imei, session_cookies=session_cookies)
client.listen()
