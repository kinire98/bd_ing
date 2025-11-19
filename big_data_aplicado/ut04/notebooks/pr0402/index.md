# PR0402: MapReduce temperaturas


```python
!apt install unzip
!wget --content-disposition -O pr0402/daily-temperature-of-major-cities.zip \
  "https://www.kaggle.com/api/v1/datasets/download/sudalairajkumar/daily-temperature-of-major-cities"

!unzip -o pr0402/daily-temperature-of-major-cities.zip -d ./pr0402
!hdfs dfs -mkdir /temperaturas
!hdfs dfs -put ./pr0402/city_temperature.csv /temperaturas
!hdfs dfs -ls /temperaturas
```

    Reading package lists... Done
    Building dependency tree... Done
    Reading state information... Done
    unzip is already the newest version (6.0-26ubuntu3.2).
    0 upgraded, 0 newly installed, 0 to remove and 139 not upgraded.
    --2025-11-19 10:59:22--  https://www.kaggle.com/api/v1/datasets/download/sudalairajkumar/daily-temperature-of-major-cities
    Resolving www.kaggle.com (www.kaggle.com)... 35.244.233.98
    Connecting to www.kaggle.com (www.kaggle.com)|35.244.233.98|:443... connected.
    HTTP request sent, awaiting response... 302 Found
    Location: https://storage.googleapis.com:443/kaggle-data-sets/694560/1215964/bundle/archive.zip?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=gcp-kaggle-com%40kaggle-161607.iam.gserviceaccount.com%2F20251119%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20251119T105922Z&X-Goog-Expires=259200&X-Goog-SignedHeaders=host&X-Goog-Signature=7cd0922e3c5a4e0062fb4862f970661a919fcff80e76bc00fbf6c95df9a3795636ee945643d6356c493d7df998da7f22fc150a3fac93d206f09620e3626bcf3a85130f24ae417e253baef36727f61a16dcb7c75a1a1b26f572e80a0abbabc4240cd46720bcad3894957842a49bfcc11c99e2a50c52820036526cfc46e8e23c40716e3cd71fa49c6a5ce83c34eefc34af8db38f6926b3b1fd58b483513bceb47241e6d20f0849d40df664f73a2b33ef76567dcc538d2ed063741550474398b7459f3501392e8d3b44b65483ae5966b33a0cbc68ec7925743b1bfb07067011b4ef1bebb6e85b90a7237894008862403a744b3921f57a0a05339b61d6f70015cbf7 [following]
    --2025-11-19 10:59:22--  https://storage.googleapis.com/kaggle-data-sets/694560/1215964/bundle/archive.zip?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=gcp-kaggle-com%40kaggle-161607.iam.gserviceaccount.com%2F20251119%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20251119T105922Z&X-Goog-Expires=259200&X-Goog-SignedHeaders=host&X-Goog-Signature=7cd0922e3c5a4e0062fb4862f970661a919fcff80e76bc00fbf6c95df9a3795636ee945643d6356c493d7df998da7f22fc150a3fac93d206f09620e3626bcf3a85130f24ae417e253baef36727f61a16dcb7c75a1a1b26f572e80a0abbabc4240cd46720bcad3894957842a49bfcc11c99e2a50c52820036526cfc46e8e23c40716e3cd71fa49c6a5ce83c34eefc34af8db38f6926b3b1fd58b483513bceb47241e6d20f0849d40df664f73a2b33ef76567dcc538d2ed063741550474398b7459f3501392e8d3b44b65483ae5966b33a0cbc68ec7925743b1bfb07067011b4ef1bebb6e85b90a7237894008862403a744b3921f57a0a05339b61d6f70015cbf7
    Resolving storage.googleapis.com (storage.googleapis.com)... 216.58.205.219, 172.217.168.187, 142.250.184.27, ...
    Connecting to storage.googleapis.com (storage.googleapis.com)|216.58.205.219|:443... connected.
    HTTP request sent, awaiting response... 200 OK
    Length: 13523007 (13M) [application/zip]
    Saving to: ‘pr0402/daily-temperature-of-major-cities.zip’
    
    pr0402/daily-temper 100%[===================>]  12.90M  12.1MB/s    in 1.1s    
    
    2025-11-19 10:59:23 (12.1 MB/s) - ‘pr0402/daily-temperature-of-major-cities.zip’ saved [13523007/13523007]
    
    Archive:  pr0402/daily-temperature-of-major-cities.zip
      inflating: ./pr0402/city_temperature.csv  
    mkdir: `/temperaturas': File exists
    put: `/temperaturas/city_temperature.csv': File exists
    Found 2 items
    -rw-r--r--   3 root supergroup  140600832 2025-11-18 10:03 /temperaturas/city_temperature.csv
    drwxr-xr-x   - root supergroup          0 2025-11-18 10:21 /temperaturas/salida_ej1


## Ejercicio 1


```python
%%writefile pr0402/ej1_mapper.py
#!/usr/bin/env python3
import sys

first = True
for line in sys.stdin:
    if first:
        first = False
        continue
    values = line.strip().split(",")
    print(f"{values[3]}\t{values[-1]}")
```

    Overwriting pr0402/ej1_mapper.py



```python
%%writefile pr0402/ej1_reducer.py
#!/usr/bin/env python3

import sys
current_city_max_temp = -10000
current_city = None
for line in sys.stdin:
    city, temp = line.strip().split("\t")
    temp = float(temp)
    if city == current_city:
        if temp > current_city_max_temp:
            current_city_max_temp = temp
    else:
        if current_city:
            print(f"{current_city}\t{current_city_max_temp}")
        current_city = city
        current_city_max_temp = temp
if current_city:
    print(f"{current_city}\t{current_city_max_temp}")

    
```

    Overwriting pr0402/ej1_reducer.py



```python
!cat pr0402/city_temperature.csv | python3 pr0402/ej1_mapper.py | sort | python3 pr0402/ej1_reducer.py
```

    Abidjan	88.6
    Abilene	94.2
    Abu Dhabi	107.3
    Addis Ababa	77.0
    Akron Canton	86.1
    Albany	88.0
    Albuquerque	89.4
    Algiers	96.6
    Allentown	91.1
    Almaty	90.9
    Amarillo	92.5
    Amman	95.4
    Amsterdam	85.5
    Anchorage	75.3
    Ankara	87.9
    Antananarivo	78.5
    Ashabad	102.2
    Asheville	85.1
    Athens	94.3
    Atlanta	92.8
    Atlantic City	93.3
    Auckland	75.4
    Austin	94.5
    Baltimore	91.9
    Bangkok	93.0
    Bangui	93.7
    Banjul	93.6
    Barcelona	86.6
    Baton Rouge	90.2
    Beijing	92.9
    Beirut	91.1
    Belfast	77.6
    Belgrade	91.9
    Belize City	92.9
    Bern	83.7
    Bilbao	94.6
    Billings	90.6
    Birmingham	91.0
    Bishkek	91.1
    Bismarck	91.7
    Bissau	100.1
    Bogota	66.7
    Boise	94.2
    Bombay (Mumbai)	92.6
    Bonn	86.9
    Bordeaux	88.8
    Boston	90.7
    Brasilia	87.7
    Bratislava	85.5
    Brazzaville	88.7
    Bridgeport	87.0
    Bridgetown	88.0
    Brisbane	87.3
    Brownsville	91.2
    Brussels	85.4
    Bucharest	91.4
    Budapest	88.2
    Buenos Aires	90.9
    Buffalo	84.4
    Bujumbura	89.1
    Burlington	88.8
    Cairo	100.2
    Calcutta	96.8
    Calgary	79.1
    Canberra	93.2
    Capetown	83.8
    Caracas	89.9
    Caribou	83.4
    Casper	87.1
    Charleston	91.6
    Charlotte	90.4
    Chattanooga	92.7
    Chengdu	90.6
    Chennai (Madras)	97.9
    Cheyenne	84.7
    Chicago	92.3
    Cincinnati	89.2
    Cleveland	87.2
    Colombo	88.3
    Colorado Springs	86.4
    Columbia	92.8
    Columbus	97.7
    Conakry	89.6
    Concord	90.1
    Copenhagen	77.5
    Corpus Christi	93.0
    Cotonou	88.6
    Dakar	87.0
    Dallas Ft Worth	98.2
    Damascus	95.5
    Dar Es Salaam	90.4
    Dayton	91.2
    Daytona Beach	87.8
    Delhi	103.7
    Denver	88.3
    Des Moines	93.0
    Detroit	88.6
    Dhahran	107.8
    Dhaka	91.4
    Doha	108.5
    Dubai	107.5
    Dublin	70.1
    Duluth	85.6
    Dusanbe	97.6
    Edmonton	82.8
    El Paso	98.1
    Elkins	92.5
    Erie	86.4
    Eugene	85.4
    Evansville	91.5
    Fairbanks	79.5
    Fargo	91.4
    Flagstaff	83.5
    Flint	89.4
    Fort Smith	100.7
    Fort Wayne	89.4
    Frankfurt	85.2
    Freetown	88.7
    Fresno	102.6
    Geneva	85.2
    Georgetown	90.6
    Goodland	91.8
    Grand Junction	92.3
    Grand Rapids	89.1
    Great Falls	100.1
    Green Bay	91.3
    Greensboro	90.4
    Guadalajara	88.5
    Guangzhou	94.7
    Guatemala City	79.8
    Guayaquil	90.0
    Halifax	80.5
    Hamburg	89.8
    Hamilton	85.4
    Hanoi	96.0
    Harrisburg	92.0
    Hartford Springfield	89.8
    Havana	88.3
    Helena	89.3
    Helsinki	79.8
    Hong Kong	92.4
    Honolulu	87.2
    Houston	93.0
    Huntsville	91.5
    Indianapolis	94.0
    Islamabad	102.4
    Istanbul	88.7
    Jackson	89.6
    Jacksonville	88.3
    Jakarta	90.6
    Juneau	72.0
    Kampala	82.9
    Kansas City	92.6
    Karachi	99.7
    Katmandu	86.6
    Kiev	86.9
    Knoxville	91.7
    Kuala Lumpur	89.6
    Kuwait	110.0
    La Paz	63.4
    Lagos	93.2
    Lake Charles	94.0
    Lansing	88.1
    Las Vegas	107.0
    Lexington	89.5
    Libreville	86.8
    Lilongwe	90.7
    Lima	81.8
    Lincoln	91.9
    Lisbon	96.3
    Little Rock	95.4
    Lome	90.1
    London	83.4
    Los Angeles	86.0
    Louisville	93.2
    Lubbock	94.1
    Lusaka	93.2
    Macon	91.1
    Madison	90.6
    Madrid	91.0
    Managua	93.9
    Manama	103.3
    Manila	91.9
    Maputo	95.6
    Medford	97.3
    Melbourne	92.8
    Memphis	93.6
    Mexico City	77.0
    Miami Beach	89.2
    Midland Odessa	94.6
    Milan	87.4
    Milwaukee	92.2
    Minneapolis St. Paul	92.0
    Minsk	83.5
    Mobile	88.9
    Monterrey	103.4
    Montgomery	91.2
    Montreal	84.6
    Montvideo	87.4
    Moscow	87.3
    Munich	81.8
    Muscat	105.9
    Nairobi	82.4
    Nashville	94.1
    Nassau	91.8
    New Orleans	90.1
    New York City	93.7
    Newark	95.6
    Niamey	102.8
    Nicosia	102.5
    Norfolk	93.2
    North Platte	91.1
    Nouakchott	99.5
    Oklahoma City	97.1
    Omaha	93.2
    Orlando	89.3
    Osaka	93.0
    Oslo	77.1
    Ottawa	84.9
    Paducah	91.8
    Panama City	90.6
    Paramaribo	90.5
    Paris	91.5
    Peoria	90.5
    Perth	95.2
    Philadelphia	92.9
    Phoenix	107.7
    Pittsburgh	88.4
    Pocatello	90.4
    Port au Prince	97.4
    Portland	89.4
    Prague	83.6
    Pristina	89.6
    Pueblo	94.7
    Pyongyang	89.4
    Quebec	82.9
    Quito	69.0
    Rabat	97.0
    Raleigh Durham	91.0
    Rangoon	99.3
    Rapid City	91.9
    Regina	83.2
    Reno	92.8
    Reykjavik	69.7
    Rhode Island	89.2
    Richmond	93.5
    Riga	81.2
    Rio de Janeiro	93.4
    Riyadh	105.0
    Roanoke	91.1
    Rochester	86.2
    Rockford	90.6
    Rome	85.8
    Sacramento	96.3
    Salem	90.5
    Salt Lake City	92.2
    San Angelo	96.3
    San Antonio	95.4
    San Diego	86.5
    San Francisco	82.7
    San Jose	85.6
    San Juan Puerto Rico	89.2
    Santo Domingo	87.4
    Sao Paulo	89.2
    Sapporo	82.5
    Sault Ste Marie	80.6
    Savannah	89.1
    Seattle	87.7
    Seoul	90.0
    Shanghai	96.8
    Shenyang	90.7
    Shreveport	95.4
    Singapore	88.5
    Sioux City	90.7
    Sioux Falls	94.3
    Skopje	88.0
    Sofia	86.0
    South Bend	89.4
    Spokane	93.2
    Springfield	92.8
    St Louis	96.3
    Stockholm	79.2
    Sydney	96.8
    Syracuse	87.5
    Taipei	94.0
    Tallahassee	92.8
    Tampa St. Petersburg	90.8
    Tashkent	95.4
    Tbilisi	90.6
    Tegucigalpa	88.0
    Tel Aviv	88.5
    Tirana	92.5
    Tokyo	90.6
    Toledo	89.8
    Topeka	95.6
    Toronto	88.8
    Tucson	101.6
    Tulsa	100.4
    Tunis	96.4
    Tupelo	92.8
    Ulan-bator	87.5
    Vancouver	83.1
    Vienna	86.2
    Vientiane	97.0
    Waco	96.1
    Warsaw	84.4
    Washington	92.8
    Washington DC	92.8
    West Palm Beach	89.3
    Wichita	96.1
    Wichita Falls	98.5
    Wilkes Barre	88.4
    Wilmington	89.7
    Windhoek	92.2
    Winnipeg	86.6
    Yakima	97.7
    Yerevan	91.8
    Youngstown	86.7
    Yuma	107.5
    Zagreb	87.5
    Zurich	82.4



