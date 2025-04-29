#Clears memory
# rm(list = ls())
# Clears console
# cat("\014")

### Load libraries
library(dplyr)
library(tm)
library(stringr)
library(tidytext)
library(textstem)
library(tidyr)
library(syuzhet)

clean_reviews <- read.csv("https://raw.githubusercontent.com/Humayun002/museum-review-analysis/refs/heads/main/clean_reviews.csv")
View(clean_reviews)

clean_reviews <- clean_reviews %>%
  select(-Location.Name) %>%
  mutate(Id = row_number()) %>%
  select(Id, everything()) #move Id to the front

clean_text <- function(text) {
  text %>%
    tolower() %>% #make lowercase
    str_replace_all("[^[:alnum:] ]", " ") %>% #remove punctuation
    str_replace_all("[0-9]", " ") %>%#remove numbers
    str_squish() #remove whitespace
}

clean_reviews$Text <- sapply(clean_reviews$Text, clean_text)


#topics we want to focus on
keywords <- c("accessible", "audio guide", "bag check", "cleanliness", "collection", 
              "display", "exhibition", "gogh", "facilities", "price", "wait",
              "groups", "noise", "crowd", "security", "smell", "staff", 
              "temperature", "restroom")

#remove stopwords and tokenize
data("stop_words")
review_tokens <- clean_reviews %>%
  select(Text) %>%
  unnest_tokens(word, Text) %>%
  anti_join(stop_words, by = "word") %>%
  filter(word %in% keywords)

#count keywords
keyword_counts <- review_tokens %>%
  count(word, sort = TRUE)

ggplot(keyword_counts, aes(x = reorder(word, n), y = n, fill = word)) +
  geom_col(show.legend = FALSE) +
  coord_flip() +
  labs(
    title = "Mentions of Museum-Specific Topics in Reviews",
    x = "Keyword",
    y = "Count"
  ) +
  theme_minimal()

#show distribution of sentiment for each keyword
#get sentiments
clean_reviews$sentiment <- get_sentiment(clean_reviews$Text, method = "afinn")

# Initialize an empty list to store the keyword presence information
keyword_sentiment <- clean_reviews

# Loop through the keywords and create binary columns for each keyword
for (keyword in keywords) {
  keyword_sentiment <- keyword_sentiment %>%
    mutate(!!paste0(keyword, "_present") := str_detect(Text, fixed(keyword)))
}

keyword_sentiment <- keyword_sentiment %>%
  pivot_longer(cols = starts_with("accessible"):starts_with("restroom"), 
               names_to = "keyword", values_to = "present") %>%
  filter(present == TRUE) %>%
  select(Id, keyword, sentiment)


ggplot(keyword_sentiment, aes(x = keyword, y = sentiment, fill = keyword)) +
  geom_boxplot() +
  labs(
    title = "Sentiment Distribution by Keyword",
    x = "Keyword",
    y = "Sentiment Score"
  ) +
  theme_minimal() +
  coord_flip()  # Flip axes for better readability