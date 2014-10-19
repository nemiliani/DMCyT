import pandas
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Hierarchic clustering app')
    parser.add_argument('-i', '--hipparcos_file', type=str, help='hipparcos data file')
    parser.add_argument('-s', '--hyades_file', type=str, help='hyades data file')
    parser.add_argument('-o', '--output_file', type=str, help='output data file')
    args = parser.parse_args()

    hip = pandas.read_csv(args.hipparcos_file, header=0)
    hya = pandas.read_csv(args.hyades_file, header=0)
    hya_ids = list(hya['cercanaHip'])
    hip['is_hyades'] = hip.apply(lambda x : 1 if x.get('HIP') in hya_ids else 0, axis=1)
    hip.to_csv(args.output_file)
