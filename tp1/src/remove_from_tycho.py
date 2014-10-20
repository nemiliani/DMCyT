import pandas
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Hierarchic clustering app')
    parser.add_argument('-t', '--tycho_file', type=str, help='tycho data file')
    parser.add_argument('-y', '--hyades_file', type=str, help='hyades data file')
    parser.add_argument('-o', '--output_file', type=str, help='output data file')
    args = parser.parse_args()

    tycho = pandas.read_csv(args.tycho_file, header=0)
    hyades = pandas.read_csv(args.hyades_file, header=0)
    ids = list(hyades['HIP'])
    tycho['keep'] = tycho.apply(lambda x : 0 if x.get('HIP') in ids else 1, axis=1)
    out = tycho[tycho.loc[:, 'keep'] == 1]
    out.to_csv(args.output_file)
    
    
