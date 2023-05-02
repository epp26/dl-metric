#!/usr/bin/python3

import argparse

import csv 

def parse_args():
    
    parser = argparse.ArgumentParser(description="Creates Evaluation Metrics")
    parser.add_argument("input_option", choices=["git", "dv8", "csv"], help='The input option to use')
    parser.add_argument("--file-change-file", help='The filename of the all-file-change-cost.csv')
    parser.add_argument("--commit-change-file", help='The filename of the all-commits-change-cost.csv')
    parser.add_argument("--tag", help='The tag to process', default='')
    parser.add_argument("--repo-path", help='The path to the repo to process', default='')
    parser.add_argument("--test", help='Run test code as well as normal processing', default=False, action='store_true')
    parser.add_argument("--csv-output", help='File used for outputting committer, commit, and file tuple', default='output.csv')
    parser.add_argument("--csv-input", help='File used for inputting committer, commit, and file tuple', default='input.csv')
    args = parser.parse_args()
    return args

def process_dv8_files(commit_change_file, file_change_file):
   
    if not commit_change_file: 
        print("dv8 Option requires --commit_change_file option")
        exit(-1)
    if not file_change_file:
        print("dv8 Option requires --file_change_file option")
        exit(-1)

    from collections import defaultdict
    commit_to_file_set = defaultdict(set)
    committer_to_commit_set = defaultdict(set)
#    all_files = set()

    with open(file_change_file, newline='') as file_csv:
        file_data = csv.DictReader(file_csv)
        for row in file_data:
#            print(row)
            commit_to_file_set[row['CommitId']].add(row['FileName'])
#            all_files.add(row['FileName'])
#           debug.add(' '.join(row.keys()))

#    size_of_commits = [len(commit_to_file_set[x]) for x in commit_to_file_set.keys()]
#    print(sum(size_of_commits))
#    print(len(all_files))
#    commit_overlap_ratio = sum(size_of_commits)/len(all_files)
#    print(commit_overlap_ratio)

    with open(commit_change_file, newline='') as commits_csv:
        commit_data = csv.DictReader(commits_csv)
        for row in commit_data:
#            print(row)
            committer_to_commit_set[row['Committer']].add(row['CommitId'])
#            all_files.add(row['FileName'])
#           debug.add(' '.join(row.keys()))

    return committer_to_commit_set, commit_to_file_set

def calculate_metrics(committer_to_commit_set, commit_to_file_set):

    commit_overlap_ratio = calculate_cor_metric(commit_to_file_set)
#   print("commit_overlap_ratio ", commit_overlap_ratio)
    commit_fileset_overlap_ratio = calculate_cfor_metric(commit_to_file_set, committer_to_commit_set)
#   print("commit_fileset_overlap_ratio", commit_fileset_overlap_ratio)
    pairwise_committer_overlap = calculate_pco_metric(commit_to_file_set, committer_to_commit_set)
#   print("pairwise_committer_overlap", pairwise_committer_overlap)
    return commit_overlap_ratio, commit_fileset_overlap_ratio, pairwise_committer_overlap


def calculate_cor_metric(commit_to_file_set):
    all_file_set = set()
    size_of_each_commit = [len(x) for x in commit_to_file_set.values()]
#   all_file_set = set(tuple(x) for x in commit_to_file_set.values())
#   all_file_set.update(x) for x in commit_to_file_set.values()
    for file_set in commit_to_file_set.values():
        all_file_set.update(file_set)
    
#   print(sum(size_of_each_commit))
#   print(len(all_file_set))
    number_of_files = len(all_file_set)
    commit_overlap_ratio = 0
    if number_of_files:
        commit_overlap_ratio = sum(size_of_each_commit)/number_of_files
#   print(commit_overlap_ratio)
    return commit_overlap_ratio
        
def calculate_cfor_metric(commit_to_file_set, committer_to_commit_set):
    
    from collections import defaultdict
    files_per_committer = defaultdict(set)
    all_file_set = set()
    for committer, commit_set in committer_to_commit_set.items():
        for commit in commit_set:
            files_per_committer[committer].update(commit_to_file_set[commit])
            all_file_set.update(commit_to_file_set[commit])

#   for committer, files in files_per_committer.items():
#       print(committer, len(files))

    file_counts = [len(files) for files in files_per_committer.values()]
#   print(sum(file_counts))
#   print(len(all_file_set))
    number_of_files = len(all_file_set)
    commit_fileset_overlap_ratio = 0
    if number_of_files:
        commit_fileset_overlap_ratio = sum(file_counts)/len(all_file_set)
    return commit_fileset_overlap_ratio

