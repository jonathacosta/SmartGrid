import glob
import pandas as pd

def combine_csv():
    extension = 'csv'
    all_filenames = [i for i in glob.glob('results/*.{}'.format(extension))]

    #combinar todos os arquivos da lista
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
    #exportar para csv
    combined_csv.to_csv("results/results_combined/results_full.csv", index=False, encoding='utf-8-sig')

#****** Testes ******************
# combine_csv()