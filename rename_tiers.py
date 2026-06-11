import os
import xml.etree.ElementTree as ET

# 直接用 "." 代表你目前 PowerShell 踩緊嘅 D:\CantoMap-master 目錄
root_dir = "."

count = 0

# 地毯式遍歷目前目錄下嘅所有子文件夾
for dirpath, _, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.endswith('.eaf'):
            file_path = os.path.join(dirpath, filename)
            
            try:
                # 解析 XML
                tree = ET.parse(file_path)
                root = tree.getroot()
                
                modified = False
                
                # 搵出所有 TIER 標籤並修改 TIER_ID
                for tier in root.findall(".//TIER"):
                    tier_id = tier.get("TIER_ID", "")
                    
                    new_id = tier_id
                    if "jyutping" in tier_id:
                        new_id = tier_id.replace("jyutping", "liujgoj")
                    elif "Jyutping" in tier_id:
                        new_id = tier_id.replace("Jyutping", "Liujgoj")
                    
                    # 如果有變動，就更新
                    if new_id != tier_id:
                        tier.set("TIER_ID", new_id)
                        modified = True
                
                # 如果檔案有被修改，就儲存番低
                if modified:
                    tree.write(file_path, encoding="utf-8", xml_declaration=True)
                    count += 1
                    print(f"[已修改] {filename}")
                    
            except Exception as e:
                print(f"❌ 讀取 {filename} 失敗: {e}")

print(f"\n🎉 成功批量修改咗 {count} 個 EAF 檔案嘅 TIER ID 標籤！")