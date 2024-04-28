import torch
from transformers import DistilBertForQuestionAnswering, DistilBertTokenizer

# 加载经过蒸馏的 DistilBERT 模型和 tokenizer
model_path = "../pre_models/distilbert"
model = DistilBertForQuestionAnswering.from_pretrained(model_path)
tokenizer = DistilBertTokenizer.from_pretrained(model_path)

def get_answer(question, context):
    # 对问题和上下文进行编码
    inputs = tokenizer(question, context, return_tensors='pt')
    
    # 进行问答预测
    outputs = model(**inputs)
    start_scores = outputs.start_logits
    end_scores = outputs.end_logits

    # 打印输出类型和值，以便调试
    print("start_scores type:", type(start_scores))
    print("end_scores type:", type(end_scores))
    print("start_scores:", start_scores)
    print("end_scores:", end_scores)
    
    # 确保 start_scores 和 end_scores 是张量类型
    start_scores = start_scores.squeeze(0)
    end_scores = end_scores.squeeze(0)
    
    # 获取最有可能的答案的索引
    answer_start = torch.argmax(start_scores)
    answer_end = torch.argmax(end_scores) + 1
    
    # 将答案从 token 转换为字符串
    answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(inputs['input_ids'][0][answer_start:answer_end]))
    
    return answer

# 示例问题和上下文
question = "Who invented the lightbulb?"
context = "The lightbulb was invented by Thomas Edison."

# 获取答案
answer = get_answer(question, context)
print("Answer:", answer)

