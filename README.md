# Replication Package for ESEC/FSE 2023 Paper "How Early Participation Determines Long-Term Sustained Activity in GitHub Projects?"

This replication package can be used for replicating results in the paper. It contains 1) a dataset of 290,255 repositories; and 2) Python scripts for training and interpreting models. 

<!-- Table of Contents -->
- [Required Environment](https://github.com/anonpros/Sustainable_projects/blob/main/README.md#Required_Environment)
- [Files and Replicating Results](https://github.com/anonpros/Sustainable_projects/blob/main/README.md#Files_and_Replicating_Results)
- [Variables](https://github.com/anonpros/Sustainable_projects/blob/main/README.md#Variables)
- [Examples of Variable Effects on Project Sustainability](https://github.com/anonpros/Sustainable_projects/blob/main/README.md#Examples_of_Variable_Effects_on_Project_Sustainability)
- [Model Hyperparameters](https://github.com/anonpros/Sustainable_projects/blob/main/README.md#Model_Hyperparameters)

## Required_Environment

We recommend manually setup the required environment in a commodity Linux machine with at least 1 CPU Core, 8GB Memory and 100GB empty storage space. We conduct development and execute all our experiments on a Ubuntu 20.04 server with two Intel Xeon Gold CPUs, 320GB memory, and 36TB RAID 5 Storage.

## Files_and_Replicating_Results

We use GHTorrent to restore historical states of 290,255 repositories with more than 57 commits, 4 PRs, 1 issue, 1 fork and 2 stars. Because the data is too large for git, please download data file separately from [Zenodo](https://zenodo.org/record/8098994) and put it under `Replication Package/`. The raw data of repositories (collected in their first 1,3,5 months(s)) are stored in `Replication Package/data/prodata_1.pkl`, `Replication Package/data/prodata_3.pkl`, and `Replication Package/data/prodata_5.pkl`. The contribution of features resulting from LIME model is stored in `Replication Package/data/limeres_m3_t2_k1.pkl`.
`Replication Package/data/X_test_m3_t2_k1.pkl` and `Replication Package/data/y_test_m3_t2_k1.pkl` store the test dataset for the LIME model. You can run `Replication Package/fitdata.py` to get the results in Table 3 and 4, run `Replication Package/draw_compare_variable.py` to get Figure 2 and run `Replication Package/allvari_statistics.py` to get Table 5. In `Replication Package/Variable_comparison_with_different_parameter.pdf`, we show the LIME results under different parameters. In `Replication Package/sample_pros.csv`, we also provide the list of randomly selected repositories in Section 3.1.

## Variables
GHTorrent records events such as making commits, reporting issues, commenting on issues, following a developer, and starring a project, along with information on the operator of the events, the occurring time of the events, and IDs of related developers/projects. We can restore the historical data of any project using this information.

Before getting the variables of a project, we need to identify its core developers, peripheral developers, and non-code contributors in the first m(1/3/5) months. This is done by the following steps:
  1. Fetch a project ID from the set of identified projects;
  2. Get the creating timestamp of the first commit of the project, which will be considered as its creating time T_start;
  3. Collect the operator IDs of events including making commits, reporting issues, and commenting on issues/PRs in the first m(1/3/5) months;
  4. Identify the user IDs of core developers, peripheral developers, and non-code contributors. 

After identifying the participants, the following variables can be obtained:

### Willingness of Participants

#### #cmt_{c|p}

- Definition: The average number of commits for core/peripheral developers.
- How to Collect Data:
  1. Use the user ID of all core/peripheral developers and the project ID to retrieve all commit events made by the core/peripheral developers in the first m months of the project;
  2. Calculate the average number of commits made by core/peripheral developers.

#### #pr_{c|p}

- Definition: The average number of pull requests for core/peripheral developers.
- How to Collect Data:
  1. Use the user ID of all core/peripheral developers and the project ID to retrieve all pull requests events made by the core/peripheral developers in the first m months of the project;
  2. Calculate the average number of pull requests for core/peripheral developers.

#### #issue_{c|p|n}

- Definition: The average number of reported issues for core developers/peripheral developers/non-code contributors.
- How to Collect Data:
  1. Use the user ID of all core/peripheral developers and the project ID to retrieve all issue reporting events made by the core/peripheral developers in the first m months of the project;
  2. Calculate the average number of reported issues for core developers/peripheral developers/non-code contributors.
 
#### #issue_comment_{c|p|n}

- Definition: The average number of issue comments for core developers/peripheral developers/non-code contributors.
- How to Collect Data:
  1. Use the project ID to retrieve all issues created in the first m months of the project;
  2. For each issue, obtain the user IDs of issue commentators in the first m months of the project;
  3. Count the number of issue comments made by each core developer/peripheral developer/non-code contributor;
  4. Calculate the average number of issue comments for each type of developer.

#### #cmt_comment_{c|p|n}

- Definition: The average number of commit comments for core developers/peripheral developers/non-code contributors.
- How to Collect Data:
  1. Use the project ID to retrieve all commits contributed in the first m months of the project;
  2. For each issue, obtain the user IDs of commit commentators in the first m months of the project;
  3. Count the number of commit comments made by each core developer/peripheral developer/non-code contributor;
  4. Calculate the average number of commit comments for each type of developer.
 
#### #iss_event_{c|p|n}

- Definition: The average number of issue events for core developers/peripheral developers/non-code contributors.
- How to Collect Data:
  1. Use the project ID to retrieve all issues created in the first m months of the project;
  2. For each issue, obtain the user IDs of operators of corresponding issue events such as subscribing to the issue;
  3. Count the number of issue events made by each core developer/peripheral developer/non-code contributor;
  4. Calculate the average number of issue events for each type of developer.

#### #following_{c|p|n}

- Definition: The average number of followed developers for core developers/peripheral developers/non-code contributors.
- How to Collect Data:
  1. Use the user ID of all core developers/peripheral developers/non-code contributors to retrieve their records of following other developers before T_start+m(months);
  2. Count the number of followed developers for each core developer/peripheral developer/non-code contributor;
  3. Calculate the average number of followed developers for each type of developer.
  
#### #star_pro_{c|p|n}

- Definition: The average number of starred projects for core developers/peripheral developers/non-code contributors.
- How to Collect Data:
  1. Use the user ID of all core developers/peripheral developers/non-code contributors to retrieve their records of starred projects before T_start+m(months);
  2. Count the number of starred projects for each core developer/peripheral developer/non-code contributor;
  3. Calculate the average number of starred projects for each type of developer.
  
#### #cmt_actday
- Definition: The number of days with commit activity.
- How to Collect Data:
  1. Use the project ID to retrieve all commit events of the project before T_start+m(months);
  2. Calculate the number of unique days on which commit events occurred.

#### #cmt_median
- Definition: The median number of commits per day.
- How to Collect Data:
  1. Use the project ID to retrieve all commit events of the project before T_start+m(months);
  2. Calculate the median number of commits per day.
     
#### #cmt_front
- Definition: The number of commits in the first half of the observation period.
- How to Collect Data:
  1. Use the project ID to retrieve all commit events of the project and their timestamp before T_start+m(months);
  2. Calculate the midpoint timestamp of the observation period;
  3. Count the number of commits made before the midpoint timestamp.

#### #cmt_end
- Definition: The number of commits in the second half of the observation period.
- How to Collect Data:
  1. Use the project ID to retrieve all commit events of the project and their timestamp before T_start+m(months);
  2. Calculate the midpoint timestamp of the observation period;
  3. Count the number of commits made after the midpoint timestamp.

#### cmt_day_std
- Definition: The standard deviation of commits per day.
- How to Collect Data:
  1. Use the project ID to retrieve all commit events before T_start+m(months) made by the core/peripheral developers in the project;
  2. Calculate the standard deviation of the average number of commits per day.

#### cmt_dev_std
- Definition: The standard deviation of commits per code contributor.
- How to Collect Data:
  1. Use the user id of all core/peripheral developers and the project ID to retrieve all commit events before T_start+m(months) made by the core/peripheral developers in the project;
  2. Count the number of commits made by each code contributor;
  3. Calculate the standard deviation of the total number of commits made by each code contributor.
     
### Capacity of Participants

#### #cmt_all_{c|p|n}
- Definition: The average number of commits on GitHub.
- How to Collect Data:
  1. Use the user ID of all core developers/peripheral developers/non-code contributors to retrieve their commit events before T_start+m(months);
  2. Calculate the average number of commits made by core developers/peripheral developers/non-code contributors on GitHub.
     
#### #pr_all_{c|p|n}
- Definition: The average number of pull requests on GitHub.
- How to Collect Data:
  1. Use the user ID of all core developers/peripheral developers/non-code contributors to retrieve their pull requests before T_start+m(months);
  2. Calculate the average number of pull requests made by core developers/peripheral developers/non-code contributors on GitHub.

#### #issue_all_{c|p|n}
- Definition: The average number of reported issues on GitHub.
- How to Collect Data:
  1. Use the user ID of all core developers/peripheral developers/non-code contributors to retrieve the issues reported by them before T_start+m(months) by them;
  2. Calculate the average number of issues reported by core developers/peripheral developers/non-code contributors on GitHub.

#### #pro_{c|p|n}
- Definition: The average number of owned projects.
- How to Collect Data:
  1. Use the user ID of all core developers/peripheral developers/non-code contributors to retrieve the projects owned by them (i.e., where they are the project owners) and created before T_start+m(months);
  2. Calculate the average number of owned projects by core developers/peripheral developers/non-code contributors.

#### #pro_oneyear_{c|p|n}
- Definition: The average number of owned one-year sustained projects.
- How to Collect Data:
  1. Use the user ID of all core developers/peripheral developers/non-code contributors to retrieve the projects owned by them created before T_start+m(months) and lasted for more than one year before T_start+m(months);
  2. Calculate the average number of owned one-year sustained projects by core developers/peripheral developers/non-code contributors.

#### #pro_twoyear_{c|p|n}
- Definition: The average number of owned two-year sustained projects.
- How to Collect Data:
  1. Use the user ID of all core developers/peripheral developers/non-code contributors to retrieve the projects owned by them created before T_start+m(months) and lasted for more than two years before T_start+m(months);
  2. Calculate the average number of owned two-year sustained projects by core developers/peripheral developers/non-code contributors.
 
#### #follower_{c|p|n}
- Definition: The average number of followers.
- How to Collect Data:
  1. Use the user ID of all core developers/peripheral developers/non-code contributors to retrieve their records of being followed by other developers before T_start+m(months);
  2. Calculate the average number of followers for core developers/peripheral developers/non-code contributors.
     
### Opportunity

#### #iss_open
- Definition: The number of open issues m months after project creation.
- How to Collect Data:
  1. Use the project ID to retrieve all open issues at m months after project creation;
  2. Count the number of open issues.

#### iss_open_ratio
- Definition: The ratio of open issues m months after project creation.
- How to Collect Data:
  1. Use the project ID to retrieve all open issues and issues at m months after project creation;
  2. Calculate the ratio of open issues.

#### #GFI
- Definition: The number of “good first issues” m months after project creation.
- How to Collect Data:
  1. Use the project ID to retrieve all issues with the "good first issue" label at m months after project creation;
  2. Count the number of GFIs.
     
#### #line_readme
- Definition: The number of README.md lines.
- How to Collect Data:
  1. Search the commits that modified the README file before T_start+m(months) and retrieve the number of added/deleted lines;
  2. Calculate the number of README.md lines.

#### #line_contributing
- Definition: The number of CONTRIBUTING.md lines.
- How to Collect Data:
  1. Search the commits that modified the CONTRIBUTING.md file before T_start+m(months) and retrieve the number of added/deleted lines;
  2. Calculate the number of CONTRIBUTING.md lines.

### Control Variables

#### show_comp_{c|p|n}
- Definition: The ratio of core developers/peripheral developers/non-code contributors showing their affiliated companies/institutions.
- How to Collect Data:
  1. Use the user ID of all core developers/peripheral developers/non-code contributors to retrieve their company data;
  2. Calculate the number of core developers/peripheral developers/non-code contributors who have displayed their company/institutions affiliation;
  3. Calculate the total number of core developers/peripheral developers/non-code contributors;
  4. Calculate the ratio of core developers/peripheral developers/non-code contributors showing their affiliated companies/institutions.

#### #org_{c|p|n}
- Definition: The average number of GitHub organizations core developers/peripheral developers/non-code contributors belong to.
- How to Collect Data:
  1. Use the user ID of all core developers/peripheral developers/non-code contributors to retrieve the GitHub organizations they belong to;
  2. Calculate the total number of organizations that all core developers/peripheral developers/non-code contributors belong to;
  3. Calculate the total number of core developers/peripheral developers/non-code contributors;
  4. Calculate the average number of GitHub organizations that all core developers/peripheral developers/non-code contributors belong to.

#### type
- Definition: The type of project owner account (0: organization, 1: user).
- How to Collect Data:
  1. Use the project ID to retrieve the owner ID of the project;
  2. Get the type (organization, user) of the owner account.

#### #star
- Definition: The number of stars m months after project creation.
- How to Collect Data:
  1. Use the project ID to retrieve all star events to the project before T_start+m(months);
  2. Count the number of stars.

#### #fork
- Definition: The number of forks m months after project creation.
- How to Collect Data:
  1. Use the project ID to retrieve all fork events to the project before T_start+m(months);
  2. Count the number of forks.

#### #member
- Definition: The number of project members m months after project creation.
- How to Collect Data:
  1. Use the project ID to retrieve all "becoming member" events to the project before T_start+m(months);
  2. Count the number of members.

## Examples_of_Variable_Effects_on_Project_Sustainability

The following part contains examples demonstrating the effects of different variables on the sustainability of open source projects. Below, we discuss some of our findings based on these examples.

### Negative Effects

#### Submitting Issues (**#issue_{c|p|n}**) and Adding Comments to Commits (**#cmt_comment_{c|p|n}**)
Our interpretation is that too many early issues and too much interaction effort in code contributions may diverge participants’ attention, harming sustainability in the long term. Some projects have many open issues but fail to be sustainable. For example, around the time that the [randori-compiler](https://github.com/RandoriAS/randori-compiler/issues) project stopped commit activities, there were approximately 20 unsolved issues. The [slash-cms](https://github.com/wakdev/slash-cms/issues) project is another similar example. An example of **#cmt_comment_{c|p|n}** is the [phalcon-basics](https://github.com/35aa/phalcon-basics/commits/master) project, where some commits are discussed extensively which can cost much effort from developers.

#### Average Number of Followed Developers (**#following_{c|p}**) and Starred Projects (**#star_pro_{c|p}**), Number of Previous PRs (**#pr_all_{c|p|n}**), and Number of Owned Projects (**#pro_{c|p|n}**)
The broad interest of core and peripheral developers may limit their effort and willingness in one single project, harming its sustainability. PRs are often submitted to external projects and thus, indicate the developers’ capacity is distributed among many projects. Owning too many OSS projects may imply one’s haphazardness in creating projects that are often abandoned rapidly. For example, Winston is the developer who contributed the most code contributions to the [dasherize](https://github.com/jollygoodcode/dasherize) project, which was only developed for no more than half a year. He starred many projects, followed many developers, and owned many projects. His energy and time are spent on many projects, and creating PRs for multiple projects during that period.

### Positive Effects

#### Issue Discussions (**#iss_comment_{c|p|n}**)
Discussions usually clarify the problem and solution before issue solvers contribute, which reduces unnecessary effort. We found that many successful projects have extensive issue discussions. The [emscripten](https://github.com/emscripten-core/emscripten/issues) project and the [GalSim](https://github.com/GalSim-developers/GalSim/issues) project are two examples of sustainable projects that have many issue discussions in the initial phase.

#### Uneven Distribution of Workload Among Developers (**cmt_dev_std**)
This variable may indicate the presence of highly competent developers and several peripheral developers, who are often vital for the incubation of successful OSS. For example, nschonni contributed most of the code contributions in the early phase of the [wet-boew](https://github.com/wet-boew/wet-boew/commits/master?before=c107a1fbf1dcf15e0e9211106e5e08cfb263bdfe+5805&branch=master&qualified_name=refs%2Fheads%2Fmaster) project. Despite now other contributors making more code contributions than him, his effort in the early phase of the project was very beneficial for the long-term sustainability of the project.

#### Ratio of Open Issues (**iss_open_ratio**) and Number of Lines of CONTRIBUTING File (**#line_contributing**)
The positive effect of the ratio of open issues (**iss_open_ratio**) and the number of lines of CONTRIBUTING file (**#line_contributing**): One possible explanation is that projects with higher open issue ratios have a better chance of attracting new contributions. Besides, more detailed contribution guidelines can reduce barriers for newcomers to contribute. For example, the [chefspec](https://github.com/chefspec/chefspec) project is under development for several years, which provided a high ratio (>0.8) of open issues and detailed CONTRIBUTING file.

Projects with higher open issue ratios have a better chance of attracting new contributions. Additionally, more detailed contribution guidelines can reduce barriers for newcomers to contribute. For example, the [chefspec](https://github.com/chefspec/chefspec) project has been under development for several years and provided a high ratio (>0.8) of open issues and a detailed CONTRIBUTING file in the early phase.

#### Hosted Under an Organization (**type**), Number of Project Members (**#member**), and Ratio of Participants Showing Their Affiliated Companies/Institutions (**show_comp_{c|p|n}**)
These positive factors often signal a larger development team (e.g., hosted under an organization, members, affiliations), making them more likely to sustain. For example, the [puppetlabs-ntp](https://github.com/puppetlabs/puppetlabs-ntp) project and the [builder](https://github.com/pytorch/builder) project are hosted under an organizational account, have many members, and most (>90%) of their initial code contributors show their affiliations. They are actively developed for many years.

We hope that these examples can provide insights into the factors that affect the sustainability of open source projects.

## Model_Hyperparameters

### Logistic regression Model:
max_iter=10000

### Random forest model:
n_estimators=10, criterion='gini'

### XGBoost model:
use_label_encoder=False, eval_metric=['logloss','auc','error']
