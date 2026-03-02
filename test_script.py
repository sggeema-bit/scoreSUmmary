import sys
sys.path.insert(0, 'c:/app/SDD/scoreSUmmary')
from src.main import analyze_innings

print('valid output:', analyze_innings(50,40,3,1))
try:
    analyze_innings(50,0,3,1)
except Exception as e:
    print('error1', e)
try:
    analyze_innings(50,40,0,0)
except Exception as e:
    print('error2', e)
