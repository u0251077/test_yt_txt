import streamlit as st
from openai import OpenAI
from pyvis.network import Network
import streamlit.components.v1 as components

# 配置 OpenAI API 密钥
api_key = st.text_input('请输入 OpenAI API 密钥', type='password')
if api_key:
    client = OpenAI(api_key=api_key)

    # 函数：获取对话中的关键信息
    def extract_concepts_from_text(text):
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "从下面的句子中提取出关键概念和它们之间的关系："+text}
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
        if user_input and api_key:
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
            
            # 打印调试信息
            st.write("当前节点:", st.session_state.nodes)
            st.write("当前边:", st.session_state.edges)

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
    else:
        st.write("没有节点，无法绘制思维导图。")
else:
    st.warning("请先输入 OpenAI API 密钥。")
