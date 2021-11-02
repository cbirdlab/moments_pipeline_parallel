#### INITIALIZE ####
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
library(tidyverse)
library(janitor)
library(readr)
library(purrr)

#### USER DEFINED VARIABLES ####
indir <- "output_286_396"
indir <- "output_88_88"

#### LOAD VARIABLES ####
file_names_optimized <- list.files(indir,
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

#### WRANGLE DATA ####
data <-
  get_all_model_results(file_names_optimized)

#### ####
data %>%
  filter(str_detect(replicate, 
                    "Round_4")) %>% view()

data %>%
  filter(str_detect(round, 
                    "4"),
         ! is.na(chi_squared) & chi_squared >= 0) %>%
  ggplot(aes(x = model,
              y = log_likelihood)) +
  geom_boxplot() +
  theme_classic() +
  theme(axis.text.x = element_text(angle = 45, vjust = 1, hjust=1))

data %>%
  filter(! is.na(chi_squared) & chi_squared >= 0) %>%
  group_by(model,
           round) %>%
  summarize(n = n()) %>%
  ggplot(aes(x = model,
             y = n)) +
  geom_col() +
  theme(axis.text.x = element_text(angle = 45, vjust = 1, hjust=1)) +
  facet_grid(round ~ .)

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


