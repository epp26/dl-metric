#!/usr/bin/python3

import argparse

import csv 

def parse_args():
    
    parser = argparse.ArgumentParser(description="Creates Evaluation Metrics")
#   parser.add_argument("input_option", choices=["git", "dv8", "csv"], help='The input option to use')
#   parser.add_argument("--file-change-file", help='The filename of the all-file-change-cost.csv')
#   parser.add_argument("--commit-change-file", help='The filename of the all-commits-change-cost.csv')
#   parser.add_argument("--tag-order", help='The list of tags to process in order', 
#       type=lambda s: [tag for tag in s.split(',')])
#   parser.add_argument("--tag1", help='The starting tag to process', default='0.9.3a')
#   parser.add_argument("--tag2", help='The ending tag to process', default='0.9.3c')
#   parser.add_argument("--repo-path", help='The path to the repo to process', default='')
#   parser.add_argument("--test", help='Run test code as well as normal processing', default=False, action='store_true')
#   parser.add_argument("--csv-output", help='File used for outputting committer, commit, and file tuple', default='output.csv')
#   parser.add_argument("--csv-input", help='File used for inputting committer, commit, and file tuple', default='input.csv')
    args = parser.parse_args()
    return args

#def process_by_repo_csv_files_bad(git_metric_file, dl_file):
#   
#    repo_to_release_to_dl_new_map = dict()
#    repo_to_release_to_dl_old_map = dict()
#    repo_to_release_to_cor_map = dict()
#    repo_to_release_to_cfor_map = dict()
#    repo_to_release_to_pco_map = dict()
#    repo_to_key_list = defaultdict(list)
#    repos_in_dict = set()
#
#    with open(dl_file, newline='') as dl_csv:
#        file_data = csv.DictReader(dl_csv)
#        for row in file_data:
##            print(row)
#            repo = row['repo']
#            tag = row['tag']
#            dl_old = row['dl_old']
#            dl = row['dl']
#            if repo in repos_in_dict:
#                repo_to_release_to_dl_new_map[repo][tag] = dl
#                repo_to_release_to_dl_old_map[repo][tag] = dl_old
#            else:
#                repos_in_dict.add(repo)
#                repo_to_release_to_dl_new_map[repo] = {}
#                repo_to_release_to_dl_new_map[repo][tag] = dl
#                repo_to_release_to_dl_old_map[repo] = {}
#                repo_to_release_to_dl_old_map[repo][tag] = dl_old
#
#    with open(git_metric_file, newline='') as git_csv:
#        file_data = csv.DictReader(git_csv)
#        for row in file_data:
##            print(row)
#            key = row['repo']+row['tag']
#            release_to_cor_map[key] = row['cor']
#            release_to_cfor_map[key] = row['cfor']
#            release_to_pco_map[key] = row['pco']
#
#    if release_to_cor_map.keys() == release_to_dl_old_map.keys():
#        dl_new_list = [float(release_to_dl_new_map[key]) for key in key_list]
#        dl_old_list = [float(release_to_dl_old_map[key]) for key in key_list]
#        cor_list = [float(release_to_cor_map[key]) for key in key_list]
#        cfor_list = [float(release_to_cfor_map[key]) for key in key_list]
#        pco_list = [float(release_to_pco_map[key]) for key in key_list]
##       dl_new_list = [float(release_to_dl_new_map[key]) for key in key_list]
##       dl_old_list = [float(release_to_dl_old_map[key]) for key in key_list]
##       cor_list = [float(release_to_cor_map[key]) if key in release_to_cor_map.keys() else 0 for key in key_list]
##       cfor_list = [float(release_to_cfor_map[key]) if key in release_to_cor_map.keys() else 0 for key in key_list]
##       pco_list = [float(release_to_pco_map[key]) if key in release_to_cor_map.keys() else 0 for key in key_list]
#
#        from scipy import stats
##       print("dl: ", dl_list, " cor: ", cor_list)
#        print("dl_new_cor: ", stats.pearsonr(dl_new_list, cor_list))
#        print("dl_new_cfor: ", stats.pearsonr(dl_new_list, cfor_list))
#        print("dl_new_pco: ", stats.pearsonr(dl_new_list, pco_list))
#        print("dl_old_cor: ", stats.pearsonr(dl_old_list, cor_list))
#        print("dl_old_cfor: ", stats.pearsonr(dl_old_list, cfor_list))
#        print("dl_old_pco: ", stats.pearsonr(dl_old_list, pco_list))
#        print("dl_old_dl: ", stats.pearsonr(dl_old_list, dl_new_list))
#    else:
#        print("Error!")
##       print("release cor keys: ", release_to_cor_map.keys(), " dl keys: ", release_to_dl_old_map.keys())
#        for x,y in zip(set(release_to_cor_map.keys()), set(release_to_dl_old_map.keys())):
#            if x != y:
#                print(" cor: ", x, " oldDL: ", y)
#                exit()