```python
!hdfs dfs -rm /temperaturas/salida_ej1/*
!hdfs dfs -rmdir /temperaturas/salida_ej1
!hadoop jar \
/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.4.0.jar \
-file pr0402/ej1_mapper.py \
-mapper pr0402/ej1_mapper.py \
-file pr0402/ej1_reducer.py \
-reducer pr0402/ej1_reducer.py \
-input /temperaturas/city_temperature.csv \
-output /temperaturas/salida_ej1
!hdfs dfs -cat /temperaturas/salida_ej1/part-00000
```

    Deleted /temperaturas/salida_ej1/_SUCCESS
    Deleted /temperaturas/salida_ej1/part-00000
    2025-11-19 10:59:33,909 WARN streaming.StreamJob: -file option is deprecated, please use generic option -files instead.
    packageJobJar: [pr0402/ej1_mapper.py, pr0402/ej1_reducer.py, /tmp/hadoop-unjar7176317682983148700/] [] /tmp/streamjob8533472280804422921.jar tmpDir=null
    2025-11-19 10:59:34,335 INFO client.DefaultNoHARMFailoverProxyProvider: Connecting to ResourceManager at yarnmanager/172.19.0.3:8032
    2025-11-19 10:59:34,458 INFO client.DefaultNoHARMFailoverProxyProvider: Connecting to ResourceManager at yarnmanager/172.19.0.3:8032
    2025-11-19 10:59:34,627 INFO mapreduce.JobResourceUploader: Disabling Erasure Coding for path: /tmp/hadoop-yarn/staging/root/.staging/job_1763549937501_0001
    2025-11-19 10:59:35,621 INFO mapred.FileInputFormat: Total input files to process : 1
    2025-11-19 10:59:35,637 INFO net.NetworkTopology: Adding a new node: /default-rack/172.19.0.6:9866
    2025-11-19 10:59:35,637 INFO net.NetworkTopology: Adding a new node: /default-rack/172.19.0.4:9866
    2025-11-19 10:59:35,637 INFO net.NetworkTopology: Adding a new node: /default-rack/172.19.0.7:9866
    2025-11-19 10:59:35,723 INFO mapreduce.JobSubmitter: number of splits:2
    2025-11-19 10:59:36,245 INFO mapreduce.JobSubmitter: Submitting tokens for job: job_1763549937501_0001
    2025-11-19 10:59:36,245 INFO mapreduce.JobSubmitter: Executing with tokens: []
    2025-11-19 10:59:36,376 INFO conf.Configuration: resource-types.xml not found
    2025-11-19 10:59:36,377 INFO resource.ResourceUtils: Unable to find 'resource-types.xml'.
    2025-11-19 10:59:36,719 INFO impl.YarnClientImpl: Submitted application application_1763549937501_0001
    2025-11-19 10:59:36,750 INFO mapreduce.Job: The url to track the job: http://yarnmanager:8088/proxy/application_1763549937501_0001/
    2025-11-19 10:59:36,751 INFO mapreduce.Job: Running job: job_1763549937501_0001
    2025-11-19 10:59:41,818 INFO mapreduce.Job: Job job_1763549937501_0001 running in uber mode : false
    2025-11-19 10:59:41,819 INFO mapreduce.Job:  map 0% reduce 0%
    2025-11-19 10:59:47,893 INFO mapreduce.Job:  map 100% reduce 0%
    2025-11-19 10:59:55,968 INFO mapreduce.Job:  map 100% reduce 100%
    2025-11-19 10:59:55,978 INFO mapreduce.Job: Job job_1763549937501_0001 completed successfully
    2025-11-19 10:59:56,012 INFO mapreduce.Job: Counters: 55
    	File System Counters
    		FILE: Number of bytes read=47411234
    		FILE: Number of bytes written=95764980
    		FILE: Number of read operations=0
    		FILE: Number of large read operations=0
    		FILE: Number of write operations=0
    		HDFS: Number of bytes read=140605140
    		HDFS: Number of bytes written=4613
    		HDFS: Number of read operations=11
    		HDFS: Number of large read operations=0
    		HDFS: Number of write operations=2
    		HDFS: Number of bytes read erasure-coded=0
    	Job Counters 
    		Launched map tasks=2
    		Launched reduce tasks=1
    		Data-local map tasks=1
    		Rack-local map tasks=1
    		Total time spent by all maps in occupied slots (ms)=7766
    		Total time spent by all reduces in occupied slots (ms)=4930
    		Total time spent by all map tasks (ms)=7766
    		Total time spent by all reduce tasks (ms)=4930
    		Total vcore-milliseconds taken by all map tasks=7766
    		Total vcore-milliseconds taken by all reduce tasks=4930
    		Total megabyte-milliseconds taken by all map tasks=7952384
    		Total megabyte-milliseconds taken by all reduce tasks=5048320
    	Map-Reduce Framework
    		Map input records=2906328
    		Map output records=2906326
    		Map output bytes=41598576
    		Map output materialized bytes=47411240
    		Input split bytes=212
    		Combine input records=0
    		Combine output records=0
    		Reduce input groups=321
    		Reduce shuffle bytes=47411240
    		Reduce input records=2906326
    		Reduce output records=321
    		Spilled Records=5812652
    		Shuffled Maps =2
    		Failed Shuffles=0
    		Merged Map outputs=2
    		GC time elapsed (ms)=225
    		CPU time spent (ms)=6030
    		Physical memory (bytes) snapshot=1038143488
    		Virtual memory (bytes) snapshot=7849746432
    		Total committed heap usage (bytes)=1309671424
    		Peak Map Physical memory (bytes)=323964928
    		Peak Map Virtual memory (bytes)=2614243328
    		Peak Reduce Physical memory (bytes)=393666560
    		Peak Reduce Virtual memory (bytes)=2623184896
    	Shuffle Errors
    		BAD_ID=0
    		CONNECTION=0
    		IO_ERROR=0
    		WRONG_LENGTH=0
    		WRONG_MAP=0
    		WRONG_REDUCE=0
    	File Input Format Counters 
    		Bytes Read=140604928
    	File Output Format Counters 
    		Bytes Written=4613
    2025-11-19 10:59:56,012 INFO streaming.StreamJob: Output directory: /temperaturas/salida_ej1
    Abidjan	88.6
    Abilene	94.2
    Abu Dhabi	107.3
    Addis Ababa	77.0
    Akron Canton	86.1
    Albany	88.0
    Albuquerque	89.4
    Algiers	96.6
    Allentown	91.1
    Almaty	90.9
    Amarillo	92.5
    Amman	95.4
    Amsterdam	85.5
    Anchorage	75.3
    Ankara	87.9
    Antananarivo	78.5
    Ashabad	102.2
    Asheville	85.1
    Athens	94.3
    Atlanta	92.8
    Atlantic City	93.3
    Auckland	75.4
    Austin	94.5
    Baltimore	91.9
    Bangkok	93.0
    Bangui	93.7
    Banjul	93.6
    Barcelona	86.6
    Baton Rouge	90.2
    Beijing	92.9
    Beirut	91.1
    Belfast	77.6
    Belgrade	91.9
    Belize City	92.9
    Bern	83.7
    Bilbao	94.6
    Billings	90.6
    Birmingham	91.0
    Bishkek	91.1
    Bismarck	91.7
    Bissau	100.1
    Bogota	66.7
    Boise	94.2
    Bombay (Mumbai)	92.6
    Bonn	86.9
    Bordeaux	88.8
    Boston	90.7
    Brasilia	87.7
    Bratislava	85.5
    Brazzaville	88.7
    Bridgeport	87.0
    Bridgetown	88.0
    Brisbane	87.3
    Brownsville	91.2
    Brussels	85.4
    Bucharest	91.4
    Budapest	88.2
    Buenos Aires	90.9
    Buffalo	84.4
    Bujumbura	89.1
    Burlington	88.8
    Cairo	100.2
    Calcutta	96.8
    Calgary	79.1
    Canberra	93.2
    Capetown	83.8
    Caracas	89.9
    Caribou	83.4
    Casper	87.1
    Charleston	91.6
    Charlotte	90.4
    Chattanooga	92.7
    Chengdu	90.6
    Chennai (Madras)	97.9
    Cheyenne	84.7
    Chicago	92.3
    Cincinnati	89.2
    Cleveland	87.2
    Colombo	88.3
    Colorado Springs	86.4
    Columbia	92.8
    Columbus	97.7
    Conakry	89.6
    Concord	90.1
    Copenhagen	77.5
    Corpus Christi	93.0
    Cotonou	88.6
    Dakar	87.0
    Dallas Ft Worth	98.2
    Damascus	95.5
    Dar Es Salaam	90.4
    Dayton	91.2
    Daytona Beach	87.8
    Delhi	103.7
    Denver	88.3
    Des Moines	93.0
    Detroit	88.6
    Dhahran	107.8
    Dhaka	91.4
    Doha	108.5
    Dubai	107.5
    Dublin	70.1
    Duluth	85.6
    Dusanbe	97.6
    Edmonton	82.8
    El Paso	98.1
    Elkins	92.5
    Erie	86.4
    Eugene	85.4
    Evansville	91.5
    Fairbanks	79.5
    Fargo	91.4
    Flagstaff	83.5
    Flint	89.4
    Fort Smith	100.7
    Fort Wayne	89.4
    Frankfurt	85.2
    Freetown	88.7
    Fresno	102.6
    Geneva	85.2
    Georgetown	90.6
    Goodland	91.8
    Grand Junction	92.3
    Grand Rapids	89.1
    Great Falls	100.1
    Green Bay	91.3
    Greensboro	90.4
    Guadalajara	88.5
    Guangzhou	94.7
    Guatemala City	79.8
    Guayaquil	90.0
    Halifax	80.5
    Hamburg	89.8
    Hamilton	85.4
    Hanoi	96.0
    Harrisburg	92.0
    Hartford Springfield	89.8
    Havana	88.3
    Helena	89.3
    Helsinki	79.8
    Hong Kong	92.4
    Honolulu	87.2
    Houston	93.0
    Huntsville	91.5
    Indianapolis	94.0
    Islamabad	102.4
    Istanbul	88.7
    Jackson	89.6
    Jacksonville	88.3
    Jakarta	90.6
    Juneau	72.0
    Kampala	82.9
    Kansas City	92.6
    Karachi	99.7
    Katmandu	86.6
    Kiev	86.9
    Knoxville	91.7
    Kuala Lumpur	89.6
    Kuwait	110.0
    La Paz	63.4
    Lagos	93.2
    Lake Charles	94.0
    Lansing	88.1
    Las Vegas	107.0
    Lexington	89.5
    Libreville	86.8
    Lilongwe	90.7
    Lima	81.8
    Lincoln	91.9
    Lisbon	96.3
    Little Rock	95.4
    Lome	90.1
    London	83.4
    Los Angeles	86.0
    Louisville	93.2
    Lubbock	94.1
    Lusaka	93.2
    Macon	91.1
    Madison	90.6
    Madrid	91.0
    Managua	93.9
    Manama	103.3
    Manila	91.9
    Maputo	95.6
    Medford	97.3
    Melbourne	92.8
    Memphis	93.6
    Mexico City	77.0
    Miami Beach	89.2
    Midland Odessa	94.6
    Milan	87.4
    Milwaukee	92.2
    Minneapolis St. Paul	92.0
    Minsk	83.5
    Mobile	88.9
    Monterrey	103.4
    Montgomery	91.2
    Montreal	84.6
    Montvideo	87.4
    Moscow	87.3
    Munich	81.8
    Muscat	105.9
    Nairobi	82.4
    Nashville	94.1
    Nassau	91.8
    New Orleans	90.1
    New York City	93.7
    Newark	95.6
    Niamey	102.8
    Nicosia	102.5
    Norfolk	93.2
    North Platte	91.1
    Nouakchott	99.5
    Oklahoma City	97.1
    Omaha	93.2
    Orlando	89.3
    Osaka	93.0
    Oslo	77.1
    Ottawa	84.9
    Paducah	91.8
    Panama City	90.6
    Paramaribo	90.5
    Paris	91.5
    Peoria	90.5
    Perth	95.2
    Philadelphia	92.9
    Phoenix	107.7
    Pittsburgh	88.4
    Pocatello	90.4
    Port au Prince	97.4
    Portland	89.4
    Prague	83.6
    Pristina	89.6
    Pueblo	94.7
    Pyongyang	89.4
    Quebec	82.9
    Quito	69.0
    Rabat	97.0
    Raleigh Durham	91.0
    Rangoon	99.3
    Rapid City	91.9
    Regina	83.2
    Reno	92.8
    Reykjavik	69.7
    Rhode Island	89.2
    Richmond	93.5
    Riga	81.2
    Rio de Janeiro	93.4
    Riyadh	105.0
    Roanoke	91.1
    Rochester	86.2
    Rockford	90.6
    Rome	85.8
    Sacramento	96.3
    Salem	90.5
    Salt Lake City	92.2
    San Angelo	96.3
    San Antonio	95.4
    San Diego	86.5
    San Francisco	82.7
    San Jose	85.6
    San Juan Puerto Rico	89.2
    Santo Domingo	87.4
    Sao Paulo	89.2
    Sapporo	82.5
    Sault Ste Marie	80.6
    Savannah	89.1
    Seattle	87.7
    Seoul	90.0
    Shanghai	96.8
    Shenyang	90.7
    Shreveport	95.4
    Singapore	88.5
    Sioux City	90.7
    Sioux Falls	94.3
    Skopje	88.0
    Sofia	86.0
    South Bend	89.4
    Spokane	93.2
    Springfield	92.8
    St Louis	96.3
    Stockholm	79.2
    Sydney	96.8
    Syracuse	87.5
    Taipei	94.0
    Tallahassee	92.8
    Tampa St. Petersburg	90.8
    Tashkent	95.4
    Tbilisi	90.6
    Tegucigalpa	88.0
    Tel Aviv	88.5
    Tirana	92.5
    Tokyo	90.6
    Toledo	89.8
    Topeka	95.6
    Toronto	88.8
    Tucson	101.6
    Tulsa	100.4
    Tunis	96.4
    Tupelo	92.8
    Ulan-bator	87.5
    Vancouver	83.1
    Vienna	86.2
    Vientiane	97.0
    Waco	96.1
    Warsaw	84.4
    Washington	92.8
    Washington DC	92.8
    West Palm Beach	89.3
    Wichita	96.1
    Wichita Falls	98.5
    Wilkes Barre	88.4
    Wilmington	89.7
    Windhoek	92.2
    Winnipeg	86.6
    Yakima	97.7
    Yerevan	91.8
    Youngstown	86.7
    Yuma	107.5
    Zagreb	87.5
    Zurich	82.4


