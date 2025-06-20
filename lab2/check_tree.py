from regex_parser import tokenize, insert_concat, to_postfix
from syntax_tree import SyntaxTree
from nfa_dfa import DFA, DFAState, dfa_to_regex, simplify_regex
from dfa_min import DFAOptimizer
from regex_engine import Regex


# Пример 1 — простая проверка
r = Regex("(a|bc)*|(a|bc)*ba(c)*").compile()
     
restored = simplify_regex(dfa_to_regex(r.dfa))
print("2. регулярка", restored)  

#print("Токены:", tokenize("(&.)*&a&b&b"))
#r1 = Regex("(a|b)*abb").compile()
# #r2 = Regex(".*abb").compile()  

# r_inter = r1.intersect(r2)
# print("3. Intersect match 'aabb':", r_inter.match("aabb"))  
# print("4. Intersect match 'ab':", r_inter.match("ab"))      



# r1 = Regex("(a|b)*abb").compile()
# r2 = Regex("a+abb").compile()

# r_diff = r1.difference(r2)
# print("5. Difference match 'abb':", r_diff.match("abb"))    
# print("6. Difference match 'aaabb':", r_diff.match("aaabb")) 



# r = Regex("(a|bc)*").compile()
# regex_restored = dfa_to_regex(r.dfa)
# print("7. Восстановленное регулярное выражение:", regex_restored)

# simplified = simplify_regex(regex_restored)
# print("8. Упрощённое регулярное выражение:", simplified)


# r = Regex("a.{1,2}c").compile()
# print("9. Match 'abc':", r.match("abc"))    
# print("10. Match 'aXc':", r.match("aXc"))   
# print("11. Match 'ac':", r.match("ac"))      


# r = Regex("(<g>a(b|c)?d)").compile()
# print("12. Match 'abd':", r.match("abd"))     
# print("13. Match 'ad':", r.match("ad"))      
# print("14. Match 'abcd':", r.match("abcd"))   


