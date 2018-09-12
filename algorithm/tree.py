
dict_tree = {
    "element": 0,
    "left": {
        "element": 1,
        "left": {
            "element": 3,
            "left": 6,
            "right": 7,
        }
    },
    "right": {
        "element": 2,
        "left": 4,
        "right": {
            "element": 5,
            "left": 8,
            "right": 9,
        },
    },
}


class BiNode(object):
    """class BiNode provide interface to set up a BiTree Node and to interact"""
    def __init__(self, element=None, left=None, right=None):
        """set up a node """
        self.element = element
        self.left = left
        self.right = right

    def get_element(self):
        """return node.element"""
        return self.element

    def dict_form(self):
        """return node as dict form"""
        dict_set = {
            "element": self.element,
            "left": self.left,
            "right": self.right,
        }
        return dict_set

    def __str__(self):
        """when print a node , print it's element"""
        return str(self.element)


class BiTree(object):
    """class BiTree provide interface to set up a BiTree and to interact"""
    def __init__(self, tree_node=None):
        """set up BiTree from BiNode and empty BiTree when nothing is passed"""
        self.root = tree_node

    def add_node_in_order(self, element):
        """add a node to existent BiTree in order"""
        node = BiNode(element)

        if self.root is None:
            self.root = node
        else:
            node_queue = list()
            node_queue.append(self.root)
            while len(node_queue):
                q_node = node_queue.pop(0)
                if q_node.left is None:
                    q_node.left = node
                    break
                elif q_node.right is None:
                    q_node.right = node
                    break
                else:
                    node_queue.append(q_node.left)
                    node_queue.append(q_node.right)

    def set_up_in_order(self, elements_list):
        """set up BiTree from lists of elements in order """
        for elements in elements_list:
            self.add_node_in_order(elements)

    def set_up_from_dict(self, dict_instance):
        """set up BiTree from a dict_form tree using level traverse, or call it copy """
        if not isinstance(dict_instance, dict):
            return None
        else:
            dict_queue = list()
            node_queue = list()
            node = BiNode(dict_instance["element"])
            self.root = node
            node_queue.append(node)
            dict_queue.append(dict_instance)
            while len(dict_queue):
                dict_in = dict_queue.pop(0)
                node = node_queue.pop(0)
                # in dict form, the leaf node might be irregular, like compressed to element type
                # Thus , all this case should be solved out respectively
                if isinstance(dict_in.get("left", None), (dict, int, float, str)):
                    if isinstance(dict_in.get("left", None), dict):
                        dict_queue.append(dict_in.get("left", None))
                        left_node = BiNode(dict_in.get("left", None)["element"])
                        node_queue.append(left_node)
                    else:
                        left_node = BiNode(dict_in.get("left", None))
                    node.left = left_node

                if isinstance(dict_in.get("right", None), (dict, int, float, str)):
                    if isinstance(dict_in.get("right", None), dict):
                        dict_queue.append(dict_in.get("right", None))
                        right_node = BiNode(dict_in.get("right", None)["element"])
                        node_queue.append(right_node)
                    else:
                        right_node = BiNode(dict_in.get("right", None))
                    node.right = right_node

    def pack_to_dict(self):
        """pack up BiTree to dict form using level traversal"""
        if self.root is None:
            return None
        else:
            node_queue = list()
            dict_queue = list()
            node_queue.append(self.root)
            dict_pack = self.root.dict_form()
            dict_queue.append(dict_pack)
            while len(node_queue):
                q_node = node_queue.pop(0)
                dict_get = dict_queue.pop(0)
                if q_node.left is not None:
                    node_queue.append(q_node.left)
                    dict_get["left"] = q_node.left.dict_form()
                    dict_queue.append(dict_get["left"])
                if q_node.right is not None:
                    node_queue.append(q_node.right)
                    dict_get["right"] = q_node.right.dict_form()
                    dict_queue.append(dict_get["right"])
        return dict_pack

    def get_depth(self):
        """method of getting depth of BiTree"""
        if self.root is None:
            return 0
        else:
            node_queue = list()
            node_queue.append(self.root)
            depth = 0
            while len(node_queue):
                q_len = len(node_queue)
                while q_len:
                    q_node = node_queue.pop(0)
                    q_len = q_len - 1
                    if q_node.left is not None:
                        node_queue.append(q_node.left)
                    if q_node.right is not None:
                        node_queue.append(q_node.right)
                depth = depth + 1
            return depth

    def pre_traversal(self):
        """method of traversing BiTree in pre-order"""
        if self.root is None:
            return None
        else:
            node_stack = list()
            output_list = list()
            node = self.root
            while node is not None or len(node_stack):
                # if node is None which means it comes from a leaf-node' right,
                # pop the stack and get it's right node.
                # continue the circulating like this
                if node is None:
                    node = node_stack.pop().right
                    continue
                #  save the front node and go next when left node exists
                while node.left is not None:
                    node_stack.append(node)
                    output_list.append(node.get_element())
                    node = node.left
                output_list.append(node.get_element())
                node = node.right
        return output_list

    def pre_traversal_simple(self, tree_base='', li=[], start=True):
        if start:
            tree_base = self.root
            if self.root is None:
                return []
            li = list()
        if tree_base is None:
            return
        li.append(tree_base.get_element())
        self.pre_traversal_simple(tree_base.left, li, start=False)
        self.pre_traversal_simple(tree_base.right, li, start=False)
        if start:
            return li







tree1 = BiTree()
tree1.set_up_from_dict(dict_tree)
output_list = tree1.pre_traversal()
print(output_list)
print(tree1.pre_traversal_simple())
