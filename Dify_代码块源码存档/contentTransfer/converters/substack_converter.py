# substack_converter.py
import markdown
from bs4 import BeautifulSoup

def convert(markdown_text):
    """将Markdown转换为Substack平台样式的内联HTML"""
    
    # 使用python-markdown转换为HTML
    html = markdown.markdown(
        markdown_text,
        extensions=['extra', 'codehilite', 'fenced_code', 'tables']
    )
    
    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html, 'html.parser')
    
    # Substack平台的样式
    styles = {
        'section': {
            "font-family": "Charter, Georgia, serif",
            "word-break": "break-word",
            "line-height": "1.6",
            "font-weight": "400",
            "font-size": "18px",
            "color": "#222222",
            "max-width": "700px",
            "margin": "0 auto"
        },
        'p': {
            "margin-top": "20px",
            "margin-bottom": "20px",
            "line-height": "1.6"
        },
        'h1': {
            "font-size": "32px", 
            "font-weight": "700",
            "margin-top": "40px",
            "margin-bottom": "20px",
            "line-height": "1.2"
        },
        'h2': {
            "font-size": "24px",
            "font-weight": "700",
            "margin-top": "32px",
            "margin-bottom": "18px",
            "line-height": "1.3"
        },
        'h3': {
            "font-size": "20px",
            "font-weight": "700",
            "margin-top": "30px",
            "margin-bottom": "16px",
            "line-height": "1.3"
        },
        'blockquote': {
            "color": "#555555",
            "padding": "0 20px",
            "margin": "20px 0",
            "border-left": "3px solid #ccc",
            "font-style": "italic"
        },
        'a': {
            "color": "#3366CC",
            "text-decoration": "underline",
            "text-decoration-color": "rgba(51, 102, 204, 0.4)"
        },
        'strong': {
            "font-weight": "700"
        },
        'em': {
            "font-style": "italic"
        },
        'ul': {
            "margin-top": "20px",
            "margin-bottom": "20px",
            "padding-left": "25px"
        },
        'ol': {
            "margin-top": "20px",
            "margin-bottom": "20px", 
            "padding-left": "25px"
        },
        'li': {
            "margin-bottom": "10px",
            "line-height": "1.6"
        },
        'code': {
            "font-family": "Menlo, Monaco, 'Courier New', monospace",
            "font-size": "16px",
            "background-color": "#f5f5f5",
            "padding": "2px 4px",
            "border-radius": "3px"
        },
        'pre': {
            "background-color": "#f5f5f5",
            "padding": "16px",
            "border-radius": "4px",
            "overflow": "auto",
            "font-family": "Menlo, Monaco, 'Courier New', monospace",
            "margin": "20px 0",
            "font-size": "14px",
            "line-height": "1.5"
        },
        'img': {
            "max-width": "100%",
            "height": "auto",
            "display": "block",
            "margin": "25px auto"
        },
        'hr': {
            "border": "none",
            "border-top": "1px solid #ddd",
            "margin": "30px 0"
        },
        'table': {
            "width": "100%",
            "border-collapse": "collapse",
            "margin": "25px 0"
        },
        'th': {
            "border-bottom": "2px solid #ddd",
            "padding": "10px 15px",
            "text-align": "left",
            "font-weight": "700"
        },
        'td': {
            "border-bottom": "1px solid #ddd",
            "padding": "10px 15px"
        }
    }
    
    # 创建包含所有元素的section
    section = soup.new_tag('section')
    section_style = '; '.join([f"{k}: {v}" for k, v in styles.get('section', {}).items()])
    section['style'] = section_style
    
    # 将所有顶级元素移动到section中
    for child in list(soup.children):
        section.append(child)
    
    # 清空soup并添加section
    soup.clear()
    soup.append(section)
    
    # 为特定元素应用内联样式
    for tag_name, tag_style in styles.items():
        if tag_name == 'section':
            continue
            
        for tag in soup.find_all(tag_name):
            tag_style_str = '; '.join([f"{k}: {v}" for k, v in tag_style.items()])
            tag['style'] = tag_style_str
    
    return str(soup)
