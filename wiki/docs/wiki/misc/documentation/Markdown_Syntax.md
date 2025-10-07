<!-- How to add inpage css<link rel="stylesheet" href="../stylesheets/custom.css">-->
# Introduction 
This page documents the markdown syntax supported and used in this wiki implementation.

### Formatting Sentences

Sentence structure can be solved in a number of ways seen below.

``` title="Paragraph layout"
Putting a sentence simply on the next line will not make a new paragraph.
This sentence will attached to the last.

Instead put a space line between the last line to denote a new paragraph. 
```

<div class="result" markdown>

Putting a sentence simply on the next line will not make a new paragraph.
This sentence will attached to the last.

Instead put a space line between the last line to denote a new paragraph. 

</div>


``` title="Line break layout"
Putting a sentence simply on the next line will not make a new line.
This sentence will attached to the last.

To instead add a new line, end the line with two or more spaces.  
There are two spaces after the last line.
```

<div class="result" markdown>

Putting a sentence simply on the next line will not make a new line.
This sentence will attached to the last.

To instead add a new line, end the line with two or more spaces.  
There are two spaces after the last line.

</div>

### Formatting page layout

To insert a horizontal rule, use three or more dashes (---) on a line with no other characters

---

### Modifying text

#### Changing text view

``` title="Text modifying"
- *Text has been italicized*
- **Text has been bolded**
- ***Text has been bolded and italicized***
```

<div class="result" markdown>

- *Text has been italicized*
- **Text has been bolded**
- ***Text has been bolded and italicized***

</div>


#### Highlighting text

``` title="Text highlighting"
- ==Text has been highlighted==
- ^^Text has been underlined^^
- ~~Text has been split~~
```

<div class="result" markdown>

- ==Text has been highlighted==
- ^^Text has been underlined^^
- ~~Text has been split~~

</div>

### Links

Links between pages and sites can be made using the format:

``` title="Page linking"
[Title](page url)
```

#### Internal  linking

For inner-wiki linking, use the following format.  

``` title="Inner-wiki page linking"
[[hedgehog|Hedgehogs]] can be found here on this wiki.
```

<div class="result" markdown>

[[hedgehog|Hedgehogs]] can be found here on this wiki.

</div>

!!! warning "Custom formatting info"

    Note the use of `/Extended-Wiki/wiki/` in front of the markdown file name of the page.
    There is special logic in page to facilitate the "compressing" of the wiki page structure and as such, using the full file path of the connecting page will result in a broken link.

---
#### External linking

For external links, the page can easily be linked as would be found on other sites.

``` title="Inner-wiki page linking"
[Hedgehogs](https://wikipedia.org/wiki/Hedgehog) can be found on Wikipedia.
```

<div class="result" markdown>

[Hedgehogs](https://wikipedia.org/wiki/Hedgehog) can be found on Wikipedia.

</div>
