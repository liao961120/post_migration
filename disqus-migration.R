library(rvest)

baseURL <- 'https://yongfu.name'
baseURLold <- 'https://liao961120.github.io'

posts <- read_html('https://yongfu.name/post/')

new_posts <- posts %>% 
  html_nodes("li[data-date] a") %>%
  html_attr('href') %>% unique()

# Remove invalid links
new_posts <- sapply(new_posts, function(x) {
  url <- paste0(baseURL, x)
  resp <- httr::GET(url)
  if (resp$status == 404) return(NULL)
  return(x)
}, USE.NAMES = FALSE) %>% unlist()
new_posts <- new_posts[!is.null(new_posts)]
old_posts <- gsub("/$", ".html", new_posts)

old_custom <- c('/2018/01/31/RlearningPath.html', 
    '/2019/03/04/OriginsOfHumanCommunication.html',
    '/2019/08/15/secretOfOurSuccess.html',
    '/2020/02/22/leipzigVue.html',
    '/2017/12/11/Life_Tables.html')
new_custom <- tolower(old_custom) %>% 
  gsub(".html", "/", ., fixed = T)
old_posts <- c(old_posts, old_custom) %>% paste0(baseURLold, .)
new_posts <- c(new_posts, new_custom) %>% paste0(baseURL, .)

csv <- paste(old_posts, new_posts, sep = ", ") 
writeLines(paste0(csv, collapse = "\n"), "disqus.csv")
