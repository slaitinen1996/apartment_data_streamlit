import etl

df=etl.extract()
df_transformed=etl.transform(df)
etl.load(df_transformed)

##upsert

etl.upsert()

## create aggrgate history

## dagster

