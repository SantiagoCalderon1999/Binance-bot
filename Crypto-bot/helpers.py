
def split_DataFrame(df, training_percentage):
    training_index = int(len(df)*training_percentage)
    df_train = df.iloc[:training_index]
    df_test = df.iloc[training_index:].reset_index()
    return df_train, df_test