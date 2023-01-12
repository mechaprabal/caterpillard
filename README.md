# Caterpillar Diagram

> A generic innovative visualization technique for univariate time-series data capable of
> forecasting the next-state transition using Markov chains.

----
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) [![License: AGPL
v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0) [![made-with-sphinx-doc](https://img.shields.io/badge/Made%20with-Sphinx-1f425f.svg)](https://www.sphinx-doc.org/) ![PyPI](https://img.shields.io/pypi/v/caterpillard?label=pypi%20package)
![PyPI - Downloads](https://img.shields.io/pypi/dm/caterpillard)
----


This is a software implementation of the proposed Caterpillar Diagram in the research
article titled [__"An innovative color-coding scheme for terrorism threat advisory
system".__](https://doi.org/10.1177/20597991221144577)

----

## What is a Caterpillar Diagram?

A Caterpillar Diagram is a visualization technique used for analyzing univariate
time-series data. It consists of a series of colored circles with varying radii. The
circle's color represents the direction of change in the time-series data, and the
circle's size shows its variation.

It implements the innovative and intuitive **_Difference of Differences (DoD)_** approach
to create a color schema. As proposed, it segregates the time-series data under analysis
into a cohort of three consecutive time units. Further, it utilizes the unsigned
differences between observations to assign a size to each cohort. This novel visualization
technique can segregate the time-series data using seven colors or five stages of
**_Aggressive, Ascent, Descent, Controlled, and Status Quo_**.

Further, the proposed mechanism utilizes the accumulated color information regarding each
cohort to forecast the next step transition using a stationary matrix of Markov Chains.

## Authors

<ol>
    <li> 
        <a href="https://orcid.org/0000-0002-0738-7629">
        <img alt="ORCID logo" 
            src="https://info.orcid.org/wp-content/uploads/2019/11/orcid_16x16.png"
            width="16"
            height="16" />
        Prabal Pratap Singh - https://orcid.org/0000-0002-0738-7629
        </a>
    </li>
    <li> 
        <a href="https://orcid.org/0000-0002-4607-9020">
        <img alt="ORCID logo" 
            src="https://info.orcid.org/wp-content/uploads/2019/11/orcid_16x16.png"
            width="16"
            height="16" />
        Prof. Deepu Philip - https://orcid.org/0000-0002-4607-9020
        </a>
    </li>
</ol>

## Installation instructions

To install `caterpillard` package from PyPI:

```console
(env) $ pip install caterpillard
```

## Documentation

The documentation for the package is available at <insert link>


## License

This package is licensed under **GNU Affero General Public License v3.0**

## Cite

This package has been developed as a part of the doctoral research titled "Modeling &
Analysis of Terrorism" by Prabal Pratap Singh under the supervision of Prof. Deepu Philip
at [Indian Institute of Technology Kanpur](https://www.iitk.ac.in/). If you utilize this
package then please use the following information to cite this package and the associated
Journal article in your work:
