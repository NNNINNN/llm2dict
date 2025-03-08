from .execute import exec_code
from .prompt import dict_prompt_template
import time
from .api import LLM_API, add_user, add_system, add_assistant


def llm2dict(msg: list | str,
             data_structures: str,
             api,
             to_code_api=None,
             delay: int = None,
             re_dict_prompt_template=None) -> dict | list | bool:
    """
    msg:发送给大语言模型的消息 [{"role": "system", "content": ""},{"role": "user", "content": ""}]
    data_structures:希望返回的格式
    api:封装好的大语言模型api接口
    to_code_api:使用另外一个封装好的大语言模型api接口
    delay:2次请求api间的休眠
    re_dict_prompt_template: 自定义生成代码请求的模板, "原文本:{},格式:{}".format(LLM第一次交互的回答,数据结构要求data_structures)
    ------en
    msg: The message sent to the large language model. Format: [{"role": "system", "content": ""}, {"role": "user", "content": ""}]
    data_structures: The desired format of the returned data.
    api: The encapsulated API interface for the large language model.
    to_code_api: An optional encapsulated API interface for another large language model (used for code generation).
    delay: The sleep time (in seconds) between two API requests.
    re_dict_prompt_template: A custom template for generating the code request. Format: "Original text: {}, Format: {}".format(LLM's first response, data_structures requirement).
    ------
    :return: dict|bool
    """
    resp = api(msg)
    if not resp: return False
    if delay: time.sleep(delay)
    if re_dict_prompt_template:
        code_Request = re_dict_prompt_template.format(resp, data_structures)
    else:
        code_Request = dict_prompt_template.format(resp, data_structures)
    print(code_Request)
    if to_code_api:
        code = to_code_api(code_Request)
    else:
        code = api(code_Request)
    print(code)
    data = exec_code(code)
    if data:
        return data
    else:
        return False
