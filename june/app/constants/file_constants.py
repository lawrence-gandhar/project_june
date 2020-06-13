#
# AUTHOR : LAWRENCE GANDHAR
# 

#==========================================================================
#   MEMORY UNITS
#==========================================================================
#

MU_BYTE = 0
MU_KB = 1
MU_MB = 2
MU_GB = 3
MU_TB = 4

MEMORY_UNITS = (
    (MU_BYTE, 'Byte'),
    (MU_KB, 'Kilo Byte'),
    (MU_MB, 'Mega Byte'),
    (MU_GB, 'Giga Byte'),
    (MU_TB, 'Tera Byte'),
)

#==========================================================================
#   DATATYPES
#==========================================================================
#

DT_STRING = 0
DT_INTEGER = 1
DT_FLOAT = 2

DTYPES = (
    (DT_STRING, 'STRING'),
    (DT_INTEGER, 'INTEGERS'),
    (DT_FLOAT, 'FLOAT'),
)

#==========================================================================
#   COLUMN CHECK
#==========================================================================
#

COLC_STRICT = 0
COLC_MODERATE = 1
COLC_NA = 2

COLUMN_CHECK = (
    (COLC_STRICT, 'STRICT'),
    (COLC_MODERATE, 'MODERATE'),
    (COLC_NA, 'NO ACTION'),
)

#==========================================================================
#   COLUMN CHECK
#==========================================================================
#


CVF_ANY = 0
CVF_ALPHA = 1
CVF_ALPHA_NUM = 2
CVF_INT = 3
CVF_P_INT = 4
CVF_N_INT = 5
CVF_FLOAT = 6
CVF_P_FLOAT = 7
CVF_N_FLOAT = 8
CVF_BOOL = 9
CVF_DATE = 10
CVF_DATETIME = 11

COLUMN_VALID_FOR = (
    (CVF_ANY, 'Any'),
    (CVF_ALPHA, 'Only Alphabets'),
    (CVF_ALPHA_NUM, 'Alphanumeric'),
    (CVF_INT, 'Integers'),
    (CVF_P_INT, 'Only Positive Integers'),
    (CVF_N_INT, 'Only Negitive Integers'),
    (CVF_FLOAT, 'Float'),
    (CVF_P_FLOAT, 'Only Positive Float'),
    (CVF_N_FLOAT, 'Only Negitive Float'),
    (CVF_BOOL, 'Boolean'),
    (CVF_DATE, 'Date'),
    (CVF_DATETIME, 'DateTime'),
)