def calculate_pco_metric(commit_to_file_set, committer_to_commit_set):

    from collections import defaultdict
    files_per_committer = defaultdict(set)
    all_file_set = set()
#   print("Committers set: ", committer_to_commit_set)
    for committer, commit_set in committer_to_commit_set.items():
        for commit in commit_set:
            files_per_committer[committer].update(commit_to_file_set[commit])
            all_file_set.update(commit_to_file_set[commit])

#   print("files per committer: ", files_per_committer)
    committer_overlap_map = defaultdict(float)
    for committer_i, files_i in files_per_committer.items():
        for committer_j, files_j in files_per_committer.items():
            if (committer_i != committer_j):
                number_of_union_files = len(files_i.union(files_j))
                if number_of_union_files:
                    committer_overlap_map[committer_i] += (len(files_i.intersection(files_j))/number_of_union_files)

#   print("Commiter Overlap: ", committer_overlap_map)
#   for committer, value in committer_overlap_map.items():
#       print(committer, value)

    if committer_overlap_map:
        from statistics import mean
        pairwise_committer_overlap = mean(committer_overlap_map.values())
#       print(pairwise_committer_overlap)
    else:
        pairwise_committer_overlap = 0

    return pairwise_committer_overlap

def output_csv_file(committer_to_commit_set, commit_to_file_set, csv_filename):

    import csv
    with open(csv_filename, 'w', newline='') as csv_file:
        field_names = ['committer', 'commit', 'file']
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writeheader()
        for committer, commits in committer_to_commit_set.items():
            for commit in commits:
                for filename in commit_to_file_set[commit]:
                    writer.writerow({'committer':committer, 'commit':commit, 'file':filename})


def determine_tag_list(possible_tag_list, repo_path):
    tag_list = possible_tag_list
    if not possible_tag_list:
        import subprocess
        process = subprocess.Popen(['git', 'tag', '--sort=creatordate'], cwd=repo_path, stdout=subprocess.PIPE)
        output = process.communicate()[0].decode()
#       print("output", output.split())
        tag_list = output.split()

    return tag_list


def determine_committer_map(tag1, tag2, repo_path):
    import subprocess
    tags_string = tag1 + ".." + tag2
    process = subprocess.Popen(['git', 'log', '--pretty=format:\'%cn, %H\'', tags_string], cwd=repo_path, stdout=subprocess.PIPE)
    output = process.communicate()[0].decode()
    from collections import defaultdict
    committer_map = defaultdict(set)
    for data_string in output.split('\n'):
        committer_map[data_string.split(',')[0]].add(data_string.split(',')[1])
#   print("data", committer_map)
    return committer_map


def determine_commit_map(commit_list, repo_path):
    import subprocess
    from collections import defaultdict
    commit_map = defaultdict(set)
    for commit in commit_list:
        commit_value = commit.split('\'')[0].strip()
#       print("c:", commit_value)
        process = subprocess.Popen(['git', 'diff-tree', '--no-commit-id', '--name-only', '-r', commit_value], cwd=repo_path, stdout=subprocess.PIPE)
        output = process.communicate()[0].decode()
#       print("out:", output)
        commit_map[commit].update(output.strip().split('\n'))
#       for filename in output.strip().split('\n'):
#           print("filename:", filename)
#           commit_map[commit].add(filename)
#       return 0
#   print("data", commit_map)

    return commit_map

def calculate_maps_using_git( tag, repo_path, print_debug=False):
    if print_debug:
        print("Processing tag ", tag, "repo: ", repo_path)
    if not tag:
        print("--tag option is required for git")
    if not repo_path:
        print("--repo-path option is required for git")

    import subprocess
    if print_debug:
        print(['git', 'log', tag.strip(), '--no-renames', '--no-color-moved', '--pretty=format:%ce,%H', '--name-only'])
    process = subprocess.Popen(['git', 'log', tag.strip(), '--no-renames', '--no-color-moved', '--pretty=format:%ce,%H', '--name-only'], cwd=repo_path, stdout=subprocess.PIPE)
    output = process.communicate()[0].decode()

#    print("output: ", output)
    from collections import defaultdict
    committer_map = defaultdict(set)
    commit_map = defaultdict(set)
    committer = "RESET"
    commit = "RESET"

    for line in output.splitlines():
        line_split = line.split(',')
        if line == "":
            committer = "RESET"
            commit = "RESET"
        elif len(line_split) == 2:
            committer = line_split[0]
            commit = line_split[1]
 #           print("Committer: ", committer, " commit: ", commit)
            committer_map[committer].add(commit)
        else:
            filename = line
            commit_map[commit].add(filename)
        
