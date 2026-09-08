<<<<<<< HEAD
# %%
from sickle import Sickle
from lxml import etree
import re
from pymongo import MongoClient
import bson
import xmltodict

# %%
# Local deployment of mongoDB Community Edition
uri = "mongodb://localhost:27017/"
client = MongoClient(uri)
database = client["oai_test"]
collection = database["records"]

# %%
# Parse single XML record and convert to dict
try:
    xml_dict = xmltodict.parse(
        xml_string,
        process_namespaces=True,
        namespaces={
            'http://www.openarchives.org/OAI/2.0/': 'oai',
            'http://www.openarchives.org/OAI/2.0/oai_dc/': 'oai_dc',
            'http://purl.org/dc/elements/1.1/': 'dc'
        }
    )

    # Convert to BSON
    bson_data = bson.encode(xml_dict)
    
    # Decode back to verify
    decoded_data = bson.decode(bson_data)
    
    # Store single record in MongoDB
    result = collection.insert_one(decoded_data)
    print(f"Stored single record ID: {result.inserted_id}")

except IOError as e:
    print(f"File error: {e}")
except etree.XMLSyntaxError as e:
    print(f"XML parsing error: {e}")
except Exception as e:
    print(f"Error: {e}")


# %%
sickle = Sickle('http://bdr.oai.bsb-muenchen.de/OAIHandler') # no longer in use

# %%
oai_sets = sickle.ListSets()
# for oai_set in oai_sets:
#    print('setSpec value for selective harvesting: ' + oai_set.setSpec)
#    print('Name of the set (setName): ' + oai_set.setName + '\n')

# %%
oai_formats = sickle.ListMetadataFormats()
# for oai_format in oai_formats:
#    print(oai_format.metadataPrefix)

# %%
# Define list of patterns before the loop
patterns = [
    re.compile(r'tafeln?', re.IGNORECASE),
    re.compile(r'tabelle[n|s]?', re.IGNORECASE),
    re.compile(r'tables?', re.IGNORECASE),
    re.compile(r'statisti', re.IGNORECASE),
    re.compile(r'tab[e|u]ul{1,2}a', re.IGNORECASE),
    # add more patterns as needed
    re.compile(r'Merc\.|Cam\.|Num\.rec\.|Num\.anc\.', re.IGNORECASE),
]

# %%
# fourth version with mongoDB
namespaces = {
    'http://www.openarchives.org/OAI/2.0/': 'oai',
    'http://www.openarchives.org/OAI/2.0/oai_dc/': 'oai_dc',
    'http://purl.org/dc/elements/1.1/': 'dc'
}

processed = 0
count = 0

records_to_insert = []
record_count = 0

try:
    for record in sickle.ListRecords(**{'metadataPrefix': 'oai_dc','set': 'all', 'from': '2025-01-01', 'until': '2025-02-13'}): 
        processed += 1
        if any(pattern.search(record.raw.lower()) for pattern in patterns): # find out what is returned in the raw field
            tree = etree.ElementTree(record.xml)
            xml_string = etree.tostring(tree.getroot(), pretty_print=True, encoding='unicode')
            count += 1
            
            records_to_insert.append(xml_string) # add to list
            record_count += 1

            xml_dict = xmltodict.parse(
                xml_string,
                process_namespaces=True,
                namespaces=namespaces
            )

            # Convert to BSON
            bson_data = bson.encode(xml_dict)
            
            # Decode back to verify
            decoded_data = bson.decode(bson_data)
            result = collection.insert_one(decoded_data)
            print(f"Stored single record ID: {result.inserted_id}")

            
    print(f"Total records processed: {record_count}")

except Exception as e:
    print(f"An error occurred: {e}")

print(f"\nTotal records processed: {processed}")
print(f"Total matching records found: {count}")


=======
# %%
from sickle import Sickle
from lxml import etree
import re
from pymongo import MongoClient
import bson
import xmltodict

# %%
# Local deployment of mongoDB Community Edition
uri = "mongodb://localhost:27017/"
client = MongoClient(uri)
database = client["oai_test"]
collection = database["records"]

# %%
# Parse single XML record and convert to dict
try:
    xml_dict = xmltodict.parse(
        xml_string,
        process_namespaces=True,
        namespaces={
            'http://www.openarchives.org/OAI/2.0/': 'oai',
            'http://www.openarchives.org/OAI/2.0/oai_dc/': 'oai_dc',
            'http://purl.org/dc/elements/1.1/': 'dc'
        }
    )

    # Convert to BSON
    bson_data = bson.encode(xml_dict)
    
    # Decode back to verify
    decoded_data = bson.decode(bson_data)
    
    # Store single record in MongoDB
    result = collection.insert_one(decoded_data)
    print(f"Stored single record ID: {result.inserted_id}")

except IOError as e:
    print(f"File error: {e}")
except etree.XMLSyntaxError as e:
    print(f"XML parsing error: {e}")
except Exception as e:
    print(f"Error: {e}")


# %%
sickle = Sickle('http://bdr.oai.bsb-muenchen.de/OAIHandler') # no longer in use

# %%
oai_sets = sickle.ListSets()
# for oai_set in oai_sets:
#    print('setSpec value for selective harvesting: ' + oai_set.setSpec)
#    print('Name of the set (setName): ' + oai_set.setName + '\n')

# %%
oai_formats = sickle.ListMetadataFormats()
# for oai_format in oai_formats:
#    print(oai_format.metadataPrefix)

# %%
# Define list of patterns before the loop
patterns = [
    re.compile(r'tafeln?', re.IGNORECASE),
    re.compile(r'tabelle[n|s]?', re.IGNORECASE),
    re.compile(r'tables?', re.IGNORECASE),
    re.compile(r'statisti', re.IGNORECASE),
    re.compile(r'tab[e|u]ul{1,2}a', re.IGNORECASE),
    # add more patterns as needed
    re.compile(r'Merc\.|Cam\.|Num\.rec\.|Num\.anc\.', re.IGNORECASE),
]

# %%
# fourth version with mongoDB
namespaces = {
    'http://www.openarchives.org/OAI/2.0/': 'oai',
    'http://www.openarchives.org/OAI/2.0/oai_dc/': 'oai_dc',
    'http://purl.org/dc/elements/1.1/': 'dc'
}

processed = 0
count = 0

records_to_insert = []
record_count = 0

try:
    for record in sickle.ListRecords(**{'metadataPrefix': 'oai_dc','set': 'all', 'from': '2025-01-01', 'until': '2025-02-13'}): 
        processed += 1
        if any(pattern.search(record.raw.lower()) for pattern in patterns): # find out what is returned in the raw field
            tree = etree.ElementTree(record.xml)
            xml_string = etree.tostring(tree.getroot(), pretty_print=True, encoding='unicode')
            count += 1
            
            records_to_insert.append(xml_string) # add to list
            record_count += 1

            xml_dict = xmltodict.parse(
                xml_string,
                process_namespaces=True,
                namespaces=namespaces
            )

            # Convert to BSON
            bson_data = bson.encode(xml_dict)
            
            # Decode back to verify
            decoded_data = bson.decode(bson_data)
            result = collection.insert_one(decoded_data)
            print(f"Stored single record ID: {result.inserted_id}")

            
    print(f"Total records processed: {record_count}")

except Exception as e:
    print(f"An error occurred: {e}")

print(f"\nTotal records processed: {processed}")
print(f"Total matching records found: {count}")


>>>>>>> 7f66c7c04acfc988496105081eacaa7d72433e18
