
try:    
    def rename(df,rename_input_list):
        rename_input_list = rename_input_list.split(",")
        
        for rename_list in rename_input_list:
            rename_name = input("What do you want to rename {}".format(df.columns[int(rename_list)]))
            df = df.rename(columns={df.columns[int(rename_list)]: rename_name})
        return df

    def print_column_name(df):
        for colums in df.columns:
            print(colums,": ",df.columns.get_indexer([colums])[0] )

    def product_rating(x):
        # checking if its already an integer/Float
        if isinstance(x,int) or isinstance(x,float) == True:
            return x
        else:
            list = ["out of 5","out of 5 stars","stars",'Rated ','star rating']
            for lists in list:
                x = x.replace(lists,"") 
            return x

    #Find out only digits from the column (Will remove the Sepeartors also)
    def only_digit(y):
        try:
            list = [",",":","."]
            for lists in list:
                y = y.replace(lists,"") 
            y = re.findall('\d+', str(y))
            
            return y[0]
        except:
            pass


    def basic_cleaning(df):
        
        #Sentance Casing the title
        df.columns = df.columns.str.title()
        df = df.rename(columns={'Sku': 'SKU','Date':'date','Root':'root','Star Rating':'Product Rating','Brand Rating':'Product Rating','Number Of Rating':'Rating Count'})
        # df.columns = df.columns.str.replace(' ', '')

        try:
            print("Number of Null Reviews : {} . Totoal Number of Review is{} ".format(df["Review"].isnull().value_counts()[True],df["Review"].isnull().value_counts()[False]))
        except:
            print("No Null Values. Totoal Number of Review is{}".format(df["Review"].isnull().value_counts()[False]))
        #Deleting Null Reviews
        df = df.dropna(subset=['Review'])

        #Finding the Null Reviews
        if any(df.duplicated(subset=['Review', 'date', 'Author'])) :
            print("Duplicates Removed are {}".format(df.duplicated(subset=['Review', 'date', 'Author']).value_counts()[True]))
        else:
            pass
        df = df.drop_duplicates(subset=['Review', 'date','Author'])
        #Removing Whitespace
        df['Review'] = df['Review'].apply(lambda x:x.strip() if isinstance(x,str) else x)

        if any([column_name for column_name in df.columns if column_name == 'Web-Scraper-Order'] ):   
            df = df.drop(['Web-Scraper-Order'], axis=1)
            df = df.rename(columns={'Web-Scraper-Start-Url': 'root'})
        
        if any([column_name for column_name in df.columns if column_name == 'Title'] ):
            df["Title"] = df["Title"].astype(str) 
            df["Review"] = df[["Title","Review"]].agg('. '.join,axis=1)
            df = df.drop(['Title'],axis= 1)
        
        if any([column_name for column_name in df.columns if column_name == '_Root'] ):  
            suntiger_drop_list = ['Pagination', 'Pagination-Href', 'Crawl Source Input', 'Brand Input','Data Crawl Completion Time(Utc)', 'Original Date']
            for suntiger_drop in suntiger_drop_list:
                if suntiger_drop in df.columns:
                    df = df.drop([suntiger_drop],axis=1)
                    df = df.rename(columns={'_Root':'root'})

        if any(df.columns.str.contains("Product Rating")) == True:
            df["Product Rating"] = df["Product Rating"].map(product_rating)

        if any(df.columns.str.contains("Review Rating")) == True:
            df["Review Rating"] = df["Review Rating"].map(product_rating)

        if any(df.columns.str.contains("Rating Count")) == True:
            df["Rating Count"] = df["Rating Count"].map(only_digit)
        
        #Deletion of unwanted column
        for colums in df.columns:
            print(colums,": ",df.columns.get_indexer([colums])[0] )
        other_rows_index_y_n = input("Is there any others rows to be removed, please provide the index with 0(y/n)")
        if other_rows_index_y_n =="y":
            loc_delete_rows = input("Enter the location of rows to delete")
            loc_delete_rows = loc_delete_rows.split(',')
            for loc_delete_row in reversed(loc_delete_rows):
                loc_delete_row = int(loc_delete_row)
                print("{}Deleted ".format(df.columns[loc_delete_row]))
                df = df.drop([df.columns[loc_delete_row]],axis=1)
        

        rename_input = input("Do you want to rename any column:?")
        if rename_input == "y":
            print_column_name(df)
            rename_input_list = input("Provide the index Number")
            df = rename(df,rename_input_list)
        else:
            pass

            
            
        
        df.head(1)
        return df
    
except Exception as e:
    print(e)
