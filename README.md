# Pagerank analysis on research papers networks

## Introduction
In the process of writing a scientific paper it is necessary to search for works in the state of art that will serve as support for the new argumentations. The stage of searching for papers belonging to a well-defined subject area can be time-consuming, since not all papers may be equally useful, or even bring no results at all. It therefore turns out to be necessary to carefully search for papers from which to take useful informations for the work we are currently doing.

## Project Idea
The project is intended to create a tool capable of constructing a citation graph between papers from an input dataset and viewing all their informations and connections. Then the pagerank algorithm will be applied to get the papers in order of relevance, based on the network created. In addition, a new methodology, called Semantic Pagerank, will be explored for calculating pagerank of graph nodes with the addition of information regarding semantic similarity among the chosen features.

## Goals and Motivations
Understanding the behavior of the pagerank algorithm is the main motivation for creating the tool. The purpose is to understand if it is a suitable metric for sorting papers in a network, based on their citation links, or if it can be upgraded with additional informations.
It can be a tool useful for the process of finding relevant papers to mention in future articles or publications, easing the collection and evaluation of sources.

## Tool Usage
You can use the tool by following the steps below:
- clone the repository
- add the datasets in the format specified below*.
- run the cells in the <b>similarities.ipynb</b> file to generate the files for the title vectors and similarity values.
- run the <b>vis_app.py</b> file and go to the link that will appear in the output terminal to reach the site. Alternatively, click on the following link: http://127.0.0.1:8080


Tip: check the files' path you are using to avoid errors.

*The datasets to be used for proper use of the tool should be as follows:

- the first containing author informations in the following format:
``` json
{
   "123456789": {
      "name": "name",
      "surname": "surname"
   },

   ...
}
```
- the second containing the papers in the following format:
``` json
[
   {
      "id": "12345689",
      "title": "paper title",
      "abstract": "abstract string",
      "authors": [
         "123456789",
         "987654321"
      ],
      "year": "2023",
      "publisher": "publisher name",
      "keywords": ["a", "list", "of", "keywords"],
      "references": [
        "1234",
        "5678",
        "4321",
        "8765"
      ]
   },

   ...
]
```