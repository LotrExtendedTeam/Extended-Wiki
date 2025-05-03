# Extended-Wiki
The static site repository for hosting Extended's Wiki



## Contributing
1. To work with mkdocs, first fork the repo and clone it to your local machine.
2. If you don't have Python or pip installed, I would recommend installing it, as later steps require it.
3. Next run the following command to set up all the required packages for a local instance.
~~~
 pip install mkdocs-material mkdocs-htmlproofer-plugin mkdocs-git-revision-date-localized-plugin
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
