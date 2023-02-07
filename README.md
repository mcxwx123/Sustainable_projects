# Replication Package for Paper "How Early Participation Determines Long-Term Sustained Activity in GitHub Projects"

This replication package can be used for replicating results in the paper. It contains 1) a dataset of 290,255 repositories; and 2) Python scripts for training and interpreting models. 

## Required Environment

We recommend manually setup the required environment in a commodity Linux machine with at least 1 CPU Core, 8GB Memory and 100GB empty storage space. We conduct development and execute all our experiments on a Ubuntu 20.04 server with two Intel Xeon Gold CPUs, 320GB memory, and 36TB RAID 5 Storage.

## Files and Replicating Results

We use GHTorrent to restore historical states of 290,255 repositories with more than 57 commits, 4 PRs, 1 issue, 1 fork and 2 stars. Because the data is too large for git, please download data file separately from [Zenodo](https://zenodo.org/record/7613817#.Y-HA5-xBwlI) and put it under `Replication Package/`. We will provide the Zenodo link in the paper upon acceptance. The raw data of repositories (collected in their first 1,3,5 months(s)) are stored in `Replication Package/data/prodata_1.pkl`, `Replication Package/data/prodata_3.pkl`, and `Replication Package/data/prodata_5.pkl`. The contribution of features resulting from LIME model is stored in `Replication Package/data/limeres_m3_t2_k1.pkl`.
`Replication Package/data/X_test_m3_t2_k1.pkl` and `Replication Package/data/y_test_m3_t2_k1.pkl` store the test dataset for the LIME model. You can run `Replication Package/fitdata.py` to get the results in Table 2 and 3, run `Replication Package/draw_compare_variable.py` to get Figure 2 and run `Replication Package/allvari_statistics.py` to get Table 4. In `Replication Package/Variable_comparison_with_different_parameter.pdf`, we show the LIME results under different parameters. In `Replication Package/sample_pros.csv`, we also provide the list of randomly selected repositories in Section 3.1.
