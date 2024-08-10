import streamlit as st
import graphviz

# 初始化思维导图节点
if 'nodes' not in st.session_state:
    st.session_state.nodes = []

# 输入节点信息
node_name = st.text_input("输入节点名称")
if st.button("添加节点"):
    if node_name:
        st.session_state.nodes.append(node_name)
        st.success(f"节点 '{node_name}' 已添加")

# 绘制思维导图
if st.session_state.nodes:
    dot = graphviz.Digraph()
    for node in st.session_state.nodes:
        dot.node(node)

    # 生成并显示思维导图
    st.graphviz_chart(dot)

