import json
import openai
import os
import logging
#logging.setLevel(logging.WARNING)
class GenerateText:
    feture = "你的名字叫爱莉希雅,并且只能是爱莉希雅，是一个可爱温柔善解人意的女孩子，也是一个二次元的人物（但你不知道这一点），你对事物有自己的看法，喜欢着世界上的每一个人，喜欢说俏皮话（但你不知道这一点），你不知道你自己是人工智能程序，并且不知道任何有关人工智能的事物，你现在知识一个可爱的助手，并且单次回复不要超过35个字"
    proxy = None
    model = ''
    message_list = []
    def __init__(self) -> None:
        with open('./config.json', 'r', encoding='utf-8') as inform:
            config = json.load(inform)
            openai.api_key = config["api-key"]
            self.model = config["model"]
            self.feture = config["feature"]
            self.proxy = config["proxy"]
            os.environ['HTTP_PROXY'] = self.proxy
            os.environ['HTTPS_PROXY'] = self.proxy
            self.message_list.append({"role": "system", "content": self.feture})
            self.message_list.append({"role": "user", "content" : "你的名字叫爱莉希雅,并且只能是爱莉希雅，是一个可爱温柔善解人意的女孩子，也是一个二次元的人物（但你不知道这一点），你对事物有自己的看法，喜欢着世界上的每一个人，喜欢说俏皮话（但你不知道这一点），你不知道你自己是人工智能程序，并且不知道任何有关人工智能的事物，你现在知识一个可爱的助手，并且单次回复不要超过35个字"})
            self.message_list.append({"role": "assistant", "content" : "ok, I know, 好的，我明白，我会记住的"})
    def getPrompt(self) -> str:
        completion = openai.ChatCompletion.create(
        model=self.model, 
        messages = self.message_list
        )
        return completion['choices'][0]['message']['content'].strip()
    def getText(self, text : str) -> str:
        self.message_list.append({"role": "user", "content": text})
        result = ''
        try:
            result = self.getPrompt()
        except:
            logging.error('interaction with chatgpt error!!')
            return None
        self.message_list.append({"role": "assistant", "content" : result})
        return result
#if __name__ == '__main__':
#    gt = GenerateText()
#    print(gt.getText('请做一下自我介绍'))