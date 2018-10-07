from parser import HomerTechniqueCSVReader

#Test examples
s = HomerTechniqueCSVReader
k = s.read_csv(file='kehlin_athlete.csv')
k = s.neuro_sum(k)
print(k)