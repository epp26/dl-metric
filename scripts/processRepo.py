#!/usr/bin/python3

import argparse

import csv 

def parse_args():
    
    parser = argparse.ArgumentParser(description="Process a repo for Evaluation Metrics")
    parser.add_argument("--tag-order", help='The list of tags to process in order', nargs='+')
    parser.add_argument("--repo-path", help='The path to the repo to process', default='')
    parser.add_argument("--test", help='Run test code as well as normal processing', default=False, action='store_true')
    parser.add_argument("--csv-output", help='File used for outputting committer, commit, and file tuple', default='output.csv')
    args = parser.parse_args()
    return args

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


def determine_tag_list(repo_path):
    import subprocess
    process = subprocess.Popen(['git', 'tag', '--sort=creatordate'], cwd=repo_path, stdout=subprocess.PIPE)
    output = process.communicate()[0].decode()
#   print("output", output.split())
    tag_list = [tag.strip() for tag in output.split()]

    return tag_list



def test():

    print("Test determine_tag_list: ", determine_tag_list('/home/ernstpisch/repos/depends/depends'))

    return 0

def process_repo(tag_list, repo_path, print_debug=False):
    import createEvalMetrics

    metrics = []
    for tag in tag_list:
        committers_map, commits_map = createEvalMetrics.calculate_maps_using_git(tag, repo_path, print_debug)
#        output_csv_file(committers_map, commits_map, args.csv_output)
        cor, cfor, pco = createEvalMetrics.calculate_metrics(committers_map, commits_map)
        metrics.append((cor, cfor, pco))
    return metrics

def add_to_csv(writer, repo_path, tag_list, metrics_list):
    repo_name = repo_path.split('/')[-1]
    for tag, metrics in zip(tag_list, metrics_list):
        writer.writerow({'repo':repo_name, 'tag':tag, 'cor':metrics[0], 'cfor':metrics[1], 'pco':metrics[2]})



def process_all_repos():
    
    import csv
    with open('repo_metrics.csv', 'w', newline='') as csv_file:
        field_names = ['repo', 'tag', 'cor', 'cfor', 'pco']
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writeheader()

        depends_repo = '/home/ernstpisch/repos/depends/depends'
        tags = determine_tag_list(depends_repo)
        metrics = process_repo(tags,depends_repo)
#       print(depends_repo, "metrics: ", metrics, "\n")
        add_to_csv(writer, depends_repo, tags, metrics) 

        repo = '/home/ernstpisch/repos/avro/avro'
        tags = determine_tag_list(repo)
        metrics = process_repo(tags,repo)
        add_to_csv(writer, repo, tags, metrics)
#       print(repo, "metrics: ", metrics, "\n")
        
        pig_release_tags = ["release-0.1.0", "release-0.1.1-rc1", "release-0.1.1", "release-0.2.0-rc0", "release-0.2.0-rc1", "release-0.2.0", "release-0.3.0", "release-0.4.0-rc0", "release-0.4.0", "release-0.5.0", "release-0.6.0-rc0", "release-0.6.0", "release-0.7.0", "release-0.8.0", "release-0.8.1-rc0", "release-0.8.1", "release-0.9.0-rc0", "release-0.9.0-rc1", "release-0.9.0", "release-0.9.1-rc0", "release-0.9.1-rc1", "release-0.9.1", "release-0.9.2-rc0", "release-0.9.2-rc1", "release-0.9.2", "release-0.10.0-rc0", "release-0.10.0.new", "release-0.10.0", "release-0.10.1-rc0", "release-0.10.1-rc1", "release-0.10.1", "release-0.11.0-rc0", "release-0.11.0-rc1", "release-0.11.0-rc2", "release-0.11.0", "release-0.11.1-rc0", "release-0.11.1", "release-0.12.0-rc0", "release-0.12.0-rc1", "release-0.12.0-rc2", "release-0.12.0", "release-0.12.1-rc0", "release-0.12.1", "release-0.13.0-rc0", "release-0.13.0", "release-0.14.0-rc0", "release-0.14.0-rc1", "release-0.14.0", "release-0.15.0-rc0", "release-0.15.0-rc1", "release-0.15.0", "release-0.16.0-rc0", "release-0.16.0", "release-0.17.0-rc0", "release-0.17.0"]
        
        repo = '/home/ernstpisch/repos/pig/pig'
        metrics = process_repo(pig_release_tags, repo, False)
        add_to_csv(writer, repo, pig_release_tags, metrics)
#       print(repo, "metrics: ", metrics, "\n")

if __name__ == '__main__':
    args = parse_args()

    if args.test:
        test()
        metrics = process_repo(args.tag_order, args.repo_path)
        print("metrics: ", metrics)
    else:
        process_all_repos()


