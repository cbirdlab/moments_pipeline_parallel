# this script parses the raw output from the moments_pipeline_parallel max-likelihood search
# this is presently intended to be run interactively in R studio
# alt+o to collapse sections

# you need to define the `indir` below, see line 14

#### INITIALIZE ####
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))

setwd(shorterExistingWorkDir)
library(tidyverse)
library(janitor)
library(readr)
library(purrr)
library(ggbeeswarm)

#### USER DEFINED VARIABLES ####
indir <- "output_286_396"
indir <- "output_88_88"
indir <- "output_28_80"
indir <- "./2D_ml-search/output_54_158"

#### LOAD VARIABLES ####
file_names_optimized <- 
  list.files(indir,
             full.names=TRUE) %>%
  tibble() %>%
  rename(file_name = 1) %>%
  filter(str_detect(file_name, 
                    "optimized")) %>%
  pull()

#### FUNCTIONS ####
get_param_names <- function(inFILE){
  # param_names <-
    read_tsv(inFILE) %>%
    clean_names() %>% 
    colnames() %>%
    tibble() %>%
    rename(col_name = 1) %>%
    filter(str_detect(col_name, 
                      "optimized")) %>%
    mutate(col_names = str_remove(col_name,
                                  "optimized_params_"),
           col_names = str_replace_all(col_names,
                                       "_",
                                       ",")) %>%
    pull(col_names) %>%
    str_split(pattern = ",") %>%
    as_vector()
}

get_model_results <- function(inFILE){
  # data_summaries <-
  param_names <- 
    get_param_names(inFILE) 
  
  read_tsv(inFILE,
           na = c("",
                  "NA",
                  "nan",
                  "--")) %>%
    clean_names() %>% 
    #if there are multiple headers, remove additional
    filter(model != "Model") %>%
    #if there are identical rows, remove them, this is from multiple runs in same dir without deleting
    distinct() %>%
    mutate(summary_file_name = inFILE) %>%
    separate(7,
             into = param_names,
             sep = ",",
             remove = FALSE) %>%
    separate(replicate,
             into = c("round",
                      "replicate"),
             sep = "_Replicate_") %>%
    mutate(round = as_factor(str_remove(round,
                                         "Round_")),
           replicate = as_factor(replicate)) %>%
    arrange(model,
            desc(log_likelihood)) 
}

get_all_model_results <- function(inFILES){
  inFILES %>%
    purrr::map(get_model_results) %>%
    bind_rows() %>%
    select(model:theta,
           starts_with("nu"),
           starts_with("m"),
           starts_with("t"),
           contains("optimized_params"))
}

#### WRANGLE DATA OUTPUT ####
data <-
  get_all_model_results(file_names_optimized) %>%
  mutate(across(nu1:t3,
                ~ as.numeric(.)))

#### VISUALIZE DATA OUTPUT####

# maximum likelihood by model
data %>%
  filter(! is.na(chi_squared) & chi_squared >= 0,
         round == "4") %>%
  group_by(model) %>%
  summarize(max_log_likelihood = max(log_likelihood,
                                     na.rm=TRUE)) %>%
  
  ggplot(aes(x = model,
             y = max_log_likelihood,
             fill = max_log_likelihood)) +
  geom_col() +
  theme_classic() +
  theme(axis.text.x = element_text(angle = 45, vjust = 1, hjust=1)) 

# maximum likelihood by model and round
data %>%
  filter(! is.na(chi_squared) & chi_squared >= 0) %>%
  group_by(model,
           round) %>%
  summarize(max_log_likelihood = max(log_likelihood,
                                     na.rm=TRUE)) %>%
  
  ggplot(aes(y = round,
             x = max_log_likelihood,
             fill = max_log_likelihood)) +
  geom_col() +
  theme_classic() +
  theme(axis.text.x = element_text(angle = 45, vjust = 1, hjust=1)) +
  facet_grid(model ~ .,
             scales ="free_y")

# log likelihood by round and model
data %>%
  filter(! is.na(chi_squared) & chi_squared >= 0) %>%
  group_by(model,
           round) %>%
  mutate(median_ll = median(log_likelihood,
                            na.rm=TRUE)) %>% 
  
  ggplot(aes(x = model,
             y = log_likelihood,
             fill = median_ll)) +
  geom_boxplot() +
  theme_classic() +
  theme(axis.text.x = element_text(angle = 45, vjust = 1, hjust=1)) +
  facet_grid(round ~ .,
             scales ="free_y")

# narrow down to above average models
ll_cutoff <-
  data %>%
    filter(! is.na(chi_squared) & chi_squared >= 0) %>%
    mutate(model = factor(model)) %>%
    filter(round == 4) %>%
    group_by(model) %>%
    mutate(median_ll = median(log_likelihood,
                              na.rm=TRUE)) %>% 
    pull(median_ll) %>%
    unique() %>%
    median()

