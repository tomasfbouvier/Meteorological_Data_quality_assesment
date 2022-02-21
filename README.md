Meteorological Data Quality Assesment
===========

The context of this master thesis is DMI's NCKF (National Center for
Climate Research) DANRA project [@DANRA], which stands for DANish
regional ReAnalyses. The target is to produce a high resolution
reanalysis for 70 years of the Danish weather (1950-2020). We understand
the purpose of a reanalyses is to create a weather data-base combining
historical observation with modern weather forecasting data. The
data-base can be later used for climate research.

The input data used in DANRA includes in-situ observation data collected
from station network spread around the model domain centered around
Denmark (DKA), as well as remote sensing observation and external model
data used for boundary conditions.

![The region surrounding Denmark, DKA, as covered by the DANRA
reanalysis. In green: the surface station network used for DANRA data
assimilation.](assimilation.png)

Surface observation stations as shown in Fig 1 report regularly
throughout the whole reanalysis period from 1950 to 2020 a set of
in-situ measurements, such as temperature, surface pressure, wind speed
and direction. Before those measurements enter the DANRA re-analyses
systems for assimilation, it is necessary to asses the quality of the
latter to avoid potentially errorneous information due to different
reasons such as biases or other instrument errors. ALthough observation
data normally goes through basic quality control, it is not uncommon to
see data set with gross errors. For reanalysis project such as DANRA
which uses historical observation data archive, it has been necessary to
apply additional quality control to secure reanalysis quality. So far
such quality control has been performed manually. The first objective of
this thesis will be to develop an improved and automated methods to
detect data that deviates severely the trend and hence potentially
wrong. Furthermore, we would like to explore correction if possible.

For achieving these objectives, of course it is impossible to compare
the measurements to the true values that we are precisely trying to
measure. However, the discrepancy and correction can be estimated by
comparing our measurements to others in the database and use some gross
assumptions about the coherence of the values:

-   Coherence in space: In the physical system that we are describing,
    measurements have to be correlated within the distance. This means
    that the closer the measurements are within each other, the more
    correlated they have to be. This is general though and some comments
    have to be made. The spatial coherence is also affected by other
    factors than the distance, for example the orography of the surface
    where the stations are placed. If two stations are placed within a
    flat surface, for example a valley, their correlation will be
    different than if they are placed within a mountain. Other aspects
    that could affect the correlation are atmospheric conditions such as
    air pressure.

-   Coherence in time: The measurements of a single station can be
    represented in the form of time series. In overall the station
    network can be seen as a multivariate time series. This series carry
    trends, features and periodicity whose description is complex.
    However, as a general rule it is abnormal to find singular values
    within a short time.

    ![Example of an time series anomaly. We can see a sudden jump within
    the time series that is unlikely to happen in the
    nature](Image-4.png)

-   Physical coherence: Apart from the spatial coherence and the time
    coherence, we recall that we are talking about a complex and chaotic
    but yet physical system, governed by physical laws. Therefore there
    should not be room for measurements that are not in the range of
    certain physical boundaries. Examples of physical effects biasing
    the measurements are weather conditions such as storms or snows,
    light exposure, wind direction and intensity, proximity to a coastal
    region, etc.

In summary, we expect our algorithm to evaluate an incoming value paying
attention to these three clues. The idea would be to create a
statistical framework to determine the joint probability distribution
that a point is considered outlier or normal value. After all mentioned
before we dispose from a set of rules. Those rules allow us to sample a
set of marginal probabilities (each rule $\equiv$ one marginal [^1]).

Moreover, through the thesis we would like to find new rules, that
escaped human's eye so far. This can be done through artificial
intelligence methods, that learn automatically from the data how to
detect outliers.

The question then is how are we going to merge all the marginals to
generate a joint probability distribution (posterior). The central tool
for this task is the well-known Bayes theorem which allows us to merge
priors and observations through hierarchical bayes and bayes networks to
create a posterior distribution for the measurement.

