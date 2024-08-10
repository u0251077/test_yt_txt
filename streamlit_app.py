import streamlit as st
from pyvis.network import Network
import streamlit.components.v1 as components

# 初始化节点
if 'nodes' not in st.session_state:
    st.session_state.nodes = []
if 'edges' not in st.session_state:
    st.session_state.edges = []

# 输入节点信息
node_name = st.text_input("输入节点名称")
node_parent = st.text_input("输入父节点名称 (留空表示根节点)")
if st.button("添加节点"):
    if node_name:
        if node_parent:
            st.session_state.edges.append((node_parent, node_name))
        st.session_state.nodes.append(node_name)
        st.success(f"节点 '{node_name}' 已添加")

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

