import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Box, Typography } from "@mui/material";

export function HelpContent() {
    return (
        <>
            <Box sx={{ padding: 2 }}>
                <ReactMarkdown
                    remarkPlugins={[remarkGfm]}
                    components={{
                        h1: ({ children }) => <Typography variant="h4" gutterBottom>{children}</Typography>,
                        h2: ({ children }) => <Typography variant="h5" gutterBottom sx={{ borderBottom: "thin solid" }}>{children}</Typography>,
                        h3: ({ children }) => <Typography variant="h6" gutterBottom >{children}</Typography>,
                        li: ({ children }) => <Typography component="li" variant="body1">{children}</Typography>,
                        p: ({ children }) => <Typography variant="body1" paragraph>{children}</Typography>,
                    }}
                >
                    {markdownContent}
                </ReactMarkdown>
            </Box >
        </>
    );
};

const markdownContent = `

# parimanaについて

## あらまし
parimanaは、公営競技で、**各出走者の能力**が投票者からどう見積もられているか、公表されているオッズに基づいて算出して示します。  
加えて、各投票券の的中確率と払戻金の期待値も示します。  

## 画面説明

### オッズ出典元

当サイトでの推定の根拠としているオッズの入手元ページへのリンクです。
オッズの入手には以下のサイトを利用しています。
 * **ボートレース**  
 BOAT RACE オフィシャルウェブサイト (https://www.boatrace.jp/)  

 * **競馬**  
 競馬総合情報メディア「netkeiba」(https://www.netkeiba.com/)


### 予想走破時計

オッズから推定された競走能力として、出走者ごとの走破時計の確率分布を示しています。  
推定方法は厳密な計算によるものではなく、ゆるふわです。   

* **＃**   
各出走者の番号（艇番、馬番）です。

* **mean**  
各出走者に期待される走破時計です。ただし、単位は秒ではありません。    
**全出走者の平均を0**としています。この値がマイナスなほど、出走者の好成績が期待されます。  

* **σ**  
各出走者の走破時計の期待の幅を示します。  
走破時計は **70%弱** の確率で、mean **±σ**  の範囲におさまると期待されます。

* **q1**, **q3**  
各出走者の期待される走破時計の第1四分位点、第3四分位点を示します。  
走破時計は **50%** の確率で **q1** ～ **q3** の範囲におさまると期待されます。


### 的中確率と払戻期待値

予想走破時計から算出された、投票券の的中確率と払い戻し額の期待値を示します。  
算出は厳密なものではなく、ゆるふわで誤差があります（大穴の投票券ほど誤差が大きいです）。

* **Betting**  
投票券の買い目です。

* **Type**  
投票券の種類です。意味は次の通りです（競馬の枠連・枠単には対応していません）。
  * **WIN** : 単勝          
  * **PLACE** : 複勝(2着まで) 
  * **SHOW** : 複勝(3着まで) 
  * **EXACTA** : 2連単, 馬単     
  * **QUINELLA** : 2連複, 馬複     
  * **WIDE** : 拡連複, ワイド   
  （なおワイドというのは和製英語の愛称で、正しい英語では quinella placeというそうです）
  * **TRIFECTA** : 3連単     
  * **TRIO** : 3連複   
  

* **Chance**  
その投票券が的中する確率です。

* **Odds**  
投票券のオッズのオッズ出典元からの引用です。  
ただし、複勝（PLACE, SHOW）、拡連複/ワイド（WIDE） のオッズは最大と最小のあいだの適当な値を表示しています。

* **Expectation**  
払い戻し金の期待値です。ChanceとOddsを掛け算した積です。  
購入額の何%が払い戻されるのを期待できるか示しています。  

* **漏斗のマーク**  
式を入力すると、表の内容を絞り込むことができます。  
次に示す式は、オッズが2桁の3連勝単式のみ表示する例です。  
\`Type == 'TRIFECTA' and 10 <= Odds < 100 \`  


## 推定・算出の方法

ちかぢかプログラムソースを公開しようと思っていますのでお待ちください。
なお、AIは使っていません。  


## 当サイトについて

当サイトは個人による非営利の趣味のサイトです。  
事情により、予告なしに停止されたり、閉鎖されたりする可能性があります。

### 免責事項

当サイトが提供する情報の正確性や妥当性は保証されません。  
当サイトの利用によって生じた損害等につきましては、一切責任を負いかねますのでご了承ください。  


### 著作権

* **オッズ**  
当サイトは著作権を持ちません。オッズは、出典元各サイトが公開している情報です。

* **オッズ以外の数値情報（オッズ分析に基づいた推定値、グラフ等）**  
当サイトは著作権を主張しません。これらの数値は当サイトにより算出されたものですが、**著作物としての創作性はない**ためです。ちかぢか算出に用いているプログラムソースが公開されれば、数値やグラフは当サイトでなくてもほんのちょっとの計算機コストで算出可能になるはずです。

* **このページ（ 「parimanaについて」 ）の内容**  
&copy; 2025 渡辺清史


### 連絡先

渡辺清史  
watanabe.kf1983@gmail.com  
https://x.com/watanabe_kf1983  


`
