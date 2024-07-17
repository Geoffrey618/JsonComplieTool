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

        self.data = self.load_and_update_json('Task2TrainingSet.json', 'images')
        self.current_index = 0
        self.current_question_index = 0

        self.create_widgets()
        self.display_image()

    def load_and_update_json(self, json_file, image_dir):
        # Load existing JSON data
        if os.path.exists(json_file):
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = []

        # Get list of existing images in JSON
        existing_images = {entry['image'][0] for entry in data}

        # Check for new images in the directory
        all_images = {os.path.join(image_dir, f) for f in os.listdir(image_dir) if f.endswith('.jpg')}
        new_images = all_images - existing_images

        # Add new images to JSON data
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

        # Save updated JSON data
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        return data

    def save_json(self):
        with open('Task2TrainingSet.json', 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def create_widgets(self):
        self.image_label = tk.Label(self.master)
        self.image_label.pack()

        self.progress_label = tk.Label(self.master, text="", font=('Arial', 12, 'bold'))
        self.progress_label.pack()

        self.question_label = tk.Label(self.master, text="User：进行提问", font=('Arial', 12, 'bold'))
        self.question_label.pack()

        self.question_text = tk.Text(self.master, height=5, font=('Arial', 12))
        self.question_text.pack()

        self.answer_label = tk.Label(self.master, text="Assistant：进行回答", font=('Arial', 12, 'bold'))
        self.answer_label.pack()

        self.answer_text = tk.Text(self.master, height=5, font=('Arial', 12))
        self.answer_text.pack()

        button_frame = tk.Frame(self.master)
        button_frame.pack(pady=10)

        button_config = {
            "font": ('Arial', 12, 'bold'),
            "height": 2,
            "width": 15,
        }

        self.save_button = tk.Button(button_frame, text="保存修改", command=self.save_entry, bg='lightblue', fg='black', **button_config)
        self.save_button.grid(row=0, column=0, padx=5)

        self.prev_button = tk.Button(button_frame, text="上一张", command=self.prev_image, bg='lightgreen', fg='black', **button_config)
        self.prev_button.grid(row=0, column=1, padx=5)

        self.next_button = tk.Button(button_frame, text="下一张", command=self.next_image, bg='lightgreen', fg='black', **button_config)
        self.next_button.grid(row=0, column=2, padx=5)

        self.exit_button = tk.Button(button_frame, text="退出", command=self.exit_tool, bg='red', fg='white', **button_config)
        self.exit_button.grid(row=0, column=3, padx=5)

    def display_image(self):
        if self.data:
            entry = self.data[self.current_index]
            image_path = entry['image'][0]
            img = Image.open(image_path)
            img = img.resize((400, 300), Image.Resampling.LANCZOS)
            img = ImageTk.PhotoImage(img)
            self.image_label.config(image=img)
            self.image_label.image = img

            # 显示当前问题和答案
            self.question_text.delete(1.0, tk.END)
            self.answer_text.delete(1.0, tk.END)
            self.question_text.insert(tk.END, entry['messages'][self.current_question_index * 2]['content'])
            self.answer_text.insert(tk.END, entry['messages'][self.current_question_index * 2 + 1]['content'])

            # 更新进度标签
            self.progress_label.config(text=f"正在处理图片 {self.current_index + 1} / {len(self.data)}")

    def save_entry(self):
        if self.data:
            entry = self.data[self.current_index]
            entry['messages'][self.current_question_index * 2]['content'] = self.question_text.get(1.0, tk.END).strip()
            entry['messages'][self.current_question_index * 2 + 1]['content'] = self.answer_text.get(1.0, tk.END).strip()
            self.save_json()
            # messagebox.showinfo("Info", "数据已保存")

            # 跳转到下一个问题
            if self.current_question_index < 2:
                self.current_question_index += 1
            else:
                self.current_question_index = 0
                if self.current_index < len(self.data) - 1:
                    self.current_index += 1
                else:
                    self.current_index = 0

            self.display_image()

    def prev_image(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.current_question_index = 0
            self.display_image()

    def next_image(self):

        if self.current_index < len(self.data) - 1:
            self.current_index += 1
            self.current_question_index = 0
            self.display_image()

    def exit_tool(self):
        self.save_json()
        self.master.quit()

if __name__ == "__main__":
    # Ensure the JSON file is generated and updated with new images
    root = tk.Tk()
    app = AnnotationTool(root)
    root.mainloop()