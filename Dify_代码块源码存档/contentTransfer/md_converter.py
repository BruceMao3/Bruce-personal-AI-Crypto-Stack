import argparse
import requests
from pathlib import Path
import importlib.util
import sys
import os

class MarkdownConverter:
    """读取文件并调用转换器进行处理"""
    
    def __init__(self, server_url="http://localhost:3000"):
        self.server_url = server_url.rstrip('/')  # 确保URL末尾没有斜杠
        self.converters_dir = Path(__file__).parent / "converters"  # 转换器目录
        self.converters = {}
        self._load_converters()
    
    def _load_converters(self):
        """自动加载转换器目录下的所有转换器"""
        if not self.converters_dir.exists():
            print(f"⚠️ 转换器目录不存在: {self.converters_dir}")
            print("创建目录...")
            self.converters_dir.mkdir(parents=True, exist_ok=True)
            return
        
        # 预期的转换器文件名
        expected_converters = {
            "vx": "VX_converter.py",
            "substack": "substack_converter.py",
            "twitter": "X_converter.py",
            "bilibili": "bilibili_converter.py"
        }
        
        # 加载每个转换器
        for platform, filename in expected_converters.items():
            converter_path = self.converters_dir / filename
            if converter_path.exists():
                if self._load_converter(platform, converter_path):
                    print(f"✅ 已加载 {platform} 转换器")
            else:
                print(f"⚠️ 未找到 {platform} 转换器: {converter_path}")
    
    def _load_converter(self, platform, converter_path):
        """加载指定的转换器模块"""
        try:
            # 动态加载模块
            spec = importlib.util.spec_from_file_location(platform, converter_path)
            if not spec:
                return False
                
            module = importlib.util.module_from_spec(spec)
            sys.modules[platform] = module
            spec.loader.exec_module(module)
            
            # 检查模块是否有convert函数
            if hasattr(module, 'convert'):
                self.converters[platform] = module.convert
                return True
            return False
                
        except Exception as e:
            print(f"❌ 加载 {platform} 转换器时出错: {e}")
            return False
    
    def process_file(self, file_path):
        """处理单个文件"""
        file_path = Path(file_path)
        if not file_path.exists():
            print(f"❌ 错误: 文件不存在 - {file_path}")
            return False
        
        if len(self.converters) == 0:
            print("❌ 错误: 没有可用的转换器")
            return False
        
        try:
            # 读取Markdown文件
            with open(file_path, 'r', encoding='utf-8') as f:
                markdown_content = f.read()
            
            title = file_path.stem  # 使用文件名作为标题
            
            # 对每个平台进行转换并发送
            for platform, converter in self.converters.items():
                try:
                    # 调用转换器
                    html_content = converter(markdown_content)
                    
                    # 准备请求数据
                    payload = {
                        "platform": platform,
                        "title": title,
                        "content": html_content
                    }
                    
                    # 发送到服务器 - 使用正确的API端点
                    try:
                        api_endpoint = f"{self.server_url}/api/card"  # 使用正确的API端点
                        
                        response = requests.post(
                            api_endpoint,
                            json=payload,
                            proxies={'http': None, 'https': None}  # 禁用代理
                        )
                        if response.status_code == 200:
                            print(f"✅ {platform}: 转换成功并已发送")
                        else:
                            print(f"❌ {platform}: 发送失败 - 状态码 {response.status_code}")
                    except requests.exceptions.RequestException as e:
                        print(f"❌ {platform}: 发送失败 - {e}")
                        
                except Exception as e:
                    print(f"❌ {platform}: 转换失败 - {e}")
            
            return True
            
        except Exception as e:
            print(f"❌ 处理文件出错: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description='Markdown多平台转换器')
    parser.add_argument('file', help='Markdown文件路径')
    parser.add_argument('--server', default="http://localhost:3000", help='服务器URL')
    
    args = parser.parse_args()
    
    converter = MarkdownConverter(server_url=args.server)
    converter.process_file(args.file)

if __name__ == "__main__":
    main()
