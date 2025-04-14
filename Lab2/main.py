import Solution

solution = Solution.Solution()
print("Generacja przybliżenia na podstawie źródła Markova pierwszego rzędu")
solution.run("../Dane/norm_wiki_sample.txt",1, 20, False)
print("Generacja przybliżenia na podstawie źródła Markova drugiego rzędu")
solution.run("../Dane/norm_wiki_sample.txt",2, 20, False)
print("Generacja przybliżenia na podstawie źródła Markova drugiego rzędu zaczynająca się od słowa 'probability")
solution.run("../Dane/norm_wiki_sample.txt",2, 20, True)
