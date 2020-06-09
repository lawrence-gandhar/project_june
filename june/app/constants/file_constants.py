#
# AUTHOR : LAWRENCE GANDHAR
# 

#==========================================================================
#   MEMORY UNITS
#==========================================================================
#

MEMORY_UNITS = (
    (0, 'Byte'),
    (1, 'Kilo Byte'),
    (2, 'Mega Byte'),
    (3, 'Giga Byte'),
    (4, 'Tera Byte'),
)

MU_BYTE = 0
MU_KB = 1
MU_MB = 2
MU_GB = 3
MU_TB = 4

#==========================================================================
#   DATATYPES
#==========================================================================
#

DTYPES = (
    (0, 'STRING'),
    (1, 'INTEGERS'),
    (2, 'FLOAT'),
)

DT_STRING = 0
DT_INTEGER = 1
DT_FLOAT = 2

#==========================================================================
#   COLUMN CHECK
#==========================================================================
#

COLUMN_CHECK = (
    (0, 'STRICT'),
    (1, 'MODERATE'),
    (2, 'NO ACTION'),
)

COLC_STRICT = 0
COLC_MODERATE = 1
COLC_NA = 2

#==========================================================================
#   COLUMN CHECK
#==========================================================================
#

COLUMN_VALID_FOR = (
    (0, 'Any'),
    (1, 'Only Alphabets'),
    (2, 'Alphanumeric'),
    (3, 'Integers'),
    (4, 'Only Positive Integers'),
    (5, 'Only Negitive Integers'),
    (6, 'Float'),
    (7, 'Only Positive Float'),
    (8, 'Only Negitive Float'),
    (9, 'Boolean'),
    (10, 'Date'),
    (11, 'DateTime'),
)

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