#   print("data", committer_map, commit_map)
    return committer_map, commit_map
    

def test():

    from collections import defaultdict
    test_committer_to_commit_set = defaultdict(set)
    test_committer_to_commit_set["p1"] = set(["c1"])
    test_committer_to_commit_set["p2"] = set(["c2"])
    test_committer_to_commit_set["p3"] = set(["c3"])

    test_commit_to_file_set1 = defaultdict(set)
    test_commit_to_file_set1["c1"] = set(["f1", "f2"])
    test_commit_to_file_set1["c2"] = set(["f3", "f4"])
    test_commit_to_file_set1["c3"] = set(["f5", "f6"])
    print("test cor1:", calculate_cor_metric(test_commit_to_file_set1))
    print("test cfor1:", calculate_cfor_metric(test_commit_to_file_set1, test_committer_to_commit_set))
    print("test pco1:", calculate_pco_metric(test_commit_to_file_set1, test_committer_to_commit_set))

    test_commit_to_file_set2 = defaultdict(set)
    test_commit_to_file_set2["c1"] = set(["f1", "f2"])
    test_commit_to_file_set2["c2"] = set(["f2", "f3"])
    test_commit_to_file_set2["c3"] = set(["f3", "f4"])
    print("test cor2:", calculate_cor_metric(test_commit_to_file_set2))
    print("test cfor2:", calculate_cfor_metric(test_commit_to_file_set2, test_committer_to_commit_set))
    print("test pco2:", calculate_pco_metric(test_commit_to_file_set2, test_committer_to_commit_set))

    test_commit_to_file_set3 = defaultdict(set)
    test_commit_to_file_set3["c1"] = set(["f1", "f2"])
    test_commit_to_file_set3["c2"] = set(["f2", "f3"])
    test_commit_to_file_set3["c3"] = set(["f3", "f1"])
    print("test cor3:", calculate_cor_metric(test_commit_to_file_set3))
    print("test cfor3:", calculate_cfor_metric(test_commit_to_file_set3, test_committer_to_commit_set))
    print("test pco3:", calculate_pco_metric(test_commit_to_file_set3, test_committer_to_commit_set))

    test_commit_to_file_set4 = defaultdict(set)
    test_commit_to_file_set4["c1"] = set(["f1", "f2", "f3"])
    test_commit_to_file_set4["c2"] = set(["f1", "f2", "f3"])
    test_commit_to_file_set4["c3"] = set(["f1", "f2", "f3"])
    print("test cor4:", calculate_cor_metric(test_commit_to_file_set4))
    print("test cfor4:", calculate_cfor_metric(test_commit_to_file_set4, test_committer_to_commit_set))
    print("test pco4:", calculate_pco_metric(test_commit_to_file_set4, test_committer_to_commit_set))

    print("Test determine_tag_list")
    print("empty tagList:", determine_tag_list([], '/home/ernstpisch/repos/depends/depends'))
    print("tagList:", determine_tag_list(["test1", "test2", "test3"], '/home/ernstpisch/repos/depends/depends'))

#   committers_to_commits = determine_committer_map("0.9.3a", "0.9.3c",  '/home/ernstpisch/repos/depends/depends')
#   print("committers:", committers_to_commits)

#   commit_list = next(iter(committers_to_commits.values()))
#   print("CL:", commit_list)
#   print("commits:", determine_commit_map(commit_list, '/home/ernstpisch/repos/depends/depends'))
    
    output_csv_file(test_committer_to_commit_set, test_commit_to_file_set1, './test_output.csv')
    return 0

def gather_inputs(args):
#   print("args: ", args)
    if args.input_option == "dv8":
        committers, commits = process_dv8_files(args.commit_change_file, args.file_change_file)
    elif args.input_option == "git":
        committers, commits = calculate_maps_using_git(args.tag, args.repo_path)
    elif args.input_option == "csv":
        committers, commits = process_csv_files(args.csv_input)
    else:
        print("ERROR!!!")
    return committers, commits
        

if __name__ == '__main__':
    args = parse_args()
    committers_map, commits_map = gather_inputs(args)
    
    output_csv_file(committers_map, commits_map, args.csv_output)

    cor, cfor, pco = calculate_metrics(committers_map, commits_map)
    print("commit_overlap_ratio ", cor)
    print("commit_fileset_overlap_ratio", cfor)
    print("pairwise_committer_overlap", pco)

    if args.test:
        test()



