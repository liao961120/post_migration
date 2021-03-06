---
title: "Wrapper of knitr::include_graphics to Handle URLs & PDF Outputs"
tags: ['R Markdown', 'R-bloggers']
---


Those who use `knitr::include_graphics()` frequently in their R Markdown files may discover some inconsistencies (from the user point of view) if the same Rmd is used for multiple output formats, especially when PDF (LaTeX) is involved.

The following code works fine for HTML outputs but fails when the outputs are PDFs:

1. ```r
   knitr::include_graphics('local.gif')
   ```

1. ```r
   knitr::include_graphics('https://commonmark.org/images/markdown-mark.png')
   ```

The first case is obvious since it's impossible to include a GIF in a PDF document. The second case may cause some users to scratch their heads: "Why can't I insert a PNG image in the PDF document?". The answer is that, for PDFs, `knitr::include_graphics()` only works for **local images** because `knitr::include_graphics` won't download the images for you, whereas for HTMLs, the images don't have to be downloaded (images can be sourced using HTML `img` tags).


To fix the problem that arise in the first case, one can use images that are compatible for both output formats, such as PNG or JPEG. Another solution is to include different figures for different output formats:

```r
if (knitr::is_html_output()) {
    knitr::include_graphics('local.gif')
} else {
    knitr::include_graphics('local.png')
}
```

To fix the problem that arise in the second case, one has to remember not to pass an URL as `path` to `knitr::include_graphics()` if the Rmd is to be compiled to PDFs.


## include_graphics2()

I can never be sure when I would want to make my Rmd, originally targeted for HTML outputs, available in PDFs. Also, I don't want to write `if (knitr::is_html_output())` every time I want to include a GIF. It is also a headache to download every figure from the web just for the PDF output.
So I decided to write a wrapper of `knitr::include_graphics()` for myself, dealing with all the problems mentioned above. 


- For including different figures for HTML and PDF outputs, use:

  ```r
  include_graphics2('local.gif', 'local.png')
  ```

  The first argument `local.gif` is used when the output format is HTML, and the second, `local.png`, is used when it's PDF.


- `include_graphics2()` also works fine with URLs. It is totally fine to use URLs instead of local file paths in the example above:

  ```r
  png_url <- 'https://commonmark.org/images/markdown-mark.png'
  gif_url <- 'https://media.giphy.com/media/k3dcUPvxuNpK/giphy.gif'
  include_graphics2(png_url, gif_url)
  ```

### Source Code

I made `include_graphics2()` available through a package I maintain ([`lingusiticsdown`](https://liao961120.github.io/linguisticsdown)). You can read the
[documentation](https://liao961120.github.io/linguisticsdown/reference/include_graphics2.html) of `include_graphics2()` and a
[vignette](https://liao961120.github.io/linguisticsdown/articles/include_graphics_wrapper.html) of its usage on the package web page.


For those who want to use `include_graphics2()` but don't want to depend on `linguisticsdown`, feel free to copy the [source](https://github.com/liao961120/linguisticsdown/blob/master/R/include_graphics2.R) of `include_graphics2()` to your personal package. If you don't have one, you can still use the source script as regular R scripts, but remember to add the following lines to the top of the script:

```r
library(knitr)
library(tools)
```