## Ejercicio 2


```python
%%writefile pr0402/ej2_mapper.py
#!/usr/bin/env python3
import sys

first = True
for line in sys.stdin:
    if first:
        first = False
        continue
    values = line.strip().split(",")
    print(f"{values[1]}\t{values[-1]}")
```

    Writing pr0402/ej2_mapper.py



```python
%%writefile pr0402/ej2_reducer.py
#!/usr/bin/env python3

import sys
current_temps = []
current_country = None
for line in sys.stdin:
    country, temp = line.strip().split("\t")
    temp = float(temp)
    if country == current_country:
        current_temps.append(temp)
    else:
        if current_country:
            print(f"{current_country}\t{sum(current_temps) / len(current_temps)}")
        current_country = country
        current_temps = []

if current_country:
    print(f"{current_country}\t{sum(current_temps) / len(current_temps)}")
```

    Overwriting pr0402/ej2_reducer.py



```python
!cat pr0402/city_temperature.csv | python3 pr0402/ej2_mapper.py | sort | python3 pr0402/ej2_reducer.py
```

    Albania	33.187188343227135
    Algeria	63.773005936319244
    Argentina	62.322309767943985
    Australia	61.63776036607733
    Austria	51.06342147868317
    Bahamas	76.5919905008634
    Bahrain	80.65498111171082
    Bangladesh	10.128662420382236
    Barbados	77.02312375600164
    Belarus	41.82575839360906
    Belgium	51.073243389098586
    Belize	73.49669617793154
    Benin	76.17103076092805
    Bermuda	67.0003326330534
    Bolivia	44.88267674042095
    Brazil	70.13760972801774
    Bulgaria	45.218909875877074
    Burundi	-65.38974020255363
    Canada	42.005814611281146
    Central African Republic	67.03743119266032
    China	59.9849723709209
    Colombia	55.26060442525617
    Congo	69.33561096718476
    Costa Rica	70.39400971397723
    Croatia	46.94436528497424
    Cuba	72.65933282953719
    Cyprus	23.79920368076451
    Czech Republic	47.60873178629256
    Denmark	46.97620075553146
    Dominican Republic	65.2334844559583
    Egypt	71.97192660550427
    Equador	59.95520990637225
    Ethiopia	25.46864643856241
    Finland	42.248569886670445
    France	54.70486751929204
    Gabon	70.4160855014572
    Gambia	59.684417106033905
    Georgia	46.54928032899247
    Germany	6.426157136516003
    Greece	59.65800121691521
    Guatemala	56.928181327576645
    Guinea	49.40540744738241
    Guinea-Bissau	2.4030652995141817
    Guyana	-22.08633491311225
    Haiti	16.697679939570513
    Honduras	68.54957901554363
    Hong Kong	75.08156502968149
    Hungary	51.115261737722484
    Iceland	41.097884511602636
    India	79.76728455021244
    Indonesia	36.00297927461157
    Ireland	49.08276308688621
    Israel	54.05342672413798
    Italy	57.21880092817414
    Ivory Coast	75.15874797625474
    Japan	55.85554196496028
    Jordan	64.17771181867255
    Kazakhstan	49.32517271157156
    Kenya	23.46699597511906
    Kuwait	79.51372908796539
    Kyrgyzstan	51.379302353945704
    Laos	79.98677819751761
    Latvia	44.14125202374535
    Lebanon	69.4165569347005
    Macedonia	54.02431994818649
    Madagascar	63.46343227199131
    Malawi	-20.57176739283214
    Malaysia	78.97233675121471
    Mauritania	73.43530041641877
    Mexico	47.620647280241805
    Mongolia	29.698294657312548
    Morocco	62.750912034538466
    Mozambique	62.800591715976445
    Myanmar (Burma)	71.53008094981159
    Namibia	58.00728548300059
    Nepal	49.50837651122627
    New Zealand	58.93079330814844
    Nicaragua	71.86976417135473
    Nigeria	62.0009264114666
    North Korea	48.215456017269396
    Norway	40.92763662760544
    Oman	21.902534768954702
    Pakistan	71.66022451292616
    Panama	79.59806799784141
    Peru	66.65516653553627
    Philippines	81.56191041554244
    Poland	47.78125202374533
    Portugal	61.875132218024824
    Qatar	82.2551861845655
    Romania	52.3808418780356
    Russia	44.96940997518219
    Saudi Arabia	79.15991581673916
    Senegal	75.57391257420363
    Serbia-Montenegro	42.4100992410975
    Sierra Leone	-9.805895618556773
    Singapore	81.67390178089514
    Slovakia	51.462698327037145
    South Africa	61.95778737182919
    South Korea	52.883734484619474
    Spain	59.47401877900496
    Sri Lanka	74.26011872639037
    Suriname	47.53072191647806
    Sweden	45.098413383702095
    Switzerland	49.83475195164953
    Syria	62.82358592400722
    Taiwan	69.35204533189409
    Tajikistan	35.16904479222889
    Tanzania	65.32251748251757
    Thailand	72.49197982755813
    The Netherlands	50.834247166756676
    Togo	71.58817053426893
    Tunisia	66.4965029681596
    Turkey	55.186730343748565
    Turkmenistan	62.067069616837465
    US	56.12237057283439
    Uganda	44.157977115716676
    Ukraine	47.6683216405829
    United Arab Emirates	82.59236414656576
    United Kingdom	51.01486158329312
    Uruguay	60.992131678359776
    Uzbekistan	58.823378305450646
    Venezuela	78.34515328152033
    Vietnam	74.75607123583342
    Yugoslavia	54.049357798165246
    Zambia	55.92571469616439