def process_by_repo_csv_files(git_metric_file, dl_file):
  
    import pandas as pd
    dl_file_data = pd.read_csv(dl_file)
    git_file_data = pd.read_csv(git_metric_file)
    merged_data = pd.merge(dl_file_data, git_file_data, on=['repo','tag'], how='inner')
#   print(merged_data)
    dl_data = merged_data.groupby('repo')['dl'].apply(list)
    dl_old_data = merged_data.groupby('repo')['dl_old'].apply(list)
    cor_data = merged_data.groupby('repo')['cor'].apply(list)
    cfor_data = merged_data.groupby('repo')['cfor'].apply(list)
    pco_data = merged_data.groupby('repo')['pco'].apply(list)
    repo_name = merged_data.groupby('repo')['repo'].apply(list)
    

#   print(len(dl_data))
#   print(len(dl_old_data))
#   print(len(cor_data))
#   print(len(cfor_data))
#   print(len(pco_data))
#   print(len(repo_name))
#   print(dl_data[0])

    from scipy import stats
    for i in range(len(repo_name)):
        print("For repo ", repo_name[i][0], ":")

        print("dl_new_cor: ", stats.pearsonr(dl_data[i], cor_data[i]))
        print("dl_new_cfor: ", stats.pearsonr(dl_data[i], cfor_data[i]))
        print("dl_new_pco: ", stats.pearsonr(dl_data[i], pco_data[i]))
        print("dl_old_cor: ", stats.pearsonr(dl_old_data[i], cor_data[i]))
        print("dl_old_cfor: ", stats.pearsonr(dl_old_data[i], cfor_data[i]))
        print("dl_old_pco: ", stats.pearsonr(dl_old_data[i], pco_data[i]))
        print("dl_old_dl: ", stats.pearsonr(dl_old_data[i], dl_data[i]))
       
    print("using log/log") 
    import numpy as np
    for i in range(len(repo_name)):
        print("For repo ", repo_name[i][0], ":")

        print("dl_new_cor: ", stats.pearsonr(np.log10(dl_data[i]), np.log10(cor_data[i])))
        print("dl_new_cfor: ", stats.pearsonr(np.log10(dl_data[i]), np.log10(cfor_data[i])))
        print("dl_new_pco: ", stats.pearsonr(np.log10(dl_data[i]), np.log10(pco_data[i])))
        print("dl_old_cor: ", stats.pearsonr(np.log10(dl_old_data[i]), np.log10(cor_data[i])))
        print("dl_old_cfor: ", stats.pearsonr(np.log10(dl_old_data[i]), np.log10(cfor_data[i])))
        print("dl_old_pco: ", stats.pearsonr(np.log10(dl_old_data[i]), np.log10(pco_data[i])))
        print("dl_old_dl: ", stats.pearsonr(np.log10(dl_old_data[i]), np.log10(dl_data[i])))
        

