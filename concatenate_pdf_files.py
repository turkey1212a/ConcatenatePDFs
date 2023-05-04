import PyPDF2
import glob
import sys
import datetime
import os
import pandas as pd


def concatenate_pdf_files(sorce_files_list: list, dst_file_path: str):
    pdf_writer = PyPDF2.PdfWriter()

    for filename in sorce_files_list:
        pdf_reader = PyPDF2.PdfReader(open(filename, "rb"))
        for page in range(len(pdf_reader.pages)):
            pdf_writer.add_page(pdf_reader.pages[page])

    with open(dst_file_path, 'wb') as out_file:
        pdf_writer.write(out_file)


if __name__ == '__main__':
    args = sys.argv

    dt_now = datetime.datetime.now()

    if len(args) < 2:
        input_pdfs = '.'
        output_path = './new_pdf_file.pdf'
    else:
        input_pdfs = args[1]
        if len(args) > 2:
            output_pdf = args[2]
            # コマンドライン引数で与えられた出力がファイルの場合
            if os.path.isfile(output_pdf):
                output_dir = os.path.dirname(output_pdf)
                output_path = output_pdf
            else:
                output_dir = output_pdf
                output_path = f'{output_dir}/new_pdf_file.pdf'
        else:
            output_dir = './out_' + dt_now.strftime('%Y%m%d_%H%M%S')
            output_path = f'{output_dir}/new_pdf_file.pdf'
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

    # 入力がファイルリスト（テキストファイル）の場合
    if os.path.isfile(input_pdfs):
        files = pd.read_csv(input_pdfs, header=None, encoding="shift-jis")
        pdf_files = files.iloc[:, 0]
    # フォルダ下の全PDFファイルを対象とする場合
    else:
        pdf_files = glob.glob(f'{input_pdfs}/*.pdf')

    concatenate_pdf_files(pdf_files, output_path)
