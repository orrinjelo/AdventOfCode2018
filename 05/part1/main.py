import os, sys

if __name__ == '__main__':
    # Parse args
    if len(sys.argv) <= 1:
        sys.exit('No filename given.')
    elif len(sys.argv) > 2:
        sys.exit('Too many arguments.')
    with open(sys.argv[1], 'r') as f:
        lines = f.readlines()
    string = ''.join(lines)

    # First step
    stack = []
    for c in string:
      if len(stack) == 0:
        stack.append(c)
      elif c.upper() == stack[-1] and c.islower():
        stack.pop()
      elif c.lower() == stack[-1] and c.isupper():
        stack.pop()
      else:
        stack.append(c)
  
    print(len(''.join(stack)))