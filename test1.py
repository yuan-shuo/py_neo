from py2neo import Node, Graph, Relationship, NodeMatcher
import pandas as pd

# 连接数据库并清空所有内容（要先启动数据库不然先注释掉）
link = Graph("http://localhost:7474", auth=("neo4j", "174235"))
graph = link
graph.delete_all()

# 读取表格内容
point_data = pd.read_excel('./point.xlsx')

# 绘制节点的函数
def plot_point(lis1, lis2, lis3):
    for i in range(len(lis1)):
        node = Node(lis2[i], name=lis1[i], level=lis3[i])
        graph.create(node)

point_name = []
for i in range(0, len(point_data)):
    point_name.append(str(point_data['节点'][i]))
var_name = []
for i in range(0, len(point_data)):
   var_name.append(str(point_data['变量名'][i]))
point_level = []
for i in range(0, len(point_data)):
   point_level.append(str(point_data['level'][i]))

plot_point(point_name, var_name, point_level)

# print(point_name)
# print(var_name)