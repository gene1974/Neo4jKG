import sys
from py2neo import Graph, Node, Relationship
from py2neo import NodeMatcher,RelationshipMatcher


# 用label表示图谱类型：Product

class NodeObject(object):
    def __init__(self, label, name, properties) -> None:
        self.label = label
        self.name = name
        self.properties = properties
        self.node = None

'''
@func:  添加一个节点，会重复添加
@usage: add_node(graph, 'Person', {'name': 'bob'})
'''
def add_node(graph, label, properties = {}):
    node  = Node(label, **properties)
    graph.create(node)
    return node.items

'''
@func:  查找图谱中存在的节点，返回匹配节点列表
@usage: find_node(graph, 'Person', {'name': 'bob'})
'''
def find_node(graph, label, properties = {}):
    node_matcher = NodeMatcher(graph)
    if isinstance(properties, dict):
        nodes = node_matcher.match(label).where(**properties)
    elif isinstance(properties, str): # 模糊匹配
        # node_matcher.match("Person").where("_.work =~ '月亮.*'")
        # node_matcher.match("Person").where("_.age > 20")
        nodes = node_matcher.match(label).where(properties)
    else:
        sys.stderr.write('Error type of properties: expect dict or str, got', type(properties))
    # return nodes.first() # 第一个匹配值
    return list(nodes)

'''
@func:  返回节点是否存在
@usage: exist_node(graph, 'Person', {'name': 'bob'})
'''
def exist_node(graph, label, properties = {}):
    nodes = find_node(graph, label, properties)
    return len(nodes) != 0

'''
@func:  获取图谱中节点的所有属性
@usage: prop = get_node_properties(graph, 'Person', {'name': 'bob'})
'''
def get_node_properties(graph, label, properties):
    nodes = find_node(graph, label, properties)
    if len(nodes) == 0:
        return {}
    else:
        return dict(nodes[0].items()) # {'name': 'c'}

'''
@func:  更新图谱中节点或关系的属性
@usage: node1 = find_node(graph, 'Person', {'name': 'alice'})[0]
        update_node_prop(graph, node1, {'gender': 'female'})
'''
def update_properties(graph, node, properties):
    for key in properties:
        node[key] = properties[key]
    graph.push(node)



# Relation
'''
@func:  向图谱中的两个节点添加关系
@usage: node1 = find_node(graph, 'Person', {'name': 'alice'})[0]
        node2 = find_node(graph, 'Person', {'name': 'bob'})[0]
        add_relation(graph, node1, 'KNOWS', node2)
'''
def add_relation(graph, node1, relation, node2, properties = {}):
    edge = Relationship(node1, relation, node2, **properties)
    graph.create(edge)

'''
@func:  查询图谱中两个节点间的关系
@usage: node1 = find_node(graph, 'Person', {'name': 'alice'})[0]
        node2 = find_node(graph, 'Person', {'name': 'bob'})[0]
        relation = find_relation(graph, [node1]) # node1的所有关系
        relation = find_relation(graph, [node1, node2]) # node1到node2的所有关系
        relation = find_relation(graph, relation = 'KNOWS') # 关系为'KNOWS'的所有关系
'''
def find_relation(graph, nodes = None, relation = None, properties = {}, limit = 10):
    rel_matcher = RelationshipMatcher(graph)
    relations = list(rel_matcher.match(nodes, r_type = relation).limit(limit))
    return relations

'''
@func:  解析关系对象Relationship
@usage: node1 = find_node(graph, 'Person', {'name': 'alice'})[0]
        node2 = find_node(graph, 'Person', {'name': 'bob'})[0]
        relation = find_relation(graph, [node1]) # node1的所有关系
        relation = find_relation(graph, [node1, node2]) # node1到node2的所有关系
        relation = find_relation(graph, relation = 'KNOWS') # 关系为'KNOWS'的所有关系
'''
def parse_relation(relation):
    print(relation)
    head = relation.start_node
    tail = relation.end_node
    rel = type(relation).__name__
    prop = relation.keys()
    # value = relation.get(key)
    return head, tail, rel

'''
@func:  查询节点的所有关系
@usage: del_all_nodes(graph)
'''
def find_all_relation(graph, node):
    rel_matcher = RelationshipMatcher(graph)
    relations = list(rel_matcher.match([node], r_type=None)) # r_type = None表示任何类型的关系均可
    return relations



'''
@func:  删除图谱中的所有节点和关系
@usage: del_all_nodes(graph)
'''
def del_all_nodes(graph):
    graph.delete_all()



if __name__ == '__main__':
    graph = Graph('http://localhost:7474', name='neo4j', password='ngn5110')
    
    # add_node
    # add_node(graph, 'Person', {'name': 'alice'})
    # add_node(graph, 'Person', {'name': 'alice'})
    # add_node(graph, 'Person', {'name': 'bob'})
    
    # # add relation
    node1 = find_node(graph, 'Person', {'name': 'alice'})[0]
    node2 = find_node(graph, 'Person', {'name': 'bob'})[0]
    # add_relation(graph, node1, 'KNOWS', node2)
    # update_node_prop(graph, node1, {'gender': 'female'})
    # rel = find_relation(graph, [node1])
    # rel = find_relation(graph, [node1, node2])
    # rel = find_relation(graph, relation = 'KNOWS')

