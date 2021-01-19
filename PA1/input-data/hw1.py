#########################################################################################
#                                       import                                          #                        
#########################################################################################
import os
import operator
import numpy as np

#########################################################################################
#                                        path                                           #                        
#########################################################################################
input_path = './web-search-files2'
all_file_list = os.listdir(input_path)
all_file_list.sort(key=lambda x: int(x.split('e')[1]))

#########################################################################################
#                                      parameter                                        #                        
#########################################################################################
page_link = {} # e.g. {'page0': ['page3', 'page5'], ...,'page500': []}
page_str = {} # e.g. {'page0': ['her clearing instrument...'], ...,'page500': []}
page_pointed = {} # e.g. {'page0': 137, ...,'page500': 13}
N = len(all_file_list) # N = 501
d = [0.25, 0.45, 0.65, 0.85]
DIFF = [0.1, 0.01, 0.001]
point_matrix = np.zeros((N, N))
word_list = []

#########################################################################################
#                                      function                                         #                        
#########################################################################################
def PageRank(allfile, d, DIFF):
    global page_pointed, N, page_pointed, all_file_list, point_matrix, page_link
    # Iteration
    diff, count = 0, 1
    while (True):
        for f in allfile:
            PR_before = page_pointed[f]
            # Calculate SUM(PR(t)/CR(t))
            weight = 0
            for i in range(N):
                if (int(point_matrix[i][eval(f[4:])]) == 1):
                    now_page = 'page' + str(i)
                    weight = weight + page_pointed[now_page]/len(page_link[now_page])
            # Page rank
            page_pointed[f] = (1-d)/N + d*weight
            diff = diff + abs(PR_before - page_pointed[f])
        # break
        if (diff < DIFF):
            break
        else: 
            count += 1
            diff = 0

def ReverseIndex():
    global word_list, page_str
    rev_name = './B07901103/' + 'reverseindex.txt'
    seq = []
    for word in word_list:
        count = 0
        content = word.ljust(20, ' ')
        for page in page_str:
            if (word in page_str[page]):
                if (count > 50):
                    content = content + '\n' + ' '*20
                    count = 0
                content = content + page + ' '
                count += 1
        content += '\n'
        seq.append(content)
    with open(rev_name, 'w') as rev_file:
        rev_file.writelines(seq)

def main():
    global all_file_list, page_link, page_str, page_pointed, N, d, DIFF, point_matrix, word_list
    # Initialize
    for file in all_file_list:
        # Initialize PR(i)
        page_pointed[file] = 1/N
    # Read files in the input_data
    for file in all_file_list:
        # Open file
        filename = './web-search-files2/'+file
        f = open(filename)
        lines = f.readlines()
        # Update page link / page string
        page_link[file] = []
        page_str[file] = []
        mark = 0
        for line in lines:
            # String
            if (mark == 1):
                page_str[file] = line
                # Build a "word list"
                temp = line.split(' ', line.count(' '))
                for i in range(len(temp)):
                    if (temp[i] != '\n') and (temp[i] not in word_list):
                        word_list.append(temp[i])
                break
            if (line[0] == '-'):
                mark = 1
                continue
            # Page
            if (mark == 0):
                page_link[file].append(line)
                point_matrix[eval(file[4:])][eval(line[4:])] = 1
        # Close file
        f.close()
    word_list.sort()
    # Main
    # Output(2): Reverse Index
    ReverseIndex()
    for prob in d:
        for delta in DIFF:
            PageRank(all_file_list, prob, delta)
            sorted_PR = dict(sorted(page_pointed.items(), key=operator.itemgetter(1),reverse=True))
            # Output(1): Page Rank List
            pr_name = './B07901103/' + 'pr_' + str(prob)[2:] + '_' + str(delta)[2:].ljust(3, '0') + '.txt'
            seq = []
            for PR in sorted_PR:
                content = PR.ljust(10, ' ') + str(len(page_link[PR])).ljust(6, ' ') + str(format(page_pointed[PR], '0.7f')) + '\n'
                seq.append(content)
            with open(pr_name, 'w') as pr_file:
                pr_file.writelines(seq)
            # Output(3): Search Engine
            list_txt = open('list.txt', 'r')
            list_line = list_txt.readlines()
            seq = []
            for lines in list_line:
                contained_page = []
                ori = lines.replace('\n', '')
                temp = lines.split(' ', lines.count(' '))
                temp[-1] = temp[-1].replace('\n', '')
                # One word, e.g. input = ["Baker"]
                if (len(temp) == 1):
                    for page in page_str:
                        if (temp[0] in page_str[page]):
                            contained_page.append(page)
                    # contained pages = 0
                    if (len(contained_page) == 0):
                        seq.append("none\n")
                    # contained pages > 0 (min{10, length(contained pages)})
                    else:
                        copy = contained_page
                        for i in range(min(10, len(contained_page))):
                            for j in sorted_PR:
                                if (j in copy):
                                    string = j + ' '
                                    seq.append(string)
                                    copy.remove(j)
                                    break
                        seq.append('\n')
                # Multi-words, e.g. input = "but emotion infinity"
                AND_page = []
                OR_page = []
                if (len(temp) > 1):
                    for page in page_str:
                        count = 0
                        for element in temp:
                            if (element not in page_str[page]):
                                break
                            if (element in page_str[page]):
                                count += 1
                                if (count == len(temp)):
                                    AND_page.append(page)
                        for element in temp:
                            if (element in page_str[page]):
                                OR_page.append(page)
                                break
                    # AND 
                    if (len(AND_page) == 0):
                        seq.append("AND none\n")
                    # contained pages > 0 (min{10, length(contained pages)})
                    if (len(AND_page) > 0):
                        seq.append("AND ")
                        copy = AND_page
                        for i in range(min(10, len(AND_page))):
                            for j in sorted_PR:
                                if (j in copy):
                                    string = j + ' '
                                    seq.append(string)
                                    copy.remove(j)
                                    break
                        seq.append('\n')
                    # OR
                    if (len(OR_page) == 0):
                        seq.append("OR none\n")
                    # contained pages > 0 (min{10, length(contained pages)})
                    if (len(OR_page) > 0):
                        seq.append("OR ")
                        copy = OR_page
                        for i in range(min(10, len(OR_page))):
                            for j in sorted_PR:
                                if (j in copy):
                                    string = j + ' '
                                    seq.append(string)
                                    copy.remove(j)
                                    break
                        seq.append('\n')
            result_name = './B07901103/' + 'result_' + str(prob)[2:] + '_' + str(delta)[2:].ljust(3, '0') + '.txt'
            with open(result_name, 'w') as result_file:
                result_file.writelines(seq)

#########################################################################################
#                                        main                                           #                        
#########################################################################################
if __name__ == '__main__':
	main()