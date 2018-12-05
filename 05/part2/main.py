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

    def react(s):
        stack = []
        for c in s:
          if len(stack) == 0:
            stack.append(c)
          elif c.upper() == stack[-1] and c.islower():
            stack.pop()
          elif c.lower() == stack[-1] and c.isupper():
            stack.pop()
          else:
            stack.append(c)
      
        return len(''.join(stack))

    best = ('0', 1000000)
    for t in 'abcdefghijklmnopqrstuvwxyz':
        kstr = string[:]
        kstr = kstr.replace(t, '')
        kstr = kstr.replace(t.upper(), '')
        num = react(kstr)
        if num < best[1]:
            best = (t, num)
    print(best)