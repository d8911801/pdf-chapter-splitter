"""
上博楚簡電子書章節分割與歸檔工具
====================================
功能：從 PDF 電子書中按書籤（大綱）分割章節，輸出命名規範的析出 PDF，
      分割後文件直接留在來源目錄，並可歸檔至「依篇目分類」目錄。

命名規則（析出文獻格式）：
  - 同作者：作者：《篇名》，《書名》.pdf
  - 不同作者：暫停詢問

用法：
  python split_ebook_chapters.py

依賴：
  pip install PyPDF2
"""

import PyPDF2
import os
import shutil

# ============================================================
# 配置區：編輯此處以新增／修改書籍
# ============================================================

# 每本書的定義：(書名, 作者, 原始PDF路徑, [(起始頁碼, 章節標題), ...])
# 頁碼為 PDF 顯示頁碼（1-based），非 0-based index
BOOKS = [
    {
        "book_title": "出土文献与早期儒家的美德伦理和政治",
        "author": "王中江",
        "path": r"C:\Users\d8911\WPSDrive\646045039\WPS云盘\電子書（gp22）\6.出土文獻\思想學術\書籍\王中江-出土文献与早期儒家的美德伦理和政治.pdf",
        "chapters": [
            (13, "第一章 「身心合一」之「仁」"),
            (43, "第二章 《性自命出》的人性模式及人道观"),
            (75, "第三章 简帛《五行》篇的「悳」观念"),
            (99, "第四章 早期儒家的「慎独论」"),
            (137, "第五章 《穷达以时》的境遇观"),
            (163, "第六章 儒家经典诠释学的起源"),
            (183, "第七章 上博《诗传》与儒家《诗》教谱系"),
            (201, "第八章 帛书「易传」中的「子曰」和孔子对「德义」的追求"),
            (221, "第九章 《唐虞之道》与王权转移中的多重因素"),
            (243, "第十章 睡虎地秦简《为吏之道》与秦国的儒家"),
        ],
    },
    # 更多書籍按相同格式添加...
]

# 輸出目錄
OUTPUT_DIR = r"C:\Users\d8911\Desktop\上博楚簡_分割章節"

# 歸檔目錄（可選）
ARCHIVE_CHAPTER_DIR = r"C:\Users\d8911\WPSDrive\646045039\WPS云盘\研究\1.主題研究\上博楚簡禮記類文獻思想研究\參考文獻\依篇目分類"


# ============================================================
# 核心函數
# ============================================================

def sanitize_filename(name: str) -> str:
    """清理 Windows 不合法的檔名字元"""
    replacements = {
        ":": "：", "?": "？", "*": "＊", "<": "＜",
        ">": "＞", "|": "｜", "/": "／", "\\": "＼",
        '"': "「", '"': "」",
    }
    for old, new in replacements.items():
        name = name.replace(old, new)
    return name


def split_book(book: dict, output_dir: str) -> list:
    """分割一本書的所有章節，返回產出的檔案路徑列表"""
    if not os.path.exists(book["path"]):
        print(f"  ⚠️ 找不到原始PDF：{book['path']}")
        return []

    reader = PyPDF2.PdfReader(book["path"])
    total_pages = len(reader.pages)
    results = []
    chapters = book["chapters"]

    for i, (start_page, chap_title) in enumerate(chapters):
        # 計算結束頁
        if i < len(chapters) - 1:
            end_page = chapters[i + 1][0] - 1
        else:
            end_page = total_pages

        start_idx = start_page - 1
        end_idx = end_page - 1

        # 生成檔名：作者：《篇名》，《書名》
        fname = f"{book['author']}：《{chap_title}》，《{book['book_title']}》.pdf"
        fname = sanitize_filename(fname)
        out_path = os.path.join(output_dir, fname)

        writer = PyPDF2.PdfWriter()
        for p in range(start_idx, end_idx + 1):
            writer.add_page(reader.pages[p])

        with open(out_path, "wb") as f:
            writer.write(f)

        page_count = end_idx - start_idx + 1
        print(f"  OK  {page_count:>3}頁 → {fname}")
        results.append(out_path)

    return results


def archive_to_chapter_folders(output_dir: str, archive_dir: str):
    """將涉及上博楚簡篇章的 PDF 複製到依篇目分類的子資料夾"""
    print(f"\n歸檔至依篇目分類：{archive_dir}")
    # ... 實現略，參見完整腳本


# ============================================================
# 主流程
# ============================================================

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    all_files = []
    for book in BOOKS:
        print(f"\n{'='*60}")
        print(f"【{book['author']}《{book['book_title']}》】")
        print(f"{'='*60}")
        files = split_book(book, OUTPUT_DIR)
        all_files.extend(files)

    print(f"\n總計分割 {len(all_files)} 個章節，輸出目錄：{OUTPUT_DIR}")


if __name__ == "__main__":
    main()
