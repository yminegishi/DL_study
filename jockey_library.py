import numpy as np

##################################
# Actually, 0 means padding data #
# so, 1: Others                  #
#     2: 武豊                    #
#     ...                        #
##################################
class create_jocker_vector():
  def __init__(self):
    self.jockey = {}
    self.jockey["武豊"] = 1
    self.jockey["横山典弘"] = 2
    self.jockey["蛯名正義"] = 3
    self.jockey["柴田善臣"] = 4
    self.jockey["福永祐一"] = 5
    self.jockey["四位洋文"] = 6
    self.jockey["岩田康誠"] = 7
    self.jockey["川田将雅"] = 8
    self.jockey["内田博幸"] = 9
    self.jockey["浜中俊"] = 10
    self.jockey["戸崎圭太"] = 11
    self.jockey["ルメール"] = 12
    self.jockey["Ｍデムー"] = 13
    self.jockey["Ｍ．デム"] = 13
    self.jockey["デムーロ"] = 13
    self.jockey["モレイラ"] = 14
    self.jockey["ムーア"] = 14
    self.jockey["ボウマン"] = 14
    self.jockey["Ｃ．デム"] = 14
    self.jockey["オドノヒ"] = 15
    self.jockey["ビュイッ"] = 15
    self.jockey["アヴドゥ"] = 15
    self.jockey["グティエ"] = 15
    self.jockey["ティータ"] = 15
    self.jockey["バルジュ"] = 15
    self.jockey["マーフィ"] = 15
    self.jockey["ミナリク"] = 15
    self.jockey["メンディ"] = 15
    self.jockey["ベリー"] = 15
    self.jockey["フォーリ"] = 15
    self.jockey["マクドノ"] = 15
    self.jockey["バルザロ"] = 15
    self.jockey["シュミノ"] = 15
    self.jockey["アッゼニ"] = 15
    self.jockey["ヴェロン"] = 15
    self.jockey["シュタル"] = 15
    self.jockey["ホワイト"] = 15
    self.jockey["オールプ"] = 15
    self.jockey["コントレ"] = 15
    self.jockey["デュプレ"] = 15
    self.jockey["ウィリア"] = 15
    self.jockey["マカヴォ"] = 15
    self.jockey["クラスト"] = 15
  
  def get_vector(self, jockey_name):
    jockey = 0
    if jockey_name in self.jockey:
      jockey = self.jockey[jockey_name]
    
    return int(jockey)


