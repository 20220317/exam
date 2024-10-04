import json
import re
import time


# 加载JSON文件
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


# 解析并提取 \n\n 之间的内容
def extract_questions(input_text):
    # 分割问答对（每个问答对之间是 \n\n）
    pairs = input_text.split("\n\n")

    # 存储提取后的结果
    question_answer_pairs = []

    for pair in pairs:
        # 匹配问句和答案部分，正则表达式匹配所有字符到最后的 "No" 或 "Yes"
        match = re.search(r'(.*?No or Yes\?)\s*(No|Yes)\s*$', pair, re.DOTALL)

        if match:
            question = match.group(1).strip()  # 提取问题
            answer = match.group(2).strip()  # 提取答案

            # 将问答对保存为字典
            question_answer_pairs.append({
                "Question": question,
                "Answer": answer
            })

    return question_answer_pairs


# 从JSON文件中的input部分提取问题和答案，并加上数字ID
def extract_questions_with_id_from_json_file(json_file_path):
    data = load_json(json_file_path)
    all_question_answer_pairs = []

    # 提取每个item中的input部分
    for idx, item in enumerate(data, start=1):
        input_text = item.get('input', '')
        question_answer_pairs = extract_questions(input_text)

        # 为每个问答对添加一个数字ID
        for pair in question_answer_pairs:
            pair_with_id = {
                "id": idx,  # 添加数字ID
                "Question": pair['Question'],
                "Answer": pair['Answer']
            }
            all_question_answer_pairs.append(pair_with_id)

    return all_question_answer_pairs


# 保存提取的问答对到JSON文件
def save_to_json_with_id(data, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


# 主程序，统计问答对总数和记录处理时间
def main(input_file_path, output_file_path):
    start_time = time.time()  # 记录开始时间

    # 提取问答对并保存
    extracted_data_with_id = extract_questions_with_id_from_json_file(input_file_path)
    save_to_json_with_id(extracted_data_with_id, output_file_path)

    end_time = time.time()  # 记录结束时间

    # 统计问答对总数
    total_questions = len(extracted_data_with_id)

    # 计算处理所花费的时间
    elapsed_time = end_time - start_time

    print(f"提取的问答对已保存到: {output_file_path}")
    print(f"从数据集中提取的问答对总数: {total_questions}")
    print(f"数据清理和转换过程所花费的时间: {elapsed_time:.2f} 秒")


# 文件路径
input_file_path = 'test.json'  # 输入文件路径
output_file_path = 'adjust.json'  # 输出文件路径

# 执行主程序
main(input_file_path, output_file_path)
