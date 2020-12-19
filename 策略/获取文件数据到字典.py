import 基本面数据.FundamentalExeclToDict as fetd
from 函数目录 import profile as pf


#################################################
#
#################################################
def getFundamentalDataToDictYear(Type,Year="2014", Length=3, Quarter="3"):
    dirName = pf.GLOBAL_PATH + pf.SEPARATOR + pf.FUNDAMENTAL_DATA + pf.SEPARATOR + Type + pf.SEPARATOR
    instance = fetd.FundamentalExeclToDict(DirName=dirName, Year=Year, Length=Length, Quarter=Quarter)
    instance.getRangeDataYearToDict()
    return instance.OutputDict

#################################################
#
#################################################
def getFundamentalDataToDictYearQuarter(Type,Year="2014", Length=3, Quarter="3"):
    dirName = pf.GLOBAL_PATH + pf.SEPARATOR + pf.FUNDAMENTAL_DATA + pf.SEPARATOR + Type + pf.SEPARATOR
    instance = fetd.FundamentalExeclToDict(DirName=dirName, Year=Year, Length=Length, Quarter=Quarter)
    instance.getRangeDataQuarterToDict()
    return instance.OutputDict