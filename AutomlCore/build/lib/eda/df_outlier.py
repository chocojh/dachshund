#%%
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

#%%
import pandas as pd
import data_frame
from utils import definitions
from algorithms import outlier

#%%
class DfOutlier(data_frame.DataFrame):
  def __init__(self, _project_name, _csv_filepath):
    self.project_name = _project_name
    self.csv_filepath = _csv_filepath
    self.df = self.__getDroppedColumnDf(_csv_filepath)
    self.__htmlfile_path = None
    self.df_outlier = None

  def __getDroppedColumnDf(self, _csv_filepath):
    df = pd.read_csv(_csv_filepath)
    drop_column_list = []
    for column, dtype in zip(df.columns, df.dtypes):
      if (dtype != 'int64') and (dtype != 'float64'):
        drop_column_list.append(column)
    df = df.drop(drop_column_list, axis=1)
    return df

  def getDataframeHtmlFilePath(self):
    eda_path = definitions.getEdaPath()
    results_path = os.path.join(eda_path, 'results')
    if os.path.exists(results_path) == False:
      os.makedirs(results_path)
    return os.path.join(results_path, (self.project_name + '-outlier.html'))

  def makeDataframeHtmlFile(self):
    if not os.path.exists(self.getDataframeHtmlFilePath()):
      pred_forest = outlier.getIsolationForest(self.df)
      pred_robust = outlier.getRobustCovairance(self.df)
      pred_local = outlier.getLocalFactor(self.df)
      df_result = self.df.copy()
      df_result['forest'] = pred_forest
      df_result['robust'] = pred_robust
      df_result['local'] = pred_local
      self.df_outlier = df_result[(df_result['forest'] == -1) & (df_result['robust'] == -1) & (df_result['local'] == -1)]    
      self.df_outlier[self.df.columns].to_html(self.getDataframeHtmlFilePath(), justify='center')
    else:
      self.df_outlier = pd.read_html(self.getDataframeHtmlFilePath(), index_col=0)

  def getRemovedOutlierDf(self):
    if not os.path.exists(self.getDataframeHtmlFilePath()):
      self.makeDataframeHtmlFile()
    return self.df.drop(self.df_outlier.index, axis=0)

# %%
if __name__ == '__main__':
  rootPath = definitions.getProjectRootPath()
  csv_path = os.path.join(rootPath, 'sample_small.csv')
  outliers = DfOutlier('test1', csv_path)
  outliers.makeDataframeHtmlFile()
  outliers.getRemovedOutlierDf()
# %%