Once the posterior known, it is possible either to discriminate
outliers, either to maximise the distribution to find the most probable
value for the observation, either to assign a weight for the observed
value that will then be taken into account through the re-analyses
system.

Anomaly detection methods
=========================

Anomaly detection is a statistical task that can be defined as the
following: Given a set of points that follow a trend, find the points of
the set that are suspicious to deviate from the trend, namely
\"outliers\". We can find anomaly detection in a myriad of fields such
as financial fraud, aircraft risk evaluation or the one that we are
interested in, error detection in electronic instrumentation .

From the definition of the task, it makes sense that any popular
approach to solve it goes through modelling the trend that our outliers
are deviating from. The differences in the statistical modelling an how
is the outlier probability evaluated from the probability distribution
are the variables that make the differences between anomaly detection
methods.

According to [@old_article] If we pay attention to the points that are
used for detection we can identify three types of modelling:

-   Type I: **No prior knowledge of the outliers**(equivalent to
    un-supervised learning). We start with the premise that every data
    point can be normal or anomaly. Then, we perform our statistical
    modelling using all data points and an unsupervised learning
    algorithm and we evaluate it on all data points, flagging the
    outliers as the remote ones. The technique subdivides further
    depending on what is decided to be done with the outliers, create a
    new cluster incorporating them (non-robust methods) or simply drop
    them from the set (robust methods).

-   Type II: **Knowledge of both normal and anomalous data
    distributions**(equivalent to supervised learning). We have enough
    data from both classes and we train a supervised learning algorithm
    on them, so it can attribute a label to any new data point. This
    method is useful for static data distributions. Otherwise, in case
    of evolution of the distribution, the algorithm needs to be
    retrained. For using this technique we need both normal examples and
    outliers.

-   Type III: **Knowledge of the normal distribution**(equivalent to
    semi-supervised learning). This implies that we have enough points
    to picture the distribution of normal points. From here, the
    boundary of normality is defined and any new point exceeding this
    boundary is classified as outlier. The requirement for this method
    is that we have access to many accurate examples of normality, but
    not outliers.

[Disclaimer: In our particular case, the number of points that have been
identified as outliers is very small compared to normal points. In the
best case we would therefore be working with a very imbalanced data-set
which would be difficult the classification. Moreover, as mentioned in
the next section many outliers and determining features in the data are
yet to be discovered. For this reason, of the three approaches mentioned
above, it seems that the we will explore mainly the first.
]{style="color: blue"}

Examples of previous attempts on quality control at DMI 
=======================================================

Alessandro's thesis
-------------------

An example of how the biases commented above are applied in a quality
control can be found in a previous thesis written at DMI
[@Alessandro; @thesis]. The author discards and corrects the data in two
ways:

-   Buddy check (spatial correlation): This is a very simple baseline
    for data consistency assurance. The idea is to subdivide the domain
    of study into little parcels. We calculate the mean and standard
    deviation of the of points in each parcel. Any point that deviates
    more than N standard deviations from the mean of its parcel is
    considered as outlier and hence discarded. Of course this very
    simple check has many disadvantages such as the dependence on many
    hyper-parameters or the different density of points in each parcel.

-   Offset correction (spatial correlation): An offset for each station
    (NETATMO) in the database by time-series comparison with a closest
    more accurate weather station (SYNOP). The offset is used for
    correcting afterwards the whole time-series. This again simple
    correction is equivalent to make an estimation of the average error
    and supress it but doesn't take into account higher moments of the
    error probability distribution.

Bjarne's work
-------------

Bjarne spends time everyday correcting data from different SYNOP
stations. He discards and corrects data by eye. The simplest outlier
detection that Bjarne performs is based on comparing the data with the
rest of the time-series. If there are sudden jumps of big size in
temperature (for example 20 K within 3 hours) then it is likely that
this will be an outlier and be discarded. Comparisons with an accurate
model prediction allow to flag offsets that can afterwards be corrected.
Furthermore, it is possible to compare by eye a station with nearby ones
while there are many additional factors to take into account when
performing it. Bjarne also corrects measurements of preassure that can
be missing or buffr to DMI database extraction errors.