# boxplot log likelihood by model, 4th round
data %>%
  filter(! is.na(chi_squared) & chi_squared >= 0) %>%
  mutate(model = factor(model)) %>%
  filter(round == 4) %>%
  group_by(model) %>%
  mutate(median_ll = median(log_likelihood,
                        na.rm=TRUE)) %>% 
  filter(median_ll > ll_cutoff) %>%
  ggplot(aes(x = model,
             y = log_likelihood,
             fill = median_ll)) +
  geom_boxplot() +
  geom_beeswarm(color = "red") +
  theme_classic() +
  theme(axis.text.x = element_text(angle = 45, vjust = 1, hjust=1)) +
  facet_grid(round ~ .,
             scales ="free_y")

# aic of better performing models
data %>%
  filter(! is.na(chi_squared) & chi_squared >= 0) %>%
  mutate(model = factor(model)) %>%
  filter(round == 4) %>%
  group_by(model) %>%
  mutate(median_ll = median(log_likelihood,
                            na.rm=TRUE)) %>% 
  filter(median_ll > ll_cutoff) %>%  
  ggplot(aes(x = model,
             y = aic,
             fill = median_ll)) +
  geom_boxplot() +
  geom_beeswarm(color = "red") +
  theme_classic() +
  theme(axis.text.x = element_text(angle = 45, vjust = 1, hjust=1)) +
  facet_grid(round ~ .,
             scales ="free_y")

# theta of better performing models
data %>%
  filter(! is.na(chi_squared) & chi_squared >= 0) %>%
  mutate(model = factor(model)) %>%
  filter(round == 4) %>%
  group_by(model) %>%
  mutate(median_ll = median(log_likelihood,
                            na.rm=TRUE)) %>% 
  filter(median_ll > ll_cutoff) %>%  
  ggplot(aes(x = model,
             y = theta,
             fill = median_ll)) +
  geom_boxplot() +
  geom_beeswarm(color = "red") +
  theme_classic() +
  theme(axis.text.x = element_text(angle = 45, vjust = 1, hjust=1)) +
  facet_grid(round ~ .,
             scales ="free_y")

# missingness
data %>%
  filter(! is.na(chi_squared) & chi_squared >= 0) %>%
  group_by(model,
           round) %>%
  summarize(n = n()) %>%
  ggplot(aes(x = model,
             y = n)) +
  geom_col() +
  theme(axis.text.x = element_text(angle = 45, vjust = 1, hjust=1)) +
  labs(y = "Number of Successful Replicates") +
  facet_grid(round ~ .,
             scales ="free_y")

#### ####
best_model = "sec_contact_asym_mig"
all_na <- function(x) any(!is.na(x))

data_best_model <- 
  data %>%
  filter(round == 4,
         model == best_model) %>%
  select_if(all_na) 

# plots of parameter estimates
data_best_model %>%
  pivot_longer(cols = theta:t2,
               names_to = "parameter") %>%
  group_by(parameter) %>%
  ggplot(aes(x=parameter,
             y=value)) +
  geom_boxplot() +
  geom_beeswarm(aes(color = log_likelihood)) +
  theme_classic() +
  theme(axis.text.x = element_text(angle = 45, vjust = 1, hjust=1)) +
  facet_wrap(. ~ parameter,
             scales ="free")

data_best_model %>%
  pivot_longer(cols = theta:t2,
               names_to = "parameter") %>%
  group_by(parameter) %>%
  mutate(median = median(value,
                         na.rm=TRUE),
         min = min(value,
                   na.rm=TRUE),
         max = max(value,
                   na.rm=TRUE)) %>%
  select(model, parameter, median, max, min) %>%
  distinct()

data_best_model



#### BASIC CODE TO READ 1 FILE ####
# # get param names
# param_names <-
#   read_tsv(head(file_names_optimized,
#                 1)) %>%
#   clean_names() %>% 
#   colnames() %>%
#   tibble() %>%
#   rename(col_name = 1) %>%
#   filter(str_detect(col_name, 
#                     "optimized")) %>%
#   mutate(col_names = str_remove(col_name,
#                                 "optimized_params_"),
#          col_names = str_replace_all(col_names,
#                                  "_",
#                                  ",")) %>%
#   pull(col_names) %>%
#   str_split(pattern = ",") %>%
#   as_vector()
# 
# data_summaries <-
#   read_tsv(head(file_names_optimized,
#                 1)) %>%
#   clean_names() %>% 
#   mutate(summary_file_name = head(file_names_optimized,
#                                   1)) %>%
#   separate(7,
#            into = param_names,
#            sep = ",",
#            remove = FALSE) %>%
#   #if there are multiple headers, remove additional
#   filter(model != "Model") %>%
#   #if there are identical rows, remove them, this is from multiple runs in same dir without deleting
#   distinct() %>%
#   arrange(desc(log_likelihood))