def process_csv_files(git_metric_file, dl_file):
   
    release_to_dl_new_map = dict()
    release_to_dl_old_map = dict()
    release_to_cor_map = dict()
    release_to_cfor_map = dict()
    release_to_pco_map = dict()
    key_list = []

    with open(dl_file, newline='') as dl_csv:
        file_data = csv.DictReader(dl_csv)
        for row in file_data:
#            print(row)
            key = row['repo']+row['tag']
            key_list.append(key)
            release_to_dl_new_map[key] = row['dl']
            release_to_dl_old_map[key] = row['dl_old']

    with open(git_metric_file, newline='') as git_csv:
        file_data = csv.DictReader(git_csv)
        for row in file_data:
#            print(row)
            key = row['repo']+row['tag']
            release_to_cor_map[key] = row['cor']
            release_to_cfor_map[key] = row['cfor']
            release_to_pco_map[key] = row['pco']

    if release_to_cor_map.keys() == release_to_dl_old_map.keys():
        dl_new_list = [float(release_to_dl_new_map[key]) for key in key_list]
        dl_old_list = [float(release_to_dl_old_map[key]) for key in key_list]
        cor_list = [float(release_to_cor_map[key]) for key in key_list]
        cfor_list = [float(release_to_cfor_map[key]) for key in key_list]
        pco_list = [float(release_to_pco_map[key]) for key in key_list]
#       dl_new_list = [float(release_to_dl_new_map[key]) for key in key_list]
#       dl_old_list = [float(release_to_dl_old_map[key]) for key in key_list]
#       cor_list = [float(release_to_cor_map[key]) if key in release_to_cor_map.keys() else 0 for key in key_list]
#       cfor_list = [float(release_to_cfor_map[key]) if key in release_to_cor_map.keys() else 0 for key in key_list]
#       pco_list = [float(release_to_pco_map[key]) if key in release_to_cor_map.keys() else 0 for key in key_list]

        from scipy import stats
#       print("dl: ", dl_list, " cor: ", cor_list)
        print("dl_new_cor: ", stats.pearsonr(dl_new_list, cor_list))
        print("dl_new_cfor: ", stats.pearsonr(dl_new_list, cfor_list))
        print("dl_new_pco: ", stats.pearsonr(dl_new_list, pco_list))
        print("dl_old_cor: ", stats.pearsonr(dl_old_list, cor_list))
        print("dl_old_cfor: ", stats.pearsonr(dl_old_list, cfor_list))
        print("dl_old_pco: ", stats.pearsonr(dl_old_list, pco_list))
        print("dl_old_dl: ", stats.pearsonr(dl_old_list, dl_new_list))
    else:
        print("Error!")
#       print("release cor keys: ", release_to_cor_map.keys(), " dl keys: ", release_to_dl_old_map.keys())
        for x,y in zip(set(release_to_cor_map.keys()), set(release_to_dl_old_map.keys())):
            if x != y:
                print(" cor: ", x, " oldDL: ", y)
                exit()
        

#def output_csv_file(committer_to_commit_set, commit_to_file_set, csv_filename):
#
#    import csv
#    with open(csv_filename, 'w', newline='') as csv_file:
#        field_names = ['committer', 'commit', 'file']
#        writer = csv.DictWriter(csv_file, fieldnames=field_names)
#        writer.writeheader()
#        for committer, commits in committer_to_commit_set.items():
#            for commit in commits:
#                for filename in commit_to_file_set[commit]:
#                    writer.writerow({'committer':committer, 'commit':commit, 'file':filename})
#