```python
!hdfs dfs -rm /temperaturas/salida_ej2/*
!hdfs dfs -rmdir /temperaturas/salida_ej2
!hadoop jar \
/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.4.0.jar \
-file pr0402/ej2_mapper.py \
-mapper pr0402/ej2_mapper.py \
-file pr0402/ej2_reducer.py \
-reducer pr0402/ej2_reducer.py \
-input /temperaturas/city_temperature.csv \
-output /temperaturas/salida_ej2
!hdfs dfs -cat /temperaturas/salida_ej2/part-00000
```

    rm: `/temperaturas/salida_ej2/*': No such file or directory
    rmdir: `/temperaturas/salida_ej2': No such file or directory
    2025-11-19 11:07:00,147 WARN streaming.StreamJob: -file option is deprecated, please use generic option -files instead.
    packageJobJar: [pr0402/ej2_mapper.py, pr0402/ej2_reducer.py, /tmp/hadoop-unjar5446525201991160942/] [] /tmp/streamjob1479522248997605680.jar tmpDir=null
    2025-11-19 11:07:00,543 INFO client.DefaultNoHARMFailoverProxyProvider: Connecting to ResourceManager at yarnmanager/172.19.0.3:8032
    2025-11-19 11:07:00,613 INFO client.DefaultNoHARMFailoverProxyProvider: Connecting to ResourceManager at yarnmanager/172.19.0.3:8032
    2025-11-19 11:07:00,781 INFO mapreduce.JobResourceUploader: Disabling Erasure Coding for path: /tmp/hadoop-yarn/staging/root/.staging/job_1763549937501_0002
    2025-11-19 11:07:01,073 INFO mapred.FileInputFormat: Total input files to process : 1
    2025-11-19 11:07:01,085 INFO net.NetworkTopology: Adding a new node: /default-rack/172.19.0.4:9866
    2025-11-19 11:07:01,085 INFO net.NetworkTopology: Adding a new node: /default-rack/172.19.0.6:9866
    2025-11-19 11:07:01,086 INFO net.NetworkTopology: Adding a new node: /default-rack/172.19.0.7:9866
    2025-11-19 11:07:01,168 INFO mapreduce.JobSubmitter: number of splits:2
    2025-11-19 11:07:01,261 INFO mapreduce.JobSubmitter: Submitting tokens for job: job_1763549937501_0002
    2025-11-19 11:07:01,261 INFO mapreduce.JobSubmitter: Executing with tokens: []
    2025-11-19 11:07:01,388 INFO conf.Configuration: resource-types.xml not found
    2025-11-19 11:07:01,388 INFO resource.ResourceUtils: Unable to find 'resource-types.xml'.
    2025-11-19 11:07:01,432 INFO impl.YarnClientImpl: Submitted application application_1763549937501_0002
    2025-11-19 11:07:01,453 INFO mapreduce.Job: The url to track the job: http://yarnmanager:8088/proxy/application_1763549937501_0002/
    2025-11-19 11:07:01,454 INFO mapreduce.Job: Running job: job_1763549937501_0002
    2025-11-19 11:07:05,514 INFO mapreduce.Job: Job job_1763549937501_0002 running in uber mode : false
    2025-11-19 11:07:05,515 INFO mapreduce.Job:  map 0% reduce 0%
    2025-11-19 11:07:10,568 INFO mapreduce.Job:  map 50% reduce 0%
    2025-11-19 11:07:11,572 INFO mapreduce.Job:  map 100% reduce 0%
    2025-11-19 11:07:16,603 INFO mapreduce.Job:  map 100% reduce 100%
    2025-11-19 11:07:16,614 INFO mapreduce.Job: Job job_1763549937501_0002 completed successfully
    2025-11-19 11:07:16,658 INFO mapreduce.Job: Counters: 54
    	File System Counters
    		FILE: Number of bytes read=37383711
    		FILE: Number of bytes written=75709934
    		FILE: Number of read operations=0
    		FILE: Number of large read operations=0
    		FILE: Number of write operations=0
    		HDFS: Number of bytes read=140605140
    		HDFS: Number of bytes written=3389
    		HDFS: Number of read operations=11
    		HDFS: Number of large read operations=0
    		HDFS: Number of write operations=2
    		HDFS: Number of bytes read erasure-coded=0
    	Job Counters 
    		Launched map tasks=2
    		Launched reduce tasks=1
    		Data-local map tasks=2
    		Total time spent by all maps in occupied slots (ms)=6643
    		Total time spent by all reduces in occupied slots (ms)=3784
    		Total time spent by all map tasks (ms)=6643
    		Total time spent by all reduce tasks (ms)=3784
    		Total vcore-milliseconds taken by all map tasks=6643
    		Total vcore-milliseconds taken by all reduce tasks=3784
    		Total megabyte-milliseconds taken by all map tasks=6802432
    		Total megabyte-milliseconds taken by all reduce tasks=3874816
    	Map-Reduce Framework
    		Map input records=2906328
    		Map output records=2906326
    		Map output bytes=31571053
    		Map output materialized bytes=37383717
    		Input split bytes=212
    		Combine input records=0
    		Combine output records=0
    		Reduce input groups=125
    		Reduce shuffle bytes=37383717
    		Reduce input records=2906326
    		Reduce output records=125
    		Spilled Records=5812652
    		Shuffled Maps =2
    		Failed Shuffles=0
    		Merged Map outputs=2
    		GC time elapsed (ms)=257
    		CPU time spent (ms)=6560
    		Physical memory (bytes) snapshot=1321504768
    		Virtual memory (bytes) snapshot=7847178240
    		Total committed heap usage (bytes)=1690304512
    		Peak Map Physical memory (bytes)=607612928
    		Peak Map Virtual memory (bytes)=2614665216
    		Peak Reduce Physical memory (bytes)=396771328
    		Peak Reduce Virtual memory (bytes)=2620653568
    	Shuffle Errors
    		BAD_ID=0
    		CONNECTION=0
    		IO_ERROR=0
    		WRONG_LENGTH=0
    		WRONG_MAP=0
    		WRONG_REDUCE=0
    	File Input Format Counters 
    		Bytes Read=140604928
    	File Output Format Counters 
    		Bytes Written=3389
    2025-11-19 11:07:16,658 INFO streaming.StreamJob: Output directory: /temperaturas/salida_ej2
    Albania	33.16910955207772
    Algeria	63.75539125742014
    Argentina	62.306605504587175
    Australia	61.6344816421677
    Austria	51.04570966001088
    Bahamas	76.57229058721927
    Bahrain	80.6342039935243
    Bangladesh	10.0979686693062
    Barbados	77.00194356632714
    Belarus	41.81947533196609
    Belgium	51.05584457636272
    Belize	73.47757503778901
    Benin	76.15181867242286
    Bermuda	66.97095588235308
    Bolivia	44.866540744738266
    Brazil	70.13141099438789
    Bulgaria	45.200831084727376
    Burundi	-65.38974020255375
    Canada	42.005286622487816
    Central African Republic	67.01817593092272
    China	59.98345277154279
    Colombia	55.24393955747434
    Congo	69.31629965457671
    Costa Rica	70.37493793847815
    Croatia	46.927018566493985
    Cuba	72.64050523588455
    Cyprus	23.799203680764528
    Czech Republic	47.603864004317245
    Denmark	46.959611440906556
    Dominican Republic	65.21448618307429
    Egypt	71.97192660550459
    Equador	59.944258532165335
    Ethiopia	25.45192597374648
    Finland	42.24505126821354
    France	54.696303491446834
    Gabon	70.39681528662429
    Gambia	59.66347978910334
    Georgia	46.51825451222274
    Germany	6.426157136515891
    Greece	59.635473075752884
    Guatemala	56.9107609282245
    Guinea	49.386152185644974
    Guinea-Bissau	2.3831300593631948
    Guyana	-22.08633491311216
    Haiti	16.67796482140942
    Honduras	68.5314227115714
    Hong Kong	75.06146788990813
    Hungary	51.097733405288565
    Iceland	41.08101457096603
    India	79.76235227456577
    Indonesia	35.98321459412776
    Ireland	49.065882352941
    Israel	54.01465517241393
    Italy	57.20981598402675
    Ivory Coast	75.13927684835389
    Japan	55.85416771594067
    Jordan	64.15894225580152
    Kazakhstan	49.32252806563032
    Kenya	23.44504207830224
    Kuwait	79.49653534808422
    Kyrgyzstan	51.37177704598162
    Laos	79.9675445223963
    Latvia	44.13760388559091
    Lebanon	69.3987911494876
    Macedonia	54.00806347150268
    Madagascar	63.44471667566092
    Malawi	-20.57176739283201
    Malaysia	78.9532541824066
    Mauritania	73.41453896490175
    Mexico	47.61432578050057
    Mongolia	29.690760928224577
    Morocco	62.7340852671343
    Mozambique	62.78274341043591
    Myanmar (Burma)	71.5105882352939
    Namibia	57.98845116028046
    Nepal	49.490630397236615
    New Zealand	58.91326497571506
    Nicaragua	71.85012981393321
    Nigeria	61.990636835052065
    North Korea	48.20714516999454
    Norway	40.921424867779656
    Oman	21.881864064602897
    Pakistan	71.6511468508822
    Panama	79.57869400971379
    Peru	66.63238919485948
    Philippines	81.54273070696159
    Poland	47.77816513761448
    Portugal	61.85815434430645
    Qatar	82.23752833243398
    Romania	52.36787911494886
    Russia	44.96309342726755
    Saudi Arabia	79.1512762398143
    Senegal	75.55609282244997
    Serbia-Montenegro	42.39334500875657
    Sierra Leone	-9.80589561855666
    Singapore	81.65392336751219
    Slovakia	51.446745817593005
    South Africa	61.93956826767391
    South Korea	52.878791149487384
    Spain	59.46845702773628
    Sri Lanka	74.24049649217473
    Suriname	47.511416855509005
    Sweden	45.09406368051824
    Switzerland	49.828387955534765
    Syria	62.804253022452436
    Taiwan	69.33206691851034
    Tajikistan	35.153642741500335
    Tanzania	65.32251748251761
    Thailand	72.49197982755824
    The Netherlands	50.818208310847254
    Togo	71.56852671343762
    Tunisia	66.4788451160281
    Turkey	55.17745939236972
    Turkmenistan	62.04801942795472
    US	56.12229576008368
    Uganda	44.139443005181356
    Ukraine	47.664090663788365
    United Arab Emirates	82.58205169715627
    United Kingdom	51.00680481355586
    Uruguay	60.973502428494434
    Uzbekistan	58.80372369131165
    Venezuela	78.32582037996553
    Vietnam	74.74056125202378
    Yugoslavia	54.0301996762007
    Zambia	55.903174831202406


### Ejercicio 3   

Se puede reutilizar el `mapper` del ejercicio 1


```python
%%writefile pr0402/ej3_reducer.py
#!/usr/bin/env python3

import sys
current_count = 0
current_city = None
for line in sys.stdin:
    city, temp = line.strip().split("\t")
    temp = float(temp)
    if city == current_city:
        temp_in_celsius = (temp - 32) / (9/5)
        if temp_in_celsius > 30:
            current_count += 1
    else:
        if current_city:
            print(f"{current_city}\t{current_count}")
        current_city = city
        current_count = 0

if current_city:
    print(f"{current_city}\t{current_count}")
```

    Overwriting pr0402/ej3_reducer.py



```python
!cat pr0402/city_temperature.csv | python3 pr0402/ej1_mapper.py | sort | python3 pr0402/ej3_reducer.py
```

    Abidjan	92
    Abilene	628
    Abu Dhabi	4275
    Addis Ababa	0
    Akron Canton	2
    Albany	2
    Albuquerque	38
    Algiers	58
    Allentown	10
    Almaty	42
    Amarillo	113
    Amman	174
    Amsterdam	0
    Anchorage	0
    Ankara	4
    Antananarivo	0
    Ashabad	1525
    Asheville	0
    Athens	289
    Atlanta	64
    Atlantic City	37
    Auckland	0
    Austin	590
    Baltimore	54
    Bangkok	1559
    Bangui	179
    Banjul	72
    Barcelona	2
    Baton Rouge	65
    Beijing	130
    Beirut	53
    Belfast	0
    Belgrade	39
    Belize City	660
    Bern	0
    Bilbao	7
    Billings	17
    Birmingham	95
    Bishkek	88
    Bismarck	8
    Bissau	571
    Bogota	0
    Boise	97
    Bombay (Mumbai)	1297
    Bonn	1
    Bordeaux	7
    Boston	19
    Brasilia	1
    Bratislava	0
    Brazzaville	16
    Bridgeport	4
    Bridgetown	8
    Brisbane	1
    Brownsville	472
    Brussels	0
    Bucharest	9
    Budapest	3
    Buenos Aires	26
    Buffalo	0
    Bujumbura	6
    Burlington	4
    Cairo	800
    Calcutta	1938
    Calgary	0
    Canberra	16
    Capetown	0
    Caracas	177
    Caribou	0
    Casper	1
    Charleston	83
    Charlotte	38
    Chattanooga	46
    Chengdu	90
    Chennai (Madras)	2971
    Cheyenne	0
    Chicago	29
    Cincinnati	14
    Cleveland	4
    Colombo	128
    Colorado Springs	1
    Columbia	196
    Columbus	182
    Conakry	204
    Concord	2
    Copenhagen	0
    Corpus Christi	407
    Cotonou	361
    Dakar	5
    Dallas Ft Worth	1128
    Damascus	225
    Dar Es Salaam	56
    Dayton	8
    Daytona Beach	13
    Delhi	2891
    Denver	3
    Des Moines	51
    Detroit	9
    Dhahran	4110
    Dhaka	412
    Doha	4382
    Dubai	4444
    Dublin	0
    Duluth	0
    Dusanbe	287
    Edmonton	0
    El Paso	789
    Elkins	3
    Erie	1
    Eugene	0
    Evansville	50
    Fairbanks	0
    Fargo	4
    Flagstaff	0
    Flint	2
    Fort Smith	414
    Fort Wayne	6
    Frankfurt	0
    Freetown	74
    Fresno	620
    Geneva	0
    Georgetown	221
    Goodland	30
    Grand Junction	81
    Grand Rapids	9
    Great Falls	5
    Green Bay	2
    Greensboro	24
    Guadalajara	1
    Guangzhou	1003
    Guatemala City	0
    Guayaquil	16
    Halifax	0
    Hamburg	3
    Hamilton	0
    Hanoi	893
    Harrisburg	18
    Hartford Springfield	15
    Havana	8
    Helena	2
    Helsinki	0
    Hong Kong	1207
    Honolulu	5
    Houston	470
    Huntsville	51
    Indianapolis	20
    Islamabad	1575
    Istanbul	10
    Jackson	99
    Jacksonville	24
    Jakarta	527
    Juneau	0
    Kampala	0
    Kansas City	109
    Karachi	2485
    Katmandu	2
    Kiev	2
    Knoxville	10
    Kuala Lumpur	345
    Kuwait	4035
    La Paz	0
    Lagos	282
    Lake Charles	149
    Lansing	3
    Las Vegas	2342
    Lexington	9
    Libreville	3
    Lilongwe	5
    Lima	0
    Lincoln	95
    Lisbon	46
    Little Rock	341
    Lome	244
    London	0
    Los Angeles	0
    Louisville	89
    Lubbock	259
    Lusaka	64
    Macon	71
    Madison	10
    Madrid	113
    Managua	626
    Manama	4090
    Manila	955
    Maputo	130
    Medford	48
    Melbourne	14
    Memphis	332
    Mexico City	0
    Miami Beach	165
    Midland Odessa	638
    Milan	2
    Milwaukee	16
    Minneapolis St. Paul	37
    Minsk	0
    Mobile	37
    Monterrey	2004
    Montgomery	95
    Montreal	0
    Montvideo	1
    Moscow	4
    Munich	0
    Muscat	2206
    Nairobi	0
    Nashville	59
    Nassau	509
    New Orleans	232
    New York City	102
    Newark	93
    Niamey	4574
    Nicosia	375
    Norfolk	81
    North Platte	24
    Nouakchott	811
    Oklahoma City	356
    Omaha	95
    Orlando	23
    Osaka	523
    Oslo	0
    Ottawa	0
    Paducah	49
    Panama City	112
    Paramaribo	47
    Paris	10
    Peoria	25
    Perth	153
    Philadelphia	72
    Phoenix	3008
    Pittsburgh	4
    Pocatello	4
    Port au Prince	2378
    Portland	5
    Prague	0
    Pristina	2
    Pueblo	27
    Pyongyang	12
    Quebec	0
    Quito	0
    Rabat	21
    Raleigh Durham	55
    Rangoon	1227
    Rapid City	28
    Regina	0
    Reno	36
    Reykjavik	0
    Rhode Island	9
    Richmond	68
    Riga	0
    Rio de Janeiro	168
    Riyadh	3886
    Roanoke	12
    Rochester	1
    Rockford	12
    Rome	0
    Sacramento	40
    Salem	5
    Salt Lake City	205
    San Angelo	779
    San Antonio	654
    San Diego	1
    San Francisco	0
    San Jose	0
    San Juan Puerto Rico	16
    Santo Domingo	33
    Sao Paulo	2
    Sapporo	0
    Sault Ste Marie	0
    Savannah	93
    Seattle	2
    Seoul	36
    Shanghai	663
    Shenyang	9
    Shreveport	451
    Singapore	218
    Sioux City	27
    Sioux Falls	22
    Skopje	17
    Sofia	0
    South Bend	10
    Spokane	8
    Springfield	107
    St Louis	258
    Stockholm	0
    Sydney	52
    Syracuse	3
    Taipei	1012
    Tallahassee	83
    Tampa St. Petersburg	100
    Tashkent	645
    Tbilisi	25
    Tegucigalpa	7
    Tel Aviv	6
    Tirana	42
    Tokyo	65
    Toledo	7
    Topeka	254
    Toronto	5
    Tucson	1554
    Tulsa	585
    Tunis	323
    Tupelo	118
    Ulan-bator	3
    Vancouver	0
    Vienna	1
    Vientiane	1250
    Waco	984
    Warsaw	0
    Washington	248
    Washington DC	248
    West Palm Beach	92
    Wichita	330
    Wichita Falls	825
    Wilkes Barre	2
    Wilmington	16
    Windhoek	40
    Winnipeg	2
    Yakima	35
    Yerevan	53
    Youngstown	1
    Yuma	1319
    Zagreb	8
    Zurich	0



