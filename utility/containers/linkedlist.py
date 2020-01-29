#!/usr/bin/env python3


class linkedlist:
  class linkedlist_node:
    def __init__(self, data, value=None):
      self.__data = data
      self.__value = value
      self.__next = None
      self.__prev = None

    @property
    def data(self):
      return self.__data

    @property
    def value(self):
      return self.__value
    @value.setter
    def value(self, value):
      self.__value = value

    @property
    def next_node(self):
      return self.__next
    @next_node.setter
    def next_node(self, value):
      self.__next = value

    @property
    def prev_node(self):
      return self.__prev
    @prev_node.setter
    def prev_node(self, value):
      self.__prev = value

    @property
    def nodes(self):
      return self.__next, self.__prev
    @nodes.setter
    def nodes(self, value):
      self.__next, self.__prev = value


  def _make_node(self, value):
    return self.linkedlist_node(self, value)

  def __init__(self):
    self.__head = self._make_node(None)
    self.__tail = self._make_node(None)
    self.__head.next_node = self.__tail
    self.__tail.prev_node = self.__head
    self.__count = 0

  def insert_before(self, where, value):
    node = self._make_node(value)
    node.nodes = where, where.prev_node
    where.prev_node.next_node = where.prev_node = node
    self.__count += 1
    return node

  def insert_after(self, where, value):
    node = self._make_node(value)
    node.nodes = where.next_node, where
    where.next_node.prev_node = where.next_node = node
    self.__count += 1
    return node

  def remove(self, where):
    if where.data is self and where.prev_node and where.next_node:
      node = where.next_node
      where.prev_node.next_node, where.next_node.prev_node = where.next_node, where.prev_node
      where.value = where.next_node = where.prev_node = None
      self.__count -= 1
      return node
    return where

  def append_back(self, value):
    return self.insert_before(self.__tail, value)

  def append_front(self, value):
    return self.insert_after(self.__head, value)

  def clear(self):
    self.__head.next_node = self.__tail
    self.__tail.prev_node = self.__head

  def __iter__(self):
    node = self.__head.next_node
    while node != self.__tail:
      yield node.value
      node = node.next_node

  def __reversed__(self):
    node = self.__tail.prev_node
    while node != self.__head:
      yield node.value
      node = node.prev_node

  def iterators(self):
    node = self.__head.next_node
    while node != self.__tail:
      yield node
      node = node.next_node

  def reverseiterators(self):
    node = self.__tail.prev_node
    while node != self.__head:
      yield node
      node = node.prev_node



def main():
  l = linkedlist()
  l.append_back(1)
  a = l.append_back(2)
  l.append_back(3)
  for v in l:
    print(v, end=", ")
  print()
  l.remove(a)
  print(list(l))

if __name__ == "__main__":
  main()
