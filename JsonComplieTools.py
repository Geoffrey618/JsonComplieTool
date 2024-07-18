import os
import json
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random

# 问题模板
image_recognition_questions = [
    "图中包含哪几道菜肴？都是什么菜肴？",
    "图中包含哪些菜肴？",
    "图中显示了哪些食物？",
    "请识别图中的菜肴。",
    "这张图片里有几道菜？",
    "能告诉我图中有哪些菜吗？",
    "图中的菜品有哪些？",
    "请列出图中所有的菜肴。",
    "图中有哪些种类的菜肴？",
    "能识别出这张图中的菜吗？",
    "这张图里有几种菜？"
]

weight_recognition_questions = [
    "图中的菜肴分别重多少克？",
    "图中的菜肴分别有多重？",
    "每道菜的重量是多少？",
    "这些菜的重量分别是多少克？",
    "请告诉我图中每道菜的重量。",
    "图中的菜肴重量各是多少？",
    "每道菜分别有多重？",
    "能估算图中每道菜的重量吗？",
    "这张图里的菜各重多少？",
    "请问这些菜的重量是多少？",
    "能计算出图中各道菜的重量吗？"
]

nutritional_value_questions = [
    "图中的菜肴有什么营养价值？",
    "每道菜的营养成分是什么？",
    "这些菜肴的营养价值如何？",
    "请分析图中菜肴的营养成分。",
    "这些菜分别有哪些营养素？",
    "图中菜肴的营养价值是什么？",
    "请告诉我图中每道菜的营养成分。",
    "能分析图中菜的营养价值吗？",
    "这些菜的营养成分各是什么？",
    "图中的菜肴有哪些营养成分？"
]


