#Python file to test small things
from pathlib import Path
def main():
    filepath = 'Categories/Advertising/Advertising.csv'
    scores = []
    with open(filepath, 'r') as f:
         for line in f:
            score = float(line.strip().split(',')[1])
            scores.append(score)
         print(sorted(scores))



if __name__ == '__main__':
    main()
