########################################################################################
# PROJECT: CREATING CUSTOMER PERSONA: SIMPLE SEGMENTATION AND RULE BASED CLASSIFICATION
########################################################################################

# Importing users ve purchases data sets:

import pandas as pd
users = pd.read_csv("2nd_week/lectures/users.csv")
purchases = pd.read_csv("2nd_week/lectures/purchases.csv")

# Merging data sets on "uid" column:

df = purchases.merge(users, how="inner", on="uid")
df.head()

# Calculating total earnings in country, device, gender, age breakdown:

df.groupby(["country","device","gender","age"]).agg({"price":"sum"})

# Sorting data set according to total earnings and creating a aggregated data set.

df_agg = df.groupby(["country","device","gender","age"], as_index=False).agg({"price":"sum"}).sort_values("price", ascending=False)
df_agg.head()

# Transforming "age" variable in to a categorical variable and adding the data set as "age_cat"

bins = [0, 19, 24, 31, 41, df_agg["age"].max()]
my_labels = ['0_18', '19_23', '24_30', '31_40', '41_' + str(df_agg["age"].max())]

df_agg["age_cat"] = pd.cut(df_agg["age"], bins, labels=my_labels)

# Dividing customers according to their demographic characteristics (age, gender, country etc.) and adding the data set as "customer_level_based".

# For example:
# USA_AND_M_0_18 --> country: USA, Android user, male, between 0-18 years old.
# BRA_AND_F_41_75 --> country: Brazil, Android user, female, between 41-75 years old.

df_agg["customer_level_based"] = [row[0] + "_" + row[1].upper() + "_" + row[2] + "_" + row[5] for row in df_agg.values]
df_agg = df_agg.groupby("customer_level_based").agg({"price": "mean"})
df_agg = df_agg.reset_index()
df_agg["customer_level_based"].count()

# Dividing personas into segments according to "price" column and adding a new columns as "segment".

# "customers_level_based" columns indicates our new personas.
# For example: "USA_AND_M_0_18". ABD-ANDROID-MALE-0-18 is a persona that indicate a customer class.
# Dividing personas into segments according to "price" column.

df_agg["segment"] = pd.qcut(df_agg["price"], 4, ["D", "C", "B", "A"])
df_agg.groupby("segment").agg({"price":"mean"}).sort_values("price",ascending=False)

# FINAL: Identifying a new customer's segment:
# New customer: 42 years old, IOS user, a Turkish women.

new_user = "TUR_IOS_F_41_75"
print(df_agg[df_agg["customer_level_based"] == new_user]) # New customer's segment is D.