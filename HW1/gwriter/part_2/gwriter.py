from wheel import Wheel

DICT = '2T3O4HNM5LRGIPCVEZDBSYFXAWJ6UQK7'
PATH_TEXT = 'plaintext.txt'
PATH_CIPHER = 'ciphertext.txt'
LENS = [47,53,59,61,64,65,67,69,71,73]
wheels = []
for i in range (10):
  wheels.append(Wheel(LENS[i]))

dicLetterToInt = {}
dicIntToLetter = {}
for i in range (32):
  dicLetterToInt[DICT[i]] = i
  dicIntToLetter[i] = DICT[i]

def parseText(path):
  message = []
  file_object  = open(path, 'r')
  for line in file_object.readlines():
    for char in line:
      try:
        alph = DICT.index(char)
        message.append(alph)
      except:
        break
  return message

def xor(wheels,value):
  data = intToArray(value)
  for index,val in enumerate(data):
    data[index] = val ^ wheels[index]
  return [arrayToInt(data),data]

def encryp(wheels,value):
  data = intToArray(value)
  for index,val in enumerate(data):
    data[index] = val ^ wheels[index]
  if wheels[5]:
    swap(data,0,4)
  if wheels[6]:
    swap(data,0,1)
  if wheels[7]:
    swap(data,1,2)
  if wheels[8]:
    swap(data,2,3)
  if wheels[9]:
    swap(data,3,4)
  return [arrayToInt(data),data]

def swap(data,n1,n2):
  temp = data[n1]
  data[n1] = data[n2]
  data[n2] = temp
  return data

def arrayToInt(array):
  number = ''
  for bit in array:
    number = number + str(bit)
  return int(number,2)

def intToArray(num):
  array = []
  bits = "{0:05b}".format(num)
  for bit in bits:
    array.append(int(bit))
  return array

def getCurrentValues(pos):
  res = []
  for wheel in wheels:
    res.append(wheel.get(pos))
  return res


def main ():
  plain_message = parseText(PATH_TEXT)
  cipher_message = parseText(PATH_CIPHER)

  for index,value in enumerate(cipher_message):
    if value == 0 or value == 31:
      bits = "{0:05b}".format(plain_message[index])
      for index_bit,bit in enumerate((bits)):
        bit = int(bit)
        if value == 0:
          val = bit
        else:
          val = bit ^ 1
        if not wheels[index_bit].exist(index):
          wheels[index_bit].set(index,val) 

  set_zero = [0b10111,0b11011,0b11101]
  set_one = [0b01000,0b00100,0b00010]

  count = 0
  for index,value in enumerate(cipher_message):
    [encrypt,encrypt_bits] = xor(getCurrentValues(index),plain_message[index])
    if encrypt in set_zero:
      count = count + 1
      index_message = encrypt_bits.index(0)
      index_sturgeon = intToArray(value).index(0)
      if index_message == index_sturgeon:
        wheels[5+index_message].set(index,0)
        wheels[5+index_sturgeon].set(index,0)
      elif index_sturgeon < index_message:
        wheels[5+index_message].set(index,1)
      else:
        for index_wheel in range(index_message+1,index_sturgeon+1):
          wheels[5+index_wheel].set(index,1)
    elif encrypt in set_one:
      count = count + 1
      index_message = encrypt_bits.index(1)
      index_sturgeon = intToArray(value).index(1)
      if index_message == index_sturgeon:
        wheels[5+index_message].set(index,0)
        wheels[5+index_sturgeon].set(index,0)
      elif index_sturgeon < index_message:
        wheels[5+index_message].set(index,1)
      else:
        for index_wheel in range(index_message+1,index_sturgeon+1):
          wheels[5+index_wheel].set(index,1)

  count = 0

  set_zero = [0b01111,0b11110]
  set_one =  [0b10000,0b00001]

  for index,value in enumerate(cipher_message):
    [encrypt,encrypt_bits] = xor(getCurrentValues(index),plain_message[index])
    if None in getCurrentValues(index):
      if encrypt in set_zero:
        index_message = encrypt_bits.index(0)
        index_sturgeon = intToArray(value).index(0)
        count = count + 1

      if encrypt in set_one:
        index_message = encrypt_bits.index(1)
        index_sturgeon = intToArray(value).index(1)
        count = count + 1

  for index,value in enumerate(cipher_message):
    option_wheels = getCurrentValues(index)
    if option_wheels.count(None) == 1:
      idx_none = option_wheels.index(None)
      opt_1 = list(option_wheels)
      opt_2 = list(option_wheels)
      opt_1[idx_none] = 1
      opt_2[idx_none] = 0
      [encrypt_1,encrypt_bits_1] = encryp(opt_1,plain_message[index])
      [encrypt_2,encrypt_bits_2] = encryp(opt_2,plain_message[index])
      if value != encrypt_1 or value != encrypt_2:
        if value == encrypt_1:
          wheels[idx_none].set(index,1)
        elif value == encrypt_2:
          wheels[idx_none].set(index,0)


  file = open("rotors.txt","w") 

  for i in range (10):
    countent = str(wheels[i].size) + ' ' + str(wheels[i].print_bits()) + '\r\n'
    file.write(countent)

main ()
