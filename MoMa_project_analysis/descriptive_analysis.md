This report provides a descriptive statistical overview and an initial time series analysis of reviews for the
Museum of Modern Art (MoMA) based on the provided dataset. We explore the distribution of review
ratings, the breakdown of reviewer types (foreign, domestic, local), the temporal distribution of reviews,
the top locations of reviewers, and trends in review counts and average ratings over time.

The dataset has 9694 reviews for MoMA. Each review includes a rating (1 to 5 stars) and the date it was
left (Year, Month, Day). The reviews span from 2005 to early 2025, covering roughly 20 years. Reviewers
are categorized by Tourist_type as foreign, domestic, local, or not specified (NA). In the analysis below,
we ensure that missing values in Tourist_type are labeled as "Not Specified" for clarity.
We compute summary statistics for the Rating column to understand its central tendency and spread.


![image](https://github.com/user-attachments/assets/7df2e31c-9a5f-4740-aad2-b20c73d82915)


Distribution of review ratings (1 = lowest, 5 = highest). Most reviews are 5-star
ratings, indicating very positive visitor experiences. The plot shows that 5-star
reviews are by far the most common (over 6,000 reviews), followed by 4-star
reviews. Lower ratings (1, 2, or 3 stars) are comparatively rare. This confirms
that the majority of visitors rated MoMA very highly, with more than 85% of
reviews being 4 or 5 stars. Only a small fraction of visitors left 1- or 2-star
reviews.


![image](https://github.com/user-attachments/assets/4c9e69c6-b609-4268-9e8f-295362061370)


Number of reviews by tourist type. "Foreign" refers to international visitors,
"Domestic" to U.S. visitors outside NYC, "Local" to New York City residents, and
"Not Specified" for unidentified origins. From the plot we see that foreign
visitors contributed the most reviews (around 3,880 reviews), followed by
domestic visitors from the U.S. (about 3,105 reviews). A smaller segment of
reviews (roughly 412) came from local New York City residents. A substantial
number of reviews (~2,300) have no specified tourist type (likely because the
reviewer’s location wasn’t provided). This breakdown suggests that MoMA is a major attraction for
international tourists, and domestic tourists also form a large share of visitors, whereas relatively few
locals write reviews.


![image](https://github.com/user-attachments/assets/3a7e3321-431f-4368-b47a-a059682c7ef6)


Total number of reviews per year (2005–2025). Review counts grew 
significantly until mid-2010s, with a sharp drop in 2020–2021. The museum saw steady growth in review 
counts from the mid-2000s through the 2010s. There was a peak around 2015–2016 (e.g., 2016 had the highest 
number of reviews, over 2,000). After 2016, the number of reviews per year started to decline somewhat. 
The most striking pattern is the sharp decrease in 2020 and 2021, where reviews dropped to 
only 135 and 66 respectively – this is clearly due to the COVID-19 pandemic (museum closures and fewer visitors). 
In 2022–2024, review counts began to recover but remained much lower than the peak years. 
(Note: 2025 is only partially included, with data up to March 2025, hence the low count for that year.)


Top 5 Cities:
City
New York City    412
London           272
Toronto          126
Sydney           120
Melbourne        103
Name: count, dtype: int64

Top 5 States/Countries:
State_Country
United Kingdom    1111
New York           637
Canada             493
Australia          470
California         328
Name: count, dtype: int64


![image](https://github.com/user-attachments/assets/b8b8c623-436e-451c-bb43-d7ccb534a038)


Monthly number of reviews over time (2005–2025). The count of reviews per month rises steeply around 2012–2016 
and then drops to nearly zero in 2020–2021, with partial recovery afterward. In this time series, each point 
represents the number of reviews in a given month. We observe very few reviews per month in the 
early years (2005–2010), often near zero. Starting around 2012, there is a rapid increase in monthly reviews. 
During the peak period (2015–2016), MoMA was receiving on the order of 150–200 reviews per month. 
After 2016, the monthly counts gradually decline. The impact of the COVID-19 pandemic is clearly visible: 
from early 2020 through 2021, the monthly review count plummets to nearly zero for several months 
(due to lockdowns and travel restrictions). From late 2021 into 2022, the museum sees reviews coming in again, 
but at a much lower rate (tens of reviews per month) compared to the pre-2020 peak. By 2023–2024, there is 
a mild recovery, but the monthly review numbers remain well below the mid-2010s peak. On an annual level, 
the same trend is reflected: after steady growth, 2016 was the highest year for reviews, and 2020–2021 were 
the lowest. Most recently, 2022–2024 have improved from the pandemic low, but are still far from the peak years.


![image](https://github.com/user-attachments/assets/e2352ff5-2059-4e2f-89b5-8cb16eb91703)


Monthly average review rating over time. Despite some fluctuations (especially in early years with few reviews), 
the average rating remains high (around 4 to 5) throughout the years. Each point on this line represents the 
average star rating for a given month’s reviews. The plot shows that the average rating per month has 
consistently stayed in the 4.0–4.5 range for most of the time period. In the very early years (e.g., 2005–2008) 
there are some larger swings in the monthly average – this is because there were very few reviews in those months,
 so one low or high rating could skew the average. Once the number of reviews became substantial (post-2010), 
 the monthly averages smooth out and hover close to 4.5 out of 5 with slight variation.

 In summary, the MoMA review data shows that visitors generally have an excellent experience at the museum 
(average rating ~4.4/5, with the majority giving 5 stars). The museum attracts a large international 
audience – foreign tourists account for the largest share of reviews, though domestic visitors are also 
significant, and relatively few locals leave reviews. The volume of reviews grew dramatically through the 2010s, 
highlighting increasing visitation or engagement, then dropped sharply in 2020–2021 due to the pandemic. 
As of 2022–2024, review counts are rebounding, albeit not yet to previous highs. Throughout these 
fluctuations in visitor volume, the satisfaction levels (as reflected in ratings) have remained very 
high and relatively stable over time.






