class AnnotationTool:
    def __init__(self, master):
        self.master = master
        self.master.title("JSON标注工具")

        # 加载并更新JSON数据
        self.data = self.load_and_update_json('Task2TrainingSet.json', 'images')
        self.current_index = 0
        self.current_message_index = 0
        self.mode = "全部查看"  # 默认模式为全部查看

        # 创建界面控件
        self.create_widgets()
        # 显示当前图片和问题
        self.display_image()

    def load_and_update_json(self, json_file, image_dir):
        # 加载现有的JSON数据
        if os.path.exists(json_file):
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = []

        # 获取JSON中已有的图片列表
        existing_images = {entry['image'][0] for entry in data}

        # 检查目录中的新图片
        all_images = {os.path.join(image_dir, f) for f in os.listdir(image_dir) if f.endswith('.jpg')}
        new_images = all_images - existing_images

        # 将新图片添加到JSON数据中
        for image in new_images:
            questions = [
                random.choice(image_recognition_questions),
                random.choice(weight_recognition_questions),
                random.choice(nutritional_value_questions)
            ]
            entry = {
                "image": [image],
                "messages": [
                    {"role": "user", "content": questions[0]},
                    {"role": "assistant", "content": ""},
                    {"role": "user", "content": questions[1]},
                    {"role": "assistant", "content": ""},
                    {"role": "user", "content": questions[2]},
                    {"role": "assistant", "content": ""}
                ]
            }
            data.append(entry)

        # 保存更新后的JSON数据
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        return data

    def save_json(self):
        # 保存JSON数据
        with open('Task2TrainingSet.json', 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def create_widgets(self):
        # 图片路径标签
        self.image_path_label = tk.Label(self.master, text="", font=('Arial', 10, 'italic'))
        self.image_path_label.pack(pady=5)

        # 图片标签
        self.image_label = tk.Label(self.master)
        self.image_label.pack(pady=5)

        # 进度框架
        progress_frame = tk.Frame(self.master)
        progress_frame.pack(pady=5)

        # 当前进度标签
        self.progress_label = tk.Label(progress_frame, text="", font=('Arial', 12, 'bold'))
        self.progress_label.pack(side=tk.LEFT, padx=5)

        # 跳转至第n张图片的输入框
        self.progress_entry = tk.Entry(progress_frame, font=('Arial', 12, 'bold'), width=7, justify='center')
        self.progress_entry.pack(side=tk.LEFT, padx=5)

        # 跳转按钮
        self.jump_button = tk.Button(progress_frame, text="跳转", bg='lightpink', command=self.jump_to_image,
                                     font=('Arial', 12, 'bold'))
        self.jump_button.pack(side=tk.LEFT, padx=5)

        # 模式选择框架
        mode_frame = tk.Frame(self.master)
        mode_frame.pack(pady=10)

        # 模式选择标签
        self.mode_label = tk.Label(mode_frame, text="选择模式:", font=('Arial', 12, 'bold'))
        self.mode_label.pack(side=tk.LEFT, padx=5)

        # 模式选择按钮配置
        button_config = {
            "font": ('Arial', 10, 'bold'),
            "height": 2,
            "width": 12,
            "bg": 'lightyellow',
            "fg": 'black'
        }

        # 模式选择按钮
        self.view_all_button = tk.Button(mode_frame, text="全部查看", command=lambda: self.change_mode("全部查看"), **button_config)
        self.view_all_button.pack(side=tk.LEFT, padx=5)
        self.count_button = tk.Button(mode_frame, text="计数", command=lambda: self.change_mode("计数"), **button_config)
        self.count_button.pack(side=tk.LEFT, padx=5)
        self.weight_button = tk.Button(mode_frame, text="计重", command=lambda: self.change_mode("计重"), **button_config)
        self.weight_button.pack(side=tk.LEFT, padx=5)
        self.nutrition_button = tk.Button(mode_frame, text="营养评估", command=lambda: self.change_mode("营养评估"), **button_config)
        self.nutrition_button.pack(side=tk.LEFT, padx=5)

        # 问题标签
        self.question_label = tk.Label(self.master, text="Role: User", font=('Arial', 12, 'bold'))
        self.question_label.pack(pady=5)

        # 问题文本框
        self.question_text = tk.Text(self.master, height=5, font=('Arial', 12))
        self.question_text.pack(padx=5, pady=5)

        # 回答标签
        self.answer_label = tk.Label(self.master, text="Role: Assistant", font=('Arial', 12, 'bold'))
        self.answer_label.pack(pady=5)

        # 回答文本框
        self.answer_text = tk.Text(self.master, height=5, font=('Arial', 12))
        self.answer_text.pack(padx=30, pady=5)

        # 按钮框架
        button_frame = tk.Frame(self.master)
        button_frame.pack(pady=10)

        # 按钮配置
        button_config = {
            "font": ('Arial', 12, 'bold'),
            "height": 2,
            "width": 15,
        }

        # 保存按钮
        self.save_button = tk.Button(button_frame, text="保存修改", command=self.save_entry, bg='lightblue', fg='black',
                                     **button_config)
        self.save_button.grid(row=0, column=0, padx=5)

        # 上一张按钮
        self.prev_button = tk.Button(button_frame, text="上一张", command=self.prev_image, bg='lightgreen', fg='black',
                                     **button_config)
        self.prev_button.grid(row=0, column=1, padx=5)

        # 下一张按钮
        self.next_button = tk.Button(button_frame, text="下一张", command=self.next_image, bg='lightgreen', fg='black',
                                     **button_config)
        self.next_button.grid(row=0, column=2, padx=5)

        # 退出按钮
        self.exit_button = tk.Button(button_frame, text="退出", command=self.exit_tool, bg='red', fg='white',
                                     **button_config)
        self.exit_button.grid(row=0, column=3, padx=5)

    def change_mode(self, mode):
        self.mode = mode
        self.current_message_index = 0
        self.display_image()

    def display_image(self):
        # 显示当前图片和问题
        if self.data:
            entry = self.data[self.current_index]
            image_path = entry['image'][0]
            img = Image.open(image_path)
            img = img.resize((400, 300), Image.Resampling.LANCZOS)
            img = ImageTk.PhotoImage(img)
            self.image_label.config(image=img)
            self.image_label.image = img

            # 更新图片路径标签
            self.image_path_label.config(text=f"当前文件：{image_path}", font=('Arial', 12, 'bold'))

            # 显示当前问题和答案
            self.question_text.delete(1.0, tk.END)
            self.answer_text.delete(1.0, tk.END)

            if self.mode == "全部查看":
                message_index = self.current_message_index * 2
                question_text = entry['messages'][message_index]['content']
                answer_text = entry['messages'][message_index + 1]['content']
            elif self.mode == "计数":
                question_text = entry['messages'][0]['content']
                answer_text = entry['messages'][1]['content']
            elif self.mode == "计重":
                question_text = entry['messages'][2]['content']
                answer_text = entry['messages'][3]['content']
            elif self.mode == "营养评估":
                question_text = entry['messages'][4]['content']
                answer_text = entry['messages'][5]['content']

            self.question_text.insert(tk.END, question_text)
            self.answer_text.insert(tk.END, answer_text)

            # 更新进度标签
            self.progress_label.config(text=f"正在处理图片 {self.current_index + 1} / {len(self.data)}")

    def save_entry(self):
        # 保存当前条目的修改
        if self.data:
            entry = self.data[self.current_index]
            if self.mode == "全部查看":
                message_index = self.current_message_index * 2
                entry['messages'][message_index]['content'] = self.question_text.get(1.0, tk.END).strip()
                entry['messages'][message_index + 1]['content'] = self.answer_text.get(1.0, tk.END).strip()
            elif self.mode == "计数":
                entry['messages'][0]['content'] = self.question_text.get(1.0, tk.END).strip()
                entry['messages'][1]['content'] = self.answer_text.get(1.0, tk.END).strip()
            elif self.mode == "计重":
                entry['messages'][2]['content'] = self.question_text.get(1.0, tk.END).strip()
                entry['messages'][3]['content'] = self.answer_text.get(1.0, tk.END).strip()
            elif self.mode == "营养评估":
                entry['messages'][4]['content'] = self.question_text.get(1.0, tk.END).strip()
                entry['messages'][5]['content'] = self.answer_text.get(1.0, tk.END).strip()
            self.save_json()

            # 跳转到下一个问题
            if self.mode == "全部查看":
                if self.current_message_index < 2:
                    self.current_message_index += 1
                else:
                    self.current_message_index = 0
                    if self.current_index < len(self.data) - 1:
                        self.current_index += 1
                    else:
                        self.current_index = 0
            else:
                if self.current_index < len(self.data) - 1:
                    self.current_index += 1
                else:
                    self.current_index = 0

            self.display_image()

    def prev_image(self):
        # 显示上一张图片
        if self.current_index > 0:
            self.current_index -= 1
            self.current_message_index = 0
            self.display_image()

    def next_image(self):
        # 显示下一张图片
        if self.current_index < len(self.data) - 1:
            self.current_index += 1
            self.current_message_index = 0
            self.display_image()

    def jump_to_image(self):
        # 跳转至指定图片
        try:
            index = int(self.progress_entry.get()) - 1
            if 0 <= index < len(self.data):
                self.current_index = index
                self.current_message_index = 0
                self.display_image()
            else:
                messagebox.showwarning("警告", "输入的数字超出范围！")
        except ValueError:
            messagebox.showwarning("警告", "请输入有效的数字！")

    def exit_tool(self):
        # 退出工具并保存数据
        self.save_json()
        self.master.quit()


if __name__ == "__main__":
    # 确保生成并更新JSON文件
    root = tk.Tk()
    app = AnnotationTool(root)
    root.mainloop()