```python
!hdfs dfs -rm /temperaturas/salida_ej3/*
!hdfs dfs -rmdir /temperaturas/salida_ej3
!hadoop jar \
/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.4.0.jar \
-file pr0402/ej1_mapper.py \
-mapper pr0402/ej1_mapper.py \
-file pr0402/ej3_reducer.py \
-reducer pr0402/ej3_reducer.py \
-input /temperaturas/city_temperature.csv \
-output /temperaturas/salida_ej3
!hdfs dfs -cat /temperaturas/salida_ej3/part-00000
```

    rm: `/temperaturas/salida_ej3/*': No such file or directory
    rmdir: `/temperaturas/salida_ej3': No such file or directory
    2025-11-19 11:18:11,910 WARN streaming.StreamJob: -file option is deprecated, please use generic option -files instead.
    packageJobJar: [pr0402/ej1_mapper.py, pr0402/ej3_reducer.py, /tmp/hadoop-unjar1862348233375108768/] [] /tmp/streamjob7938068666038933389.jar tmpDir=null
    2025-11-19 11:18:12,339 INFO client.DefaultNoHARMFailoverProxyProvider: Connecting to ResourceManager at yarnmanager/172.19.0.3:8032
    2025-11-19 11:18:12,446 INFO client.DefaultNoHARMFailoverProxyProvider: Connecting to ResourceManager at yarnmanager/172.19.0.3:8032
    2025-11-19 11:18:12,569 INFO mapreduce.JobResourceUploader: Disabling Erasure Coding for path: /tmp/hadoop-yarn/staging/root/.staging/job_1763549937501_0003
    2025-11-19 11:18:12,842 INFO mapred.FileInputFormat: Total input files to process : 1
    2025-11-19 11:18:12,852 INFO net.NetworkTopology: Adding a new node: /default-rack/172.19.0.7:9866
    2025-11-19 11:18:12,852 INFO net.NetworkTopology: Adding a new node: /default-rack/172.19.0.4:9866
    2025-11-19 11:18:12,852 INFO net.NetworkTopology: Adding a new node: /default-rack/172.19.0.6:9866
    2025-11-19 11:18:12,928 INFO mapreduce.JobSubmitter: number of splits:2
    2025-11-19 11:18:13,024 INFO mapreduce.JobSubmitter: Submitting tokens for job: job_1763549937501_0003
    2025-11-19 11:18:13,025 INFO mapreduce.JobSubmitter: Executing with tokens: []
    2025-11-19 11:18:13,125 INFO conf.Configuration: resource-types.xml not found
    2025-11-19 11:18:13,125 INFO resource.ResourceUtils: Unable to find 'resource-types.xml'.
    2025-11-19 11:18:13,168 INFO impl.YarnClientImpl: Submitted application application_1763549937501_0003
    2025-11-19 11:18:13,189 INFO mapreduce.Job: The url to track the job: http://yarnmanager:8088/proxy/application_1763549937501_0003/
    2025-11-19 11:18:13,190 INFO mapreduce.Job: Running job: job_1763549937501_0003
    2025-11-19 11:18:17,253 INFO mapreduce.Job: Job job_1763549937501_0003 running in uber mode : false
    2025-11-19 11:18:17,254 INFO mapreduce.Job:  map 0% reduce 0%
    2025-11-19 11:18:23,334 INFO mapreduce.Job:  map 100% reduce 0%
    2025-11-19 11:18:29,403 INFO mapreduce.Job:  map 100% reduce 100%
    2025-11-19 11:18:30,425 INFO mapreduce.Job: Job job_1763549937501_0003 completed successfully
    2025-11-19 11:18:30,489 INFO mapreduce.Job: Counters: 55
    	File System Counters
    		FILE: Number of bytes read=47411234
    		FILE: Number of bytes written=95764980
    		FILE: Number of read operations=0
    		FILE: Number of large read operations=0
    		FILE: Number of write operations=0
    		HDFS: Number of bytes read=140605140
    		HDFS: Number of bytes written=3949
    		HDFS: Number of read operations=11
    		HDFS: Number of large read operations=0
    		HDFS: Number of write operations=2
    		HDFS: Number of bytes read erasure-coded=0
    	Job Counters 
    		Launched map tasks=2
    		Launched reduce tasks=1
    		Data-local map tasks=1
    		Rack-local map tasks=1
    		Total time spent by all maps in occupied slots (ms)=7167
    		Total time spent by all reduces in occupied slots (ms)=4502
    		Total time spent by all map tasks (ms)=7167
    		Total time spent by all reduce tasks (ms)=4502
    		Total vcore-milliseconds taken by all map tasks=7167
    		Total vcore-milliseconds taken by all reduce tasks=4502
    		Total megabyte-milliseconds taken by all map tasks=7339008
    		Total megabyte-milliseconds taken by all reduce tasks=4610048
    	Map-Reduce Framework
    		Map input records=2906328
    		Map output records=2906326
    		Map output bytes=41598576
    		Map output materialized bytes=47411240
    		Input split bytes=212
    		Combine input records=0
    		Combine output records=0
    		Reduce input groups=321
    		Reduce shuffle bytes=47411240
    		Reduce input records=2906326
    		Reduce output records=321
    		Spilled Records=5812652
    		Shuffled Maps =2
    		Failed Shuffles=0
    		Merged Map outputs=2
    		GC time elapsed (ms)=257
    		CPU time spent (ms)=6990
    		Physical memory (bytes) snapshot=1332834304
    		Virtual memory (bytes) snapshot=7850975232
    		Total committed heap usage (bytes)=1639448576
    		Peak Map Physical memory (bytes)=612577280
    		Peak Map Virtual memory (bytes)=2614095872
    		Peak Reduce Physical memory (bytes)=396611584
    		Peak Reduce Virtual memory (bytes)=2623139840
    	Shuffle Errors
    		BAD_ID=0
    		CONNECTION=0
    		IO_ERROR=0
    		WRONG_LENGTH=0
    		WRONG_MAP=0
    		WRONG_REDUCE=0
    	File Input Format Counters 
    		Bytes Read=140604928
    	File Output Format Counters 
    		Bytes Written=3949
    2025-11-19 11:18:30,489 INFO streaming.StreamJob: Output directory: /temperaturas/salida_ej3
    Abidjan	92
    Abilene	628
    Abu Dhabi	4274
    Addis Ababa	0
    Akron Canton	2
    Albany	2
    Albuquerque	38
    Algiers	58
    Allentown	10
    Almaty	42
    Amarillo	113
    Amman	174
    Amsterdam	0
    Anchorage	0
    Ankara	4
    Antananarivo	0
    Ashabad	1524
    Asheville	0
    Athens	289
    Atlanta	64
    Atlantic City	37
    Auckland	0
    Austin	590
    Baltimore	54
    Bangkok	1559
    Bangui	179
    Banjul	72
    Barcelona	2
    Baton Rouge	65
    Beijing	130
    Beirut	53
    Belfast	0
    Belgrade	39
    Belize City	660
    Bern	0
    Bilbao	7
    Billings	17
    Birmingham	95
    Bishkek	88
    Bismarck	8
    Bissau	571
    Bogota	0
    Boise	97
    Bombay (Mumbai)	1296
    Bonn	1
    Bordeaux	7
    Boston	19
    Brasilia	1
    Bratislava	0
    Brazzaville	16
    Bridgeport	4
    Bridgetown	8
    Brisbane	1
    Brownsville	472
    Brussels	0
    Bucharest	9
    Budapest	3
    Buenos Aires	26
    Buffalo	0
    Bujumbura	6
    Burlington	4
    Cairo	800
    Calcutta	1938
    Calgary	0
    Canberra	16
    Capetown	0
    Caracas	177
    Caribou	0
    Casper	1
    Charleston	83
    Charlotte	38
    Chattanooga	46
    Chengdu	90
    Chennai (Madras)	2971
    Cheyenne	0
    Chicago	29
    Cincinnati	14
    Cleveland	4
    Colombo	128
    Colorado Springs	1
    Columbia	196
    Columbus	182
    Conakry	204
    Concord	2
    Copenhagen	0
    Corpus Christi	407
    Cotonou	361
    Dakar	5
    Dallas Ft Worth	1128
    Damascus	225
    Dar Es Salaam	56
    Dayton	8
    Daytona Beach	13
    Delhi	2891
    Denver	3
    Des Moines	51
    Detroit	9
    Dhahran	4110
    Dhaka	412
    Doha	4382
    Dubai	4444
    Dublin	0
    Duluth	0
    Dusanbe	287
    Edmonton	0
    El Paso	789
    Elkins	3
    Erie	1
    Eugene	0
    Evansville	50
    Fairbanks	0
    Fargo	4
    Flagstaff	0
    Flint	2
    Fort Smith	414
    Fort Wayne	6
    Frankfurt	0
    Freetown	74
    Fresno	620
    Geneva	0
    Georgetown	221
    Goodland	30
    Grand Junction	81
    Grand Rapids	9
    Great Falls	5
    Green Bay	2
    Greensboro	24
    Guadalajara	1
    Guangzhou	1003
    Guatemala City	0
    Guayaquil	16
    Halifax	0
    Hamburg	3
    Hamilton	0
    Hanoi	893
    Harrisburg	18
    Hartford Springfield	15
    Havana	8
    Helena	2
    Helsinki	0
    Hong Kong	1207
    Honolulu	5
    Houston	470
    Huntsville	51
    Indianapolis	20
    Islamabad	1575
    Istanbul	10
    Jackson	99
    Jacksonville	24
    Jakarta	527
    Juneau	0
    Kampala	0
    Kansas City	109
    Karachi	2485
    Katmandu	2
    Kiev	2
    Knoxville	10
    Kuala Lumpur	345
    Kuwait	4034
    La Paz	0
    Lagos	282
    Lake Charles	149
    Lansing	3
    Las Vegas	2342
    Lexington	9
    Libreville	3
    Lilongwe	5
    Lima	0
    Lincoln	95
    Lisbon	46
    Little Rock	341
    Lome	244
    London	0
    Los Angeles	0
    Louisville	89
    Lubbock	259
    Lusaka	64
    Macon	71
    Madison	10
    Madrid	113
    Managua	626
    Manama	4089
    Manila	955
    Maputo	130
    Medford	48
    Melbourne	14
    Memphis	332
    Mexico City	0
    Miami Beach	165
    Midland Odessa	638
    Milan	2
    Milwaukee	16
    Minneapolis St. Paul	37
    Minsk	0
    Mobile	37
    Monterrey	2004
    Montgomery	95
    Montreal	0
    Montvideo	1
    Moscow	4
    Munich	0
    Muscat	2206
    Nairobi	0
    Nashville	59
    Nassau	509
    New Orleans	232
    New York City	102
    Newark	93
    Niamey	4573
    Nicosia	375
    Norfolk	81
    North Platte	24
    Nouakchott	811
    Oklahoma City	356
    Omaha	95
    Orlando	23
    Osaka	523
    Oslo	0
    Ottawa	0
    Paducah	49
    Panama City	112
    Paramaribo	47
    Paris	10
    Peoria	25
    Perth	153
    Philadelphia	72
    Phoenix	3008
    Pittsburgh	4
    Pocatello	4
    Port au Prince	2377
    Portland	5
    Prague	0
    Pristina	2
    Pueblo	27
    Pyongyang	12
    Quebec	0
    Quito	0
    Rabat	21
    Raleigh Durham	54
    Rangoon	1227
    Rapid City	28
    Regina	0
    Reno	36
    Reykjavik	0
    Rhode Island	9
    Richmond	68
    Riga	0
    Rio de Janeiro	168
    Riyadh	3886
    Roanoke	12
    Rochester	1
    Rockford	12
    Rome	0
    Sacramento	40
    Salem	5
    Salt Lake City	204
    San Angelo	779
    San Antonio	654
    San Diego	1
    San Francisco	0
    San Jose	0
    San Juan Puerto Rico	16
    Santo Domingo	33
    Sao Paulo	2
    Sapporo	0
    Sault Ste Marie	0
    Savannah	93
    Seattle	2
    Seoul	36
    Shanghai	663
    Shenyang	9
    Shreveport	451
    Singapore	218
    Sioux City	27
    Sioux Falls	22
    Skopje	17
    Sofia	0
    South Bend	10
    Spokane	8
    Springfield	107
    St Louis	258
    Stockholm	0
    Sydney	52
    Syracuse	3
    Taipei	1012
    Tallahassee	83
    Tampa St. Petersburg	100
    Tashkent	645
    Tbilisi	25
    Tegucigalpa	7
    Tel Aviv	6
    Tirana	42
    Tokyo	65
    Toledo	7
    Topeka	254
    Toronto	5
    Tucson	1554
    Tulsa	585
    Tunis	323
    Tupelo	118
    Ulan-bator	3
    Vancouver	0
    Vienna	1
    Vientiane	1250
    Waco	984
    Warsaw	0
    Washington	248
    Washington DC	248
    West Palm Beach	92
    Wichita	330
    Wichita Falls	825
    Wilkes Barre	2
    Wilmington	16
    Windhoek	40
    Winnipeg	2
    Yakima	35
    Yerevan	53
    Youngstown	1
    Yuma	1318
    Zagreb	8
    Zurich	0


