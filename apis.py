import re

from openai import OpenAI

client = OpenAI(api_key="sk-fd29d704f45e4675bf9df4a70034654d", base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",)


def analyze_essay(text):
    """

    :param text:
    :return:
    """
    rounds_result = []
    #scores = []  # 存储各模块评分

    # 打开文件以写入内容
    with open("output.txt", "a", encoding="utf-8") as file:
        # Round 1
        """       
        messages = [{"role": "user", "content": f"请阅读以下作文内容：{text}"}]
        response = client.chat.completions.create(
            model="qwen-plus",
            messages=messages
        )

        messages.append(response.choices[0].message)
        print(f"Messages Round 1: {response.choices[0].message.content}")
        """
        # Round 2
        messages=[{"role": "user", "content": f"""请分析以下文本{text}，是否有错别字，如果没有则输出无，如果有错别字则提供以下信息，注意不要错判误判：
        - 位置：错别字在文本中的具体位置（例如：第几段第几行）
        - 类型：错别字的类型（例如：拼写错误、用词不当，谐音字词，混淆音字词，字词顺序颠倒，字词补全，形似字错误，中文拼音全拼，中文拼音缩写，语法错误、标点错误）
        - 修改前：错别字的具体内容
        - 修改后：正确的字词
        - 个数：错别字的总个数
        -总结每种错误类型的个数
        -- 综合评价打分：根据错别字的数量和种类，给出百分制评价打分（满分100分） ,输出格式：错别字评分：XX分，注意不要输出其他内容（包括理由）"""}]
        response = client.chat.completions.create(
            model="qwen-max",
            messages=messages
        )

        messages.append(response.choices[0].message)
        print(f"Messages Round 2: {response.choices[0].message.content}")
        rounds_result.append(f"## 错别字分析\n\n{response.choices[0].message.content}\n\n")

        # Round 3
        messages.append({"role": "user", "content": """请分析上述作文的词汇丰富度，并提供以下信息：
        - 每种词汇的个数：名词、动词、形容词、副词、介词、连词、代词的个数（不需要具体列举，只需要个数）
        - 综合评价打分：根据词汇的多样性和使用情况，给出综合评价打分（满分100分），输出格式：词汇丰富度评分：XX分，注意不要输出其他内容"""})
        response = client.chat.completions.create(
            model="qwen-max",
            messages=messages
        )

        messages.append(response.choices[0].message)
        print(f"Messages Round 3: {response.choices[0].message.content}")
        rounds_result.append(f"## 词汇丰富度分析\n\n{response.choices[0].message.content}\n\n")

        # Round 4
        messages.append({"role": "user", "content": """
        对上述作文的篇章结构进行划分和分析和列举，看看哪些语段符合所给的篇章结构类型，输出下面的任务：
        - 成分标签标注：根据原文内容，标注出各成分的具体标签类型（类型：文章开篇：设置悬念、开门见山、总领全文、概括介绍、背景介绍、对话开篇、故事开篇、俗语开篇、歌词开篇、诗歌开篇、题记开篇
        人物描写：人物肖像描写、人物行动描写、人物语言描写、人物心理描写
        事件描写：事件时间、事件地点、事件人物、事件起因、事件经过、事件结果
        总结结尾：首尾照应、文题照应、前后照应、点题、主题升华、概览全文、引发深思
        其他：过渡、转折、顺承、承上启下、过渡段、假设、递进、并列、因果、并列、铺垫），确保标注精准且完整。
        - 简要分析：针对每个标注的标签类型进行简要分析，说明该部分在文章中的作用和效果。
        - 综合评价打分：基于以上标注和分析，从文章结构、内容丰富性、逻辑连贯性和情感表达等方面进行综合评估，给出最终评分（满分100）输出格式：篇章结构评分：XX分，注意不要输出其他内容（包括理由）"""})
        response = client.chat.completions.create(
            model="qwen-max",
            messages=messages
        )

        messages.append(response.choices[0].message)
        print(f"Messages Round 4: {response.choices[0].message.content}")
        rounds_result.append(f"## 篇章结构分析\n\n{response.choices[0].message.content}\n\n")

        # Round 5
        messages.append({"role": "user", "content": """请分析上述作文的内容情感，输出以下任务：
        - 文章类型：文本的类型（例如：叙事文、议论文、说明文,想象文，写人文，读后感）
        - 主要内容：文本的主要故事或内容概述
        - 主旨情感：文本的主旨情感
        - 综合评价打分：根据文本的内容和情感丰富性，给出综合评价打分（满分100分）输出格式：内容情感评分：XX分，注意不要输出其他内容（包括理由）。 """})
        response = client.chat.completions.create(
            model="qwen-max",
            messages=messages
        )

        messages.append(response.choices[0].message)
        print(f"Messages Round 5: {response.choices[0].message.content}")
        rounds_result.append(f"## 内容情感分析\n\n{response.choices[0].message.content}\n\n")

        # Round 6
        messages.append({"role": "user", "content": """请分析上述作文中的修辞和描写手法手法，并提供以下信息：
        1. 修辞和描写手法分析：
        - 位置：修辞和描写手法在文本中的具体位置（例如：第几段第几行）
        - 文本内容：出现修辞和描写手法的具体句子或段落
        - 类型：修辞和描写手法的具体类型（例如：比喻、拟人、排比、夸张、引用，心理描写，语言描写等）
        - 分析：对该修辞和描写手法的作用进行简要分析，例如如何增强表达效果或情感张力
        
        2. 各类修辞和描写手法的数量统计：（没有的不用输出）
      
        3. 综合评分：
        - 根据修辞和描写手法的多样性、丰富性和适用性，对修辞运用进行百分制评分（满分100分），输出格式：修辞和描写手法评分：XX分，注意不要输出其他内容（包括理由）

        4. 简单评价：
        - 对修辞和描写手法的整体运用进行简要评价，例如：是否与文章主题契合，是否有效提升了语言表达的美感或感染力。"""})

        response = client.chat.completions.create(
            model="qwen-max",
            messages=messages
        )

        messages.append(response.choices[0].message)
        print(f"Messages Round 6: {response.choices[0].message.content}")
        rounds_result.append(f"## 修辞手法分析\n\n{response.choices[0].message.content}\n\n")

        # Round 7
        messages.append({"role": "user", "content": """请根据以上分析结果，提供该篇作文的以下信息：
        - 综合评分：根据错别字、词汇丰富度、篇章结构、内容情感、修辞手法的综合表现，分别给出百分制评分，给出综合评分（满分100分）
        - 批改建议：针对文本的不足之处，提出具体的改进建议
        - 知识点讲解：建议中的涉及到的相关知识点解释（3-5个）
        - 修改后的作文：根据以上分析和建议，给出修改后的作文版本，要求内容不变，语法正确，逻辑清晰，表达流畅。"""})
        response = client.chat.completions.create(
            model="qwen-max",
            messages=messages
        )

        messages.append(response.choices[0].message)
        print(f"Messages Round 7: {response.choices[0].message.content}")
        comprehensive_score = f"## 综合评分与建议\n\n{response.choices[0].message.content}\n\n"
        # 将综合评分与建议放在最前面输出
        final_result = [comprehensive_score] + rounds_result
        # 提取分数
        all_text = "\n".join(final_result)
        scores = extract_scores(all_text)

        file.write(all_text)
        return final_result, scores




def extract_scores(text):
   
    # 使用正则表达式匹配分数
    score_labels = ["错别字", "词汇丰富度", "篇章结构", "内容情感", "修辞和描写手法"]
    scores = []

    for label in score_labels:
        # 匹配 "错别字评分：85" 或 "错别字：85分" 等格式
        match = re.search(rf"{label}.*?(\d{{1,3}})(?:\s*分|\s*分数)?", text)
        if match:
            scores.append(int(match.group(1)))
        else:
            scores.append(0)  # 如果未匹配到，默认分数为 0

    return scores


# 本地调试
if __name__ == '__main__':
    text = "请输入测试作文内容..."
    result, scores = analyze_essay(text)
    print("Detailed Results:", result)
    print("Scores:", scores)




