# coding=utf-8
#---------------------------------------------------------------------------
# Copyright 2011 utahta
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#---------------------------------------------------------------------------
import datetime

class QuoteData(object):
    def __init__(self, date, open, high, low, close, volume, adj_close):
        self.date = self._datetime(date) # 日時
        self.open = self._int(open) # 初値
        self.high = self._int(high) # 高値
        self.low = self._int(low) # 安値
        self.close = self._int(close) # 終値
        self.volume = self._int(volume) # 出来高
        self.adj_close = self._int(adj_close) # 調整後終値（株式分割後など）
        self._adjust()
        
    def _adjust(self):
        """株式分割を考慮
        adj_closeが分割後の終値
        """
        rate = self.close / self.adj_close
        if rate > 1:
            self.open /= rate
            self.high /= rate
            self.low /= rate
            self.close /= rate
            self.volume /= rate
    
    def _datetime(self, val):
        if type(val) == datetime.datetime:
            return val
        try:
            return datetime.datetime.strptime(val, '%Y年%m月%d日')
        except ValueError:
            return datetime.datetime.strptime(val, '%Y年%m月')
        except:
            raise # 発生した例外をそのままリレー
        
    def _int(self, val):
        """文字列を数値オブジェクトに変換
        カンマがあったら取り除く（5,400とかのやつ）
        """
        if type(val) == int:
            return val
        return int(val.replace(',', ''))
    
    def __repr__(self):
        """デバッグ文字列
        """
        return "<date:%s open:%s high:%s low:%s close:%s volume:%s adj_close:%s>" % (self.date, self.open, self.high, self.low, self.close, self.volume, self.adj_close)
