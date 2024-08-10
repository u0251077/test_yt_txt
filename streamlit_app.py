import streamlit as st
from openai import OpenAI
from pyvis.network import Network
import streamlit.components.v1 as components

# 配置 OpenAI API 密钥
api_key = st.text_input('請輸入 OpenAI API 金鑰', type='password')
openai.api_key = api_key
client = OpenAI(api_key=api_key)

# 函数：获取对话中的关键信息
def extract_concepts_from_text(text):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "請用中文摘要以下內容"+prompt}
        ],
        max_tokens=150
    )
    return completion.choices[0].message.content.strip()
    
# 初始化思维导图的节点和边
if 'nodes' not in st.session_state:
    st.session_state.nodes = []
if 'edges' not in st.session_state:
    st.session_state.edges = []

# 用户输入
user_input = st.text_area("请输入您的对话内容")
if st.button("提取概念并更新思维导图"):
    if user_input:
        extracted_text = extract_concepts_from_text(user_input)
        st.write("提取的内容:", extracted_text)
        
        # 假设提取的内容格式为：概念1 -> 概念2
        for line in extracted_text.split('\n'):
            if '->' in line:
                source, target = line.split('->')
                source = source.strip()
                target = target.strip()
                if source not in st.session_state.nodes:
                    st.session_state.nodes.append(source)
                if target not in st.session_state.nodes:
                    st.session_state.nodes.append(target)
                st.session_state.edges.append((source, target))

# 创建图形
def create_graph(nodes, edges):
    net = Network(height='600px', width='100%', notebook=True)
    for node in nodes:
        net.add_node(node)
    for edge in edges:
        net.add_edge(edge[0], edge[1])
    return net

# 绘制思维导图
if st.session_state.nodes:
    net = create_graph(st.session_state.nodes, st.session_state.edges)
    
    # 将 pyvis 图形渲染为 HTML
    net_html = net.generate_html()
    
    # 显示 HTML
    components.html(net_html, height=600)

