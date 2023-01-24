---
title: 'caterpillard: A novel technique to visualize & forecast univariate time-series data using Python'
tags:
  - Python
  - data-visualization
  - Difference of Differences
  - Markov chains
  - Threat advisory
authors:
 - name: "Prabal Pratap Singh"
   orcid: 0000-0002-0738-7629
   affiliation: "1"
 - name: "Deepu Philip"
   orcid: 0000-0002-4607-9020
   affiliation: "1"
affiliations:
 - name: Department of Industrial & Management Engineering, Indian Institute of Technology Kanpur
   index: 1
date: 24 January 2023
bibliography: paper.bib
---

# Summary

Researchers utilize univariate time-series data for monitoring certain quantities of
interest in their domain. Line charts and other traditional visualization methods depict
data as it is. The innovative Caterpillar diagram is a visualization tool
[@singhInnovativeColorcodingScheme2022] that combines both Difference of Differences (DoD)
approach and the popular Markov chain forecasting method to capture and illustrate
variations in the univariate time series data. A collection of colored circles of various
radii constitute the proposed diagram. These sequential circles capture the differences in
the data's successive cohorts, created by three successive time units. The size of the
circle and the color scheme indicate the quantity and direction of the fluctuation in
data.

Caterpillar diagram offers two major advantages compared to traditional tools like a line
chart. First, the Caterpillar diagram eliminates the clutter associated with line charts
when dealing with multiple datasets. Caterpillar diagram de-clutters by creating a single
diagram that simultaneously represents the variance in all constituting data series.
Second, the Caterpillar diagram can also function as a forecasting tool because the color
transition between two consecutive cohorts follows the Markov process.

# Statement of need

System monitoring is crucial for any system that generates data with time. Caterpillar
Diagram provides a generic color-coding scheme to quickly and effectively communicate the
variations of the system. Scholarly research in the domain of terrorism majorly requires
monitoring the variations in terrorist activities and their accumulated impact. The
genesis of this novel technique lies in summarizing the univariate Global Terrorist Impact
Scores (GTI-IS) for nations or regions [@hyslopMeasuringTerrorismGlobal2014]. The
comprehensive Global Terrorism Database facilitates the evaluation of GTI-IS for each
recorded event in the database [@lafreeIntroducingGlobalTerrorism2007],
[@startGTDCodebook20202021].

A fundamental premise of the Caterpillar diagram is that a cohort's color entirely depends
on the previous cohort, thereby capturing the lingering effects of terrorism. Any
implementation in a different domain must meet these requirements to use the Markovian
forecasting characteristic of this technique.

# References