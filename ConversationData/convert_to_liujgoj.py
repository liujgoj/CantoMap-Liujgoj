import os
import re
import xml.etree.ElementTree as ET
import pandas as pd

def load_syllable_dict(xlsx_path):
    """
    讀取 syllables.xlsx，建立粵拼到溜歌羅馬字嘅嚴格映射詞典
    """
    print(f"正在載入對照表: {xlsx_path}...")
    # 讀取 Excel，假設第一列係 Jyutping，第二列係 Liujgoj
    df = pd.read_excel(xlsx_path, header=None)
    
    # 轉為 Dictionary，並確保全部轉為條理嘅字串同細寫，方便精準匹配
    mapping = {}
    for _, row in df.iterrows():
        jyutping = str(row[0]).strip().lower()
        liujgoj = str(row[1]).strip()
        if jyutping and liujgoj:
            mapping[jyutping] = liujgoj
            
    print(f"成功載入 {len(mapping)} 個音節對照紀錄。")
    return mapping

def convert_text(text, syllable_dict):
    """
    核心替換邏輯：嚴格提取音節，完全匹配後替換，保留其餘符號與空格結構
    """
    if not text:
        return text
    
    # 正則表達式：匹配 [英文字母] 後面緊跟 [數字調號] 的標準粵拼音節
    # 例如：tim4, hong6, nung4, zong1, laa1, m4
    pattern = re.compile(r'([a-zA-Z]+[1-9])')
    
    def replace_match(match):
        token = match.group(1)
        token_lower = token.lower()
        
        # 喺 syllables.xlsx 第一列進行「完全匹配」查找
        if token_lower in syllable_dict:
            return syllable_dict[token_lower]
        
        # 如果對照表無呢個音節，原封不動傳回（例如一啲非標準嘅口語擬聲詞）
        return token

    # 全局搜索並替換
    return pattern.sub(replace_match, text)

def process_eaf_file(file_path, syllable_dict):
    """
    解析單個 EAF 檔案，定位目標 TIER 並替換內容
    """
    try:
        # 為了保留 XML 原始嘅命名空間同縮排結構，使用 ElementTree 解析
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        modified = False
        
        # 遍歷所有 TIER 標籤
        for tier in root.findall(".//TIER"):
            tier_id = tier.get("TIER_ID", "")
            
            # 要求 1：明確只處理包含 -jyutping 嘅層 (如 G-jyutping, E-jyutping, F-jyutping)
            if tier_id.endswith("-jyutping") or tier_id == "jyutping":
                # 搵出呢層下面所有嘅 ANNOTATION_VALUE
                for annotation in tier.findall(".//ANNOTATION_VALUE"):
                    if annotation.text:
                        original_text = annotation.text
                        # 執行轉換
                        converted_text = convert_text(original_text, syllable_dict)
                        
                        if original_text != converted_text:
                            annotation.text = converted_text
                            modified = True
                            
        if modified:
            # 覆寫原本嘅 EAF 檔案（如果你想安全啲，可以改做寫入新檔名）
            tree.write(file_path, encoding='UTF-8', xml_declaration=True)
            print(f"  [成功轉換] {file_path}")
        else:
            print(f"  [無需變更] {file_path}")
            
    except Exception as e:
        print(f"  [❌ 錯誤] 處理檔案 {file_path} 時出錯: {e}")

def main():
    # 確保程序執行在當前腳本所在的目錄
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_dir)
    
    xlsx_file = "syllables.xlsx"
    if not os.path.exists(xlsx_file):
        print(f"❌ 錯誤：喺當前目錄找不到 {xlsx_file} 文件！請確認擺放位置。")
        return
        
    # 1. 載入對照表
    syllable_dict = load_syllable_dict(xlsx_file)
    
    print("\n開始掃描子文件夾內的 EAF 檔案...")
    
    # 2. 遞歸遍歷當前目錄下所有子文件夾內嘅 EAF 文件
    eaf_count = 0
    for root_dir, dirs, files in os.walk("."):
        # 避免掃描 Git 或程序自身的虛擬環境隱藏資料夾
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            if file.lower().endswith(".eaf"):
                file_path = os.path.join(root_dir, file)
                process_eaf_file(file_path, syllable_dict)
                eaf_count += 1
                
    print(f"\n✨ 任務完成！共掃描並處理咗 {eaf_count} 個 EAF 檔案。")

if __name__ == "__main__":
    main()