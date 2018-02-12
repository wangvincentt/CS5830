class Wheel(object):
  def __init__(self,size=0,offset=0,data=None):
    self.size = size
    self.data = [None]*size
    self.pos = offset
    if data:
      self.data = []
      for char in data:
        self.data.append(int(char)) 
      self.size = len(data)
      print (self.size,self.pos)

  def get(self,pos=None):
    if pos == None:
      val = self.data[self.pos]
      self.pos = self.pos + 1
      if self.pos == self.size:
        self.pos = 0
      return val 
    return self.data[pos % self.size]

  def set(self,pos,value):
    if self.data[pos % self.size] != None and self.data[pos % self.size] != value:
      print ('Diferent value',self.data[pos % self.size],value)
    self.data[pos % self.size] = value

  def getTotal(self):
    return sum(data != None for data in self.data)

  def exist(self,pos):
    return self.data[pos % self.size] != None

  def print_bits(self):
    bits = ''
    for bit in self.data:
      bits = bits + str(bit)
    return bits