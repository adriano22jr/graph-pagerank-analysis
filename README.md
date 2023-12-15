# Pagerank analysis on research papers networks

## Introduction
In the process of writing a scientific paper it is necessary to search for works in the state of art that will serve as support for the new argumentations.
The stage of searching for papers belonging to a well-defined subject area can be time-consuming, since not all papers may be equally useful, or even bring no results at all. It therefore turns out to be necessary to carefully search for papers from which to take useful informations for the work we are currently doing.

## Project Idea
The project is intended to create a pipeline capable of constructing a citation graph between papers from an input dataset.
Then the pagerank algorithm will be applied to get the papers in order of relevance, based on the network created, and then it will be validated by comparing the results with well-known statistics.
As an alternative it will be possible to construct graphs with weighted edges according to the selected features to see how the results change.

## Goals and Motivations
Understanding the behavior of the pagerank algorithm is the main motivation for creating the pipeline. The purpose is to understand if it is a suitable metric for sorting papers in a network, based on their citation links.
It can be a tool useful for the process of finding relevant papers to mention in future articles or publications, easing the collection and evaluation of sources.

Finally as the main goal is to provide a high compatible tool. In other words, with the limitations on the format of the dataset to be provided to the pipeline removed, the tool should be able to generate the citation graph and apply the chosen ranking algorithms for any paper dataset passed as input.