## Ejercicio 4

Se puede volver a reutilizar el mapper del ejercicio 1. El reducer también es muy similar al de ese ejercicio.


```python
%%writefile pr0402/ej4_reducer.py
#!/usr/bin/env python3

import sys
current_city_max_temp = -10000
current_city_min_temp = 10000
current_city = None
for line in sys.stdin:
    city, temp = line.strip().split("\t")
    temp = float(temp)
    if city == current_city:
        if temp > current_city_max_temp:
            current_city_max_temp = temp
        if temp < current_city_min_temp and temp != -99.0:
            current_city_min_temp = temp
    else:
        if current_city:
            print(f"{current_city}\t({current_city_min_temp}/{current_city_max_temp})")
        current_city = city
        current_city_max_temp = temp
        if temp != -99.0:
            current_city_min_temp = temp
        else:
            current_city_min_temp = 10000

if current_city:
    print(f"{current_city}\t({current_city_min_temp}/{current_city_max_temp})")
```

    Overwriting pr0402/ej4_reducer.py



```python
!cat pr0402/city_temperature.csv | python3 pr0402/ej1_mapper.py | sort | python3 pr0402/ej4_reducer.py
```

    Abidjan	(40.3/88.6)
    Abilene	(13.5/94.2)
    Abu Dhabi	(55.8/107.3)
    Addis Ababa	(50.4/77.0)
    Akron Canton	(-6.1/86.1)
    Albany	(-5.4/88.0)
    Albuquerque	(3.0/89.4)
    Algiers	(33.3/96.6)
    Allentown	(4.0/91.1)
    Almaty	(-14.2/90.9)
    Amarillo	(2.1/92.5)
    Amman	(33.3/95.4)
    Amsterdam	(11.0/85.5)
    Anchorage	(-19.6/75.3)
    Ankara	(3.2/87.9)
    Antananarivo	(33.8/78.5)
    Ashabad	(6.8/102.2)
    Asheville	(6.6/85.1)
    Athens	(28.4/94.3)
    Atlanta	(13.7/92.8)
    Atlantic City	(4.6/93.3)
    Auckland	(41.1/75.4)
    Austin	(22.1/94.5)
    Baltimore	(9.0/91.9)
    Bangkok	(63.0/93.0)
    Bangui	(59.9/93.7)
    Banjul	(64.6/93.6)
    Barcelona	(32.6/86.6)
    Baton Rouge	(22.5/90.2)
    Beijing	(5.2/92.9)
    Beirut	(44.5/91.1)
    Belfast	(12.5/77.6)
    Belgrade	(1.4/91.9)
    Belize City	(64.6/92.9)
    Bern	(4.7/83.7)
    Bilbao	(30.8/94.6)
    Billings	(-22.0/90.6)
    Birmingham	(11.1/91.0)
    Bishkek	(-10.8/91.1)
    Bismarck	(-28.1/91.7)
    Bissau	(65.4/100.1)
    Bogota	(46.7/66.7)
    Boise	(-0.5/94.2)
    Bombay (Mumbai)	(63.4/92.6)
    Bonn	(4.7/86.9)
    Bordeaux	(21.7/88.8)
    Boston	(0.2/90.7)
    Brasilia	(56.1/87.7)
    Bratislava	(5.6/85.5)
    Brazzaville	(61.2/88.7)
    Bridgeport	(3.2/87.0)
    Bridgetown	(74.2/88.0)
    Brisbane	(45.6/87.3)
    Brownsville	(31.4/91.2)
    Brussels	(8.8/85.4)
    Bucharest	(1.9/91.4)
    Budapest	(7.3/88.2)
    Buenos Aires	(35.3/90.9)
    Buffalo	(-4.6/84.4)
    Bujumbura	(48.2/89.1)
    Burlington	(-14.1/88.8)
    Cairo	(45.2/100.2)
    Calcutta	(52.9/96.8)
    Calgary	(-27.9/79.1)
    Canberra	(30.7/93.2)
    Capetown	(44.9/83.8)
    Caracas	(71.5/89.9)
    Caribou	(-20.9/83.4)
    Casper	(-18.1/87.1)
    Charleston	(1.8/91.6)
    Charlotte	(15.6/90.4)
    Chattanooga	(10.3/92.7)
    Chengdu	(31.9/90.6)
    Chennai (Madras)	(69.7/97.9)
    Cheyenne	(-12.0/84.7)
    Chicago	(-16.4/92.3)
    Cincinnati	(-2.2/89.2)
    Cleveland	(-5.9/87.2)
    Colombo	(70.3/88.3)
    Colorado Springs	(-7.7/86.4)
    Columbia	(21.8/92.8)
    Columbus	(-3.8/97.7)
    Conakry	(65.2/89.6)
    Concord	(-5.0/90.1)
    Copenhagen	(9.3/77.5)
    Corpus Christi	(29.5/93.0)
    Cotonou	(56.4/88.6)
    Dakar	(63.2/87.0)
    Dallas Ft Worth	(16.1/98.2)
    Damascus	(26.8/95.5)
    Dar Es Salaam	(65.0/90.4)
    Dayton	(-6.6/91.2)
    Daytona Beach	(32.5/87.8)
    Delhi	(43.9/103.7)
    Denver	(-11.0/88.3)
    Des Moines	(-17.8/93.0)
    Detroit	(-12.4/88.6)
    Dhahran	(46.1/107.8)
    Dhaka	(54.3/91.4)
    Doha	(49.6/108.5)
    Dubai	(58.7/107.5)
    Dublin	(17.1/70.1)
    Duluth	(-29.8/85.6)
    Dusanbe	(7.5/97.6)
    Edmonton	(-29.2/82.8)
    El Paso	(8.4/98.1)
    Elkins	(-4.2/92.5)
    Erie	(-5.9/86.4)
    Eugene	(4.2/85.4)
    Evansville	(-0.7/91.5)
    Fairbanks	(-50.0/79.5)
    Fargo	(-29.5/91.4)
    Flagstaff	(10.2/83.5)
    Flint	(-13.2/89.4)
    Fort Smith	(11.9/100.7)
    Fort Wayne	(-10.4/89.4)
    Frankfurt	(13.0/85.2)
    Freetown	(57.8/88.7)
    Fresno	(27.6/102.6)
    Geneva	(15.3/85.2)
    Georgetown	(67.0/90.6)
    Goodland	(-5.6/91.8)
    Grand Junction	(-2.3/92.3)
    Grand Rapids	(-7.3/89.1)
    Great Falls	(-24.1/100.1)
    Green Bay	(-21.2/91.3)
    Greensboro	(10.8/90.4)
    Guadalajara	(45.8/88.5)
    Guangzhou	(38.7/94.7)
    Guatemala City	(51.2/79.8)
    Guayaquil	(67.2/90.0)
    Halifax	(-7.8/80.5)
    Hamburg	(13.5/89.8)
    Hamilton	(51.1/85.4)
    Hanoi	(44.7/96.0)
    Harrisburg	(8.7/92.0)
    Hartford Springfield	(-2.1/89.8)
    Havana	(46.9/88.3)
    Helena	(-26.4/89.3)
    Helsinki	(-13.6/79.8)
    Hong Kong	(40.2/92.4)
    Honolulu	(65.7/87.2)
    Houston	(25.9/93.0)
    Huntsville	(7.8/91.5)
    Indianapolis	(-7.8/94.0)
    Islamabad	(36.2/102.4)
    Istanbul	(24.1/88.7)
    Jackson	(15.1/89.6)
    Jacksonville	(28.7/88.3)
    Jakarta	(71.3/90.6)
    Juneau	(-4.1/72.0)
    Kampala	(64.4/82.9)
    Kansas City	(-6.1/92.6)
    Karachi	(52.2/99.7)
    Katmandu	(36.6/86.6)
    Kiev	(-11.1/86.9)
    Knoxville	(4.9/91.7)
    Kuala Lumpur	(73.4/89.6)
    Kuwait	(41.4/110.0)
    La Paz	(32.8/63.4)
    Lagos	(71.6/93.2)
    Lake Charles	(26.4/94.0)
    Lansing	(-13.4/88.1)
    Las Vegas	(30.4/107.0)
    Lexington	(-0.9/89.5)
    Libreville	(40.6/86.8)
    Lilongwe	(50.9/90.7)
    Lima	(57.5/81.8)
    Lincoln	(-12.0/91.9)
    Lisbon	(39.0/96.3)
    Little Rock	(12.5/95.4)
    Lome	(69.6/90.1)
    London	(24.6/83.4)
    Los Angeles	(44.8/86.0)
    Louisville	(1.7/93.2)
    Lubbock	(6.7/94.1)
    Lusaka	(47.8/93.2)
    Macon	(18.8/91.1)
    Madison	(-20.0/90.6)
    Madrid	(24.9/91.0)
    Managua	(68.5/93.9)
    Manama	(50.5/103.3)
    Manila	(70.9/91.9)
    Maputo	(53.2/95.6)
    Medford	(13.1/97.3)
    Melbourne	(45.7/92.8)
    Memphis	(10.1/93.6)
    Mexico City	(43.0/77.0)
    Miami Beach	(40.0/89.2)
    Midland Odessa	(11.4/94.6)
    Milan	(14.3/87.4)
    Milwaukee	(-16.6/92.2)
    Minneapolis St. Paul	(-23.8/92.0)
    Minsk	(-15.8/83.5)
    Mobile	(21.9/88.9)
    Monterrey	(28.6/103.4)
    Montgomery	(18.4/91.2)
    Montreal	(-14.4/84.6)
    Montvideo	(35.7/87.4)
    Moscow	(-20.4/87.3)
    Munich	(1.8/81.8)
    Muscat	(60.7/105.9)
    Nairobi	(51.8/82.4)
    Nashville	(4.4/94.1)
    Nassau	(58.7/91.8)
    New Orleans	(26.1/90.1)
    New York City	(8.3/93.7)
    Newark	(7.6/95.6)
    Niamey	(63.5/102.8)
    Nicosia	(33.9/102.5)
    Norfolk	(14.8/93.2)
    North Platte	(-9.0/91.1)
    Nouakchott	(58.3/99.5)
    Oklahoma City	(7.2/97.1)
    Omaha	(-13.4/93.2)
    Orlando	(34.7/89.3)
    Osaka	(27.8/93.0)
    Oslo	(-8.7/77.1)
    Ottawa	(-15.4/84.9)
    Paducah	(1.6/91.8)
    Panama City	(73.4/90.6)
    Paramaribo	(71.6/90.5)
    Paris	(13.8/91.5)
    Peoria	(-13.7/90.5)
    Perth	(43.1/95.2)
    Philadelphia	(9.4/92.9)
    Phoenix	(37.3/107.7)
    Pittsburgh	(-4.6/88.4)
    Pocatello	(-9.2/90.4)
    Port au Prince	(71.4/97.4)
    Portland	(-3.7/89.4)
    Prague	(-3.1/83.6)
    Pristina	(-3.3/89.6)
    Pueblo	(-7.3/94.7)
    Pyongyang	(-4.7/89.4)
    Quebec	(-20.5/82.9)
    Quito	(49.1/69.0)
    Rabat	(33.8/97.0)
    Raleigh Durham	(11.6/91.0)
    Rangoon	(50.9/99.3)
    Rapid City	(-19.0/91.9)
    Regina	(-36.5/83.2)
    Reno	(5.4/92.8)
    Reykjavik	(10.6/69.7)
    Rhode Island	(0.3/89.2)
    Richmond	(9.8/93.5)
    Riga	(-12.1/81.2)
    Rio de Janeiro	(60.0/93.4)
    Riyadh	(38.0/105.0)
    Roanoke	(7.9/91.1)
    Rochester	(-2.3/86.2)
    Rockford	(-20.0/90.6)
    Rome	(31.0/85.8)
    Sacramento	(29.8/96.3)
    Salem	(17.9/90.5)
    Salt Lake City	(2.8/92.2)
    San Angelo	(16.5/96.3)
    San Antonio	(23.0/95.4)
    San Diego	(45.1/86.5)
    San Francisco	(38.3/82.7)
    San Jose	(63.1/85.6)
    San Juan Puerto Rico	(69.7/89.2)
    Santo Domingo	(65.0/87.4)
    Sao Paulo	(44.8/89.2)
    Sapporo	(-1.7/82.5)
    Sault Ste Marie	(-15.1/80.6)
    Savannah	(26.7/89.1)
    Seattle	(20.1/87.7)
    Seoul	(-0.6/90.0)
    Shanghai	(21.8/96.8)
    Shenyang	(-17.0/90.7)
    Shreveport	(20.3/95.4)
    Singapore	(73.3/88.5)
    Sioux City	(-16.3/90.7)
    Sioux Falls	(-22.2/94.3)
    Skopje	(0.3/88.0)
    Sofia	(2.6/86.0)
    South Bend	(-15.6/89.4)
    Spokane	(-9.4/93.2)
    Springfield	(-11.8/92.8)
    St Louis	(-5.2/96.3)
    Stockholm	(-5.0/79.2)
    Sydney	(39.5/96.8)
    Syracuse	(-9.8/87.5)
    Taipei	(41.5/94.0)
    Tallahassee	(27.0/92.8)
    Tampa St. Petersburg	(34.0/90.8)
    Tashkent	(3.8/95.4)
    Tbilisi	(14.7/90.6)
    Tegucigalpa	(56.1/88.0)
    Tel Aviv	(45.1/88.5)
    Tirana	(24.9/92.5)
    Tokyo	(32.3/90.6)
    Toledo	(-10.1/89.8)
    Topeka	(-2.7/95.6)
    Toronto	(-5.4/88.8)
    Tucson	(27.6/101.6)
    Tulsa	(4.2/100.4)
    Tunis	(36.6/96.4)
    Tupelo	(10.6/92.8)
    Ulan-bator	(-37.2/87.5)
    Vancouver	(14.2/83.1)
    Vienna	(3.8/86.2)
    Vientiane	(51.4/97.0)
    Waco	(18.5/96.1)
    Warsaw	(-8.1/84.4)
    Washington	(11.9/92.8)
    Washington DC	(11.9/92.8)
    West Palm Beach	(38.5/89.3)
    Wichita	(1.3/96.1)
    Wichita Falls	(10.6/98.5)
    Wilkes Barre	(-1.0/88.4)
    Wilmington	(7.6/89.7)
    Windhoek	(38.8/92.2)
    Winnipeg	(-35.7/86.6)
    Yakima	(-5.9/97.7)
    Yerevan	(-8.8/91.8)
    Youngstown	(-6.4/86.7)
    Yuma	(45.3/107.5)
    Zagreb	(10.2/87.5)
    Zurich	(7.8/82.4)



