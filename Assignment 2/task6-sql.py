#!/usr/bin/env python

import sys
from pyspark.sql import SparkSession
from csv import reader

from pyspark.sql.functions import format_string

spark = SparkSession.builder.appName("task2SQL").getOrCreate()
parking_violation = spark.read.format('csv').options(header='true',inferschema='true').load(sys.argv[1])
parking_violation.createOrReplaceTempView("parking")

violation_count = spark.sql("SELECT plate_id, registration_state, count(violation_code) violation_code_count FROM parking GROUP BY plate_id, registration_state ORDER BY plate_id")
violation_count_temp = violation_count.createOrReplaceTempView("violation_count")
max_violation = spark.sql("SELECT plate_id, registration_state, violation_code_count FROM violation_count ORDER BY violation_code_count DESC LIMIT 20")

max_violation.select(format_string('%s, %s\t%d',max_violation.plate_id ,max_violation.registration_state, max_violation.violation_code_count)).write.save("task6-sql.out",format="text")
