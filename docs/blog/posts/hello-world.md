---
date: 2023-01-31
authors: [nima]
categories:
  - Hello
  - World
tags:
  - Foo
  - Bar
slug: hello-world
readtime: 15
links:
  - plugins/search.md
  - insiders/index.md#how-to-become-a-sponsor
  - Nested section:
    - External link: https://pharmb.io
    - setup/setting-up-site-search.md
---

# Hello world!

While post URLs are dynamically computed, the built-in blog plugin ensures that all links from and to posts and a post's assets are correct. If you want to link to a post, just use the path to the Markdown file as a link reference (links must be relative):

[Hello World!](blog/posts/hello-world.md)

Linking from a post to a page, e.g. the index, follows the same method:

[Authors](../authors.md)

!!! note

    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
    nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
    massa, nec semper lorem quam in massa.

=== "C"

    ``` c
    #include <stdio.h>

    int main(void) {
      printf("Hello world!\n");
      return 0;
    }
    ```

=== "C++"

    ``` c++
    #include <iostream>

    int main(void) {
      std::cout << "Hello world!" << std::endl;
      return 0;
    }
    ```


