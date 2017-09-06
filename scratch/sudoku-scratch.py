
def cross(str1,str2):
  return [ x+y  for x in str1 for y in str2]

print(cross('abc','def'))
