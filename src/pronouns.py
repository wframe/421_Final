f_pers = ['I', 'me', 'myself', 'mine', 'my', 'mine', 'me', 'we', 'us', 'ourselves', 'ourself', 'ours', 'our']
s_pers = ['you', 'yourself', 'yours', 'your', 'yourselves']

#third person
masc = ['he', 'him', 'himself', 'hisself', 'his']
fem = ['she', 'her', 'herself', 'hers', 'her']

neut =	['it', 'itself', 'its']
epi = ['they', 'them', 'themself', 'themselves', 'theirself', 'theirselves', 'theirs', 'their']

plur = ['they', 'them', 'themselves', 'theirselves', 'theirs', 'their']

genless = neut + epi

t_pers = masc + fem + genless
pros = f_pers + s_pers + t_pers 