#def test():
#
#    from collections import defaultdict
#    test_committer_to_commit_set = defaultdict(set)
#    test_committer_to_commit_set["p1"] = set(["c1"])
#    test_committer_to_commit_set["p2"] = set(["c2"])
#    test_committer_to_commit_set["p3"] = set(["c3"])
#
#    test_commit_to_file_set1 = defaultdict(set)
#    test_commit_to_file_set1["c1"] = set(["f1", "f2"])
#    test_commit_to_file_set1["c2"] = set(["f3", "f4"])
#    test_commit_to_file_set1["c3"] = set(["f5", "f6"])
#    print("test cor1:", calculate_cor_metric(test_commit_to_file_set1))
#    print("test cfor1:", calculate_cfor_metric(test_commit_to_file_set1, test_committer_to_commit_set))
#    print("test pco1:", calculate_pco_metric(test_commit_to_file_set1, test_committer_to_commit_set))
#
#    test_commit_to_file_set2 = defaultdict(set)
#    test_commit_to_file_set2["c1"] = set(["f1", "f2"])
#    test_commit_to_file_set2["c2"] = set(["f2", "f3"])
#    test_commit_to_file_set2["c3"] = set(["f3", "f4"])
#    print("test cor2:", calculate_cor_metric(test_commit_to_file_set2))
#    print("test cfor2:", calculate_cfor_metric(test_commit_to_file_set2, test_committer_to_commit_set))
#    print("test pco2:", calculate_pco_metric(test_commit_to_file_set2, test_committer_to_commit_set))
#
#    test_commit_to_file_set3 = defaultdict(set)
#    test_commit_to_file_set3["c1"] = set(["f1", "f2"])
#    test_commit_to_file_set3["c2"] = set(["f2", "f3"])
#    test_commit_to_file_set3["c3"] = set(["f3", "f1"])
#    print("test cor3:", calculate_cor_metric(test_commit_to_file_set3))
#    print("test cfor3:", calculate_cfor_metric(test_commit_to_file_set3, test_committer_to_commit_set))
#    print("test pco3:", calculate_pco_metric(test_commit_to_file_set3, test_committer_to_commit_set))
#
#    test_commit_to_file_set4 = defaultdict(set)
#    test_commit_to_file_set4["c1"] = set(["f1", "f2", "f3"])
#    test_commit_to_file_set4["c2"] = set(["f1", "f2", "f3"])
#    test_commit_to_file_set4["c3"] = set(["f1", "f2", "f3"])
#    print("test cor4:", calculate_cor_metric(test_commit_to_file_set4))
#    print("test cfor4:", calculate_cfor_metric(test_commit_to_file_set4, test_committer_to_commit_set))
#    print("test pco4:", calculate_pco_metric(test_commit_to_file_set4, test_committer_to_commit_set))
#
#    print("Test determine_tag_list")
#    print("empty tagList:", determine_tag_list([], '/home/ernstpisch/repos/depends/depends'))
#    print("tagList:", determine_tag_list(["test1", "test2", "test3"], '/home/ernstpisch/repos/depends/depends'))
#
##   committers_to_commits = determine_committer_map("0.9.3a", "0.9.3c",  '/home/ernstpisch/repos/depends/depends')
##   print("committers:", committers_to_commits)
#
##   commit_list = next(iter(committers_to_commits.values()))
##   print("CL:", commit_list)
##   print("commits:", determine_commit_map(commit_list, '/home/ernstpisch/repos/depends/depends'))
#    
#    output_csv_file(test_committer_to_commit_set, test_commit_to_file_set1, './test_output.csv')
#    return 0

if __name__ == '__main__':
    args = parse_args()
    
#   process_csv_files("/home/ernstpisch/repos/dv8Output/csvFolder/depends/repo_metrics.csv", "/home/ernstpisch/repos/dv8Output/csvFolder/depends/old_new_dl.csv")
#   process_by_repo_csv_files("/home/ernstpisch/repos/dv8Output/csvFolder/depends/repo_metrics.csv", "/home/ernstpisch/repos/dv8Output/csvFolder/depends/old_new_dl.csv")
    process_by_repo_csv_files("./inputs/repo_metrics.csv", "./inputs/old_new_dl.csv")

#   print("commit_overlap_ratio ", cor)
#   print("commit_fileset_overlap_ratio", cfor)
#   print("pairwise_committer_overlap", pco)

#   if args.test:
#       test()



