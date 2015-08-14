'''Author: Preeti Singh, Computer Science Department, Carnegie Mellon University'''

''' Following is the Pseudocode for B-tree implementation for Approch A) '''

''' This file is imported in iphash_btree_Lookup()'''

'''-------------------------------------********************************----------------------------------------'''

class _BNode(object):
	__slots__ = ["tree", "contents", "children"]
 
	def __init__(self, tree, contents=None, children=None):
		self.tree = tree
		self.contents = contents or []
		self.children = children or []
		if self.children:
			assert len(self.contents) + 1 == len(self.children), \
			"one more child than data item required"

	def grow(self, ancestors):
		parent, parent_index = ancestors.pop()
		minimum = self.tree.order // 2
		left_sib = right_sib = None
 
	# try to borrow from the right sibling
		if parent_index + 1 < len(parent.children):
			right_sib = parent.children[parent_index + 1]
		if len(right_sib.contents) > minimum:
			right_sib.lateral(parent, parent_index + 1, self, parent_index)
		return
 
	# try to borrow from the left sibling
		if parent_index:
			left_sib = parent.children[parent_index - 1]
		if len(left_sib.contents) > minimum:
			left_sib.lateral(parent, parent_index - 1, self, parent_index)
		return
 
	# consolidate with a sibling - try left first
		if left_sib:
			left_sib.contents.append(parent.contents[parent_index - 1])
			left_sib.contents.extend(self.contents)
		if self.children:
			left_sib.children.extend(self.children)
			parent.contents.pop(parent_index - 1)
			parent.children.pop(parent_index)
		else:
			self.contents.append(parent.contents[parent_index])
			self.contents.extend(right_sib.contents)
		if self.children:
			self.children.extend(right_sib.children)
			parent.contents.pop(parent_index)
			parent.children.pop(parent_index + 1)
	 
		if len(parent.contents) < minimum:
			if ancestors:
			# parent is not the root
			parent.grow(ancestors)
			elif not parent.contents:
			# parent is root, and its now empty
			self.tree._root = left_sib or self
 
	def split(self):
		center = len(self.contents) // 2
		median = self.contents[center]
		sibling = type(self)(
		self.tree,
		self.contents[center + 1:],
		self.children[center + 1:])
		self.contents = self.contents[:center]
		self.children = self.children[:center + 1]
	return sibling, median

	def insert(self, index, item, ancestors):
		self.contents.insert(index, item)
		if len(self.contents) > self.tree.order:
		self.shrink(ancestors)

class BTree(object):
	BRANCH = LEAF = _BNode
 
	def __init__(self, order):
		self.order = order
		self._root = self._bottom = self.LEAF(self)
 
	def _path_to(self, item):
		current = self._root
		ancestry = []
		while getattr(current, "children", None):
			index = bisect.bisect_left(current.contents, item)
			ancestry.append((current, index))
			if index < len(current.contents) \
			and current.contents[index] == item:
		return ancestry
		current = current.children[index]
 
		index = bisect.bisect_left(current.contents, item)
		ancestry.append((current, index))
		present = index < len(current.contents)
		present = present and current.contents[index] == item
 
	return ancestry

	#find if the B_tree consists of the node having particluar Ip_address 
	
	def _present(self, item, ancestors):
		last, index = ancestors[-1]
	return index < len(last.contents) and last.contents[index] == item

 
 	def __contains__(self, item):
		return self._present(item, self._path_to(item)

	 @classmethod
	#BulkLoading (Part of optimisation _ 
	def bulkload(cls, items, order):
		tree = object.__new__(cls)
		tree.order = order 
		leaves = tree._build_bulkloaded_leaves(items)
		tree._build_bulkloaded_branches(leaves)
 
	return tree
 
	def _build_bulkloaded_leaves(self, items):
		minimum = self.order // 2
		leaves, seps = [[]], []
 
		for item in items:
			if len(leaves[-1]) < self.order:
				leaves[-1].append(item)
			else:
				seps.append(item)
				leaves.append([])
 
			if len(leaves[-1]) < minimum and seps:
				last_two = leaves[-2] + [seps.pop()] + leaves[-1]
				leaves[-2] = last_two[:minimum]
				leaves[-1] = last_two[minimum + 1:]
				seps.append(last_two[minimum])
			return [self.LEAF(self, contents=node) for node in leaves], seps

	def _build_bulkloaded_branches(self, (leaves, seps)):
		minimum = self.order // 2
		levels = [leaves]
 
		while len(seps) > self.order + 1:
			items, nodes, seps = seps, [[]], []
 
		for item in items:
			if len(nodes[-1]) < self.order:
				nodes[-1].append(item)
			else:
				seps.append(item)
				nodes.append([])
 
			if len(nodes[-1]) < minimum and seps:
				last_two = nodes[-2] + [seps.pop()] + nodes[-1]
				nodes[-2] = last_two[:minimum]
				nodes[-1] = last_two[minimum + 1:]
				seps.append(last_two[minimum])
 
				offset = 0
			for i, node in enumerate(nodes):
				children = levels[-1][offset:offset + len(node) + 1]
				nodes[i] = self.BRANCH(self, contents=node, children=children)
				offset += len(node) + 1
				levels.append(nodes)
				self._root = self.BRANCH(self, contents=seps, children=levels[-1])
