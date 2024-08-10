import streamlit as st
from openai import OpenAI
from pyvis.network import Network
import streamlit.components.v1 as components
import re

# 配置 OpenAI API 密钥
api_key = st.text_input('请输入 OpenAI API 密钥', type='password')
if api_key:
    client = OpenAI(api_key=api_key)

    # 函数：获取对话中的关键信息
    def extract_concepts_from_text(text):
        try:
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "从下面的句子中提取出关键概念和它们之间的关系："+text}
                ],
                max_tokens=150
            )
            return completion.choices[0].message.content.strip()
        except Exception as e:
            st.error(f"提取概念时发生错误: {e}")
            return ""

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
            
            # 处理提取的内容
            if extracted_text:
                st.session_state.nodes = []  # 清空节点和边
                st.session_state.edges = []
                
                # 提取节点和边
                nodes_set = set()
                edges_set = set()
                
                # 通过正则表达式提取概念和关系
                matches = re.findall(r'(\S+) → (\S+)', extracted_text)
                for source, target in matches:
                    source = source.strip()
                    target = target.strip()
                    nodes_set.add(source)
                    nodes_set.add(target)
                    edges_set.add((source, target))
                
                st.session_state.nodes.extend(nodes_set)
                st.session_state.edges.extend(edges_set)
                
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
        try:
            net = create_graph(st.session_state.nodes, st.session_state.edges)
            
            # 将 pyvis 图形渲染为 HTML
            net_html = net.generate_html()
            
            # 显示 HTML
            components.html(net_html, height=600)
        except Exception as e:
            st.error(f"绘制思维导图时发生错误: {e}")
    else:
        st.write("没有节点，无法绘制思维导图。")
else:
    st.warning("请先输入 OpenAI API 密钥。")