In general, manual anomaly detection is accurate but requires a
scientist to dedicate an insane amount of time and effort to the task,
as the amount of data and factors affecting the quality is giant. With
this amount increasing exponentially it will soon be impossible to do
this by hand. Moreover this is an intuitive anomaly detection, not based
on any statistics but on knowledge and priors that the researcher has on
the data he is working with. It is likely that many hidden features in
the data which could reveal anomalies are not taken into account.

Note o Bayes theorem
====================

Depending on what we wish to solve Bayes can be useful in different
ways. So far we found how using Bayes theorem we can estimate the
probability that a measurement is correct or incorrect depending on
different tests that will perform. Let's denote the measurement as being
bad by \"B\" and the different tests by $T_{1}, T_{2}, T_{3} ...$. Let's
particularize for two tests. As described in [@multiple_bayes], the
probability that we wish to estimate is given by bayes rule
$$P(B| T_{1},T_{2})= \frac{ P(T_{1},T_{2} | B )P(B)}{P(T_{1},T_{2} )}$$

This allows us to make a statistical model from samples corrected by
Bjarne or other sources of information. Let's analyze the previous
formula element by element. $P(B)$ is the prior information that we have
from a measurement being detected to be an outlier. If we particularise
our model for a single station we would consider that this is the amount
of outliers in our training set station divided by the full set size in
the station.

For $P(T1,T2| B)$ and $P(T1,T2)$ we need to perform an approximation
which vality is arguable. In order to make the best use of our data, we
assume statistical independence of the two tests. This corresponds to
assume that a success/failure of one test is uncorrelated with the
others. This allows us to split the numerator conditional probability as
follows $$P(T1,T2| B) = P(T1|B)P(T2|B)$$

For the last term, we make use of the normalization condition and asume
that a data point is either good (G) or bad:
$$1 = P(B| T_{1},T_{2}) + P(G| T_{1},T_{2}) =  \frac{ P(T_{1},T_{2} | B )P(B)}{P(T_{1},T_{2} )} + \frac{ P(T_{1},T_{2} | G )P(G)}{P(T_{1},T_{2} )} \Longrightarrow$$
$$P(T1,T2) =   P(T_{1},T_{2} | B )P(B) + P(T_{1},T_{2} | G )P(G)$$

Plugging this in the previous equation we get an estimation of the
probability of a point being outlier if flagged by the tests:

$$\boxed{P(B| T_{1},T_{2})= \frac{ P(T1|B)P(T2|B)P(B)}{P(T1|B)P(T2|B)P(B) + P(T1|G)P(T2|G)P(G) }}$$

It is possible to generalise this expression to the case of an arbitrary
set of N statistically independent tests:
$$P(B|T_{1},..., T_{N}) =.\frac{P(B) \prod_{i}^{N} P(T_{i}|B)}{P(B) \prod_{i}^{N} P(T_{i}|B)+P(G) \prod_{i}^{N} P(T_{i}|G)}$$

In order to get a good estimator of new incoming data we need to
evaluate the probability of a positive test on ground truth cases
provided by Bjarne. However this is not straight as our tests perform
differently under different circumstances. We need to study how the
tests correlate to the observation, hence $P(T_{i}|B)$, depending on
external parameters such as, in a spatial correlation test, the distance
or the wind exposure.

Refferences
====================

A Survey of Outlier Detection Methodologies.Victoria J. Hodge
(vicky\@cs.york.ac.uk) and Jim Austin

A study on preprocessing and assimilation of Netatmo data in a NWP
system, Alessandro Falcione

Yang, X, K. S. Hintz, C. P. Aros and B. Amstrup, 2021, Danish Regional
Atmospheric Reanalysis: Final scientific report of the 2020 NCKF Work
Package 3.2.1, Regional Reanalysis Pilot. DMI report 21-31, 2021.

Scott D. Anderson, 2007, Combining Evidence using Bayes' Rule

[^1]: under the assumption that rules are uncorrelated
