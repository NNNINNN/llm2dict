dict_prompt_template = """
#按照需求补充python代码，根据文本提取出数据，写成python代码。
思考把要把哪些内容写在数据结构中，如果文本中没有数据结构中想要的数据，需要使用False代替。
最后，要检查返回的python代码是否正确。

#原文本:
'''{}'''

---
#提取的数据要求和数据结构：
'''{}'''

---
#返回python代码
##如果需要返回的是dict:
```python
data = {{
    #在此处补充
}}
```
##如果需要返回的是list:
```python
data = [
    #在此处补充
]
```
"""