from py2neo import Node, Graph, Relationship, NodeMatcher, Subgraph
import pandas as pd

# 连接数据库并清空所有内容（要先启动数据库不然先注释掉）
link = Graph("http://localhost:7474", auth=("neo4j", "174235"))
graph = link
graph.delete_all()

# 读取表格内容
point_data = pd.read_excel('./point.xlsx')

# 绘制节点的函数
def plot_point(lis1, lis2, lis3, lis4):
    for i in range(len(lis1)):
        node = Node(lis2[i], name=lis1[i], level=lis3[i], father=lis4[i])
        graph.create(node)

# 联系节点的函数
def link_point(point_name, level_list):
    # 所有level 1=>0
    node_a = graph.nodes.match(level='1').all()
    node_b = graph.nodes.match(level='0').first()
    for na in node_a:
        rel_ab = Relationship(na, "评估参数", node_b)
        graph.create(rel_ab)

    # 所有level 2=>1
    for i in range(len(level_list)):
        if level_list[i] == '1':
            p_name = point_name[i]
            node_a = graph.nodes.match(father=p_name).all()
            node_b = graph.nodes.match(name=p_name).first()
            if node_a:
                for na in node_a:
                    rel_ab = Relationship(na, "评估参数", node_b)
                    graph.create(rel_ab)

point_name = []
for i in range(0, len(point_data)):
    point_name.append(str(point_data['节点'][i]))
var_name = []
for i in range(0, len(point_data)):
   var_name.append(str(point_data['变量名'][i]))
point_level = []
for i in range(0, len(point_data)):
   point_level.append(str(point_data['level'][i]))
point_father = []
for i in range(0, len(point_data)):
   point_father.append(str(point_data['father'][i]))

# 画点
plot_point(point_name, var_name, point_level, point_father)
# 连线
link_point(point_name, point_level)

# a_have=graph.nodes.match("分级方法",name="RMR").first()
# b_have=graph.nodes.match("使用参数", father="RMR").all()
# for node_b in b_have:
#     rel_a = Relationship(node_b, "评估参数", a_have)
#     graph.create(rel_a)

# print(point_name)
# print(var_name)