
import xlrd

class StockList:
    # 初始化
    def __init__(self):
        # 股票代码
        self.StockNumber = ""
        self.filename = ""

    #################################################
    #
    #################################################
    def getStockToList(self):
        workbook = xlrd.open_workbook(self.filename)
        sheet = workbook.sheet_by_index(0)
        rows = sheet.nrows
        cols = sheet.ncols

        for i in range(rows):
            for j in range(cols):
                segments = str(sheet.cell_value(i, j))
                print(segments)

if __name__ == '__main__':
    aa = StockList()
    aa.filename = "C:\量化\基本面数据\股票列表\stocklist.xlsx"
    aa.getStockToList()