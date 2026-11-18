from llm_sdk import Small_LLM_Model as SLM 
import math
import random as rdm

TOP_NB = 5

def softmax(element: float, total: float) -> float:
    return math.exp(element)/total

def sum_of_exp(elements: list[float]) -> float:
    elementsExp = [math.exp(e) for e in elements]
    return sum(elementsExp)

def softmax_for_all(logits: list[float]) -> list[float]:
    sums = sum_of_exp(logits)
    return [softmax(i, sums) for i in logits]

def get_topi(logits: list[float]) -> tuple[list[int], list[float]]:
    top = [-math.inf] * TOP_NB 
    topi = [-1] * TOP_NB 
    si = 0 # Small Index
    for index, value in enumerate(logits) :
        if top[si] < value :
            top[si] = value
            topi[si] = index
            min = math.inf
            for i, val in enumerate(top):
                if val < min :
                    min = val
                    si = i
    #print(f"{softmax_for_all(top)}, sum :{sum(softmax_for_all(top))}")
    return (topi, top)

def get_magic_number(probaList: list[float]) -> int:
    n = rdm.random()
    pre = 0
    for i, val in enumerate(probaList):
        pre += val
        if pre < n:
            return i
    return -1


qwen = SLM()
tensor = qwen.encode("Once upon")
tensor = tensor.tolist()
# print(qwen.decode(tensor))
tensor = tensor[0]
# print(qwen.decode(tensor))
# print(tensor)

# print(len(logits))

txt = ""
for t in range(200):

    logits = qwen.get_logits_from_input_ids(tensor)
    topi, top = get_topi(logits)
    txt = qwen.decode(tensor)
    tensor.append(topi[get_magic_number(softmax_for_all(top))])

print(txt)

#print (f"max= {max}, max I = {maxi}, plus = {plus}")
# print(logits)

# vocab_path = qwen.get_path_to_vocab_file()
# merges_path = qwen.get_path_to_merges_file()
# tokenizer_path = qwen.get_path_to_tokenizer_file()
# print(f"vocab : '{vocab_path}', merges : '{merges_path}', tomkenizer : '{tokenizer_path}'")