```python
!hdfs dfs -rm /temperaturas/salida_ej4/*
!hdfs dfs -rmdir /temperaturas/salida_ej4
!hadoop jar \
/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.4.0.jar \
-file pr0402/ej1_mapper.py \
-mapper pr0402/ej1_mapper.py \
-file pr0402/ej4_reducer.py \
-reducer pr0402/ej4_reducer.py \
-input /temperaturas/city_temperature.csv \
-output /temperaturas/salida_ej4
!hdfs dfs -cat /temperaturas/salida_ej4/part-00000
```

    rm: `/temperaturas/salida_ej4/*': No such file or directory
    rmdir: `/temperaturas/salida_ej4': No such file or directory
    2025-11-19 11:24:11,036 WARN streaming.StreamJob: -file option is deprecated, please use generic option -files instead.
    packageJobJar: [pr0402/ej1_mapper.py, pr0402/ej4_reducer.py, /tmp/hadoop-unjar8784177987011928528/] [] /tmp/streamjob3271888188041382994.jar tmpDir=null
    2025-11-19 11:24:11,431 INFO client.DefaultNoHARMFailoverProxyProvider: Connecting to ResourceManager at yarnmanager/172.19.0.3:8032
    2025-11-19 11:24:11,543 INFO client.DefaultNoHARMFailoverProxyProvider: Connecting to ResourceManager at yarnmanager/172.19.0.3:8032
    2025-11-19 11:24:11,677 INFO mapreduce.JobResourceUploader: Disabling Erasure Coding for path: /tmp/hadoop-yarn/staging/root/.staging/job_1763549937501_0004
    2025-11-19 11:24:11,942 INFO mapred.FileInputFormat: Total input files to process : 1
    2025-11-19 11:24:11,955 INFO net.NetworkTopology: Adding a new node: /default-rack/172.19.0.6:9866
    2025-11-19 11:24:11,955 INFO net.NetworkTopology: Adding a new node: /default-rack/172.19.0.4:9866
    2025-11-19 11:24:11,955 INFO net.NetworkTopology: Adding a new node: /default-rack/172.19.0.7:9866
    2025-11-19 11:24:12,025 INFO mapreduce.JobSubmitter: number of splits:2
    2025-11-19 11:24:12,124 INFO mapreduce.JobSubmitter: Submitting tokens for job: job_1763549937501_0004
    2025-11-19 11:24:12,124 INFO mapreduce.JobSubmitter: Executing with tokens: []
    2025-11-19 11:24:12,242 INFO conf.Configuration: resource-types.xml not found
    2025-11-19 11:24:12,243 INFO resource.ResourceUtils: Unable to find 'resource-types.xml'.
    2025-11-19 11:24:12,291 INFO impl.YarnClientImpl: Submitted application application_1763549937501_0004
    2025-11-19 11:24:12,315 INFO mapreduce.Job: The url to track the job: http://yarnmanager:8088/proxy/application_1763549937501_0004/
    2025-11-19 11:24:12,316 INFO mapreduce.Job: Running job: job_1763549937501_0004
    2025-11-19 11:24:16,372 INFO mapreduce.Job: Job job_1763549937501_0004 running in uber mode : false
    2025-11-19 11:24:16,372 INFO mapreduce.Job:  map 0% reduce 0%
    2025-11-19 11:24:21,423 INFO mapreduce.Job:  map 50% reduce 0%
    2025-11-19 11:24:22,433 INFO mapreduce.Job:  map 100% reduce 0%
    2025-11-19 11:24:27,469 INFO mapreduce.Job:  map 100% reduce 100%
    2025-11-19 11:24:27,480 INFO mapreduce.Job: Job job_1763549937501_0004 completed successfully
    2025-11-19 11:24:27,539 INFO mapreduce.Job: Counters: 56
    	File System Counters
    		FILE: Number of bytes read=47411234
    		FILE: Number of bytes written=95764980
    		FILE: Number of read operations=0
    		FILE: Number of large read operations=0
    		FILE: Number of write operations=0
    		HDFS: Number of bytes read=140605140
    		HDFS: Number of bytes written=6862
    		HDFS: Number of read operations=11
    		HDFS: Number of large read operations=0
    		HDFS: Number of write operations=2
    		HDFS: Number of bytes read erasure-coded=0
    	Job Counters 
    		Killed map tasks=1
    		Launched map tasks=2
    		Launched reduce tasks=1
    		Data-local map tasks=1
    		Rack-local map tasks=1
    		Total time spent by all maps in occupied slots (ms)=7270
    		Total time spent by all reduces in occupied slots (ms)=3337
    		Total time spent by all map tasks (ms)=7270
    		Total time spent by all reduce tasks (ms)=3337
    		Total vcore-milliseconds taken by all map tasks=7270
    		Total vcore-milliseconds taken by all reduce tasks=3337
    		Total megabyte-milliseconds taken by all map tasks=7444480
    		Total megabyte-milliseconds taken by all reduce tasks=3417088
    	Map-Reduce Framework
    		Map input records=2906328
    		Map output records=2906326
    		Map output bytes=41598576
    		Map output materialized bytes=47411240
    		Input split bytes=212
    		Combine input records=0
    		Combine output records=0
    		Reduce input groups=321
    		Reduce shuffle bytes=47411240
    		Reduce input records=2906326
    		Reduce output records=321
    		Spilled Records=5812652
    		Shuffled Maps =2
    		Failed Shuffles=0
    		Merged Map outputs=2
    		GC time elapsed (ms)=258
    		CPU time spent (ms)=7020
    		Physical memory (bytes) snapshot=1335615488
    		Virtual memory (bytes) snapshot=7849578496
    		Total committed heap usage (bytes)=1673003008
    		Peak Map Physical memory (bytes)=609329152
    		Peak Map Virtual memory (bytes)=2614087680
    		Peak Reduce Physical memory (bytes)=404242432
    		Peak Reduce Virtual memory (bytes)=2624589824
    	Shuffle Errors
    		BAD_ID=0
    		CONNECTION=0
    		IO_ERROR=0
    		WRONG_LENGTH=0
    		WRONG_MAP=0
    		WRONG_REDUCE=0
    	File Input Format Counters 
    		Bytes Read=140604928
    	File Output Format Counters 
    		Bytes Written=6862
    2025-11-19 11:24:27,539 INFO streaming.StreamJob: Output directory: /temperaturas/salida_ej4
    Abidjan	(40.3/88.6)
    Abilene	(13.5/94.2)
    Abu Dhabi	(55.8/107.3)
    Addis Ababa	(50.4/77.0)
    Akron Canton	(-6.1/86.1)
    Albany	(-5.4/88.0)
    Albuquerque	(3.0/89.4)
    Algiers	(33.3/96.6)
    Allentown	(4.0/91.1)
    Almaty	(-14.2/90.9)
    Amarillo	(2.1/92.5)
    Amman	(33.3/95.4)
    Amsterdam	(11.0/85.5)
    Anchorage	(-19.6/75.3)
    Ankara	(3.2/87.9)
    Antananarivo	(33.8/78.5)
    Ashabad	(6.8/102.2)
    Asheville	(6.6/85.1)
    Athens	(28.4/94.3)
    Atlanta	(13.7/92.8)
    Atlantic City	(4.6/93.3)
    Auckland	(41.1/75.4)
    Austin	(22.1/94.5)
    Baltimore	(9.0/91.9)
    Bangkok	(63.0/93.0)
    Bangui	(59.9/93.7)
    Banjul	(64.6/93.6)
    Barcelona	(32.6/86.6)
    Baton Rouge	(22.5/90.2)
    Beijing	(5.2/92.9)
    Beirut	(44.5/91.1)
    Belfast	(12.5/77.6)
    Belgrade	(1.4/91.9)
    Belize City	(64.6/92.9)
    Bern	(4.7/83.7)
    Bilbao	(30.8/94.6)
    Billings	(-22.0/90.6)
    Birmingham	(11.1/91.0)
    Bishkek	(-10.8/91.1)
    Bismarck	(-28.1/91.7)
    Bissau	(65.4/100.1)
    Bogota	(46.7/66.7)
    Boise	(-0.5/94.2)
    Bombay (Mumbai)	(63.4/92.6)
    Bonn	(4.7/86.9)
    Bordeaux	(21.7/88.8)
    Boston	(0.2/90.7)
    Brasilia	(56.1/87.7)
    Bratislava	(5.6/85.5)
    Brazzaville	(61.2/88.7)
    Bridgeport	(3.2/87.0)
    Bridgetown	(74.2/88.0)
    Brisbane	(45.6/87.3)
    Brownsville	(31.4/91.2)
    Brussels	(8.8/85.4)
    Bucharest	(1.9/91.4)
    Budapest	(7.3/88.2)
    Buenos Aires	(35.3/90.9)
    Buffalo	(-4.6/84.4)
    Bujumbura	(48.2/89.1)
    Burlington	(-14.1/88.8)
    Cairo	(45.2/100.2)
    Calcutta	(52.9/96.8)
    Calgary	(-27.9/79.1)
    Canberra	(30.7/93.2)
    Capetown	(44.9/83.8)
    Caracas	(71.5/89.9)
    Caribou	(-20.9/83.4)
    Casper	(-18.1/87.1)
    Charleston	(1.8/91.6)
    Charlotte	(15.6/90.4)
    Chattanooga	(10.3/92.7)
    Chengdu	(31.9/90.6)
    Chennai (Madras)	(69.7/97.9)
    Cheyenne	(-12.0/84.7)
    Chicago	(-16.4/92.3)
    Cincinnati	(-2.2/89.2)
    Cleveland	(-5.9/87.2)
    Colombo	(70.3/88.3)
    Colorado Springs	(-7.7/86.4)
    Columbia	(21.8/92.8)
    Columbus	(-3.8/97.7)
    Conakry	(65.2/89.6)
    Concord	(-5.0/90.1)
    Copenhagen	(9.3/77.5)
    Corpus Christi	(29.5/93.0)
    Cotonou	(56.4/88.6)
    Dakar	(63.2/87.0)
    Dallas Ft Worth	(16.1/98.2)
    Damascus	(26.8/95.5)
    Dar Es Salaam	(65.0/90.4)
    Dayton	(-6.6/91.2)
    Daytona Beach	(32.5/87.8)
    Delhi	(43.9/103.7)
    Denver	(-11.0/88.3)
    Des Moines	(-17.8/93.0)
    Detroit	(-12.4/88.6)
    Dhahran	(46.1/107.8)
    Dhaka	(54.3/91.4)
    Doha	(49.6/108.5)
    Dubai	(58.7/107.5)
    Dublin	(17.1/70.1)
    Duluth	(-29.8/85.6)
    Dusanbe	(7.5/97.6)
    Edmonton	(-29.2/82.8)
    El Paso	(8.4/98.1)
    Elkins	(-4.2/92.5)
    Erie	(-5.9/86.4)
    Eugene	(4.2/85.4)
    Evansville	(-0.7/91.5)
    Fairbanks	(-50.0/79.5)
    Fargo	(-29.5/91.4)
    Flagstaff	(10.2/83.5)
    Flint	(-13.2/89.4)
    Fort Smith	(11.9/100.7)
    Fort Wayne	(-10.4/89.4)
    Frankfurt	(13.0/85.2)
    Freetown	(57.8/88.7)
    Fresno	(27.6/102.6)
    Geneva	(15.3/85.2)
    Georgetown	(67.0/90.6)
    Goodland	(-5.6/91.8)
    Grand Junction	(-2.3/92.3)
    Grand Rapids	(-7.3/89.1)
    Great Falls	(-24.1/100.1)
    Green Bay	(-21.2/91.3)
    Greensboro	(10.8/90.4)
    Guadalajara	(45.8/88.5)
    Guangzhou	(38.7/94.7)
    Guatemala City	(51.2/79.8)
    Guayaquil	(67.2/90.0)
    Halifax	(-7.8/80.5)
    Hamburg	(13.5/89.8)
    Hamilton	(51.1/85.4)
    Hanoi	(44.7/96.0)
    Harrisburg	(8.7/92.0)
    Hartford Springfield	(-2.1/89.8)
    Havana	(46.9/88.3)
    Helena	(-26.4/89.3)
    Helsinki	(-13.6/79.8)
    Hong Kong	(40.2/92.4)
    Honolulu	(65.7/87.2)
    Houston	(25.9/93.0)
    Huntsville	(7.8/91.5)
    Indianapolis	(-7.8/94.0)
    Islamabad	(36.2/102.4)
    Istanbul	(24.1/88.7)
    Jackson	(15.1/89.6)
    Jacksonville	(28.7/88.3)
    Jakarta	(71.3/90.6)
    Juneau	(-4.1/72.0)
    Kampala	(64.4/82.9)
    Kansas City	(-6.1/92.6)
    Karachi	(52.2/99.7)
    Katmandu	(36.6/86.6)
    Kiev	(-11.1/86.9)
    Knoxville	(4.9/91.7)
    Kuala Lumpur	(73.4/89.6)
    Kuwait	(41.4/110.0)
    La Paz	(32.8/63.4)
    Lagos	(71.6/93.2)
    Lake Charles	(26.4/94.0)
    Lansing	(-13.4/88.1)
    Las Vegas	(30.4/107.0)
    Lexington	(-0.9/89.5)
    Libreville	(40.6/86.8)
    Lilongwe	(50.9/90.7)
    Lima	(57.5/81.8)
    Lincoln	(-12.0/91.9)
    Lisbon	(39.0/96.3)
    Little Rock	(12.5/95.4)
    Lome	(69.6/90.1)
    London	(24.6/83.4)
    Los Angeles	(44.8/86.0)
    Louisville	(1.7/93.2)
    Lubbock	(6.7/94.1)
    Lusaka	(47.8/93.2)
    Macon	(18.8/91.1)
    Madison	(-20.0/90.6)
    Madrid	(24.9/91.0)
    Managua	(68.5/93.9)
    Manama	(50.5/103.3)
    Manila	(70.9/91.9)
    Maputo	(53.2/95.6)
    Medford	(13.1/97.3)
    Melbourne	(45.7/92.8)
    Memphis	(10.1/93.6)
    Mexico City	(43.0/77.0)
    Miami Beach	(40.0/89.2)
    Midland Odessa	(11.4/94.6)
    Milan	(14.3/87.4)
    Milwaukee	(-16.6/92.2)
    Minneapolis St. Paul	(-23.8/92.0)
    Minsk	(-15.8/83.5)
    Mobile	(21.9/88.9)
    Monterrey	(28.6/103.4)
    Montgomery	(18.4/91.2)
    Montreal	(-14.4/84.6)
    Montvideo	(35.7/87.4)
    Moscow	(-20.4/87.3)
    Munich	(1.8/81.8)
    Muscat	(60.7/105.9)
    Nairobi	(51.8/82.4)
    Nashville	(4.4/94.1)
    Nassau	(58.7/91.8)
    New Orleans	(26.1/90.1)
    New York City	(8.3/93.7)
    Newark	(7.6/95.6)
    Niamey	(63.5/102.8)
    Nicosia	(33.9/102.5)
    Norfolk	(14.8/93.2)
    North Platte	(-9.0/91.1)
    Nouakchott	(58.3/99.5)
    Oklahoma City	(7.2/97.1)
    Omaha	(-13.4/93.2)
    Orlando	(34.7/89.3)
    Osaka	(27.8/93.0)
    Oslo	(-8.7/77.1)
    Ottawa	(-15.4/84.9)
    Paducah	(1.6/91.8)
    Panama City	(73.4/90.6)
    Paramaribo	(71.6/90.5)
    Paris	(13.8/91.5)
    Peoria	(-13.7/90.5)
    Perth	(43.1/95.2)
    Philadelphia	(9.4/92.9)
    Phoenix	(37.3/107.7)
    Pittsburgh	(-4.6/88.4)
    Pocatello	(-9.2/90.4)
    Port au Prince	(71.4/97.4)
    Portland	(-3.7/89.4)
    Prague	(-3.1/83.6)
    Pristina	(-3.3/89.6)
    Pueblo	(-7.3/94.7)
    Pyongyang	(-4.7/89.4)
    Quebec	(-20.5/82.9)
    Quito	(49.1/69.0)
    Rabat	(33.8/97.0)
    Raleigh Durham	(11.6/91.0)
    Rangoon	(50.9/99.3)
    Rapid City	(-19.0/91.9)
    Regina	(-36.5/83.2)
    Reno	(5.4/92.8)
    Reykjavik	(10.6/69.7)
    Rhode Island	(0.3/89.2)
    Richmond	(9.8/93.5)
    Riga	(-12.1/81.2)
    Rio de Janeiro	(60.0/93.4)
    Riyadh	(38.0/105.0)
    Roanoke	(7.9/91.1)
    Rochester	(-2.3/86.2)
    Rockford	(-20.0/90.6)
    Rome	(31.0/85.8)
    Sacramento	(29.8/96.3)
    Salem	(17.9/90.5)
    Salt Lake City	(2.8/92.2)
    San Angelo	(16.5/96.3)
    San Antonio	(23.0/95.4)
    San Diego	(45.1/86.5)
    San Francisco	(38.3/82.7)
    San Jose	(63.1/85.6)
    San Juan Puerto Rico	(69.7/89.2)
    Santo Domingo	(65.0/87.4)
    Sao Paulo	(44.8/89.2)
    Sapporo	(-1.7/82.5)
    Sault Ste Marie	(-15.1/80.6)
    Savannah	(26.7/89.1)
    Seattle	(20.1/87.7)
    Seoul	(-0.6/90.0)
    Shanghai	(21.8/96.8)
    Shenyang	(-17.0/90.7)
    Shreveport	(20.3/95.4)
    Singapore	(73.3/88.5)
    Sioux City	(-16.3/90.7)
    Sioux Falls	(-22.2/94.3)
    Skopje	(0.3/88.0)
    Sofia	(2.6/86.0)
    South Bend	(-15.6/89.4)
    Spokane	(-9.4/93.2)
    Springfield	(-11.8/92.8)
    St Louis	(-5.2/96.3)
    Stockholm	(-5.0/79.2)
    Sydney	(39.5/96.8)
    Syracuse	(-9.8/87.5)
    Taipei	(41.5/94.0)
    Tallahassee	(27.0/92.8)
    Tampa St. Petersburg	(34.0/90.8)
    Tashkent	(3.8/95.4)
    Tbilisi	(14.7/90.6)
    Tegucigalpa	(56.1/88.0)
    Tel Aviv	(45.1/88.5)
    Tirana	(24.9/92.5)
    Tokyo	(32.3/90.6)
    Toledo	(-10.1/89.8)
    Topeka	(-2.7/95.6)
    Toronto	(-5.4/88.8)
    Tucson	(27.6/101.6)
    Tulsa	(4.2/100.4)
    Tunis	(36.6/96.4)
    Tupelo	(10.6/92.8)
    Ulan-bator	(-37.2/87.5)
    Vancouver	(14.2/83.1)
    Vienna	(3.8/86.2)
    Vientiane	(51.4/97.0)
    Waco	(18.5/96.1)
    Warsaw	(-8.1/84.4)
    Washington	(11.9/92.8)
    Washington DC	(11.9/92.8)
    West Palm Beach	(38.5/89.3)
    Wichita	(1.3/96.1)
    Wichita Falls	(10.6/98.5)
    Wilkes Barre	(-1.0/88.4)
    Wilmington	(7.6/89.7)
    Windhoek	(38.8/92.2)
    Winnipeg	(-35.7/86.6)
    Yakima	(-5.9/97.7)
    Yerevan	(-8.8/91.8)
    Youngstown	(-6.4/86.7)
    Yuma	(45.3/107.5)
    Zagreb	(10.2/87.5)
    Zurich	(7.8/82.4)

