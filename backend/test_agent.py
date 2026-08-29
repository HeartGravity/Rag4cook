#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
厨房知识（Tips）抽取 Prompt 效果测试脚本
调用阿里云百炼模型，验证非标准化 md 文档的实体与安全警告抽取效果。
"""

import os
import json
import re
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from openai import OpenAI
from pathlib import Path

# 尝试导入 python-dotenv，如果未安装则使用备用文件解析方式
try:
    from dotenv import load_dotenv
    # 自动向上寻找根目录下的 .env 文件
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))
    load_dotenv()  # 当前目录兜底
except ImportError:
    pass

def load_env_manually():
    """手动读取 .env 文件（在未安装 python-dotenv 时的容错处理）"""
    possible_paths = [
        ".env",
        os.path.join("..", ".env"),
        os.path.join("..", "..", ".env")
    ]
    for path in possible_paths:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        k = k.strip()
                        v = v.strip().strip("'\"")
                        if k not in os.environ:
                            os.environ[k] = v
            break

load_env_manually()

# ============================
# 1. 数据结构定义 (TipInfo)
# ============================
@dataclass
class TipInfo:
    """厨房其他技巧信息"""
    name: str
    category: str
    description: str
    related_tools: List[str] = None
    related_ingredients: List[str] = None
    related_methods: List[str] = None
    safety_warnings: List[str] = None
    tags: List[str] = None

    def __post_init__(self):
        if self.related_tools is None:
            self.related_tools = []
        if self.related_ingredients is None:
            self.related_ingredients = []
        if self.related_methods is None:
            self.related_methods = []
        if self.safety_warnings is None:
            self.safety_warnings = []
        if self.tags is None:
            self.tags = []


# ============================
# 2. 百炼提取 Agent 实现
# ============================
class BailianTipExtractor:
    def __init__(self, api_key: str, model_name: str, base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"):
        self.api_key = api_key
        self.model_name = model_name
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )

    def extract_tip_info(self, markdown_content: str, file_path: str = "") -> Optional[TipInfo]:
        """使用大模型从 Markdown 文档中提取 TipInfo"""
        prompt = f"""
请分析以下无固定格式的厨房知识/技巧Markdown文档，提取结构化信息并以严格的JSON格式返回。

文件路径: {file_path}
文档内容：
{markdown_content}

## 文档特性说明
与标准菜谱不同，这是一篇厨房技巧、工具使用说明、厨房趣味知识或安全指南。文章结构自由，可能包含原理说明、操作步骤、注意事项和避坑指南。

## 提取规则
1. **知识点名称 (name)**：通常从一级标题提取（如"如何洗碗"、"糖色的炒制"、"微波炉"）。
2. **知识分类 (category)**：结合文件路径和内容判定（例如：烹饪技巧、工具说明、食材处理、清洁卫生、食品安全）。
3. **核心简介 (description)**：用一两句话高度概括这篇文档的核心目的或原理。
4. **关联实体提取**：
   - **工具 (related_tools)**：提取文中提到的实体器具（如：微波炉、海绵、空气炸锅、铁锅等）。
   - **食材 (related_ingredients)**：提取文中提到的具体食材或调料（如：大豆油、料酒、生肉、鸡蛋等）。
   - **方法 (related_methods)**：提取文中提到的烹饪或处理动作（如：焯水、腌制、油炸、热锅凉油等）。
5. **安全警告 (safety_warnings)**：提取所有涉及人身安全、健康隐患、损坏器具的警告（如致癌风险、烫伤危险、爆炸风险、涂层损坏等）。如果没有，则返回空列表。
6. **标签 (tags)**：生成3-4个有助于检索此文档的关键词。

请返回标准JSON格式（注意保持键名一致）：
{{
    "name": "知识点名称",
    "category": "知识分类",
    "description": "高度概括的核心简介",
    "related_tools": ["工具1", "工具2"],
    "related_ingredients": ["食材1", "食材2"],
    "related_methods": ["动作1", "动作2"],
    "safety_warnings": [
        "明确的安全隐患或强烈不建议的操作1",
        "明确的安全隐患或强烈不建议的操作2"
    ],
    "tags": ["标签1", "标签2", "标签3"]
}}

## 重要提示：
1. **防幻觉**：如果文中完全没有提到任何工具、食材或方法，对应字段请返回空列表 []，绝不允许自行捏造。
2. **安全优先**：留意文中带有“绝对不要”、“禁止”、“导致”、“风险”、“注意”等字眼的内容，将其归纳整理后放入 safety_warnings。
3. **实体纯净化**：在提取 tools, ingredients, methods 时，尽量提取纯名词或动词（如提取“不粘锅”而不是“使用不粘锅”）。
4. 必须只返回标准JSON字符串，不要包含多余的前缀或后缀解释。
"""

        messages = [
            {"role": "system", "content": "你是一个专业的烹饪与厨房知识图谱构建专家，擅长从非结构化文本中提取高质量的结构化实体与安全规范。"},
            {"role": "user", "content": prompt}
        ]

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=0.2,
                response_format={"type": "json_object"}
            )
            raw_text = response.choices[0].message.content.strip()

            # 清理 Markdown 代码块标记（如 ```json ... ```）
            if raw_text.startswith("```"):
                raw_text = re.sub(r"^```[a-zA-Z]*\n?", "", raw_text)
                raw_text = re.sub(r"\n?```$", "", raw_text)

            data = json.loads(raw_text)

            return TipInfo(
                name=data.get("name", ""),
                category=data.get("category", ""),
                description=data.get("description", ""),
                related_tools=data.get("related_tools", []),
                related_ingredients=data.get("related_ingredients", []),
                related_methods=data.get("related_methods", []),
                safety_warnings=data.get("safety_warnings", []),
                tags=data.get("tags", [])
            )

        except Exception as e:
            print(f"❌ 解析失败: {e}")
            return None


# ============================
# 3. 运行测试用例
# ============================
def main():
    # 读取环境变量
    api_key = os.getenv("BAILIAN_API_KEY") or os.getenv("DASHSCOPE_API_KEY") or os.getenv("API_KEY")
    model_name = os.getenv("MODEL_NAME") or os.getenv("BAILIAN_MODEL") or "qwen-plus"

    print("========================================")
    print(" 🛠️  厨房 Tips 提取 Prompt 测试")
    print("========================================")
    print(f"📌 模型名称: {model_name}")
    print(f"🔑 API Key : {api_key[:6]}******{api_key[-4:] if api_key else '未找到'}")
    
    if not api_key:
        print("❌ 错误: 未能在 .env 中找到 API KEY，请检查配置。")
        return

    extractor = BailianTipExtractor(api_key=api_key, model_name=model_name)

    sample_path = Path(__file__).parent.parent.parent / "HowToCook" / "tips" / "other" / "如何选择现在吃什么.md"
    sample_content = sample_path.read_text(encoding="utf-8")

    print(f"\n📄 正在提取文档: {sample_path} ...")
    tip_info = extractor.extract_tip_info(sample_content, file_path=sample_path)

    if tip_info:
        print("\n✅ 提取成功！结构化数据输出如下：")
        print("----------------------------------------")
        print(json.dumps(asdict(tip_info), ensure_ascii=False, indent=2))
        print("----------------------------------------")
        
        # 针对 Safety Warnings 进行针对性检查提示
        print(f"🛡️  提取到的安全警告数量: {len(tip_info.safety_warnings)} 条")
        for i, warning in enumerate(tip_info.safety_warnings, 1):
            print(f"   [{i}] {warning}")
    else:
        print("\n❌ 提取失败，请检查模型响应或网络。")

if __name__ == "__main__":
    main()