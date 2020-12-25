# encoding:utf-8
import sys

#交易数据采集，深圳和上海，有个地方需要改，0和1的关系
#http://12.push2his.eastmoney.com/api/qt/stock/kline/get?cb=jQuery1124019585994690087272_1607051333177&secid=1.600663&ut=fa5fd1943c7b386f172d6893dbfba10b&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60%2Cf61&klt=101&fqt=2&end=20201204&lmt=120000&_=1607051333337

GLOBAL_PATH = '/home/wangleisldt/collect_data'
SEPARATOR = "/"
#两个后缀文件的结尾
Execl = ".xlsx"
PklFile = ".pkl"
GZ = '.gz'

#采集的时候是否使用代理服务器
proxies = None
'''
proxies = {
    'http':'http://10.5.22.68:8118',
    'https':'https://10.5.22.68:8118'
}
'''
#'http':'http://用户名:密码@IP:端口号',
#'https':'https://用户名:密码@IP:端口号'



#数据库的连接串
DATABASE_STRING_沪深港通持股 = 'sqlite:////home/wangleisldt/collect_data/sqlite3/hsgtcg.db'

#基本面数据相关目录常量
FUNDAMENTAL_DATA = "基本面数据"

PerformanceReport = "业绩报告（主表）"
ProfitAbility = "盈利能力"
OperationCapacity = "营运能力"
GrowthAbility = "成长能力"
DebtPayingAbility = "偿债能力"
CashFlow = "现金流量"

FinancialIndex = '财务指标'
BalanceSheet = '资产负债表'
CashFlowSheet = '现金流量表'
CompanyProfitStatement = '公司利润表'

#股票列表目录、文件常量
StockList = "股票列表"
StockListFilename = "stocklist"

#一些表头
股票清单表头 = ['股票代码', '股票名称', '最新价', '涨跌幅', '涨跌额', '成交量(手)', '成交额', '振幅', '最高', '最低', '今开', '昨收', '量比' , '换手率', '市盈率(动态)', '市净率', '总市值', '流通市值', '60日涨跌幅', '年初至今涨跌幅', '上市日期','交易市场',]
股票日交易表头 = [  '日期', '开盘', '收盘', '最高', '最低',  '成交量', '成交额','振幅', '涨跌幅', '涨跌额', '换手率']

#交易数据目录常量
TransactionData = "交易数据"
交易数据 = "交易数据"

#投资者关系活动记录表
投资者关系活动记录表="投资者关系活动记录表"
原始数据 = "原始数据"
汇总数据 = "汇总数据"
展现数据 = "展现数据"
单个汇总 = "单个汇总"
要去除的字符串组 = ['参与单位','人员姓名','□','√','对象调研','现场参观']

#沪深港通持股
沪深港通持股 = '沪深港通持股'
步骤一 = '步骤一'
步骤二 = '步骤二'
步骤三 = '步骤三'
步骤四 = '步骤四'


#老行情数据
HistoryData = "历史行情"
RehabilitationOfHistoricalData = "复权数据"
Qfq = "qfq"
Hfq = "hfq"


RealtimeQuotesData = "实时行情"
StockRealtimeQuotesDataFilename = "StockRealtimeQuotes"

#行情数据
历史行情 = "历史行情"
#前复权 = "前复权"
后复权 = "后复权"



AfterFinishingData = "整理后的数据目录"


###################################################################

P_TYPE = {'http': 'http://', 'ftp': 'ftp://'}

#采集的link
#http://money.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/000001/ctrl/2017/displaytype/4.phtml
财务指标_URL = '%smoney.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/%s/ctrl/%s/displaytype/%s.phtml'
#http://money.finance.sina.com.cn/corp/go.php/vFD_BalanceSheet/stockid/000952/ctrl/2016/displaytype/4.phtml
资产负债表_URL = '%smoney.finance.sina.com.cn/corp/go.php/vFD_BalanceSheet/stockid/%s/ctrl/%s/displaytype/%s.phtml'
#http://money.finance.sina.com.cn/corp/go.php/vFD_CashFlow/stockid/000952/ctrl/2016/displaytype/4.phtml
现金流量表_URL = '%smoney.finance.sina.com.cn/corp/go.php/vFD_CashFlow/stockid/%s/ctrl/%s/displaytype/%s.phtml'
#http://money.finance.sina.com.cn/corp/go.php/vFD_ProfitStatement/stockid/000001/ctrl/2016/displaytype/4.phtml
公司利润表_URL = '%smoney.finance.sina.com.cn/corp/go.php/vFD_ProfitStatement/stockid/%s/ctrl/%s/displaytype/%s.phtml'

DATA_GETTING_TIPS = '[Getting data:]'
DATA_GETTING_FLAG = '#'

def _write_head():
    sys.stdout.write(DATA_GETTING_TIPS)
    sys.stdout.flush()

def _write_console():
    sys.stdout.write(DATA_GETTING_FLAG)
    sys.stdout.flush()

def _write_msg(msg):
    sys.stdout.write(msg)
    sys.stdout.flush()



DATE_CHK_MSG = '年度输入错误：请输入1989年以后的年份数字，格式：YYYY'
DATE_CHK_Q_MSG = '季度输入错误：请输入1、2、3或4数字'

def _check_input(year, quarter):
    if isinstance(year, str) or year < 1989 :
        raise TypeError(DATE_CHK_MSG)
    elif quarter is None or isinstance(quarter, str) or quarter not in [1, 2, 3, 4]:
        raise TypeError(DATE_CHK_Q_MSG)
    else:
        return True


#季度文件和时间的转换
End_OF_SEASON_DAY = {1: '-03-31', 2: '-06-30', 3: '-09-30', 4: '-12-31'}



