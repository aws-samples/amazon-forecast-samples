
# Item Metadata (IM)

Especially for cold-starts, or new product introductions, it is important to have Item Metadata (IM).  **Item Metadata is static information with respect to time, it varies only per fixed "item_id"**.  Examples of metadata are type of item, product group, genre, color, class.

***Figure 3 - Example of Item Metadata with sample data records***
<br>
![IM](../images/item-metadata.png)

You are able to define your IM with JSON; this example supports the Figure 3 schema.
```
{
   "Attributes":[
      {
         "AttributeName":"item_id",
         "AttributeType":"string"
      },
      {
         "AttributeName":"food_category",
         "AttributeType":"string"
      },
      {
         "AttributeName":"food_cuisine",
         "AttributeType":"string"
      }
   ]
}
```
**For a more comprehensive list of considerations, visit the [item metadata documentation](https://docs.aws.amazon.com/forecast/latest/dg/item-metadata-datasets.html) page.**



<br><br>
[Return to Datasets](./Datasets.md)
[Return to Table of Contents](../README.md)
