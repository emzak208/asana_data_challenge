library(tidyverse)
library(lubridate)


REPO_PATH <- "/Users/eric/Documents/asana_challenge"
ADOPTION_PATH <- "./data/adoption.csv"
ENGAGEMENT_PATH <- "./data/takehome_user_engagement-intern.csv"
USERS_PATH <- "./data/takehome_users-intern.csv"


#' Read data.
setwd(REPO_PATH)
engagement_raw <- readr::read_csv(ENGAGEMENT_PATH)
users_raw <- readr::read_csv(USERS_PATH)
adoption_raw <- readr::read_csv(ADOPTION_PATH)


#' Clean and format data.
engagement <- engagement_raw %>% 
  mutate(time_stamp = ymd_hms(time_stamp),
         date = date(time_stamp))

users <- users_raw %>% 
  rename(user_id = object_id) %>%
  mutate(creation_date = as_date(creation_time))

adoption <- adoption_raw %>% 
  select(user_id, date)


#' Feature engineering.

# Might be an ideal time window for engaging
first_engagement <- engagement %>%
  group_by(user_id) %>%
  summarise(first_engagement = min(date))

top_emails <- users$email_domain %>% 
  table() %>% 
  sort(decreasing=T) %>% 
  head(6) %>%  # Big dropoff after the first 6 email domains
  names()

# There's probably a cohesion effect with adoption
org_users <- users %>% 
  group_by(org_id) %>% 
  summarise(org_num_users = n())  # Tempting to look at # of adopted users, but that'd introduce leakage


user_features <- users %>%
  select(-name, -email, -last_session_creation_time) %>% 
  # Response variable
  mutate(is_adopted = ifelse(user_id %in% adoption$user_id, 1, 0)) %>%
  # Time features
  left_join(rename(adoption, adoption_date = date), by = "user_id") %>% 
  left_join(first_engagement, by = "user_id") %>% 
  mutate(creation_time = ymd_hms(creation_time),
         creation_date = date(creation_time),
         creation_year = year(creation_time),
         creation_month = month(creation_time),
         creation_day_of_week = weekdays(creation_time) %>% as.factor(),
         days_between_creation_firstuse = first_engagement - creation_date) %>% 
  select(-creation_time) %>% 
  # Categorical features
  mutate(creation_source = creation_source %>% as.factor(),
         email_domain = purrr::map_chr(email_domain, function(x) if (x %in% top_emails) x else "other") %>% as.factor(),
         invited_by_adopted = ifelse(invited_by_user_id %in% adoption$user_id, 1, 0)) %>% 
  # Other features
  left_join(org_users, by = "org_id") %>% 
  mutate(org_id = org_id %>% as.factor())

str(user_features)
