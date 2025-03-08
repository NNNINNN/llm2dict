# llm2dict

**llm2dict** 通过与大型语言模型（LLM）的两次交互，将自然语言的回答自动转换为结构化的 Python **字典dict** / **列表list**。

<!-- 旨在通过与大语言模型（LLM）的两次交互，将自然语言转换为结构化的 Python 字典或列表数据。这个包的核心功能是通过两次提问，第一次获取大语言模型的自然语言回答，第二次则提取特定格式的数据并将其转换为 Python 可执行的代码，最终返回结构化的数据(**dict**或**list**)。 -->
 
### 功能特点  

**llm2dict** 将提取格式的任务交给了 LLM 处理：

- 第一次提问：获取 LLM 的自然语言回答。 
- 第二次提问：让 LLM 根据第一次的回答和指定的数据结构，生成提取数据的 Python 代码。 
- 代码执行：自动执行生成的代码，返回结构化的数据。 

你只需输入问题和期望的数据结构，即可获得**关键词确定**的结构化的数据。

### 优点  

- 让LLM的注意力回到问题本身，而非关注数据结构
- 返回确定的数据结构，无需手动编写提取函数
  
### 缺点  
- Token消耗会变大


### 其他  
- 需要使用QWQ32b/deepseek-r1:671b或同等智能的模型
- 仍有一定几率提取失败

## 安装与使用  

你可以通过以下命令安装 **llm2dict** 包：
```bash
pip install llm2dict
```  

**使用示例**  
```python
from llm2dict import llm2dict,LLM_API,add_user,add_system
#  调用硅基流动的LLM API: https://cloud.siliconflow.cn/models
api_key = "<修改成你的api_key>"
url = "https://api.siliconflow.cn/v1/chat/completions"
model_name = "Qwen/QwQ-32B"
llm=LLM_API(api_key,model_name,url)
llm.max_tokens=16000 #QwQ-32B 推理模型 口水比较多 max_tokens要设长一点,不然答案还没生完就中断了
llm.max_seq_len=16000

# 构建提问,[{"role": "system", "content": "设定"},{"role": "user", "content": "提问"},...]
提问 = add_system([],"你是专业的作词语作曲家,从专业的歌曲创作角度出发思考,帮助用户完成歌曲写作")
提问 = add_user(提问,"写关于爱情的歌，要顺口，歌词不要太多重复，可以短一点。写一下这首歌的简介（50字）。起一个歌名。为这首歌写一个吸引人的长句标题（参考小红书风格）。写5条这首歌的评论（参考网易云音乐的评论风格）")

#str 用文本设定返回的数据结构
返回格式 = """
{
    "歌名": str,
    "歌词": list,  # 每一句歌词一项,放到列表里
    "简介": str,
    "标题": str,
    "评论": list,
}
"""

#llm2dict需要传入3个参数:
# 1.提问(str|list), 如果是list要符合[{"role": "user", "content": "提问"},...]
# 2.输出格式(str),
# 3.封装好的大模型API函数,可以使用LLM_API中的send_request函数,
#   也可以使用自己写的,但是要注意封装成: 函数(str问题) -> str回答 #只有一个参数,输入str格式的提问,输出str格式的回答
数据 = llm2dict(提问,返回格式,llm.send_request)
print("返回",数据)
```  

返回数据:
```python
{'歌名': '《心跳拼图》',
 '歌词': ['图书馆第三排的风掀动书页',
        '你睫毛投下的阴影 在我手背作祟',
        '橡皮擦蹭过草稿纸的轻响',
        '偷走了所有解题公式',
        '指纹在玻璃窗写下未完成的吻',
        '时针停摆在借阅卡签名的那秒',
        '我们都是散落的拼图碎片',
        '在安全距离外 碰撞成银河',
        '自动贩卖机吞下硬币的闷响',
        '映出你侧脸轮廓的金属回响',
        '奶茶杯沿的唇印半颗月亮',
        '被我藏进校服口袋发酵成糖'],
 '简介': "慵懒吉他与电子音效交织，讲述暗恋时笨拙又甜蜜的试探。用'指纹吻''时针停摆'等意象，勾勒出不敢完全靠近却渴望完整的心动模样。",
 '标题': '#爱情就像散落的拼图碎片 我在歌词里藏了三个心动瞬间 星星吻过眼睑的夜晚 愿你也拥有《心跳拼图》的勇气🌙✨',
 '评论': ["副歌那句'碰撞成银河'直接戳到泪点，想起高三教室窗外的星光",
        "verse里'吞下硬币的闷响'细节太戳我！就是我们初遇的自动贩卖机",
        '建议循环播放第五遍开始，电子音效像心跳漏拍的节奏，耳膜在恋爱',
        '最后奶茶杯沿的唇印细节太绝了！我直接把这句设为锁屏壁纸了',
        "在网易云听歌时旁边女生突然小声念'指纹在玻璃窗写下未完成的吻'，原来我们都在听这首"]}
```  

