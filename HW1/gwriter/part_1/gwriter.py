str = '2T3O4HNM5LRGIPCVEZDBSYFXAWJ6UQK7'
dicLetterToInt = {}
dicIntToLetter = {}
for i in range (32):
  dicLetterToInt[str[i]] = i
  dicIntToLetter[i] = str[i]

def readFile(file_name):
  arr = []
  with open (file_name) as f: 
    for line in f: 
      arr.append(line.rstrip())
  return arr

def rotorRead(file_name):
  arr = readFile(file_name)
  for i in range (len(arr)):
    arr[i] = arr[i][9:]
  return arr

def swap(arr, i, j):
  tmp = arr[i]
  arr[i] = arr[j]
  arr[j] = tmp

def bits_to_int(bits):
  res = 0
  for i in range (5):
    t = bits[i] << (4 - i)
    res +=  t 
  return res

def encryption(plaintexts, rotors, order, offset, lens):
  steps = 0;
  file = open("test-ciphertext.txt","w") 

  for j in range (len(plaintexts)):
    for i in range (len(plaintexts[j])):
      bits = [1 if ((rotors[order[j]][(offset[j] + steps) % lens[order[j]]]) == '1') else 0 for j in range (10)]
      pt = dicLetterToInt[plaintexts[j][i]]
      c = [((pt >> i) & (1)) for i in range (4, -1, -1)]
      for i in range (5):
        c[i] = ( c[i] ^ bits[i]) 
      
      if (bits[5] == 1):
        swap(c, 0, 4)
      if (bits[6] == 1):
        swap(c, 0, 1)
      if (bits[7] == 1):
        swap(c, 1, 2)
      if (bits[8] == 1):
        swap(c, 2, 3)
      if (bits[9] == 1):
        swap(c, 3, 4)
      res = bits_to_int(c)
      steps += 1
      file.write(dicIntToLetter[res])
    file.write('\r\n')

def decryption(ciphers, rotors, order, offset, lens):
  steps = 0
  file = open("test-plaintext.txt","w") 

  for j in range (len(ciphers)):
    for i in range (len(ciphers[j])):
      bits = [1 if ((rotors[order[j]][(offset[j] + steps) % lens[order[j]]]) == '1') else 0 for j in range (10)]
      ct = dicLetterToInt[ciphers[j][i]]
      p = [((ct >> i) & (1)) for i in range (4, -1, -1)]

      if (bits[9] == 1):
        swap(p, 3, 4)
      if (bits[8] == 1):
        swap(p, 2, 3)
      if (bits[7] == 1):
        swap(p, 1, 2)
      if (bits[6] == 1):
        swap(p, 0, 1)
      if (bits[5] == 1):
        swap(p, 0, 4)

      for i in range (5):
        p[i] = ( p[i] ^ bits[i]) 
      steps += 1
      res = bits_to_int(p)
      file.write(dicIntToLetter[res])
    file.write('\r\n')

def main ():
  cipher_file = 'ciphertext.txt'
  plaintext_file = 'plaintext.txt'
  rotor_file = 'rotors.txt'
  ciphers = readFile(cipher_file)
  plaintexts = readFile(plaintext_file)
  rotors = rotorRead(rotor_file)
  order = [8,7,2,4,3,5,6,1,0,9]
  offset = [44,52,35,14,19,55,6,4,3,51]
  lens = [47,53,59,61,64,65,67,69,71,73]
  
  encryption(plaintexts, rotors, order, offset, lens)
  decryption(ciphers, rotors, order, offset, lens)

main()


