Properties in Colaba and Bandra command significantly higher prices than Borivali.
Price per square meter is the strongest driver of total property value.
Large properties above 150 sqm show exponential price growth.
Premium locations contribute more to property value than bedroom count.


# Mumbai Real Estate Intelligence - Business Insights

## Executive Summary

An XGBoost machine learning model was developed to predict residential property prices in Mumbai based on:

* Area
* Property Size
* Number of Bedrooms
* Price per Square Meter
* Year

The model achieved strong predictive performance and was integrated into an interactive Streamlit dashboard.

---

## Key Findings

### 1. Price Per Square Meter is the Strongest Driver

Feature importance analysis shows that Price_per_sqm_Local contributes most significantly to property valuation.

Business Impact:

Developers and investors should monitor local price-per-square-meter trends closely when evaluating opportunities.

---

### 2. Premium Locations Command Higher Prices

Properties in Bandra, Colaba, and Powai consistently demonstrate higher average market values.

Business Impact:

Location continues to be one of the strongest determinants of property valuation.

---

### 3. Larger Properties Generate Higher Absolute Returns

Properties with larger built-up areas show significantly higher market prices.

Business Impact:

Investors seeking capital appreciation should prioritize larger units in premium areas.

---

### 4. Area Influence Exceeds Bedroom Count

The model indicates that geographical location has a stronger impact on valuation than the number of bedrooms.

Business Impact:

Location strategy should be prioritized over unit configuration when evaluating investments.

---

## Investment Recommendation

Based on the Investment Score Engine, the highest-ranked area offers the best balance between:

* Property Value
* Affordability
* Growth Potential
* Size

Investors may use this score as an initial screening metric before conducting detailed due diligence.

---

## Tools Used

* Python
* Pandas
* NumPy
* XGBoost
* SHAP
* Streamlit
* Matplotlib
* Seaborn

---

## Future Improvements

* Integration with live property APIs
* Geographic clustering
* Time-series price forecasting
* Rental yield prediction
* Real-time investment recommendations
