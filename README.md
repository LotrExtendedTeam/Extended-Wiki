# Extended-Wiki
The static site repository for hosting Extended's Wiki built off of [MkDocs](https://github.com/squidfunk/mkdocs-material)



## Contributing
1. To work with mkdocs, first fork the repository to your own account and then clone it to your local machine.
2. If you don't have Python or pip installed, I would recommend installing it, as later steps require it.
3. Next run the following command to set up all the required packages for a local instance.
~~~
 pip install mkdocs-material mkdocs-htmlproofer-plugin mkdocs-git-revision-date-localized-plugin mkdocs-glightbox mkdocs-literate-nav "mkdocs-material[imaging]" imageio
~~~
4. With your shell of choice, run the following command to start the live-reloading local-instance docs server.
~~~
 mkdocs serve
~~~
5. Now every change you make to your wiki instance will be reflected live in your web browser.
6. When you are satisfied your changes, open a PR to the main repo to have your changes/additions added to the wiki.
7. Profit?

### Note
- Do not contribute to the gh-pages branch, as this branch is created automatically when the Docs Deploy workflow is run.
- Also don't edit any Github workflows, your PR will not be accepted if you edit them, unless we deem it absolutely necessary.

## License
* Extended Wiki
  - (c) 2025 LotrExtendedTeam
  - [![License](https://img.shields.io/badge/License-MIT-blue.svg?style=flat)](https://github.com/LotrExtendedTeam/Extended-Wiki/blob/main/LICENSE)
## Attributions
* Mkdocs Material
  - (c) 2016-2025 Martin Donath
  - [![License](https://img.shields.io/badge/License-MIT-blue.svg?style=flat)](https://squidfunk.github.io/mkdocs-material/license/)
* mkdocs-htmlproofer-plugin
  - (c) 2018 Lukas Geiter
  - [![License](https://img.shields.io/badge/License-MIT-blue.svg?style=flat)](https://github.com/manuzhang/mkdocs-htmlproofer-plugin/blob/main/LICENSE.md)
* mkdocs-git-revision-date-localized-plugin
  - (c) 2018 Terry Zhao
  - (c) 2019 Tim Vink
  - [![License](https://img.shields.io/badge/License-MIT-blue.svg?style=flat)](https://github.com/timvink/mkdocs-git-revision-date-localized-plugin/blob/master/LICENSE)
* MkDocs GLightbox
  - (c) 2022 Blueswen
  - [![License](https://img.shields.io/badge/License-MIT-blue.svg?style=flat)](https://github.com/blueswen/mkdocs-glightbox/blob/main/LICENSE)