#### **llm2dict()** 核心函数，使模型输出结构化数据
```python
llm2dict(msg, data_structures, api)
```

**参数**  
- **msg** (str|list)： **提问内容**，如果是list要符合[{"role": "user", "content": "提问"},...]
- **data_structures** (str)： **期望返回的数据结构**，用str表示，例如：`"{'歌名': str, '歌词': list, '简介': str, '标题': str, '评论': list,}"`
- **api** (函数)： **封装好的大模型API函数**，可以使用LLM_API中的send_request，也可以使用自己写的，但是要注意封装成: 函数(str问题) -> str回答 | **入参只有一个：str格式的提问，输出str格式的回答**
-  **to_code_api** (函数)(可选)：**默认和api一样**，用于将回答转换为python代码的api模型函数
- **delay** (int)(可选)：**默认为0**，调用api的间隔时间，单位为秒
- **re_dict_prompt_template** (str)(可选)：用于替换生成代码的请求模板,文本中需要有2个{}{}，第一个{}会被替换为LLM第一交互的回答，第二个{}{}会被替换为期望返回的数据结构, `"原文本:{},格式:{}".format(LLM第一次交互的回答,数据结构要求data_structures)`


#### **LLM_API**（class） 大模型API接口
```python
llm=LLM_API(api_key, model_name, url)
llm.send_request("1+1等于多少?")
```
**参数** 
- **api_key** (str)：**大模型API的key**
- **model_name** (str)：**大模型API的模型名称**
- **url** (str)：**大模型API的完整请求url**

### 支持API平台
**硅基流动**
```python
    # 硅基流动 https://cloud.siliconflow.cn/models
    api_key = "填入api_key"
    url = "https://api.siliconflow.cn/v1/chat/completions"
    model_name = "Qwen/QwQ-32B"
    llm = LLM_API(api_key=api_key, model_name=model_name, url=url)
    print(llm.send_request("1+1等于多少?"))
```

**DeepSeek**
```python
    # DeepSeek https://platform.deepseek.com/usage
    api_key = "填入api_key" 
    url = "https://api.deepseek.com/v1/chat/completions"
    model_name = "deepseek-chat"
    llm = LLM_API(api_key=api_key, model_name=model_name, url=url)
    print(llm.send_request("1+1等于多少?"))
```

**KIMI**
```python
    # KIMI https://platform.moonshot.cn/docs/intro#%E6%96%87%E6%9C%AC%E7%94%9F%E6%88%90%E6%A8%A1%E5%9E%8B
    api_key = "填入api_key"
    url = "https://api.moonshot.cn/v1/chat/completions"
    model_name = "moonshot-v1-8k"
    llm = LLM_API(api_key=api_key, model_name=model_name, url=url)
    print(llm.send_request("1+1等于多少?"))
```

**阿里云百炼**
```python
    # 阿里云百炼 https://www.aliyun.com/product/bailian
    api_key = "填入api_key"
    url = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
    model_name = "qwq-32b"
    #阿里云需要stream=True
    llm = LLM_API(api_key=api_key, model_name=model_name, url=url, stream=True)
    print(llm.send_request("1+1等于多少?"))
```
**火山引擎**
```python
    # 豆包 https://www.volcengine.com/product/doubao
    api_key = "填入api_key"
    url = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
    model_name = "deepseek-r1-250120"
    llm = LLM_API(api_key=api_key, model_name=model_name, url=url)
    print(llm.send_request("1+1等于多少?"))
```